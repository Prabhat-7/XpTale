from pydantic import BaseModel,Field

class ImageFilterOutput(BaseModel):
    keep:bool=Field(description="Whether to keep the image as a memory")
    quality_score: int = Field(description="A number from 1 to 10")
    issues: list[str] = Field(description="An array of short phrases describing issues")
    primary_reason: str = Field(description="One short sentence explaining the decision")


