"""Per-video feature extraction. Language/script detection is heuristic."""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

SCRIPT_RANGES = {
    "devanagari": (0x0900, 0x097F),
    "bengali": (0x0980, 0x09FF),
    "malayalam": (0x0D00, 0x0D7F),
}

# Small romanized-Hindi wordlist. Deliberately excludes words that are common English
# (to, the, me, hi, in, of, ...). HEURISTIC: expect false positives/negatives.
HINGLISH_WORDS = frozenset("""
kya hai hain nahi nahin mat ke ki ka ko se mein par pe bhai yaar ye yeh wo woh aur bhi toh
kaise kyun kyu kaun kab kahan sabse bohot bahut mera meri mere tera teri apna apni aapka aap tum
tumhara hum karo kar kiya kiye karna dekho dekh ghar paisa pura poora sach jab tab agar lekin
magar abhi ab wala wali wale gaya gayi gaye raha rahi rahe tha thi hoga hogi kuch sab ek
""".split())

_EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕⌚⌛⏩-⏺←-⇿]")
_HASHTAG = re.compile(r"#[^\s#]+")
_WORD = re.compile(r"[A-Za-z']+")


def duration_bucket(seconds: int | None) -> str:
    if seconds is None:
        return "unknown"
    for limit, label in ((15, "0-15s"), (30, "16-30s"), (45, "31-45s"), (60, "46-60s"),
                         (180, "61-180s"), (600, "181-600s")):
        if seconds <= limit:
            return label
    return "601s+"


def detect_script(text: str) -> str:
    counts = {k: 0 for k in SCRIPT_RANGES}
    counts["latin"] = 0
    for ch in text:
        cp = ord(ch)
        for name, (lo, hi) in SCRIPT_RANGES.items():
            if lo <= cp <= hi and ch.isalpha():
                counts[name] += 1
                break
        else:
            if ch.isascii() and ch.isalpha():
                counts["latin"] += 1
    total = sum(counts.values())
    if total == 0:
        return "none"
    top, n = max(counts.items(), key=lambda kv: kv[1])
    if n / total < 0.8:
        return "mixed"
    return top


def hinglish_score(text: str) -> tuple[int, int]:
    words = [w.lower() for w in _WORD.findall(text)]
    return sum(w in HINGLISH_WORDS for w in words), len(words)


def detect_language(text: str, script: str | None = None) -> str:
    """HEURISTIC language guess from the title: script first; romanized Hindi via wordlist.

    Devanagari is reported as 'hindi' but may be Marathi/Nepali etc. Latin text is
    'hinglish' if >=2 wordlist hits or >=25% of words hit, else 'english'.
    """
    script = script or detect_script(text)
    if script == "devanagari":
        return "hindi"
    if script in ("bengali", "malayalam"):
        return script
    if script == "latin":
        hits, n = hinglish_score(text)
        return "hinglish" if hits >= 2 or (hits >= 1 and hits / n >= 0.25) else "english"
    if script == "mixed":
        return "mixed"
    return "unknown"


def extract_features(video: dict, shorts_max_seconds: int = 180) -> dict:
    title = video.get("title", "") or ""
    desc = video.get("description", "") or ""
    dur = video.get("duration_s")
    pub: datetime = video["published_at"]
    ist = pub.astimezone(IST)
    script = detect_script(title)
    return {
        "duration_bucket": duration_bucket(dur),
        "is_short_heuristic": dur is not None and 0 < dur <= shorts_max_seconds,
        "title_length": len(title),
        "title_script": script,
        "title_language_heuristic": detect_language(title, script),
        "hashtag_count": len(_HASHTAG.findall(title)) + len(_HASHTAG.findall(desc)),
        "title_has_question": "?" in title or "？" in title,
        "title_has_number": any(c.isdigit() for c in title),
        "title_has_emoji": bool(_EMOJI.search(title)),
        "publish_hour_ist": ist.hour,
        "publish_weekday_ist": ist.strftime("%a"),
    }
