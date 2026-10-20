import numpy as np, wave, sys
sr=44100
rng=np.random.default_rng(7)
def formant(x,centers,widths,gains):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/sr);H=np.zeros_like(f)
    for c,w,g in zip(centers,widths,gains): H+=g*np.exp(-0.5*((f-c)/w)**2)
    H+=0.05
    return np.fft.irfft(X*H,len(x))
def cluck(scale,dur=None):
    dur=dur or rng.uniform(0.07,0.13)
    n=int(dur*sr);t=np.arange(n)/sr
    f0=scale*np.interp(t/dur,[0,0.25,1],[520,820,430])
    ph=2*np.pi*np.cumsum(f0)/sr
    x=sum((1/k**0.8)*np.sin(k*ph) for k in range(1,9))
    x*=(1+0.35*np.sin(2*np.pi*rng.uniform(35,60)*t))
    x+=0.25*rng.standard_normal(n)
    x=formant(x,[900*scale,2100*scale,3200],[250,500,600],[1.0,0.8,0.3])
    env=np.minimum(t/0.006,1)*np.exp(-t/(dur*0.45))
    x*=env
    return x/np.max(np.abs(x))
def flutter(dur=0.18):
    n=int(dur*sr);t=np.arange(n)/sr
    x=rng.standard_normal(n)*(0.6+0.4*np.sin(2*np.pi*22*t))
    x=formant(x,[1800,3500],[800,1200],[1,0.6])
    x*=np.minimum(t/0.01,1)*np.exp(-t/(dur*0.5))
    return x/np.max(np.abs(x))
def build(total,start,out):
    N=int(total*sr);bed=np.zeros(N)
    # clucks: sparse at start, denser as chickens flood in
    times=[]
    t=start
    while t<total-0.15:
        density=np.interp(t,[start,start+1.2,total],[4,10,14])  # clucks per second
        t+=rng.exponential(1/density)
        times.append(t)
    for t0 in times:
        if t0>total-0.2: break
        burst=rng.integers(1,4)
        tt=t0;sc=rng.uniform(0.75,1.35);amp=rng.uniform(0.25,1.0)
        for _ in range(burst):
            c=cluck(sc)*amp*np.interp(t0,[start,start+1.5,total],[0.5,1,1])
            i=int(tt*sr);j=min(N,i+len(c))
            if i<N: bed[i:j]+=c[:j-i]
            tt+=rng.uniform(0.11,0.19)
    for t0 in np.arange(start,total-0.3,0.35):
        f=flutter()*rng.uniform(0.15,0.35);i=int((t0+rng.uniform(0,0.2))*sr);j=min(N,i+len(f))
        if i<N: bed[i:j]+=f[:j-i]
    # gentle 'distance': low-pass via FFT
    X=np.fft.rfft(bed);fr=np.fft.rfftfreq(N,1/sr);X*=1/(1+(fr/4500)**4);bed=np.fft.irfft(X,N)
    bed/=np.max(np.abs(bed))
    fade=int(0.01*sr);bed[:fade]*=np.linspace(0,1,fade)
    pcm=(bed*0.9*32767).astype(np.int16)
    with wave.open(out,'wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
build(float(sys.argv[1]),float(sys.argv[2]),sys.argv[3])
