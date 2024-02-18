from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime

from django.db.models.fields import BLANK_CHOICE_DASH

LOGIN_TYPE_CHOICES = (
    ('normal', 'normal'),
    ('facebook', 'facebook'),
    ('apple', 'apple')
)

DISTRICT_CHOICES = (
    ('Lombardy', 'Lombardy'),
    ('Non Valley', 'Non Valley'),
    ('Molo', 'Molo'),
    ('Florence', 'FLorence'),
    ('Aurora', 'Aurora'),
    ('Turro', 'Turro'),
    ('Noto', 'Noto'),
    ('Albaredo per San Marco', 'Albaredo per San Marco'),
    ('Capitoline Hill', 'Capitoline Hill'),
    ('Cannaregio', 'Cannaregio'),
    ('Milano', 'Milano'),
    ('Trentino', 'Trentino'),
    ('Roma', 'Roma'),
    ('Venezia', 'Venezia'),
    ('Agrigento', 'Agrigento'),
    ('Alessandria', 'Alessandria'),
    ('Ancona', 'Ancona'),
    ('Aosta', 'Aosta'),
    ("L'Aquila", "L'Aquila"),
    ('Arezzo', 'Arezzo'),
    ('Ascoli-Piceno', 'Ascoli-Piceno'),
    ('Asti', 'Asti'),
    ('Avellino', 'Avellino'),
    ('Bari', 'Bari'),
    ('Barletta-Andria-Trani', 'Barletta-Andria-Trani'),
    ('Belluno', 'Belluno'),
    ('Benevento', 'Benevento'),
    ('Bergamo', 'Bergamo'),
    ('Biella', 'Biella'),
    ('Bologna', 'Bologna'),
    ('Bolzano', 'Bolzano'),
    ('Brescia', 'Brescia'),
    ('Brindisi', 'Brindisi'),
    ('Cagliari', 'Cagliari'),
    ('Caltanissetta', 'Caltanissetta'),
    ('Campobasso', 'Campobasso'),
    ('Carbonia Iglesias', 'Carbonia Iglesias'),
    ('Caserta', 'Caserta'),
    ('Catania', 'Catania'),
    ('Catanzaro', 'Catanzaro'),
    ('Chieti', 'Chieti'),
    ('Como', 'Como'),
    ('Cosenza', 'Cosenza'),
    ('Cremona', 'Cremona'),
    ('Crotone', 'Crotone'),
    ('Cuneo', 'Cuneo'),
    ('Enna', 'Enna'),
    ('Fermo', 'Fermo'),
    ('Ferrara', 'Ferrara'),
    ('Firenze', 'Firenze'),
    ('Foggia', 'Foggia'),
    ('Forli-Cesena', 'Forli-Cesena'),
    ('Frosinone', 'Frosinone'),
    ('Genova', 'Genova'),
    ('Gorizia', 'Gorizia'),
    ('Grosseto', 'Grosseto'),
    ('Imperia', 'Imperia'),
    ('Isernia', 'Isernia'),
    ('La-Spezia', 'La-Spezia'),
    ('Latina', 'Latina'),
    ('Lecce', 'Lecce'),
    ('Lecco', 'Lecco'),
    ('Livorno', 'Livorno'),
    ('Lodi', 'Lodi'),
    ('Lucca', 'Lucca'),
    ('Macerata', 'Macerata'),
    ('Mantova', 'Mantova'),
    ('Massa-Carrara', 'Massa-Carrara'),
    ('Matera', 'Matera'),
    ('Medio Campidano', 'Medio Campidano'),
    ('Messina', 'Messina'),
    ('Modena', 'Modena'),
    ('Monza-Brianza', 'Monza-Brianza'),
    ('Napoli', 'Firenze'),
    ('Novara', 'Novara'),
    ('Nuoro', 'Nuoro'),
    ('Ogliastra', 'Ogliastra'),
    ('Olbia Tempio', 'Olbia Tempio'),
    ('Padova', 'Padova'),
    ('Novara', 'Novara'),
    ('Palermo', 'Palermo'),
    ('Parma', 'Parma'),
    ('Pavia', 'Pavia'),
    ('Perugia', 'Perugia'),
    ('Pesaro-Urbino', 'Pesaro-Urbino'),
    ('Pescara', 'Pescara'),
    ('Piacenza', 'Piacenza'),
    ('Pisa', 'Pisa'),
    ('Pistoia', 'Pistoia'),
    ('Ravenna', 'Ravenna'),
    ('Reggio-Calabria', 'Reggio-Calabria'),
    ('Reggio-Emilia', 'Reggio-Emilia'),
    ('Rieti', 'Rieti'),
    ('Rimini', 'Rimini'),
    ('Rovigo', 'Rovigo'),
    ('Pistoia', 'Pistoia'),
    ('Salerno', 'Salerno'),
    ('Sassari', 'Sassari'),
    ('Savona', 'Savona'),
    ('Siena', 'Siena'),
    ('Siracusa', 'Siracusa'),
    ('Sondrio', 'Sondrio'),
    ('Taranto', 'Taranto'),
    ('Terni', 'Terni'),
    ('Torino', 'Torino'),
    ('Trapani', 'Trapani'),
    ('Trento', 'Trento'),
    ('Treviso', 'Treviso'),
    ('Trieste', 'Trieste'),
    ('Udine', 'Udine'),
    ('Varese', 'Varese'),
    ('Verbania', 'Verbania'),
    ('Vercelli', 'Vercelli'),
    ('Verona', 'Verona'),
    ('Vibo-Valentia', 'Vibo-Valentia'),
    ('Vicenza', 'Vicenza'),
    ('Viterbo', 'Viterbo')
)

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Email is Required')
        if not first_name:
            raise ValueError('First Name is Required')
        if not last_name:
            raise ValueError('Last Name is Required')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
            )
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    login_type = models.CharField(max_length=20, choices=LOGIN_TYPE_CHOICES, default='normal')
    facebook_id = models.CharField(max_length=50, blank=True, null=True)
    apple_id = models.IntegerField(blank=True, null=True)
    email = models.EmailField(verbose_name='Email Address', max_length=60, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=30, choices=DISTRICT_CHOICES, blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def username(self):
        return self.first_name + ' ' + self.last_name


CODE_CHOICES = (
    ('Register', 'Register'),
    ('Forgot', 'Forgot'),
)

class Code(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=4)
    usage = models.CharField(max_length=20, choices=CODE_CHOICES, default='Register')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def email(self):
        return self.user.email