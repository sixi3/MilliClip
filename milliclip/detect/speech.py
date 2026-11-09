"""Optional speech transcription via faster-whisper.

Degrades gracefully: if faster-whisper is not installed, returns empty results and the
pipeline continues using audio + scene signals only. When available, produces both:
  - word-level timings (for subtitles), and
  - 'speech' signals weighted by excitement cues (exclamations, keyword hits).
"""
from __future__ import annotations

from typing import List, Tuple

from ..models import Signal

# Words that often mark a hype/notable moment in gameplay commentary.
_EXCITEMENT = {
    "no", "wow", "what", "insane", "clutch", "won", "win", "kill", "dead", "died",
    "let's", "lets", "go", "oh", "yes", "nice", "crazy", "bro", "wtf", "huge",
}


def available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except Exception:
        return False


def transcribe(path: str, model: str = "base", language: str = "en"
               ) -> Tuple[str, List[dict]]:
    """Return (full_text, words) where words = [{word,start,end}]. Empty if unavailable."""
    if not available():
        return "", []
    from faster_whisper import WhisperModel  # type: ignore

    wm = WhisperModel(model, device="auto", compute_type="int8")
    segments, _ = wm.transcribe(path, language=language, word_timestamps=True)
    words: List[dict] = []
    texts: List[str] = []
    for seg in segments:
        texts.append(seg.text.strip())
        for w in (seg.words or []):
            words.append({"word": w.word.strip(), "start": float(w.start),
                          "end": float(w.end)})
    return " ".join(texts).strip(), words


def speech_signals(words: List[dict]) -> List[Signal]:
    """Derive 'speech' signals from excitement cues in word timings."""
    signals: List[Signal] = []
    for w in words:
        token = w["word"].lower().strip("!?.,")
        is_excl = w["word"].endswith("!")
        if token in _EXCITEMENT or is_excl:
            strength = 0.8 if is_excl else 0.6
            signals.append(Signal(kind="speech", start=float(w["start"]),
                                  end=float(w["end"]), strength=strength,
                                  note=w["word"]))
    return signals
