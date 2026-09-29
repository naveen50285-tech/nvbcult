import os
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

os.makedirs("static/products", exist_ok=True)

# Load fonts
FONT_DIR = r"C:\Windows\Fonts"
def get_font(name, size):
    try:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    except:
        pass
    return ImageFont.load_default()

font_hero = get_font("georgia.ttf", 42)
font_title_lg = get_font("georgia.ttf", 32)
font_title_md = get_font("georgia.ttf", 24)
font_title_sm = get_font("georgia.ttf", 17)
font_sans_bold_lg = get_font("arialbd.ttf", 26)
font_sans_bold = get_font("arialbd.ttf", 20)
font_sans_md = get_font("arialbd.ttf", 15)
font_sans_sm = get_font("arialbd.ttf", 12)
font_mono_lg = get_font("consola.ttf", 18)
font_mono_bold = get_font("consola.ttf", 15)
font_mono = get_font("consola.ttf", 13)

# Load official logo
logo_path = "static/nvb-logo.png"
raw_logo = Image.open(logo_path).convert("RGBA") if os.path.exists(logo_path) else None

def get_circular_logo(size):
    if not raw_logo: return None
    logo_res = raw_logo.resize((size, size), Image.Resampling.LANCZOS)
    # create circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size, size], fill=255)
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(logo_res, (0, 0), mask)
    return output

def create_studio_base(sku, category, drop_title, badge_text="ORIGINAL SPECIMEN"):
    """Creates 1000x1000 obsidian studio canvas with luxury gold framing and markings."""
    bg = Image.new("RGBA", (1000, 1000), (8, 8, 12, 255))
    
    # Radial gold ambient glow
    spot = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    spot_draw = ImageDraw.Draw(spot)
    for r in range(480, 40, -8):
        alpha = int((1.0 - (r / 480.0)) * 50)
        spot_draw.ellipse([500 - r, 460 - int(r*0.75), 500 + r, 460 + int(r*0.75)], fill=(212, 175, 55, alpha))
    spot = spot.filter(ImageFilter.GaussianBlur(25))
    bg = Image.alpha_composite(bg, spot)
    
    # Studio pedestal platform
    ped = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    ped_draw = ImageDraw.Draw(ped)
    ped_draw.ellipse([110, 710, 890, 930], fill=(16, 16, 24, 255), outline=(212, 175, 55, 70), width=2)
    ped_draw.ellipse([190, 740, 810, 905], fill=(12, 12, 18, 255), outline=(251, 191, 36, 45), width=1)
    ped = ped.filter(ImageFilter.GaussianBlur(1))
    bg = Image.alpha_composite(bg, ped)
    
    # Luxury double border framing
    fr_draw = ImageDraw.Draw(bg)
    fr_draw.rectangle([18, 18, 981, 981], outline=(212, 175, 55, 90), width=1)
    fr_draw.rectangle([24, 24, 975, 975], outline=(212, 175, 55, 35), width=1)
    
    # Golden corner accents
    corners = [(24, 24), (975, 24), (24, 975), (975, 975)]
    bracket_len = 28
    for cx, cy in corners:
        dx = bracket_len if cx < 500 else -bracket_len
        dy = bracket_len if cy < 500 else -bracket_len
        fr_draw.line([(cx, cy), (cx + dx, cy)], fill=(251, 191, 36, 220), width=2)
        fr_draw.line([(cx, cy), (cx, cy + dy)], fill=(251, 191, 36, 220), width=2)
        
    # Top strip metadata
    fr_draw.text((45, 42), f"NVB CULT // {category.upper()}", fill=(212, 175, 55), font=font_mono_bold)
    fr_draw.text((45, 66), f"SKU: {sku} • EST. 2026", fill=(148, 163, 184), font=font_mono)
    
    # Top right verified original seal
    seal_w = 230
    fr_draw.rectangle([955 - seal_w, 40, 955, 78], fill=(18, 18, 26, 230), outline=(212, 175, 55, 190), width=1)
    fr_draw.text((955 - seal_w + 14, 50), f"✦ {badge_text}", fill=(251, 191, 36), font=font_sans_sm)
    
    # Bottom strip
    fr_draw.line([(45, 920), (955, 920)], fill=(212, 175, 55, 75), width=1)
    fr_draw.text((45, 933), drop_title.upper()[:42], fill=(255, 255, 255), font=font_title_sm)
    fr_draw.text((45, 960), "DREAM • PLAN • ACHIEVE  |  OFFICIAL DROP", fill=(212, 175, 55), font=font_mono)
    fr_draw.text((760, 946), "NEXT VISION BRAND", fill=(148, 163, 184), font=font_mono)
    
    return bg

