# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

INK="#16120e"; RED=(225,29,29,255)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def rounded(size, radius_ratio=0.22):
    img=Image.new("RGBA",(size,size),(0,0,0,0))
    d=ImageDraw.Draw(img)
    r=int(size*radius_ratio)
    d.rounded_rectangle([0,0,size-1,size-1], radius=r, fill=INK)
    # text 67
    fs=int(size*0.62)
    f=ImageFont.truetype(FONT, fs)
    txt="67"
    bb=d.textbbox((0,0),txt,font=f)
    w=bb[2]-bb[0]; h=bb[3]-bb[1]
    x=(size-w)/2 - bb[0]
    y=(size-h)/2 - bb[1]
    d.text((x,y),txt,font=f,fill=RED)
    return img

# master + downscale for crispness
master=rounded(512)
os.makedirs("assets",exist_ok=True)
master.save("assets/icon-512.png")
for s in (16,32,48,180,192):
    master.resize((s,s),Image.LANCZOS).save(f"assets/favicon-{s}.png")
os.replace("assets/favicon-180.png","assets/apple-touch-icon.png")
os.replace("assets/favicon-192.png","assets/icon-192.png")
# ICO with multiple sizes
master.save("assets/favicon.ico", sizes=[(16,16),(32,32),(48,48)])
print("generated:", [f for f in os.listdir("assets") if f.startswith(("favicon","icon","apple"))])
