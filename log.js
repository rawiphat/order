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

// โหลดเลขห้องจาก env
const GUILD_ID = process.env.GUILD_ID;
const LOG_CHANNELS = {
    logMessage: process.env.LOG_MESSAGE_CHANNEL,
    logMember: process.env.LOG_MEMBER_CHANNEL,
    logBan: process.env.LOG_BAN_CHANNEL
};

// ฟังก์ชันช่วยตัดข้อความยาวเกิน 1024 ตัวอักษร
const truncate = (str, max = 1024) => str?.length > max ? str.slice(0, max - 3) + "..." : str;

client.once("ready", async () => {
    console.log(`✅ Logged in as ${client.user.tag}`);

    const guild = client.guilds.cache.get(GUILD_ID);
    if (!guild) {
        console.log(`❌ Guild with ID ${GUILD_ID} not found`);
        return;
    }

    try {
        // ตรวจ bot permissions
        await guild.members.fetch(client.user.id);
        if (!guild.members.me.permissions.has(PermissionsBitField.Flags.Administrator)) {
            console.log(`❌ Bot missing Admin permission in ${guild.name}`);
            return;
        }

        // ตรวจ category "🤖┃ บอท & ระบบ" (ไม่สร้างใหม่)
        const category = guild.channels.cache.find(
            c => c.name === "🤖┃ บอท & ระบบ" && c.type === ChannelType.GuildCategory
        );
        if (!category) {
            console.log(`⚠️ Warning: Category "🤖┃ บอท & ระบบ" not found. No new category will be created.`);
        }

        // ตรวจห้อง log แต่ละประเภท ตาม ID ใน env (ไม่สร้างใหม่)
        for (const [key, channelId] of Object.entries(LOG_CHANNELS)) {
            const ch = guild.channels.cache.get(channelId);
            if (!ch) {
                console.log(`⚠️ Warning: Channel ID for ${key} not found in guild. No new channel will be created.`);
            }
        }

        console.log(`✅ Guild initialization completed for ${guild.name}`);
    } catch (err) {
        console.log(`❌ Error initializing guild ${guild.name}: ${err.message}`);
    }
});

// ------------------ EVENT LOGS ------------------

// ข้อความถูกลบ
client.on("messageDelete", async (message) => {
    if (!message.guild || message.author?.bot) return;
    if (message.guild.id !== GUILD_ID) return;

    const logChannel = message.guild.channels.cache.get(LOG_CHANNELS.logMessage);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: message.author.tag, iconURL: message.author.displayAvatarURL() })
        .setDescription(`🗑 **Message deleted in** ${message.channel}`)
        .addFields(
            { name: "Message Content", value: truncate(message.content) || "ไม่มีข้อความ" },
            { name: "Message ID", value: message.id },
            { name: "Author ID", value: message.author.id },
            { name: "LOG_CHANNEL_ID", value: logChannel.id }
        )
        .setColor("Red")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ข้อความถูกแก้ไข
client.on("messageUpdate", async (oldMessage, newMessage) => {
    if (!oldMessage.guild || oldMessage.author?.bot) return;
    if (oldMessage.guild.id !== GUILD_ID) return;
    if (oldMessage.content === newMessage.content) return;

    const logChannel = oldMessage.guild.channels.cache.get(LOG_CHANNELS.logMessage);
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

// สมาชิกเข้า
client.on("guildMemberAdd", async (member) => {
    if (member.guild.id !== GUILD_ID) return;
    const logChannel = member.guild.channels.cache.get(LOG_CHANNELS.logMember);
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

// สมาชิกออก
client.on("guildMemberRemove", async (member) => {
    if (member.guild.id !== GUILD_ID) return;
    const logChannel = member.guild.channels.cache.get(LOG_CHANNELS.logMember);
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

// การแบน
client.on("guildBanAdd", async (ban) => {
    if (ban.guild.id !== GUILD_ID) return;
    const logChannel = ban.guild.channels.cache.get(LOG_CHANNELS.logBan);
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
