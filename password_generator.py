"""
password_generator.py - the brain of ZPC's generator side.

index.html sends the user's choices to POST /api/generate. This file builds the
password, then analyses it for the results page (score, charts, strong and weak points).

Run it on its own:   python password_generator.py   ->  http://127.0.0.1:8000
Or plug it into the server you already have (Flask example):

    from password_generator import handle_request

    @app.post("/api/generate")
    def generate():
        body, status = handle_request(request.get_json(silent=True))
        return jsonify(body), status
"""
import json
import math
import re
import secrets
import string
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

MIN_LENGTH, MAX_LENGTH = 12, 128

SETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "numbers": string.digits,
    "symbols": "@#$%&*+=?",
    "special": "!^~_-.,;:()[]{}<>|/",
}
NAMES = {"lower": "Lowercase letters", "upper": "Uppercase letters", "numbers": "Numbers",
         "symbols": "Symbols", "special": "Special characters"}
SPEEDS = (("Online, no limits", "1,000 guesses/s", 1e3),
          ("Offline, fast hashing", "10 billion guesses/s", 1e10),
          ("Offline, cracking rig", "1 trillion guesses/s", 1e12))


# ---------------------------------------------------------------- generating
def find_patterns(pw):
    """Return which weak patterns are in the password: 'repeated' and/or 'sequence'."""
    found = []
    if re.search(r"(.)\1\1", pw):
        found.append("repeated")
    low = pw.lower()
    for i in range(len(low) - 2):
        tri = low[i:i + 3]
        a, b, c = map(ord, tri)
        if tri.isalnum() and b - a == c - b and abs(b - a) == 1:
            found.append("sequence")
            break
    return found


def generate_password(length, symbols=True, special=True, uppercase=True, numbers=True):
    """Build a random password. Lowercase letters are always the base set."""
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError("Length must be a whole number.")
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH} characters.")
    kinds = ["lower"] + [k for k, on in (("upper", uppercase), ("numbers", numbers),
                                         ("symbols", symbols), ("special", special)) if on]
    pool = "".join(SETS[k] for k in kinds)
    rng = secrets.SystemRandom()
    for _ in range(200):  # redo the rare draw that lands on a repeat or an easy sequence
        chars = [secrets.choice(SETS[k]) for k in kinds]  # at least one of every chosen type
        chars += [secrets.choice(pool) for _ in range(length - len(kinds))]
        rng.shuffle(chars)
        pw = "".join(chars)
        if not find_patterns(pw):
            break
    return pw


# ----------------------------------------------------------------- analysing
def human_time(s):
    if s < 1:
        return "Instantly"
    for name, div in (("second", 60), ("minute", 60), ("hour", 24), ("day", 365)):
        if s < div:
            v = round(s)
            return f"{v} {name}{'' if v == 1 else 's'}"
        s /= div
    for limit, div, name in ((1e3, 1, "years"), (1e6, 1e3, "thousand years"),
                             (1e9, 1e6, "million years"), (1e12, 1e9, "billion years")):
        if s < limit:
            return f"{round(s / div)} {name}"
    return f"about {s:.2e} years"


