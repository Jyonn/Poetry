from django.urls import include, path

urlpatterns = [
    path('poem/', include('Poem.urls')),
    path('user/', include('User.urls')),
]
