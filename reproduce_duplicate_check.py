import cv2
import numpy as np
import os
from image_filter.image_filter import Filter
from image_filter.config import Config

def create_dummy_image(filename, width, height, color=(100, 100, 100)):
    # Create a simple image with some structure (random noise + geometric shape)
    img = np.zeros((height, width, 3), np.uint8)
    img[:] = color
    # Add a rectangle
    cv2.rectangle(img, (width//4, height//4), (3*width//4, 3*height//4), (200, 200, 200), -1)
    cv2.imwrite(filename, img)
    return img

def test_different_sizes():
    Config.DUPLICATE_SSIM_THRESHOLD = 0.9 # Ensure threshold is set

    img1_path = "test_img1.png"
    img2_path = "test_img2.png"

    # Create original image
    create_dummy_image(img1_path, 800, 600)

    # Create resized version (half size) - this essentially is the "same" image content but smaller
    img1 = cv2.imread(img1_path)
    img2 = cv2.resize(img1, (400, 300))
    cv2.imwrite(img2_path, img2)

    print(f"Testing with {img1_path} (800x600) and {img2_path} (400x300)")

    try:
        is_dup = Filter.is_duplicate(img1_path, img2_path)
        print(f"Is duplicate: {is_dup}")
        
        if is_dup:
            print("SUCCESS: Detected duplicate despite size difference.")
        else:
            print("FAILURE: Did not detect duplicate.")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if os.path.exists(img1_path):
            os.remove(img1_path)
        if os.path.exists(img2_path):
            os.remove(img2_path)

if __name__ == "__main__":
    test_different_sizes()
