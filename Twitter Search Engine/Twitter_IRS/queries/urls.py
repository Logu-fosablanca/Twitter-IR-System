from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('query/', views.home),
    path('jd_query/', views.home),
    path('ed_query/', views.home),
    path('t_query/', views.home),

    path('query/<str:q>', views.queries),
    path('jd_query/<str:q>', views.jaccard_distance_queries),
    path('ed_query/<str:q>', views.edit_distance_queries),
    path('t_query/<str:q>', views.thesauras_queries),
]
