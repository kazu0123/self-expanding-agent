from pydantic import BaseModel, Field

class DateInfo(BaseModel):
  timezone: str = Field(description="取得したいタイムゾーン", examples=["JST", "UTC"])
