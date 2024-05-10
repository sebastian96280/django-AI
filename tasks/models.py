from django.db import models
from django.contrib.auth.models import User
import os
import uuid
import datetime
import holidays
# Enviar correos
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives



# Creando modelos de bases de datos


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by' + self.user.username

# tabla tipo de documento


class tTipe_document(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
# tabla tipo solicitud


class tTipo_solicitud(models.Model):
    nombre_solicitud = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

# tabla estado de solicitud


class tEstado_solicitud(models.Model):
    nombre_tipoS = models.CharField(max_length=100)

# tabla de areas de la compañia


class tArea(models.Model):
    nombre_area = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

# tabla de estado activo de todo


class tEstado_Activo(models.Model):
    esta_activo = models.BooleanField()

# tabla de estado del usuario(volver booleano 0 inactivo 1 para activo - NO SE PUEDE YA SE AÑADIO UN USUARIO O MIRAR COMO SE PUEDE HACER PARA REEMPLAZAR EL VALOR)


class tEstado_usuario(models.Model):
    nombre_estado = models.CharField(max_length=100)


# tabla de usuarios de la compañia


class usuarioExtendido(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    id_documento = models.ForeignKey(tTipe_document, on_delete=models.CASCADE)
    numero_identificacion = models.CharField(max_length=20)
    id_area = models.ForeignKey(tArea, on_delete=models.CASCADE)
    esta_activo = models.BooleanField(default=True)


# tabla de la solicitud
class tformatoSolicitud(models.Model):
    nombre_formato = models.CharField(max_length=100)

class tSolicitud(models.Model):
    # datos usuario
    nombre = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    id_tipo_identificacion = models.ForeignKey(tTipe_document, on_delete=models.CASCADE)
    numero_identificacion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    # datos solicitud

    asunto = models.CharField(max_length=100)
    id_nombre_formato = models.ForeignKey(tformatoSolicitud, on_delete=models.PROTECT)
    mensaje = models.TextField(max_length=250)
    archivo = models.FileField(upload_to='pdfs/', null=True)

    # estado solicitud
    id_tipo_solicitud = models.ForeignKey(tTipo_solicitud, on_delete=models.CASCADE, blank=True, null=True)
    id_estado_solicitud = models.ForeignKey(tEstado_solicitud, on_delete=models.CASCADE, default =1)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    archivo_respuesta = models.FileField(upload_to='respuestas/', null=True)
    id_area = models.ForeignKey(tArea, on_delete=models.CASCADE, blank=True, null=True)
    id_esta_activo = models.ForeignKey(tEstado_Activo, on_delete=models.CASCADE, default=True)
    politica_privacidad = models.BooleanField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)
    fecha_de_respuesta_oportuna = models.DateTimeField(null=True, blank=True)
    fecha_de_cierre = models.DateTimeField(null=True, blank=True)    

    def save(self, *args, **kwargs):
        # Guarda el objeto primero para asegurarte de que self.fecha_de_registro esté establecida
        super().save(*args, **kwargs)
        if self.fecha_de_respuesta_oportuna is None:
            self.fecha_de_respuesta_oportuna = self.calcular_fecha_oportuna()
            # Guarda el objeto de nuevo, pero solo actualiza fecha_de_respuesta_oportuna
            super().save(update_fields=['fecha_de_respuesta_oportuna'])
            self.correo_registro_solicitud()

    def calcular_fecha_oportuna(self):
        fecha = self.fecha_de_registro
        dias_habiles = 0
        festivos_colombia = holidays.Colombia()

        while dias_habiles < 14:
            fecha += datetime.timedelta(days=1)
            if fecha.weekday() < 5 and fecha not in festivos_colombia:  # 0-4 corresponde a Lunes-Viernes
                dias_habiles += 1

        return fecha
    
    def correo_registro_solicitud(self):
        radicado = self.id
        fecha_radicado = self.fecha_de_registro
        solicitante = self.nombre + " " + self.apellidos
        asunto = 'Radicado #'+str(self.id)+' radicado con exido - UDC'
        descripcion = self.mensaje
        enlace = 'http://127.0.0.1:8000/consultarRadicado/?numero_identificacion='+self.numero_identificacion+'&correo='+self.correo
        plantilla_correo = render_to_string('plantilla_correo.html', {
            'radicado': radicado,
            'fecha_radicado': fecha_radicado,
            'solicitante': solicitante,
            'asunto': self.asunto,
            'descripcion': descripcion,
            'enlace': enlace
        })
        email = EmailMultiAlternatives(
            asunto,
            plantilla_correo,
            settings.EMAIL_HOST_USER,
            [self.correo]
        )
        email.attach_alternative(plantilla_correo, "text/html")
        email.fail_silently = False
        email.send()


class configuracion_correo(models.Model):
    email_backend = models.CharField(max_length=255)
    email_host = models.CharField(max_length=255)
    email_port = models.IntegerField()
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)
    email_use_tls = models.BooleanField()


# ENVIO DE CORREOS
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'jhoan.96280@gmail.com'
#EMAIL_HOST_PASSWORD= 'ndmbsetlqjitdcrk'
#EMAIL_USE_TLS = True
