# GenderBender

A MIDI drum-pattern generator for REAPER (JSFX plugin). It plays 7 voices (kick, snare, clap, closed hat, open hat, high tom, low tom) from styles of 9 patterns each, blended with an XY pad.

**[See every style's patterns →](https://toast3r.github.io/genderbender/fingerprints.html)** Press **▶ Play** on any style to hear its base loop at its BPM (synthesized drums, not your sampler; Density and swing apply).

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
| Afro / Caribbean | AFRO BEAT & JU JU (110), SOCA (155), 101 ZOUK KIZOMBA (90), ZOUK KIZOMBA 2 (90) |
| Afro / Latin club | AMAPIANO 112 (112), AFRO HOUSE 122 (122), KUDURO 135 (135), GUARACHA 130 (130), SINGELI 200 (200), NORTEC 125 (125) |
| Bass music | FUTURE BASS 150 (150), MIDTEMPO BASS 105 (105) |
| Brazil | MARACATU 90 (90), FREVO 140 (140), SAMBA 100 (100), BAIAO 100 (100), AXE 130 (130) |
| Breaks | BIG BEAT 125 (125), BALTIMORE CLUB 130 (130), BREAKCORE 190 (190), JERSEY BASICS (140), DRILL N BASS 175 (175), BROKEN BEAT 120 (120) |
| Celtic | REEL 110 (110), JIG 115 (115), STRATHSPEY 120 (120), IRISH POLKA 140 (140) |
| Country / Americana | BLUES SHUFFLE 100 (100), WESTERN SWING 170 (170), BLUEGRASS 120 (120), COUNTRY SHUFFLE 120 (120), TRAIN BEAT 110 (110), ROCKABILLY 180 (180), ZYDECO 120 (120), TWO-STEP 140 (140) |
| Cumbia | CUMBIA COLOMBIANA (95), CUMBIA SONIDERA (92), CUMBIA VILLERA (98), CUMBIA DIGITAL (100), CUMBIA REBAJADA (72), CUMBION (95) |
| Downtempo / chill | BOSSA NOVA CHILL 100 (100) |
| Drum & bass | JUNGLE 165 (165), RAGGA JUNGLE 165 (165), HARDSTEP 172 (172), JUMP-UP 174 (174), DANCEFLOOR DNB 174 (174), TECHSTEP 172 (172), HALFTIME 174 (174), drumbass (174), DurumBass160 (160), DURUMBREAK_160 (160), SAMBASS 172 (172), NEUROFUNK 174 (174), LIQUID DNB 174 (174) |
| EBM / industrial | EBM 120 (120), BELGIAN EBM 118 (118), NEW BEAT 110 (110), AGGROTECH 140 (140), EBM TECHNO 130 (130) |
| Electro | CYBOTRON ELECTRO 125 (125), ELECTRO FUNK 127 (127), DARKWAVE 120 (120), ELECTRO BASS 130 (130), DETROIT ELECTRO 130 (130), DARK ELECTRO 125 (125), GHETTOTECH 150 (150), ELECTROCLASH 125 (125), ELECTRO HOUSE 128 (128), SYNTHWAVE 100 (100), OUTRUN 118 (118), INDUSTRIAL ELECTRO 130 (130) |
| Flamenco | TANGOS 100 (100), TIENTOS 75 (75), BULERIA 80 (80), SOLEA 50 (50), SEGUIRIYA 45 (45), SEVILLANA 65 (65), FANDANGO DE HUELVA 60 (60) |
| Folk ibérico | MUINEIRA 120 (120), PASACORREDOIRA 110 (110), MARCHA PROCESIONAL 70 (70), ARIN-ARIN 130 (130), BIRIBILKETA 110 (110), JOTA ARAGONESA 60 (60), SARDANA 100 (100), BALL DE BASTONS 110 (110), TAJARASTE 110 (110) |
| Footwork / juke | 101 JUKE (160), Juke160 (160), 101 FOOTWORK (160), 102 JUKE (160) |
| Funk / New Orleans | MOTOWN BREAKS (100), NEW ORLEANS (95), NEW ORLEANS BOUNCE (100), ACID JAZZ 105 (105) |
| Gqom | GQOM (122) |
| Hard house | UK HARD HOUSE 150 (150), HARD NRG 155 (155), SCOUSE HOUSE 150 (150), CHICAGO HARD HOUSE 135 (135), DUTCH HOUSE 128 (128) |
| Hardcore / hard dance | TRANCE 138 (138), MAKINA 170 (170), GABBER 180 (180), GABBER ROLL 180 (180), HAPPY HARDCORE 170 (170), FRENCHCORE 200 (200), INDUSTRIAL HARDCORE 150 (150), HARDSTYLE 150 (150), BAKALAO 125 (125) |
| Hip-hop | BOOM BAP 90 (90), LOFI HIPHOP 82 (82), TRIP HOP 88 (88), NEW JACK SWING 104 (104) |
| House | Chicago.Jouse 125 (125), JetoHouse 135 (135), MIAMI BEIGE 135 (135), DEEP HOUSE 122 (122), TECH HOUSE 126 (126), ACID HOUSE 124 (124), ITALO HOUSE 122 (122), MICROHOUSE 124 (124) |
| IDM / experimental | GLITCH HOP 110 (110), IDM 120 (120), SKWEEE 100 (100), DECONSTRUCTED CLUB 130 (130) |
| Latin / Caribbean | SON 95 (95), RUMBA GUAGUANCO 100 (100), BOLERO 80 (80), MERENGUE 130 (130), MAMBO 190 (190), CHA-CHA-CHA 120 (120), KOMPA 120 (120), SALSA 180 (180), BACHATA 130 (130) |
| Phonk | PHONK 130 (130), DRIFT PHONK 155 (155), BRAZILIAN PHONK 130 (130) |
| Psytrance | GOA TRANCE 145 (145), FULL-ON 145 (145), PROGRESSIVE PSY 138 (138), DARK PSY 150 (150), FOREST PSY 150 (150), PSYCORE 190 (190), ZENONESQUE 135 (135), MINIMAL PSY 140 (140), HI-TECH 180 (180), NITZHONOT 150 (150), SUOMISAUNDI 150 (150), PSYBREAKS 135 (135), PSYDUB 100 (100), PSYBIENT 100 (100) |
| R&B / trap | RB (90), WCOAST R&B 110 (110), VAPORTRAP (70), TRAP 140 (140), UK DRILL 142 (142) |
| Rave / oldskool | RAVE 91 130 (130), HARDCORE TECHNO 145 (145), BREAKBEAT HARDCORE 145 (145), DARKCORE 155 (155) |
| Reggae / dancehall | SKA 120 (120), ROCKSTEADY 80 (80), ROOTS REGGAE 75 (75), DUB 70 (70), ROCKERS 80 (80), STEPPERS 75 (75), TWO TONE 160 (160), DIGITAL DANCEHALL 95 (95), 101 DANCEHALL (95), MODERN DANCEHALL 100 (100) |
| Reggaeton / funk carioca | 101 RAGATON (95), 101 FUNK FAVELA (130), DEMBOW 120 (120), FUNK DE RAIZ 130 (130) |
| South America | CANDOMBE 110 (110), TANGO 64 (64), MILONGA 90 (90), CHACARERA 70 (70), HUAYNO 90 (90) |
| Synth / disco | DISCO 118 (118), ITALO DISCO 120 (120), BOOGIE 110 (110), MOTORIK 120 (120) |
| Techno | DETROIT TECHNO 128 (128), BLEEP TECHNO 122 (122), AMBIENT TECHNO 120 (120), UK TECHNO 135 (135), MINIMAL TECHNO 126 (126), DUB TECHNO 118 (118), HARDGROOVE 135 (135), TRIBAL TECHNO 130 (130), ACID TECHNO 140 (140), SCHRANZ 150 (150), SCHAFFEL 125 (125), DEEP TECHNO 124 (124), HYPNOTIC TECHNO 130 (130), PEAK TIME TECHNO 132 (132), INDUSTRIAL TECHNO 140 (140), HARD TECHNO 145 (145), techAXX (130), TekkBooooring (130), TekkChungo (130), TekkThump (130) |
| UK garage | garage_2step (132), Two-stepppo (132), SPEED GARAGE 135 (135), BASSLINE 138 (138), GRIME140 (140), Grimer140 (140), DUBSTEP140 (140), DubSteppo (140), 101 STEPPA (140), RIDDIM 140 (140), uk_fungui (130), FUTURE GARAGE 130 (130), garage_uk_4x4 (132), uk_garbage (132), BREAKSTEP 140 (140), WONKY 140 (140) |
| World folk | HUAPANGO 110 (110), SON JAROCHO 120 (120), FREYLEKHS 130 (130), BHANGRA 95 (95), KEHERWA 100 (100) |
| Other | 101 SPARSE (120), BELLY DANCE (100), ZZZ BLACK (120) |

Ternary styles (MUINEIRA, JOTA ARAGONESA, SARDANA, TAJARASTE, BULERIA, SOLEA, SEGUIRIYA, SEVILLANA, FANDANGO DE HUELVA, BLUES SHUFFLE 100, WESTERN SWING 170, COUNTRY SHUFFLE 120, JIG 115, CHACARERA 70, HUAPANGO 110, SON JAROCHO 120, BHANGRA 95) are written as triplets and **need the global swing at 67**; with swing 50 they sound distorted. Their BPM is the plugin's: one quarter note = one dotted quarter (6/8), one 3/4 bar, three flamenco compás beats, or one shuffled quarter note.

This table also sets the families on the fingerprints page, so keep its format.

## Contributing

GenderBender is free software and contributions are welcome: new styles, bug fixes, ideas. Open an [issue](https://github.com/TOAST3R/genderbender/issues) to report a problem or suggest something, or fork the repo and send a pull request. For a new style, include its `.style` source and make sure `tools/check_styles.py` prints `ok`.

Bigger changes go through [OpenSpec](https://github.com/Fission-AI/OpenSpec) (`npm install -g @fission-ai/openspec@1.3.1`, then `/opsx:propose`, `/opsx:apply`, `/opsx:archive`). AI agents: read `AGENTS.md`.

## License

Original version by Sergio Millán. Released under the [GNU GPL v3](LICENSE): you can use, study, modify and share it, and modified versions you distribute must stay under the GPL.
