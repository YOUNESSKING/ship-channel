import sys, glob
from PIL import Image
ims=[Image.open(glob.glob(f"scenes/v01_{s}/.hyperframes/artifacts/snapshots/*/contact-sheet.jpg")[-1] if False else sorted(glob.glob(f"scenes/v01_{s}/.hyperframes/artifacts/snapshots/*/contact-sheet.jpg"), key=lambda p: __import__('os').path.getmtime(p))[-1]) for s in sys.argv[2:]]
w=max(i.width for i in ims); out=Image.new("RGB",(w,sum(i.height for i in ims)))
y=0
for i in ims: out.paste(i,(0,y)); y+=i.height
out.save(sys.argv[1],quality=88)
