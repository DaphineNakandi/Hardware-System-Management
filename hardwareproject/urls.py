from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Aunthentication URLs, login, logout, password_change
    # path('accounts/', include('django.contrib.auth.urls')),
  
    
    #Main App URLs
    path('', include('hardware_app.urls')),
    path('users/', include("users.urls"))


]
