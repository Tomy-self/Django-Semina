from django.contrib import admin
from .models import Reporter
from .models import Article

admin.site.register(Reporter)
admin.site.register(Article)
