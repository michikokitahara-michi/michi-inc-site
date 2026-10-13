import random, math
W,H=1440,820
FOC=(560,600)
rnd=random.Random(21)
pts=[FOC]
# poisson-ish
tries=0
while tries<60000:
    tries+=1
    p=(rnd.uniform(-40,W+40),rnd.uniform(-40,H+40))
    # slightly sparser in the central text area
    cx,cy=(p[0]-720)/330,(p[1]-410)/170
    md=118 if cx*cx+cy*cy<1 else 92
    if all(math.dist(p,q)>=md for q in pts): pts.append(p)
pts=[(round(x),round(y)) for x,y in pts]
def inter(p1,p2,p3,p4):
    if len({p1,p2,p3,p4})<4: return False
    def ccw(a,b,c): return (c[1]-a[1])*(b[0]-a[0])-(b[1]-a[1])*(c[0]-a[0])
    return (ccw(p1,p3,p4)>0)!=(ccw(p2,p3,p4)>0) and (ccw(p1,p2,p3)>0)!=(ccw(p1,p2,p4)>0)
cand=sorted((math.dist(p,q),i,j) for i,p in enumerate(pts) for j,q in enumerate(pts) if i<j)
edges=[];deg=[0]*len(pts)
for d,i,j in cand:
    if d>185: break
    if deg[i]>=5 or deg[j]>=5: continue
    if any(inter(pts[i],pts[j],pts[a],pts[b]) for a,b in edges): continue
    edges.append((i,j));deg[i]+=1;deg[j]+=1
# keep a subset to stay airy
rnd.shuffle(edges)
edges=edges[:int(len(edges)*0.9)]
fd=lambda p: math.dist(p,FOC)
maxd=max(fd(p) for p in pts)
# style per dot
dots=[]
for i,p in enumerate(pts):
    if i==0: r,black=9,True
    else:
        black=rnd.random()<0.16
        r=rnd.choice([5,6,7]) if black else rnd.choice([3,3.5,4,4.5,5])
    turn = (not black) and rnd.random()<0.38   # turns black at the end
    dots.append((p,r,black,turn))

from collections import deque
adj={i:[] for i in range(len(pts))}
for i,j in edges: adj[i].append(j); adj[j].append(i)
depth={0:0}; q=deque([0])
while q:
    u=q.popleft()
    for v in adj[u]:
        if v not in depth: depth[v]=depth[u]+1; q.append(v)
for i in range(len(pts)):
    if i not in depth: depth[i]=None
maxdep=max(d for d in depth.values() if d is not None)
T0,T1=17.0,74.0   # % of cycle: when spreading starts / ends
DUR=3.6          # % of cycle an edge takes to draw (~0.6s)
step=(T1-T0-DUR)/max(1,maxdep)
jr=random.Random(5)
def nd(i):  # depth with fallback for isolated
    return depth[i] if depth[i] is not None else round(fd(pts[i])/maxd*maxdep)
edge_t={}
for i,j in edges:
    a,b=(i,j) if nd(i)<=nd(j) else (j,i)
    edge_t[(a,b)]=T0+nd(a)*step+jr.uniform(0,step*0.9)
dot_t={}
for i in range(len(pts)):
    if i==0: dot_t[i]=0.0; continue
    inc=[t for (a,b),t in edge_t.items() if b==i or a==i]
    first=min(inc) if inc else T0+nd(i)*step
    dot_t[i]=min(first-2.0, 0.8+fd(pts[i])/maxd*15+jr.uniform(-0.8,0.8))
    dot_t[i]=max(0.5,dot_t[i])
