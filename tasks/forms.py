from django.forms import ModelForm
from django import forms
# se importa la BD de .models para usarla como from
from .models import tTipe_document
from .models import tArea
from .models import tEstado_solicitud
from .models import tSolicitud
from .models import tTipo_solicitud
from .models import tEstado_Activo
from .models import usuarioExtendido
from .models import tformatoSolicitud
from .models import configuracion_correo

# se importan los modelos necesario para extender el usuario(para no afectar el administrador de usuarios de django)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# mark_safe es una función de Django que marca una cadena como segura para su uso en HTML
from django.utils.safestring import mark_safe



class tDocumentoForm(ModelForm):
    class Meta:
        model = tTipe_document
        fields = ['nombre_tipo']
        widgets = {
            'nombre_tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre tipo de documento'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class tTipoSForm(ModelForm):
    class Meta:
        model = tTipo_solicitud
        fields = ['nombre_solicitud']
        widgets = {
            'nombre_solicitud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de solicitud'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class tAreaForm(ModelForm):
    class Meta:
        model = tArea
        fields = ['nombre_area']
        widgets = {
            'nombre_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del area o departamento'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class tEstadoActivoForm(ModelForm):
    class Meta:
        model = tEstado_Activo
        fields = ['esta_activo']


class tEstadoSForm(ModelForm):
    class Meta:
        model = tEstado_solicitud
        fields = ['nombre_tipoS']


class miUsuarioExtFormModificacion(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label="Correo")
    # UserExtend
    nombre_completo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label="Nombre Completo")
    
    class Meta:
        model = usuarioExtendido
        fields = ('email','nombre_completo')

    def save(self, commit=True):
        modelo1 = super().save(commit=False)
        id_user_modelo2 = modelo1.user_id
        modelo2, created = User.objects.get_or_create(pk=id_user_modelo2)  # Obtén la instancia existente de Modelo2 apartir del Modelo1

        # Actualiza los campos relevantes en ambas instancias
        modelo1.nombre_completo=self.cleaned_data['nombre_completo']

        modelo2.email = self.cleaned_data['email']

        if commit:
            modelo1.save()
            modelo2.save()

        return modelo1, modelo2
    
class usuarioExtFormModificacion(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}), label="Correo")
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label="Es Adminitrador?", help_text="Indica que este usuario tiene todos los permisos")
    # UserExtend
    nombre_completo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Joe Doe'}), label="Nombre Completo")
    cargo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Administrador'}), label="Cargo")
    id_documento = forms.ModelChoiceField(queryset=tTipe_document.objects.all(),
                                          empty_label="-------------",
                                          widget=forms.Select(
                                              attrs={'class': 'form-control'}),
                                          label="Tipo de Identificación"
                                          )
    numero_identificacion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}), label="Número de Identificación")
    id_area = forms.ModelChoiceField(queryset=tArea.objects.all(),
                                     empty_label="-------------",
                                     widget=forms.Select(
                                         attrs={'class': 'form-control'}),
                                     label="Area o Departamento")

    class Meta:
        model = usuarioExtendido
        fields = ('email','is_superuser','nombre_completo','cargo','id_documento','numero_identificacion','id_area')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_documento'].label_from_instance = lambda obj: f"{obj.nombre_tipo}" if obj else ""
        self.fields['id_area'].label_from_instance = lambda obj: f"{obj.nombre_area}" if obj else ""

    def save(self, commit=True):
        modelo1 = super().save(commit=False)
        id_user_modelo2 = modelo1.user_id
        modelo2, created = User.objects.get_or_create(pk=id_user_modelo2)  # Obtén la instancia existente de Modelo2 apartir del Modelo1

        # Actualiza los campos relevantes en ambas instancias

        modelo1.nombre_completo=self.cleaned_data['nombre_completo']
        modelo1.id_documento=self.cleaned_data['id_documento']
        modelo1.numero_identificacion=self.cleaned_data['numero_identificacion']
        modelo1.cargo=self.cleaned_data['cargo']
        modelo1.id_area=self.cleaned_data['id_area']

        modelo2.email = self.cleaned_data['email']
        modelo2.is_superuser = self.cleaned_data['is_superuser']

        if commit:
            modelo1.save()
            modelo2.save()

        return modelo1, modelo2

class usuarioExtForm(UserCreationForm):
    # User
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}), label="Nombre del usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}), label="Correo")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '***********'}), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '***********'}), label="Confirmar Contraseña")
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label="Es Adminitrador?", help_text="Indica que este usuario tiene todos los permisos")
    # UserExtend
    nombre_completo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Joe Doe'}), label="Nombre Completo")
    cargo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Administrador'}), label="Cargo")
    id_documento = forms.ModelChoiceField(queryset=tTipe_document.objects.all(),
                                          empty_label="-------------",
                                          widget=forms.Select(
                                              attrs={'class': 'form-control'}),
                                          label="Tipo de Identificación"
                                          )
    numero_identificacion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}), label="Número de Identificación")
    id_area = forms.ModelChoiceField(queryset=tArea.objects.all(),
                                     empty_label="-------------",
                                     widget=forms.Select(
                                         attrs={'class': 'form-control'}),
                                     label="Area o Departamento")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_documento'].label_from_instance = lambda obj: f"{obj.nombre_tipo}" if obj else ""
        self.fields['id_area'].label_from_instance = lambda obj: f"{obj.nombre_area}" if obj else ""

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        user_extend = usuarioExtendido.objects.create(user=user,
                                                      nombre_completo=self.cleaned_data['nombre_completo'],
                                                      id_documento=self.cleaned_data['id_documento'],
                                                      numero_identificacion=self.cleaned_data[
                                                          'numero_identificacion'],
                                                      cargo=self.cleaned_data['cargo'],
                                                      id_area=self.cleaned_data['id_area'])
        return user, user_extend


