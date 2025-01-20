from django.urls import path
from . import views

urlpatterns = [
    path('dynamic-graph/', views.dynamic_graph_view, name='dynamic_graph'),
]
