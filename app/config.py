from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    RABBIT_URL: str = "amqp://guest:guest@localhost/"

    RABBIT_REQUEST_QUEUE: str = "pb.nalog.search.request"
    RABBIT_STATUS_QUEUE: str = "pb.nalog.search.status"

    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_TOPIC: str = "pb.nalog.search.response"


settings = Settings()