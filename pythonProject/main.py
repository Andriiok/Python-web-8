from mongoengine import Document, StringField, ListField

import connect


class Quote(Document):
    text = StringField(required=True)
    author = StringField(required=True, max_length=100)
    tags = ListField(StringField(max_length=30))


# Функція для пошуку цитат за ім'ям автора
def search_by_author(author_name):
    quotes = Quote.objects(author=author_name)
    return quotes


# Функція для пошуку цитат за тегом
def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return quotes


# Функція для пошуку цитат за набором тегів
def search_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    return quotes


# Головний цикл для введення команд
while True:
    command = input("Введіть команду: ")

    if command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        result = search_by_author(author_name)

    elif command.startswith("tag:"):
        tag = command.split(":")[1].strip()
        result = search_by_tag(tag)

    elif command.startswith("tags:"):
        tags = command.split(":")[1].split(",")
        tags = [tag.strip() for tag in tags]
        result = search_by_tags(tags)

    elif command == "exit":
        break

    else:
        print("Невідома команда. Спробуйте ще раз.")
        continue

    # Виведення результатів у форматі utf-8
    for quote in result:
        print(f"Цитата: {quote.text.encode('utf-8')}, Автор: {quote.author.encode('utf-8')}, Теги: {quote.tags}")

# Завершення програми
print("Дякую за використання скрипта.")
