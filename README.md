# GenderBender

A MIDI drum-pattern generator for REAPER, written as a JSFX plugin, plus the tools used to write its drum styles.

The plugin plays 7 voices: kick, snare, clap, closed hat, open hat, high tom and low tom. Each style has 9 patterns (p0–p8). An XY pad blends between patterns. Per-voice controls set density, division, break, velocity and duration, and a GROOVE strip adds swing and slide.

## Layout

| Path | What it is |
|------|------------|
| `GenderBender/genderbender.jsfx` | The plugin (66 sliders, GUI designed at 686×486 and scaled to the window) |
| `GenderBender/genderbender.jsfx-ysfx.rpl` | Preset library (one preset, CUMBIA SONIDERA) |
| `GenderBender/bg.png` | GUI background, generated from `bg_original.png` by `tools/extend_bg.py` |
| `drum_styles_v/*.txt` | Styles the plugin loads (sliders 1–8 read this folder) |
| `styles_src/*.style` | Readable sources for the cumbia styles |
| `tools/make_style.py` | Builds a `.style` into a `.txt`, or decodes a `.txt` back into a `.style` |
| `tools/extend_bg.py` | Regenerates `bg.png` (needs Pillow) |
| `tools/check_styles.py` | Checks that every style is valid and that every source matches its `.txt` |
| `tools/install.sh` | Copies the plugin and the styles into REAPER |
| `editor/` | The original SuperCollider style editor (`Gender_bender_editor.scd`, plus the older `drummermenu*.scd`) |
| `presets/` | The editor's presets (`.preset`, `.h`, `.txt` in the editor's own format, not the plugin's) |
| `presets_archive/` | Test presets kept out of the editor's list |
| `openspec/` | Specs and change proposals (OpenSpec workflow) |

## Included styles

There are 31 styles in `drum_styles_v/`, each with 9 patterns. The BPM comes from the style's name, and the plugin doesn't set the tempo.

| Family | Styles (BPM) |
|--------|--------------|
| Cumbia | CUMBIA COLOMBIANA (95), CUMBIA SONIDERA (92), CUMBIA VILLERA (98), CUMBIA DIGITAL (100), CUMBIA REBAJADA (72) |
| Footwork / juke | 101 JUKE, Juke160 (160) |
| Reggaeton / dancehall | 101 RAGATON |
| House | Chicago.Jouse 125 (125), JetoHouse 135 (135), MIAMI BEIGE 135 (135) |
| UK garage / 2-step | Two-stepppo, uk_fungui, uk_garbage |
| Grime | GRIME140 (140), Grimer140 (140) |
| Dubstep | DUBSTEP140 (140), DubSteppo |
| Drum & bass | drumbass, DurumBass160 (160) |
| Techno | techAXX, TekkBooooring, TekkChungo, TekkThump |
| R&B / trap | RB, WCOAST R&B 110 (110), VAPORTRAP |
| Gqom | GQOM |
| Other | ESTAIL, TEST2, ZZZZ BLACK |

- Only the cumbias have readable sources in `styles_src/`; the rest were made with the SuperCollider editor, and most have a matching folder in `presets/`.
- `DUBSTEP140`, `RB` and `TekkChungo` had patterns the plugin couldn't read: an empty editor pattern saved as `i`, and `-10.0` values. Those voices kept playing whatever the previous style had loaded. They're now empty (all 0): DUBSTEP140 kick p1, TekkChungo kick p2, and RB open hat in every pattern except p1.
- In `ZZZZ BLACK`, `ESTAIL`, `GQOM` and `TEST2`, the FILL pattern (p8) is empty.
- `presets/` also has folders with no style in `drum_styles_v/`: `DURUMBASS_160` and `DURUMBREAK_160`, plus these newer grooves that still need exporting from the SuperCollider editor before the plugin can play them: 101 DANCEHALL, 101 FOOTWORK, 101 FUNK FAVELA, 101 SPARSE, 101 STEPPA, 101 ZOUK KIZOMBA, 102 JUKE, AFRO BEAT, AFRO BEAT & JU JU, BASS 101, BELLY DANCE, BOUNCE, CUMBION, ELECTRO CYBOTRON, ELECTRO UR 138, JERSEY BASICS, MOTOWN BREAKS, NEW ORLEANS, NEW ORLEANS BOUNCE, SOCA, TekkBooooring 2222 and ZOUK KIZOMBA 2.

## Install in REAPER

The plugin runs from REAPER's resource folder, not from this repo. Run the installer after each change:

```sh
sh tools/install.sh                                   # macOS
REAPER_DIR="$APPDATA/REAPER" sh tools/install.sh     # Windows (Git Bash), or any other resource folder
```

It copies:

- `GenderBender/*` → `<REAPER>/Effects/GenderBender/` (the plugin, its background and the preset library)
- `drum_styles_v/*.txt` → `<REAPER>/Data/drum_styles_v/`

