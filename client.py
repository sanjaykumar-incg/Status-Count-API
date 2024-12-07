import time
import random
import pika
import json


def main():
    """
    Main function to simulate an MQTT client that publishes random status messages to RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="mongo")
    try:
        while True:
            status = random.randint(0, 6)
            message = {"status": status}
            channel.basic_publish(exchange="", routing_key="mongo", body=json.dumps(message))
            print(f"Published: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping client...")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
