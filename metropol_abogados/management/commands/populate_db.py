# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def insertar_datos_pruebas(self):

        print('Insertando datos de pruebas...')
        print('Insertando datos de pruebas....OK\n')

    @staticmethod
    def insertar_datos_produccion(self):

        print('Insertando datos de producción...')
        print('Insertando datos de producción....OK\n')

    @staticmethod
    def clean_tables(self):

        print('Eliminando datos de las tablas...')
        print('Eliminando datos de las tablas....OK')

    def add_arguments(self, parser):

        parser.add_argument('--produccion',
                            action='store_true',
                            dest='produccion',
                            default=False,
                            help='Inserta los datos de produccion en la base de datos')

    def handle(self, *args, **options):

        self.clean_tables(self)

        if options['produccion']:
            self.insertar_datos_produccion(self)
        else:
            self.insertar_datos_pruebas(self)
