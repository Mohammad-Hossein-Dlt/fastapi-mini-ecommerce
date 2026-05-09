from src.infra.broker_config.app import app
from src.worker.consumer.nats.broker import client

app.set_broker(client.broker)