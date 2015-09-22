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

        user_alfonso_fernandez = User(
            username='alffermac',
            first_name='Alfonso',
            last_name='Fernández Machuca',
            email='alfonsoprofe10@gmail.com',
        )
        user_alfonso_fernandez.set_password('metropol')
        user_alfonso_fernandez.save()
        user_alfonso_fernandez.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_alfonso_fernandez.save()

        user_santiago_machuca = User(
            username='sanmacrod',
            first_name='Santiago',
            last_name='Machuca Rodríguez',
            email='santiago.machuca@juntadeandalucia.es',
        )
        user_santiago_machuca.set_password('metropol')
        user_santiago_machuca.save()
        user_santiago_machuca.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_santiago_machuca.save()

        user_antonia_carbonell = User(
            username='antcarmor',
            first_name='Antonia',
            last_name='Carbonell Morilla',
            email='tmorilla@gmail.com',
        )
        user_antonia_carbonell.set_password('metropol')
        user_antonia_carbonell.save()
        user_antonia_carbonell.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_antonia_carbonell.save()

        user_ana_ruiz = User(
            username='anaruigon',
            first_name='Ana',
            last_name='Ruiz González',
            email='ruiz1989@hotmail.com',
        )
        user_ana_ruiz.set_password('metropol')
        user_ana_ruiz.save()
        user_ana_ruiz.user_permissions.add(Permission.objects.get(codename='management_metropol'))
        user_ana_ruiz.save()

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

    def add_arguments(self, parser):
        parser.add_argument('--production', action='store_true', dest='production', default=False,
                            help='Populates the database with production data')

    def handle(self, *args, **options):
        self.clean_tables()
        self.clean_permissions()
        self.insert_permissions()
        self.insert_production_data() if options['production'] else self.insert_test_data()
