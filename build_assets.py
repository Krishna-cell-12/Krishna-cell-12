"""
Generates every SVG used by README.md (blue theme).
Run:  python build_assets.py
Optional: put your photo at assets/photo.jpg (or .png/.webp) first -> it is embedded in the hero banner.
"""
import os, io, base64, random
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets")
os.makedirs(A, exist_ok=True)

# ---------- palette ----------
BG, ACC, ACC2, SOFT = "#060B16", "#58A6FF", "#1F6FEB", "#A5D6FF"
TXT, MUT, CARD1, CARD2 = "#E6EDF3", "#7D93B2", "#0C1E3F", "#071225"

CSS = """
.serif{font-family:Georgia,'Times New Roman',serif}
.mono{font-family:Consolas,'SFMono-Regular','Courier New',monospace}
.sans{font-family:'Segoe UI',Helvetica,Arial,sans-serif}
.it{font-style:italic}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
.pulse{animation:pulse 2.4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.fl{animation:float 5s ease-in-out infinite}
@keyframes slide{0%{transform:translateX(0)}50%{transform:translateX(1100px)}100%{transform:translateX(0)}}
.slide{animation:slide 9s ease-in-out infinite}
@keyframes show{to{opacity:1}}
.ln{opacity:0;animation:show .3s forwards}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.blink{animation:blink 1s steps(1) infinite}
"""

