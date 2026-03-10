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
wts --dry-run profile opacity "Ubuntu" 80
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
wts profile list                                         # List all profiles
wts profile show "Ubuntu"                                # Show a profile's settings
wts profile add "MyProfile" --commandline "zsh"          # Add a profile
wts profile add "MyProfile" --commandline "zsh" \
  --starting-directory "~" --icon "🐧" --tab-title "Dev" --elevate
wts profile delete "MyProfile"                           # Delete (asks for confirmation)
wts profile delete "MyProfile" --force                   # Skip confirmation
```

#### Font

```bash
wts profile font "Ubuntu" --face "DroidSansM Nerd Font" --size 12 --weight bold
```

#### Cursor

```bash
wts profile cursor "Ubuntu" --shape bar --color "#ffffff"
wts profile cursor "Ubuntu" --shape vintage --height 25
```

Cursor shapes: `bar`, `doubleUnderscore`, `emptyBox`, `filledBox`, `underscore`, `vintage`.

#### Bell

```bash
wts profile bell "Ubuntu" --style audible
wts profile bell "Ubuntu" --style visual --sound "C:/sounds/bell.wav"
wts profile bell "Ubuntu" --disable
```

Bell styles: `audible`, `none`, `visual`, `window_title`.

#### Background image

```bash
wts profile background "Ubuntu" --image "C:/Users/you/Pictures/bg.png" --opacity 0.2
wts profile background "Ubuntu" --stretch uniformToFill --alignment center
wts profile background "Ubuntu" --clear
```

Stretch modes: `fill`, `none`, `uniform`, `uniformToFill`.
Alignments: `bottom`, `bottomLeft`, `bottomRight`, `center`, `left`, `right`, `top`, `topLeft`, `topRight`.

#### Opacity

```bash
wts profile opacity "Ubuntu" 80 --acrylic
wts profile opacity "Ubuntu" 100 --no-acrylic
```

#### Colors

```bash
wts profile colors "Ubuntu" --scheme "Dark+"
wts profile colors "Ubuntu" --foreground "#d4d4d4" --background "#1e1e1e"
wts profile colors "Ubuntu" --selection-bg "#264f78" --tab-color "#ff0000"
wts profile colors "Ubuntu" --intense-style bold --adjust-indistinguishable always
```

#### Window

```bash
wts profile window "Ubuntu" --padding "8"
wts profile window "Ubuntu" --scrollbar hidden
```

Scrollbar states: `always`, `hidden`, `visible`.

#### Advanced

```bash
wts profile advanced "Ubuntu" --history-size 9001
wts profile advanced "Ubuntu" --close-on-exit graceful
wts profile advanced "Ubuntu" --antialiasing cleartype
wts profile advanced "Ubuntu" --suppress-title --no-altgr-aliasing
wts profile advanced "Ubuntu" --auto-mark-prompts --show-marks
wts profile advanced "Ubuntu" --path-translation wsl
```

Close on exit modes: `always`, `graceful`, `never`.
Antialiasing modes: `aliased`, `cleartype`, `grayscale`.
Path translation styles: `cygwin`, `none`, `wsl`.

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
