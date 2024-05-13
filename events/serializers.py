from rest_framework import serializers
from events.models import formdata


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = formdata
        fields = '__all__'
