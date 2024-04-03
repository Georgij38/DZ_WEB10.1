from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('quotes.urls')),
    path('users/', include('users.urls')),
    path('creation_new_author/', include('creation_new_author.urls')),

]
