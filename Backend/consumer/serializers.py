from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model


class ConsumerSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
