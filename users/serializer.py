from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address']
        


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address']