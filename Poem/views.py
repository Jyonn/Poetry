import datetime

from SmartDjango import Excp, Analyse, P, models
from django.views import View

from Base.auth import Auth
from Base.common import last_timer, int_or_float, time_dictor
from Poem.models import PM_CONTENT, PM_TITLE, Poem, PoemError


PM_LAST = P('last').process(int_or_float).process(last_timer)
PM_COUNT = P('count').process(int).process(lambda v: min(max(v, 1), 15))
PM_POEM_ID = P('poem_id', '诗歌ID').process(P.Processor(Poem.get_by_id, yield_name='poem'))


class PoemIDView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(a=[PM_POEM_ID])
    @Auth.require_login
    def get(r, poem_id):
        poem = r.d.poem

        if not poem.belong(r.user):
            return PoemError.POEM_NOT_BELONG

        return poem.d()

    @staticmethod
    @Excp.handle
    @Analyse.r(a=[PM_POEM_ID], b=[PM_TITLE, PM_CONTENT])
    @Auth.require_login
    def put(r, poem_id):
        poem = r.d.poem

        if not poem.belong(r.user):
            return PoemError.POEM_NOT_BELONG

        poem.update(**r.d.dict('title', 'content'))


class BaseView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(q=[PM_LAST, PM_COUNT])
    @Auth.require_login
    def get(r):
        poems = Poem.objects.filter(user=r.user)
        time_d_pager = models.Pager(ascend=False, compare_field='create_time')
        page = poems.page(time_d_pager, **r.d.dict())
        return page.dict(object_dictor=Poem.d_list, next_dictor=time_dictor)

    @staticmethod
    @Excp.handle
    @Analyse.r(b=[PM_TITLE, PM_CONTENT])
    @Auth.require_login
    def post(r):
        poem = Poem.create(user=r.user, **r.d.dict())
        return poem.d_create()


class SearchView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(q=['keyword', PM_LAST, PM_COUNT])
    def get(r):
        objects = Poem.objects.search(**r.d.dict('keyword'))
        page = objects.page(models.Pager(ascend=False), **r.d.dict('last', 'count'))
        return page.dict(object_dictor=Poem.d)


class SummaryView(View):
    @staticmethod
    @Excp.handle
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
