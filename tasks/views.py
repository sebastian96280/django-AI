from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import time
import re
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from io import BytesIO
from datetime import datetime
import pytz
from django.conf import settings

# importar formulario y modelo(BD) de usuario extendido
from .forms import usuarioExtForm
from .models import usuarioExtendido
from .forms import usuarioExtFormModificacion
from .forms import miUsuarioExtFormModificacion
# importar formulario y modelo(BD) de tipo de documento
from .forms import tDocumentoForm
from .models import tTipe_document
# importar formulario y modelo(BD) de tipo de solicitud
from .forms import tTipoSForm
from .models import tTipo_solicitud
# importar formulario y modelo(BD) de area
from .forms import tAreaForm
from .models import tArea
# importar formulario y modelo(BD) de estado solicitud
from .forms import tEstadoSForm
from .models import tEstado_solicitud
# importar formulario y modelo(BD) de crear solicitud
from .forms import tSolicitudForm
from .models import tSolicitud
from .forms import tSolicitudFormRespuesta
from .forms import tSolicitudFormModificacionAreaTipo
from .forms import tSolicitudFormModificacionAll
from .forms import tSolicitudFormAsignacionUsuario
# importar formulario y modelo(BD) de crear estado activo
from .forms import tEstadoActivoForm
from .models import tEstado_Activo
# importar formulario y modelo(BD) de configuración de correo
from .forms import configuracionCorreoForm
from .models import configuracion_correo

# importar para crear pdf.
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# importar form para buscar radicados
from .forms import ConsultarRadicadosForm
# permitir realizar 2 consultas a la vez
from django.db.models import Q

# manipulador del os
import os
import shutil

# importar pdf
from django.http import FileResponse


# crea pdf a imagen.
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
# modificación archivos alfanumericos
import uuid

# convertir imagenes a texto.
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'


#Ejecución de IA
import pandas as pd 
from imblearn.under_sampling import RandomUnderSampler
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from django_pandas.io import read_frame
from .models import tSolicitud
#ramdom de usuarios
import random
#requerir iniicio de sesión @login_required
from django.contrib.auth.decorators import login_required


def error_404_view(request, exception):
    return render(request, '404.html')


def signup(request):
    title = 'variable'

    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'mytitle': title,
            'form': UserCreationForm
        })
    else:
        print('obteniendo datos')
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # guardamos al usuario en el objeto user para registrarlo
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()

                # crear la sesión del usuario
                login(request, user)

                # redireccionar a task.html
                return redirect(creaTipoSolicitud)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'error el usuario existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'contraseña no coincide'
        })

def singnin(request):
    if request.method == 'GET':

        return render(request, 'inicio_sesion.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inicio_sesion.html', {
                'form': AuthenticationForm,
                'error': 'El usuario y/o la contraseña son incorrectos'
            })
        else:
            # crear la sesión del usuario
            login(request, user)
            return redirect('consultarSolicitud')

# -------------------------------------- Funciones de creación --------------------------------------

def crearUsuario(request):
    if request.method == 'GET':
        return render(request, 'crea_usuario.html', {
            'form': usuarioExtForm
        })
    else:
        print(request.POST)
        form = usuarioExtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultarUsuario')
        else:
            return render(request, 'crea_usuario.html', {
                'form': form
            })

@login_required
def creaTdocumento(request):
    if request.method == 'GET':
        return render(request, 'crea_tipo_d.html', {
            'form': tDocumentoForm
        })
    else:
        print(request.POST)
        form = tDocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            estado = 'Creado'
            mensaje = 'Tipo documento ' + request.POST['nombre_tipo']+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            tipos_documento = tTipe_document.objects.all()
            return render(request, 'consulta_tipos_documento.html', {
                'mensaje': mensaje,
                'tipos_documento': tipos_documento  # Pasa los usuarios a la plantilla
            })
        else:
            return render(request, 'crea_tipo_d.html', {
                'form': form, 'error': 'Por favor, provee datos válidos'
            })

@login_required
def creaTipoSolicitud(request):
    if request.method == 'GET':
        return render(request, 'crea_tipo_solicitud.html', {
            'form': tTipoSForm
        })
    else:
        print(request.POST)
        form = tTipoSForm(request.POST)
        if form.is_valid():
            form.save()
            estado = 'Creado'
            mensaje = 'Tipo de solicitud ' + request.POST['nombre_solicitud']+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            tipos_solicitudes = tTipo_solicitud.objects.all()
            return render(request, 'consulta_tipos_solicitudes.html', {
                'mensaje': mensaje,
                'tipos_solicitudes': tipos_solicitudes  # Pasa los usuarios a la plantilla
            })
        else:
            return render(request, 'crea_tipo_solicitud.html', {
                'form': form, 'error': 'Por favor, provee datos válidos'
            })

@login_required
def creaTarea(request):
    if request.method == 'GET':
        return render(request, 'crea_area.html', {
            'form': tAreaForm
        })        
    else:
        print(request.POST)
        form = tAreaForm(request.POST)
        if form.is_valid():
            form.save()
            estado = 'Creado'
            mensaje = 'Area o departamento ' + request.POST['nombre_area']+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            areas = tArea.objects.all()
            return render(request, 'consulta_area.html', {
                'mensaje': mensaje,
                'areas': areas  # Pasa los usuarios a la plantilla
            })
        else:
            return render(request, 'crea_area.html', {
                'form': form, 'error': 'Por favor, provee datos válidos'
            })

