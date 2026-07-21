import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Server giả giúp Render không bị lỗi Port Timeout
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
    print(f"🤖 Bot {bot.user} đã online thành công!")

# --- Danh sách các lệnh ---
@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

# Lệnh print siêu linh hoạt (không lo lỗi cú pháp/dấu ngoặc)
@bot.command()
async def print(ctx, *, text: str = None):
    if text is None:
        await ctx.send("⚠️ Bạn chưa nhập nội dung! Ví dụ: `!print gay`")
        return
    
    # Cắt sạch các loại dấu ngoặc nếu lỡ gõ vào
    cleaned = text.strip().strip('()').strip('"\'“”')
    
    if cleaned:
        await ctx.send(cleaned)
    else:
        await ctx.send("⚠️ Nội dung trống rồi bạn ơi!")

token = os.environ.get('BOT_TOKEN')
bot.run(token)
