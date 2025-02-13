from django.contrib import admin
from .models import ExcelData

@admin.register(ExcelData)
class ExcelDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'data_preview')

    def data_preview(self, obj):
        # Display a preview of the JSON data (first 50 characters)
        return str(obj.data)[:50] + "..."
    
    data_preview.short_description = "Data Preview"