@login_required
def creaEstadoS(request):
    if request.method == 'GET':
        return render(request, 'crea_estado_Sol.html', {
            'form': tEstadoSForm
        })
    else:
        print(request.POST)
        form = tEstadoSForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'crea_estado_Sol.html', {
                'form': tEstadoSForm,
                'error': 'creado exitosamente'
            })
        else:
            return render(request, 'crea_estado_Sol.html', {
                'form': form, 'error': 'Por favor, provee datos válidos'
            })


def creaSolicitud(request):
    if request.method == 'GET':
        return render(request, 'crea_solicitud.html', {'form': tSolicitudForm()})
    else:
        form = tSolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_solicitud = form.save(commit=False)
            if request.POST['id_nombre_formato'] == '1':
                # Crea un objeto de archivo PDF
                nombre_archivo_cambiado = cambiar_nombre_archivo('nombre_archivo_original.pdf')
                ruta_archivo = os.path.join('pdfs/', nombre_archivo_cambiado)

                # Crea el objeto PDF, usando la ruta del archivo como su "archivo"
                p = canvas.Canvas(ruta_archivo, pagesize=letter)

                # Dibuja cosas en el PDF. Aquí es donde comienza la generación del PDF.
                asunto = request.POST['asunto']
                mensaje = request.POST['mensaje']
                p.drawString(100, 750, "Asunto: " + asunto)
                p.drawString(100, 730, "Mensaje: " + mensaje)

                # Cierra el objeto PDF limpiamente y termina la página.
                p.showPage()
                p.save()
                # Aquí puedes guardar la ruta del archivo en tu objeto de solicitud si lo necesitas
                nueva_solicitud.archivo.name = ruta_archivo
                id_ia = ejecutar_IA_Tipo_Solicitud(asunto)
                if id_ia != 0:
                    id_tipo_solicitud = id_ia
                    tipo_solicitud = get_object_or_404(tTipo_solicitud, pk=id_tipo_solicitud)
                    nueva_solicitud.id_tipo_solicitud = tipo_solicitud                 
                nueva_solicitud.save()

                ultimo_objeto = tSolicitud.objects.latest('id')
                dividir_nombre_carpetaYarchivo(nombre_archivo_cambiado)
                ultimo_id = ultimo_objeto.id
                preparar_IA(ultimo_id)

                return render(request, 'crea_solicitud.html', {'form': tSolicitudForm(), 'confirmacion': 'Se ha recibido su solicitud. Pronto recibirá en su correo electrónico el número de radicado correspondiente, así como las instrucciones para consultar el estado de la misma.'})
            
            elif request.POST['id_nombre_formato'] == '2':
                nombre_archivo_original = nueva_solicitud.archivo.name
                nombre_archivo_cambiado = cambiar_nombre_archivo(nombre_archivo_original)
                nueva_solicitud.archivo.name = nombre_archivo_cambiado

                #Se envia el asunto al modelo IA para que nos retorne ID, si el ID es 0 quiere decir que la coincidencia es menor del 80%      
                asunto = request.POST['asunto']
                id_ia = ejecutar_IA_Tipo_Solicitud(asunto)
                if id_ia != 0:
                    #Se guarda la solicitud de acuerdo con el ID que determine la IA
                    id_tipo_solicitud = id_ia
                    tipo_solicitud = get_object_or_404(tTipo_solicitud, pk=id_tipo_solicitud)
                    nueva_solicitud.id_tipo_solicitud = tipo_solicitud 
                    #Se guarda la solicitud con el estado Clasificada
                    '''
                    id_estado_solicitud = 4
                    tipo_solicitud = get_object_or_404(tEstado_solicitud, pk=id_estado_solicitud)
                    nueva_solicitud.id_estado_solicitud = tipo_solicitud
                    '''
                else:
                    #Se guarda la solicitud con el estado Clasificación Manual
                    '''
                    id_estado_solicitud = 3
                    tipo_solicitud = get_object_or_404(tEstado_solicitud, pk=id_estado_solicitud)
                    nueva_solicitud.id_estado_solicitud = tipo_solicitud
                    '''
                nueva_solicitud.save()

                ultimo_objeto = tSolicitud.objects.latest('id')
                dividir_nombre_carpetaYarchivo(nombre_archivo_cambiado)
                ultimo_id = ultimo_objeto.id
                preparar_IA(ultimo_id)           
            

            return render(request, 'crea_solicitud.html', {'form': tSolicitudForm(), 'confirmacion': 'Se ha recibido su solicitud. Pronto recibirá en su correo electrónico el número de radicado correspondiente, así como las instrucciones para consultar el estado de la misma.'})
        else:
            return render(request, 'crea_solicitud.html', {'form': form, 'error': 'Por favor, provee datos válidos'})



def CrearActivo(request):
    if request.method == 'GET':
        return render(request, 'crear_activo.html', {
            'form': tEstadoActivoForm
        })
    else:
        form = tEstadoActivoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'crear_activo.html', {
                'form': tEstadoActivoForm
            })
        else:
            return render(request, 'crear_activo.html', {
                'form': form, 'error': 'Por favor, provee datos válidos'
            })

