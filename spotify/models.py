from django.db import models


class SpotifyUser(models.Model):
    id = models.CharField(max_length=30, primary_key=True)

    class Meta:
        verbose_name_plural = "SpotifyUsers"
        verbose_name = "SpotifyUser"


class Token(models.Model):
    access_token = models.CharField(max_length=139)
    token_type = models.CharField(max_length=30)
    expiry_time = models.DateTimeField()


class Credential(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id)
