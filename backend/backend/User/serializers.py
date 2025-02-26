from django.contrib.auth import get_user_model
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, ReadOnlyField
# from rest_framework.exceptions import bad_request
from .models import Post


USER_MODEL = get_user_model()


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        model = self.Meta.model

        data = self.initial_data.dict()

        password = data.pop("password")


        if model.objects.filter(username=data["username"]):
            return None


        user = model.objects.create(**data)

        user.set_password(password)
        user.save()    

        return user


class PostsAddSerializers(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'id', 'last_login')


class PostUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'id')
        # read_only_fields = ('id',)


class PostsGetSerializers(ModelSerializer):
    user = PostUserSerializers()

    class Meta:
        model = Post
        exclude = ('founded',)
        read_only_fields = ('id',)