def analyze(pw):
    """Score a password and explain it. Weak points are listed only when they are real."""
    n = len(pw)
    counts = {k: sum(c in chars for c in pw) for k, chars in SETS.items()}
    kinds = [k for k, v in counts.items() if v]
    pool = sum(len(SETS[k]) for k in kinds)
    bits = round(n * math.log2(pool), 1) if pool else 0.0
    score = min(100, round(bits / 1.2))
    grade = next(g for t, g in ((90, "A+"), (75, "A"), (60, "B"), (40, "C"), (20, "D"), (0, "F")) if score >= t)
    verdict = next(v for t, v in ((90, "Excellent"), (75, "Strong"), (60, "Good"), (40, "Fair"), (0, "Weak")) if score >= t)
    patterns = find_patterns(pw)

    crack = []
    for name, rate_label, rate in SPEEDS:
        secs = 2.0 ** min(bits - 1, 1000) / rate if bits > 0 else 0
        pct = max(2, min(100, round(math.log10(max(secs, 1)) / 19.5 * 100)))
        crack.append({"name": name, "rate": rate_label, "seconds": secs, "human": human_time(secs), "pct": pct})
    fast = crack[1]

    strong = []
    if n >= 20:
        strong.append(f"Very long at {n} characters. Length is the strongest defence against brute force.")
    elif n >= 16:
        strong.append(f"Long at {n} characters, which puts it well out of casual brute-force reach.")
    elif n >= MIN_LENGTH:
        strong.append(f"Meets the {MIN_LENGTH}-character minimum with {n} characters.")
    if len(kinds) >= 4:
        strong.append(f"Mixes {len(kinds)} of 5 character types, so an attacker has to cover {pool} possible characters per position.")
    if bits >= 80:
        strong.append(f"About {bits:.0f} bits of entropy, far more than a brute-force attack can realistically search.")
    if not patterns:
        strong.append("No repeated runs or easy sequences such as aaa or 123.")
    strong.append("Generated with Python's secrets module (cryptographically secure randomness), so there is no human habit to guess.")
    if fast["seconds"] >= 3.15e7:
        strong.append(f"Even at 10 billion guesses per second, cracking it would take {fast['human']}.")

    weak = []
    if n < MIN_LENGTH:
        weak.append(f"Only {n} characters. Aim for at least {MIN_LENGTH}.")
    elif n < 16:
        weak.append(f"Moderate length ({n} characters). 16 or more would add a large safety margin.")
    for k in SETS:
        if not counts[k]:
            weak.append(f"No {NAMES[k].lower()}, which keeps the pool {len(SETS[k])} characters smaller than it could be.")
    if "repeated" in patterns:
        weak.append("Contains the same character three or more times in a row.")
    if "sequence" in patterns:
        weak.append("Contains an easy sequence such as abc or 123.")
    if bits < 60:
        weak.append(f"Only about {bits:.0f} bits of entropy, which a determined offline attack could eventually reach.")

    names = [NAMES[k].lower() for k in kinds]
    mix = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    summary = (f"Your {n}-character password scored {score}/100 (grade {grade}, {verdict.lower()}). "
               f"It uses {mix} and carries about {bits:.0f} bits of entropy. "
               f"At 10 billion guesses per second, an attacker would need {fast['human']} on average. "
               + (f"The main thing to improve: {weak[0][0].lower() + weak[0][1:]}" if weak
                  else "No real weak points were found."))

    return {
        "score": score, "grade": grade, "verdict": verdict, "entropy_bits": bits, "length": n, "pool_size": pool,
        "summary": summary, "strong": strong, "weak": weak, "crack": crack,
        "composition": [{"name": NAMES[k], "count": counts[k], "pct": round(counts[k] / n * 100) if n else 0} for k in SETS],
        "radar": [
            {"name": "Length", "value": min(100, round(n / 20 * 100))},
            {"name": "Variety", "value": round(len(kinds) / 5 * 100)},
            {"name": "Entropy", "value": min(100, round(bits / 120 * 100))},
            {"name": "Uniqueness", "value": round(len(set(pw)) / n * 100) if n else 0},
            {"name": "Pattern-free", "value": max(0, 100 - 35 * len(patterns))},
        ],
    }


# ------------------------------------------------------------ request handler
def handle_request(payload):
    """payload: {length, symbols, special, uppercase, numbers}  ->  (response dict, HTTP status)"""
    if not isinstance(payload, dict):
        return {"error": "Send a JSON object."}, 400
    try:
        pw = generate_password(payload.get("length"), bool(payload.get("symbols", True)),
                               bool(payload.get("special", True)), bool(payload.get("uppercase", True)),
                               bool(payload.get("numbers", True)))
    except ValueError as e:
        return {"error": str(e)}, 400
    return {"password": pw, "analysis": analyze(pw)}, 200


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, status=200, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        page = Path(__file__).with_name("index.html")
        if self.path.split("?")[0] in ("/", "/index.html") and page.exists():
            self._send(page.read_bytes(), 200, "text/html; charset=utf-8")
        else:
            self._send({"error": "Not found."}, 404)

    def do_POST(self):
        if self.path != "/api/generate":
            return self._send({"error": "Not found."}, 404)
        try:
            size = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(min(size, 4096)) or b"{}")
        except ValueError:
            payload = None
        body, status = handle_request(payload)
        self._send(body, status)

    def log_message(self, *args):  # never log requests: the responses hold passwords
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"ZPC generator running at http://127.0.0.1:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()