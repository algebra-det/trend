from django.db import models
from account.models import MyUser
from reward.models import MagicBox, Trophy

DIFFICULTY_FIELDS = (
    ('easy', 'Facile'),
    ('medium', 'Media'),
    ('hard', 'Difficile'),
)

def game_directory_path(instance, filename):
    return 'games/{}/{}'.format(instance.title, filename)

def challenge_directory_path(instance, filename):
    return 'games/{}/challenge{}/{}'.format(instance.game.title, instance.title, filename)


def user_directory_game_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/profile/user_{0}/{1}/{2}'.format(instance.user.id, instance.challenge.title, filename)

def user_directory_promotion_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'games/{}/promotions/{}'.format(instance.game.title, filename)


GAME_CHOICES = (
    ('Classic', 'Classic'),
    ('Event', 'Event')
)

OBJECT_TYPE_CHOICES = (
    ('person', 'person'),
    ('bicycle', 'bicycle'),
    ('car', 'car'),
    ('motorcycle', 'motorcycle'),
    ('airplane', 'airplane'),
    ('bus', 'bus'),
    ('train', 'train'),
    ('truck', 'truck'),
    ('boat', 'boat'),
    ('traffic light', 'traffic light'),
    ('fire hydrant', 'fire hydrant'),
    ('stop sign', 'stop sign'),
    ('parking meter', 'parking meter'),
    ('bench', 'bench'),
    ('bird', 'bird'),
    ('cat', 'cat'),
    ('dog', 'dog'),
    ('horse', 'horse'),
    ('sheep', 'sheep'),
    ('cow', 'cow'),
    ('elephant', 'elephant'),
    ('bear', 'bear'),
    ('zebra', 'zebra'),
    ('giraffe', 'giraffe'),
    ('backpack', 'backpack'),
    ('umbrella', 'umbrella'),
    ('handbag', 'handbag'),
    ('tie', 'tie'),
    ('suitcase', 'suitcase'),
    ('frisbee', 'frisbee'),
    ('skis', 'skis'),
    ('snowboard', 'snowboard'),
    ('sports ball', 'sports ball'),
    ('kite', 'kite'),
    ('baseball bat', 'baseball bat'),
    ('baseball glove', 'baseball glove'),
    ('skateboard', 'skateboard'),
    ('surfboard', 'surfboard'),
    ('tennis racket', 'tennis racket'),
    ('bottle', 'bottle'),
    ('wine glass', 'wine glass'),
    ('cup', 'cup'),
    ('fork', 'fork'),
    ('knife', 'knife'),
    ('spoon', 'spoon'),
    ('bowl', 'bowl'),
    ('banana', 'banana'),
    ('apple', 'apple'),
    ('sandwich', 'sandwich'),
    ('orange', 'orange'),
    ('broccoli', 'broccoli'),
    ('carrot', 'carrot'),
    ('hot dog', 'hot dog'),
    ('pizza', 'pizza'),
    ('donut', 'donut'),
    ('cake', 'cake'),
    ('chair', 'chair'),
    ('couch', 'couch'),
    ('potted plant', 'potted plant'),
    ('bed', 'bed'),
    ('dining table', 'dining table'),
    ('toilet', 'toilet'),
    ('tv', 'tv'),
    ('laptop', 'laptop'),
    ('mouse', 'mouse'),
    ('remote', 'remote'),
    ('keyboard', 'keyboard'),
    ('cell phone', 'cell phone'),
    ('microwave', 'microwave'),
    ('oven', 'oven'),
    ('toaster', 'toaster'),
    ('sink', 'sink'),
    ('refrigerator', 'refrigerator'),
    ('book', 'book'),
    ('clock', 'clock'),
    ('vase', 'vase'),
    ('scissors', 'scissors'),
    ('teddy bear', 'teddy bear'),
    ('hair drier', 'hair drier'),
    ('toothbrush', 'toothbrush')
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

class Game(models.Model):
    title = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=30, choices=GAME_CHOICES, default='Classic')
    min_players = models.IntegerField(default=0)
    total_point = models.IntegerField()
    clue = models.TextField()
    province = models.CharField(max_length=30, choices=DISTRICT_CHOICES, blank=True, null=True)
    location_name = models.CharField(max_length=300)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    brief = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_FIELDS)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=False)
    image = models.ImageField(upload_to=game_directory_path)
    image1 = models.ImageField(upload_to=game_directory_path, null=True, blank=True)
    image2 = models.ImageField(upload_to=game_directory_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=game_directory_path, null=True, blank=True)
    rules_yes = models.TextField()
    rules_no = models.TextField()
    joined_players = models.ManyToManyField(MyUser, default=None, blank=True, related_name='joined_players')

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.title

    @property
    def challenges(self):
        return self.games.all()


class Challenge(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    location_name = models.CharField(max_length=300)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    object_type = models.CharField(max_length=30, choices=OBJECT_TYPE_CHOICES, null=True, blank=True)
    clue = models.TextField()
    hint = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    trophy = models.ForeignKey(Trophy, on_delete=models.SET_NULL, null=True, blank=True)
    magic_box = models.ForeignKey(MagicBox, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=challenge_directory_path)
    image1 = models.ImageField(upload_to=challenge_directory_path, blank=True)
    image2 = models.ImageField(upload_to=challenge_directory_path, blank=True)
    image3 = models.ImageField(upload_to=challenge_directory_path, blank=True)
    # Image and Object Detection

    def __str__(self):
        return self.title


class EventGame(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='eventgame')
    participants = models.ManyToManyField(MyUser, default=None, blank=True, related_name='participants')
    num_players = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.title

    @property
    def total_participants(self):
        return self.participants.all().count()

    # def game_id(self):
    #     return self.game.id


# class SubmitChallenge(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='submitchallenges')
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=user_directory_game_path)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '{} for {} in {} challenge'.format(self.user, self.game, self.challenge)


class Promotion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_promotion_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title