# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from metropol_abogados.models import Usuario


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def insertar_datos_pruebas(self):

        print('Insertando datos de pruebas...')

        usu_carlos_borja = Usuario(
            username='carborgar',
            first_name='Carlos',
            last_name='Borja García - Baquero',
            email='carlosborja93@gmail.com',
        )
        usu_carlos_borja.set_password('metropol')
        usu_carlos_borja.save()
        usu_carlos_borja.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_carlos_borja.save()

        usu_juan_elias_maireles = Usuario(
            username='juamaiosu',
            first_name='Juan Elias',
            last_name='Maireles Osuna',
            email='juane.maireles@gmail.com',
        )
        usu_juan_elias_maireles.set_password('metropol')
        usu_juan_elias_maireles.save()
        usu_juan_elias_maireles.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_juan_elias_maireles.user_permissions.add(Permission.objects.get(codename='admin_metropol'))
        usu_juan_elias_maireles.save()

        print('Insertando datos de pruebas....OK\n')

    @staticmethod
    def insertar_datos_produccion(self):

        print('Insertando datos de producción...')

        usu_administrador = Usuario(
            username='admin',
            first_name='Juan Elias',
            last_name='Maireles Osuna',
            email='juane.maireles@gmail.com',
        )
        usu_administrador.set_password('metropol')
        usu_administrador.save()
        usu_administrador.user_permissions.add(Permission.objects.get(codename='admin_metropol'))
        usu_administrador.save()

        usu_alfonso_fernandez = Usuario(
            username='alffermac',
            first_name='Alfonso',
            last_name='Fernández Machuca',
            email='alfonsoprofe10@gmail.com',
        )
        usu_alfonso_fernandez.set_password('metropol')
        usu_alfonso_fernandez.save()
        usu_alfonso_fernandez.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_alfonso_fernandez.save()

        usu_santiago_machuca = Usuario(
            username='sanmacrod',
            first_name='Santiago',
            last_name='Machuca Rodríguez',
            email='santiago.machuca@juntadeandalucia.es',
        )
        usu_santiago_machuca.set_password('metropol')
        usu_santiago_machuca.save()
        usu_santiago_machuca.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_santiago_machuca.save()

        usu_antonia_carbonell = Usuario(
            username='antcarmor',
            first_name='Antonia',
            last_name='Carbonell Morilla',
            email='tmorilla@gmail.com',
        )
        usu_antonia_carbonell.set_password('metropol')
        usu_antonia_carbonell.save()
        usu_antonia_carbonell.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_antonia_carbonell.save()

        usu_ana_ruiz = Usuario(
            username='anaruigon',
            first_name='Ana',
            last_name='Ruiz González',
            email='ruiz1989@hotmail.com',
        )
        usu_ana_ruiz.set_password('metropol')
        usu_ana_ruiz.save()
        usu_ana_ruiz.user_permissions.add(Permission.objects.get(codename='gestion_metropol'))
        usu_ana_ruiz.save()

        print('Insertando datos de producción....OK\n')

    @staticmethod
    def clean_tables(self):

        print('Eliminando datos de las tablas...')
        Usuario.objects.all().delete()
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
