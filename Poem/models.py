import datetime

from SmartDjango import E, models, Hc
from django.db.models import Q


@E.register(id_processor=E.idp_cls_prefix())
class PoemError:
    POEM_NOT_FOUND = E("不存在的诗歌", hc=Hc.NotFound)
    CREATE_POEM = E("发布诗歌失败", hc=Hc.InternalServerError)
    POEM_NOT_BELONG = E("没有查看权限", hc=Hc.Unauthorized)


class Poem(models.Model):
    title = models.CharField(
        verbose_name='诗名',
        max_length=100,
    )

    content = models.TextField(
        verbose_name='正文',
    )

    create_time = models.DateTimeField(
        verbose_name='发布时间',
    )

    user = models.ForeignKey(
        'User.User',
        verbose_name='作者',
        default=None,
        null=True,
        on_delete=models.SET_NULL,
    )

    @classmethod
    def create(cls, title, content, user):
        crt_time = datetime.datetime.now()

        try:
            poem = cls(
                user=user,
                title=title,
                content=content,
                create_time=crt_time,
            )
            poem.save()
            return poem
        except Exception as err:
            raise PoemError.CREATE_POEM(debug_message=err)

    """
    查询函数
    """

    @classmethod
    def get_by_id(cls, poem_id):
        try:
            return cls.objects.get(pk=poem_id)
        except cls.DoesNotExist:
            raise PoemError.POEM_NOT_FOUND

    def belong(self, user):
        return self.user == user

    """
    筛选函数
    """

    @staticmethod
    def _search_keyword(v):
        return Q(title__contains=v) | Q(content__contains=v)

    """
    字典函数
    """

    def _readable_create_time(self):
        return self.create_time.timestamp()

    def d_create(self):
        return self.dictify('pk->id')

    def d_list(self):
        return self.dictify('pk->id', 'title', 'create_time')

    def d(self):
        return self.dictify('title', 'content', 'create_time')

    """
    修改函数
    """

    def update(self, title, content):
        self.title = title
        self.content = content
        self.create_time = datetime.datetime.now()
        self.save()


PM_TITLE, PM_CONTENT = Poem.get_params('title', 'content')
