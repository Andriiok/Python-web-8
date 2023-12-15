import json
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField
import connect



# Оголошення моделей
class Author(Document):
    fullname = StringField(required=True, max_length=100)
    born_date = DateTimeField()
    born_location = StringField(max_length=100)
    description = StringField()

class Quote(Document):
    text = StringField(required=True)
    author = StringField(required=True, max_length=100)
    tags = ListField(StringField(max_length=30))

# Зчитування даних з файлу authors.json і збереження їх у колекції авторів
with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

for author_data in authors_data:
    born_date_str = author_data.get('born_date')
    born_date = None
    if born_date_str:
        born_date = datetime.strptime(born_date_str, "%B %d, %Y")

    new_author = Author(
        fullname=author_data['fullname'],
        born_date=born_date,
        born_location=author_data.get('born_location'),
        description=author_data.get('description')
    )
    new_author.save()

# Зчитування даних з файлу quotes.json і збереження їх у колекції цитат
with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

for quote_data in quotes_data:
    new_quote = Quote(
        text=quote_data['quote'],
        author=quote_data['author'],
        tags=quote_data.get('tags', [])
    )
    new_quote.save()