def draw_tshirt_silhouette(draw, cx=500, cy=460, color=(18, 18, 24), outline=(45, 45, 60)):
    """Draws drop-shoulder boxy luxury streetwear tee silhouette."""
    # Tee coordinates relative to center
    pts = [
        (cx - 70, cy - 250), # Left collar
        (cx - 240, cy - 190), # Left shoulder drop
        (cx - 330, cy - 80), # Left sleeve outer
        (cx - 240, cy - 30), # Left sleeve cuff inner
        (cx - 200, cy - 100), # Left armpit
        (cx - 210, cy + 240), # Left hem
        (cx + 210, cy + 240), # Right hem
        (cx + 200, cy - 100), # Right armpit
        (cx + 240, cy - 30), # Right sleeve cuff inner
        (cx + 330, cy - 80), # Right sleeve outer
        (cx + 240, cy - 190), # Right shoulder drop
        (cx + 70, cy - 250), # Right collar
    ]
    # Drop shadow
    shadow_pts = [(x + 4, y + 8) for (x, y) in pts]
    draw.polygon(shadow_pts, fill=(0, 0, 0, 180))
    # Main body
    draw.polygon(pts, fill=color, outline=outline, width=3)
    
    # Crew neck ribbed collar curve
    draw.arc([cx - 75, cy - 280, cx + 75, cy - 215], start=0, end=180, fill=(212, 175, 55, 120), width=4)
    draw.arc([cx - 65, cy - 275, cx + 65, cy - 225], start=0, end=180, fill=(10, 10, 15), width=8)
    
    # Inner collar brand tag
    draw.rectangle([cx - 45, cy - 235, cx + 45, cy - 212], fill=(12, 12, 16), outline=(212, 175, 55, 160), width=1)
    draw.text((cx - 38, cy - 230), "NVB CULT", fill=(212, 175, 55), font=font_mono)

