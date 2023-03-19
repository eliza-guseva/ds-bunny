from typing import List, Dict
import json
import pika
from pathlib import Path

from src import rmq_queue as rq


"""
task_params is a list of dicts with the following keys
{
    "script_path": "str",
    "python_path": Optional["str"]=None,
    "args": Optional[Dict["str", Any]]=None,
}

"""

def send_tasks(task_params: List[Dict]):
    connection, channel, queue_name = rq.task_queue()
    for task in task_params:
        script_name = Path(task["script_path"]).name
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(task),
            mandatory=True,
            properties=pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f" [x] Sent task: {script_name}: {task['args']}")
    connection.close()


