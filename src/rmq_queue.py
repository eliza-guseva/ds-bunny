from typing import Tuple, Optional
import pika
from config import (
    QUEUE_NAME, QUEUE_LIMIT,
)



def task_queue():
    # publisher confirms
    """Connect to the queue."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='', exchange_type='direct', durable=True)
    channel.queue_declare(
        queue=QUEUE_NAME, 
        durable=True,
        arguments={"x-max-priority": 10, 
                   'x-max-length': QUEUE_LIMIT, 
                   'x-overflow': 'reject-publish'}
        )
    channel.confirm_delivery()
    return connection, channel, QUEUE_NAME


def bind_client_to_queue(
    channel: pika.adapters.blocking_connection.BlockingChannel, 
    ):
    channel.queue_bind(
        exchange='', 
        queue=QUEUE_NAME,
        )