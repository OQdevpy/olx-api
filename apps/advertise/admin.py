from django.contrib import admin
from .models import Advertise, Category, Images
# Register your models here.
class AdImageInline(admin.TabularInline):
    model = Images
    extra = 5
class AdAdmin(admin.ModelAdmin):
    list_display = ['title','description','category',   'price', 'created_at','expiration_date']
    list_filter = [ 'category',]
    readonly_fields = ['expiration_date']
    inlines = [AdImageInline]

admin.site.register(Category)
admin.site.register(Advertise, AdAdmin)