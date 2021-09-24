####----------------- ADMIN.PY -----------------
from django.contrib import admin
from .models import *
from django.contrib.auth import admin as auth_admin
from .forms import UserCreationForm, UserChangeForm


# Register your models here.j

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    # tirar comentário e colocar os nomes dos campos adicionais
    """fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Campos Extras!", {"fields":("is_cnpj",)}),
    )"""

# admin.site.register()
