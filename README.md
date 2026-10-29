# GenderBender

A MIDI drum-pattern generator for REAPER (JSFX plugin). It plays 7 voices (kick, snare, clap, closed hat, open hat, high tom, low tom) from styles of 9 patterns each, blended with an XY pad.

**[See every style's patterns →](https://toast3r.github.io/genderbender/fingerprints.html)**

## Install

```sh
sh tools/install.sh                                   # macOS
REAPER_DIR="$APPDATA/REAPER" sh tools/install.sh     # Windows (Git Bash) or another folder
```

In REAPER, add **MIDI GenderBender** to a track, send its MIDI to a drum sampler (base note 36), and press play. **ALL RND** picks a random style for all voices, **EACH RND** one per voice.

Other DAWs: load `Effects/GenderBender/genderbender.jsfx` in the [ysfx](https://github.com/JoepVanlier/ysfx) instrument plugin (VST3/AU/CLAP). Install with `REAPER_DIR=<some folder> sh tools/install.sh` so `Effects/` and `Data/` sit side by side.

## Writing a style

Write a `.style` file in `styles_src/`, build it, and check it:

```sh
python3 tools/make_style.py build styles_src/cumbia_villera_98.style    # -> drum_styles_v/CUMBIA VILLERA 98.txt
python3 tools/make_style.py decode "drum_styles_v/GQOM.txt"            # print an existing style as a grid
python3 tools/view_styles.py                                           # update docs/fingerprints.html
python3 tools/check_styles.py                                          # must print "ok"
```

```
name: MY STYLE 120
[p4 p5]                       # these patterns get the lines below
kick   X... .... X... ....    # 16 chars = 16ths, 32 = 32nds; spaces ignored
hhc    XXxX XXxX XXxX XXxX
```

- Levels: `X=255 x=204 o=153 -=102 ,=51 .=0`, or `[n]` for 0–255. `decode` snaps each value to the nearest level. At default density only `X` plays.
- Voices: `kick`, `snare`, `clap`, `hhc`, `hho`, `hitom`, `lotom`.
- Never edit `drum_styles_v/*.txt` by hand: a bad file silences the plugin with no error.

## Layout

| Path | What it is |
|------|------------|
| `GenderBender/` | The plugin, its background and preset library |
| `drum_styles_v/` | Styles the plugin loads |
| `styles_src/` | Readable style sources |
| `tools/` | Style build/check scripts and the installer |
| `docs/` | Style fingerprints page (GitHub Pages) |
| `editor/`, `presets/` | The original SuperCollider style editor and its presets |
| `openspec/` | Specs and change proposals |

## Included styles

| Family | Styles (BPM) |
|--------|--------------|
| Afro / Caribbean | AFRO BEAT, AFRO BEAT & JU JU, SOCA, 101 ZOUK KIZOMBA, ZOUK KIZOMBA 2 |
| Afro / Latin club | AMAPIANO 112 (112), AFRO HOUSE 122 (122), KUDURO 135 (135), GUARACHA 130 (130), SINGELI 200 (200), NORTEC 125 (125) |
| Bass music | FUTURE BASS 150 (150), MIDTEMPO BASS 105 (105) |
| Breaks | BIG BEAT 125 (125), BALTIMORE CLUB 130 (130), BREAKCORE 190 (190), JERSEY BASICS, DRILL N BASS 175 (175), BROKEN BEAT 120 (120) |
| Cumbia | CUMBIA COLOMBIANA (95), CUMBIA SONIDERA (92), CUMBIA VILLERA (98), CUMBIA DIGITAL (100), CUMBIA REBAJADA (72), CUMBION |
| Downtempo / chill | BOSSA NOVA CHILL 100 (100) |
| Drum & bass | JUNGLE 165 (165), RAGGA JUNGLE 165 (165), HARDSTEP 172 (172), JUMP-UP 174 (174), DANCEFLOOR DNB 174 (174), TECHSTEP 172 (172), HALFTIME 174 (174), drumbass, DurumBass160 (160), DURUMBREAK_160 (160), SAMBASS 172 (172), NEUROFUNK 174 (174), LIQUID DNB 174 (174) |
| Dubstep | DUBSTEP140 (140), DubSteppo, 101 STEPPA, RIDDIM 140 (140) |
| EBM / industrial | EBM 120 (120), BELGIAN EBM 118 (118), NEW BEAT 110 (110), AGGROTECH 140 (140), DARK ELECTRO 125 (125), EBM TECHNO 130 (130) |
| Electro / Miami bass | ELECTRO CYBOTRON, ELECTRO UR 138 (138), BASS 101 |
| Footwork / juke | 101 JUKE, Juke160 (160), 101 FOOTWORK, 102 JUKE |
| Funk / New Orleans | MOTOWN BREAKS, NEW ORLEANS, NEW ORLEANS BOUNCE, ACID JAZZ 105 (105) |
| Gqom | GQOM |
| Grime | GRIME140 (140), Grimer140 (140) |
| Hard house | UK HARD HOUSE 150 (150), HARD NRG 155 (155), SCOUSE HOUSE 150 (150), CHICAGO HARD HOUSE 135 (135), DUTCH HOUSE 128 (128) |
| Hardcore / hard dance | TRANCE 138 (138), MAKINA 170 (170), GABBER 180 (180), GABBER ROLL 180 (180), HAPPY HARDCORE 170 (170), FRENCHCORE 200 (200), INDUSTRIAL HARDCORE 150 (150), HARDSTYLE 150 (150), BAKALAO 125 (125) |
| Hip-hop | BOOM BAP 90 (90), LOFI HIPHOP 82 (82), TRIP HOP 88 (88), NEW JACK SWING 104 (104) |
| House | Chicago.Jouse 125 (125), JetoHouse 135 (135), MIAMI BEIGE 135 (135), DEEP HOUSE 122 (122), TECH HOUSE 126 (126), GHETTOTECH 150 (150), ACID HOUSE 124 (124), ITALO HOUSE 122 (122), MICROHOUSE 124 (124) |
| IDM / experimental | GLITCH HOP 110 (110), IDM 120 (120), SKWEEE 100 (100), DECONSTRUCTED CLUB 130 (130) |
| Phonk | PHONK 130 (130), DRIFT PHONK 155 (155), BRAZILIAN PHONK 130 (130) |
| Psytrance | GOA TRANCE 145 (145), FULL-ON 145 (145), PROGRESSIVE PSY 138 (138), DARK PSY 150 (150), FOREST PSY 150 (150), PSYCORE 190 (190), ZENONESQUE 135 (135), MINIMAL PSY 140 (140), HI-TECH 180 (180), NITZHONOT 150 (150), SUOMISAUNDI 150 (150), PSYBREAKS 135 (135), PSYDUB 100 (100), PSYBIENT 100 (100) |
| R&B / trap | RB, WCOAST R&B 110 (110), VAPORTRAP, TRAP 140 (140), UK DRILL 142 (142) |
| Rave / oldskool | RAVE 91 130 (130), HARDCORE TECHNO 145 (145), BREAKBEAT HARDCORE 145 (145), DARKCORE 155 (155) |
| Reggaeton / dancehall | 101 RAGATON, 101 DANCEHALL, 101 FUNK FAVELA, DEMBOW 120 (120), FUNK DE RAIZ 130 (130) |
| Synth / disco | SYNTHWAVE 100 (100), DISCO 118 (118), ITALO DISCO 120 (120), BOOGIE 110 (110), MOTORIK 120 (120) |
| Techno | techAXX, TekkBooooring, TekkChungo, TekkThump, SCHAFFEL 125 (125), DETROIT TECHNO 128 (128), MINIMAL TECHNO 126 (126), HARD TECHNO 145 (145), ACID TECHNO 140 (140), UK TECHNO 135 (135), DUB TECHNO 118 (118), SCHRANZ 150 (150), HARDGROOVE 135 (135) |
| UK garage / 2-step | Two-stepppo, uk_fungui, uk_garbage, garage_2step, garage_uk_4x4, FUTURE GARAGE 130 (130) |
| Other | 101 SPARSE, BELLY DANCE, ZZZ BLACK |

This table also sets the families on the fingerprints page, so keep its format.

## Contributing

GenderBender is free software and contributions are welcome: new styles, bug fixes, ideas. Open an [issue](https://github.com/TOAST3R/genderbender/issues) to report a problem or suggest something, or fork the repo and send a pull request. For a new style, include its `.style` source and make sure `tools/check_styles.py` prints `ok`.

Bigger changes go through [OpenSpec](https://github.com/Fission-AI/OpenSpec) (`npm install -g @fission-ai/openspec@1.3.1`, then `/opsx:propose`, `/opsx:apply`, `/opsx:archive`). AI agents: read `AGENTS.md`.

## License

Original version by Sergio Millán. Released under the [GNU GPL v3](LICENSE): you can use, study, modify and share it, and modified versions you distribute must stay under the GPL.
