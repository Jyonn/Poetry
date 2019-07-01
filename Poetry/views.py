from django.shortcuts import render
from django.views import View


class IndexView(View):
    @staticmethod
    def get(r):
        return render(r, 'index.html')


class WriterView(View):
    @staticmethod
    def get(r, **kwargs):
        return render(r, 'writer.html', context=kwargs)
