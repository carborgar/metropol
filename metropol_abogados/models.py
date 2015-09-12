from django.contrib.auth.models import User
from django.db import models


class Usuario(User):

    class Meta:
        ordering = ['last_name', 'first_name']
        db_table = 'metropol_t_r_usu_usuario'

    def __str__(self):
        return self.last_name + ', ' + self.first_name
