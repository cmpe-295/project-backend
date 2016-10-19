from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ("first_name", "last_name", "id", "sjsu_id")

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name
