# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def insert_test_data():
        print('Populating with test data...')
        print('Populating with test data....OK\n')

    @staticmethod
    def insert_production_data():
        print('Populating with production data...')
        print('Populating with production data....OK\n')

    @staticmethod
    def clean_tables():
        print('Dropping tables...')
        print('Dropping tables....OK')

    def add_arguments(self, parser):
        parser.add_argument('--production', action='store_true', dest='production', default=False,
                            help='Populates the database with production data')

    def handle(self, *args, **options):
        self.clean_tables()
        self.insert_production_data() if options['production'] else self.insert_test_data()
