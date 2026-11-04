"""Spoken word count of script.md (paragraphs that follow a [MAP]/[ARCHIVE] tag line). run from sherman/."""
import re
t = open("script.md").read(); n = 0; per = []
for sec in t.split("\n## ")[1:]:
    for p in sec.split("\n\n"):
        if p.startswith("["):
            m = re.match(r"^\[([^\]|]*)", p); s = re.sub(r"^\[[^\]]*\]\s*", "", p).strip(); w = len(s.split()); n += w; per.append((m.group(1).strip(), w))
for tag, w in per: print(f"{tag:14s} {w}")
print("TOTAL", n, "words ~", round(n / 150, 1), "min at 150 wpm")
