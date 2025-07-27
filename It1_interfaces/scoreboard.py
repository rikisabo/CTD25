from collections import defaultdict
import cv2
from bus import subscribe

PIECE_VALUE = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}

class ScoreBoard:
    def __init__(self):
        self.score = defaultdict(int)          # {"A": 0, "B": 0}
        subscribe("piece_captured", self._update)

    # ←──── עדכון הניקוד (כבר תוקן קודם) ──────────────────────────────
    def _update(self, data):
        victim = data["victim"]
        kind_code = victim.piece_id.split("_")[0] if hasattr(victim, "piece_id") else victim.split("_")[0]
        kind  = kind_code[0]
        owner = victim.player if hasattr(victim, "player") else "?"
        self.score[owner] += PIECE_VALUE.get(kind, 0)

    # ←──── ציור הניקוד על‑גבי התמונה ─────────────────────────────────
    def draw(self, img, origin=(10, 30)):
        """
        מצייר "Player A: X" ו‑"Player B: Y" בפינה שמאלית‑עליון‎ת (ברירת‑מחדל).
        origin – קואורדינטה (x, y) של השורה הראשונה.
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale, thick = 0.8, 2

        a_text = f"Player A: {self.score['A']}"
        b_text = f"Player B: {self.score['B']}"

        x, y = origin
        cv2.putText(img, a_text, (x, y),             font, scale, (0, 0, 255), thick, cv2.LINE_AA)
        cv2.putText(img, b_text, (x, y + 30),        font, scale, (255, 0, 0), thick, cv2.LINE_AA)
