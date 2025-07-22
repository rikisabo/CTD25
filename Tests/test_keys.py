import cv2
import numpy as np

img = np.zeros((200, 200, 3), dtype=np.uint8)
cv2.imshow("Test", img)
while True:
    key = cv2.waitKey(0)
    print("key:", key)
    if key == 27:
        break
cv2.destroyAllWindows()