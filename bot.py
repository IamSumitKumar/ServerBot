import discord
from discord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"  # Prefix for commands

# Initialize Bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Welcome Message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! Enjoy your stay!")

# Farewell Message
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"{member.mention} has left the server. We'll miss you!")

# Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

# Kick Command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked. Reason: {reason}")

# Ban Command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned. Reason: {reason}")

# Joke Command
@bot.command()
async def joke(ctx):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the chicken join a band? Because it had the drumsticks!",
    ]
    await ctx.send(random.choice(jokes))

# Play Music Command
@bot.command()
async def play(ctx, url: str):
    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()
    ctx.voice_client.stop()
    await ctx.send(f"Playing: {url}")

# Weather Command
@bot.command()
async def weather(ctx, city: str):
    # Replace this with an actual API integration for real-time weather
    fake_weather = f"The weather in {city} is sunny with a temperature of 25°C."
    await ctx.send(fake_weather)

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist.")
    else:
        await ctx.send("An error occurred.")

# Run the Bot
bot.run(TOKEN)
