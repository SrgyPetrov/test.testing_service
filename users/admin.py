from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from quizzes.utils import get_user_stats

from .models import User, UserAnswer


class UserAnswerAdmin(admin.ModelAdmin):

    list_filter = ('user__username',)


class UserAdmin(BaseUserAdmin):

    stats_template = 'admin/users/stats.html'
    readonly_fields = ['stats']
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Statistic'), {'fields': ('stats',)}),
    )

    def stats(self, instance):
        template = loader.get_template(self.stats_template)
        stats = get_user_stats(instance)
        return template.render({'stats': stats})

    stats.short_description = _("Statistic")


admin.site.register(User, UserAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.unregister(Group)
