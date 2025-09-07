require("dotenv").config();
const { 
    Client, 
    GatewayIntentBits, 
    EmbedBuilder 
} = require("discord.js");

const TOKEN = process.env.DISCORD_TOKEN;
const LOG_CHANNEL_ID = process.env.LOG_CHANNEL_ID;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.MessageContent
    ]
});

client.once("ready", () => {
    console.log(`✅ Logged in as ${client.user.tag}`);
});

// ---------------------- LOG: ข้อความถูกลบ ----------------------
client.on("messageDelete", async (message) => {
    if (!message.guild || message.author?.bot) return;
    const logChannel = message.guild.channels.cache.get(LOG_CHANNEL_ID);
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

// ---------------------- LOG: ข้อความถูกแก้ไข ----------------------
client.on("messageUpdate", async (oldMessage, newMessage) => {
    if (!oldMessage.guild || oldMessage.author?.bot) return;
    if (oldMessage.content === newMessage.content) return;

    const logChannel = oldMessage.guild.channels.cache.get(LOG_CHANNEL_ID);
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

// ---------------------- LOG: สมาชิกเข้า ----------------------
client.on("guildMemberAdd", async (member) => {
    const logChannel = member.guild.channels.cache.get(LOG_CHANNEL_ID);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: member.user.tag, iconURL: member.user.displayAvatarURL() })
        .setDescription(`✅ **Member joined:** ${member}`)
        .addFields(
            { name: "User ID", value: member.id }
        )
        .setColor("Green")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

// ---------------------- LOG: สมาชิกออก ----------------------
client.on("guildMemberRemove", async (member) => {
    const logChannel = member.guild.channels.cache.get(LOG_CHANNEL_ID);
    if (!logChannel) return;

    const embed = new EmbedBuilder()
        .setAuthor({ name: member.user.tag, iconURL: member.user.displayAvatarURL() })
        .setDescription(`❌ **Member left:** ${member.user.tag}`)
        .addFields(
            { name: "User ID", value: member.id }
        )
        .setColor("DarkGrey")
        .setTimestamp();

    logChannel.send({ embeds: [embed] });
});

client.login(TOKEN);
