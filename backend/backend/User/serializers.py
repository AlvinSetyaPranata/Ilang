from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


USER_MODEL = get_user_model()


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        model = self.Meta.model

        password = validated_data.pop("password")

        user = model.objects.create(**validated_data)

        user.set_password(password)
        user.save()    

        return user
