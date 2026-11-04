"""Build build/Arnold-publishing-guide.pdf (adapted from Patton's). Run from arnold/: python3 tools/make_publish_guide.py"""
import os, re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); os.chdir(ROOT)
pdfmetrics.registerFont(TTFont("Oswald", "tools/oswald-latin-700-normal.ttf"))
pdfmetrics.registerFont(TTFont("Elite", "tools/special-elite-latin-400-normal.ttf"))
INK, PAPER, BLUE, RED, EDGE = colors.HexColor("#2a241b"), colors.HexColor("#f4ecd8"), colors.HexColor("#2c57b7"), colors.HexColor("#bc2528"), colors.HexColor("#c9b48a")
S = {"cover": ParagraphStyle("cover", fontName="Oswald", fontSize=30, leading=36, textColor=INK, alignment=TA_CENTER),
     "coversub": ParagraphStyle("coversub", fontName="Elite", fontSize=12, leading=17, textColor=INK, alignment=TA_CENTER),
     "h1": ParagraphStyle("h1", fontName="Oswald", fontSize=20, leading=26, textColor=BLUE, spaceBefore=4, spaceAfter=8),
     "h2": ParagraphStyle("h2", fontName="Oswald", fontSize=13, leading=17, textColor=INK, spaceBefore=8, spaceAfter=4),
     "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK, spaceAfter=6),
     "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=11.5, textColor=INK),
     "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9, leading=11.5, textColor=INK),
     "mono": ParagraphStyle("mono", fontName="Courier", fontSize=7.6, leading=9.6, textColor=INK),
     "warn": ParagraphStyle("warn", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, backColor=colors.HexColor("#fbeceb"), borderColor=RED, borderWidth=0.8, borderPadding=7, spaceBefore=6, spaceAfter=10)}
P = lambda t, s="body": Paragraph(t, S[s])
bullets = lambda items: [P("&bull;&nbsp; " + i) for i in items]
def table(rows, widths):
    data = [[Paragraph(str(c), S["cellb" if r == 0 else "cell"]) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, EDGE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, 0), PAPER), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)])); return t
def img(path, w):
    from PIL import Image as PI
    iw, ih = PI.open(path).size; return Image(path, width=w * mm, height=w * mm * ih / iw)
def page(c, d):
    c.saveState(); c.setFillColor(PAPER); c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0); c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor("#8a7f6a"))
    c.drawString(18 * mm, 10 * mm, "Benedict Arnold's Top 3 Legendary Tactical Moves  |  publishing guide"); c.drawRightString(A4[0] - 18 * mm, 10 * mm, str(d.page)); c.restoreState()
desc = open("youtube/youtube_title_and_description.txt").read().strip(); TITLE = desc.splitlines()[0].strip()
chapters = [l for l in desc.splitlines() if re.match(r"^\d+:\d\d\s", l)]
TA, TB = "youtube/arnold-thumb-A_NO_COMMAND.jpg", "youtube/arnold-thumb-B_BEFORE_THE_TREASON.jpg"
LINK = os.environ.get("GOFILE_LINK", "(not uploaded yet: say 'upload' in the chat)")
LEN = os.environ.get("LEN", "15:2x"); LUFS = os.environ.get("LUFS", "-14 LUFS")
story = [Spacer(1, 18 * mm), P("BENEDICT ARNOLD", "cover"), P("TOP 3 LEGENDARY TACTICAL MOVES", "cover"), Spacer(1, 4 * mm),
         P("Publishing guide: everything you need to upload the finished video", "coversub"), Spacer(1, 8 * mm), img(TA, 150), Spacer(1, 3 * mm),
         P("Thumbnail A (NO COMMAND, vidIQ 86). The owner picks the main title and thumbnail; the others are for Test &amp; compare.", "coversub"), PageBreak()]
story += [P("1. The finished video", "h1"),
          table([["Item", "Details"], ["File", "Arnold-Top3-1080p.mp4 (1920x1080, 30 fps, H.264 + AAC; " + LUFS + ")"], ["Download", LINK], ["Length", LEN],
                 ["Voice", "Plain Kokoro am_michael narration (STYLE_LOCK 2c default)"], ["Music", "Kevin MacLeod, 4 tracks, CC BY 4.0, ducked under the voice (locked level 0.08)"],
                 ["Sound effects", "The channel's locked kit (Freesound CC BY / CC0, original effects)"],
                 ["Flags", "Americans: Continental Colours for 1775-76, 13-star flag for 1777; British: Union Flag (1606 pattern). Americans blue, British red"],
                 ["Look", "Map look v11, no trees, no modern reservoirs or canals (Flagstaff, Wyman, Champlain Canal left off), territory colours only on wide shots"]], [32, 138]),
          Spacer(1, 5 * mm), P("Chapters", "h2"), table([["Starts", "Chapter"]] + [[c.split(" ", 1)[0], c.split(" ", 1)[1]] for c in chapters], [20, 150])]
