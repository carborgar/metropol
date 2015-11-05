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


class BranchEvent(models.Model):
    law_branch = models.ForeignKey('LawBranch', db_column='id_law_branch')
    event = models.ForeignKey('Event', db_column='id_event')

    class Meta:
        db_table = 'branch_event'


class Budget(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    attorney = models.BooleanField(default=False)
    state_budget = models.ForeignKey('StateBudget', db_column='id_state_budget', blank=True, null=True)

    class Meta:
        db_table = 'budget'


class Event(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'event'


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
    attendant = models.ForeignKey('Attendant', db_column='id_user_type', blank=True, null=True)
    phase = models.ForeignKey('Phase', db_column='id_phase', blank=True, null=True)
    state = models.ForeignKey('State', db_column='id_state')
    headquarters = models.ForeignKey('Headquarters', db_column='id_headquarters', blank=True, null=True)
    persons = models.ManyToManyField('Person', through=ExpPerRol)
    budget = models.ForeignKey(Budget, db_column='id_budget', blank=True, null=True)

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
        # Returns the attorneys of the expedient that are not part of metropol
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='PROCURADOR_CONTRARIO')]

    def own_attorneys(self):
        # Returns the attorneys of the expedient that are part of metropol
        return [expperrol.person for expperrol in self.expperrol_set.filter(role__text_help__iexact='PROCURADOR_PROPIO')]

    class Meta:
        db_table = 'expedient'
        ordering = ['-id']
        get_latest_by = 'id'


class Expiration(models.Model):
    place = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, null=True)
    expedient = models.ForeignKey(Expedient, db_column='id_expedient')
    event = models.ForeignKey(Event, db_column='id_event', blank=True, null=True)

    class Meta:
        db_table = 'expiration'
        ordering = ['date']


class Headquarters(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'headquarters'
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(models.Model):
    description = models.CharField(max_length=255)
    person = models.ForeignKey('Person', db_column='id_person', blank=True, null=True)
    expedient = models.ForeignKey(Expedient, db_column='id_exp', blank=True, null=True)

    class Meta:
        db_table = 'note'

    def __str__(self):
        return self.description


class Payment(models.Model):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    budget = models.ForeignKey(Budget, db_column='id_budget', blank=True, null=True)

    class Meta:
        db_table = 'payment'
        ordering = ['date']


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


class StateBudget(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'state_budget'
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


class Attendant(models.Model):
    name = models.CharField(max_length=255)
    text_help = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_type'
        ordering = ['name']

    def __str__(self):
        return self.name
