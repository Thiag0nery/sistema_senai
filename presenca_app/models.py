from django.db import models

class RegistroProfessor(models.Model):
    type_choices = [
        ('MATUTINO', 'Matutino'),
        ('VESPERTINO', 'Vespertino'),
        ('NOTURNO', 'Noturno'),
    ]
    id = models.AutoField(primary_key=True)  
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final = models.TimeField(blank=True, null=True)
    sala = models.CharField(max_length=80)
    curso = models.CharField(max_length=80)
    turma = models.CharField(max_length=80)
    professor = models.CharField(max_length=80)
    disciplina = models.CharField(max_length=80)
    data = models.CharField(max_length=10, blank=True, null=True)  
    turno = models.CharField(max_length=15,choices=type_choices, blank=True, null=True)
    def get_campos_ordem(self):
        return [self.sala, self.curso, self.turma, self.professor, self.disciplina, self.hora_inicial, self.hora_final, self.data, self.turno]

    def __str__(self):
        return f"{self.id} - {self.sala} - {self.curso} - {self.turma} - {self.professor} - {self.disciplina} - {self.data} - {self.turno}"



