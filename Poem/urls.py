from django.urls import path

from Poem.views import BaseView, PoemIDView, SearchView, SummaryView

urlpatterns = [
    path('', BaseView.as_view()),
    path('search', SearchView.as_view()),
    path('summary', SummaryView.as_view()),
    path('@<int:poem_id>', PoemIDView.as_view()),
]
