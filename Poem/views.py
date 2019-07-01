import datetime

from SmartDjango import Packing, Analyse, Param, SmartPager
from django.views import View

from Poem.models import PM_CONTENT, PM_TITLE, Poem


PM_LAST = Param('last').process(int).process(lambda v: v if v else Poem.objects.count() + 1)
PM_COUNT = Param('count').process(int).process(lambda v: min(max(v, 1), 15))


class PoemIDView(View):
    @staticmethod
    @Packing.http_pack
    def get(r, poem_id):
        ret = Poem.get_by_id(poem_id)
        if not ret.ok:
            return ret
        poem = ret.body

        return poem.d()


class BaseView(View):
    @staticmethod
    @Packing.http_pack
    @Analyse.r(q=[PM_LAST, PM_COUNT])
    def get(r):
        page = Poem.objects.page(SmartPager(ascend=False), **r.d.dict())
        return page.dict(object_dictor=Poem.d_list)

    @staticmethod
    @Packing.http_pack
    @Analyse.r([PM_TITLE, PM_CONTENT])
    def post(r):
        ret = Poem.create(**r.d.dict())
        if not ret.ok:
            return ret
        poem = ret.body
        return poem.d_create()


class SearchView(View):
    @staticmethod
    @Packing.http_pack
    @Analyse.r(q=[Param('keyword'), PM_LAST, PM_COUNT])
    def get(r):
        objects = Poem.objects.search(**r.d.dict('keyword'))
        page = objects.page(SmartPager(ascend=False), **r.d.dict('last', 'count'))
        return page.dict(object_dictor=Poem.d)


class SummaryView(View):
    @staticmethod
    @Packing.http_pack
    def get(r):
        crt_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        objects = Poem.objects.filter(create_time__gte=crt_date)
        today_count = objects.count()

        crt_month = crt_date.replace(day=1)
        objects = Poem.objects.filter(create_time__gte=crt_month)
        month_count = objects.count()

        return dict(
            today=today_count,
            month=month_count,
        )
