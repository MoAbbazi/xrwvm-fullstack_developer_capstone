from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display

# Admin class for CarMake with inline CarModels
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']
    list_filter = ['car_make', 'type', 'year']
    search_fields = ['name', 'car_make__name']

# Register models with custom admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
