# NKRYPT Codebreaking Project

## What Is NKRYPT?

NKRYPT is a cryptographic sculpture installation outside Questacon (the National Science and Technology Centre) in Canberra, Australia. It consists of eight stainless steel pillars with codes and ciphers laser-cut into them. Installed in March 2013 for the Centenary of Canberra, it was designed by Dr Stuart Kohlhagen PSM (Deputy Director of Questacon).

Only about half of NKRYPT's codes have been publicly solved since 2013. The plaque reads: "From simple to hard, the key to the last is found in all the rest." The pillars are discrete but interlinked. Solving one provides clues to others. The final code requires a key that emerges from all other solutions.

Kohlhagen has stated there are approximately 60 puzzles on and around the eight columns, far more than the 16 directly visible ciphertexts. Some puzzles are layered and only become visible once another is solved.

---

## Reference Material

All reference data lives in this project folder. The canonical reference site is at `site/index.html`, which is also published as a GitHub Pages site. The machine-readable data backing it is at `site/nkrypt-data.json`.

**Priority order for lookups:**
1. `site/nkrypt-data.json` -- structured JSON with all pillar data, ciphertexts, solutions, and cross-references.
2. `site/index.html` -- the rendered reference site.
3. `reference-docs-md/` -- clean Markdown conversions of all external sources.
4. `reference-docs/` -- original images and maps.
5. `pillars/` -- high-resolution photographs of each pillar, plus vector source files (SVG, PDF).
6. Live web sources: [meme.net.au/nkrypt](https://www.meme.net.au/nkrypt/), [dkrypt.org](https://www.dkrypt.org/), [Cipherbrain](https://scienceblogs.de/klausis-krypto-kolumne/).

---

## Naming Conventions

Two naming schemes are in common use. Always reference both.

| meme.net.au letter | dkrypt.org number | Common name |
|----|----|----|
| A | 7 | Caesar |
| B | 4 | Scytale |
| C | 6 | Enigma/Rotor |
| D | 2 | Cogs |
| E | 8 | Braille/Bubbles |
| F | 3 | DNA/Hexstars |
| G | 5 | Squircles |
| H | 1 | Title/Labyrinth/PVL |

---

## The Eight Pillars

### Physical Properties

All ring ciphers sit at exactly **1709 mm** above ground (uniform across all 8 pillars). Height variation encodes the **extension above the ring**. Three independent per-pillar measurement channels exist:

| Pillar | Total height (mm) | Extension above ring (mm) | Fiducial separation (mm) | Fiducial direction | Traversal code |
|--------|-------------------|---------------------------|--------------------------|-------------------|---------------|
| A (#7) | 1709 | 0 | 0 | SE | DNOI |
| B (#4) | 1887 | 178 | 116 | NE | CFEC |
| C (#6) | 2153 | 444 | 354 | NE | FHIG |
| D (#2) | 2347 | 638 | 571 | SW | HWCJ |
| E (#8) | 2393 | 684 | 628 | SE | EFCF |
| F (#3) | 2379 | 670 | 636 | NW | CMBH |
| G (#5) | 2432 | 723 | 655 | SE | ???? |
| H (#1) | 2569 | 860 | 786 | NW | SMOU |

All three series are monotone in pillar letter (A smallest, H largest). They are different measurements and must not be conflated.

### Ring Cipher System (Labyrinth)

Every pillar carries a 26x5 symbol grid at ring height, read in a labyrinth (boustrophedon) pattern:
- Row 1: left to right
- Row 2: right to left
- Row 3: left to right
- Row 4: right to left
- Row 5: left to right

Between each pair of rows there is exactly one "down" transition and one "up" transition. The column positions of these four transitions give a 4-letter traversal code per pillar. These codes are believed to encode rotor settings for the Pillar C machine.

**Ring endpoints:** The end of the ring cipher is below the fiducial (pillars A, B, D, H) or 180 degrees from the fiducial (pillars C, E, F). Most start and end on the top row; pillar D starts on the bottom row.

**Pillar G's traversal code is unknown.** Solving the squircle cipher should reveal it.

### Pillar Pairings (SPECULATIVE)

**Status: Unverified hypothesis.** The following pairings were inferred from analysis of the Kohlhagen template (shared with Schmeh and Dunin in 2022) but have NOT been confirmed by the creator. Treat as one possible interpretation, not fact.

| Pair | Basis | Speculative cross-pillar hypothesis |
|------|-------|-------------------------------------|
| C and A | Tightest pair in template extent channels | A's solved Caesar/geospatial data may key C's rotor cipher |
| H and B | Compact upper, sparse lower | B's solved semaphore/scytale solutions feed H's PVL |
| G and F | Long lower ciphers | F's solved DNA codon output may key G's waveform |
| E and D | Mid lower, both pictographic | E's solved railfence/braille solutions may shift D's cogs |

Kohlhagen did confirm that pillars should be read in relation to each other, not independently. However, the specific pairing assignments above are analytical inferences and may be wrong. Alternative groupings should be considered.

### Constellation Layout

The eight pillars form a constellation pattern when viewed from above. Kohlhagen confirmed (2022) that positions and heights encode meaning. Working hypothesis: pillars B, G, F, C, D form the Southern Cross (Crux); pillars A, E, H are Alpha, Beta, and Omega Centauri. Thematic link: Centaurus/Centenary wordplay for Canberra's 1913-2013 centenary.

---

## Solved Ciphers

Each solved plaintext describes its own cipher's history or technique (self-referential). This is a confirmed meta-pattern.

### Pillar A (#7) -- Caesar
**Geospatial (lower):** Number string as GPS coordinates for 10 Canberra suburbs named after scientists. Solution to Questacon's Centenary Code challenge (2014). Solved by Glenn McIntosh.

**Caesar/shift/al-Kindi/Vigenere (upper):** Four stanzas, each encrypted with the technique the stanza describes. Final Vigenere key: `VIGENERE`. Solved by Gregory Lloyd.

### Pillar B (#4) -- Scytale
**Semaphore (ring):** Chappe semaphore system. Poem about French optical telegraph. Solved by Bob Dovenberg.

**Scytale (lower):** Hexagonal baton scytale. Poem about Histiaeus and Lysander of Sparta (404 BC). Solved by 'skintigh'.

### Pillar C (#6) -- Binary (ring only)
**Binary (ring):** Dash=1, dot=0 in 2x3 arrays. Names of 20 telegraph/wireless pioneers (Branly, Braun, Faraday, Gauss, Hertz, Marconi, Morse, Tesla, etc.). Solved by Glenn McIntosh.

### Pillar D (#2) -- Pigpen (ring only)
**Pigpen (ring):** Pigpen cipher in German. Queen of the Night aria from Mozart's Die Zauberfloete, ending with "1 2 3". Pigpen was a Freemason cipher; the opera has Masonic motifs. The "123" may reference the three opening chords, three Masonic pillars, or three veiled ladies. Solved by Bob Dovenberg.

### Pillar E (#8) -- Braille/Railfence
**Braille (ring):** Braille cipher (RTL lines upside-down). Poem about Napoleon, Barbier, and Louis Braille. Solved by Bob Dovenberg.

**Rail fence (lower):** Rail fence transposition. Poem about Alberti, Trithemius, and Rossignol. Solved by Matthew Bienik.

### Pillar F (#3) -- DNA (ring only)
**DNA codons (ring):** 3-letter codons to amino acid single-letter codes. "Far sighted lady, we may spawn a repainted thylacine." May reference Karen Firestone and thylacine DNA recovery. Solved by Bob Dovenberg.

### Pillar H (#1) -- Labyrinth (ring only)
**Labyrinth (ring):** Direct labyrinth cipher. "A labyrinth stands before you / and is but one of eight / Mark all the twists and turns / for patterns they create / That one by one step through / the enigmas that await." Solved by Glenn McIntosh.

**Title:** "NKRYPT" spelled vertically (trivial).

---

## Unsolved Ciphers

### Pillar C (#6) -- Rotor (lower)
An Enigma-like machine with four rotors plus a fixed reflector. Manual advancement (not automatic).

**Ciphertext:**
```
Line 1: BIOB AXQC NLPA MNXE SBNT FJLD DL
Line 2: JAWS FDHD MATX EJHM PVUJ XJOM KH
```
52 characters total. Line 1 has 6 groups of 4 plus orphan pair DL. Line 2 has 6 groups of 4 plus orphan pair KH.

**Rotor wirings:**
```
Rotor 1: ABCDEFGHIJKLMNOPQRSTUVWXYZ -> UDBCFGEJHILMKTSNOPQRWXYZAV
Rotor 2: ABCDEFGHIJKLMNOPQRSTUVWXYZ -> BZCXWHIFGLMJKVUPSQRTONEDYA
Rotor 3: ABCDEFGHIJKLMNOPQRSTUVWXYZ -> ZADEFGCHMIJKLOPQRNWSTUVBXY
Rotor 4: ABCDEFGHIJKLMNOPQRSTUVWXYZ -> BDFCEGIJKLSMAZNHOPQRTVXUWY
Reflector: ABCDEFGHIJKLMNOPQRSTUVWXYZ -> ZYVMLIHGFKJEDURQPOTSNCXWBA
```

The machine is involutive (encrypt = decrypt with same key when rotors are not advanced). A 4-letter key sets rotor offsets. A C++ implementation exists at meme.net.au/nkrypt/enigma.cpp.

Key fact: `ROT13(FJLD) = SWYQ`. Using rotor key SWYQ with no advancement decodes the last 16 characters of Senator Lundy's opening-day tweet to "thecentenarycode".

### Pillar D (#2) -- Cogs (lower)
71 cog-shaped glyphs across 7 columns (16, 10, 9, 10, 10, 7, 9 cogs per column).

**Variables per cog:** number of tooth sets (2, 3, or 4), dot angle (clockwise from north), number of internal dots, and tooth arc extents.

**Mesh-compatibility groups (43 groups across 71 cogs):**
| Col | Groups | Pattern |
|-----|--------|---------|
| 1 | 9 | A \| BCD \| E \| F \| G \| HIJK \| L \| MNO \| P |
| 2 | 5 | A \| BC \| DEFGH \| I \| J |
| 3 | 7 | AB \| C \| D \| E \| FG \| H \| I |
| 4 | 6 | ABCD \| EF \| G \| H \| I \| J |
| 5 | 4 | AB \| C \| DE \| FGHIJ |
| 6 | 5 | A \| B \| CD \| E \| FG |
| 7 | 7 | A \| B \| C \| D \| E \| FG \| HI |

Authoritative vector sources: `pillars/Pillar 2 D - Cogs/Cogs.pdf` and `pillars/Pillar 2 D - Cogs/cogs.svg`. Note: horizontal spacing between columns is inaccurate (parallax); only vertical order within columns is reliable.

### Pillar F (#3) -- Astroids (lower)
Four-pointed star glyphs (U+2726) in 42 columns with irregular vertical spacing. Each astroid is approximately 15 mm across, columns spaced approximately 22 mm apart.

**Per-column counts:** [4, 4, 18, 6, 4, 10, 3, 13, 4, 13, 8, 12, 4, 4, 3, 12, 9, 11, 9, 8, 12, 4, 10, 10, 13, 16, 11, 14, 7, 12, 6, 4, 6, 3, 11, 6, 16, 15, 6, 8, 12, 8]

Mean 8.79 per column, range 3-18, 14 distinct count values. Canonical source: `pillars/Pillar 3 F - Hexstars/Astroid.svg` (369 astroids with sub-pixel y precision). Conjecture: may represent light spectra.

### Pillar G (#5) -- Squircles (ring)
10x26 grid of 4-orientation petal/cam shapes (encoded 0-3):
```
R01: 01110011011101021231331012
R02: 02030013322303333000200032
R03: 21221133103032320102000132
R04: 23123002121223001301131123
R05: 10103100010101201201221103
R06: 30212131033000203011112330
R07: 30101111212032132012210133
R08: 13303323023120222333322012
R09: 00000101022001203231310031
R10: 30110333202120112302112123
```

**Creator hints (Kohlhagen via Schmeh, confirmed):**
- Squircles group in vertical pairs to form a 26x5 labyrinth grid (same as all ring ciphers).
- Each plaintext letter is represented by 4 squircles (codon-like redundancy).
- 260 cells / 4 = approximately 65 letters of plaintext.
- "Squircles was one of the few of the labyrinth codes that was developed with a bit of encryption strategy."

**Known structure:** Using pair-boustrophedon reading with odd start column, there are 50 distinct 4-cell patterns across 65 positions. One pattern (1,3,0,3) appears 8 times (12.3%), consistent with English E (12.7%).

### Pillar G (#5) -- Waveform/Helix (lower)
515 characters in double-helix visual layout:
```
UWGHTLIYCOEYDY
RFKVOACMHPUCEAL
BANYUJHEESHABPS
NAYIDQGILTIVKTE
FAESOKTMZQDMRGH
HYLHNICNLBNWWXX
KGAPYHIIQHSKETZ
RRENUCMTVUINLZR
ICYRFFGTKDNBQSH
NLXZWKMVCICTCDD
ZAOWRSUNVMDOIXG
ZCCFCUEAKAKFSMP
YRHUUTMCYSSMPFG
TUCIESREQXAICHL
LYVBKNNZVBPKNQA
EXQSHOSGVZDHDFM
HYPHCUDQTMWVNEK
NGACBGTSACXEHRE
DUUHNQVDATWTIEK
ZRFHTOFRUPTKHNP
XYNFBBHWPVSSKIN
NOHYWLJQZKWRSQO
UIEEQKYEMPRQEDM
IVSVAPNGKDVPQME
XGCIOAVXVIGTPIQ
ORDQRJEKWFPVWZP
ECYNYRCGWWIFCYX
GVLGPLBSJGMIJCX
RHYEOHHWTXOAGYS
FSDOZGZJGNPTRUA
ESTRPYFTJVZQHOP
EQLOQRGPHPKEDEI
IQHCZYWPJZKAZQA
KSKMIPLDRGCWCAD
GZCDBB
```

35 lines (14 + 33x15 + 6 chars). Lines offset like a double-helix projection. IC = 1.014 (flat). Frequency distribution is near-uniform. Not simple substitution or transposition.

### Pillar H (#1) -- PVL (upper, FINAL PUZZLE)
26x10 letter grid above the ring cipher. Letters P, V, L appear in larger font.
```
OXPUWAOEKZVCRLUYFMLXTPNATW
VGZTCGVGDAAXFDKOCRFRUOKAPW
LCMPTFPBTYXRSZKKQUBJAMHYUL
MZVSXXZHDLYHOKWWEJUXLXKRZU
PPESLBOEKOGRTAYDFOHRHVMPBN
DTEZBTYDXNMPXHVNKCIYEMJFVE
MNKDIQBOSUFFFWBVDNKHRTLIMZ
WRRQUFNNBGKUWNQCHDEFSTZZRQ
UIUDPTKGATPSJIFXXGGSNTWJLA
BRYVUCSBNPYAVSTTONZFWIUUNW
```

Frequency distribution is flat (not simple substitution). Likely requires combined keys/information from all other ciphers. This is the final puzzle.

### Opening Day Tweet (partially solved)
Senator Kate Lundy tweeted on 4 March 2013:
```
hdxjnfjxzjezthdbmmwqzjturogoucrfruohhzmlqpmbkuykkcrnkdlndlxjnidihjihqkwdpci
```
75 characters. Last 16 decode to "thecentenarycode" using rotor key SWYQ. First 59 characters are unsolved.

Kohlhagen wrote: "the piece was developed before we had her or the idea of a coded tweet in mind... perhaps thinking about how a person might select a protocol based on a specifically personal 'attribute' might help with HER tweet."

---

## Base Code DNA

15 autosomal STR loci per pillar base, matching PowerPlex 16 HS forensic DNA profiling. Loci order (alphabetic): CSF1PO, D13S317, D16S539, D18S51, D21S11, D3S1358, D5S818, D7S820, D8S1179, FGA, PentaD, PentaE, TH01, TPOX, vWA.

Full profiles are in `site/nkrypt-data.json`. Population: European/Asian origin probable. Conjectured parental connections: AE to D, HD to F, HD to G, and either HD to B or HB to C.

---

## Key Principles for Working on NKRYPT

1. **Self-referential plaintexts.** Every solved cipher's plaintext describes its own technique or history. Use this to predict themes for unsolved ciphers.
2. **Pillar pairings.** Cross-pillar attacks should target structural pairs first.
3. **No modern cryptography.** Kohlhagen confirmed none of the ciphers use AES, DES, RSA, or similar.
4. **Layered puzzles.** Some puzzles only become visible after others are solved.
5. **The plaque is the roadmap.** "From simple to hard, the key to the last is found in all the rest."
6. **Approximately 60 total puzzles.** Far more than the 16 visible ciphertexts.
7. **Physical properties encode meaning.** Heights, positions, fiducial directions, and fiducial separations all carry information.

---

## Working Rules

- **Australian English** in all output.
- **No hallucinations.** Flag uncertainty. If unsure about a transcription or analysis, say so.
- **Show your working.** Document method, parameters, and results for every attempt.
- **Preserve original data.** Never modify files in `pillars/` or `reference-docs/`. Work in `working/`.
- **Small steps.** Start with one approach and check in before trying the next.
- **Cite sources.** Note whether information came from meme.net.au, dkrypt.org, Schmeh, or the canonical JSON.
- **Use the JSON.** `site/nkrypt-data.json` is the single source of truth for all structured data. Read it before starting work on any cipher.
- **Distinguish fact from hypothesis.** Clearly label what is confirmed by Kohlhagen versus what is analytical inference or conjecture.
