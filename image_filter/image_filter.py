import base64
from dotenv import load_dotenv
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.messages import HumanMessage

from .structured_outputs import ImageDuplicateOutput
from .prompts import DUPLICATE_PROMPT

load_dotenv()
class Filter:
    @staticmethod
    def encode_image(path: Path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    @staticmethod
    def get_mime(path: Path):
        ext = path.suffix.lower()
        if ext == ".png":
            return "image/png"
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        if ext == ".webp":
            return "image/webp"
        return "image/jpeg"
    @staticmethod
    def is_duplicate(img1_path, img2_path):
        llm =ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        ).with_structured_output(ImageDuplicateOutput)

        img1_path = Path(img1_path)
        img2_path = Path(img2_path)

        img1_b64 = Filter.encode_image(img1_path)
        img2_b64 = Filter.encode_image(img2_path)

        message = HumanMessage(content=[
            {"type": "text", "text": DUPLICATE_PROMPT},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{Filter.get_mime(img1_path)};base64,{img1_b64}"
                }
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{Filter.get_mime(img2_path)};base64,{img2_b64}"
                }
            }
        ])

        response = llm.invoke([message])
        return response
    
