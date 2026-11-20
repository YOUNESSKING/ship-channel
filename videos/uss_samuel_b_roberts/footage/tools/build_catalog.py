#!/usr/bin/env python3
"""build_catalog.py - footage.json + FOOTAGE_LIST.md for the Samuel B. Roberts video. Inputs: nara_photos_meta.jsonl, nara_docs_meta.jsonl, nara_films_meta.jsonl, commons_meta.jsonl, noaa_meta.jsonl, overrides.json, film_notes.py"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(ROOT); sys.path.insert(0, HERE)
from film_notes import N as FN, NOAA as NN
from PIL import Image
J = lambda f: [json.loads(l) for l in open(f)] if os.path.exists(f) else []
OV = json.load(open('overrides.json')) if os.path.exists('overrides.json') else {}
esc = lambda s: (s or '').replace('|', '/').replace('\n', ' ')
GROUPS = {'A': 'Samuel B. Roberts (DE-413) herself, 1944', 'B': 'People: Copeland, Evans, Sprague, Kurita', 'C': 'Battle off Samar, 25 Oct 1944 (80-G / NH photos from Taffy 3)',
 'D': 'Taffy 3 ships in other moments: carriers and escorts (portraits, ILLUSTRATIVE for the day)', 'E': 'Sister John C. Butler-class destroyer escorts and DE plans (ILLUSTRATIVE)',
 'F': 'Japanese ships: Yamato, Musashi, Kongo, Chokai, Haguro, Tone, Chikuma, Noshiro (Center Force)', 'G': 'Leyte Gulf context: Sibuyan Sea, Cape Engano, Princeton, Suwannee and Sangamon kamikaze (other task groups)',
 'H': 'NARA documents: the real Samuel B. Roberts action report (20 Nov 1944) and War History pages', 'I': 'Namesake ships and survivors (1985-86 DVIC stills, FFG-58, 1988 mine strike)',
 'J': 'Deep ocean and deep submergence (ILLUSTRATIVE): Trieste 1960 with DE-535 Lewis, Alvin, NOAA ROV stills', 'K': 'USAAF 13th AF photos of the Japanese force in the Sulu Sea, 26-27 Oct 1944'}
FG = {'A': 'Taffy 3 / Samar-day film', 'B': 'Japanese air attack on carriers (other task groups, ILLUSTRATIVE)', 'C': 'Escort-carrier flight operations 1944', 'D': 'Smoke screens, Leyte shipping, destroyers, aerials (ILLUSTRATIVE)', 'E': 'Abandon ship and rescue (ILLUSTRATIVE)', 'F': 'Burning ships / ASW (ILLUSTRATIVE)', 'G': 'Deep ocean, NOAA Ocean Exploration (ILLUSTRATIVE)'}
NARA_REC = {'80-G-270516': 221950187, '80-G-287497': 221950379, '80-G-48888': 221950377, '80-G-288881': 221950390, '80-G-287512': 221949729, '80-G-272555': 221950371, '80-G-288099': 221950385}
GEN = {'C': 'Ship identity and exact time come from the Commons/NHHC/NARA caption only; hull numbers not legible unless the shows text says so; no sound',
 'D': 'Not the Battle off Samar day unless the date says 25 Oct 1944; ship portraits show the ship before/after the battle', 'E': 'Not Samuel B. Roberts: another ship of the class, label ILLUSTRATIVE',
 'F': 'Japanese ship identity is the Commons/NHHC caption; not at Samar unless the date says 25 Oct 1944', 'G': 'Not the Battle off Samar (Halsey / TF 38 / Sibuyan Sea / other days)', 'J': 'Not the Samuel B. Roberts wreck; ILLUSTRATIVE only',
 'A': 'Photo taken before the battle (Oct 1944 or earlier): not the wreck, not the battle', 'B': 'Portrait only', 'K': 'Army Air Forces photos, Sulu Sea 26-27 Oct 1944: not Samar'}
def grp(t):
    T = t.lower()
    if re.search(r'samuel b\.? roberts|nh_96011|nh_90603', T) and 'ffg' not in T and 'mighty' not in T and 'frigate' not in T: return 'A'
    if re.search(r'copeland|evans|sprague|kurita|nh_92320', T): return 'B'
    if re.search(r'trieste|alvin|lewis \(de-535\)|330-psa|noaa|bathyscaph', T): return 'J'
    if re.search(r'john c\.? butler|raymond|dennis|profile', T) and 'making smoke' not in T and 'heermann' not in T: return 'E'
    if re.search(r'yamato|musashi|kongo|chokai|haguro|tone|kumano|noshiro|chikuma|brunei|haruna', T) and 'samar' not in T: return 'F'
    if re.search(r'samar|80-g-2885|80-g-2875|80-g-2874|80-g-2705|80-g-48888|80-g-46989|80-g-378525|80-g-287497|80-g-288881|80-g-288882|80-g-288885|80-g-288886|80-g-287512|80-g-288149|80-g-288154|destroyers laying|smoke|kamikaze attacks uss white|l42-09.06.03|cve-71 launching|gambier bay and escorts|gambier bay \(cve-73\) under', T): return 'C'
    if re.search(r'suwannee|princeton|sibuyan|leyte|cape|80-g-272|80-g-288099|80-g-2871|80-g-46988|80-g-47162|visayan|under attack|sangamon', T): return 'G'
    if re.search(r'gambier|st\.? ?lo|kalinin|white plains|fanshaw|kitkun|johnston|hoel|heermann|cve', T): return 'D'
    return 'D'
P = []
def addphoto(**k):
    f = k['file']; im = Image.open(f); k['w'], k['h'] = im.size; P.append(k)
for m in J('nara_photos_meta.jsonl'):
    t = m['title']; stem = m['stem']; fam = 'K' if m['local'].startswith('342-FH') else ('I' if re.search(r'SAMUEL B', t, re.I) else 'D')
    shows = 'NARA caption: ' + t.strip()
    nots = {'K': 'Photos by the 13th AAF/USAAF, Sulu Sea 26-27 Oct 1944 (after Samar); caption says "Yamato class" but ship identity is the USAAF caption only; high-altitude bomb run, no US ships', 'I': 'Post-war ceremony/ship: not the 1944 DE-413. Survivors and guests are identifiable people: do not name them'}.get(fam, '')
    addphoto(stem=stem, group=fam, file=m['file'], title=f"{m['local']}: {t}", url='https://catalog.archives.gov/id/' + str(m['naId']), rights='NARA useRestriction: ' + json.dumps(m['use']), date=(m.get('date') or [''])[0] if isinstance(m.get('date'), list) else '', shows=shows, not_shows=nots, source='NARA')
for m in J('nara_docs_meta.jsonl'):
    addphoto(stem=m['stem'], group='H', file=m['file'], title=f"{m['title']} (page {m['page']} of {m['pages']})", url='https://catalog.archives.gov/id/' + str(m['naId']), rights='NARA useRestriction: ' + json.dumps(m['use']), date='1944-11-20' if m['naId'] == '78682556' else '1944', shows='Typed page of the NARA World War II war diary/action report series (microfilm scan). ' + m['note'], not_shows='A document page, no picture. Text pages must be readable on screen only if zoomed to the lines used', source='NARA')
for m in J('commons_meta.jsonl'):
    t = m['title'][5:]; g = grp(t + ' ' + m['stem']); loc = re.search(r'(80-G-\d+)', t)
    rights = 'Commons licence markers: ' + ', '.join(m['pdcats'][:4]) + '. Page: ' + m['url'] + '. Commons source field: ' + esc(m.get('source'))[:120]
    if loc and loc.group(1) in NARA_REC: rights += f'. NARA catalog record naId {NARA_REC[loc.group(1)]} (' + loc.group(1) + '): useRestriction {"status": "Unrestricted"} (record has no digitised copy)'
    d = m.get('desc') or ''
    addphoto(stem=m['stem'], group=g, file=m['file'], title=t, url=m['url'], rights=rights, date=m.get('date', '')[:30], shows='Commons title: ' + t + ('. Description: ' + d[:230] if d else ''), not_shows=GEN.get(g, ''), source='Wikimedia Commons (US Navy / NHHC / NARA / PD)')
for m in J('noaa_meta.jsonl'):
    if m['mime'].startswith('image'):
        addphoto(stem=m['stem'], group='J', file=m['file'], title=m['title'] or m['stem'], url=m['page'], rights='NOAA Ocean Exploration media-kit "Usage and Credit": credit NOAA Ocean Exploration; only items whose caption says "copyright" need extra permission (this caption does not). Caption: ' + esc(m['caption'])[:160], date=m['date'], shows='NOAA caption: ' + (m['caption'][:260] or m['title'] or 'no caption text'), not_shows='Not the Samuel B. Roberts wreck; ILLUSTRATIVE of the deep sea / ROV work only', source='NOAA Ocean Exploration')
for p in P:
    o = OV.get(p['stem'])
    if o:
        if o.get('shows'): p['shows'] = o['shows']
        if o.get('not'): p['not_shows'] = o['not']
        if o.get('group'): p['group'] = o['group']
P.sort(key=lambda p: (p['group'], p['stem']))
# ---------------- films
F = []
def probe(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', f], capture_output=True, text=True).stdout
    d = json.loads(r); return d['streams'][0]['width'], d['streams'][0]['height'], float(d['format']['duration'])
NR = ('NARA useRestriction: {"status": "Undetermined"} (NARA default for unreviewed RG 428 reels). Basis: US Navy camera-unit film (Record Group 428, Naval Photographic Center slate "428.NPC.<n>"), so a US federal work in the public domain. Where available the item is also on archive.org with Public Domain Mark.')
for m in J('nara_films_meta.jsonl'):
    nid = str(m['naId']); n = FN.get(nid)
    if not n: continue
    w, h, d = probe(m['file']); stem = m['stem']
    rights = NR if m['use'].get('status') == 'Undetermined' else 'NARA useRestriction: ' + json.dumps(m['use'])
    sheets = sorted(os.path.basename(x) for x in os.listdir('sheets') if x.startswith(stem + '_'))
    F.append(dict(stem=stem, group=n['group'], file=m['file'], title=f"{m['title']} ({m['local']})", url='https://catalog.archives.gov/id/' + nid, rights=rights, date=(m.get('date') or [''])[0] if isinstance(m.get('date'), list) else '', shows=n['shows'], not_shows=n['not_shows'], w=w, h=h, res=f'{w}x{h} H.264, NARA mp4 as downloaded (Digital Betacam copy, SD)', duration=round(d, 1), windows=[dict(**{'in': a, 'out': b, 'shows': s, 'not_shows': ns}) for a, b, s, ns in n['w']], avoid=n['avoid'], status='reviewed on a 10 s overview + 2 s sheets' if n['w'] else 'title-level only: overview not studied, check the 2 s sheets', sheets=sheets))
for m in J('noaa_meta.jsonl'):
    if not m['mime'].startswith('video'): continue
    nid = str(m['id']); n = NN.get(nid)
    if not n: continue
    w, h, d = probe(m['file']); stem = m['stem']; sheets = sorted(os.path.basename(x) for x in os.listdir('sheets') if x.startswith(stem + '_'))
    F.append(dict(stem=stem, group='G', file=m['file'], title=(m['title'] or n[0][:50]) + f' (NOAA media {nid})', url=m['page'], rights='NOAA Ocean Exploration media-kit "Usage and Credit": "All video on the portal is in the public domain and should be credited to NOAA Ocean Exploration"; only captions containing "copyright" need permission. This item\'s caption: ' + esc(m['caption'])[:150], date=m['date'], shows=n[0], not_shows=n[1] + '. ILLUSTRATIVE deep ocean b-roll only: not the Samuel B. Roberts wreck, not the 2022 dives', w=w, h=h, res=f'{w}x{h} H.264 as published', duration=round(d, 1), windows=[dict(**{'in': 0, 'out': int(d), 'shows': n[0], 'not_shows': ''})], avoid='none noted (no slate)', status='reviewed from caption; whole clip is usable', sheets=sheets))
F.sort(key=lambda f: (f['group'], f['stem']))
json.dump(dict(photos=P, films=F, groups=GROUPS, film_groups=FG), open('footage.json', 'w'), indent=1)
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
o = [open('tools/list_head.md').read()]
for g in sorted(GROUPS):
    it = [p for p in P if p['group'] == g]
    if not it: continue
    o.append(f'### {g}. {GROUPS[g]} ({len(it)})\n'); o.append('| stem | date | px | shows | does NOT show | record | rights |\n|---|---|---|---|---|---|---|')
    for p in it: o.append(f"| `{p['stem']}` | {esc(p['date'])} | {p['w']}x{p['h']} | {esc(p['shows'])} | {esc(p['not_shows'])} | {p['url']} | {esc(p['rights'])} |")
    o.append('')
o.append('## Films and video\n')
for g in sorted(FG):
    it = [f for f in F if f['group'] == g]
    if not it: continue
    o.append(f'### Group {g}: {FG[g]}\n')
    for f in it:
        o.append(f"#### `{f['stem']}`: {esc(f['title'])}"); o.append(f"- file `{f['file']}`, {f['res']}, {mm(f['duration'])} ({f['duration']} s), date {esc(f['date'])}; record {f['url']}")
        o.append(f"- rights: {esc(f['rights'])}"); o.append(f"- shows: {esc(f['shows'])}"); o.append(f"- does NOT show: {esc(f['not_shows'])}")
        o.append(f"- avoid: {esc(f['avoid'])}; status: {f['status']}; sheets: {len(f['sheets'])} (`sheets/{f['stem']}_NN.jpg`)")
        if f['windows']:
            o.append('- windows (seconds from file start):')
            for w in f['windows']: o.append(f"  - {mm(w['in'])}-{mm(w['out'])} ({w['in']}-{w['out']} s): {esc(w['shows'])}" + (f" / not: {esc(w['not_shows'])}" if w['not_shows'] else ''))
        o.append('')
open('FOOTAGE_LIST.md', 'w').write('\n'.join(o)); print(len(P), 'photos', len(F), 'films')
