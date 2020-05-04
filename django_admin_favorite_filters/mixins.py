from copy import deepcopy

from django.contrib import messages
from django.contrib.admin.options import csrf_protect_m
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .constants import FAVORITE_FILTER_QUERY_KEY, FAVORITE_FILTER_SESSION_KEY
from .models import FavoriteFilter


class FavoriteFilterMixin(object):

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        The 'change list' admin view for this model.
        """
        favorite_filter_id = request.GET.get(FAVORITE_FILTER_QUERY_KEY)
        if favorite_filter_id:
            try:
                favorite_filter = FavoriteFilter.objects.get(id=favorite_filter_id)  # TODO: Add same filter above.
            except (FavoriteFilter.DoesNotExist, ValidationError) as e:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f"Error ({e}) occured while getting the requested filter: {favorite_filter_id}")
                )
            else:
                messages.add_message(request, messages.SUCCESS, 'Displaying results filtered by %s.' % favorite_filter.name)
                request.session[FAVORITE_FILTER_SESSION_KEY] = True
                return HttpResponseRedirect("?%s" % favorite_filter.query_parameters)
        else:
            user_came_by_a_favorite_filter = request.session.pop(FAVORITE_FILTER_SESSION_KEY, False)
            if not user_came_by_a_favorite_filter:
                request_parameters = deepcopy(request.GET)
                request_parameters.pop("o", None)  # Do not count ordering.
                request_parameters.pop("e", None)  # Do not count errors.
                if len(request_parameters) > 0:  # This means that user is actually using a filter.
                    add_favorite_url = reverse('admin:%s_%s_add' % (FavoriteFilter._meta.app_label, FavoriteFilter._meta.model_name))
                    filtered_model = ContentType.objects.get_for_model(self.model)
                    add_favorite_url = f"{add_favorite_url}?filtered_model={filtered_model.id}&query_parameters={request.META['QUERY_STRING']}"

                    messages.add_message(
                        request,
                        messages.INFO,
                        mark_safe(_(
                            f"<b>This search hasn’t been saved for future use.</b> "
                            f"If this is something you use on a regular basis, you can save this search and "
                            f"(optionally) share it with other users. If you wish to save this search, click "
                            f"<b><a href='{add_favorite_url}'>here</a></b>. It will then appear under the 'Favorite Filters'.")
                    ))
        return super(FavoriteFilterMixin, self).changelist_view(request, extra_context)
