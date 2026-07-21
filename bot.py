import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Server giả giữ cho Render không bị Port Timeout
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

# 3. Lắng nghe mọi tin nhắn (Bắt được cả dính liền lẫn có khoảng cách)
@bot.event
async def on_message(message):
    # Không phản hồi tin nhắn của chính bot
    if message.author == bot.user:
        return

    content = message.content.strip()

    # Xử lý riêng cho lệnh !print
    if content.startswith("!print"):
        # Lấy phần còn lại đằng sau chữ !print
        rest = content[6:].strip()
        
        # Lọc đúng cú pháp ("nội dung") hoặc ('nội dung')
        match = re.search(r'^\(\s*["\'“”](.*?)["\'“”]\s*\)$', rest)
        if match:
            text_to_send = match.group(1)
            await message.channel.send(text_to_send)
        else:
            await message.channel.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')
        return

    # Để các lệnh khác (!hi, !khen, !gay) vẫn chạy bình thường
    await bot.process_commands(message)

# --- CÁC LỆNH KHÁC ---
@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

token = os.environ.get('BOT_TOKEN')
bot.run(token)
