import base64
import cv2
import numpy as np
from pathlib import Path
from skimage.metrics import structural_similarity as ssim
import shutil
from langchain_ollama import ChatOllama
from .config import Config
from .structured_outputs import ImageFilterOutput
from langchain.messages import HumanMessage
from .prompts import SYSTEM_PROMPT, USER_PROMPT
# -----------------------------
# CHECK FUNCTIONS
# -----------------------------
class Filter:
    @staticmethod
    def is_eligible(img_path):
        llm = ChatOllama(model="gemma3:12b").with_structured_output(ImageFilterOutput)
        
        # Read and encode the image as base64
        image_path = Path(img_path)
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Determine the image MIME type
        mime_type = "image/jpeg"
        if image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        elif image_path.suffix.lower() in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif image_path.suffix.lower() in [".webp"]:
            mime_type = "image/webp"
        
        message = [
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": USER_PROMPT
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_data}"
                    }
                }
            ])
        ]
        
        response = llm.invoke(message)
        return response

    @staticmethod
    def is_duplicate(img1, img2):
        g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        score, _ = ssim(g1, g2, full=True)
        return score >Config.DUPLICATE_SSIM_THRESHOLD

    # -----------------------------
    # MAIN FUNCTION
    # -----------------------------
    @staticmethod
    def filter_frames(input_dir, output_dir):
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for img_path in sorted(input_dir.iterdir()):
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue

            img = cv2.imread(str(img_path))
            if img is None:
                continue

            if Filter.is_blurry(img):
                continue
            shutil.copy(img_path, output_dir / img_path.name)
            
     
              
