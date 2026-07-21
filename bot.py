import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Web server giả (tránh Render bị Port Timeout)
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

# 2. Khởi tạo Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã online!")

# --- Các lệnh cơ bản ---
@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

# Lệnh print BẮT BUỘC cú pháp ("...")
@bot.command()
async def print(ctx, *, text: str = None):
    if text is None:
        await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')
        return
    
    text = text.strip()
    
    # Kiểm tra dấu ( mở đầu và ) kết thúc
    if text.startswith('(') and text.endswith(')'):
        inner = text[1:-1].strip()
        
        # Kiểm tra dấu ngoặc kép bên trong (chấp nhận cả " ' “ ”)
        if (inner.startswith('"') and inner.endswith('"')) or \
           (inner.startswith("'") and inner.endswith("'")) or \
           (inner.startswith('“') and inner.endswith('”')) or \
           (inner.startswith('“') and inner.endswith('“')) or \
           (inner.startswith('”') and inner.endswith('”')):
            
            content = inner[1:-1]
            await ctx.send(content)
            return
            
    # Nếu gõ thiếu ngoặc hoặc sai dạng -> Báo lỗi
    await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
