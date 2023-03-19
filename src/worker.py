import json
from pathlib import Path
import subprocess

from src import rmq_queue as rq


def callback(channel, method, properties, body: bytes) -> None:
    """
    checks that all is good with the vpn
    then scrapes google maps
    """
    task = json.loads(body)
    script_name = Path(task["script_path"]).name
    print(f" [x] Received {script_name}: {task['args']}")
    call_script(task)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")  
    
def main(self) -> None:
    connection, channel, queue_name = rq.task_queue()
    rq.bind_client_to_queue(channel)
    channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=False)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
    
# HELPERS
def python(task):
    if task["python_path"] is None:
        return "python"
    else:
        return task["python_path"]
    
    
def script_folder(task):
    script_path = Path(task["script_path"])
    return script_path.parent


def call_script(task):
    """
    using subproccess cd into the script folder and run the script
    using specified python path, changes args into cmd agrs with --
    """
    subprocess.run(
        [
            "cd", script_folder(task) , "&&", 
            python(task), task["script_path"], 
            *("--" + (arg_key, arg_value) for (arg_key, arg_value) in task["args"].items())
        ]
    )


if __name__ == "__main__":
    main()
