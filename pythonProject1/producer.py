import json
from mongoengine import connect, Document, StringField, BooleanField
import pika
import faker
import connect


# Оголошення моделі для контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

# Генератор фейкових контактів
def generate_fake_contacts(num_contacts):
    fake = faker.Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        )
        contacts.append(contact)
    return contacts

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                               port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів
fake_contacts = generate_fake_contacts(5)

# Запис контактів у базу даних та надсилання повідомлень у чергу RabbitMQ
for contact in fake_contacts:
    contact.save()
    message = {
        'contact_id': str(contact.id),
    }
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Producer: Фейкові контакти збережено та повідомлення надіслано.")
connection.close()


