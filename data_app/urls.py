from django.urls import path
from .views import import_excel_view, import_and_display_excel_view  # Import the view

urlpatterns = [
    path('import-excel/', import_excel_view, name='import_excel'),
    path('import-display-json/', import_and_display_excel_view, name='import_display_json'),
]
