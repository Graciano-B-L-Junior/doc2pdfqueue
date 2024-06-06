import pika
import os

def init_rabbitmq():
    try:
        credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_DEFAULT_USER'),os.environ.get('RABBITMQ_DEFAULT_PASS'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get('RABBITMQ_SERVICE'),
                credentials=credentials
                )
            )

        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                            routing_key='hello',
                            body='Hello World!')
        print(" [x] Sent 'Hello World!'")
        connection.close()
    except Exception as err:
        print(err)