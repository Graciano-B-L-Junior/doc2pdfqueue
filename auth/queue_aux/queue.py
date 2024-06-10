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

def send_doc_file(filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.environ.get('RABBITMQ_SERVICE'),
                    )
                )
            
            channel = connection.channel()
            channel.queue_declare(queue='file',durable=True)
            channel.basic_publish(exchange='',
                                routing_key='file',
                                body=file_data,
                                properties=pika.BasicProperties(
                                    delivery_mode=pika.DeliveryMode.Persistent
                                ))
            connection.close()
            os.remove(filename)
            return True
    except Exception as err:
        print(err)

    return False