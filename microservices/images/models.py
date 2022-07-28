from pydantic.main import BaseModel


class UpdateObjImages(BaseModel):
    on_site: bool
