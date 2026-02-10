from blog.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'This Commands inserts category data'

    def handle(self, *args, **options):
        
        Category.objects.all().delete()

        categories = [
            'Technology',
            'Health',
            'Business',
            'Science',
            'Entertainment',
            'Sports',
            'Travel',
            'Lifestyle',
            'Education',
            'Food',
        ]

        for cate in categories:
            Category.objects.create(name=cate)

        self.stdout.write(self.style.SUCCESS('Completed inserting category data'))
        