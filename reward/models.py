from django.db import models

# Create your models here.

def magic_box_directory_path(instance, filename):
    return 'magic_box/{}/{}'.format(instance.title, filename)

def trophy_directory_path(instance, filename):
    return 'trophies/{}/{}'.format(instance.title, filename)

class MagicBox(models.Model):
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=magic_box_directory_path)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Trophy(models.Model):
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=trophy_directory_path)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
