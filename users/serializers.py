from rest_auth import serializers as auth_serializers
from users.models import User
from allauth.account.forms import ResetPasswordForm
from django.contrib.auth import password_validation
from rest_framework import serializers


class UserDetailsSerializer(auth_serializers.UserDetailsSerializer):

	class Meta:
		model = User
		fields = ('pk', 'email', 'phone')

	def validate_email(self, email):
		email = get_adapter().clean_email(email)
		if allauth_settings.UNIQUE_EMAIL:
			if email and email_address_exists(email):
				raise serializers.ValidationError(("A user is already registered with this e-mail address."))
		return email


class PasswordResetSerializer(auth_serializers.PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    password_reset_form_class = ResetPasswordForm


class RegisterSerializerCustom(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'password', 'email', 'first_name', 'last_name', 'phone')
		read_only_fields = ('id',)
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def validate_password(self, value):
		password_validation.validate_password(value, self.instance)
		return value

	def create(self, validated_data):
		user = User.objects.create(
			email=validated_data['email'],
			phone=validated_data['phone'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

		user.set_password(validated_data['password'])
		user.save()

		return user
