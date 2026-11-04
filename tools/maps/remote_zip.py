#!/usr/bin/env python3
"""remote_zip.py URL [NAME_SUBSTR ... -o DIR] : list a remote zip via HTTP Range requests, or extract only the named members (no full download)."""
import sys, io, os, zipfile, urllib.request
class RFile(io.RawIOBase):
    def __init__(s, url):
        s.url = url; s.pos = 0
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=0-0"}))
        s.size = int(r.headers["Content-Range"].split("/")[1]); s.url = r.geturl()
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s, o, w=0):
        s.pos = o if w == 0 else s.pos + o if w == 1 else s.size + o; return s.pos
    def read(s, n=-1):
        if n < 0: n = s.size - s.pos
        if n == 0 or s.pos >= s.size: return b""
        end = min(s.pos + n, s.size) - 1
        r = urllib.request.urlopen(urllib.request.Request(s.url, headers={"Range": f"bytes={s.pos}-{end}"}), timeout=300)
        d = r.read(); s.pos += len(d); return d
    def readinto(s, b): d = s.read(len(b)); b[:len(d)] = d; return len(d)
if __name__ == "__main__":
    a = sys.argv[1:]; out = "."
    if "-o" in a: i = a.index("-o"); out = a[i + 1]; del a[i:i + 2]
    z = zipfile.ZipFile(io.BufferedReader(RFile(a[0]), 1 << 20))
    if len(a) == 1:
        for i in z.infolist(): print(i.filename, i.file_size)
    else:
        for i in z.infolist():
            if any(k in i.filename for k in a[1:]):
                p = os.path.join(out, os.path.basename(i.filename)); open(p, "wb").write(z.read(i)); print("got", p)
