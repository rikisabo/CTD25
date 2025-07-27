from bus import subscribe
import time
import cv2

MAX_ROWS = 8          # כמה מהלכים אחרונים להציג לכל שחקן
ROW_H    = 22         # גובה שורה בפיקסלים

class MoveLog:
    """
    רושם כל תזוזה ומסוגל לצייר טבלה גרפית על‑גבי מסך המשחק.
    """

    def __init__(self):
        self.moves = {"A": [], "B": []}          # {"A": [(time, id), ...]}
        subscribe("piece_moved", self._record)

    # — event — --------------------------------------------------------------
    def _record(self, data):
        piece = data["piece"]
        now   = time.strftime("%H:%M:%S", time.localtime())
        self.moves[piece.player].append((now, piece.piece_id))

        # קצץ רשימות ארוכות
        for pl in ("A", "B"):
            self.moves[pl] = self.moves[pl][-MAX_ROWS:]

    # — draw — ---------------------------------------------------------------
    def draw(self, img, origin=(820, 40)):
        """
        מצייר שתי טבלאות (A,B) בצד ימין של הלוח.
        origin –  נקודת התחלה (x,y) של כותרת Player A.
        התאימי לפי גודל התמונה שלך.
        """
        font, scale, thick = cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        x0, y0 = origin

        for idx, player in enumerate(("A", "B")):
            # כותרת
            y = y0 + idx * (MAX_ROWS + 2) * ROW_H
            cv2.putText(img, f"Player {player}", (x0, y),
                        font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            y += ROW_H
            cv2.putText(img, "TIME       MOVE", (x0, y),
                        font, scale, (255, 255, 255), thick, cv2.LINE_AA)
            y += ROW_H

            # שורות
            for t, m in self.moves[player]:
                cv2.putText(img, f"{t}  {m}", (x0, y),
                            font, scale, (200, 200, 200), thick, cv2.LINE_AA)
                y += ROW_H
