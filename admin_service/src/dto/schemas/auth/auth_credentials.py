from src.infra.utils.custom_base_model import CustomBaseModel

class AuthCredentials(CustomBaseModel):
    access_token: str
    refresh_token: str
    token_type: str
            