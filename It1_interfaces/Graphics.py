import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import copy
from It1_interfaces.img import Img
from It1_interfaces.Command import Command



class Graphics:
    def __init__(self,
                 sprites_folder: pathlib.Path,
                 cell_size: tuple[int, int],        # NEW
                 loop: bool = True,
                 fps: float = 6.0):
        """Initialize graphics with sprites folder, cell size, loop setting, and FPS."""
        self.sprites_folder = sprites_folder #תיקית התמונות של האנימציה
        self.cell_size = cell_size  #גודל התא בלוח
        self.loop = loop #האם האנימציה חוזרת בלולאה
        self.fps = fps #קצב רענון האנימציה
        self.sprites: Dict[str, Img] = {} #מילון של התמונות
        self.current_frame: Optional[Img] = None #התמונה הנוכחית של האנימציה
        self.frames: List[Img] = []
        self.current_frame_index: int = 0
        self.last_update_time: int = 0
        self.load_sprites()
       # self.reset(Command())
        self.current_frame = self.frames[0] if self.frames else None

    def load_sprites(self):
        """Load all sprite images from the sprites folder."""
        #print(f"Loading sprites from: {self.sprites_folder}")
        for img_path in self.sprites_folder.glob("*.png"):
            #print(f"Loading: {img_path}")
            img = Img().read(img_path)
            self.sprites[img_path.stem] = img
            self.frames.append(img)
        #print(f"Loaded {len(self.frames)} frames.")

    def copy(self):
        """Create a shallow copy of the graphics object."""
        new_graphics = copy.copy(self)
        new_graphics.frames = copy.copy(self.frames)
        new_graphics.current_frame = copy.copy(self.current_frame)
        return new_graphics

    def reset(self, cmd=None):
        if cmd is None:
           cmd = Command(timestamp=int(time.time() * 1000), piece_id="", type="idle", params=[])
        """Reset the animation with a new command."""
        pass

    def update(self, now_ms: int):
        """Advance animation frame based on game-loop time, not wall time."""
        pass

    def get_img(self) -> Img:
        """Get the current frame image."""
        if self.current_frame is None:
            raise ValueError("No current frame set in graphics.")
        return copy.copy(self.current_frame)