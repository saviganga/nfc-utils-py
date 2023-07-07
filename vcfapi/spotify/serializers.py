from rest_framework import serializers
from spotify import models as spotify_models


class DummySerializer(serializers.ModelSerializer):

    class Meta:
        model = spotify_models.DummyDB
        fields = '__all__'

