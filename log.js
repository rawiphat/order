import "dotenv/config";
import fetch from "node-fetch";
import { Client, GatewayIntentBits, EmbedBuilder } from "discord.js";

// ---------------- Discord Bot ----------------
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildBans
    ]
});

// ---------------- Env Variables ----------------
const GUILD_ID = process.env.GUILD_ID;
const LOG_CHANNELS = {
    logMessage: process.env.LOG_MESSAGE_CHANNEL,
    logMember: process.env.LOG_MEMBER_CHANNEL,
    logBan: process.env.LOG_BAN_CHANNEL
};

// ---------------- Helper ----------------
const truncate = (str, max = 1024) => str?.length > max ? str.slice(0, max - 3) + "..." : str;

// ---------------- Keep Alive Self Ping ทุก 10 วินาที ----------------
if (process.env.SELF_PING_URL) {
    setInterval(async () => {
        try {
            await fetch(process.env.SELF_PING_URL);
            console.log("🌐 Pinged self to stay alive");
        } catch (err) {
            console.error("❌ Ping failed", err);
        }
    }, 10 * 1000); // ทุก 10 วินาที
}

// ---------------- Event Handlers ----------------
client.once("ready", () => {
    console.log(`✅ Logged in as ${client.user.tag}`);
});

// Message Delete
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

// Message Update
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

// Member Join
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

// Member Leave
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

// Guild Ban
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
