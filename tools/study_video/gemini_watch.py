#!/usr/bin/env python3
"""Let Google Gemini watch AND listen to a public YouTube video (Google fetches it; nothing is downloaded here).

Works from the cloud session too (YouTube blocks yt-dlp there). Needs a free key from
https://aistudio.google.com/apikey in the env var GEMINI_API_KEY (never print or commit it).

Usage:
    python3 tools/study_video/gemini_watch.py URL --ask design|sound|hook|full [--start 0 --end 180] [--model gemini-2.5-pro]
Writes research/video_study/<id>/gemini_<ask>_<start>-<end>.md
"""
import argparse, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "research" / "video_study"
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

RULES = ("Cite MM:SS for every claim. Separate SEEN from HEARD. Say 'not sure' instead of guessing. "
         "This is a study of a competitor's craft for our own original channel; describe, do not transcribe music.")
ASKS = {
    "sound": """You are a film sound designer. Map this video's SOUND DESIGN in detail.
1. A timeline table for the given window: time | what is seen | voice (paraphrase) | music (state: none/bed/build/drop, mood, instruments, tempo feel) | SFX (each one: what it is, e.g. whoosh, sub boom, riser, reverse swell, impact, sonar ping, water ambience, creature roar, UI blip, typing, heartbeat) | what the sound does for the viewer.
2. Patterns: how often hits land (per minute), what every hit is synced to (cut, text pop, reveal, word), how music drops before reveals and how long the silence lasts, risers (length, what they lead into), ambience beds under the voice, how loud music sits under voice (ducking), transitions between sections, any signature sound repeated as branding.
3. Voice: AI or human, pace (words per minute estimate), tone, processing (reverb, low end), pauses for effect.
4. The 10 most effective sound moments, each with time and why it works.
5. A recipe: 10 concrete, copyable rules a small channel could follow to get this level of sound design with stock SFX and self-made music.""",
    "design": """You are a motion designer. Describe the VISUAL DESIGN and EDITING in the given window.
1. Shot-by-shot table: time | shot length (s) | what is shown (footage / AI image / 2D drawing / 3D / map / chart / text card) | camera move or animation | on-screen text (exact words, font style, colour, position, how it animates) | transition into the next shot.
2. Graphics system: colour palette (hex guesses), fonts (style), arrows, circles, labels, scale comparisons, maps, the look of the art (engraving / painterly / photo), recurring templates.
3. Editing rhythm: average shot length, fastest and slowest stretches, how cuts sync to the voice and sound.
4. What makes this look premium, and what is cheap or repetitive.
5. 10 concrete rules a small channel could adopt.""",
    "hook": """Break down the HOOK (first 60 s) shot by shot: time | voice (verbatim if possible) | what is seen | sound | the retention trick used. Then: the central question, the promise, open loops, how many named creatures appear and when, when the first joke lands, and when the structure/roadmap is shown.""",
    "full": """Summarise the whole video: title promise, structure (every section with start time and what it covers, e.g. each prehistoric ocean or period and each animal), verdict or ranking system if any, how it ends, and length of each section. List every prehistoric animal and place named, with times.""",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--ask", choices=ASKS, default="sound")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=180)
    ap.add_argument("--model", default="gemini-2.5-pro")
    ap.add_argument("--fps", type=float, default=2.0, help="frames per second Gemini samples (default 2; 1 is Google's default)")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set (free key: https://aistudio.google.com/apikey).")
    vid = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", a.url)
    vid = vid[1] if vid else "video"
    whole = a.ask == "full"
    part = {"file_data": {"file_uri": f"https://www.youtube.com/watch?v={vid}"},
            "video_metadata": {"fps": 0.5 if whole else a.fps}}
    if not whole:
        part["video_metadata"].update(start_offset=f"{a.start}s", end_offset=f"{a.end}s")
    prompt = ASKS[a.ask] + ("" if whole else f"\nWindow: {a.start // 60}:{a.start % 60:02} to {a.end // 60}:{a.end % 60:02}.") + "\n" + RULES
    body = {"contents": [{"parts": [part, {"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "mediaResolution": "MEDIA_RESOLUTION_LOW" if whole else "MEDIA_RESOLUTION_MEDIUM"}}
    req = urllib.request.Request(API.format(model=a.model), data=json.dumps(body).encode(), method="POST",
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini HTTP {e.code}: {e.read().decode(errors='replace')[:800].replace(key, '[key]')}")
    text = "".join(p.get("text", "") for c in data.get("candidates", []) for p in c.get("content", {}).get("parts", []))
    use = data.get("usageMetadata", {})
    d = OUT / vid
    d.mkdir(parents=True, exist_ok=True)
    name = f"gemini_{a.ask}" + ("" if whole else f"_{a.start}-{a.end}") + ".md"
    (d / name).write_text(f"# Gemini {a.model} | {a.ask} | {a.url} | window {'whole' if whole else f'{a.start}-{a.end}s'}\n"
                          f"Tokens: {use.get('promptTokenCount')} in, {use.get('candidatesTokenCount')} out. "
                          "Evidence tag [G]: AI watch+listen, times about +/-2 s; check key claims by ear.\n\n" + text)
    print(d / name)
    print(text[:3000])


if __name__ == "__main__":
    main()
