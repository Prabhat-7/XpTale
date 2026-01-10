from pydantic import BaseModel,Field


class ImageDuplicateOutput(BaseModel):
    is_duplicate: bool = Field(
        description="True if both images show the same scene/object captured at the same moment or same setup, even if angle, lighting, or crop differs."
    )
    confidence: float = Field(
        description="Confidence score between 0 and 1"
    )
    reason: str = Field(
        description="Brief explanation focusing on visual evidence"
    )

