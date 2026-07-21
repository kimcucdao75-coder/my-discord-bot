import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# Server giả giúp Render không bị lỗi Port Scan Timeout
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã online!")

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
        await ctx.send(text[2:-2])
    elif text.startswith("('") and text.endswith("')"):
        await ctx.send(text[2:-2])
    else:
        await ctx.send('⚠️ Sai cú pháp! Dùng dạng: `!print("nội dung")`')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
