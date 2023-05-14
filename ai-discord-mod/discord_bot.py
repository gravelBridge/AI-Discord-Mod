import discord
from discord.ext import commands, tasks
from ai_discord_functions import image_is_safe, message_is_safe
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

warning_list={}

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MUTE_TIME = os.getenv("MUTE_TIME")
WARNINGS = os.getenv("WARNINGS")
USE_TRIGGERING_WORDS = os.getenv("USE_TRIGGERING_WORDS")

if USE_TRIGGERING_WORDS == "True":
    TRIGGERING_WORDS_FILE = os.getenv("TRIGGERING_WORDS")
    if TRIGGERING_WORDS_FILE:
        with open(TRIGGERING_WORDS_FILE, "r") as file:
            TRIGGERING_WORDS = file.read().split(",")
    else:
        TRIGGERING_WORDS = []
else:
    TRIGGERING_WORDS = []

if not BOT_TOKEN or not OPENAI_API_KEY:
    print("You did not set your .env file correctly.")
    exit()


async def tempmute(ctx, member: discord.Member=None, time=None):
    guild = ctx.guild
    reason = f"sending more than {WARNINGS} inappropriate messages."
    bot_member = guild.get_member(bot_id)
    try:
        seconds = int(time[:-1])
        duration = time[-1]
        if duration == "s":
            seconds = seconds * 1
        elif duration == "m":
            seconds = seconds * 60
        elif duration == "h":
            seconds = seconds * 60 * 60
        elif duration == "d":
            seconds = seconds * 86400
        else:
            await ctx.send("Invalid duration input")
            return
    except Exception as e:
        print(e)
        await ctx.send("Invalid duration input")
        return

    Muted = discord.utils.get(guild.roles, name="Muted")
    if not Muted:
        Muted = await guild.create_role(name="Muted")
        all_roles = await guild.fetch_roles()
        for i in range(len(all_roles)):
            if all_roles[i] in [y for y in bot_member.roles]:
                role_of_muted = len(all_roles)-i-1
        await Muted.edit(reason=None, position=role_of_muted)
        for channel in guild.channels:
            await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(Muted, reason=reason)
    muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by AI-Moderator for {reason} Muted for {time}.")
    await ctx.send(embed=muted_embed)
    await asyncio.sleep(seconds)
    await member.remove_roles(Muted)
    unmute_embed = discord.Embed(title="Mute over!", description=f'AI-Moderator muted {member.mention} for {reason} Is over after {time}')
    await ctx.send(embed=unmute_embed)


class AI_Discord(discord.Client):
    async def on_ready(self):
        global bot_id
        bot_id = self.user.id
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        sent_message = message

        if message.author.id == self.user.id:
            return
        if USE_TRIGGERING_WORDS == "True":
            if not any(map(message.content.__contains__, TRIGGERING_WORDS)):
                return
            else:
                print("Triggering word found in the filter, sending to OpenAI...")

        if message.attachments:
            attachments = message.attachments
            for attachment in attachments:
                if attachment.content_type.startswith("image"):
                    await attachment.save("toModerate.jpeg")
                    result = await image_is_safe()

                    if not result:
                        await sent_message.delete()
                        print("Deleted a message with an inappropriate image. The message was sent from " + str(sent_message.author.id))
                        if sent_message.author.id in warning_list:
                            warning_list[sent_message.author.id] += 1
                            if warning_list[sent_message.author.id] >= int(WARNINGS):
                                await tempmute(sent_message.channel, sent_message.author, MUTE_TIME)
                                warning_list[sent_message.author.id] = 0
                        else:
                            warning_list[sent_message.author.id] = 1
                        await sent_message.channel.send("Deleted " + sent_message.author.mention + "'s image because it was inappropriate. " + sent_message.author.mention + " has " + str(int(WARNINGS) -  warning_list[sent_message.author.id]) + " warnings left.")
                        return
        
        if await(message_is_safe(message.content, OPENAI_API_KEY)):
            await sent_message.delete()
            print("Deleted an inappropriate message. The message was sent from " + str(sent_message.author.id))

            if sent_message.author.id in warning_list:
                warning_list[sent_message.author.id] += 1
                if warning_list[sent_message.author.id] >= int(WARNINGS):
                    await tempmute(sent_message.channel, sent_message.author, MUTE_TIME)
                    warning_list[sent_message.author.id] = 0
            else:
                warning_list[sent_message.author.id] = 1
            await sent_message.channel.send("Deleted " + sent_message.author.mention + "'s message because it was inappropriate. " + sent_message.author.mention + " has " + str(int(WARNINGS) -  warning_list[sent_message.author.id]) + " warnings left.")



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = AI_Discord(intents=intents)
client.run(BOT_TOKEN)
