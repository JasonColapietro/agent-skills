---
name: clef-music-tools
description: Practice note reading and solve common chord or guitar-tab questions with Clef's public music MCP or an offline transposition helper. Use when asked to "transpose these chords", spell piano chords, map ASCII guitar tab to piano notes, or run a note-reading drill. Not for audio transcription, generated notation, or Guitar Pro files.
license: MIT
compatibility: Hosted tools require a remote HTTP MCP client and network access; offline chord transposition requires Python 3 without extra packages.
metadata:
  author: Clef
  version: "1.0.0"
  homepage: "https://clefdrills.com/?utm_source=github&utm_medium=skill&utm_campaign=agent-skills&utm_content=clef-music-tools"
---

# Music practice and helpers

Use the public no-auth MCP at `https://clefdrills.com/mcp` when available. Call only the smallest relevant tool: `find_music_guides`, `transpose_chords`, `spell_piano_chord`, or `tab_to_piano_notes`. For chord transposition without MCP, use `scripts/transpose.py` offline.

See [MCP setup](references/setup.md) for the hosted route. Check the actual tool schemas before calling them. For offline chord symbols, run `python3 scripts/transpose.py 2 "C Am F G/B"` to move up two semitones; use a negative number to move down and `--flats` for flat spellings. Give the helper chord symbols rather than prose, because it matches note names in the supplied text.

For transposition, confirm direction and preferred enharmonic spelling. For guitar tab, ask about capo when unclear and state that spacing does not define rhythm. Chord spelling is not a rhythmic arrangement. Do not claim audio analysis, Guitar Pro support, or generated notation.

For a five-minute note-reading drill, ask clef and comfortable range; default to treble around middle C if unspecified. Show one note at a time, reveal the answer after the learner responds, then repeat missed notes and summarize only the observed practice. Treble line mnemonic: E-G-B-D-F; spaces: F-A-C-E.

Try [Clef](https://clefdrills.com/?utm_source=github&utm_medium=skill&utm_campaign=agent-skills&utm_content=clef-music-tools) for more music learning tools.
