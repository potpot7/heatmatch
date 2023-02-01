from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUser,Account,Profile

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Account)
admin.site.register(Profile)
