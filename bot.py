import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã online trên Render 24/24!")

@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

@bot.command()
async def print(ctx, *, text: str):
    if text.startswith('("') and text.endswith('")'):
        content = text[2:-2]
        await ctx.send(content)
    elif text.startswith("('") and text.endswith("')"):
        content = text[2:-2]
        await ctx.send(content)
    else:
        await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')

# Render sẽ tự đọc TOKEN từ biến môi trường
token = os.environ.get('BOT_TOKEN')
bot.run(token)
