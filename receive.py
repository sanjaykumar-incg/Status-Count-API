import pika, sys
import pymongo
import json
from datetime import datetime


# Initialize MongoDB client and define database and collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")    
mydb = myclient["mqtt"]
mycol = mydb["status message"]


def insert_mongo(ch, method, properties, body):
    """
    Callback function to process and insert MQTT messages into MongoDB.
    """
    message = body.decode('utf-8')
    data = json.loads(message)
    data['timestamp'] = str(datetime.now())
    mycol.insert_one(data)
    print(f" [x] Received {body}")


def main():
    """
    Main function to establish RabbitMQ connection, declare a queue, 
    and start consuming messages.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=insert_mongo, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)