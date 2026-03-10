# wt-settings

A CLI to read and write [Windows Terminal](https://github.com/microsoft/terminal) `settings.json` directly — works on both **WSL** and **native Windows**.

## Installation

```bash
uv tool install wt-settings
```

Or from source:

```bash
git clone https://github.com/mirai-toto/wt-settings.git
cd wt-settings
uv tool install -e .
```

## Usage

The CLI is available as `wts`.

```bash
wts --help
```

### Global options

| Option | Description |
|--------|-------------|
| `--settings PATH` | Path to `settings.json`. Auto-discovered if not provided. |
| `--dry-run` | Print what would be written without modifying the file. |

```bash
wts --settings "C:/Users/you/AppData/Local/Packages/.../settings.json" profile list
wts --dry-run appearance opacity "Ubuntu" 80
```

---

### `wts path`

Print the resolved path to `settings.json`:

```bash
wts path
```

---

### Profiles

```bash
wts profile list                                        # List all profiles
wts profile show "Ubuntu"                               # Show a profile's settings
wts profile add "MyProfile" --commandline "zsh"         # Add a profile
wts profile add "MyProfile" --commandline "zsh" --guid "{...}"  # With explicit GUID
wts profile delete "MyProfile"                          # Delete (asks for confirmation)
wts profile delete "MyProfile" --force                  # Skip confirmation
```

---

### Appearance

```bash
# Font
wts appearance font "Ubuntu" --face "DroidSansM Nerd Font" --size 12

# Opacity & acrylic
wts appearance opacity "Ubuntu" 80 --acrylic
wts appearance opacity "Ubuntu" 100 --no-acrylic

# Background image
wts appearance background "Ubuntu" --image "C:/Users/you/Pictures/bg.png" --opacity 0.2
wts appearance background "Ubuntu" --image "C:/Users/you/Pictures/bg.png" --stretch uniformToFill
wts appearance background "Ubuntu" --clear
```

Stretch modes: `fill`, `none`, `uniform`, `uniformToFill`.

---

### Supported profile fields

All standard Windows Terminal profile fields are recognized and preserved. Use `wts profile show <name>` to inspect them.

| Category | Fields |
|---|---|
| **General** | `name`, `guid`, `source`, `commandline`, `startingDirectory`, `icon`, `tabTitle`, `hidden`, `elevate` |
| **Font** | `font.face`, `font.size`, `font.weight`, `font.features`, `font.axes` |
| **Cursor** | `cursorShape`, `cursorHeight`, `cursorColor` |
| **Colors** | `colorScheme`, `foreground`, `background`, `selectionBackground`, `tabColor`, `adjustIndistinguishableColors`, `intenseTextStyle` |
| **Background image** | `backgroundImage`, `backgroundImageOpacity`, `backgroundImageStretchMode`, `backgroundImageAlignment` |
| **Transparency** | `opacity`, `useAcrylic` |
| **Window** | `padding`, `scrollbarState`, `unfocusedAppearance` |
| **Advanced** | `suppressApplicationTitle`, `antialiasingMode`, `altGrAliasing`, `snapOnInput`, `historySize`, `closeOnExit`, `bellStyle`, `bellSound`, `autoMarkPrompts`, `showMarksOnScrollbar`, `pathTranslationStyle` |

---

### Color Schemes

```bash
wts scheme list                           # List all schemes
wts scheme show "Dark+"                   # Show a scheme's colors
wts scheme add ./my-scheme.json           # Add scheme from a JSON file
wts scheme delete "MyScheme"              # Delete (asks for confirmation)
wts scheme delete "MyScheme" --force      # Skip confirmation
wts scheme apply "Ubuntu" "Dark+"         # Apply a scheme to a profile
```

#### Scheme JSON format

```json
{
  "name": "MyScheme",
  "background": "#1E1E1E",
  "foreground": "#D4D4D4",
  "black": "#1E1E1E",
  "red": "#F44747",
  "green": "#6A9955",
  "yellow": "#D7BA7D",
  "blue": "#569CD6",
  "purple": "#C586C0",
  "cyan": "#4EC9B0",
  "white": "#D4D4D4",
  "brightBlack": "#808080",
  "brightRed": "#F44747",
  "brightGreen": "#6A9955",
  "brightYellow": "#D7BA7D",
  "brightBlue": "#569CD6",
  "brightPurple": "#C586C0",
  "brightCyan": "#4EC9B0",
  "brightWhite": "#FFFFFF"
}
```

## License

MIT
