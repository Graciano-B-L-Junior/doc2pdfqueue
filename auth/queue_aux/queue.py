import pika
import os

def init_rabbitmq():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get('RABBITMQ_SERVICE'),
                )
            )

        channel = connection.channel()
        channel.queue_declare(queue='hello',durable=True)
        channel.basic_publish(exchange='',
                            routing_key='hello',
                            body='Hello World!',
                            properties=pika.BasicProperties(
                                delivery_mode=pika.DeliveryMode.Persistent
                            ))
        print(" [x] Sent 'Hello World!'")
        connection.close()
    except Exception as err:
        print(err)