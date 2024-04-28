from django.db import transaction
from pymongo import MongoClient
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dz_project.settings')
django.setup()
# Підключення до MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['DZ_10']


from quotes.models import Quote, Tag, Author # noqa

# Перенесення даних з quotes
quotes_collection = mongo_db['quotes']
for quote_doc in quotes_collection.find():
    with transaction.atomic():  # Використовуємо transaction.atomic для забезпечення атомарності операцій
        # Отримуємо ID автора з цитати
        author_id = quote_doc['author']

        # Отримуємо ім'я автора за його ID
        author_doc = mongo_db['authors'].find_one({'_id': author_id})
        author_fullname = author_doc['fullname'] if author_doc else None

        # Отримуємо або створюємо автора у PostgreSQL
        author, _ = Author.objects.get_or_create(
            fullname=author_fullname,
            defaults={
                'born_date': author_doc['born_date'] if author_doc else '',
                'born_location': author_doc['born_location'] if author_doc else '',
                'description': author_doc['description'] if author_doc else ''
            }
        )

        # Створюємо нову цитату
        quote = Quote.objects.create(
            quote=quote_doc['quote'],
            author=author
        )

        # Додаємо теги до цитати
        for tag_name in quote_doc['tags']:
            if len(tag_name) < 30:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
            else:
                print(f"Ім'я тегу {tag_name} занадто довге. Пропускаємо.")