# bucket times to limit CSS size
def tb(t): return round(t*2)/2
E_T=sorted(set(tb(t) for t in edge_t.values())); V_T=sorted(set(tb(t) for t in dot_t.values()))
near=set([0]+[j for i,j in edges if i==0]+[i for i,j in edges if j==0])
def layer():
    out=[]
    for (a,b),t in edge_t.items():
        A,B=pts[a],pts[b]; L=round(math.dist(A,B),1)
        dark=(dots[a][2] or dots[a][3]) and (dots[b][2] or dots[b][3])
        k=E_T.index(tb(t))
        out.append(f'<line class="e t{k}{" ek" if dark else ""}" x1="{A[0]}" y1="{A[1]}" x2="{B[0]}" y2="{B[1]}" style="--l:{L}"></line>')
    for i,(p,r,black,turn) in enumerate(dots):
        fill='#111111' if black else '#A6A6A6'
        k=V_T.index(tb(dot_t[i]))
        out.append(f'<circle class="v u{k}{" vk" if turn else ""}" cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{fill}"></circle>')
    return '\n'.join(out)
svg=f"""<svg class="net" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style="position: absolute; inset: 0; width: 100%; height: 100%; overflow: hidden">
<defs><filter id="dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.2"></feGaussianBlur></filter></defs>
<g class="cam">
<g class="soft" filter="url(#dof)">
{layer()}
</g>
<g class="crisp">
{layer()}
</g>
</g>
</svg>"""
css=[]
css.append(f'.cam{{transform-origin:{FOC[0]}px {FOC[1]}px;transform-box:view-box;animation:cam 16s cubic-bezier(.45,0,.2,1) infinite}}')
css.append('@keyframes cam{0%{transform:scale(3.2)}20%,100%{transform:scale(1)}}')
css.append('.soft{animation:soft 16s ease infinite}@keyframes soft{0%,3%{opacity:1}17%,100%{opacity:0}}')
css.append('.crisp{animation:crisp 16s ease infinite}@keyframes crisp{0%,3%{opacity:0}17%,96.2%{opacity:1}100%{opacity:0}}')
css.append('.e{stroke:#C9C9C9;stroke-width:1;fill:none;stroke-dasharray:var(--l) 99999;stroke-dashoffset:var(--l)}')
css.append('.v{transform-box:fill-box;transform-origin:center;opacity:0}')
for k,t in enumerate(E_T):
    css.append(f'.t{k}{{animation:t{k} 16s cubic-bezier(.4,0,.2,1) infinite}}@keyframes t{k}{{0%,{t:.1f}%{{stroke-dashoffset:var(--l)}}{t+DUR:.1f}%,100%{{stroke-dashoffset:0}}}}')
    css.append(f'.ek.t{k}{{animation:t{k} 16s cubic-bezier(.4,0,.2,1) infinite,ek 16s ease infinite}}')
for k,t in enumerate(V_T):
    css.append(f'.u{k}{{animation:u{k} 16s ease-out infinite}}@keyframes u{k}{{0%,{t:.1f}%{{opacity:0;transform:scale(0)}}{t+2.2:.1f}%,96.2%{{opacity:1;transform:scale(1)}}100%{{opacity:0;transform:scale(1)}}}}')
    css.append(f'.vk.u{k}{{animation:u{k} 16s ease-out infinite,vk 16s ease infinite}}')
css.append('@keyframes vk{0%,74%{fill:#A6A6A6}82%,100%{fill:#111111}}')
css.append('@keyframes ek{0%,74%{stroke:#C9C9C9}82%,100%{stroke:#7A7A7A}}')
css.append('@media (prefers-reduced-motion: reduce){.cam,.soft,.crisp,.e,.v{animation:none!important}.cam{transform:none}.soft{opacity:0}.crisp{opacity:1}.e{stroke-dashoffset:0}.v{opacity:1;transform:none}.crisp .vk{fill:#111111}.crisp .ek{stroke:#7A7A7A}.ph{display:none}.fin{animation:none!important;opacity:1!important}}')
out_css='\n'.join(css)
print('maxdep',maxdep,'edges',len(edges),'E_T',len(E_T),'V_T',len(V_T))
