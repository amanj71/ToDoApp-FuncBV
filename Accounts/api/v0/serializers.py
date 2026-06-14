from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from ...models import MyUser


## Create your serializers here
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True) #add confirm pass fields to ensure user input data
    class Meta:
        model = MyUser
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        try:                                                 # this try - except block checks password compaxility
            validate_password(attrs.get('password')) 
        except exceptions.ValidationError as errors:
            raise serializers.ValidationError({'password': list(errors.messages)})

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'details': 'Password fields didn\'t match!'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return MyUser.objects.create_user(**validated_data)

class ResendActivationLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        user = get_object_or_404(MyUser, email=email)
        if user.is_active:
            raise serializers.ValidationError({'details': 'User ALREADY is Activate'})
        attrs['user'] = user  # pass user to data which are sent to view, for simpler user get in views 
        return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        print(self.context.get('request'))
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError("Your current password was entered incorrectly.")
        return value
    
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "New password fields didn't match."})
        
        # Prevent setting the new password to the exact same as the old password
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})

        # Run Django's built-in password strength validation
        # Pass the user instance so validators can check against user attributes (like username/email)
        try:
            validate_password(attrs.get('new_password'), user=self.context['request'].user)
        except serializers.ValidationError as errors:
            raise serializers.ValidationError({"new_password": list(errors.messages)})

        return attrs
    
    def save(self):
        user = self.context['request'].user
        # Set the new password (this automatically handles hashing)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
class SetLoginJWTSerializer(serializers.Serializer):
    email = serializers.CharField(help_text="User's email")
    password = serializers.CharField(help_text="User's password", write_only=True)

class ResetPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        try:                                                 # this try - except block checks password compaxility
            validate_password(attrs.get('password')) 
        except exceptions.ValidationError as errors:
            raise serializers.ValidationError({'password': list(errors.messages)})

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'details': 'Password fields didn\'t match!'})
        user = self.context.get('request')
        print(attrs)
        return attrs
