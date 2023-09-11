import pickle
import time

import pika
from faker import Faker

from connection.connect import connect
from models.models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='sms_queue', durable=True)
print(' [*] Waiting for contact`s id. To exit press CTRL+C')

def callback(ch, method, properties, body) -> None:

    contact_id = pickle.loads(body)
    contact = Contact.objects(id=contact_id).first()
    
    # Send random email message
    fake = Faker()
    email_message = fake.text()
    print(f" [x] Sending SMS to {contact.phone}: {email_message}")
    time.sleep(2)
    
    # Update contact's is_delivered attribute to True
    contact.is_delivered = True
    contact.save()
    print(f" [x] SMS was sent to {contact.phone}")
    # каже, щоб RabbitMQ не надсилав нове повідомлення для працівника доти, 
    # доки він не обробить і не підтвердить обробку попереднього повідомлення. 
    # Натомість він відправить його наступному працівникові, який ще не зайнятий.
    # ch.basic_ack(delivery_tag=method.delivery_tag)
    

# відповідає за відправлення відповідного підтвердження від працівника, 
# як тільки виконання завдання завершиться.
channel.basic_qos(prefetch_count=1)  
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)


if __name__ == '__main__':
    channel.start_consuming()