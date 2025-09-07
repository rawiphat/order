require("dotenv").config();
const fs = require("fs");
const { 
    Client, 
    GatewayIntentBits, 
    EmbedBuilder, 
    ChannelType, 
    PermissionsBitField 
} = require("discord.js");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildBans
    ]
});

// --- ฟังก์ชันช่วยตัดข้อความยาวเกิน 1024 ---
const truncate = (str, max = 1024) => str?.length > max ? str.slice(0, max - 3) + "..." : str;

// --- โหลด logChannels.json เพื่อใช้ ID ล็อคห้อง log ---
const LOG_FILE = "./logChannels.json";
let logChannelsData = {};
if (fs.existsSync(LOG_FILE)) {
    logChannelsData = JSON.parse(fs.readFileSync(LOG_FILE, "utf8"));
}
client.logChannels = logChannelsData;

// --- ฟังก์ชันบันทึก logChannels ลงไฟล์ ---
const saveLogChannels = () => {
    fs.writeFileSync(LOG_FILE, JSON.stringify(client.logChannels, null, 2));
};

// --- ตอนบอทพร้อม ---
client.once("ready", async () => {
    console.log(`✅ Logged in as ${client.user.tag}`);

    for (const guild of client.guilds.cache.values()) {
        try {
            // Fetch bot member เพื่อเช็ค permissions
            await guild.members.fetch(client.user.id);
            if (!guild.members.me.permissions.has(PermissionsBitField.Flags.Administrator)) {
                console.log(`❌ Bot missing Admin permission in ${guild.name}`);
                continue;
            }

            // ตรวจว่ามี Category หรือยัง
            let category = guild.channels.cache.find(
                c => c.name.includes("🤖┃ บอท & ระบบ") && c.type === ChannelType.GuildCategory
            );

            if (category) {
                const canManage = guild.members.me.permissionsIn(category).has(PermissionsBitField.Flags.ManageChannels);
                if (!canManage) {
                    console.log(`❌ Cannot use category "${category.name}" in ${guild.name}, missing permission. Will create a new one.`);
                    category = null;
                }
            }

            if (!category) {
                category = await guild.channels.create({
                    name: "🤖┃ บอท & ระบบ",
                    type: ChannelType.GuildCategory
                });
                console.log(`📂 Created new category in ${guild.name}`);
            }

            // --- กำหนดห้อง log ที่ต้องมี ---
            const logChannelsList = [
                { key: "logMessage", name: "📝┃log-ข้อความ", type: ChannelType.GuildText },
                { key: "logMember", name: "🛡️┃log-สมาชิก", type: ChannelType.GuildText },
                { key: "logBan", name: "⚔️┃log-แบน", type: ChannelType.GuildText }
            ];

            client.logChannels[guild.id] = client.logChannels[guild.id] || {};

            for (const ch of logChannelsList) {
                let exists = null;
                // เช็คว่า ID ล็อคไว้แล้วหรือยัง
                const lockedId = client.logChannels[guild.id][ch.key];
                if (lockedId) {
                    exists = guild.channels.cache.get(lockedId);
                    if (!exists) {
                        console.log(`⚠️ Locked channel ID ${lockedId} not found in ${guild.name}. Will create new.`);
                    }
                }

                if (!exists) {
                    try {
                        exists = await guild.channels.create({
                            name: ch.name,
                            type: ch.type,
                            parent: category?.id,
                            permissionOverwrites: [
                                { id: guild.roles.everyone.id, deny: [PermissionsBitField.Flags.SendMessages] },
                                { id: client.user.id, allow: [PermissionsBitField.Flags.SendMessages, PermissionsBitField.Flags.ViewChannel] }
                            ]
                        });
                        console.log(`✅ Created channel ${ch.name} in ${guild.name}`);
                        client.logChannels[guild.id][ch.key] = exists.id;
                        saveLogChannels(); // บันทึก ID ล็อค
                    } catch (err) {
                        console.log(`❌ Failed to create channel ${ch.name} in ${guild.name}: ${err.message}`);
                    }
                }
            }
        } catch (e) {
            console.log(`❌ Error initializing guild ${guild.name}: ${e.message}`);
        }
    }
});

// ---------- LOG: ข้อความถูกลบ ----------
client.on("messageDelete", async (message) => {
    if (!message.guild || message.author?.bot) return;

    const logId = client.logChannels?.[message.guild.id]?.logMessage;
    const logChannel = logId && message.guild.channels.cache.get(logId);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: message.author.tag, iconURL: message.author.displayAvatarURL() })
        .setDescription(`🗑 **Message deleted in** ${message.channel}`)
        .addFields(
            { name: "Message Content", value: truncate(message.content) || "ไม่มีข้อความ" },
            { name: "Message ID", value: message.id },
            { name: "Author ID", value: message.author.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id } // แสดง ID ของ log channel
        )
        .setColor("Red")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ---------- LOG: ข้อความถูกแก้ไข ----------
client.on("messageUpdate", async (oldMessage, newMessage) => {
    if (!oldMessage.guild || oldMessage.author?.bot) return;
    if (oldMessage.content === newMessage.content) return;

    const logId = client.logChannels?.[oldMessage.guild.id]?.logMessage;
    const logChannel = logId && oldMessage.guild.channels.cache.get(logId);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: oldMessage.author.tag, iconURL: oldMessage.author.displayAvatarURL() })
        .setDescription(`✏️ **Message edited in** ${oldMessage.channel}`)
        .addFields(
            { name: "Before", value: truncate(oldMessage.content) || "ไม่มีข้อความ" },
            { name: "After", value: truncate(newMessage.content) || "ไม่มีข้อความ" },
            { name: "Message ID", value: oldMessage.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id }
        )
        .setColor("Orange")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ---------- LOG: สมาชิกเข้า ----------
client.on("guildMemberAdd", async (member) => {
    const logId = client.logChannels?.[member.guild.id]?.logMember;
    const logChannel = logId && member.guild.channels.cache.get(logId);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: member.user.tag, iconURL: member.user.displayAvatarURL() })
        .setDescription(`✅ **Member joined:** ${member}`)
        .addFields(
            { name: "User ID", value: member.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id }
        )
        .setColor("Green")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ---------- LOG: สมาชิกออก ----------
client.on("guildMemberRemove", async (member) => {
    const logId = client.logChannels?.[member.guild.id]?.logMember;
    const logChannel = logId && member.guild.channels.cache.get(logId);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: member.user.tag, iconURL: member.user.displayAvatarURL() })
        .setDescription(`❌ **Member left:** ${member.user.tag}`)
        .addFields(
            { name: "User ID", value: member.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id }
        )
        .setColor("DarkGrey")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ---------- LOG: การแบน ----------
client.on("guildBanAdd", async (ban) => {
    const logId = client.logChannels?.[ban.guild.id]?.logBan;
    const logChannel = logId && ban.guild.channels.cache.get(logId);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: ban.user.tag, iconURL: ban.user?.displayAvatarURL() || null })
        .setDescription(`⚔️ **User banned**`)
        .addFields(
            { name: "User", value: ban.user.tag },
            { name: "User ID", value: ban.user.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id }
        )
        .setColor("DarkRed")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

client.login(process.env.DISCORD_TOKEN);
