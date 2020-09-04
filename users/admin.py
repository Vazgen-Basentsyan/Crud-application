# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User, Home, HomeImage


class HomeImageAdmin(admin.TabularInline):
    model = HomeImage


class UserAdmin(admin.ModelAdmin):
    fields = ("email", "first_name", "last_name", "age", "password")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and form.data.get("password"):
            obj.set_password(form.data.get("password"))
            obj.save()


class HomeAdmin(admin.ModelAdmin):
    fields = ("title", "location", "land_sqm", "place_sqm", "bedrooms")
    inlines = [HomeImageAdmin]
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and form.data.get("password"):
            obj.set_password(form.data.get("password"))
            obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(Home, HomeAdmin)
