from __future__ import unicode_literals
from django.db import models


class Accommodation(models.Model):
    id_accommodation = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    population = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    id_person = models.ForeignKey('Person', db_column='id_person')

    class Meta:
        db_table = 'accommodation'


class EstadoMinuta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'estado minuta'


class ExpPerRol(models.Model):
    id_exp_per_rol = models.AutoField(primary_key=True)
    id_person = models.ForeignKey('Person', db_column='id_person')
    id_role = models.ForeignKey('Role', db_column='id_role')
    id_exp = models.ForeignKey('Expedient', db_column='id_exp')
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exp_per_rol'
        unique_together = (('id_person', 'id_role', 'id_exp'),)


class Expedient(models.Model):
    id_exp = models.AutoField(primary_key=True)
    expedientesaño_exp = models.FloatField(db_column='ExpedientesAño Exp', blank=True, null=True)
    expedientesdescripción = models.CharField(db_column='ExpedientesDescripción', max_length=255, blank=True, null=True)
    expedientescódigo_expediente = models.FloatField(db_column='ExpedientesCódigo Expediente', blank=True, null=True)
    expedientesfecha_alta = models.DateTimeField(db_column='ExpedientesFecha Alta', blank=True,
                                                 null=True)
    expedientesfecha_cierre = models.CharField(db_column='ExpedientesFecha Cierre', max_length=255, blank=True,
                                               null=True)
    expedientesnúm_asunto = models.CharField(db_column='ExpedientesNúm Asunto', max_length=255, blank=True,
                                             null=True)
    expedientestotal_cuantía = models.FloatField(db_column='ExpedientesTotal Cuantía', blank=True,
                                                 null=True)
    estadominuta = models.IntegerField(db_column='EstadoMinuta', blank=True, null=True)
    id_type_user = models.ForeignKey('TypeUser', db_column='id_type_user', blank=True, null=True)
    ramaderecho = models.IntegerField(db_column='RamaDerecho', blank=True, null=True)
    id_state = models.ForeignKey('State', db_column='id_state')
    id_headquarters = models.ForeignKey('Headquarters', db_column='id_headquarters', blank=True, null=True)

    class Meta:
        db_table = 'expedient'


class Headquarters(models.Model):
    id_headquarters = models.AutoField(primary_key=True)
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
    id_note = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    id_person = models.ForeignKey('Person', db_column='id_person', blank=True, null=True)
    id_exp = models.ForeignKey(Expedient, db_column='id_exp', blank=True, null=True)

    class Meta:
        db_table = 'note'


class Person(models.Model):
    id_person = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    id_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    web = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'person'


class Phone(models.Model):
    id_phone = models.AutoField(primary_key=True)
    number = models.CharField(max_length=255)
    id_person = models.ForeignKey(Person, db_column='id_person')
    id_type_phone = models.ForeignKey('TypePhone', db_column='id_type_phone')

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
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'role'


class State(models.Model):
    id_state = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'state'

    def __str__(self):
        return self.name


class TypePhone(models.Model):
    id_type_phone = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'type_phone'

    def __str__(self):
        return self.name


class TypeUser(models.Model):
    id_type_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'type_user'

    def __str__(self):
        return self.name


class Vencimientos(models.Model):
    númexpediente = models.FloatField(db_column='NúmExpediente')
    fechavencimiento = models.DateTimeField(db_column='FechaVencimiento')
    descripción = models.CharField(db_column='Descripción', max_length=255, blank=True, null=True)
    juicio = models.CharField(db_column='Juicio', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'vencimientos'