class tSolicitudFormRespuesta(ModelForm):    

    class Meta:
        model = tSolicitud
        fields = ['archivo_respuesta']
        widgets = {
            'archivo_respuesta': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }

class tSolicitudFormAsignacionUsuario(ModelForm):

    id_tipo_solicitud = forms.ModelChoiceField(
        queryset=tTipo_solicitud.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
        label="Seleccione el tipo de solicitud"
    )
    id_area = forms.ModelChoiceField(
        queryset=tArea.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control','onchange': 'toggleFields()','readonly': 'readonly'}),
        label="Seleccione el area o departamento"
    )
    id_usuario = forms.ModelChoiceField(
        queryset=usuarioExtendido.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control','onchange': 'toggleFields()'}),
        label="Seleccione el usuario"
    )

    class Meta:
        model = tSolicitud
        fields = ['asunto','id_tipo_solicitud','id_area','id_usuario']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John','readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tipo_solicitud'].label_from_instance = lambda obj: f"{obj.nombre_solicitud}" if obj else ""
        self.fields['id_area'].label_from_instance = lambda obj: f"{obj.nombre_area}" if obj else ""
        if self.instance.id_area:
            self.fields['id_usuario'].queryset = User.objects.filter(usuarioextendido__id_area=self.instance.id_area)

class tSolicitudFormModificacionAll(ModelForm):

    id_tipo_identificacion = forms.ModelChoiceField(
        queryset=tTipe_document.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de identificación"
    )

    class Meta:
        model = tSolicitud
        fields = ['nombre', 'apellidos', 'id_tipo_identificacion', 'numero_identificacion',
                  'correo', 'telefono', 'asunto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3101234567'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Derecho de Petición, Tutela etc.'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tipo_identificacion'].label_from_instance = lambda obj: f"{obj.nombre_tipo}" if obj else ""



class tSolicitudFormModificacionAreaTipo(ModelForm):

    id_tipo_solicitud = forms.ModelChoiceField(
        queryset=tTipo_solicitud.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Seleccione el tipo de solicitud"
    )
    id_area = forms.ModelChoiceField(
        queryset=tArea.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control',
                                   'required': True,
                                   'onchange': 'toggleFields()',
                                   }),
        label="Seleccione el area o departamento"
    )

    class Meta:
        model = tSolicitud
        fields = ['id_tipo_solicitud', 'id_area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tipo_solicitud'].label_from_instance = lambda obj: f"{obj.nombre_solicitud}" if obj else ""
        self.fields['id_area'].label_from_instance = lambda obj: f"{obj.nombre_area}" if obj else ""
        
class tSolicitudForm(ModelForm):
    politica_privacidad = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label=mark_safe("Acepto los <a href='https://universitariadecolombia.edu.co/politica-privacidad/' target='_blank'>términos y condiciones</a>."), help_text="Indica que este usuario tiene todos los permisos")
    
    id_tipo_identificacion = forms.ModelChoiceField(
        queryset=tTipe_document.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de identificación"
    )
    id_nombre_formato = forms.ModelChoiceField(
        queryset=tformatoSolicitud.objects.all(),
        empty_label="-------------",
        widget=forms.Select(attrs={'class': 'form-control',
                                   'required': True,
                                   'onchange': 'toggleFields()',
                                   }),
        label="Por favor, elija el modo en el que desea presentar su solicitud"
    )

    class Meta:
        model = tSolicitud
        fields = ['nombre', 'apellidos', 'id_tipo_identificacion', 'numero_identificacion',
                  'correo', 'telefono', 'asunto', 'id_nombre_formato', 'mensaje', 'archivo','politica_privacidad']
        
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3101234567'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Derecho de Petición, Tutela etc.'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tipo_identificacion'].label_from_instance = lambda obj: f"{obj.nombre_tipo}" if obj else ""
        self.fields['id_nombre_formato'].label_from_instance = lambda obj: f"{obj.nombre_formato}" if obj else ""
        self.fields['mensaje'].required = False
        self.fields['archivo'].required = False


class ConsultarRadicadosForm(forms.Form):
    numero_identificacion = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    

class configuracionCorreoForm(ModelForm):

    class Meta:
        model = configuracion_correo
        fields = ['email_backend', 'email_host','email_port','email_host_user','email_host_password','email_use_tls']

        widgets = {
            'email_backend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'django.core.mail.backends.smtp.EmailBackend'}),
            'email_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'smtp.gmail.com'}),
            'email_port': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}),
            'email_host_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'email_host_password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567891'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }