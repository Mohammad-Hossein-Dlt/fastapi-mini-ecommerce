import jwt
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import InvalidTokenException
from datetime import datetime, timezone, timedelta

class JWTHandler:

    def __init__(
        self,
        secret,
        algorithm,
        jwt_expiration_minutes,
        jwt_refresh_expiration_minutes
    ):
        self.JWT_SECRET = secret
        self.JWT_ALGORITHM = algorithm
        self.jwt_expiration_minutes = jwt_expiration_minutes
        self.jwt_refresh_expiration_minutes = jwt_refresh_expiration_minutes
        
    
    def create_jwt_token(
        self,
        payload: JWTPayload,
    ) -> str:
        
        now = datetime.now(timezone.utc).replace(microsecond=0)
        
        if payload.type == "access":
            payload.exp = now + timedelta(minutes=self.jwt_expiration_minutes)
        elif payload.type == "refresh":
            payload.exp = now + timedelta(minutes=self.jwt_refresh_expiration_minutes)
        
        return jwt.encode(payload.model_dump(), self.JWT_SECRET, self.JWT_ALGORITHM)

    def decode_jwt_token(
        self,
        token: str,
    ) -> JWTPayload:
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
        except jwt.exceptions.PyJWTError as ex:            
            raise InvalidTokenException(status_code=401, message=str(ex))
        
        return JWTPayload.model_validate(payload)