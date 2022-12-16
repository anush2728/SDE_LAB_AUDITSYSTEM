from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(User)
admin.site.register(Auditor)
admin.site.register(Subcontractor)
admin.site.register(Event)
admin.site.register(Act)
admin.site.register(UploadFile)

