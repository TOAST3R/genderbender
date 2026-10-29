# AGENTS.md

Read `README.md` first for the layout and the style format.

## Conventions

- The code, comments, specs and commit text in this repo are in **Spanish**. Write new ones in Spanish too.
- Changes go through OpenSpec: `openspec/changes/<name>/` (proposal, design, tasks, specs). Use the `/opsx:propose`, `/opsx:apply` and `/opsx:archive` commands. Finished specs live in `openspec/specs/`. The skills need the `openspec` CLI 1.3.1. There is one copy, in `.claude/skills/`; `.opencode/`, `.codex/`, `.cursor/`, `.github/` and `.gemini/` each have a `skills` symlink to it. Don't edit the skills by hand. `openspec update --force .` writes through the links and leaves OpenCode's `/opsx-…` wording in the shared copy, so run `openspec init --tools claude .` after it. `adding-styles` is the one skill written by hand: it is not OpenSpec's, so edit it directly.
- The repo is on git (`origin` is https://github.com/TOAST3R/genderbender). Earlier versions of the plugin are in its history, not in a backup folder. Don't push without the user's go-ahead.

## Hard rules

- **Never hand-edit or rewrite existing `drum_styles_v/*.txt`.** It is one line in an exact format: voices joined by `/`, patterns joined by tabs, and a trailing tab. Generate files with `tools/make_style.py build`. A bad file silences the plugin without any error.
- Every style needs exactly 7 voices × 9 patterns × 32 steps, with values from 0 to 255.
- The plugin's slider 8 (`allStyles`) is unused, except that `countStyles()` in `@init` uses it to count the style files. Don't give it a real job without moving that count.
- `@gfx` height in the JSFX must match `NEW_H` in `tools/extend_bg.py` (currently 486).
- Do not renumber sliders. Presets and projects store them by index, and old presets must still load. Add new sliders at the end.
- Sliders 65 and 66 need a current REAPER (older versions allowed 64 sliders).
- The SuperCollider scripts in `editor/` find presets at `../presets/`, so every folder in `presets/` shows up as a preset. Put test or old presets in `presets_archive/`. Their REAPER save path is the `reaperFolder` setting at the top of each script.

## Checks

- Run `python3 tools/check_styles.py` after any change to styles or `tools/`. It must print `ok`.
- JSFX and timing changes can only be verified in REAPER. Install it with `sh tools/install.sh`, record the plugin's MIDI output, and check note positions against the spec. Past checks covered: no compile errors, all 66 sliders automatable, swing and slide offsets, loop wrap without double hits, no hung notes on stop or seek, and old presets loading with defaults.
- No SuperCollider (`sclang`) is installed on this machine.
