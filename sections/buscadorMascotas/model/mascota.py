from pydantic import BaseModel


class Mascota(BaseModel):
    number: int = 0
    name: str | None = ""
    image: str | None = ""
    raza: str | None = ""
    sex: str | None = ""
    age: str | None = ""
    comunidadAutonoma: str | None = ""
    protectora: str | None = ""
    link: str | None = ""