Files with the same name are overwritten, and nothing is deleted, so styles you removed or renamed here stay in REAPER until you delete them there. If the REAPER folder doesn't exist, the script stops without copying anything. In REAPER, **Options → Show REAPER resource path** shows the folder to use for `REAPER_DIR`.

Then add **MIDI GenderBender** (`genderbender.jsfx`) to a track, send its MIDI to a drum sampler (base note 36 by default), and press play. **ALL RND** gives every voice the same random style; **EACH RND** picks one per voice.

Projects saved with the plugin's old name still point to the old file. REAPER finds JSFX by file name, so keep the old plugin installed for them or swap in GenderBender in each project.

## Use in other DAWs (VST3 / AU / CLAP via ysfx)

JSFX only runs in REAPER, but [ysfx](https://github.com/JoepVanlier/ysfx) (the maintained fork) is a VST3/AU/CLAP plugin that loads `.jsfx` files in any DAW. GenderBender only uses standard JSFX features, so it should load as is.

1. Install ysfx from its releases page.
2. Install GenderBender into any folder with the same installer. It creates the `Effects/` + `Data/` layout ysfx expects:

   ```sh
   REAPER_DIR="$HOME/Documents/GenderBender-ysfx" sh tools/install.sh
   ```

   If REAPER is installed, you can skip this and point ysfx at REAPER's resource folder instead.
3. In the DAW, add the ysfx **instrument** (the variant with MIDI output), load `Effects/GenderBender/genderbender.jsfx`, and route its MIDI output to a drum sampler. How you route MIDI out of a plugin depends on the DAW.

Check these the first time:

- **Style lists are empty:** ysfx didn't find `Data/drum_styles_v/`. Keep `Effects/` and `Data/` side by side in the same folder.
- **The hitom and lotom slides (sliders 65 and 66) are missing:** the ysfx build only supports 64 sliders. Update ysfx. The sliders can't be renumbered.
- **GUI text is slightly off:** ysfx draws fonts its own way. This is cosmetic.

The SuperCollider editor still saves styles to REAPER's `Data/drum_styles_v/`. To use it with ysfx, change its `reaperFolder` setting or copy the `.txt` files across.

## Writing a style

```sh
python3 tools/make_style.py build styles_src/cumbia_villera_98.style    # -> drum_styles_v/CUMBIA VILLERA 98.txt
python3 tools/make_style.py decode "drum_styles_v/GQOM.txt"            # prints a readable grid
```

The `.style` format:

```
name: MY STYLE 120
[p4 p5]                       # these patterns get the lines below
kick   X... .... X... ....    # 16 chars = 16ths, 32 = 32nds; spaces ignored
hhc    XXxX XXxX XXxX XXxX
```

- Levels: `X=255 x=170 o=120 -=60 .=0`, or `[n]` for an exact value from 0 to 255.
- Voices: `bdrum|kick`, `sdrum|snare`, `clap`, `hhclosed|hhc`, `hhopen|hho`, `hitom`, `lotom`.
- Density decides which steps play. At the default (50), only `X` plays. Put the core rhythm on `X` and the ornaments on lower levels.
- Cumbia pad layout: p4/p5 BASE (center), p2/p3 ENERGY, p6/p7 VARIATION, p0/p1 INTRO, p8 FILL.

A malformed `.txt` makes the plugin go silent without showing an error, so check styles before installing them:

```sh
python3 tools/check_styles.py
```

The checker:

- decodes every `drum_styles_v/*.txt` (7 voices × 9 patterns × 32 steps, values 0–255) and checks it writes back byte for byte;
- builds every `styles_src/*.style` and checks it matches its `.txt` exactly (if not, run `make_style.py build` again).

It prints `ok`, or one line per problem and exits with code 1. Run it after any change to a style or to `tools/`, then listen to the style in REAPER.

## SuperCollider editor

Open `editor/Gender_bender_editor.scd` in SuperCollider. It lists the folders in `presets/` and, when you save, also writes the playable `.txt` straight into REAPER's `Data/drum_styles_v/`. That path is set once, near the top of the file. Copy new styles back into `drum_styles_v/` here so they're kept in the repo.

## Contributing with an AI agent

Changes follow [OpenSpec](https://github.com/Fission-AI/OpenSpec). The repo includes its skills and commands for Claude Code (`.claude/`), OpenCode (`.opencode/`), Codex (`.codex/`), Cursor (`.cursor/`), GitHub Copilot (`.github/`) and Gemini CLI (`.gemini/`). The skills live once in `.claude/skills/`, and each other folder links to it. They need the CLI:

```sh
npm install -g @fission-ai/openspec@1.3.1
```

Then use `/opsx:propose`, `/opsx:apply`, `/opsx:archive` and `/opsx:explore` (`/opsx-…` in OpenCode, Cursor and Copilot; Codex has no slash commands, so ask it to use the `openspec-propose` skill and so on). Agents also read `AGENTS.md`. To add another agent, run `openspec init --tools <tool> .`, then replace its new `skills` folder with a symlink: `rm -r .<tool>/skills && ln -s ../.claude/skills .<tool>/skills`.