# ==================== PRODUCT 1: DREAM • PLAN • ACHIEVE TEE ====================
def make_tee_dpa():
    im = create_studio_base("NVB-TEE-DPA-01", "T-Shirts", "Dream • Plan • Achieve Heavyweight Tee 260 GSM", "260 GSM FRENCH TERRY")
    draw = ImageDraw.Draw(im)
    draw_tshirt_silhouette(draw, 500, 470, color=(16, 16, 22), outline=(212, 175, 55, 70))
    
    # Gold chest artwork
    # Official logo badge
    logo = get_circular_logo(130)
    if logo:
        im.paste(logo, (500 - 65, 340), logo)
        
    # Typography
    t1 = "DREAM • PLAN • ACHIEVE"
    bbox1 = font_sans_bold.getbbox(t1)
    tw1 = bbox1[2] - bbox1[0]
    draw.text((500 - tw1//2, 490), t1, fill=(251, 191, 36), font=font_sans_bold)
    
    t2 = "NEXT VISION BRAND // CULT VAULT"
    bbox2 = font_mono.getbbox(t2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((500 - tw2//2, 525), t2, fill=(212, 175, 55), font=font_mono)
    
    # Woven gold hem badge
    draw.rectangle([450, 680, 550, 705], fill=(20, 20, 28), outline=(212, 175, 55), width=1)
    draw.text((458, 686), "260 GSM COTTON", fill=(251, 191, 36), font=font_sans_sm)
    
    im.convert("RGB").save("static/products/nvb-tee-dream-plan-achieve.jpg", quality=95)
    print("Saved nvb-tee-dream-plan-achieve.jpg")

# ==================== PRODUCT 2: GOLDEN EYE OF HORUS TEE ====================
def make_tee_horus():
    im = create_studio_base("NVB-TEE-HORUS-02", "T-Shirts", "Golden Eye of Horus Cyber-Graphic Acid Wash Tee", "METALLIC GOLD FOIL")
    draw = ImageDraw.Draw(im)
    draw_tshirt_silhouette(draw, 500, 470, color=(24, 24, 30), outline=(212, 175, 55, 80))
    
    # Acid wash subtle specks
    import random
    random.seed(42)
    for _ in range(80):
        rx = random.randint(320, 680)
        ry = random.randint(300, 650)
        r_rad = random.randint(1, 3)
        draw.ellipse([rx, ry, rx + r_rad, ry + r_rad], fill=(55, 55, 70, 80))
        
    # Draw metallic Eye of Horus graphic
    cx, cy = 500, 440
    # Outer eye almond shape
    draw.arc([cx - 110, cy - 80, cx + 110, cy + 60], start=190, end=350, fill=(251, 191, 36), width=4)
    draw.arc([cx - 110, cy - 40, cx + 110, cy + 100], start=10, end=170, fill=(251, 191, 36), width=4)
    # Pupil
    draw.ellipse([cx - 30, cy - 10, cx + 30, cy + 50], fill=(212, 175, 55), outline=(255, 255, 255), width=2)
    draw.ellipse([cx - 12, cy + 8, cx + 12, cy + 32], fill=(12, 12, 18))
    # Horus spiral & tear markings
    draw.line([(cx - 70, cy + 35), (cx - 70, cy + 95), (cx - 110, cy + 120)], fill=(251, 191, 36), width=3)
    draw.line([(cx + 20, cy + 35), (cx + 20, cy + 105)], fill=(251, 191, 36), width=3)
    
    # Circuit traces
    draw.line([(cx - 160, cy + 20), (cx - 120, cy + 20)], fill=(212, 175, 55), width=2)
    draw.line([(cx + 120, cy + 20), (cx + 160, cy + 20)], fill=(212, 175, 55), width=2)
    
    t1 = "HORUS // CYBER ARCHIVE"
    bbox1 = font_sans_bold.getbbox(t1)
    draw.text((500 - (bbox1[2]-bbox1[0])//2, 575), t1, fill=(251, 191, 36), font=font_sans_bold)
    
    im.convert("RGB").save("static/products/nvb-tee-golden-eye-horus.jpg", quality=95)
    print("Saved nvb-tee-golden-eye-horus.jpg")

# ==================== PRODUCT 3: OBSIDIAN SUPIMA LUXURY TEE ====================
def make_tee_supima():
    im = create_studio_base("NVB-TEE-SUPIMA-03", "T-Shirts", "NVB Obsidian Luxury Supima Plain Minimalist Tee", "100% SUPIMA COTTON")
    draw = ImageDraw.Draw(im)
    draw_tshirt_silhouette(draw, 500, 470, color=(11, 11, 15), outline=(60, 60, 75))
    
    # Micro gold embroidered crest on left chest
    logo = get_circular_logo(70)
    if logo:
        im.paste(logo, (420, 360), logo)
    
    draw.text((412, 438), "NVB CULT", fill=(212, 175, 55), font=font_mono_bold)
    draw.text((410, 456), "PARIS • 2026", fill=(148, 163, 184), font=font_mono)
    
    # Fabric quality callout
    draw.line([(550, 480), (670, 450)], fill=(212, 175, 55, 120), width=1)
    draw.text((675, 442), "EXTRA-LONG STAPLE SUPIMA", fill=(212, 175, 55), font=font_mono)
    draw.text((675, 460), "SILK-LIKE DRAPE & LUSTRE", fill=(148, 163, 184), font=font_sans_sm)
    
    im.convert("RGB").save("static/products/nvb-tee-supima-obsidian-luxury.jpg", quality=95)
    print("Saved nvb-tee-supima-obsidian-luxury.jpg")

# ==================== PRODUCT 4: CYBERPUNK DROP-SHOULDER TEE ====================
def make_tee_cyberpunk():
    im = create_studio_base("NVB-TEE-CYBER-04", "T-Shirts", "NVB Melodic Cyberpunk Drop-Shoulder Heavy Tee", "ANALOG AUDIO EDITION")
    draw = ImageDraw.Draw(im)
    draw_tshirt_silhouette(draw, 500, 470, color=(17, 17, 24), outline=(212, 175, 55, 80))
    
    # Analog soundwave graphic on chest
    cx, cy = 500, 440
    # Draw digital synthesizer frequencies
    wave_pts = []
    for i in range(-140, 145, 10):
        h = int(math.sin(i * 0.15) * 35 + math.cos(i * 0.05) * 20)
        draw.line([(cx + i, cy - h), (cx + i, cy + h)], fill=(251, 191, 36), width=4)
        
    t1 = "ANALOG SOUNDTRACK // CULT 2026"
    bbox1 = font_sans_bold.getbbox(t1)
    draw.text((500 - (bbox1[2]-bbox1[0])//2, 530), t1, fill=(251, 191, 36), font=font_sans_bold)
    
    t2 = "SIDE A • 260 GSM DROP SHOULDER"
    bbox2 = font_mono.getbbox(t2)
    draw.text((500 - (bbox2[2]-bbox2[0])//2, 565), t2, fill=(212, 175, 55), font=font_mono)
    
    im.convert("RGB").save("static/products/nvb-tee-cyberpunk-analog-drop.jpg", quality=95)
    print("Saved nvb-tee-cyberpunk-analog-drop.jpg")

# ==================== PRODUCT 5: CYBERDECK ANC EARBUDS ====================
def make_elec_earbuds():
    im = create_studio_base("NVB-AUD-ANC-01", "Electronics", "NVB CyberDeck ANC Studio Earbuds (Black & Gold)", "45dB HYBRID ANC")
    draw = ImageDraw.Draw(im)
    
    cx, cy = 500, 480
    # Earbuds charging case (matte obsidian rounded pebble)
    # Shadow
    draw.rounded_rectangle([cx - 170, cy - 90 + 15, cx + 170, cy + 130 + 15], radius=60, fill=(0, 0, 0, 180))
    # Case body
    draw.rounded_rectangle([cx - 170, cy - 90, cx + 170, cy + 130], radius=60, fill=(20, 20, 28), outline=(212, 175, 55), width=3)
    # Gold seam divide
    draw.line([(cx - 165, cy + 15), (cx + 165, cy + 15)], fill=(251, 191, 36), width=2)
    # Center gold logo
    logo = get_circular_logo(85)
    if logo:
        im.paste(logo, (cx - 42, cy - 65), logo)
    # LED indicator
    draw.ellipse([cx - 4, cy + 40, cx + 4, cy + 48], fill=(34, 197, 94)) # Green battery LED
    
    # Left Earbud floating outside
    el_x, el_y = cx - 240, cy + 20
    draw.ellipse([el_x - 35, el_y - 45, el_x + 35, el_y + 45], fill=(26, 26, 36), outline=(212, 175, 55), width=2)
    draw.rounded_rectangle([el_x - 12, el_y + 15, el_x + 12, el_y + 90], radius=8, fill=(20, 20, 28), outline=(212, 175, 55), width=2)
    draw.ellipse([el_x - 18, el_y - 25, el_x + 18, el_y + 10], fill=(251, 191, 36)) # Touch gold ring
    
    # Right Earbud floating outside
    er_x, er_y = cx + 240, cy + 20
    draw.ellipse([er_x - 35, er_y - 45, er_x + 35, er_y + 45], fill=(26, 26, 36), outline=(212, 175, 55), width=2)
    draw.rounded_rectangle([er_x - 12, er_y + 15, er_x + 12, er_y + 90], radius=8, fill=(20, 20, 28), outline=(212, 175, 55), width=2)
    draw.ellipse([er_x - 18, er_y - 25, er_x + 18, er_y + 10], fill=(251, 191, 36)) # Touch gold ring
    
    # Spec callouts
    draw.text((cx - 130, cy + 85), "40H PLAYTIME • LOW LATENCY", fill=(212, 175, 55), font=font_mono)
    
    im.convert("RGB").save("static/products/nvb-elec-cyberdeck-anc-earbuds.jpg", quality=95)
    print("Saved nvb-elec-cyberdeck-anc-earbuds.jpg")

# ==================== PRODUCT 6: MAGFAST 65W GaN CHARGER ====================
def make_elec_charger():
    im = create_studio_base("NVB-PWR-GAN-02", "Electronics", "NVB MagFast 65W GaN Turbo Multi-Port Fast Charger", "GaN III TECH")
    draw = ImageDraw.Draw(im)
    
    cx, cy = 500, 480
    # 3D isometric styled GaN brick
    # Shadow
    draw.rounded_rectangle([cx - 130 + 10, cy - 170 + 20, cx + 130 + 10, cy + 170 + 20], radius=24, fill=(0, 0, 0, 180))
    # Charger body
    draw.rounded_rectangle([cx - 130, cy - 170, cx + 130, cy + 170], radius=24, fill=(18, 18, 26), outline=(212, 175, 55), width=3)
    
    # Gold pins at bottom
    draw.rectangle([cx - 60, cy + 170, cx - 35, cy + 225], fill=(251, 191, 36), outline=(180, 140, 20), width=1)
    draw.rectangle([cx + 35, cy + 170, cx + 60, cy + 225], fill=(251, 191, 36), outline=(180, 140, 20), width=1)
    
    # USB-C1 Port
    draw.rounded_rectangle([cx - 45, cy - 120, cx + 45, cy - 85], radius=10, fill=(10, 10, 14), outline=(251, 191, 36), width=2)
    draw.text((cx + 55, cy - 110), "Type-C1 (65W MAX)", fill=(212, 175, 55), font=font_mono)
    
    # USB-C2 Port
    draw.rounded_rectangle([cx - 45, cy - 60, cx + 45, cy - 25], radius=10, fill=(10, 10, 14), outline=(251, 191, 36), width=2)
    draw.text((cx + 55, cy - 50), "Type-C2 (30W)", fill=(212, 175, 55), font=font_mono)
    
    # USB-A Port
    draw.rectangle([cx - 50, cy + 0, cx + 50, cy + 35], fill=(10, 10, 14), outline=(251, 191, 36), width=2)
    draw.text((cx + 55, cy + 10), "USB-A (18W QC)", fill=(212, 175, 55), font=font_mono)
    
    # Brand branding on brick
    draw.text((cx - 85, cy + 75), "NVB CULT // 65W GaN", fill=(251, 191, 36), font=font_sans_bold)
    draw.text((cx - 95, cy + 110), "OVERCHARGE PROTECTION", fill=(148, 163, 184), font=font_mono)
    
    im.convert("RGB").save("static/products/nvb-elec-magfast-65w-gan.jpg", quality=95)
    print("Saved nvb-elec-magfast-65w-gan.jpg")

# ==================== PRODUCT 7: CREATOR SOUNDTRACK STUDIO MIC ====================
def make_elec_mic():
    im = create_studio_base("NVB-MIC-POD-03", "Electronics", "NVB Creator SoundTrack XLR/USB Studio Podcast Mic", "BROADCAST GRADE")
    draw = ImageDraw.Draw(im)
    
    cx, cy = 500, 480
    # Mic body shadow
    draw.rounded_rectangle([cx - 70 + 10, cy - 220 + 20, cx + 70 + 10, cy + 120 + 20], radius=35, fill=(0, 0, 0, 180))
    
    # Main cylinder mic body
    draw.rounded_rectangle([cx - 70, cy - 220, cx + 70, cy + 120], radius=35, fill=(16, 16, 22), outline=(50, 50, 65), width=2)
    
    # Gold mesh capsule top grille
    draw.rounded_rectangle([cx - 65, cy - 215, cx + 65, cy - 60], radius=30, fill=(24, 20, 12), outline=(251, 191, 36), width=3)
    # Mesh cross-hatch
    for y in range(cy - 200, cy - 70, 12):
        draw.line([(cx - 55, y), (cx + 55, y)], fill=(212, 175, 55, 160), width=1)
    
    # Gold band in middle
    draw.rectangle([cx - 70, cy - 60, cx + 70, cy - 40], fill=(251, 191, 36))
    
    # Logo & dial on lower body
    logo = get_circular_logo(55)
    if logo:
        im.paste(logo, (cx - 27, cy - 25), logo)
    
    # Gain dial
    draw.ellipse([cx - 22, cy + 45, cx + 22, cy + 89], fill=(25, 25, 35), outline=(251, 191, 36), width=2)
    draw.line([(cx, cy + 47), (cx, cy + 60)], fill=(251, 191, 36), width=2)
    
    # Heavy duty shockmount outer ring
    draw.arc([cx - 150, cy - 40, cx + 150, cy + 150], start=0, end=180, fill=(212, 175, 55), width=5)
    draw.line([(cx - 150, cy + 55), (cx - 70, cy + 55)], fill=(251, 191, 36), width=3)
    draw.line([(cx + 70, cy + 55), (cx + 150, cy + 55)], fill=(251, 191, 36), width=3)
    
    # Stand pole
    draw.rectangle([cx - 15, cy + 150, cx + 15, cy + 240], fill=(251, 191, 36))
    
    im.convert("RGB").save("static/products/nvb-elec-creator-soundtrack-mic.jpg", quality=95)
    print("Saved nvb-elec-creator-soundtrack-mic.jpg")

# ==================== PRODUCT 8: CHRONOSYNC AMOLED SMARTWATCH ====================
def make_elec_watch():
    im = create_studio_base("NVB-WCH-SYNC-04", "Electronics", "NVB ChronoSync AMOLED Cyberpunk Smartwatch", "TITANIUM & GOLD")
    draw = ImageDraw.Draw(im)
    
    cx, cy = 500, 470
    
    # Black silicone strap top & bottom
    draw.rounded_rectangle([cx - 65, cy - 270, cx + 65, cy - 140], radius=15, fill=(15, 15, 20), outline=(50, 50, 65), width=2)
    draw.rounded_rectangle([cx - 65, cy + 140, cx + 65, cy + 270], radius=15, fill=(15, 15, 20), outline=(50, 50, 65), width=2)
    # Strap rib lines
    for sy in range(cy - 250, cy - 150, 18):
        draw.line([(cx - 50, sy), (cx + 50, sy)], fill=(30, 30, 40), width=3)
    for sy in range(cy + 160, cy + 260, 18):
        draw.line([(cx - 50, sy), (cx + 50, sy)], fill=(30, 30, 40), width=3)
        
    # Watch case shadow
    draw.ellipse([cx - 170 + 8, cy - 170 + 16, cx + 170 + 8, cy + 170 + 16], fill=(0, 0, 0, 190))
    
    # Watch Case Outer Bezel (Titanium & Gold)
    draw.ellipse([cx - 170, cy - 170, cx + 170, cy + 170], fill=(20, 20, 28), outline=(212, 175, 55), width=6)
    
    # Knurled Gold Crown button on right
    draw.rounded_rectangle([cx + 165, cy - 30, cx + 195, cy + 30], radius=6, fill=(251, 191, 36), outline=(180, 140, 20), width=1)
    
    # Watch AMOLED Display Dial
    draw.ellipse([cx - 145, cy - 145, cx + 145, cy + 145], fill=(5, 5, 8), outline=(251, 191, 36, 120), width=2)
    
    # Dial markings
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x1 = cx + math.cos(rad) * 130
        y1 = cy + math.sin(rad) * 130
        x2 = cx + math.cos(rad) * 142
        y2 = cy + math.sin(rad) * 142
        draw.line([(x1, y1), (x2, y2)], fill=(251, 191, 36), width=3 if deg % 90 == 0 else 1)
        
    # Brand on watch face
    draw.text((cx - 50, cy - 75), "NVB CULT", fill=(212, 175, 55), font=font_sans_bold)
    draw.text((cx - 38, cy - 50), "EST. 2026", fill=(148, 163, 184), font=font_mono)
    
    # Digital time in center
    draw.text((cx - 55, cy - 15), "10:26", fill=(255, 255, 255), font=font_hero)
    
    # Battery & Heart rate stats
    draw.text((cx - 70, cy + 45), "♥ 74 BPM  •  ⚡ 98%", fill=(251, 191, 36), font=font_mono)
    draw.text((cx - 80, cy + 72), "DREAM • PLAN • ACHIEVE", fill=(148, 163, 184), font=font_mono)
    
    im.convert("RGB").save("static/products/nvb-elec-chronosync-amoled-watch.jpg", quality=95)
    print("Saved nvb-elec-chronosync-amoled-watch.jpg")

if __name__ == "__main__":
    make_tee_dpa()
    make_tee_horus()
    make_tee_supima()
    make_tee_cyberpunk()
    make_elec_earbuds()
    make_elec_charger()
    make_elec_mic()
    make_elec_watch()
    print("ALL 8 ORIGINAL NVB CULT PRODUCT ASSETS GENERATED!")
