import os
import re
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
from discord.ui import Button, View

# --- 1. WEB SERVER GIẢ (CHỐNG RENDER TIMEOUT) ---
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

# --- 2. KHỞI TẠO BOT ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None) # Tắt help mặc định

wallets = {}

def get_balance(user_id):
    if user_id not in wallets:
        wallets[user_id] = 1000  # Tặng sẵn 1,000 xu vốn khởi nghiệp
    return wallets[user_id]

def update_balance(user_id, amount):
    wallets[user_id] = get_balance(user_id) + amount

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã sẵn sàng hoạt động!")

# --- 3. LẮNG NGHE LỆNH PRINT DÍNH LIỀN ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()

    # Bắt riêng cú pháp !print(...)
    if content.startswith("!print"):
        rest = content[6:].strip()
        match = re.search(r'^\(\s*["\'“”](.*?)["\'“”]\s*\)$', rest)
        if match:
            text_to_send = match.group(1)
            await message.channel.send(text_to_send)
        else:
            await message.channel.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')
        return

    await bot.process_commands(message)

# --- 4. LỆNH HELP HƯỚNG DẪN CHI TIẾT ---
@bot.command(aliases=['trogiup', 'h'])
async def help(ctx):
    embed = discord.Embed(
        title="📚 HƯỚNG DẪN SỬ DỤNG BOT",
        description="Dưới đây là danh sách toàn bộ các lệnh bạn có thể dùng:",
        color=discord.Color.blue()
    )

    # Nhóm Lệnh Cơ Bản
    embed.add_field(
        name="💬 **Lệnh Cơ Bản**",
        value="• `!hi` - Chào hỏi bot\n"
              "• `!khen` - Khen chủ bot depzai\n"
              "• `!gay` - Kiểm tra độ gay\n"
              "• `!print("nội dung")` - In chuỗi ra màn hình (bắt buộc đúng ngoặc)",
        inline=False
    )

    # Nhóm Kinh Tế & Xu
    embed.add_field(
        name="💰 **Ví Tiền & Kiếm Xu**",
        value="• `!cash` (hoặc `!bal`) - Xem số xu hiện đang có\n"
              "• `!daily` - Báo danh nhận 500 xu mỗi ngày\n"
              "• `!work` - Đi làm việc kiếm xu ngẫu nhiên\n"
              "• `!beg` - Xin tiền người qua đường (hên xui)\n"
              "• `!pay @người_dùng [số_tiền]` - Tặng/chuyển xu cho bạn bè",
        inline=False
    )

    # Nhóm Mini Game
    embed.add_field(
        name="🎮 **Mini Game Hấp Dẫn**",
        value="• `!mines [số mìn]` - Chơi dò mìn cược 10 xu mặc định (VD: `!mines 3`)\n"
              "• `!mines [tiền cược] [số mìn]` - Tự chỉnh cược và mìn (VD: `!mines 50 4`)",
        inline=False
    )

    embed.set_footer(text=f"Yêu cầu bởi {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# --- 5. LỆNH CƠ BẢN ---
@bot.command()
async def hi(ctx):
    await ctx.send("lô")

@bot.command()
async def khen(ctx):
    await ctx.send("khuaaoxanh depzai lam do")

@bot.command()
async def gay(ctx):
    await ctx.send("gay là bạn hả?")

# --- 6. LỆNH VÍ TIỀN & KIẾM XU ---
@bot.command(aliases=['bal', 'coin', 'tien'])
async def cash(ctx):
    bal = get_balance(ctx.author.id)
    await ctx.send(f"💰 **{ctx.author.name}** hiện có: **{bal:,}** xu 🪙")

@bot.command()
async def daily(ctx):
    update_balance(ctx.author.id, 500)
    bal = get_balance(ctx.author.id)
    await ctx.send(f"🎁 **{ctx.author.name}** vừa nhận **500 xu** điểm danh! Tổng xu: **{bal:,}** xu.")

@bot.command()
async def work(ctx):
    earned = random.randint(50, 200)
    jobs = ["chạy Grab", "rửa bát", "code dạo", "nhặt ve chai", "sửa máy tính"]
    job = random.choice(jobs)
    update_balance(ctx.author.id, earned)
    bal = get_balance(ctx.author.id)
    await ctx.send(f"🛠️ **{ctx.author.name}** đi {job} kiếm được **+{earned} xu**! Hiện có: **{bal:,}** xu.")

@bot.command()
async def beg(ctx):
    if random.random() < 0.7:
        earned = random.randint(10, 80)
        update_balance(ctx.author.id, earned)
        bal = get_balance(ctx.author.id)
        await ctx.send(f"🥺 Ai đó đã cho **{ctx.author.name}** **{earned} xu**! Hiện có: **{bal:,}** xu.")
    else:
        await ctx.send(f"😅 **{ctx.author.name}** xin tiền nhưng bị từ chối thẳng thừng!")

@bot.command()
async def pay(ctx, member: discord.Member = None, amount: int = None):
    if not member or not amount:
        await ctx.send("⚠️ Cú pháp: `!pay @người_nhận [số_tiền]`")
        return
    if member == ctx.author:
        await ctx.send("❌ Không thể tự chuyển tiền cho chính mình!")
        return
    if amount <= 0:
        await ctx.send("⚠️ Số tiền phải lớn hơn 0!")
        return

    sender_bal = get_balance(ctx.author.id)
    if sender_bal < amount:
        await ctx.send(f"❌ Bạn không đủ xu! Hiện có: **{sender_bal:,}** xu.")
        return

    update_balance(ctx.author.id, -amount)
    update_balance(member.id, amount)
    await ctx.send(f"💸 **{ctx.author.name}** đã chuyển **{amount:,} xu** cho **{member.name}**!")

# --- 7. MINES GAME ---
class MinesGameView(View):
    def __init__(self, author, bet, num_mines):
        super().__init__(timeout=120)
        self.author = author
        self.bet = bet
        self.num_mines = num_mines
        self.gems_found = 0
        self.multiplier = 1.0
        self.is_over = False
        self.step_multiplier = 0.2 + (num_mines * 0.15)

        self.grid = ['gem'] * (9 - num_mines) + ['mine'] * num_mines
        random.shuffle(self.grid)

        for i in range(9):
            btn = Button(label="?", style=discord.ButtonStyle.secondary, custom_id=str(i), row=i // 3)
            btn.callback = self.make_button_callback(i)
            self.add_item(btn)

        self.cashout_btn = Button(label="💵 Cash Out", style=discord.ButtonStyle.success, row=3)
        self.cashout_btn.callback = self.cashout_callback
        self.add_item(self.cashout_btn)

    def make_button_callback(self, index):
        async def callback(interaction: discord.Interaction):
            if interaction.user != self.author or self.is_over:
                if interaction.user != self.author:
                    await interaction.response.send_message("❌ Đây không phải bàn chơi của bạn!", ephemeral=True)
                return

            btn = self.children[index]
            btn.disabled = True

            if self.grid[index] == 'mine':
                self.is_over = True
                btn.label = "💣"
                btn.style = discord.ButtonStyle.danger
                self.reveal_all()
                embed = discord.Embed(
                    title="💥 BOOM! Trúng mìn rồi!",
                    description=f"**{self.author.name}** đã mất **{self.bet:,}** xu!",
                    color=discord.Color.red()
                )
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                self.gems_found += 1
                self.multiplier += self.step_multiplier
                btn.label = "💎"
                btn.style = discord.ButtonStyle.primary

                if self.gems_found == (9 - self.num_mines):
                    self.is_over = True
                    win_amount = int(self.bet * self.multiplier)
                    update_balance(self.author.id, win_amount)
                    self.reveal_all()
                    embed = discord.Embed(
                        title="🎉 THẮNG LỚN! (CLEARED)",
                        description=f"Dọn sạch kim cương!\nMức nhân: **{self.multiplier:.2f}x** | Thưởng: **+{win_amount:,}** xu!",
                        color=discord.Color.gold()
                    )
                    await interaction.response.edit_message(embed=embed, view=self)
                else:
                    current_win = int(self.bet * self.multiplier)
                    next_mult = self.multiplier + self.step_multiplier
                    embed = discord.Embed(
                        title=f"💣 Mines Game - {self.author.name}",
                        description=f"**Bet:** {self.bet:,} | **Mìn:** {self.num_mines}\n"
                                    f"**Ăn hiện tại:** {current_win:,} xu ({self.multiplier:.2f}x)\n"
                                    f"**Ô tiếp theo:** {next_mult:.2f}x",
                        color=discord.Color.blue()
                    )
                    await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def cashout_callback(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("❌ Đây không phải bàn chơi của bạn!", ephemeral=True)
            return
        if self.gems_found == 0:
            await interaction.response.send_message("⚠️ Phải mở ít nhất 1 ô mới Cash Out được!", ephemeral=True)
            return

        self.is_over = True
        win_amount = int(self.bet * self.multiplier)
        update_balance(self.author.id, win_amount)
        self.reveal_all()

        embed = discord.Embed(
            title="💰 CASH OUT THÀNH CÔNG!",
            description=f"**{self.author.name}** đã chốt lời!\nNhận được: **{win_amount:,}** xu ({self.multiplier:.2f}x)",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)

    def reveal_all(self):
        for i, item in enumerate(self.grid):
            btn = self.children[i]
            btn.disabled = True
            if item == 'mine':
                btn.label = "💣"
                btn.style = discord.ButtonStyle.danger
            elif btn.label == "?":
                btn.label = "💎"
        self.cashout_btn.disabled = True

@bot.command()
async def mines(ctx, arg1: int = 10, arg2: int = None):
    if arg2 is None:
        bet = 10
        num_mines = arg1
    else:
        bet = arg1
        num_mines = arg2

    if num_mines < 1 or num_mines > 8:
        await ctx.send("⚠️ Số mìn phải nằm trong khoảng từ 1 đến 8!")
        return
    if bet <= 0:
        await ctx.send("⚠️ Số tiền cược phải lớn hơn 0!")
        return

    user_bal = get_balance(ctx.author.id)
    if bet > user_bal:
        await ctx.send(f"❌ Bạn không đủ xu! Số dư hiện tại: **{user_bal:,}** xu.")
        return

    # Trừ tiền cược khi mở game
    update_balance(ctx.author.id, -bet)

    view = MinesGameView(author=ctx.author, bet=bet, num_mines=num_mines)
    step = 0.2 + (num_mines * 0.15)
    
    embed = discord.Embed(
        title=f"💣 Mines Game - {ctx.author.name}",
        description=f"**Bet:** {bet:,} xu | **Mìn:** {num_mines}\n"
                    f"**Ăn hiện tại:** 0 xu (0.00x)\n"
                    f"**Ô tiếp theo:** {1.0 + step:.2f}x",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=view)

token = os.environ.get('BOT_TOKEN')
bot.run(token)
