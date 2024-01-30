from rest_framework import serializers

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext_lazy as _


class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('email'),
            password=attrs.get('password'),
        )

        if not user:
            msg = _("Unable to authenticate the provided credentials.")
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
