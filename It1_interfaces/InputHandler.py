import cv2

class InputHandler:
    def __init__(self, board):
        self.board = board
        self.focus_a = [0, 0]  # שחקן א'
        self.focus_b = [7, 7]  # שחקן ב'
        self.stage_a = 0  # 0=בחירת כלי, 1=בחירת יעד
        self.stage_b = 0
        self.selected_a = None
        self.selected_b = None

    def handle_keyboard(self, key):
        print("key:", key)
        cmd = None
         # שחקן א' - אדום - ';lp בלבד
        if key == ord('l'):  # שמאלה
           self.focus_a[1] = max(0, self.focus_a[1] - 1)
        elif key == ord("'"):  # ימינה
           self.focus_a[1] = min(self.board.W_cells-1, self.focus_a[1] + 1)
        elif key == ord('p'):  # למעלה
           self.focus_a[0] = max(0, self.focus_a[0] - 1)
        elif key == ord(';'):  # למטה
           self.focus_a[0] = min(self.board.H_cells-1, self.focus_a[0] + 1)
        elif key == 13:  # Enter
            cmd = ("A", self.focus_a[:], self.stage_a)
            self.stage_a = (self.stage_a + 1) % 2

        # שחקן ב' - ירוק - asdw בלבד
        if key == ord('a'):  # שמאלה
            self.focus_b[1] = max(0, self.focus_b[1] - 1)
        elif key == ord('d'):  # ימינה
            self.focus_b[1] = min(self.board.W_cells-1, self.focus_b[1] + 1)
        elif key == ord('w'):  # למעלה
            self.focus_b[0] = max(0, self.focus_b[0] - 1)
        elif key == ord('s'):  # למטה
            self.focus_b[0] = min(self.board.H_cells-1, self.focus_b[0] + 1)
        elif key == 32:  # רווח
            cmd = ("B", self.focus_b[:], self.stage_b)
            self.stage_b = (self.stage_b + 1) % 2

        return cmd

    def draw_focus(self, img):
        cell_h, cell_w = self.board.cell_H_pix, self.board.cell_W_pix
        y, x = self.focus_a
        cv2.rectangle(img, (x*cell_w, y*cell_h), ((x+1)*cell_w-1, (y+1)*cell_h-1), (0,0,255), 8)
        # שחקן ב' - ריבוע ירוק עבה
        y, x = self.focus_b
        cv2.rectangle(
            img,
            (x * cell_w, y * cell_h),
            ((x + 1) * cell_w - 1, (y + 1) * cell_h - 1),
            (0, 255, 0), 8
        )