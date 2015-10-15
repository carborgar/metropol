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
    expedient = models.ForeignKey('Expedient', db_column='id_exp')
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exp_per_rol'
        unique_together = (('person', 'role', 'expedient'),)


class Expedient(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    user_type = models.ForeignKey('UserType', db_column='id_user_type', blank=True, null=True)
    phase = models.ForeignKey('Phase', db_column='id_phase', blank=True, null=True)
    state = models.ForeignKey('State', db_column='id_state')
    headquarters = models.ForeignKey('Headquarters', db_column='id_headquarters', blank=True, null=True)
    # persons = models.ManyToManyField('Person', through=ExpPerRol)

    def customers(self):
        # Returns the customers of the expedient
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='CLIENTE')]

    def contraries(self):
        # Returns the contraries (not lawyers) of the expedient
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='CONTRARIO')]

    def contrary_lawyers(self):
        # Returns the contrary lawyers of the expedient
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='ABOGADO_CONTRARIO')]

    def attorneys(self):
        # Returns the attorneys of the expedient
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='PROCURADOR')]

    class Meta:
        db_table = 'expedient'


class Headquarters(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'headquarters'
        ordering = ['name']

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
    creation_date = models.DateTimeField()

    class Meta:
        db_table = 'person'

    def __str__(self):
        return self.name or ''


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


class LawBranch(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'law_branch'
        ordering = ['name']


class Phase(models.Model):
    sequence = models.IntegerField()
    name = models.CharField(max_length=255)
    text_help = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    law_branch = models.ForeignKey(LawBranch, db_column='id_law_branch')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phase'
        ordering = ['sequence']
        unique_together = (('id', 'sequence'),)


class Role(models.Model):
    text_help = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
        ordering = ['name']

    def __str__(self):
        return self.name


class State(models.Model):
    text_help = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'state'
        ordering = ['name']

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
    text_help = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_type'
        ordering = ['name']

    def __str__(self):
        return self.name


class Vencimientos(models.Model):
    númexpediente = models.FloatField(db_column='NúmExpediente')
    fechavencimiento = models.DateTimeField(db_column='FechaVencimiento')
    descripción = models.CharField(db_column='Descripción', max_length=255, blank=True, null=True)
    juicio = models.CharField(db_column='Juicio', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'vencimientos'
