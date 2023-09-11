import pickle

import pika
from faker import Faker

from connection.connect import connect
from models.models import Contact


def generate_contacts_to_db(count: int, email: str = None) -> None:
    """Generate fake contacts to the database
    :param count: number of contacts to generate
    :param email: email to use for the contacts
    :return: None
    """
    fake = Faker()
    for _ in range(count):
        contact = Contact(
            fullname=fake.name(),
            email=email or fake.email(),
            address=fake.address(),
            phone=fake.phone_number(),
            delivery_preference=fake.random_element(['sms', 'email']),
        )
        contact.save()


def producer() -> None:
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='contacts_topic', exchange_type='topic')

    channel.queue_declare(queue='email_queue', durable=True)
    channel.queue_bind(exchange='contacts_topic', queue='email_queue', routing_key='email')
    channel.queue_declare(queue='sms_queue', durable=True)
    channel.queue_bind(exchange='contacts_topic', queue='sms_queue', routing_key='sms')
    
    generate_contacts_to_db(20)
    contacts = Contact.objects.all()
    
    for contact in contacts:
        message = pickle.dumps(contact.id)
        routing_key = contact.delivery_preference
        
        channel.basic_publish(
            exchange='contacts_topic',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f" [x] Sent contact`s '{contact.fullname}' id '{contact.id}'")
    
    connection.close()

if __name__ == '__main__':
    producer()
