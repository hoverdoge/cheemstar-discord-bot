import discord
from PIL import Image, ImageDraw

async def getPfp(user):
    filename = "avatar.jpg"
    await user.avatar_url.save(filename)
    pfp = discord.File(fp=filename)
    pfp = Image.open("avatar.jpg")
    pfp = pfp.resize((150, 150), 1)

    thumb_width = 150

    pfp_square = crop_max_square(pfp).resize((thumb_width, thumb_width), Image.LANCZOS)
    pfp_thumb = mask_circle_transparent(pfp_square, 4)
    pfp_thumb.save('newavatar.png')

    newpfp = Image.open('newavatar.png')

    return [newpfp, pfp_thumb]


async def getRankC(filename):
	pfp = Image.open(filename)
	pfp = pfp.resize((150, 150), 1)

	thumb_width = 150

	pfp_square = crop_max_square(pfp).resize((thumb_width, thumb_width), Image.LANCZOS)
	pfp_thumb = mask_circle_transparent(pfp_square, 4)
	pfp_thumb.save('newRankC.png')

	newRankC = Image.open('newRankC.png')

	return [newRankC, pfp_thumb]

async def getDimC():
	pfp = Image.open('images/dimc.png')
	pfp = pfp.resize((150, 150), 1)

	thumb_width = 150

	pfp_square = crop_max_square(pfp).resize((thumb_width, thumb_width), Image.LANCZOS)
	pfp_thumb = mask_circle_transparent(pfp_square, 4)
	pfp_thumb.save('dimC.png')

	newRankC = Image.open('dimC.png')

	return [newRankC, pfp_thumb]
def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    
    result = pil_img.copy()
    result.putalpha(mask)

    return result

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))