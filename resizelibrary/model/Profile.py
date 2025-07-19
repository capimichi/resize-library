from pydantic import BaseModel, Field
from typing import List

class Profile(BaseModel):
    folder: str = Field(
        ...,
        description="Path to the folder containing media files to be resized."
    )
    allowed_extensions: List[str] = Field(
        default=['mov', 'mp4', 'mkv', 'avi'],
        description="List of allowed file extensions"
    )
    video_encoding: str = Field(
        default='libx264',
        description="Video encoding format"
    )
    audio_encoding: str = Field(
        default='aac',
        description="Audio encoding format"
    )
    audio_bitrate: str = Field(
        default='128k',
        description="Audio bitrate"
    )
    speed_profile: str = Field(
        default='slow',
        description="Encoding speed profile"
    )
    video_profile: str = Field(
        default='yuv420p',
        description="Video profile"
    )
    max_height: int = Field(
        default=1080,
        description="Maximum height for resize"
    )
    crf: int = Field(
        default=22,
        description="CRF value for encoding"
    )
    output_format: str = Field(
        default='mkv',
        description="Output container format"
    )