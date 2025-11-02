from pydantic import BaseModel
class SettingOut(BaseModel):
    ui_theme: str
    notify_email: bool
class SettingUpdate(BaseModel):
    ui_theme: str | None = None
    notify_email: bool | None = None
