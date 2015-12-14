# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def insert_test_data():
        print('Populating with test data...')

        user_carlos_borja = User(
            username='carborgar',
            first_name='Carlos',
            last_name='Borja García - Baquero',
            email='carlosborja93@gmail.com',
        )
        user_carlos_borja.set_password('metropol')
        user_carlos_borja.save()
        user_carlos_borja.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_carlos_borja.save()

        user_juan_elias_maireles = User(
            username='juamaiosu',
            first_name='Juan Elias',
            last_name='Maireles Osuna',
            email='juane.maireles@gmail.com',
        )
        user_juan_elias_maireles.set_password('metropol')
        user_juan_elias_maireles.save()
        user_juan_elias_maireles.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_juan_elias_maireles.save()

        print('Populating with test data....OK\n')

    @staticmethod
    def insert_production_data():
        print('Populating with production data...')

        # Intentionally empty

        print('Populating with production data....OK\n')

    @staticmethod
    def clean_tables():

        print('Dropping tables...')

        User.objects.all().delete()

        print('Dropping tables....OK')

    @staticmethod
    def clean_permissions():

        print('Dropping permissions...')

        Permission.objects.all().delete()

        print('Dropping permissions....OK')

    @staticmethod
    def insert_permissions():
        print('Inserting permissions...')

        Permission.objects.create(
            codename='management_metropol',
            name='Management Metropol',
            content_type=ContentType.objects.get_for_model(User)
        )

        print('Inserting permissions....OK')

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--production', action='store_true', dest='production', default=False,
                            help='Populates the database with production data')

    def handle(self, *args, **options):
        self.clean_tables()
        self.clean_permissions()
        self.insert_permissions()
        self.insert_production_data() if options['production'] else self.insert_test_data()
