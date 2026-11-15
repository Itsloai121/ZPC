# 🟣 ZPC — Zynx Password Checker

**ZPC is a local-first password analysis and generation toolkit.** It helps you understand the basic strength of a password, see which patterns make it easier to guess, estimate how long a theoretical guessing attack might take, and create a new random password.

ZPC brings the original Python terminal checker into a larger application with a browser interface, a desktop interface, a terminal interface, and a password generator. The analysis and generation logic run on your own computer; the browser interface communicates with a local Flask server.

> [!IMPORTANT]
> **Use disposable test values when checking an existing password. Do not type a password that protects a real account.** ZPC is an educational tool, not a breach checker, password-cracking program, or replacement for a password manager or an organization's security policy. Scores, entropy, and crack-time figures are estimates—not guarantees.

## Contents

- [01 · Introduction](#01--introduction)
- [02 · Installation, Usage & Safe Running](#02--installation-usage--safe-running)
- [03 · Deep-Dive: How It Works](#03--deep-dive-how-it-works)
- [04 · Security, Scope & Metadata](#04--security-scope--metadata)

---

# 01 · Introduction

## What is ZPC?

ZPC stands for **Zynx Password Checker**. It is a Python project for learning about password strength, predictable password choices, entropy, and password-guessing scenarios.

The project has two related jobs:

1. **Check a test password.** ZPC examines its length, character types, common words, and simple patterns. It then produces a score, a strength grade, recommendations, an entropy estimate, and illustrative crack-time estimates.
2. **Generate a new password.** The web interface can create a random password using selected character types. The generator uses Python's `secrets` module and shows an analysis of the generated result.

## Main features

- **Three ways to use the checker:** a browser-based interface, a Tkinter desktop GUI, and a Rich terminal interface (TUI).
- **Password analysis:** length, lowercase and uppercase letters, numbers, symbols, whitespace, common-password matches, dictionary words, and simple predictable patterns.
- **Readable results:** a 0–100 educational score, a strength grade, entropy, character-pool information, findings, and recommendations.
- **Crack-time examples:** separate illustrative online and offline guessing scenarios, each with a stated assumed speed.
- **Password generation:** choose a length and enable or disable character groups, then view the generated password and its strength report.
- **Local Flask backend:** the browser UI sends analysis and generation requests to the Flask service running on your own computer.
- **Input limits and validation:** the checker rejects invalid input and limits analyzed passwords to 1,024 characters.
- **Built-in tests:** the checker includes a self-test command for important analysis and input-validation cases.
- **Custom visual style:** a black-dominant background, purple gradients, white accents, animated loading feedback, and organized result panels.

## How the project evolved

The repository keeps the original terminal implementation as a reference and builds on it.

| Original version | Updated project |
|---|---|
| `first project.py` identifies itself as version `1.0.0`. | `zynx_password_checker.py` identifies the checker as version `2.0.0`. |
| A Rich-based terminal application. | The Rich TUI remains available, and a Tkinter desktop GUI has been added. |
| Password analysis is started and viewed in the terminal. | You can also use the browser interface, which displays the report in a visual layout. |
| Focused on checking a password. | The browser interface also includes a password-generation workflow. |
| No Flask web application in the original script. | `app.py` provides local web routes for the page, analysis, password generation, and the Windows TUI hand-off. |

The analysis engine remains in Python. The newer interfaces call or present the analysis rather than replacing the core idea of the original project.

---

# 02 · Installation, Usage & Safe Running

## Requirements

- **Python 3.10 or newer**
- **Flask 3.x** for the browser application
- **Rich 13.x or 14.x** for the terminal interface
- **Tkinter** for the standalone desktop GUI. It is commonly included with Python, but some Linux distributions package it separately.
- A modern web browser for the browser interface

The exact Python package ranges are listed in `requirements.txt`:

```text
Flask >= 3.0, < 4
Rich  >= 13.7, < 15
```

The password-generation module uses Python's standard library and does not need another third-party package.

## 1. Download the project

Clone the repository and enter its folder:

```bash
git clone https://github.com/Itsloai121/ZPC.git
cd ZPC
```

Or download the repository as a ZIP file from GitHub and extract it.

## 2. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other Python projects:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

## 3. Install the dependencies

Run this command from the repository folder:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Start the browser application

The browser application is the main way to use the web interface and its password generator:

```bash
python app.py
```

When the server starts, open this address in your browser:

```text
http://127.0.0.1:5000
```

The first screen lets you choose an interface:

- **GUI:** stay in the browser and use the visual password checker.
- **TUI:** ask the local application to open the Rich terminal checker. The automatic browser-to-PowerShell hand-off is supported on Windows. On Linux and macOS, start the TUI from a terminal using the command below.

To stop the Flask server, return to the terminal and press `Ctrl+C`.

### Check a test password in the browser

1. Start the application with `python app.py`.
2. Open `http://127.0.0.1:5000`.
3. Choose **GUI**.
4. Enter a temporary test value in the masked input field.
5. Select **Enter** and review the report.
6. Use **Check another** to clear the input and test another value.

### Generate a new password in the browser

1. Open the browser application.
2. Choose the password-generation screen using **Checker**.
3. Select the character groups you want to include.
4. Choose a length. The browser control allows up to 64 characters and prevents generation below 12 characters.
5. Select **Generate**.
6. Review the generated password, its strength profile, character composition, and estimated crack times. Use **Copy** only when you are ready to place it in a trusted password manager.

The generator module itself validates lengths from 12 to 128 characters. The browser control currently exposes a smaller range.

## 5. Start the standalone desktop GUI or TUI

You can run the Python checker without starting Flask.

Open the interface chooser:

```bash
python zynx_password_checker.py
```

Open the desktop GUI directly:

```bash
python zynx_password_checker.py --gui
```

Open the terminal interface directly:

```bash
python zynx_password_checker.py --tui
```

The desktop GUI requires Tkinter. The TUI uses Rich and asks for the password with hidden terminal input. If the terminal cannot hide the input safely, the TUI stops rather than falling back to visible password entry.

## 6. Run the built-in checks

Run the checker's built-in unit tests:

```bash
python zynx_password_checker.py --self-test
```

Display the checker version:

```bash
python zynx_password_checker.py --version
```

Show the available command-line options:

```bash
python zynx_password_checker.py --help
```

## Safe-running checklist

- Run the Flask application locally and keep its address as `127.0.0.1`. Do not change it to `0.0.0.0` or expose the development server to your network or the public internet.
- Use a temporary example when testing an existing password. Never submit a password currently used for email, banking, university, social media, or another real account.
- Do not share screenshots that reveal a generated password or the results page containing it.
- Store a generated password in a reputable password manager. ZPC is not a password vault and does not provide account synchronization or recovery.
- Close the browser tab when you finish. The analysis input is cleared when you choose **Check another**; do not leave the page open on a shared or unattended computer.

---

# 03 · Deep-Dive: How It Works

## Application architecture

ZPC has separate interface, analysis, and generation parts:

```text
Browser
  |
  |  GET /
  v
Flask application (app.py)  <--- runs on 127.0.0.1:5000
  |
  +---- POST /api/analyze ----> zynx_password_checker.py
  |                              |-- validate input
  |                              |-- analyze password
  |                              |-- return report data
  |
  +---- POST /api/generate ---> password_generator.py
  |                              |-- generate with secrets
  |                              |-- analyze generated value
  |                              |-- return password + report
  |
  +---- POST /api/launch-tui -> Windows PowerShell hand-off

Standalone checker (zynx_password_checker.py)
  |-- Tkinter desktop GUI
  `-- Rich terminal interface
```

The browser page is stored in `templates/index.html`. The Flask application connects the browser to the Python analysis and password-generation modules.

## A. Password analysis process

### 1. Validate and measure the input

The checker expects a string and rejects values longer than **1,024 characters**. It measures the password as entered, including spaces; it does not remove spaces before calculating the length. Python's string length is used, so the measurement is based on Unicode code points.

### 2. Identify character categories

ZPC checks whether the password contains:

- Lowercase letters (`a–z`)
- Uppercase letters (`A–Z`)
- Digits (`0–9`)
- Symbols and punctuation
- Whitespace, such as spaces or tabs

The report shows which categories appear and uses them to estimate a possible character pool.

### 3. Check common passwords and dictionary words

The checker compares the input against a small built-in demonstration list of common passwords and words. It also applies Unicode normalization, case-insensitive comparison, and a limited set of common letter-to-number substitutions (often called *leetspeak*).

For example, changing a letter to a look-alike number does not automatically make a familiar word unpredictable. The checker reports a general match reason; it does not need to display the matched password text.

**Important:** this list is intentionally small. It is not connected to a live breach database and cannot tell you whether a password has appeared in a real data leak.

### 4. Detect simple patterns

ZPC checks for a few patterns that people commonly use and attackers can often guess early:

- The same character repeated three or more times in a row.
- Familiar keyboard patterns such as `qwerty` or `asdf`.
- Simple ascending or descending four-character sequences, such as `abcd` or `4321`.

These checks are basic warnings, not a complete password-pattern detector.

### 5. Estimate structural entropy

The checker uses this model:

```text
H = L × log2(N)
```

Where:

- `H` is the estimated entropy, measured in bits.
- `L` is the password length.
- `N` is the estimated number of possible characters in the pool.

For example, if a password has 10 characters and the estimated pool contains 62 possible characters:

```text
H = 10 × log2(62)
H ≈ 59.54 bits
```

This is a theoretical estimate. It assumes that every character is selected independently and uniformly at random from the full pool. Human-created passwords often contain habits, words, dates, or patterns, so their real guess resistance can be much lower. Unicode character groups use a rough estimate rather than a precise count, which makes Unicode results less exact.

### 6. Estimate crack time

ZPC estimates the median number of guesses as:

```text
Expected guesses ≈ 2^(H - 1)
Estimated time   = Expected guesses / guesses per second
```

The checker compares two example scenarios:

| Scenario | Assumed rate in the checker |
|---|---:|
| Online / rate-limited guessing | 10 guesses per second |
| Offline / fast unsalted-hash example | 1,000,000,000 guesses per second |

These are fixed demonstration assumptions, not measurements of a real attack. Real speeds depend on the service's rate limits, password-hashing algorithm and settings, hardware, salts, and attack method. The estimates do not predict how long a real account would remain safe.

### 7. Calculate the educational score

The checker produces a score from **0 to 100** and one of these labels:

- `VERY WEAK`
- `WEAK`
- `FAIR`
- `STRONG`
- `VERY STRONG`

The score is a transparent rule-based teaching aid. It gives weight to password length and character variety, then reduces the result for common-password matches and obvious patterns. A common-password or dictionary-word match forces the score to remain low.

It is not a recognized security certification or a formal password-policy standard. A high score does not guarantee that a password is safe.

## B. Password-generation process

The generator is handled by `password_generator.py` and is connected to the browser through `POST /api/generate`.

1. The user selects a length and character options.
2. Lowercase letters are always included as the base character group. Uppercase letters, numbers, symbols, and additional special characters can be enabled or disabled.
3. The generator uses Python's `secrets` module to choose characters. It includes at least one character from each selected group, fills the remaining positions from the combined pool, and shuffles the result.
4. It checks for simple repeated-character runs and short ascending or descending sequences, retrying generation when it finds one.
5. The browser displays the generated password and an analysis report with a score, grade, character composition, strength profile, estimated crack times, and strong or weak points.

The generator's report uses its own illustrative assumptions. Its three example rates are 1,000 guesses per second for online guessing, 10 billion per second for a fast offline-hashing example, and 1 trillion per second for a high-speed cracking-rig example. Do not compare these figures directly with the checker's two scenarios as though they were measured on the same system.

## C. The interfaces

| Interface | Technology | What it does |
|---|---|---|
| Browser GUI | HTML, CSS, JavaScript, Flask | Password analysis, generated-password workflow, animated loading, visual reports, and charts. |
| Desktop GUI | Tkinter | A standalone desktop checker with a dark purple design, an animated analysis screen, and an organized report. |
| Terminal TUI | Rich and `getpass` | A keyboard-driven checker with hidden password input and a formatted terminal report. |

The browser TUI launcher starts PowerShell automatically only on Windows. The standalone `--tui` command can be used directly in a terminal on other operating systems.

---

# 04 · Security, Scope & Metadata

## Security and privacy model

- **Local analysis:** the browser sends the password to the local Flask endpoint at `/api/analyze`. The Python analysis code processes it on the same computer; it does not send the password to a remote password-analysis API.
- **Loopback binding:** `app.py` starts Flask on `127.0.0.1:5000`, with debug mode disabled. This keeps the application bound to the local machine by default. Keep that setting; do not expose the Flask development server to other devices or the internet.
- **No password database:** the project does not include a database or a password-history feature. The checker returns derived analysis information rather than storing a password in a project data file.
- **Hidden input:** the TUI uses `getpass` so the typed password is not echoed in the terminal. The desktop and browser interfaces use masked password fields.
- **Bounded input:** the analysis endpoint limits the password length to 1,024 characters, and the Flask app also limits request size.
- **Generator randomness:** the generator uses Python's `secrets` module for random selection. This is separate from the approximate strength calculations shown in the report.
- **Memory limitation:** Python strings are immutable. Removing a variable or clearing an input field does not guarantee that every copy of the original value is immediately erased from process memory.

### External font requests

The browser page includes Google Fonts references for its typography. A browser may contact `fonts.googleapis.com` and `fonts.gstatic.com` to download those fonts. These requests are for the interface fonts; the password-analysis request is sent to the local Flask server. System-font fallbacks are defined in the page for cases where the remote fonts are unavailable.

If your requirement is to make **no external browser requests at all**, remove the Google Fonts references from `templates/index.html` and use local fonts only.

## What ZPC does not do

ZPC is deliberately limited to education and local demonstrations. It does **not**:

- Check a password against live data breaches or a current online blocklist.
- Log in to websites or test a password against a real account.
- Crack, recover, or steal passwords.
- Model every password-guessing technique or attacker capability.
- Guarantee that a password is secure because it receives a high score or a long estimated crack time.
- Replace a password manager, multi-factor authentication, unique passwords, or secure password storage.

## Project structure

```text
ZPC/
├── app.py                       # Local Flask web application and API routes
├── zynx_password_checker.py     # Main checker: analysis, Tkinter GUI, Rich TUI, tests
├── password_generator.py        # Random password generation and generator analysis
├── templates/
│   └── index.html               # Browser interface
├── first project.py             # Original version 1.0.0 terminal implementation
├── requirements.txt             # Flask and Rich dependencies
├── README.md                    # Project documentation
├── design style.txt             # Original visual-design notes
├── bugs to fix.txt              # Original review checklist
└── how to run.txt               # Basic run instructions
```

## Technology

| Component | Technology |
|---|---|
| Main language | Python |
| Browser backend | Flask |
| Browser frontend | HTML, CSS, JavaScript |
| Desktop interface | Tkinter |
| Terminal interface | Rich, `getpass` |
| Password generation | Python `secrets`, `string` |
| Analysis and estimates | Python standard library (`math`, `re`, `string`, `unicodedata`, and related modules) |

## Metadata

| Field | Value |
|---|---|
| Project | ZPC — Zynx Password Checker |
| Repository | [Itsloai121/ZPC](https://github.com/Itsloai121/ZPC) |
| Main checker version | `2.0.0` (`python zynx_password_checker.py --version`) |
| Original checker version | `1.0.0` (`first project.py`) |
| Main language | Python |
| Runtime | Python 3.10+ |
| Package dependencies | Flask 3.x and Rich 13.7–14.x |
| Default local web address | `http://127.0.0.1:5000` |
| License | No license file is currently included in the repository. Check with the repository owner before redistributing or reusing the project. |

---

**Remember:** a long, unique password generated with secure randomness is generally a better starting point than a short password built from personal information. Use a reputable password manager, enable multi-factor authentication where possible, and treat every estimate in ZPC as an educational approximation.
