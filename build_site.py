#!/usr/bin/env python3
"""Build the NKRYPT reference site from nkrypt-data.json."""
import json, html, textwrap, math

with open(__file__.replace('build_site.py','nkrypt-data.json')) as f:
    D = json.load(f)

def h(s): return html.escape(str(s))

# ── SVG GENERATORS ─────────────────────────────────────────────────

def svg_constellation_map():
    """Top-down pillar layout with Crux overlay."""
    # Approximate positions from McIntosh aerial map (normalised to 600x400 viewBox)
    positions = {
        'A': (480, 340), 'B': (180, 280), 'C': (340, 180),
        'D': (420, 240), 'E': (520, 200), 'F': (260, 140),
        'G': (300, 80), 'H': (140, 120)
    }
    crux = {'B','G','F','C','D'}
    svg = ['<svg viewBox="0 0 620 420" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:620px;font-family:monospace;">']
    svg.append('<rect width="620" height="420" rx="8" fill="#0e1117" stroke="#2a313c"/>')
    # Draw Crux lines
    crux_order = ['G','F','C','D','B']  # cross shape
    pts = [positions[p] for p in ['F','D']]  # vertical bar
    svg.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="#ffb54733" stroke-width="2" stroke-dasharray="6,4"/>')
    pts = [positions[p] for p in ['G','B']]  # horizontal bar
    svg.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="#ffb54733" stroke-width="2" stroke-dasharray="6,4"/>')
    pts = [positions[p] for p in ['C','B']]
    svg.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="#ffb54733" stroke-width="1" stroke-dasharray="4,4"/>')
    pts = [positions[p] for p in ['C','G']]
    svg.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="#ffb54733" stroke-width="1" stroke-dasharray="4,4"/>')

    for letter, (x,y) in positions.items():
        p = next(p for p in D['pillars'] if p['letter']==letter)
        r = 8 + p['total_height_mm']/200
        color = '#ffb547' if letter in crux else '#6ec1ff'
        solved = all(c['status']=='solved' for c in p['ciphers'])
        opacity = '1' if not solved else '0.7'
        svg.append(f'<circle cx="{x}" cy="{y}" r="{r:.0f}" fill="{color}" opacity="{opacity}"/>')
        svg.append(f'<text x="{x}" y="{y+r+14}" text-anchor="middle" fill="#e8eaed" font-size="12" font-weight="bold">{letter}</text>')
        svg.append(f'<text x="{x}" y="{y+r+26}" text-anchor="middle" fill="#9aa0a6" font-size="9">#{p["number"]}</text>')

    svg.append('<text x="10" y="410" fill="#9aa0a6" font-size="10">Gold = Crux hypothesis (B,G,F,C,D) | Blue = Centaurus (A,E,H) | Size = height</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def svg_rotor_wiring():
    """Rotor machine wiring diagram."""
    rm = D['rotor_machine']
    svg = ['<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:800px;font-family:monospace;">']
    svg.append('<rect width="800" height="320" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    labels = ['Input','R1','R2','R3','R4','Reflector']
    x_positions = [40, 160, 300, 440, 580, 720]

    for i, (label, x) in enumerate(zip(labels, x_positions)):
        svg.append(f'<text x="{x}" y="20" fill="#ffb547" font-size="11" text-anchor="middle" font-weight="bold">{label}</text>')
        for j in range(26):
            y = 30 + j * 11
            letter = chr(65+j)
            svg.append(f'<text x="{x}" y="{y}" fill="#9aa0a6" font-size="8" text-anchor="middle">{letter}</text>')

    svg.append('<text x="400" y="315" fill="#9aa0a6" font-size="10" text-anchor="middle">4 rotors + reflector | Manual advancement | Key = 4 letters (e.g. SWYQ)</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def svg_squircle_grid():
    """10x26 squircle orientation grid with actual shapes."""
    grid_data = [
        "01110011011101021231331012",
        "02030013322303333000200032",
        "21221133103032320102000132",
        "23123002121223001301131123",
        "10103100010101201201221103",
        "30212131033000203011112330",
        "30101111212032132012210133",
        "13303323023120222333322012",
        "00000101022001203231310031",
        "30110333202120112302112123"
    ]
    cell = 18
    pad = 30
    w = 26*cell + pad*2
    ht = 10*cell + pad*2 + 20
    svg = [f'<svg viewBox="0 0 {w} {ht}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{w}px;font-family:monospace;">']
    svg.append(f'<rect width="{w}" height="{ht}" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    colors = ['#6ec1ff','#ffb547','#4caf50','#ef5350']

    # Squircle shape paths for each orientation (0=UR, 1=LR, 2=LL, 3=UL)
    def squircle_path(cx, cy, orient, size=6):
        """Draw a petal/cam shape pointing in one of 4 directions."""
        s = size
        if orient == 0:  # upper-right
            return f'M{cx-s},{cy} Q{cx-s},{cy-s} {cx},{cy-s} Q{cx+s},{cy-s} {cx+s},{cy} Q{cx+s},{cy+s*0.3} {cx},{cy+s*0.3} Q{cx-s},{cy+s*0.3} {cx-s},{cy}Z'
        elif orient == 1:  # lower-right
            return f'M{cx},{cy-s*0.3} Q{cx+s},{cy-s*0.3} {cx+s},{cy} Q{cx+s},{cy+s} {cx},{cy+s} Q{cx-s},{cy+s} {cx-s},{cy} Q{cx-s},{cy-s*0.3} {cx},{cy-s*0.3}Z'
        elif orient == 2:  # lower-left
            return f'M{cx+s},{cy} Q{cx+s},{cy+s} {cx},{cy+s} Q{cx-s},{cy+s} {cx-s},{cy} Q{cx-s},{cy-s*0.3} {cx},{cy-s*0.3} Q{cx+s},{cy-s*0.3} {cx+s},{cy}Z'
        else:  # upper-left
            return f'M{cx+s},{cy} Q{cx+s},{cy-s} {cx},{cy-s} Q{cx-s},{cy-s} {cx-s},{cy} Q{cx-s},{cy+s*0.3} {cx},{cy+s*0.3} Q{cx+s},{cy+s*0.3} {cx+s},{cy}Z'

    # Column numbers
    for c in range(26):
        x = pad + c*cell + cell//2
        svg.append(f'<text x="{x}" y="{pad-8}" fill="#9aa0a6" font-size="7" text-anchor="middle">{c+1}</text>')

    # Row labels
    for r in range(10):
        y = pad + r*cell + cell//2 + 3
        svg.append(f'<text x="{pad-12}" y="{y}" fill="#9aa0a6" font-size="7" text-anchor="end">R{r+1}</text>')

    for r, row in enumerate(grid_data):
        for c, ch in enumerate(row):
            v = int(ch)
            cx = pad + c*cell + cell//2
            cy = pad + r*cell + cell//2
            path = squircle_path(cx, cy, v, size=cell//2-2)
            svg.append(f'<path d="{path}" fill="{colors[v]}" opacity="0.85"/>')

    # Legend
    ly = ht - 14
    for i, (col, label) in enumerate(zip(colors, ['0 (UR)','1 (LR)','2 (LL)','3 (UL)'])):
        lx = pad + i*120
        svg.append(f'<rect x="{lx}" y="{ly-7}" width="10" height="10" rx="2" fill="{col}" opacity="0.85"/>')
        svg.append(f'<text x="{lx+14}" y="{ly+2}" fill="#9aa0a6" font-size="9">{label}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def svg_pvl_grid():
    """PVL 26x10 letter grid with P, V, L highlighted."""
    rows = [
        "OXPUWAOEKZVCRLUYFMLXTPNATW",
        "VGZTCGVGDAAXFDKOCRFRUOKAPW",
        "LCMPTFPBTYXRSZKKQUBJAMHYUL",
        "MZVSXXZHDLYHOKWWEJUXLXKRZU",
        "PPESLBOEKOGRTAYDFOHRHVMPBN",
        "DTEZBTYDXNMPXHVNKCIYEMJFVE",
        "MNKDIQBOSUFFFWBVDNKHRTLIMZ",
        "WRRQUFNNBGKUWNQCHDEFSTZZRQ",
        "UIUDPTKGATPSJIFXXGGSNTWJLA",
        "BRYVUCSBNPYAVSTTONZFWIUUNW"
    ]
    cell = 22
    pad = 30
    w = 26*cell + pad*2
    ht = 10*cell + pad*2
    svg = [f'<svg viewBox="0 0 {w} {ht}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{w}px;font-family:monospace;">']
    svg.append(f'<rect width="{w}" height="{ht}" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            x = pad + c*cell + cell//2
            y = pad + r*cell + cell//2
            if ch in 'PVL':
                svg.append(f'<rect x="{x-cell//2+1}" y="{y-cell//2+1}" width="{cell-2}" height="{cell-2}" rx="3" fill="#b58aff22" stroke="#b58aff" stroke-width="1"/>')
                svg.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#b58aff" font-size="12" font-weight="bold">{ch}</text>')
            else:
                svg.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#e8eaed" font-size="10">{ch}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def svg_labyrinth_pattern():
    """Diagram showing the labyrinth traversal pattern."""
    svg = ['<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:600px;font-family:monospace;">']
    svg.append('<rect width="600" height="200" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    rows_y = [30, 60, 90, 120, 150]
    row_labels = ['Row 1 (LTR)','Row 2 (RTL)','Row 3 (LTR)','Row 4 (RTL)','Row 5 (LTR)']

    for i, (y, label) in enumerate(zip(rows_y, row_labels)):
        color = '#6ec1ff' if i%2==0 else '#ffb547'
        x1, x2 = (80, 550) if i%2==0 else (550, 80)
        svg.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>')
        svg.append(f'<text x="20" y="{y+4}" fill="#9aa0a6" font-size="9">{label}</text>')

    # Transition arrows between rows
    for i in range(4):
        y1 = rows_y[i]
        y2 = rows_y[i+1]
        x = 350 + (i%2)*100 - 50  # approximate transition points
        svg.append(f'<line x1="{x}" y1="{y1+5}" x2="{x}" y2="{y2-5}" stroke="#4caf5088" stroke-width="2" stroke-dasharray="4,3"/>')
        svg.append(f'<text x="{x+5}" y="{(y1+y2)//2+4}" fill="#4caf50" font-size="8">T{i+1}</text>')

    svg.append('<text x="300" y="185" text-anchor="middle" fill="#9aa0a6" font-size="10">T1-T4 = traversal transition points (encode as 4-letter code per pillar)</text>')
    svg.append('<defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#6ec1ff"/></marker></defs>')
    svg.append('</svg>')
    return '\n'.join(svg)


def svg_pairing_diagram():
    """Visual diagram of pillar pairings."""
    svg = ['<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:600px;font-family:monospace;">']
    svg.append('<rect width="600" height="220" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    pairs = [('C','A','#6ec1ff'), ('H','B','#b58aff'), ('G','F','#ffb547'), ('E','D','#4caf50')]

    for i, (p1, p2, color) in enumerate(pairs):
        x = 75 + i*140
        # Pillar 1
        svg.append(f'<circle cx="{x-25}" cy="80" r="22" fill="none" stroke="{color}" stroke-width="2"/>')
        svg.append(f'<text x="{x-25}" y="85" text-anchor="middle" fill="{color}" font-size="16" font-weight="bold">{p1}</text>')
        # Pillar 2
        svg.append(f'<circle cx="{x+25}" cy="80" r="22" fill="none" stroke="{color}" stroke-width="2"/>')
        svg.append(f'<text x="{x+25}" y="85" text-anchor="middle" fill="{color}" font-size="16" font-weight="bold">{p2}</text>')
        # Connection
        svg.append(f'<line x1="{x-3}" y1="80" x2="{x+3}" y2="80" stroke="{color}" stroke-width="2"/>')
        # Label
        pi = D['pairings']['pairs'][i]
        svg.append(f'<text x="{x}" y="130" text-anchor="middle" fill="#9aa0a6" font-size="9" style="max-width:120px">{h(pi["relationship"][:30])}</text>')

    svg.append('<text x="300" y="170" text-anchor="middle" fill="#e8eaed" font-size="11" font-weight="bold">Pillar Pairings (by template analysis)</text>')
    svg.append('<text x="300" y="190" text-anchor="middle" fill="#9aa0a6" font-size="9">Source: Kohlhagen template shared with Schmeh/Dunin 2022</text>')
    svg.append('<text x="300" y="205" text-anchor="middle" fill="#9aa0a6" font-size="9">Ring ciphers at uniform 1709mm | Height variation = extension above ring</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def svg_pillar_heights():
    """Bar chart of pillar heights showing ring line and extension."""
    pillars = D['pillars']
    w = 600
    ht = 280
    svg = [f'<svg viewBox="0 0 {w} {ht}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{w}px;font-family:monospace;">']
    svg.append(f'<rect width="{w}" height="{ht}" rx="8" fill="#0e1117" stroke="#2a313c"/>')

    max_h = 2600
    base_y = 250
    scale = 200 / max_h
    bar_w = 40
    gap = 20
    start_x = 60

    for i, p in enumerate(pillars):
        x = start_x + i*(bar_w+gap)
        total = p['total_height_mm']
        ring = 1709
        ext = p['extension_above_ring_mm']

        # Ring portion (blue)
        ring_h = ring * scale
        svg.append(f'<rect x="{x}" y="{base_y-ring_h}" width="{bar_w}" height="{ring_h}" fill="#6ec1ff44" stroke="#6ec1ff" stroke-width="0.5"/>')

        # Extension portion (gold)
        if ext > 0:
            ext_h = ext * scale
            svg.append(f'<rect x="{x}" y="{base_y-ring_h-ext_h}" width="{bar_w}" height="{ext_h}" fill="#ffb54744" stroke="#ffb547" stroke-width="0.5"/>')

        # Label
        svg.append(f'<text x="{x+bar_w//2}" y="{base_y+14}" text-anchor="middle" fill="#e8eaed" font-size="11" font-weight="bold">{p["letter"]}</text>')
        svg.append(f'<text x="{x+bar_w//2}" y="{base_y+26}" text-anchor="middle" fill="#9aa0a6" font-size="8">#{p["number"]}</text>')
        svg.append(f'<text x="{x+bar_w//2}" y="{base_y-total*scale-6}" text-anchor="middle" fill="#9aa0a6" font-size="8">{total}</text>')

    # Ring line
    ring_y = base_y - 1709*scale
    svg.append(f'<line x1="40" y1="{ring_y}" x2="{start_x+8*(bar_w+gap)}" y2="{ring_y}" stroke="#6ec1ff" stroke-width="1" stroke-dasharray="6,3"/>')
    svg.append(f'<text x="38" y="{ring_y+4}" text-anchor="end" fill="#6ec1ff" font-size="8">Ring 1709mm</text>')

    # Legend
    svg.append(f'<rect x="420" y="10" width="12" height="12" fill="#6ec1ff44" stroke="#6ec1ff"/>')
    svg.append(f'<text x="436" y="20" fill="#9aa0a6" font-size="9">Ring cipher zone</text>')
    svg.append(f'<rect x="420" y="26" width="12" height="12" fill="#ffb54744" stroke="#ffb547"/>')
    svg.append(f'<text x="436" y="36" fill="#9aa0a6" font-size="9">Extension above ring</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


# ── HTML GENERATION ────────────────────────────────────────────────

def badge(status):
    s = status.lower().strip()
    # Handle compound statuses like "SOLVED (trivial)" or "UNSOLVED (FINAL PUZZLE)"
    if 'final' in s:
        return '<span class="badge final">Final Puzzle</span>'
    if 'trivial' in s:
        return '<span class="badge solved">Trivial</span>'
    if 'partial' in s:
        return '<span class="badge active">Partial</span>'
    cls_map = {'solved':'solved','unsolved':'blocked'}
    cls = cls_map.get(s, 'untested')
    label_map = {'solved':'Solved','unsolved':'Unsolved'}
    label = label_map.get(s, status.replace('_',' ').title())
    return f'<span class="badge {cls}">{label}</span>'


def render_cipher_card(cipher):
    parts = []
    parts.append(f'<div class="cipher-card">')
    parts.append(f'<h3>{h(cipher["name"])} {badge(cipher["status"])}</h3>')
    parts.append(f'<div class="ciphertype">{h(cipher["type"])}</div>')

    if cipher.get('description'):
        parts.append(f'<p>{h(cipher["description"])}</p>')

    if cipher.get('ciphertext'):
        ct = cipher['ciphertext']
        parts.append(f'<details><summary>Ciphertext</summary><div class="ciphertext">{h(ct)}</div></details>')

    if cipher.get('plaintext'):
        pt = cipher['plaintext']
        parts.append(f'<div class="poem">{h(pt)}</div>')

    if cipher.get('key'):
        parts.append(f'<p><strong>Key:</strong> <code>{h(cipher["key"])}</code></p>')

    if cipher.get('note'):
        parts.append(f'<div class="conjecture"><strong>Note:</strong> {h(cipher["note"])}</div>')

    if cipher.get('suburbs'):
        subs = cipher['suburbs']
        if subs and isinstance(subs[0], str):
            parts.append(f'<p><strong>Decoded suburbs:</strong> {", ".join(h(s) for s in subs)}</p>')
        else:
            parts.append('<details open><summary>Decoded locations</summary><table class="canon"><thead><tr><th>Lat</th><th>Lon</th><th>Suburb</th><th>Note</th></tr></thead><tbody>')
            for sub in subs:
                parts.append(f'<tr><td>{h(sub["lat"])}</td><td>{h(sub["lon"])}</td><td>{h(sub["suburb"])}</td><td>{h(sub.get("note",""))}</td></tr>')
            parts.append('</tbody></table></details>')

    if cipher.get('attempts_summary'):
        parts.append(f'<details><summary>Approaches tested</summary><div class="attempts">{h(cipher["attempts_summary"])}</div></details>')

    if cipher.get('mesh_groups'):
        parts.append('<details open><summary>Mesh-compatibility groups</summary><table class="canon"><thead><tr><th>Column</th><th>Cogs</th><th>Groups</th><th>Group pattern</th></tr></thead><tbody>')
        for g in cipher['mesh_groups']:
            parts.append(f'<tr><td>{g["column"]}</td><td>{g["cog_count"]}</td><td>{g["group_count"]}</td><td><code>{h(g["pattern"])}</code></td></tr>')
        parts.append('</tbody></table></details>')

    if cipher.get('grid'):
        parts.append(f'<details><summary>Grid data</summary><div class="ciphertext">{h(cipher["grid"])}</div></details>')

    if cipher.get('astroid_counts'):
        parts.append(f'<details><summary>Per-column counts (42 columns)</summary><div class="ciphertext">{cipher["astroid_counts"]}</div></details>')

    if cipher.get('attribution'):
        parts.append(f'<p class="attribution">Solved by: {h(cipher["attribution"])}</p>')

    parts.append('</div>')
    return '\n'.join(parts)


def render_pillar_section(pillar):
    p = pillar
    parts = []
    letter = p['letter']
    number = p['number']
    name = p['common_name']

    all_solved = all('solved' in c['status'].lower() or 'trivial' in c['status'].lower() for c in p['ciphers'])
    any_unsolved = any('unsolved' in c['status'].lower() or 'final' in c['status'].lower() for c in p['ciphers'])

    parts.append(f'<section class="page" id="pillar-{letter}">')
    parts.append(f'<h1 class="page-title">Pillar {letter} / #{number} &mdash; {h(name)}</h1>')

    # Metadata table
    parts.append('<div class="pillar-meta"><table>')
    parts.append(f'<tr><th>Letter (meme.net.au)</th><td>{letter}</td></tr>')
    parts.append(f'<tr><th>Number (dkrypt.org)</th><td>{number}</td></tr>')
    parts.append(f'<tr><th>Total height</th><td>{p["total_height_mm"]} mm</td></tr>')
    parts.append(f'<tr><th>Extension above ring</th><td>{p["extension_above_ring_mm"]} mm</td></tr>')
    parts.append(f'<tr><th>Fiducial separation</th><td>{p["fiducial_separation_mm"]} mm</td></tr>')
    parts.append(f'<tr><th>Fiducial direction</th><td>{p["fiducial_direction"]}</td></tr>')
    parts.append(f'<tr><th>Traversal code</th><td><code>{p["traversal_code"]}</code></td></tr>')

    # Paired pillar
    for pair in D['pairings']['pairs']:
        if letter in pair['pillars']:
            partner = [x for x in pair['pillars'] if x != letter][0]
            parts.append(f'<tr><th>Paired with</th><td><a href="#pillar-{partner}">Pillar {partner}</a> &mdash; {h(pair["relationship"])}</td></tr>')

    parts.append('</table></div>')

    # Ciphers
    for cipher in p['ciphers']:
        parts.append(render_cipher_card(cipher))

    parts.append('</section>')
    return '\n'.join(parts)


# ── MAIN HTML ──────────────────────────────────────────────────────

CSS = """
:root {
  --bg: #0e1014; --bg-card: #161a21; --bg-card-2: #1c222b;
  --fg: #e8eaed; --fg-dim: #9aa0a6; --accent: #ffb547; --accent-2: #6ec1ff;
  --border: #2a313c; --good: #4caf50; --warn: #ffb547; --bad: #ef5350;
  --info: #6ec1ff; --final: #b58aff;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
html, body { margin:0; padding:0; background:var(--bg); color:var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height:1.6; }
a { color:var(--accent-2); text-decoration:none; }
a:hover { text-decoration:underline; }
code, pre { font-family: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace; }
pre { background:var(--bg-card-2); padding:12px; border-radius:6px; overflow-x:auto; font-size:12px; white-space:pre-wrap; }
code { background:var(--bg-card-2); padding:1px 5px; border-radius:3px; font-size:12px; }
.layout { display:grid; grid-template-columns:260px 1fr; min-height:100vh; }
@media (max-width:800px) { .layout { grid-template-columns:1fr; } nav.sidebar { display:none; } }
nav.sidebar { background:var(--bg-card); border-right:1px solid var(--border);
  padding:20px 16px; position:sticky; top:0; height:100vh; overflow-y:auto; }
nav.sidebar h1 { font-size:20px; margin:0 0 4px 0; color:var(--accent); letter-spacing:0.15em; }
nav.sidebar .subtitle { font-size:11px; color:var(--fg-dim); margin-bottom:18px; }
nav.sidebar ul { list-style:none; padding:0; margin:0 0 12px 0; }
nav.sidebar li { margin:2px 0; }
nav.sidebar a { color:var(--fg); display:block; padding:4px 8px; border-radius:4px; font-size:12px; transition:background 0.15s; }
nav.sidebar a:hover { background:var(--bg-card-2); text-decoration:none; }
nav.sidebar a.solved { opacity:0.6; }
nav.sidebar .group-label { font-size:10px; text-transform:uppercase; letter-spacing:0.08em;
  color:var(--fg-dim); margin:14px 0 4px 8px; font-weight:600; }
main { padding:28px 36px; max-width:1200px; }
@media (max-width:800px) { main { padding:16px; } }
section.page { margin-bottom:60px; padding-bottom:28px; border-bottom:1px dashed var(--border); }
section.page:last-child { border-bottom:none; }
h1.page-title { font-size:26px; margin:0 0 6px 0; color:var(--accent); }
h2 { color:var(--accent-2); font-size:18px; margin:24px 0 8px 0; }
h3 { color:var(--fg); font-size:15px; margin:18px 0 6px 0; }
.page-subtitle { color:var(--fg-dim); font-size:13px; margin-bottom:18px; }
.pillar-meta { margin-bottom:20px; }
.pillar-meta table { width:100%; max-width:700px; font-size:13px; border-collapse:collapse; }
.pillar-meta th, .pillar-meta td { text-align:left; padding:5px 10px; border-bottom:1px solid var(--border); vertical-align:top; }
.pillar-meta th { color:var(--fg-dim); font-weight:500; width:35%; }
.cipher-card { background:var(--bg-card); border:1px solid var(--border); border-radius:8px;
  padding:16px 20px; margin:16px 0; }
.cipher-card h3 { margin:0 0 6px 0; font-size:16px; }
.badge { display:inline-block; padding:2px 8px; font-size:11px; border-radius:10px;
  font-weight:600; letter-spacing:0.02em; margin-left:8px; vertical-align:middle; }
.badge.solved { background:var(--good); color:#fff; }
.badge.active { background:var(--warn); color:#2a1a00; }
.badge.blocked { background:var(--bad); color:#fff; }
.badge.untested { background:#555; color:#fff; }
.badge.final { background:var(--final); color:#fff; }
.ciphertype { color:var(--fg-dim); font-size:12px; margin:-2px 0 8px 0; }
.ciphertext { font-family:"JetBrains Mono",ui-monospace,monospace; font-size:11px;
  background:var(--bg-card-2); padding:10px 12px; border-radius:4px; overflow-x:auto; white-space:pre; line-height:1.5; }
.poem { background:var(--bg-card-2); border-left:3px solid var(--accent-2);
  padding:10px 14px; margin:10px 0; font-style:italic; white-space:pre-wrap; font-size:13px; }
.conjecture { background:rgba(110,193,255,0.06); border-left:3px solid var(--info);
  padding:10px 14px; margin:8px 0; font-size:13px; border-radius:4px; }
.attempts { background:var(--bg-card-2); padding:10px 14px; border-radius:4px; font-size:12px; white-space:pre-wrap; line-height:1.5; }
.attribution { font-size:11px; color:var(--fg-dim); margin:6px 0 0 0; font-style:italic; }
table.canon { width:100%; border-collapse:collapse; font-size:13px; margin:12px 0; }
table.canon th, table.canon td { padding:6px 10px; border-bottom:1px solid var(--border); text-align:left; }
table.canon th { color:var(--fg-dim); font-weight:500; background:var(--bg-card-2); }
table.canon tr:hover td { background:var(--bg-card-2); }
.stat-row { display:flex; gap:8px; flex-wrap:wrap; margin:8px 0; }
.stat { background:var(--bg-card-2); padding:6px 10px; border-radius:4px; font-size:12px; }
.stat .label { color:var(--fg-dim); margin-right:4px; }
.stat .val { color:var(--fg); font-weight:500; }
details { margin:8px 0; }
summary { cursor:pointer; color:var(--accent-2); font-size:13px; }
.plaque { background:var(--bg-card-2); border-left:3px solid var(--accent); padding:14px 18px;
  font-style:italic; white-space:pre-wrap; font-size:13px; }
.svg-container { margin:16px 0; overflow-x:auto; }
.footer { font-size:11px; color:var(--fg-dim); margin-top:40px; padding-top:14px;
  border-top:1px solid var(--border); }
.toc-status { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; }
.toc-status.green { background:var(--good); }
.toc-status.red { background:var(--bad); }
.toc-status.orange { background:var(--warn); }
.toc-status.purple { background:var(--final); }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media (max-width:800px) { .grid-2 { grid-template-columns:1fr; } }
.key-insight { background:rgba(255,181,71,0.08); border-left:3px solid var(--accent);
  padding:10px 14px; margin:12px 0; border-radius:4px; font-size:13px; }
"""

# Build sidebar
def pillar_status_dot(p):
    statuses = [c['status'].lower() for c in p['ciphers']]
    if all('solved' in s or 'trivial' in s for s in statuses):
        return 'green'
    if any('final' in s for s in statuses):
        return 'purple'
    if any('unsolved' in s for s in statuses):
        has_solved = any('solved' in s for s in statuses)
        return 'orange' if has_solved else 'red'
    return 'orange'

sidebar_items = []
sidebar_items.append('<h1>NKRYPT</h1>')
sidebar_items.append('<div class="subtitle">Canonical Reference Site</div>')
sidebar_items.append('<ul>')
sidebar_items.append('<li><a href="#overview">Overview</a></li>')
sidebar_items.append('<li><a href="#structure">Physical Structure</a></li>')
sidebar_items.append('<li><a href="#labyrinth">Ring Cipher System</a></li>')
sidebar_items.append('</ul>')
sidebar_items.append('<div class="group-label">Pillars</div>')
sidebar_items.append('<ul>')
for p in D['pillars']:
    dot = pillar_status_dot(p)
    sidebar_items.append(f'<li><a href="#pillar-{p["letter"]}"><span class="toc-status {dot}"></span>{p["letter"]} / #{p["number"]} &middot; {p["common_name"]}</a></li>')
sidebar_items.append('</ul>')
sidebar_items.append('<div class="group-label">Cross-cutting</div>')
sidebar_items.append('<ul>')
sidebar_items.append('<li><a href="#pairings">Pillar Pairings</a></li>')
sidebar_items.append('<li><a href="#structure">Constellation</a></li>')
sidebar_items.append('<li><a href="#rotor-machine">Rotor Machine</a></li>')
sidebar_items.append('<li><a href="#basecode">Base Code DNA</a></li>')
sidebar_items.append('<li><a href="#tweet">Opening Tweet</a></li>')
sidebar_items.append('</ul>')
sidebar_items.append('<div class="group-label">Data</div>')
sidebar_items.append('<ul>')
sidebar_items.append('<li><a href="nkrypt-data.json">Machine-readable JSON</a></li>')
sidebar_items.append('<li><a href="#sources">Sources</a></li>')
sidebar_items.append('</ul>')

sidebar = '\n'.join(sidebar_items)

# Build main content
main_parts = []

# ── Overview ──
proj = D['project']
main_parts.append(f'''
<section class="page" id="overview">
<h1 class="page-title">NKRYPT</h1>
<div class="page-subtitle">Eight stainless steel pillars bearing encrypted inscriptions.
  Questacon, Canberra, Australia. Installed March 2013 for the Centenary of Canberra.
  Designed by Dr Stuart Kohlhagen PSM (Deputy Director, Questacon).</div>

<div class="plaque">{h(proj["plaque"]["haiku"])}

{h(proj["plaque"]["key_phrase"])}

{h(proj["plaque"]["centenary_note"])}
Proudly supported by {h(proj["plaque"]["supporters"])}</div>

<h2>Status</h2>
<div class="stat-row">
  <div class="stat"><span class="label">Total ciphers:</span><span class="val">19</span></div>
  <div class="stat"><span class="label">Solved:</span><span class="val">11</span></div>
  <div class="stat"><span class="label">Unsolved:</span><span class="val">7</span></div>
  <div class="stat"><span class="label">Partially solved:</span><span class="val">1 (tweet)</span></div>
</div>

<table class="canon">
<thead><tr><th>Pillar</th><th>Ring cipher</th><th>Lower cipher</th><th>Extra</th></tr></thead>
<tbody>
''')

for p in D['pillars']:
    cells = [f'{p["letter"]} / #{p["number"]} ({p["common_name"]})']
    for c in p['ciphers']:
        cells.append(f'{c["name"]} {badge(c["status"])}')
    while len(cells) < 4:
        cells.append('')
    main_parts.append(f'<tr>{"".join(f"<td>{c}</td>" for c in cells)}</tr>')

main_parts.append('</tbody></table>')

main_parts.append(f'''
<div class="key-insight">
<strong>Meta-pattern:</strong> {h(proj["meta_pattern"])}
</div>

<h2>Naming conventions</h2>
<p>Two naming schemes are in common use. The meme.net.au site (Glenn McIntosh) labels pillars A through H
by fiducial spacing. The dkrypt.org site (Greg Lloyd) numbers them 1 through 8. This site always shows both:
<code>Pillar A (#7)</code>. The mapping is: {", ".join(f"{k}={v}" for k,v in D["naming"]["mapping"].items())}.</p>

<h2>External references</h2>
<p><a href="https://www.meme.net.au/nkrypt/">meme.net.au/nkrypt</a> (Glenn McIntosh) &mdash; the most comprehensive independent analysis.<br>
<a href="https://www.dkrypt.org/">dkrypt.org</a> (Greg Lloyd) &mdash; high-resolution photographs and per-pillar pages.<br>
<a href="https://scienceblogs.de/klausis-krypto-kolumne/">Cipherbrain</a> (Klaus Schmeh) &mdash; multiple articles, including 2022 interview with Kohlhagen.<br>
<a href="https://www.questacon.edu.au/visiting/galleries/outdoor/exhibits/nkrypt">Questacon official page</a></p>
</section>
''')

# ── Physical Structure ──
main_parts.append(f'''
<section class="page" id="structure">
<h1 class="page-title">Physical Structure</h1>
<div class="page-subtitle">Heights, fiducials, and the pillar constellation.</div>

<h2>Pillar heights</h2>
<div class="svg-container">{svg_pillar_heights()}</div>

<p>All ring ciphers sit at exactly <strong>1709 mm</strong> above ground (uniform across all 8 pillars).
The height variation between pillars is encoded as the <em>extension above the ring</em>. Pillar A (shortest)
has zero extension; Pillar H (tallest) has 860 mm of extension, occupied by the PVL cipher.</p>

<h3>Three independent measurement channels</h3>
<table class="canon">
<thead><tr><th>Pillar</th><th>Total height (mm)</th><th>Extension above ring (mm)</th><th>Fiducial separation (mm)</th><th>Fiducial direction</th></tr></thead>
<tbody>
''')
for p in D['pillars']:
    main_parts.append(f'<tr><td>{p["letter"]} (#{p["number"]})</td><td>{p["total_height_mm"]}</td><td>{p["extension_above_ring_mm"]}</td><td>{p["fiducial_separation_mm"]}</td><td>{p["fiducial_direction"]}</td></tr>')

main_parts.append(f'''
</tbody></table>
<p>All three series (total height, extension, fiducial separation) are monotone in pillar letter (A smallest, H largest).
They are <em>not</em> the same measurement and must not be conflated.</p>

<h2>Constellation layout</h2>
<div class="svg-container">{svg_constellation_map()}</div>
<p>The eight pillars are arranged in a constellation pattern when viewed from above. Kohlhagen confirmed (2022, via Schmeh/Dunin)
that positions and heights encode meaning. Working hypothesis: pillars B, G, F, C, D form the Southern Cross (Crux);
pillars A, E, H represent Alpha, Beta, and Omega Centauri. The thematic link: Centaurus/Centenary wordplay for Canberra\'s
1913-2013 centenary.</p>
</section>
''')

# ── Labyrinth / Ring Cipher System ──
rc = D['ring_ciphers']
main_parts.append(f'''
<section class="page" id="labyrinth">
<h1 class="page-title">Ring Cipher System</h1>
<div class="page-subtitle">The labyrinth traversal pattern shared by all eight pillars.</div>

<div class="svg-container">{svg_labyrinth_pattern()}</div>

<p>{h(rc["description"])} The four transition positions between row pairs are recorded as a 4-letter
traversal code per pillar. These codes are believed to encode rotor settings or parameters for the
Pillar C rotor machine.</p>

<h2>Traversal codes</h2>
<table class="canon">
<thead><tr><th>Pillar</th><th>Traversal code</th><th>Endpoint position</th><th>Start row</th></tr></thead>
<tbody>
''')
for letter in 'ABCDEFGH':
    code = rc['traversal_codes'][letter]
    endpoint = 'Below fiducial' if letter in rc['endpoints']['below_fiducial'] else 'Opposite fiducial'
    start = 'Top row' if letter in rc['endpoints']['start_top_row'] else 'Bottom row'
    main_parts.append(f'<tr><td>{letter}</td><td><code>{code}</code></td><td>{endpoint}</td><td>{start}</td></tr>')

main_parts.append('''
</tbody></table>
<div class="key-insight">
<strong>Pillar G's traversal code is unknown.</strong> Solving the squircle cipher should reveal it, completing the set of eight codes needed for the final puzzle.
</div>
</section>
''')

# ── Per-pillar sections ──
for p in D['pillars']:
    main_parts.append(render_pillar_section(p))
    # Add special SVGs for certain pillars
    if p['letter'] == 'G':
        main_parts.append(f'<div class="svg-container"><h3>Squircle orientation grid</h3>{svg_squircle_grid()}</div>')
    elif p['letter'] == 'H':
        main_parts.append(f'<div class="svg-container"><h3>PVL letter grid (P, V, L highlighted)</h3>{svg_pvl_grid()}</div>')

# ── Pairings ──
main_parts.append(f'''
<section class="page" id="pairings">
<h1 class="page-title">Pillar Pairings</h1>
<div class="page-subtitle">Structural pairs derived from the Kohlhagen template.</div>

<div class="svg-container">{svg_pairing_diagram()}</div>

<p>The Kohlhagen template (shared with Schmeh and Dunin in 2022) reveals that ring ciphers sit at the same height
across all pillars. Height differences encode the extension above the ring. Lower ciphers cluster into pairs
by effective extent: G and F, E and D, C and A, H and B.</p>

<div class="key-insight"><strong>Implication:</strong> cross-pillar attacks should target pairs first. A solved pillar may unlock its partner.
The template sharing was itself a deliberate hint that pillars should be read in relation to each other.</div>

<h2>Pair details</h2>
''')

for pair in D['pairings']['pairs']:
    p1, p2 = pair['pillars']
    main_parts.append(f'''
<div class="cipher-card">
<h3>{p1} and {p2}</h3>
<p><strong>Relationship:</strong> {h(pair["relationship"])}</p>
<p><strong>Cross-pillar attack:</strong> {h(pair["attack"])}</p>
</div>
''')
main_parts.append('</section>')

# ── Rotor Machine ──
rm = D['rotor_machine']
main_parts.append(f'''
<section class="page" id="rotor-machine">
<h1 class="page-title">Rotor Machine (Pillar C)</h1>
<div class="page-subtitle">Enigma-like encryption device with four rotors and a reflector.</div>

<p>{h(rm["description"])}</p>

<div class="svg-container">{svg_rotor_wiring()}</div>

<h2>Rotor wirings</h2>
''')

for name in ['rotor1','rotor2','rotor3','rotor4','reflector']:
    w = rm['wirings'][name]
    label = name.replace('rotor','Rotor ').replace('reflector','Reflector').title()
    main_parts.append(f'''
<details><summary>{label}</summary>
<div class="ciphertext">Plain:  {w["plain"]}
Cipher: {w["cipher"]}</div>
</details>
''')

main_parts.append(f'''
<h2>Key properties</h2>
<p><strong>Key format:</strong> {h(rm["key_format"])}<br>
<strong>Involutive:</strong> {"Yes (encrypt = decrypt with same key, no advancement)" if rm["involutive"] else "No"}<br>
<strong>Advancement:</strong> {h(rm["advancement"])}</p>
</section>
''')

# ── Base Code DNA ──
bc = D['base_code']
main_parts.append(f'''
<section class="page" id="basecode">
<h1 class="page-title">Base Code DNA</h1>
<div class="page-subtitle">{h(bc["description"])}</div>

<h2>STR profiles (15 loci per pillar)</h2>
<div style="overflow-x:auto;">
<table class="canon">
<thead><tr><th>Pillar</th>{"".join(f"<th>{l}</th>" for l in bc["loci_order"])}</tr></thead>
<tbody>
''')

for letter in 'ABCDEFGH':
    profile = bc['profiles'][letter]
    main_parts.append(f'<tr><td><strong>{letter}</strong></td>{"".join(f"<td>{v}</td>" for v in profile)}</tr>')

main_parts.append(f'''
</tbody></table>
</div>

<h2>Conjectured relationships</h2>
<p>Population origin: {h(bc["population"])}. Possible parental connections: {", ".join(bc["conjectured_parents"])}.</p>
<div class="conjecture">If these are genetic fingerprints of real people, Kohlhagen may have immortalised his own family.
The relationships between profiles have not been conclusively determined.</div>
</section>
''')

# ── Tweet ──
tw = D['tweet']
main_parts.append(f'''
<section class="page" id="tweet">
<h1 class="page-title">Opening Day Tweet</h1>
<div class="page-subtitle">Encrypted tweet by {h(tw["sender"])}, {h(tw["date"])}.</div>

<div class="ciphertext">{h(tw["ciphertext"])}</div>
<p><strong>Length:</strong> {tw["length"]} characters</p>

<h2>Partial solution</h2>
<p>Positions {tw["partial_solution"]["positions"]} decrypt to <code>{h(tw["partial_solution"]["plaintext"])}</code>
using rotor key <code>{h(tw["partial_solution"]["key"])}</code>.</p>
<div class="conjecture">{h(tw["partial_solution"]["note"])}</div>

<p><strong>Unsolved:</strong> {h(tw["unsolved"])}.</p>
<p>A photograph from the opening ceremony shows rotor setting <code>{h(tw["photo_rotor_setting"])}</code>.</p>

<div class="key-insight">Stuart Kohlhagen wrote: "the piece was developed before we had her or the idea of a coded tweet
in mind... and we did want to suggest that if folk wanted to they could select their own coding protocol...
perhaps thinking about how a person might select a protocol based on a specifically personal 'attribute' might help
with HER tweet." The emphasis on "HER" and "personal attribute" may be significant.</div>
</section>
''')

# ── Sources ──
main_parts.append('''
<section class="page" id="sources">
<h1 class="page-title">Sources</h1>
<div class="page-subtitle">All data on this site is sourced from the following references.</div>

<table class="canon">
<thead><tr><th>Source</th><th>Description</th><th>Key contributions</th></tr></thead>
<tbody>
<tr><td><a href="https://www.meme.net.au/nkrypt/">meme.net.au/nkrypt</a></td><td>Glenn McIntosh</td><td>Most comprehensive analysis; pillar naming A-H; transcriptions; C++ rotor implementation; SVG diagrams</td></tr>
<tr><td><a href="https://www.dkrypt.org/">dkrypt.org</a></td><td>Greg Lloyd</td><td>High-resolution photographs; pillar numbering 1-8; detailed per-pillar pages</td></tr>
<tr><td><a href="https://scienceblogs.de/klausis-krypto-kolumne/">Cipherbrain (Klaus Schmeh)</a></td><td>Cryptology historian</td><td>Multiple articles; 2022 video interview with Kohlhagen; squircle codon hint</td></tr>
<tr><td><a href="https://www.questacon.edu.au/visiting/galleries/outdoor/exhibits/nkrypt">Questacon</a></td><td>Official source</td><td>Background, design intent, Centenary Code challenge</td></tr>
</tbody>
</table>

<h2>Machine-readable data</h2>
<p>All structured data from this site is available as <a href="nkrypt-data.json">nkrypt-data.json</a> for programmatic access and LLM consumption.</p>
</section>
''')

# ── Footer ──
main_parts.append('''
<div class="footer">
<p>NKRYPT Reference Site. Data compiled from meme.net.au, dkrypt.org, Cipherbrain, and Questacon sources.
This is an independent research project and is not affiliated with Questacon or Dr Stuart Kohlhagen.</p>
<p>Built April 2026. Hosted on GitHub Pages.</p>
</div>
''')

# ── Assemble ──
html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>NKRYPT - Canonical Reference</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="NKRYPT cryptographic sculpture - comprehensive reference site with all cipher data, solutions, and analysis.">
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
{sidebar}
</nav>
<main>
{"".join(main_parts)}
</main>
</div>
</body>
</html>'''

import os
out_path = os.path.join(os.path.dirname(__file__), 'index.html')
with open(out_path, 'w') as f:
    f.write(html_doc)

print(f"Written {len(html_doc):,} bytes to {out_path}")
