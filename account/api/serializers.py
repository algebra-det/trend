from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework import exceptions

from account.models import MyUser

from trend import utils

districts = utils.get_districts_list()


# districts = ['Lombardy', 'Non Valley']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '').lower()
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_admin or user.is_superuser:
                    msg = "Impossibile accedere con queste credenziali"
                    raise exceptions.ValidationError(msg)
                else:
                    if user.is_active:
                        if user.is_verified:
                            data['user'] = user
                        else:
                            msg = "L'account non è verificato, verificalo prima!"
                            raise exceptions.ValidationError(msg)
                    else:
                        msg = "L'account non è attivato !"
                        raise exceptions.ValidationError(msg)
            else:
                msg = 'Credenziali errate!'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Both fields are required!'
            raise exceptions.ValidationError(msg)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'dob', 'city', 'province', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        dob = attrs.get('dob', '')
        city = attrs.get('city', '')
        province = attrs.get('province', '')

        if not first_name:
            raise serializers.ValidationError('First name field is required')
        if not email:
            raise serializers.ValidationError('Email field is required')
        if not last_name:
            raise serializers.ValidationError('Last name field is required')
        # if not dob:
        #     raise serializers.ValidationError('dob field is required')
        # if not city:
        #     raise serializers.ValidationError('city field is required')
        if not province:
            raise serializers.ValidationError('province field is required')
        if province not in districts:
            raise serializers.ValidationError('Please Choose province from the options!')

        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Questo indirizzo email esiste già!')

        attrs['email'] = email
        return attrs
    
    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            dob=self.validated_data.get('dob'),
            city=self.validated_data.get('city'),
            province=self.validated_data.get('province'),

        )
        password = self.validated_data['password']
        password1 = self.validated_data['password1']

        if password != password1:
            raise serializers.ValidationError({'password': 'Le password devono essere identiche.'})
        elif len(password) < 6:
            raise serializers.ValidationError({'password': 'La password deve contenere più di 6 cifre.'})
        account.set_password(password)
        account.is_staff = False
        account.is_verified = False
        account.save()
        return account




class FacebookRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['login_type', 'facebook_id', 'email', 'first_name', 'last_name', 'dob', 'city', 'province', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        login_type = attrs.get('login_type', '')
        facebook_id = attrs.get('facebook_id', '')
        email = attrs.get('email', '').lower()
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        dob = attrs.get('dob', '')
        city = attrs.get('city', '')
        province = attrs.get('province', '')

        if not login_type:
            raise serializers.ValidationError('login_type field is required')
        if not facebook_id:
            raise serializers.ValidationError('facebook_id field is required')
        if not int(facebook_id):
            raise serializers.ValidationError('facebook_id field must be an integer')
        if not first_name:
            raise serializers.ValidationError('First name field is required')
        if not email:
            raise serializers.ValidationError('Email field is required')
        if not last_name:
            raise serializers.ValidationError('Last name field is required')
        # if not dob:
        #     raise serializers.ValidationError('dob field is required')
        # if not city:
        #     raise serializers.ValidationError('city field is required')
        if province and province not in districts:
            raise serializers.ValidationError('Please Choose province from the options!')

        if login_type != 'facebook':
            raise serializers.ValidationError('login_type not available')

        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Questo indirizzo email esiste già!')
        
        if MyUser.objects.filter(facebook_id=facebook_id).exists():
            raise serializers.ValidationError('Questo ID Facebook esiste già!')

        attrs['email'] = email
        return attrs
    
    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            province=self.validated_data.get('province'),
            facebook_id=self.validated_data['facebook_id']

        )
        password = self.validated_data['password']
        password1 = self.validated_data['password1']

        if password != password1:
            raise serializers.ValidationError({'password': 'Le password devono essere identiche.'})
        elif len(password) < 6:
            raise serializers.ValidationError({'password': 'La password deve contenere più di 6 cifre.'})
        account.set_password(password)
        account.is_staff = False
        account.is_verified = True
        account.save()
        return account



class AppleRegisterSerializer(serializers.ModelSerializer):
    # password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['login_type', 'apple_id', 'email', 'first_name', 'last_name', 'dob', 'city', 'province']

    def validate(self, attrs):
        login_type = attrs.get('login_type', '')
        apple_id = attrs.get('apple_id', '')
        email = attrs.get('email', '').lower()
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        # dob = attrs.get('dob', '')
        # city = attrs.get('city', '')
        province = attrs.get('province', '')

        if not login_type:
            raise serializers.ValidationError('login_type field is required')
        if not apple_id:
            raise serializers.ValidationError('facebook_id field is required')
        if not int(apple_id):
            raise serializers.ValidationError('facebook_id field must be an integer')
        if not first_name:
            raise serializers.ValidationError('First name field is required')
        if not email:
            raise serializers.ValidationError('Email field is required')
        if not last_name:
            raise serializers.ValidationError('Last name field is required')
        # if not dob:
        #     raise serializers.ValidationError('dob field is required')
        # if not city:
        #     raise serializers.ValidationError('city field is required')
        # if not province:
        #     raise serializers.ValidationError('province field is required')
        if province and province not in districts:
            raise serializers.ValidationError('Please Choose province from the options!')

        if login_type != 'apple':
            raise serializers.ValidationError('login_type not available')

        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Questo indirizzo email esiste già!')
        
        if MyUser.objects.filter(apple_id=apple_id).exists():
            raise serializers.ValidationError('Questo ID Facebook esiste già!')

        attrs['email'] = email
        return attrs
    
    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            login_type='apple',
            dob=self.validated_data.get('dob'),
            city=self.validated_data.get('city'),
            province=self.validated_data.get('province'),
            apple_id=self.validated_data['apple_id']

        )
        account.set_password('SomePasswordForApple21')
        account.is_staff = False
        account.is_verified = True
        account.save()
        return account



class ChangePasswordSerializer(serializers.Serializer):
    # old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        fields = ['new_password', 'confirm_new_password']

    def validate(self, attrs):
        # old_password = attrs.get('old_password', '')
        new_password = attrs.get('new_password', '')
        confirm_new_password = attrs.get('confirm_new_password', '')

        # if not old_password:
        #     raise serializers.ValidationError({"old_password is required"})

        if not new_password:
            raise serializers.ValidationError({"new_password is required"})

        if not confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password is required"})

        if new_password!=confirm_new_password:
            raise serializers.ValidationError({"error": "Le password devono essere identiche"})

        if len(new_password) < 8:
            raise serializers.ValidationError({"error": "La password deve contenere più di 6 cifre"})
        
        return attrs
