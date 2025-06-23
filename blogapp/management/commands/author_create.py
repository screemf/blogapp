from django.core.management.base import  BaseCommand
from blogapp.models import Author


class Command(BaseCommand):
    help = 'Creates author'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of author')


    def handle(self, *args, **options):
        name=options.get('name')
        author = Author.objects.create (name=name,
                                        age = 40,
                                        email = f'{name}@mail.com',
                                        bio = f'test {name}')
        author.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {author}'))