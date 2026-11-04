#!/usr/bin/env python3
"""Square face crops (400x400 RGB) from sherman/assets/media/<name>_src.jpg.
Box = (left, top, right, bottom) in source pixels. Run: python3 cleburne/tools/make_heads.py [name ...]
_head_flat.png = RGB crop; _head.png = RGBA cut-out of it (rembg isnet-general-use) if cleburne/tools/cutout_heads.py is run."""
import sys
from PIL import Image
M = "/home/user/battle-maps/arnold/assets/media/"
BOXES = {
    "arnold":      ("grant_src.jpg",      (195, 170, 475, 450)),
    "lincoln":    ("lincoln_src.jpg",    (197, 243, 376, 422)),
    "sherman": ("sherman_src.jpg", (108, 142, 483, 517)),
    "johnston": ("johnston_src.jpg", (85, 90, 505, 510)),
    "hood": ("hood_src.jpg", (145, 161, 445, 461)),
    "thomas": ("thomas_src.jpg", (139, 165, 514, 540)),
    "mcpherson": ("mcpherson_src.jpg", (125, 153, 500, 528)),
    "schofield": ("schofield_src.jpg", (76, 130, 476, 530)),
    "howard": ("howard_src.jpg", (118, 163, 493, 538)),
    "slocum": ("slocum_src.jpg", (118, 170, 493, 545)),
    "hardee": ("hardee_src.jpg", (74, 240, 454, 620)),
    "kilpatrick": ("kilpatrick_src.jpg", (245, 260, 625, 640)),
    "hazen": ("hazen_src.jpg", (243, 276, 623, 656)),
    "mower": ("mower_src.jpg", (98, 189, 498, 589)),
    "wheeler": ("wheeler_src.jpg", (146, 86, 526, 466)),
    "hampton": ("hampton_src.jpg", (136, 205, 516, 585)),
    "beauregard": ("beauregard_src.jpg", (140, 224, 520, 604)),
    "polk": ("polk_src.jpg", (239, 139, 509, 409)),
    "davis": ("davis_src.jpg", (205, 148, 455, 398)),
    "jcdavis": ("jcdavis_src.jpg", (108, 153, 483, 528)),
    "cleburne": ("cleburne_src.jpg", (185, 133, 585, 533)),
    "bragg": ("bragg_src.jpg", (161, 183, 541, 563)),
    "hooker": ("hooker_src.jpg", (190, 220, 520, 550)),
    "wood": ("wood_src.jpg", (164, 257, 424, 517)),
    "osterhaus": ("osterhaus_src.jpg", (340, 87, 670, 417)),
    "geary": ("geary_src.jpg", (146, 222, 496, 572)),
    "lowrey": ("lowrey_src.jpg", (218, 190, 548, 520)),
    "bierce": ("bierce_src.jpg", (190, 40, 1090, 940)),
    "dahlgren": ("dahlgren_src.jpg", (132, 218, 507, 593)),
}
for k in (sys.argv[1:] or BOXES):
    f, box = BOXES[k]
    im = Image.open(M + f).convert("RGB").crop(box).resize((400, 400), Image.LANCZOS)
    im.save(M + k + "_head_flat.png")
    print(k, box)
