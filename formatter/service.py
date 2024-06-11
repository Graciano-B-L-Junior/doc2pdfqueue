import pika, sys, os
import time
from spire.doc import *
from spire.doc.common import *

def connect_rabbitmq(retries=5, delay=2):
    attempt =0
    while attempt < retries:
        print("Init connection")
        try:
            connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_SERVICE'),
            )
        )
            channel = connection.channel()
            return channel
        except pika.exceptions.AMQPConnectionError:
            attempt+=1
            time.sleep(delay)
            delay*=2
            print("Connection failed, retrying...")
            sys.stdout.flush()
    raise Exception("Failed to connect to RabbitMQ after several retries")

def send_pdf_file_to_queue():
    try:
        channel = connect_rabbitmq()
        channel.queue_declare(queue='pdf_queue',durable=True)
        

        with open('file.pdf', 'rb') as file:
            file_data = file.read()
            channel.basic_publish(
            exchange='',
            routing_key='pdf_queue',
            body=file_data,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
            )

        channel.close()
        os.remove('file.pdf')
    except Exception as err:
        print(err)

def convert_file_from_queue():
    channel = connect_rabbitmq()
    channel.queue_declare(queue='file',durable=True)

    def callback(ch, method, properties, body):
        doc_name = "document.docx"
        with open(doc_name,'wb',) as file:
            file.write(body)

        document = Document()
        document.LoadFromFile(doc_name)
        document.SaveToFile("file.pdf", FileFormat.PDF)
        document.Close()
        os.remove(doc_name)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        send_pdf_file_to_queue()



    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='file', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    channel.close()


def main():
   convert_file_from_queue()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)