import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Server giả giữ cho Render không bị Port Scan Timeout
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

# 2. Khởi tạo Discord Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã online!")

# --- DANH SÁCH LỆNH ---
@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

# Lệnh print nhận cả gõ dính !print("a") lẫn gõ cách !print ("a")
@bot.command()
async def print(ctx, *, text: str = None):
    if not text:
        await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')
        return
    
    # Dùng Regex lọc lấy chính xác chữ nằm trong ("...") hoặc ('...')
    match = re.search(r'^\s*\(\s*["\'“”](.*?)["\'“”]\s*\)\s*$', text)
    
    if match:
        content = match.group(1)
        await ctx.send(content)
    else:
        await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
