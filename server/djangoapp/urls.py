from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    path('get_cars', views.get_cars, name='getcars'),
    path('dealerships', views.get_dealerships, name='dealerships'),
    path('dealer/<int:dealer_id>/reviews', views.get_dealer_reviews, name='dealer_reviews'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('review/add', views.add_review, name='add_review'),
]

# Append media files handling
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