if os.path.exists("build/guide_frames.jpg"): story += [Spacer(1, 5 * mm), P("Key frames", "h2"), img("build/guide_frames.jpg", 170)]
story += [PageBreak(), P("2. Titles and thumbnails (Test &amp; compare)", "h1"),
          table([["", "Title", "vidIQ", "Claim check (research/FACT_NOTES.md)"],
                 ["A", "Benedict Arnold's Top 3 Legendary Tactical Moves | The Man Who Turned the Tide at Saratoga", "90", "His charge broke Burgoyne's line on 7 Oct (NPS, Gates's own report); Saratoga = turning point (French alliance)"],
                 ["B", "Before He Was a Traitor: Benedict Arnold's Charge That Won Saratoga", "92", "Charge decisive (Gates's report; Boot Monument: 'winning for his countrymen the decisive battle'); Gates commanded the army. A stronger-worded variant 'How Benedict Arnold Won the Battle of Saratoga' scored 96 but overclaims: not recommended"],
                 ["C", "Benedict Arnold's Top 3 Legendary Tactical Moves | Before He Became a Traitor", "91", "True (treason 1780, all three moves 1775-77)"]], [8, 82, 12, 68]),
          P("The owner picks the main title and main thumbnail; the others go into Test &amp; compare. Judge on CTR and impressions on days 1-3, SEPARATELY from retention at 0:30 and 1:00.", "warn"),
          Table([[img(TA, 82), img(TB, 82)], [img("youtube/thumbs_feed_strip.jpg", 82), ""]], colWidths=[85 * mm, 85 * mm]),
          P("Thumbnails by vidIQ (references: 3 Tactical Genius thumbnails): A NO COMMAND (86; true: he had no command on 7 Oct; fits titles A, B), B BEFORE THE TREASON (85; fits titles B, C). The portrait is an AI-generated generic Continental general in colour, not a likeness of Arnold (no life portrait in colour exists); banner spelling checked; B's map label was misspelled by the AI (HUOSON) and repainted from A. The fort is drawn as a star-shaped log fort: Breymann's redoubt was a log breastwork, so it is an illustration, not a plan.", "warn"), PageBreak()]
story += [P("3. Description (copy and paste)", "h1"), P("The first line is the title. NO links (channel rule). Keep the credit lines. Add the business email if you use one.", "warn"), Preformatted(desc, S["mono"], maxLineLength=100), PageBreak()]
story += [P("4. Upload settings", "h1"),
          table([["Setting", "Value"], ["Tags", open("youtube/tags.txt").read().strip()], ["Category", "Education"], ["Audience", "Not made for kids"],
                 ["Captions", "English; auto-caption, then check names (Kennebec, Chaudière, bateaux, Sault-au-Matelot, Valcour, Skenesborough, Pellew, Burgoyne, Breymann, Bemis Heights, Mahan)"],
                 ["Altered or synthetic content", "Yes: AI narration and AI thumbnails. Tick the box."], ["Chapters", "Automatic from the description (first at 0:00)"],
                 ["Pinned comment", "Which was Arnold's greatest move: 1, 2 or 3? And which commander should we cover next?"],
                 ["End screen", "From the channel's busiest video (Morgan or Thomas) plus subscribe, over the last ~20 s"],
                 ["Publish order (DATA_RULES)", "Revolution = proven era: publish right after a hot upload, never after a flop"]], [45, 125]),
          P("Upload checklist", "h2"), *bullets(["Play the master once (sound, sync, no black frames).", "Upload the master; paste title, description, tags; upload the main thumbnail (1280x720).", "Set up Test &amp; compare with the other titles/thumbnails.", "Tick 'altered or synthetic content'; add end screen; schedule.", "Days 1-3: run the standard Studio prompt (research/DATA_RULES.md) and log it in research/CHANNEL_LOG.md."]),
          P("<b>Facts to double-check</b> (arnold/research/FACT_NOTES.md, FACTCHECK_A/B/C): Quebec losses differ by source (30-60 killed, about 400 captured); surrender about 6,000 (NPS ~6,300 soldiers); Valcour vessels lost 10 or 11 of 15; the Quebec wound's side (left) rests on biographies, not the journals; how Arnold reached the field on 7 Oct is disputed (said so in the video). Gemini items NOT used: 'no man shall keep me in my tent', 'ball through my heart', '5,791', '88 vs 83 guns', '545 vs 1,032 lb', 'Ferris Bay', the officers' petition.", "warn")]
out = "build/Arnold-publishing-guide.pdf"
SimpleDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm, title="Benedict Arnold - publishing guide").build(story, onFirstPage=page, onLaterPages=page)
print(out)