def svg(w, h, body, css="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
<linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CARD1}"/><stop offset="1" stop-color="{CARD2}"/></linearGradient>
<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{ACC2}"/><stop offset="1" stop-color="{ACC2}" stop-opacity="0"/></linearGradient>
<radialGradient id="glow" cx="0.85" cy="0.05" r="0.9"><stop offset="0" stop-color="{ACC2}" stop-opacity="0.38"/><stop offset="1" stop-color="{ACC2}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="{ACC2}" stroke-opacity="0.07"/></pattern>
{defs}
</defs>
<style>{CSS}{css}</style>
{body}
</svg>'''

def card(x, y, w, h, r=18, grid=False):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#card)"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glow)"/>'
    if grid:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#grid)"/>'
    s += f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" stroke="{ACC2}" stroke-opacity="0.38"/>'
    return s

def stars(n, x0, y0, x1, y1, seed=1):
    rnd = random.Random(seed); s = ""
    for _ in range(n):
        s += (f'<circle class="pulse" cx="{rnd.randint(x0,x1)}" cy="{rnd.randint(y0,y1)}" r="{rnd.choice([1,1,1.5,2])}" '
              f'fill="{SOFT}" style="animation-delay:{rnd.random()*3:.2f}s"/>')
    return s

def save(name, s):
    with open(os.path.join(A, name), "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", name, len(s)//1024, "KB")

def pills(x, y, tags):
    out, cx = "", x
    for t in tags:
        w = len(t) * 7 + 24
        out += (f'<rect x="{cx}" y="{y}" width="{w}" height="24" rx="12" fill="#0B1F42" stroke="{ACC2}" stroke-opacity=".5"/>'
                f'<text x="{cx+w/2}" y="{y+16}" text-anchor="middle" class="mono" font-size="11" fill="{SOFT}">{esc(t)}</text>')
        cx += w + 10
    return out

# ================= HERO =================
def hero():
    photo_tag = None
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = os.path.join(A, f"photo.{ext}")
        if os.path.exists(p):
            try:
                from PIL import Image
                im = Image.open(p).convert("RGB")
                tw, th = 400, 400                      # crop to the square for the circle frame
                r = max(tw / im.width, th / im.height)
                im = im.resize((int(im.width * r), int(im.height * r)))
                l, t = (im.width - tw) // 2, (im.height - th) // 6
                im = im.crop((l, t, l + tw, t + th))
                buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
                data = base64.b64encode(buf.getvalue()).decode()
            except Exception:
                data = base64.b64encode(open(p, "rb").read()).decode()
            photo_tag = (f'<image href="data:image/jpeg;base64,{data}" x="880" y="135" width="200" height="200" '
                         f'preserveAspectRatio="xMidYMid slice" clip-path="url(#arch)"/>')
    if not photo_tag:
        photo_tag = (f'<circle cx="980" cy="235" r="100" fill="#0B1F42"/>'
                     f'<text x="980" y="257" text-anchor="middle" class="serif it" font-size="64" fill="{SOFT}" opacity=".85">KA</text>')
    defs = '<clipPath id="arch"><circle cx="980" cy="235" r="100"/></clipPath>'
    b = card(0, 0, 1200, 480, 20, grid=True) + stars(26, 40, 30, 1160, 440, 7)
    b += f'<rect x="60" y="40" width="330" height="34" rx="17" fill="#050A14" stroke="{ACC2}" stroke-opacity=".5"/>'
    b += f'<circle class="pulse" cx="82" cy="57" r="4" fill="{ACC}"/>'
    b += f'<text x="98" y="62" class="mono" font-size="12" fill="{MUT}">~/krishna <tspan fill="{ACC}">$</tspan> <tspan fill="{TXT}" font-weight="bold">build --from-kernel-up</tspan></text>'
    b += f'<line x1="60" y1="108" x2="95" y2="108" stroke="{ACC}"/><text x="108" y="112" class="mono" font-size="12" letter-spacing="4" fill="{ACC}">FULL-STACK · ML / AI · SYSTEMS</text>'
    b += f'<text x="58" y="215" class="serif" font-size="104" fill="#FFFFFF">Krishna</text>'
    b += f'<text x="58" y="310" class="serif it" font-size="104" fill="{SOFT}">Abhang<tspan fill="{ACC}">.</tspan></text>'
    b += f'<rect x="60" y="328" width="560" height="2" fill="url(#line)"/>'
    b += f'<text x="60" y="366" class="mono" font-size="13" letter-spacing="3" fill="{TXT}">FULL STACK DEVELOPER · ML/AI · SYSTEMS PROGRAMMER</text>'
    b += f'<text x="60" y="400" class="serif it" font-size="21" fill="{MUT}">Building software, from the kernel up.</text>'
    b += f'<line x1="60" y1="435" x2="1140" y2="435" stroke="{ACC2}" stroke-opacity=".3"/>'
    b += f'<text x="60" y="460" class="mono" font-size="11" letter-spacing="2" fill="{MUT}">B.TECH CSE · VIT BHOPAL · CGPA 7.71</text>'
    b += f'<text x="1140" y="460" text-anchor="end" class="mono" font-size="11" letter-spacing="2" fill="{MUT}">FULL STACK INTERN &apos;26 · DEVELOPER @ BIHAAN.ORG</text>'
    # orbit + photo
    b += f'<circle cx="980" cy="235" r="185" stroke="{ACC2}" stroke-opacity=".25"/>'
    b += f'<circle class="spin" cx="980" cy="235" r="150" stroke="{ACC}" stroke-opacity=".55" stroke-dasharray="4 10"/>'
    b += f'<g class="fl">{photo_tag}'
    b += f'<circle cx="980" cy="235" r="100" stroke="{SOFT}" stroke-opacity=".7" stroke-width="1.5"/></g>'
    for (x, y, lab, dx, anchor) in [(980, 85, "ML", 12, "start"), (1110, 160, "API", 14, "start"),
                                    (1110, 310, "DATA", 14, "start"), (830, 235, "OS", -14, "end")]:
        b += f'<circle class="pulse" cx="{x}" cy="{y}" r="4" fill="{ACC}"/>'
        b += f'<text x="{x+dx}" y="{y+4}" text-anchor="{anchor}" class="mono" font-size="11" letter-spacing="2" fill="{MUT}">{lab}</text>'
    save("hero.svg", svg(1200, 480, b, defs=defs))

# ================= SECTION HEADERS =================
def header(fname, num, label, right, parts):
    b = f'<text x="36" y="26" class="mono" font-size="12" letter-spacing="3" fill="{ACC}"><tspan font-weight="bold" fill="{TXT}">{num}</tspan>  {esc(label)}</text>'
    b += f'<text x="1164" y="26" text-anchor="end" class="mono" font-size="11" letter-spacing="3" fill="{MUT}">{esc(right)}</text>'
    t = ""
    for txt, it in parts:
        t += f'<tspan class="{"it" if it else ""}" fill="{SOFT if it else "#FFFFFF"}">{esc(txt)}</tspan>'
    b += f'<text x="36" y="76" class="serif" font-size="46">{t}</text>'
    b += f'<rect x="36" y="90" width="1128" height="1.5" fill="url(#line)"/>'
    b += f'<circle class="slide" cx="36" cy="91" r="3.5" fill="{SOFT}"/>'
    save(fname, svg(1200, 104, b))

# ================= ABOUT TERMINAL =================
def about():
    lines = [("c", "whoami"), ("o", "Krishna Abhang · Full-Stack Developer · ML/AI"),
             ("c", "cat education.txt"), ("o", "B.Tech CSE · VIT Bhopal · CGPA 7.71 · class of 2028"),
             ("c", "cat experience.txt"), ("o", "Full Stack Developer Intern · Prashant Kumar LTD · 2026"),
             ("o", "Developer · BIHAAN.org · SEO & discoverability"),
             ("c", "ls ./shipped"), ("o", "nexusguard-ai  talentmatch-ai  os-kernel  lunar-ice-ipi"),
             ("c", "echo $FOCUS"), ("o", "full-stack · machine learning · systems · remote sensing")]
    b = card(0, 0, 1200, 380, 20)
    b += f'<rect x="30" y="24" width="700" height="332" rx="14" fill="#040912" stroke="{ACC2}" stroke-opacity=".4"/>'
    for i, c in enumerate([ACC2, ACC, SOFT]):
        b += f'<circle cx="{54+i*18}" cy="48" r="5" fill="{c}" opacity=".8"/>'
    b += f'<text x="380" y="52" text-anchor="middle" class="mono" font-size="11" fill="{MUT}">krishna@portfolio: ~</text>'
    b += f'<line x1="30" y1="68" x2="730" y2="68" stroke="{ACC2}" stroke-opacity=".25"/>'
    y = 96
    for i, (k, t) in enumerate(lines):
        d = f'style="animation-delay:{i*0.35:.2f}s"'
        if k == "c":
            b += f'<text class="mono ln" {d} x="52" y="{y}" font-size="13"><tspan fill="{ACC}">$</tspan> <tspan fill="#FFFFFF">{esc(t)}</tspan></text>'
        else:
            b += f'<text class="mono ln" {d} x="52" y="{y}" font-size="13" fill="{SOFT}" fill-opacity=".85"><tspan fill="{ACC2}">→</tspan> {esc(t)}</text>'
        y += 22
    b += f'<text class="mono ln" style="animation-delay:{len(lines)*0.35:.2f}s" x="52" y="{y}" font-size="13" fill="{ACC}">$</text>'
    b += f'<rect class="blink" x="68" y="{y-12}" width="8" height="15" fill="{SOFT}"/>'
    cards = [("FULL-STACK", "React · Node.js", "Next.js · FastAPI · Spring Boot"),
             ("ML / AI", "Python", "DBSCAN · Random Forest · FAISS"),
             ("SYSTEMS", "C · x86 Assembly", "custom OS kernel · QEMU")]
    for i, (lab, big, sub) in enumerate(cards):
        y0 = 24 + i * 110
        b += f'<rect x="770" y="{y0}" width="400" height="96" rx="12" fill="#07142B" stroke="{ACC2}" stroke-opacity=".35"/>'
        b += f'<rect x="770" y="{y0+10}" width="3" height="76" fill="{ACC}"/>'
        b += f'<text x="794" y="{y0+26}" class="mono" font-size="10" letter-spacing="3" fill="{ACC}">{lab}</text>'
        b += f'<text x="794" y="{y0+60}" class="serif" font-size="32" fill="#FFFFFF">{esc(big)}</text>'
        b += f'<text x="794" y="{y0+82}" class="sans" font-size="12" fill="{MUT}">{esc(sub)}</text>'
    save("about-terminal.svg", svg(1200, 380, b))

# ================= SNAPSHOT =================
def snapshot():
    b = card(0, 0, 1200, 400, 20)
    feats = [(30, "BAH'26", "NOW BUILDING · ISRO-THEMED HACKATHON", "Lunar Ice Detection", "BAH 2026 · Chandrayaan-2 DFSAR · IPI model"),
             (615, "INTERN", "EXPERIENCE · MAY – AUG 2026", "Full Stack Developer Intern", "Prashant Kumar LTD")]
    for x, ghost, lab, title, sub in feats:
        b += f'<rect x="{x}" y="24" width="555" height="170" rx="14" fill="#07142B" stroke="{ACC2}" stroke-opacity=".35"/>'
        b += f'<text x="{x+540}" y="110" text-anchor="end" class="serif it" font-size="92" fill="{ACC2}" fill-opacity=".14">{esc(ghost)}</text>'
        b += f'<text x="{x+24}" y="108" class="mono" font-size="10" letter-spacing="3" fill="{ACC}">{esc(lab)}</text>'
        b += f'<text x="{x+24}" y="150" class="serif" font-size="36" fill="#FFFFFF">{esc(title)}</text>'
        b += f'<text x="{x+24}" y="176" class="sans" font-size="13" fill="{MUT}">{esc(sub)}</text>'
    b += f'<line x1="60" y1="238" x2="1140" y2="238" stroke="{ACC2}" stroke-opacity=".35"/>'
    cols = [("ACADEMICS", "7.71", "CGPA · B.Tech CSE"), ("YEAR", "3rd", "VIT Bhopal · class of 2028"),
            ("INTERNSHIP", "1", "Full Stack · completed 2026"), ("PREP PLAN", "365", "day SDE placement plan"),
            ("CERTIFIED", "2", "Oracle Java · MongoDB DBA")]
    for i, (lab, val, sub) in enumerate(cols):
        x = 60 + i * 216
        b += f'<circle class="pulse" cx="{x}" cy="238" r="4" fill="{SOFT}" style="animation-delay:{i*.4}s"/>'
        b += f'<text x="{x}" y="276" class="mono" font-size="10" letter-spacing="3" fill="{ACC}">{lab}</text>'
        b += f'<text x="{x}" y="326" class="serif" font-size="52" fill="#FFFFFF">{val}</text>'
        b += f'<text x="{x}" y="354" class="sans" font-size="12" fill="{MUT}">{esc(sub)}</text>'
    save("snapshot.svg", svg(1200, 400, b))

# ================= PROJECT CARDS =================
def pipeline(labels, cap):
    b = f'<text x="970" y="38" text-anchor="middle" class="mono" font-size="10" letter-spacing="3" fill="{MUT}">{esc(cap)}</text>'
    ys = [60, 118, 176, 234]
    for i, (l, y) in enumerate(zip(labels, ys)):
        b += f'<rect x="860" y="{y}" width="220" height="40" rx="10" fill="#08142B" stroke="{ACC}" stroke-opacity="{.95 if i==3 else .4}"/>'
        b += f'<text x="970" y="{y+25}" text-anchor="middle" class="mono" font-size="13" fill="{TXT}">{esc(l)}</text>'
        if i < 3:
            b += f'<line x1="970" y1="{y+40}" x2="970" y2="{y+58}" stroke="{ACC2}" stroke-dasharray="3 3"/>'
    b += f'<circle class="drop" cx="970" cy="100" r="4" fill="{SOFT}"/>'
    css = "@keyframes drop{0%{transform:translateY(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(150px);opacity:0}}.drop{animation:drop 3s ease-in-out infinite}"
    return b, css

def layers(labels, cap):
    b = f'<text x="970" y="38" text-anchor="middle" class="mono" font-size="10" letter-spacing="3" fill="{MUT}">{esc(cap)}</text>'
    for i, l in enumerate(labels):
        y = 62 + i * 54
        pts = f"{880},{y} {1090},{y} {1070},{y+38} {860},{y+38}"
        b += (f'<g class="fl" style="animation-delay:{i*.5}s"><polygon points="{pts}" fill="#08142B" stroke="{ACC}" stroke-opacity="{.35+i*.2:.2f}"/>'
              f'<text x="975" y="{y+24}" text-anchor="middle" class="mono" font-size="12" fill="{TXT}">{esc(l)}</text></g>')
    return b, ""

def crater(cap):
    cx, cy = 970, 150
    b = f'<text x="970" y="38" text-anchor="middle" class="mono" font-size="10" letter-spacing="3" fill="{MUT}">{esc(cap)}</text>'
    for r, o in [(105, .3), (75, .5), (45, .8)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{ACC2}" stroke-opacity="{o}"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="44" fill="#040912"/>'
    b += f'<path class="sweep" d="M{cx},{cy} L{cx},{cy-105} A105,105 0 0 1 {cx+74},{cy-74} Z" fill="{ACC}" fill-opacity=".18"/>'
    for i, (dx, dy) in enumerate([(-15, 8), (12, -14), (20, 16), (-8, -18), (2, 24)]):
        b += f'<circle class="pulse" cx="{cx+dx}" cy="{cy+dy}" r="3" fill="{SOFT}" style="animation-delay:{i*.5}s"/>'
    b += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" class="mono" font-size="10" fill="{MUT}" opacity=".0">PSR</text>'
    b += f'<text x="970" y="275" text-anchor="middle" class="mono" font-size="11" letter-spacing="2" fill="{MUT}">PSR · permanently shadowed region</text>'
    css = ".sweep{transform-origin:970px 150px;animation:spin 6s linear infinite}"
    return b, css

def project(fname, meta, title, sub, built, stats, tags, diagram):
    d, css = diagram
    b = card(0, 0, 1200, 310, 20, grid=True)
    b += f'<text x="50" y="52" class="mono" font-size="11" letter-spacing="3" fill="{ACC}">{esc(meta)}</text>'
    b += f'<text x="48" y="112" class="serif" font-size="54" fill="#FFFFFF">{esc(title)}</text>'
    b += f'<text x="50" y="146" class="sans" font-size="17" fill="{TXT}" fill-opacity=".85">{esc(sub)}</text>'
    b += f'<text x="50" y="176" class="mono" font-size="12" fill="{MUT}"><tspan fill="{ACC2}">BUILT ›</tspan> {esc(built)}</text>'
    b += f'<line x1="50" y1="196" x2="760" y2="196" stroke="{ACC2}" stroke-opacity=".35"/>'
    for i, (v, l) in enumerate(stats):
        x = 50 + i * 240
        b += f'<text x="{x}" y="236" class="serif" font-size="34" fill="#FFFFFF">{esc(v)}</text>'
        b += f'<text x="{x}" y="256" class="sans" font-size="12" fill="{MUT}">{esc(l)}</text>'
    b += pills(50, 270, tags)
    b += d
    save(fname, svg(1200, 310, b, css=css))

# ================= TOOLKIT =================
def toolkit():
    cells = [("01  LANGUAGES", "Java", "Python", "C · x86 ASM · TypeScript · JavaScript"),
             ("02  AI · ML", "ML & Embeddings", "DBSCAN · Random Forest", "FAISS · Gemini API · Groq"),
             ("03  FRONTEND", "React", "Next.js · TypeScript", "Tailwind · Framer Motion · Zustand"),
             ("04  BACKEND & APIS", "Node.js", "FastAPI · Spring Boot", "REST APIs · Express"),
             ("05  DATA & INFRA", "MongoDB", "Docker · AWS EC2", "Polygon blockchain"),
             ("06  TOOLS & SYSTEMS", "Git · GitHub", "QEMU · Semgrep", "Satellite / remote sensing data")]
    b = card(0, 0, 1200, 440, 20)
    for i, (lab, a, s2, s3) in enumerate(cells):
        x, y = 36 + (i % 3) * 380, 30 + (i // 3) * 200
        b += f'<rect x="{x}" y="{y}" width="360" height="180" rx="14" fill="#07142B" stroke="{ACC2}" stroke-opacity=".35"/>'
        b += f'<text x="{x+24}" y="{y+34}" class="mono" font-size="10" letter-spacing="3" fill="{ACC}">{esc(lab)}</text>'
        b += f'<text x="{x+24}" y="{y+88}" class="serif" font-size="38" fill="#FFFFFF">{esc(a)}</text>'
        b += f'<text x="{x+24}" y="{y+124}" class="serif" font-size="21" fill="{SOFT}" fill-opacity=".85">{esc(s2)}</text>'
        b += f'<text x="{x+24}" y="{y+154}" class="sans" font-size="13" fill="{MUT}">{esc(s3)}</text>'
        b += f'<circle class="pulse" cx="{x+336}" cy="{y+30}" r="3" fill="{ACC}" style="animation-delay:{i*.3}s"/>'
    save("toolkit.svg", svg(1200, 440, b))

# ================= CREDENTIALS =================
def credentials():
    items = [("ORACLE", "Java Foundations Associate", "Oracle Certified Foundations Associate", "ISSUED JUL 2026"),
             ("DATABASES", "MongoDB Database Administration", "Completed certification", "COMPLETED")]
    b = card(0, 0, 1200, 220, 20)
    for i, (lab, t, s2, tag) in enumerate(items):
        x = 36 + i * 570
        b += f'<rect x="{x}" y="30" width="552" height="160" rx="14" fill="#07142B" stroke="{ACC}" stroke-opacity=".45"/>'
        b += f'<text x="{x+24}" y="62" class="mono" font-size="10" letter-spacing="3" fill="{ACC}">{lab}</text>'
        b += f'<circle class="pulse" cx="{x+520}" cy="58" r="3.5" fill="{SOFT}"/>'
        b += f'<line x1="{x+24}" y1="76" x2="{x+528}" y2="76" stroke="{ACC2}" stroke-opacity=".3"/>'
        b += f'<text x="{x+24}" y="118" class="serif" font-size="28" fill="#FFFFFF">{esc(t)}</text>'
        b += f'<text x="{x+24}" y="146" class="sans" font-size="14" fill="{MUT}">{esc(s2)}</text>'
        b += f'<text x="{x+24}" y="172" class="mono" font-size="10" letter-spacing="3" fill="{SOFT}" fill-opacity=".8">{tag}</text>'
    save("credentials.svg", svg(1200, 220, b))

# ================= FOOTER =================
def footer():
    b = card(0, 0, 1200, 220, 20) + stars(22, 40, 20, 1160, 200, 3)
    b += f'<text x="600" y="108" text-anchor="middle" class="serif it" font-size="84" fill="{SOFT}">Krishna</text>'
    b += f'<rect x="300" y="130" width="600" height="1.5" fill="{ACC2}" fill-opacity=".6"/><circle class="slide" cx="300" cy="131" r="3.5" fill="{SOFT}" style="animation-name:none"/>'
    b += f'<text x="600" y="165" text-anchor="middle" class="serif it" font-size="22" fill="{TXT}">Building software, from the kernel up.</text>'
    b += f'<text x="600" y="194" text-anchor="middle" class="mono" font-size="11" letter-spacing="4" fill="{MUT}">FULL-STACK · ML / AI · SYSTEMS</text>'
    save("footer.svg", svg(1200, 220, b))

if __name__ == "__main__":
    hero()
    header("sec-01-about.svg", "01", "ABOUT", "WHO I AM", [("Hello, I'm ", False), ("Krishna.", True)])
    about()
    header("sec-02-snapshot.svg", "02", "SNAPSHOT", "EDUCATION · EXPERIENCE · FOCUS", [("At a ", False), ("glance.", True)])
    snapshot()
    header("sec-03-work.svg", "03", "SELECTED WORK", "FOUR PROJECTS · KERNEL TO CLOUD", [("Things I ", False), ("built.", True)])
    project("project-1.svg", "01 · SECURITY · AI · DEVOPS", "NexusGuard AI", "A GitHub-native security scanner with AI analysis.",
            "Semgrep + TruffleHog scans · Gemini API · Polygon blockchain · Docker",
            [("2", "scanners: Semgrep · TruffleHog"), ("Gemini", "LLM analysis layer"), ("Polygon", "blockchain layer")],
            ["Semgrep", "TruffleHog", "Docker", "Gemini API", "Polygon"],
            pipeline(["GitHub repo", "Semgrep + TruffleHog", "Gemini analysis", "Polygon record"], "SCAN PIPELINE"))
    project("project-2.svg", "02 · AI · SEARCH · RANKING", "TalentMatch-AI", "A candidate ranking engine built on semantic search.",
            "FAISS vector search · all-MiniLM-L6-v2 embeddings · Groq Llama-3.3-70B",
            [("FAISS", "vector index"), ("MiniLM", "sentence embeddings"), ("70B", "Llama-3.3 on Groq")],
            ["Python", "FAISS", "MiniLM", "Groq", "Llama-3.3"],
            pipeline(["Resume / JD text", "MiniLM embeddings", "FAISS retrieval", "Llama-3.3 ranking"], "RANKING PIPELINE"))
    project("project-3.svg", "03 · SYSTEMS · LOW-LEVEL", "Custom OS Kernel", "An operating-system kernel written from scratch.",
            "GDT / IDT setup in C and x86 Assembly · tested in QEMU",
            [("C + ASM", "implementation"), ("GDT/IDT", "descriptor tables"), ("QEMU", "emulated hardware")],
            ["C", "x86 Assembly", "QEMU", "GDT", "IDT"],
            layers(["bootloader · ASM", "GDT", "IDT · interrupts", "kernel main · C"], "KERNEL LAYERS"))
    project("project-4.svg", "04 · ML · REMOTE SENSING · BAH 2026", "Lunar Ice Detection", "Hunting subsurface ice in permanently shadowed craters.",
            "IPI (Ice Probability Index) model on Chandrayaan-2 DFSAR mosaic data",
            [("IPI", "ice probability index"), ("DFSAR", "Chandrayaan-2 radar data"), ("BAH 2026", "ISRO-themed hackathon")],
            ["Python", "ML", "DFSAR", "LOLA PSR"],
            crater("ICE PROBABILITY SCAN"))
    header("sec-04-toolkit.svg", "04", "TOOLKIT", "LANGUAGES · AI · WEB · DATA · INFRA", [("My ", False), ("toolkit.", True)])
    toolkit()
    header("sec-05-commits.svg", "05", "COMMIT LOG", "REAL DATA · LIVE", [("A year of ", False), ("shipping.", True)])
    header("sec-06-credentials.svg", "06", "CREDENTIALS", "ORACLE · MONGODB", [("Learning, ", False), ("certified.", True)])
    credentials()
    header("sec-07-connect.svg", "07", "CONNECT", "OPEN INBOX", [("Let's build something ", False), ("together.", True)])
    footer()
