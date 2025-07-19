"""
Some "gen & send" functions.
"""

from discord import User, Member, TextChannel, File
from os      import sep

async def image_welcome(member : User | Member, channel : TextChannel) :
    """Send a welcome image to `member` in `channel`."""
    # Imports
    from aiohttp  import ClientSession
    from io      import BytesIO
    from PIL     import Image, ImageDraw, ImageFont
    assets = sep + "assets" + sep
    # Get user avatar
    avatar_url = member.display_avatar.replace(size = 256, format="png").url
    async with ClientSession() as session :
        async with session.get(avatar_url) as resp :
            avatar_data = await resp.read()
    # Scale avatar
    avatar_img = Image.open(BytesIO(avatar_data)).convert("RGBA")
    avatar_img = avatar_img.resize((248, 248))
    # Round avatar
    mask = Image.new("L", (248, 248), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 248, 248), fill=255)
    avatar_img.putalpha(mask)
    # Paste avatar
    back = Image.open(assets + "png" + sep + "welcome_card.png").convert("RGBA")
    back.paste(avatar_img, (36, 36), avatar_img)
    # Write username
    draw = ImageDraw.Draw(back)
    font = ImageFont.truetype(assets + "fonts" + sep + "domine.ttf", 32)
    draw.text((338, 160), f"{member.name}", font = font, fill = "#dfe0e2")
    # Temp save
    buffer = BytesIO()
    back.save(buffer, format="PNG")
    buffer.seek(0)
    # Send
    await channel.send(content = f"<@{member.id}>", file = File(buffer, "welcome_card.png"))