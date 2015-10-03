from __future__ import unicode_literals
from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    person = models.ForeignKey('Person', db_column='id_person')

    class Meta:
        db_table = 'address'


class EstadoMinuta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'estado minuta'


class ExpPerRol(models.Model):
    person = models.ForeignKey('Person', db_column='id_person')
    role = models.ForeignKey('Role', db_column='id_role')
    exp = models.ForeignKey('Expedient', db_column='id_exp')
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exp_per_rol'
        unique_together = (('person', 'role', 'exp'),)


class Expedient(models.Model):
    expedientesaño_exp = models.FloatField(db_column='ExpedientesAño Exp', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedientesdescripción = models.CharField(db_column='ExpedientesDescripción', max_length=255, blank=True, null=True)  # Field name made lowercase.
    expedientescódigo_expediente = models.FloatField(db_column='ExpedientesCódigo Expediente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedientesfecha_alta = models.DateTimeField(db_column='ExpedientesFecha Alta', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedientesfecha_cierre = models.CharField(db_column='ExpedientesFecha Cierre', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedientesnúm_asunto = models.CharField(db_column='ExpedientesNúm Asunto', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedientestotal_cuantía = models.FloatField(db_column='ExpedientesTotal Cuantía', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estadominuta = models.IntegerField(db_column='EstadoMinuta', blank=True, null=True)  # Field name made lowercase.
    user_type = models.ForeignKey('UserType', db_column='id_user_type', blank=True, null=True)
    ramaderecho = models.IntegerField(db_column='RamaDerecho', blank=True, null=True)  # Field name made lowercase.
    state = models.ForeignKey('State', db_column='id_state')
    headquarters = models.ForeignKey('Headquarters', db_column='id_headquarters', blank=True, null=True)

    class Meta:
        db_table = 'expedient'


class Headquarters(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'headquarters'

    def __str__(self):
        return self.name


class HistorialPresupuestos(models.Model):
    expediente = models.IntegerField(db_column='Expediente')
    fecha = models.DateTimeField(db_column='Fecha')
    cantidad_entregada = models.DecimalField(db_column='Cantidad_entregada', max_digits=19, decimal_places=4)

    class Meta:
        db_table = 'historial_presupuestos'


class Note(models.Model):
    description = models.CharField(max_length=255)
    person = models.ForeignKey('Person', db_column='id_person', blank=True, null=True)
    expedient = models.ForeignKey(Expedient, db_column='id_exp', blank=True, null=True)

    class Meta:
        db_table = 'note'


class Person(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    id_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    web = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'person'

    def __str__(self):
        return self.name


class Phone(models.Model):
    number = models.CharField(max_length=255)
    person = models.ForeignKey(Person, db_column='id_person')
    phone_type = models.ForeignKey('PhoneType', db_column='id_phone_type')

    class Meta:
        db_table = 'phone'


class Presupuestos(models.Model):
    númeroexpediente = models.FloatField(db_column='NúmeroExpediente', primary_key=True)
    presupuesto_total = models.DecimalField(db_column='Presupuesto total', max_digits=19, decimal_places=4, blank=True,
                                            null=True)
    cantidad_entregada = models.DecimalField(db_column='Cantidad entregada', max_digits=19, decimal_places=4,
                                             blank=True, null=True)
    estadominuta = models.IntegerField(db_column='EstadoMinuta', blank=True, null=True)
    última_revisión = models.DateTimeField(db_column='Última revisión', blank=True, null=True)
    descripción = models.CharField(db_column='Descripción', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'presupuestos'


class RamaDerecho(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    rama = models.CharField(db_column='Rama', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'rama derecho'


class Role(models.Model):
    text_help = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
        ordering = ['name']

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'state'

    def __str__(self):
        return self.name


class PhoneType(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'phone_type'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserType(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'user_type'

    def __str__(self):
        return self.name


class Vencimientos(models.Model):
    númexpediente = models.FloatField(db_column='NúmExpediente')
    fechavencimiento = models.DateTimeField(db_column='FechaVencimiento')
    descripción = models.CharField(db_column='Descripción', max_length=255, blank=True, null=True)
    juicio = models.CharField(db_column='Juicio', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'vencimientos'
