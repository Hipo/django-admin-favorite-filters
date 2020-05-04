from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .constants import FAVORITE_FILTER_QUERY_KEY
from .models import FavoriteFilter


class FavoriteFiltersFilter(SimpleListFilter):
    title = _("Favorite Filters")
    parameter_name = FAVORITE_FILTER_QUERY_KEY

    def lookups(self, request, model_admin):
        filtered_model = ContentType.objects.get_for_model(model_admin.model)
        return FavoriteFilter.objects.filter(filtered_model=filtered_model).filter(
            Q(is_public=True)
            |
            Q(user=request.user
          )
        ).distinct().values_list("id", "name")

    def queryset(self, request, queryset):
        return queryset

