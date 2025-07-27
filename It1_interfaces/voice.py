# voice.py
from pathlib import Path
from threading import Thread
from playsound import playsound      # התקני:  pip install playsound==1.3
from bus import subscribe
SOUNDS_DIR = Path(__file__).parent / "sounds"   # <root>/sounds/*.wav
def _play_async(path: Path):
    """נגן בקובץ WAV/MP3 ב‑Thread נפרד כדי לא לחסום את הלולאה."""
    if path.exists():
        Thread(target=playsound, args=(str(path),), daemon=True).start()
class VoiceSFX:
    """
    מאזין ל‑piece_moved  ו‑piece_captured ומשמיע צלילים מתאימים.
    """
    def __init__(self):
        subscribe("piece_moved",    self._on_move)
        subscribe("piece_captured", self._on_capture)
    def _on_move(self, _):
        _play_async(SOUNDS_DIR / "move.mp3")
    def _on_capture(self, _):
        _play_async(SOUNDS_DIR / "capture.mp3")