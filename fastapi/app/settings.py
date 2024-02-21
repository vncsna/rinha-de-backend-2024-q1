from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str = "user"
    postgres_pass: str = "pass"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "rinha"

    @property
    def postgres_dsn(self):
        return PostgresDsn(
            f"postgresql://{self.postgres_user}:{self.postgres_pass}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