# --------------------------------- Funciones de consulta---------------------------------

# consultar tipo de documento


def consulta_tipoDocumento(request):
    tipos_documento = tTipe_document.objects.all()
    return render(request, 'consulta_tipos_documento.html', {
        'tipos_documento': tipos_documento
    })


def consulta_tipoSolicitud(request):
    tipos_solicitudes = tTipo_solicitud.objects.all()
    return render(request, 'consulta_tipos_solicitudes.html', {
        'tipos_solicitudes': tipos_solicitudes
    })


def consulta_area(request):
    areas = tArea.objects.all()
    return render(request, 'consulta_area.html', {
        'areas': areas
    })

@login_required
def consulta_usuario(request):
    usuarios = usuarioExtendido.objects.all()
    return render(request, 'consulta_usuarios.html', {
        'usuarios': usuarios
    })

@login_required
def consulta_solicitudes_sin_clasificar(request):
    solicitudes = tSolicitud.objects.filter(Q (id_area=None) | Q (id_tipo_solicitud=None))
    return render(request, 'consulta_solicitudes_sin_clasificar.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_solicitudes(request):
    solicitudes = tSolicitud.objects.all()
    return render(request, 'consulta_solicitudes_abi_cerr.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_solicitudes_cerradas(request):
    solicitudes = tSolicitud.objects.filter((~Q (id_area=None) & ~Q (id_tipo_solicitud=None)) & Q (id_esta_activo=2))
    return render(request, 'consulta_solicitudes_abi_cerr.html', {
        'solicitudes': solicitudes
    })
@login_required
def consulta_solicitudes_abiertas(request):
    solicitudes = tSolicitud.objects.filter(id_esta_activo=1)
    return render(request, 'consulta_solicitudes.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_mis_solicitudes(request):
    usuario_actual = request.user
    solicitudes = tSolicitud.objects.filter(id_usuario=usuario_actual)
    return render(request, 'consulta_mis_solicitudes.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_mis_solicitudes_abiertas(request):
    usuario_actual = request.user
    solicitudes = tSolicitud.objects.filter(id_usuario=usuario_actual,id_esta_activo=1)
    return render(request, 'consulta_mis_solicitudes_abiertas.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_mis_solicitudes_cerradas(request):
    usuario_actual = request.user
    solicitudes = tSolicitud.objects.filter(id_usuario=usuario_actual,id_esta_activo=2)
    return render(request, 'consulta_mis_solicitudes_cerradas.html', {
        'solicitudes': solicitudes
    })

@login_required
def consulta_solicitudes_del_area(request):
    usuario_actual = request.user
    usuario_extendido = usuarioExtendido.objects.get(user=usuario_actual)
    id_area = usuario_extendido.id_area.id    
    solicitudes = tSolicitud.objects.filter(id_area=id_area)
    return render(request, 'consulta_solicitudes_del_area.html', {
        'solicitudes': solicitudes
    })

def consultar_radicados(request):
    form = ConsultarRadicadosForm(request.GET)
    resultados = None
    error = None

    if 'numero_identificacion' in request.GET or 'correo' in request.GET:
        if form.is_valid():
            numero_identificacion = form.cleaned_data.get(
                'numero_identificacion')
            correo = form.cleaned_data.get('correo')
            if numero_identificacion != '' and correo != '':
                resultados = tSolicitud.objects.all()
                if numero_identificacion:
                    resultados = resultados.filter(
                        numero_identificacion=numero_identificacion)
                if correo:
                    resultados = resultados.filter(correo=correo)
                if not resultados.exists():
                    error = 'El radicado no ha sido encontrado. Por favor, verifique la información proporcionada e intente nuevamente'
            else:
                error = 'Por favor, ingrese los dos criterios de búsqueda'
    return render(request, 'consulta_radicado.html', {'form': form, 'resultados': resultados, 'error': error})


# --------------------------------- Funciones de Restablecer contraseña Usuario ---------------------

def restabler_contrasena(request, usuario_id):
    if request.method == 'GET':
        usuario = get_object_or_404(User, pk=usuario_id)
        form = usuarioExtForm(instance=usuario)
        return render(request, 'restablecer_contrasena.html', {'usuario': usuario})
    else:
        try:
            usuario = get_object_or_404(User, pk=usuario_id)
            if request.POST['password1'] == request.POST['password2']:
                nueva_contrasena = request.POST['password1']
                usuario.set_password(nueva_contrasena)
                usuario.save()

                correo_restablecmiento_contrasena(usuario_id, nueva_contrasena)

                mensaje = 'Contraseña de ' + usuario.username + ' cambiado/a con exito.'
                usuarios = usuarioExtendido.objects.all()
                return render(request, 'consulta_usuarios.html', {
                    'mensaje': mensaje,
                    'usuarios': usuarios
                })
            else:
                return render(request, 'restablecer_contrasena.html', {
                    'usuario': usuario,
                    'error': 'Las contraseñas no coinciden'
                })
        except ValueError:
            return render(request, 'restablecer_contrasena.html', {
                'usuario': usuario,
                'error': 'Error al intentar cambiar la contraseña'
            })


def correo_restablecmiento_contrasena(usuario_id, nueva_contrasena):
    # Obtén el usuario por su ID
    usuario = User.objects.get(pk=usuario_id)

    # Ahora puedes acceder a los campos del usuario
    username = usuario.username
    email = usuario.email
    asunto = 'Restablecimiento Contraseña - Plataforma UDC'

    plantilla_correo = render_to_string('plantilla_correo_res_contrasena.html', {
        'username': username,
        'nueva_contrasena': nueva_contrasena
    })
    email = EmailMultiAlternatives(
        asunto,
        plantilla_correo,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(plantilla_correo, "text/html")
    email.fail_silently = False
    email.send()

def correo_respuesta_solicitud(id_solicitud):
    usuario = tSolicitud.objects.get(pk=id_solicitud)
    radicado = usuario.id
    correo = usuario.correo
    fecha_radicado = usuario.fecha_de_registro
    enlace = 'http://127.0.0.1:8000/consultarRadicado/?numero_identificacion='+usuario.numero_identificacion+'&correo='+usuario.correo
    asunto = 'Respuesta Radicado #' + str(radicado) + '- Plataforma UDC'

    plantilla_correo = render_to_string('plantilla_correo_respuesta_solicitud.html', {
        'enlace': enlace,
        'radicado':radicado,
        'fecha_radicado':fecha_radicado
    })
    email = EmailMultiAlternatives(
        asunto,
        plantilla_correo,
        settings.EMAIL_HOST_USER,
        [correo]
    )
    email.attach_alternative(plantilla_correo, "text/html")
    email.fail_silently = False
    email.send()

# --------------------------------- Funciones de Activar Desactivar ---------------------------------


def activar_desactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(usuarioExtendido, pk=usuario_id)
    usuario.esta_activo = not usuario.esta_activo
    usuario.user.is_active = not usuario.user.is_active
    usuario.save()
    usuario.user.save()
    estado = 'Activado' if usuario.user.is_active else 'Desactivado'
    mensaje = 'Usuario ' + usuario.user.username+' ' + estado + ' con exito.'
    # Vuelve a consultar los usuarios
    usuarios = usuarioExtendido.objects.all()

    return render(request, 'consulta_usuarios.html', {
        'mensaje': mensaje,
        'usuarios': usuarios  # Pasa los usuarios a la plantilla
    })

def activar_desactivar_tipo_documento(request, tipod_id):
    tipo_documento = get_object_or_404(tTipe_document, pk=tipod_id)
    tipo_documento.estado = not tipo_documento.estado
    tipo_documento.save()
    estado = 'Activado' if tipo_documento.estado else 'Desactivado'
    mensaje = 'Tipo documento ' + tipo_documento.nombre_tipo+' ' + estado + ' con exito.'
    # Vuelve a consultar el modelo
    tipos_documento = tTipe_document.objects.all()

    return render(request, 'consulta_tipos_documento.html', {
        'mensaje': mensaje,
        'tipos_documento': tipos_documento  # Pasa los usuarios a la plantilla
    })

def activar_desactivar_tipo_solicitud(request, tipod_id):
    tipo_solicitud = get_object_or_404(tTipo_solicitud, pk=tipod_id)
    tipo_solicitud.estado = not tipo_solicitud.estado
    tipo_solicitud.save()
    estado = 'Activado' if tipo_solicitud.estado else 'Desactivado'
    mensaje = 'Tipo de solicitud ' + tipo_solicitud.nombre_solicitud + ' ' + estado + ' con exito.'
    # Vuelve a consultar el modelo
    tipos_solicitudes = tTipo_solicitud.objects.all()

    return render(request, 'consulta_tipos_solicitudes.html', {
        'mensaje': mensaje,
        'tipos_solicitudes': tipos_solicitudes  # Pasa los usuarios a la plantilla
    })

def activar_desactivar_area(request, area_id):
    area = get_object_or_404(tArea, pk=area_id)
    area.estado = not area.estado
    area.save()
    estado = 'Activado' if area.estado else 'Desactivado'
    mensaje = 'Area o departamenot ' + area.nombre_area + ' ' + estado + ' con exito.'
    # Vuelve a consultar el modelo
    areas = tArea.objects.all()

    return render(request, 'consulta_area.html', {
        'mensaje': mensaje,
        'areas': areas  # Pasa los usuarios a la plantilla
    })

def activar_solicitud(request, solicitud_id):
    solicitudes = get_object_or_404(tSolicitud, pk=solicitud_id)
    estado_activo = tEstado_Activo.objects.get(id=1)  # Asume que 1 es el estado activo
    estado_solicitud = tEstado_solicitud.objects.get(id=5)
    solicitudes.id_esta_activo = estado_activo
    solicitudes.id_estado_solicitud = estado_solicitud
    solicitudes.save()
    estado = 'Re Abierta'
    mensaje = 'Solicitud ' + str(solicitudes.id) +' ' + estado + ' con exito.'
    # Vuelve a consultar las solicitudes
    usuario_actual = request.user
    solicitudes = tSolicitud.objects.filter(id_usuario=usuario_actual,id_esta_activo=2)                                          #<-------------------------pendiente cambiar consulta

    return render(request, 'consulta_mis_solicitudes_cerradas.html', {
        'mensaje': mensaje,
        'solicitudes': solicitudes  # Pasa los usuarios a la plantilla
    })



# --------------------------------- Funciones de modificación---------------------------------
def modificar_usuario(request, usuario_id):
    documentos = tTipe_document.objects.all()
    areas = tArea.objects.all()
    if request.method == 'GET':
        usuario = get_object_or_404(usuarioExtendido, pk=usuario_id)
        form = usuarioExtFormModificacion(instance=usuario)
        return render(request, 'modificar_usuario.html', {
            'form': form, 'usuario': usuario, 'documentos': documentos, 'areas': areas
    })
    else:
        usuario = get_object_or_404(usuarioExtendido, pk=usuario_id)
        form = usuarioExtFormModificacion(request.POST, instance=usuario)
        if form.is_valid():            
            form.save()

            usuarios = usuarioExtendido.objects.all()
            estado = 'Modificado'
            mensaje = 'Usuario  ' + str(usuario.id)+' ' + estado + ' con exito.'
            return render(request, 'consulta_usuarios.html', {
            'usuarios': usuarios, 'mensaje': mensaje
        })

        else:
            print(form.errors)           
            return render(request, 'modificar_usuario.html', {
                'form': form, 'usuario': usuario, 'documentos': documentos, 'areas': areas
        })

@login_required
def consulta_mi_usuario(request):
    usuario_actual = request.id
    usuarios = usuarioExtendido.objects.filter(id_usuario=usuario_actual)
    return render(request, 'consulta_mi_usuario.html', {
        'usuarios': usuarios
    })

@login_required
def modificar_mi_usuario(request):
    documentos = tTipe_document.objects.all()
    areas = tArea.objects.all()
    usuario_actual = request.user.id
    if request.method == 'GET':
        usuario = get_object_or_404(usuarioExtendido, user_id=usuario_actual)
        form = miUsuarioExtFormModificacion(instance=usuario)
        return render(request, 'modificar_mi_usuario.html', {
            'form': form, 'usuario': usuario, 'documentos': documentos, 'areas': areas
    })
    else:
        usuario = get_object_or_404(usuarioExtendido, user_id=usuario_actual)
        form = miUsuarioExtFormModificacion(request.POST, instance=usuario)
        if form.is_valid():            
            form.save()
            usuarios = usuarioExtendido.objects.all()
            estado = 'Modificado'
            mensaje = 'Usuario  ' + str(usuario.id)+' ' + estado + ' con exito.'
            return render(request, 'consulta_usuarios.html', {
            'usuarios': usuarios, 'mensaje': mensaje
        })

        else:
            print(form.errors)           
            return render(request, 'modificar_usuario.html', {
                'form': form, 'usuario': usuario, 'documentos': documentos, 'areas': areas
        })

@login_required        
def modificar_solicitud_completa(request, tipo_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
        form = tSolicitudFormModificacionAll(instance=solicitud)
        return render(request, 'modificar_solicitud_total.html', {
            'solicitud': solicitud, 'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
            form = tSolicitudFormModificacionAll(request.POST, instance=solicitud)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            estado = 'Modificado'
            mensaje = 'Número radicado  ' + str(solicitud.id)+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            solicitudes = tSolicitud.objects.all()
            return render(request, 'consulta_solicitudes.html', {
                'mensaje': mensaje,
                'solicitudes': solicitudes  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            print(form.errors)
            return render(request, 'consulta_solicitudes.html', {
                'solicitudes': solicitudes, 'form': form,
                'error': 'Error al actualizar tipos de documento'
            })
@login_required
def modificar_solicitud_usuario(request, tipo_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
        form = tSolicitudFormAsignacionUsuario(instance=solicitud)
        return render(request, 'modificar_usuario_solicitud.html', {
            'solicitud': solicitud, 'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
            form = tSolicitudFormAsignacionUsuario(request.POST, instance=solicitud)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            estado = 'Modificado'
            mensaje = 'Número radicado  ' + str(solicitud.id)+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            solicitudes = tSolicitud.objects.all()
            return render(request, 'consulta_solicitudes.html', {
                'mensaje': mensaje,
                'solicitudes': solicitudes  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            print(form.errors)
            return render(request, 'consulta_solicitudes.html', {
                'solicitudes': solicitudes, 'form': form,
                'error': 'Error al actualizar tipos de documento'
            })

def asignar_usuario_aleatorio(area_id):
    # Obtén el objeto tArea correspondiente al id dado
    area = get_object_or_404(tArea, id=area_id)

    # Obtén todos los usuarios asociados a esa área
    usuarios = usuarioExtendido.objects.filter(id_area=area)

    # Si no hay usuarios, devuelve None
    if not usuarios.exists():
        return None

    # Elige un usuario aleatorio
    usuario_aleatorio = random.choice(usuarios)

    return usuario_aleatorio.user

def editar_solicitud_area_tipo(request, tipo_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
        form = tSolicitudFormModificacionAreaTipo(instance=solicitud)
        return render(request, 'modificar_area_tipo.html', {
            'solicitud': solicitud, 'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
            form = tSolicitudFormModificacionAreaTipo(request.POST, instance=solicitud)
            if form.is_valid():
                nueva_solicitud = form.save(commit=False)
                # Obtener el Id del area para despues ejecutar la función asignar solicitud, para asignar el usuario.
                id_area=request.POST['id_area']
                usuario = asignar_usuario_aleatorio(id_area)
                nueva_solicitud.id_usuario = usuario

                #Cambia el estado de la solicitud a Area Asignada.    
                id_estado_solicitud = 5
                tipo_solicitud = get_object_or_404(tEstado_solicitud, pk=id_estado_solicitud)
                nueva_solicitud.id_estado_solicitud = tipo_solicitud    

                nueva_solicitud.save()
            else:
                print(form.errors)
            estado = 'Clasificado'
            mensaje = 'Número radicado  ' + str(solicitud.id)+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            solicitudes = tSolicitud.objects.all()
            return render(request, 'consulta_solicitudes.html', {
                'mensaje': mensaje,
                'solicitudes': solicitudes  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            print(form.errors)
            return render(request, 'consulta_solicitudes.html', {
                'mensaje': form.errors, 'form': form,
                'error': 'Error al actualizar tipos de documento'
            })

def responder_solicitud(request, tipo_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
        form = tSolicitudFormRespuesta(instance=solicitud)
        return render(request, 'responder_solicitud.html', {
            'solicitud': solicitud, 'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(tSolicitud, pk=tipo_id)
            form = tSolicitudFormRespuesta(request.POST, request.FILES, instance=solicitud)
            if form.is_valid():

                nueva_solicitud = form.save(commit=False)
                nombre_archivo_original = nueva_solicitud.archivo_respuesta.name
                nombre_archivo_cambiado = cambiar_nombre_archivo(nombre_archivo_original)
                nueva_solicitud.archivo_respuesta.name = nombre_archivo_cambiado
                
                # Establecer la fecha de cierre a la fecha actual
                nueva_solicitud.fecha_de_cierre = datetime.now(pytz.UTC)
                
                # Establecer id_esta_activo a 2
                estado_activo = get_object_or_404(tEstado_Activo, pk=2)
                nueva_solicitud.id_esta_activo = estado_activo
                estado_solicitud_1 = get_object_or_404(tEstado_solicitud, pk=7)
                estado_solicitud_2 = get_object_or_404(tEstado_solicitud, pk=8)
                
                # Establecer id_estado_solicitud basado en la condición
                if datetime.now(pytz.UTC) <= nueva_solicitud.fecha_de_respuesta_oportuna:
                    nueva_solicitud.id_estado_solicitud = estado_solicitud_1
                else:
                    nueva_solicitud.id_estado_solicitud = estado_solicitud_2
                
                nueva_solicitud.save()

                correo_respuesta_solicitud(tipo_id)

            else:
                print(form.errors)
            estado = 'Respondido'
            mensaje = 'Número radicado  ' + str(solicitud.id)+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            solicitudes = tSolicitud.objects.all()

            return render(request, 'consulta_solicitudes.html', {
                'mensaje': mensaje,
                'solicitudes': solicitudes  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            print(form.errors)
            return render(request, 'consulta_solicitudes.html', {
                'solicitudes': solicitudes, 'form': form,
                'error': 'Error al actualizar tipos de documento'
            })

def modificar_tipo_documento(request, tipo_id):
    if request.method == 'GET':
        tipo_documento = get_object_or_404(tTipe_document, pk=tipo_id)
        form = tDocumentoForm(instance=tipo_documento)
        return render(request, 'modificar_tipos_documento.html', {
            'tipo_documento': tipo_documento, 'form': form
        })
    else:
        try:
            tipo_documento = get_object_or_404(tTipe_document, pk=tipo_id)
            form = tDocumentoForm(request.POST, instance=tipo_documento)
            form.save()
            estado = 'Modificado'
            mensaje = 'Tipo documento ' + tipo_documento.nombre_tipo+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            tipos_documento = tTipe_document.objects.all()

            return render(request, 'consulta_tipos_documento.html', {
                'mensaje': mensaje,
                'tipos_documento': tipos_documento  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            return render(request, 'modificar_tipos_documento.html', {
                'tipo_documento': tipo_documento, 'form': form,
                'error': 'Error al actualizar tipos de documento'
            })


def modificar_tipo_solicitud(request, tipo_id):
    if request.method == 'GET':
        tipo_solictud = get_object_or_404(tTipo_solicitud, pk=tipo_id)
        form = tTipoSForm(instance=tipo_solictud)
        return render(request, 'modificiar_tipos_solicitud.html', {
            'tipo_solictud': tipo_solictud, 'form': form
        })
    else:
        try:
            tipo_solictud = get_object_or_404(tTipo_solicitud, pk=tipo_id)
            form = tTipoSForm(request.POST, instance=tipo_solictud)
            form.save()
            estado = 'modificada'
            mensaje = 'Tipo de solicitud ' + tipo_solictud.nombre_solicitud+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            tipos_solicitudes = tTipo_solicitud.objects.all()

            return render(request, 'consulta_tipos_solicitudes.html', {
                'mensaje': mensaje,
                'tipos_solicitudes': tipos_solicitudes  # Pasa los usuarios a la plantilla
            })    
        except ValueError:
            return render(request, 'modificiar_tipos_solicitud.html', {
                'tipo_solictud': tipo_solictud, 'form': form,
                'error': 'Error actualizar tipos de documento'
            })


def modificar_area(request, area_id):
    if request.method == 'GET':
        area = get_object_or_404(tArea, pk=area_id)
        form = tAreaForm(instance=area)
        return render(request, 'modificar_area.html', {
            'area': area, 'form': form
        })
    else:
        try:
            area = get_object_or_404(tArea, pk=area_id)
            form = tAreaForm(request.POST, instance=area)
            form.save()
            estado = 'modificada'
            mensaje = 'Area o departamento ' + area.nombre_area+' ' + estado + ' con exito.'
            # Vuelve a consultar el modelo
            areas = tArea.objects.all()

            return render(request, 'consulta_area.html', {
                'mensaje': mensaje,
                'areas': areas  # Pasa los usuarios a la plantilla
            })
        except ValueError:
            return render(request, 'modificar_area.html', {
                'area': area, 'form': form,
                'error': 'Error actualizar tipos de documento'
            })


# --------------------------------- Función de cierre de sesión ---------------------------------------


def signout(request):
    logout(request)
    return redirect('creaSolicitud')


def generar_nombre_unico(nombre):
    nombre_base, extension = os.path.splitext(nombre)
    return f"{nombre_base}_{uuid.uuid4().hex}{extension}"


def cambiar_nombre_archivo(nombre_archivo_original):
    # Obtener la extensión del archivo original
    extension = nombre_archivo_original.split('.')[-1]
    # Generar un nuevo nombre de archivo con uuid4
    nombre_limpio = f"{uuid.uuid4().hex[:10]}.{extension}"
    return nombre_limpio



def dividir_nombre_carpetaYarchivo(nombre_archivo):
    # Obtener el nombre de archivo sin la extensión
    nombre_archivo_tex = nombre_archivo
    nombre_pdf = nombre_archivo_tex
    partes_nombre = nombre_archivo_tex.split('.')
    if len(partes_nombre) > 1:
        nombre_carpeta = partes_nombre[0]
    else:
        nombre_carpeta = nombre_archivo
    crear_carpeta_nombre_pdf(nombre_carpeta, nombre_pdf)


def crear_carpeta_nombre_pdf(nombre_carpeta, nombre_pdf):
    # Ruta de la nueva carpeta
    ruta_nueva_carpeta = os.path.join('pdfs', nombre_carpeta)
    # Verificar si la carpeta ya existe
    if not os.path.exists(ruta_nueva_carpeta):
        # Crear la carpeta
        os.makedirs(ruta_nueva_carpeta)
        convertir_pdf_a_imagen(nombre_pdf, nombre_carpeta)


def convertir_pdf_a_imagen(nombre_pdf, nombre_carpeta):
    # Construir las rutas del archivo y de la carpeta de salida
    ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(ruta_proyecto, 'pdfs', nombre_pdf)
    output_folder = os.path.join(ruta_proyecto, 'pdfs', nombre_carpeta)

    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Convertir el PDF en una lista de imágenes
    images = convert_from_path(pdf_path)

    # Guardar cada imagen en la carpeta de salida
    for i, image in enumerate(images):
        image.save(f'{output_folder}/output_{i}.png', 'PNG')

    print(output_folder)

    extraer_texto_imagenes(output_folder)

# C:\Program Files\Tesseract-OCR
def extraer_texto_imagenes(carpeta_imagenes):
    # Obtener una lista de todas las imágenes en la carpeta
    nombres_imagenes = os.listdir(carpeta_imagenes)

    # Crear un archivo de texto para almacenar el texto extraído
    ruta_archivo = os.path.join(
        'pdfs', carpeta_imagenes, carpeta_imagenes + '.txt')
    with open(ruta_archivo, 'w') as f:
        # Recorrer todas las imágenes
        for nombre_imagen in nombres_imagenes:
            # Abrir la imagen
            imagen = Image.open(os.path.join(carpeta_imagenes, nombre_imagen))

            # Extraer el texto de la imagen con Tesseract
            texto = pytesseract.image_to_string(imagen, lang='spa')
            texto = limpiar_texto(texto)

            # Escribir el texto en el archivo
            f.write(texto + '\n\n')
    # Eliminar la carpeta
    shutil.rmtree(carpeta_imagenes)

def limpiar_texto(texto):
    # Elimina las etiquetas HTML
    soup = BeautifulSoup(texto, "html.parser")
    texto = soup.get_text(separator=" ")

    # Convierte el texto a minúsculas
    texto = texto.lower()

    # Elimina los caracteres extraños
    texto = re.sub(r'[^a-záéíóúñü \n]', '', texto)

    # Elimina los espacios extra
    texto = re.sub(r' +', ' ', texto)
    texto = texto.strip()
    return texto


# --------------------------------- Lector de PDF solicitudes ---------------------------------------


def pdf_view(request, nombre_del_pdf):
    ruta_archivos = 'pdfs'
    ruta_completa = os.path.join(ruta_archivos, nombre_del_pdf)
    print(ruta_archivos)
    with open(ruta_completa, 'rb') as pdf:
        pdf_data = pdf.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={nombre_del_pdf}'
    return response



# --------------------------------- Lector de PDF respuestas ---------------------------------------

def pdf_view_res(request, nombre_del_pdf):
    ruta_archivos = 'respuestas'
    ruta_completa = os.path.join(ruta_archivos, nombre_del_pdf)
    with open(ruta_completa, 'rb') as pdf:
        pdf_data = pdf.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={nombre_del_pdf}'
    return response

# --------------------------------- Funciones de IA ---------------------------------------
# Crear una función que mantenga los 3 estados principales de IA (En proceso de clasificación,Clasificación manual,Clasificada)


def preparar_IA(ultimo_id):
    ultimo_objeto_almacenado = tSolicitud.objects.get(id=ultimo_id)
    # Obtener la instancia de tEstado_solicitud que quieres asignar
    estado_solicitud = tEstado_solicitud.objects.get(id=2)  # Reemplaza '2' con el ID que quieras
    # Cambiar el id_estado_solicitud del último objeto guardado
    ultimo_objeto_almacenado.id_estado_solicitud = estado_solicitud
    ultimo_objeto_almacenado.save()   

def ejecutar_IA_Tipo_Solicitud(asunto):
    modelo_svc = joblib.load('modelosIA/modelo_entrenado5.pkl')
    vectorizador_tfidf = joblib.load('modelosIA/vectorizador_tfidf5.pkl')
    texto_nuevo = [asunto]
    # Supongamos que 'datos_entrada' son tus datos de entrada
    prediccion = modelo_svc.predict(vectorizador_tfidf.transform(texto_nuevo))
    probabilidades = modelo_svc.predict_proba(vectorizador_tfidf.transform(texto_nuevo)) 
    
    # Obtener la clase con la mayor probabilidad
    clase_predicha = probabilidades.argmax()
    max_probabilidad = probabilidades[0][clase_predicha]

    # Verificar si la probabilidad máxima es menor que 0.8
    if max_probabilidad < 0.80:
        print(probabilidades)
        return 0   

    else:
        # Supongamos que 'le' es tu LabelEncoder que usaste para codificar las categorías
        le = LabelEncoder()
        tus_categorias = [1, 2]
        # Ajustar el LabelEncoder a tus categorías
        le.fit(tus_categorias)
        # Obtener la categoría original
        categoria_predicha = le.inverse_transform([clase_predicha])
        print(probabilidades)
        return categoria_predicha
  


def entrenar_IA(request):

    # Obteniendo los datos del modelo
    qs = tSolicitud.objects.filter(id_esta_activo=2)
    df = read_frame(qs)

    # Seleccionando las columnas que se usarán para el entrenamiento
    X = df['asunto']
    y = df['id_tipo_solicitud']

    # Dividiendo los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Ruta al archivo de texto con las stopwords en español
    file_path = os.path.join(settings.BASE_DIR, r'C:\Users\Trabajo\Desktop\Proyecto-Grado\spanish.txt')
    with open(file_path, "r", encoding="utf-8") as file:
        spanish_stop_words = file.read()
    # Crea el arreglo con las stopwords
    spanish_stop_words = spanish_stop_words.split('\\n')
    
    #spanish_stop_words = read_stopwords_from_file(archivo_stopwords)   
        
    # Normalizando los datos
    tfidf = TfidfVectorizer(stop_words=spanish_stop_words)
    X_train = tfidf.fit_transform(X_train)
    X_test = tfidf.transform(X_test)

    # Entrenando el modelo SVC
    model = SVC(kernel='linear', random_state=42 , probability=True)
    model.fit(X_train, y_train)

    # Haciendo predicciones
    y_pred = model.predict(X_test)

    # Evaluando el modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy*100}%')

    # Definiendo los parámetros para GridSearchCV
    paremetros = {'C':[1,4,8,16,32], 'kernel':['linear', 'rbf'], 'probability':[True]}

    # Creando el modelo SVC
    svc = SVC()

    # Creando GridSearchCV
    svc_grid = GridSearchCV(svc, paremetros, cv=4)
    # Primero, necesitamos convertir el texto en vectores utilizando TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words=spanish_stop_words)
    train_x_vector = X_train

    # Ahora, podemos ajustar el modelo
    svc_grid.fit(train_x_vector, y_train)

    # Guarda el modelo en un archivo
    ruta_modelo = os.path.join(settings.STATIC_URL, 'modelo_entrenado.pkl')
    joblib.dump(svc_grid, ruta_modelo)

def read_stopwords_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            stopwords_list = [line.strip() for line in file]
        return stopwords_list
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")
        return []
    
# --------------------------------- Funciones de configuración de Correo ---------------------------------------

def editar_configuracion_correo(request):
    config = configuracion_correo.objects.first()
    if config is None:
        config = configuracion_correo.objects.create(
            email_backend = '',
            email_host = '',
            email_port = 0,
            email_host_user = '',
            email_host_password = '',
            email_use_tls = True,
        )  # Crea una nueva instancia

    if request.method == 'POST':
        form = configuracionCorreoForm(request.POST, instance=config)
        if form.is_valid():
            form.save()

            confirmacion = 'Su Configuración Ha Sido Actualizada'
            return render(request, 'editar_configuracion_correo.html', {'form': form,'confirmacion':confirmacion})
    else:
        form = configuracionCorreoForm(instance=config)

    return render(request, 'editar_configuracion_correo.html', {'form': form})


