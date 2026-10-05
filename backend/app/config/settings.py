from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Roaming Reconciliation Portal"
    app_env: str = "development"

    database_url: str
    ra_input_path: str = "./input/ra"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    admin_name: str
    admin_email: str
    admin_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()