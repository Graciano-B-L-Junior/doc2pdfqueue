import pika
import os
import time



def connect_rabbitmq():
    try:
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.environ.get('RABBITMQ_SERVICE'),
                    )
                )
        return connection
    except:
        return None

def send_doc_file(filename):
    try:
        with open(os.path.join('/app/files',filename), 'rb') as file:
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
            os.remove(os.path.join('/app/files',filename))
            return True
    except Exception as err:
        print(err)

    return False

def download_pdf_file():
    conn = connect_rabbitmq()
    channel = conn.channel()
    channel.queue_declare(queue='pdf_queue',durable=True)

    def callback(ch, method, properties, body):
        doc_name = "/app/files/file.pdf"
        with open(doc_name,'wb',) as file:
            file.write(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)



    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='pdf_queue', on_message_callback=callback,consumer_tag="tag")

    print(' [*] Waiting for pdf file. To exit press CTRL+C')
    channel.start_consuming()

    channel.close()
    conn.close()
