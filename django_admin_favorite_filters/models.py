from uuid import uuid4

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils.translation import ugettext_lazy as _


class FavoriteFilter(models.Model):
    """
    Holds favorited filters
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, help_text=_(""))
    filtered_model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    query_parameters = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - for {self.filtered_model}"



