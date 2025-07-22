import pathlib

from It1_interfaces.Graphics import Graphics


class GraphicsFactory:
    @staticmethod
    def create_graphics(sprites_folder: pathlib.Path, cell_size: tuple[int, int], loop: bool = True, fps: float = 6.0) -> Graphics:
        return Graphics(sprites_folder, cell_size, loop, fps)
    
    def load(self,
             sprites_dir: pathlib.Path,
             cfg: dict,
             cell_size: tuple[int, int]) -> Graphics:
        """Load graphics from sprites directory with configuration."""
        pass 