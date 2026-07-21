@bot.command()
async def print(ctx, *, text: str):
    # Xóa bớt khoảng trắng thừa 2 đầu
    text = text.strip()
    
    # Kiểm tra xem có bắt đầu bằng ( và kết thúc bằng ) không
    if text.startswith('(') and text.endswith(')'):
        # Cắt bỏ 2 dấu ngoặc đơn ở 2 đầu: ( ... )
        inner = text[1:-1].strip()
        
        # Nếu bên trong có dấu ngoặc kép/đơn (kể cả dấu ngoặc cong điện thoại), cắt tiếp
        if (inner.startswith('"') and inner.endswith('"')) or \
           (inner.startswith("'") and inner.endswith("'")) or \
           (inner.startswith('“') and inner.endswith('”')) or \
           (inner.startswith('”') and inner.endswith('”')):
            inner = inner[1:-1]
            
        await ctx.send(inner)
    else:
        await ctx.send('⚠️ Cú pháp sai rồi! Bạn phải gõ đúng dạng: `!print("nội dung")`')
