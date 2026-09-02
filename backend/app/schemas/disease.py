from pydantic import BaseModel, ConfigDict


class DiseaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str
    affected_part: str
    symptoms: tuple[str, ...]

