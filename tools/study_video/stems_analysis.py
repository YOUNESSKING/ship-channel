#!/usr/bin/env python3
"""Sound layers of a studied video: run Demucs first (python3 -m demucs -n htdemucs -o <dir>/sound/stems <dir>/sound/full44.wav),
then: cd research/video_study/<id>/sound && python3 ../../../../tools/study_video/stems_analysis.py
Prints voice/music/SFX levels, ducking, SFX transients per minute; writes sfx_transients.csv and stems_map_0-3min.png."""
import numpy as np, subprocess, sys, json
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
S="stems/htdemucs/full44/"
def load(n):
    raw=subprocess.run(["ffmpeg","-loglevel","error","-i",S+n+".wav","-ac","1","-ar","22050","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
st={n:load(n) for n in ["vocals","drums","bass","other"]}
hop=2205  # 0.1 s
def rms_db(x):
    n=len(x)//hop; return 20*np.log10(np.maximum(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1)),1e-6))
L={k:rms_db(v) for k,v in st.items()}
music=st["other"]+st["bass"]
L["music"]=rms_db(music)
n=min(len(v) for v in L.values()); t=np.arange(n)*0.1
for k in L: L[k]=L[k][:n]
voc_on=L["vocals"]>-40
print("voice active % :", round(voc_on.mean()*100,1))
for k in ["vocals","music","drums","bass","other"]:
    a=L[k]; print(f"{k:7s} median dB {np.median(a):6.1f}  while voice {np.median(a[voc_on]):6.1f}  in gaps {np.median(a[~voc_on]) if (~voc_on).any() else 0:6.1f}  p95 {np.percentile(a,95):6.1f}")
gap=L["vocals"][voc_on]-L["music"][voc_on]
print("voice over music (dB) median", round(float(np.median(gap)),1), "p10", round(float(np.percentile(gap,10)),1), "p90", round(float(np.percentile(gap,90)),1))
# ducking: music level when voice on vs off
print("music when voice off minus on:", round(float(np.median(L['music'][~voc_on])-np.median(L['music'][voc_on])),1))
# music continuity: fraction of time music above -45
print("music present % (>-45 dBFS):", round((L["music"]>-45).mean()*100,1))
# SFX transients in drums stem (20ms frames)
d=st["drums"]; h=441; m=len(d)//h
e=20*np.log10(np.maximum(np.sqrt((d[:m*h].reshape(m,h)**2).mean(1)),1e-6)); et=np.arange(m)*h/22050
base=np.convolve(e,np.ones(50)/50,mode="same")
ev=[];last=-9
for i in range(1,m):
    if e[i]-base[i]>10 and e[i]-e[i-1]>6 and e[i]>-40 and et[i]-last>0.25: ev.append(round(float(et[i]),2)); last=et[i]
ev=np.array(ev)
print("drum-stem transients (SFX hits/clicks/whooshes):", len(ev), "=", round(len(ev)/(t[-1]/60),1), "/min; first 30s:", int((ev<30).sum()), "; first 60s:", int((ev<60).sum()))
np.savetxt("sfx_transients.csv",ev,fmt="%.2f",header="t (s) of SFX transients from the demucs drums stem")
# per-minute table
print("min | sfx | voice% | music dB(med)")
for mn in range(10):
    s=(t>=mn*60)&(t<(mn+1)*60)
    print(mn, int(((ev>=mn*60)&(ev<(mn+1)*60)).sum()), round(voc_on[s].mean()*100), round(float(np.median(L['music'][s])),1))
# music tempo estimate via onset autocorrelation on 'other' (simple)
o=st["other"]; h2=512; m2=len(o)//h2
env=np.sqrt((o[:m2*h2].reshape(m2,h2)**2).mean(1)); flux=np.maximum(np.diff(env),0)
ac=np.correlate(flux[:20000]-flux[:20000].mean(),flux[:20000]-flux[:20000].mean(),"full")[19999:]
fr=22050/h2; lags=np.arange(len(ac))/fr
sel=(lags>0.33)&(lags<1.5); bl=lags[sel][np.argmax(ac[sel])]
print("music beat estimate: ~", round(60/bl), "BPM (rough)")
# spectral centroid of music
spec=np.abs(np.fft.rfft(music[:2048*640].reshape(-1,2048)*np.hanning(2048),axis=1)).mean(0); f=np.fft.rfftfreq(2048,1/22050)
print("music spectral centroid Hz:", int((spec*f).sum()/spec.sum()), "; energy <200Hz %:", round(float(spec[f<200].sum()/spec.sum()*100),1))
# plot first 3 minutes
fig,axs=plt.subplots(3,1,figsize=(20,9))
for r in range(3):
    ax=axs[r]; s=(t>=r*60)&(t<(r+1)*60)
    ax.plot(t[s],L["vocals"][s],color="black",lw=0.8,label="voice")
    ax.plot(t[s],L["music"][s],color="tab:blue",lw=1,label="music (other+bass)")
    ax.plot(t[s],L["drums"][s],color="tab:orange",lw=0.6,alpha=0.7,label="drums stem (SFX/percussion)")
    for x in ev[(ev>=r*60)&(ev<(r+1)*60)]: ax.axvline(x,color="red",lw=0.6,alpha=0.6)
    ax.set_xlim(r*60,(r+1)*60); ax.set_ylim(-70,-5)
axs[0].legend(loc="lower right"); axs[0].set_title("Depth Theory sperm whale 0:00-3:00: stems (red = SFX transient)")
fig.tight_layout(); fig.savefig("stems_map_0-3min.png",dpi=80)
