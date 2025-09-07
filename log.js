require("dotenv").config();
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

client.once("ready", async () => {
    console.log(`✅ Logged in as ${client.user.tag}`);

    client.guilds.cache.forEach(async guild => {
        // ตรวจว่ามี Category "🤖┃ บอท & ระบบ" หรือยัง
        let category = guild.channels.cache.find(
            c => c.name.includes("🤖┃ บอท & ระบบ") && c.type === ChannelType.GuildCategory
        );

        if (!category) {
            category = await guild.channels.create({
                name: "🤖┃ บอท & ระบบ",
                type: ChannelType.GuildCategory
            });
            console.log(`📂 สร้างหมวดหมู่ใหม่ใน ${guild.name}`);
        }

        // ห้องที่ต้องมี
        const logChannels = [
            { key: "logMessage", name: "📝┃log-ข้อความ", type: ChannelType.GuildText },
            { key: "logMember", name: "🛡️┃log-สมาชิก", type: ChannelType.GuildText },
            { key: "logBan", name: "⚔️┃log-แบน", type: ChannelType.GuildText }
        ];

        client.logChannels = client.logChannels || {};
        client.logChannels[guild.id] = {};

        for (const ch of logChannels) {
            let exists = guild.channels.cache.find(c => c.name === ch.name);
            if (!exists) {
                exists = await guild.channels.create({
                    name: ch.name,
                    type: ch.type,
                    parent: category.id,
                    permissionOverwrites: [
                        {
                            id: guild.roles.everyone.id,
                            deny: [PermissionsBitField.Flags.SendMessages] // ห้ามพิมพ์ในห้อง log
                        }
                    ]
                });
                console.log(`✅ สร้างห้อง ${ch.name} ใน ${guild.name}`);
            }
            client.logChannels[guild.id][ch.key] = exists.id;
        }
    });
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
            { name: "Message Content", value: message.content || "ไม่มีข้อความ" },
            { name: "Message ID", value: message.id },
            { name: "Author ID", value: message.author.id }
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
            { name: "Before", value: oldMessage.content || "ไม่มีข้อความ" },
            { name: "After", value: newMessage.content || "ไม่มีข้อความ" },
            { name: "Message ID", value: oldMessage.id }
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
        .addFields({ name: "User ID", value: member.id })
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
        .addFields({ name: "User ID", value: member.id })
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
        .setAuthor({ name: ban.user.tag, iconURL: ban.user.displayAvatarURL() })
        .setDescription(`⚔️ **User banned**`)
        .addFields(
            { name: "User", value: ban.user.tag },
            { name: "User ID", value: ban.user.id }
        )
        .setColor("DarkRed")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

client.login(process.env.DISCORD_TOKEN);
