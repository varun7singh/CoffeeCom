from django.contrib import admin
from .models import Movies, StreamingPlatform, Reviews

# Register your models here.
admin.site.register(Movies)
admin.site.register(StreamingPlatform)
admin.site.register(Reviews)

