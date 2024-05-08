from rest_framework import serializers
from .models import tTipe_document

class projectSerealizer( serializers.ModelSerializer ):
    class Meta:
        model = tTipe_document
        fields = ('id','nombre_tipo')
        # campo solo para leer read_only_fields =
        #read_only_fields = ('created',)