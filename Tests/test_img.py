import pytest
from It1_interfaces.img import Img
import numpy as np
import tempfile
import cv2
import pathlib

def test_read_and_clone(tmp_path):
    img_path = tmp_path / "test.png"
    arr = np.zeros((10, 10, 3), dtype=np.uint8)
    cv2.imwrite(str(img_path), arr)
    img = Img().read(img_path)
    assert img.img.shape == (10, 10, 3)
    clone = img.clone()
    assert np.array_equal(img.img, clone.img)

def test_put_text(tmp_path):
    img_path = tmp_path / "test.png"
    arr = np.zeros((20, 20, 3), dtype=np.uint8)
    cv2.imwrite(str(img_path), arr)
    img = Img().read(img_path)
    img.put_text("hi", 5, 15, 0.5)
    assert img.img is not None