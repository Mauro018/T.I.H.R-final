from django.contrib import admin
from .models import User, UserAdmin, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, UserClientes

admin.site.register(User)
admin.site.register(UserAdmin)
admin.site.register(Mesas)
admin.site.register(Sillas)
admin.site.register(Armarios)
admin.site.register(Cajoneras)
admin.site.register(Escritorios)
admin.site.register(Utensilios)
admin.site.register(UserClientes)