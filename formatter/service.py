import pika, sys, os
import time

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


def main():
    
    
    channel = connect_rabbitmq()
    channel.queue_declare(queue='hello',durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    channel.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)