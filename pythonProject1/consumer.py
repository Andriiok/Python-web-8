import json
from mongoengine import connect, Document, StringField, BooleanField
import pika
import time
import connect



# Оголошення моделі для контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

# Функція-заглушка для імітації надсилання повідомлення по email
def send_email(contact_id):
    print(f"Consumer: Надсилаю email для контакту з ID {contact_id}")
    # код для надсилання повідомлення по email
    time.sleep(2)  # Затримка для імітації надсилання

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                               port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Функція для обробки повідомлення з черги RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)

    # Виклик функції для імітації надсилання повідомлення по email
    send_email(contact_id)

    # Позначення контакту як надісланого
    contact.message_sent = True
    contact.save()

    print(f"Consumer: Оброблено повідомлення для контакту з ID {contact_id}")

# Встановлення функції зворотнього виклику для обробки повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print("Consumer: Очікування повідомлень. Для виходу натисніть CTRL+C.")
channel.start_consuming()

