from django.db import models


class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)

    def __str__(self):
        return self.texto_pregunta


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_opcion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_opcion
