from django.db import models


class PlayerIdInfo(models.Model):
    source = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'player_id_infos'
