import datetime

from SmartDjango import Excp, Analyse, P, models
from django.views import View

from Base.auth import Auth
from Poem.models import PM_CONTENT, PM_TITLE, Poem, PoemError

PM_LAST = P('last').process(int).process(lambda v: v if v else Poem.objects.count() + 1)
PM_COUNT = P('count').process(int).process(lambda v: min(max(v, 1), 15))


class PoemIDView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(a=[P('poem_id', '诗歌ID').process(P.Processor(Poem.get_by_id, yield_name='poem'))])
    @Auth.require_login
    def get(r, poem_id):
        poem = r.d.poem

        if not poem.belong(r.user):
            return PoemError.POEM_NOT_BELONG

        return poem.d()


class BaseView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(q=[PM_LAST, PM_COUNT])
    @Auth.require_login
    def get(r):
        poems = Poem.objects.filter(user=r.user)
        page = poems.page(models.Pager(ascend=False), **r.d.dict())
        return page.dict(object_dictor=Poem.d_list)

    @staticmethod
    @Excp.handle
    @Analyse.r([PM_TITLE, PM_CONTENT])
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
