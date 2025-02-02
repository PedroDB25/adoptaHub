from pydantic import BaseModel


class Protectora(BaseModel):
    number: int = 0
    name: str = ""
    phone: str | None = ""
    web: str | None = ""
    mailto: str | None = ""
    facebook: str | None = ""
    comunidad_autonoma: str = ""
    paginas: list | None = ""
    da_datos: int = 0
    logo: str | None = ""

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
