from django.contrib import admin
from django.urls import path
from . import views
from .views import book_ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signup,name='signup'),
    path('loginform',views.loginform,name='loginform'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.passenger_register, name='passenger_register'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('staffregister/', views.staff_register, name='staff_register'),
    path('add_bed/', views.add_bed, name='add_bed'),
    path('update_bedroll/<int:ticket_id>/', views.update_bedroll, name='update_bedroll'),

]