"""
URL configuration for proyectogrado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/create', views.create_task, name="create_task"),

    path('logout/', views.signout, name="logout"),
    path('signin/', views.singnin, name="signin"),
    path('creaUsuario/', views.crearUsuario, name="creaUsuario"),
    path('consultarUsuario/', views.consulta_usuario, name="consultarUsuario"),
    path('activar_desactivar_usuario/<int:usuario_id>', views.activar_desactivar_usuario, name="activar_desactivar_usuario"),
    path('restabler_contrasena/<int:usuario_id>', views.restabler_contrasena, name="restabler_contrasena"),
    path('modificar_usuario/<int:usuario_id>', views.modificar_usuario, name="modificar_usuario"),
    path('modificar_mi_usuario/', views.modificar_mi_usuario, name="modificar_mi_usuario"),

    path('creaTdocumento/', views.creaTdocumento, name="creaTdocumento"),
    path('tiposDocumento/', views.consulta_tipoDocumento, name="tiposDocumento"),
    path('tiposDocumento/<int:tipo_id>/', views.modificar_tipo_documento, name="modificarDocumento"),
    path('activar_desactivar_tipo_documento/<int:tipod_id>', views.activar_desactivar_tipo_documento, name="activar_desactivar_tipo_documento"),

    path('creaTsolicitud/', views.creaTipoSolicitud, name="creaTsolicitud"),
    path('tiposSolicitudes/', views.consulta_tipoSolicitud, name="tiposSolicitudes"),
    path('tiposSolicitudes/<int:tipo_id>', views.modificar_tipo_solicitud, name="modificartipoSolicitud"),
    path('activar_desactivar_tipo_solicitud/<int:tipod_id>', views.activar_desactivar_tipo_solicitud, name="activar_desactivar_tipo_solicitud"), 

    path('creaTarea/', views.creaTarea, name="creaTarea"),
    path('areas/', views.consulta_area, name="areas"),
    path('areas/<int:area_id>', views.modificar_area, name="ModificarArea"),    
    path('activar_desactivar_area/<int:area_id>', views.activar_desactivar_area, name="activar_desactivar_area"),
    
    path('CrearActivo/', views.CrearActivo, name="CrearActivo"),
    path('creaEstadoS/', views.creaEstadoS, name="creaEstadoS"),
    path('creaEstadoU/', views.creaEstadoU, name="creaEstadoU"),
    #path('', views.test, name="test"),

    path('', views.creaSolicitud, name="creaSolicitud"),
    path('consultarRadicado/', views.consultar_radicados, name="consultar_radicados"),

    path('consulta_solicitudes_sin_clasificar/', views.consulta_solicitudes_sin_clasificar, name="consulta_solicitudes_sin_clasificar"),
    path('editar_solicitud_area_tipo/<int:tipo_id>', views.editar_solicitud_area_tipo, name="editar_solicitud_area_tipo"),

    path('consultarSolicitud/', views.consulta_solicitudes, name="consultarSolicitud"),
    path('consulta_solicitudes_cerradas/', views.consulta_solicitudes_cerradas, name="consulta_solicitudes_cerradas"),
    path('consulta_solicitudes_abiertas/', views.consulta_solicitudes_abiertas, name="consulta_solicitudes_abiertas"),
    path('consulta_mis_solicitudes/', views.consulta_mis_solicitudes, name="consulta_mis_solicitudes"),
    path('consulta_mis_solicitudes_abiertas/', views.consulta_mis_solicitudes_abiertas, name="consulta_mis_solicitudes_abiertas"),
    path('consulta_mis_solicitudes_cerradas/', views.consulta_mis_solicitudes_cerradas, name="consulta_mis_solicitudes_cerradas"),
    path('consulta_solicitudes_del_area/', views.consulta_solicitudes_del_area, name="consulta_solicitudes_del_area"),
    path('responder_solicitud/<int:tipo_id>', views.responder_solicitud, name="responder_solicitud"), 
    
    path('modificar_solicitud_completa/<int:tipo_id>', views.modificar_solicitud_completa, name="modificar_solicitud_completa"),
    path('modificar_solicitud_usuario/<int:tipo_id>', views.modificar_solicitud_usuario, name="modificar_solicitud_usuario"),   
    

    path('pdfs/<str:nombre_del_pdf>/', views.pdf_view, name='pdf_view'),
    path('pdfs2/<str:nombre_del_pdf>/', views.pdf_view_res, name='pdf_view_res'),

    #IA
    path('ejecutar_IA/', views.ejecutar_IA_Tipo_Solicitud, name='ejecutar_IA'),

    
    
    

]
