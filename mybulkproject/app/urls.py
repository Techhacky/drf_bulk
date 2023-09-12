# urls.py
from django.urls import path
from .views import BulkUpdateCreateView

urlpatterns = [
    path('bulk-update-create/', BulkUpdateCreateView.as_view(), name='bulk-update-create'),
]
