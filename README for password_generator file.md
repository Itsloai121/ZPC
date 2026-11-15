# 🔐 ZPC Password Generator — Personal Guide

This guide explains the separate `password_generator.py` file in simple language. It is written for you as the developer, not as the repository's public README.

## 1. 🎯 What does this file do?

`password_generator.py` creates random passwords that are difficult to guess.

Every password it creates must contain all four character groups:

| Character group | Examples |
|---|---|
| Lowercase letters | `a b c ... z` |
| Uppercase letters | `A B C ... Z` |
| Numbers | `0 1 2 ... 9` |
| Symbols / special characters | `! @ # $ % ^ & *` and other punctuation |

The generator has these length rules:

- **Minimum:** 12 characters.
- **Default:** 20 characters, when you do not choose a length.
- **Maximum:** 256 characters.

The generator does not use names, birthdays, dictionary words, or patterns to build passwords. It chooses characters randomly.

## 2. 🧠 The Python logic, step by step

### Step 1 — Import the tools

The file imports:

- `secrets`: chooses random characters using Python's security-focused random source.
- `string`: provides the standard lowercase, uppercase, digit, and punctuation character sets.
- `argparse`: reads options when you run the file from a terminal.
- `sys`: returns the program's exit status.

No extra package needs to be installed.

### Step 2 — Define the character groups

The code creates four separate character collections:

```python
LOWERCASE_CHARACTERS = string.ascii_lowercase
UPPERCASE_CHARACTERS = string.ascii_uppercase
NUMBER_CHARACTERS = string.digits
SYMBOL_CHARACTERS = string.punctuation
```

It combines them into `ALL_CHARACTERS`. The resulting alphabet contains 94 ASCII characters.

### Step 3 — Validate the requested length

`_validate_length()` checks the requested length before generation starts.

- A value below 12 is rejected.
- A value above 256 is rejected.
- A value that is not an integer is rejected.

This prevents invalid input from reaching the generation logic.

### Step 4 — Generate a candidate password

`generate_password()` uses this logic:

```python
password = "".join(
    secrets.choice(ALL_CHARACTERS)
    for _ in range(length)
)
```

In simple language:

1. Choose one random character from the 94-character alphabet.
2. Repeat until the requested number of characters has been selected.
3. Join the selected characters into one password.

`secrets.choice()` is used instead of the ordinary `random` module because password generation needs a cryptographically secure random source.

### Step 5 — Check the four required groups

`_contains_all_character_groups()` checks whether the candidate contains:

1. At least one lowercase letter.
2. At least one uppercase letter.
3. At least one number.
4. At least one symbol.

If even one group is missing, the candidate is rejected and another candidate is generated. The program returns a password only after all four checks pass.

This method is called **rejection sampling**. It avoids putting a required symbol or number in a predictable position. It also means the output is uniformly selected from the valid passwords of the requested length.

### Step 6 — Return the result

`generate_password()` returns the password as a Python `str`.

It does not save the password to a file, send it to a server, or write it to a log. The caller decides what to do with the returned value.

## 3. 🧩 Main functions and what they do

| Function | Responsibility |
|---|---|
| `_validate_length(length)` | Checks the allowed password length. |
| `_contains_all_character_groups(password)` | Checks that all four required groups are present. |
| `generate_password(length=20)` | Generates and returns one password. |
| `generate_passwords(count=1, length=20)` | Generates multiple independent passwords. |
| `_build_argument_parser()` | Defines terminal options such as `--length` and `--count`. |
| `main(argv=None)` | Runs the terminal version of the generator. |

A name beginning with `_` is conventionally treated as an internal helper. You normally call `generate_password()` or `generate_passwords()` from another part of your application.

## 4. ▶️ How to run it

Open a terminal in the folder containing `password_generator.py`.

**Generate one password using the default length (20):**

```powershell
python password_generator.py
```

**Generate one password with 16 characters:**

```powershell
python password_generator.py --length 16
```

**Generate five passwords, each 24 characters long:**

```powershell
python password_generator.py --length 24 --count 5
```

**See the available options:**

```powershell
python password_generator.py --help
```

The same commands work with `python3` on many Linux and macOS systems.

## 5. 🔌 How to use it from another Python file

Because the generator is a separate module, another Python file can import its function.

```python
from password_generator import generate_password

new_password = generate_password(20)
print(new_password)
```

Or generate a list:

```python
from password_generator import generate_passwords

password_list = generate_passwords(count=3, length=24)
for password in password_list:
    print(password)
```

Keep `password_generator.py` in the same directory as the Python file that imports it, or make sure its folder is available on Python's import path.

## 6. 🌐 How this relates to your current ZPC project

Your current project has a Flask backend in `app.py`. It imports the password checker and exposes `/api/analyze` for checking a password. The new file is a separate generator engine; it does **not** automatically add a generator button to the website or create a Flask route.

To connect it to Flask later, the backend can import the function:

```python
from password_generator import generate_password
```

A future API route could call `generate_password(length)` and return the result as JSON. The website would also need a generator input/button and JavaScript to call that route. Keep the generated password out of server logs, analytics, and error messages.

The generator can be tested and used independently before you connect it to the web interface.

## 7. 🛡️ Security notes you should understand

- **No password is literally impossible to break.** A long, securely random password can make brute-force guessing computationally impractical, but no software can promise absolute invulnerability.
- A 12-character password is the minimum requested here, not the strongest option. The default is 20 characters; longer passwords generally provide a larger search space.
- The program uses `secrets`, not `random`, because `secrets` is designed for security-sensitive values.
- Use a different generated password for every account.
- Save passwords in a reputable password manager. Do not reuse them or send them in chat messages.
- Turn on multi-factor authentication where possible. Password strength cannot protect an account from phishing, malware, or a compromised service.
- Some websites reject certain punctuation characters. This generator includes Python's standard ASCII punctuation set, so a website with a restricted symbol policy may reject a generated password.
- The generator does not check whether an output password has appeared in a data breach. It creates random passwords; it is not a breach-checking service.

## 8. ✅ Quick checklist

- [x] Uses Python's standard library only.
- [x] Uses cryptographically secure randomness through `secrets`.
- [x] Enforces a 12-character minimum.
- [x] Includes lowercase letters, uppercase letters, numbers, and symbols in every result.
- [x] Allows a default length of 20 characters.
- [x] Supports generating multiple passwords.
- [x] Rejects invalid lengths and counts.
- [x] Does not write generated passwords to files or send them over the network.
- [ ] Does not yet add a generator screen or API endpoint to the ZPC website; that is a separate integration step.

---

**File purpose:** `password_generator.py` is the password-generation engine. This README is your learning and integration guide for that file.
