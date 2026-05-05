# NKRYPT -- Recommended Folder Structure for a Fresh Session

## Overview

This document describes the optimal folder layout for starting a fresh Cowork session on NKRYPT. The `docs/` folder contains the canonical reference site and data. Working files go in `working/`. Solutions go in `solutions/`.

## Folder Structure

```
nkrypt-v2/
├── INSTRUCTIONS.md              <-- Copy site/INSTRUCTIONS.md here as the Cowork project instructions
│
├── site/                        <-- CANONICAL REFERENCE (git repo: github.com/NKRYPT-Q/nkrypt)
│   ├── index.html               <-- Reference website (open in browser)
│   ├── nkrypt-data.json         <-- Machine-readable structured data (THE source of truth)
│   ├── build_site.py            <-- Site generator (run to rebuild after data changes)
│   ├── INSTRUCTIONS.md          <-- Clean instruction file (template)
│   └── NEW_SESSION_SETUP.md     <-- This file
│
├── reference-docs-md/           <-- Markdown conversions of external sources
│   ├── index.md                 <-- Index of all reference documents
│   ├── meme-net-au-nkrypt.md    <-- Glenn McIntosh's comprehensive analysis
│   ├── scienceblogs-articles.md <-- Klaus Schmeh's Cipherbrain articles
│   ├── dkrypt-org-1.md to dkrypt-org-8.md  <-- Per-pillar dkrypt.org pages
│   ├── base-code.md             <-- DNA STR loci data
│   ├── informational-plaque.md  <-- Plaque text
│   ├── nkrypt-tweet.md          <-- Senator Lundy's tweet
│   └── questacon-official.md    <-- Questacon official material
│
├── reference-docs/              <-- Key reference images and maps
│   ├── NKRYPT-map.png           <-- McIntosh aerial layout (plan view positions)
│   └── NKRYPT-whole-614.png     <-- Kohlhagen template (all 8 pillars, shared 2022)
│
├── pillars/                     <-- High-resolution photographs + vector sources
│   ├── Pillar 1 H - Title/     <-- = Pillar H (#1)
│   ├── Pillar 2 D - Cogs/      <-- = Pillar D (#2), includes Cogs.pdf, cogs.svg
│   ├── Pillar 3 F - Hexstars/  <-- = Pillar F (#3), includes Astroid.svg
│   ├── Pillar 4 B - Scytale/   <-- = Pillar B (#4)
│   ├── Pillar 5 G - Squircles/ <-- = Pillar G (#5), includes squircle.svg
│   ├── Pillar 6 C - Enigma/    <-- = Pillar C (#6)
│   ├── Pillar 7 A - Caesar/    <-- = Pillar A (#7)
│   └── Pillar 8 E - Bubbles/   <-- = Pillar E (#8)
│
├── working/                     <-- ALL session work goes here
│   ├── transcriptions/          <-- Machine-readable transcriptions
│   ├── analysis/                <-- One .md file per cipher being analysed
│   ├── tools/                   <-- Python scripts built during analysis
│   ├── figures/                 <-- Generated images, SVG overlays
│   ├── cache/                   <-- Expensive precomputed artefacts
│   └── results/                 <-- Output from one-shot experiments
│
└── solutions/                   <-- Confirmed or candidate solutions
```

## Session Start Procedure

1. Read `INSTRUCTIONS.md`
2. Read `site/nkrypt-data.json` (or load it programmatically)
3. Review `working/` directory for any prior session artefacts
4. Give a concise status summary and one recommended next action

## What to Put Where

| Content | Location |
|---------|----------|
| Cipher transcriptions (clean, machine-readable) | `working/transcriptions/` |
| Analysis notes per cipher | `working/analysis/{cipher_name}.md` |
| Python scripts and tools | `working/tools/` |
| Generated visualisations | `working/figures/` |
| Precomputed data (quadgrams, permutation caches) | `working/cache/` |
| Experiment output files | `working/results/` |
| Confirmed or candidate solutions | `solutions/` |
| Updates to canonical data | `site/nkrypt-data.json` (then rebuild site) |

## Key Files to Preserve

These files should never be modified:
- Everything in `pillars/`
- Everything in `reference-docs/`
- Everything in `reference-docs-md/`

These files can be updated when new data is confirmed:
- `site/nkrypt-data.json` (rebuild site with `python3 site/build_site.py` afterwards)
