# NKRYPT -- Recommended Folder Structure for a Fresh Session

## Overview

This document describes the optimal folder layout for starting a fresh Cowork session on NKRYPT. The `docs/` folder contains the canonical reference site and data. Working files go in `working/`. Solutions go in `solutions/`.

## Folder Structure

```
nkrypt-project/
├── INSTRUCTIONS.md              <-- Copy docs/INSTRUCTIONS.md here as the Cowork project instructions
│
├── docs/                        <-- CANONICAL REFERENCE (read-only during work)
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
├── reference-docs/              <-- Original .docx files + key images
│   ├── NKRYPT-map.png           <-- McIntosh aerial layout (plan view positions)
│   └── NKRYPT-whole-614.png     <-- Kohlhagen template (all 8 pillars, shared 2022)
│
├── photos/                      <-- High-resolution photographs (~220MB)
│   ├── Pillar 1 - Title/        <-- = Pillar H
│   ├── Pillar 2 - Cogs/         <-- = Pillar D (includes Cogs.pdf vector source)
│   ├── Pillar 3 - Hexstars/     <-- = Pillar F
│   ├── Pillar 4 - Scytale/      <-- = Pillar B
│   ├── Pillar 5 - Squircles/    <-- = Pillar G (includes squircle.svg)
│   ├── Pillar 6 - Enigma/       <-- = Pillar C
│   ├── Pillar 7 - Caesar/       <-- = Pillar A
│   └── Pillar 8 - Bubbles/      <-- = Pillar E
│
├── working/                     <-- ALL session work goes here
│   ├── PROGRESS_LOG.md          <-- Session log (update at end of every session)
│   ├── transcriptions/          <-- Machine-readable transcriptions
│   │   └── README.md            <-- Index of transcription files
│   ├── analysis/                <-- One .md file per cipher being analysed
│   ├── tools/                   <-- Python scripts built during analysis
│   │   └── README.md            <-- Tool catalogue
│   ├── figures/                 <-- Generated images, SVG overlays
│   │   └── Astroid.svg          <-- Canonical astroid source (369 astroids, vector)
│   ├── cache/                   <-- Expensive precomputed artefacts
│   └── results/                 <-- Output from one-shot experiments
│
└── solutions/                   <-- Confirmed or candidate solutions
    └── README.md                <-- Solution log with confidence levels
```

## Session Start Procedure

1. Read `INSTRUCTIONS.md`
2. Read `docs/nkrypt-data.json` (or load it programmatically)
3. Read `working/PROGRESS_LOG.md` (if it exists from a prior session)
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
| Updates to canonical data | `docs/nkrypt-data.json` (then rebuild site) |

## Key Files to Preserve

These files should never be modified:
- Everything in `photos/`
- Everything in `reference-docs/`
- Everything in `reference-docs-md/`

These files should only be modified by appending:
- `working/PROGRESS_LOG.md`

These files can be updated when new data is confirmed:
- `docs/nkrypt-data.json` (rebuild site with `python3 docs/build_site.py` afterwards)
