from django.contrib import admin

# Register your models here.

from .models import Benchmark

admin.site.register(Benchmark)
