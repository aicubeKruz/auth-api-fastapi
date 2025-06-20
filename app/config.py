from decouple import config

SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
API_KEY = config("API_KEY", default="dev-api-key")