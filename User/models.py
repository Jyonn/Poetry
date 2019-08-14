from SmartDjango import SmartModel, Packing, ErrorCenter, E
from django.db import models


class UserError(ErrorCenter):
    USER_NOT_FOUND = E("不存在的用户", hc=404)
    CREATE_USER = E("新建用户错误", hc=500)


UserError.register()


class User(SmartModel):
    MAX_L = {
        'avatar': 1024,
        'nickname': 10,
        'qt_user_app_id': 16,
        'qt_token': 256,
    }

    avatar = models.CharField(
        verbose_name='头像',
        default=None,
        null=True,
        blank=True,
        max_length=MAX_L['avatar']
    )

    nickname = models.CharField(
        verbose_name='昵称',
        default=None,
        blank=True,
        null=True,
        max_length=MAX_L['nickname']
    )

    qt_user_app_id = models.CharField(
        verbose_name='齐天簿ID',
        max_length=MAX_L['qt_user_app_id']
    )

    qt_token = models.CharField(
        verbose_name='齐天簿口令',
        max_length=MAX_L['qt_token']
    )

    @staticmethod
    @Packing.pack
    def get_by_qt_user_app_id(qt_user_app_id):
        try:
            o_user = User.objects.get(qt_user_app_id=qt_user_app_id)
        except User.DoesNotExist as err:
            return UserError.USER_NOT_FOUND
        return o_user

    @classmethod
    @Packing.pack
    def create(cls, qt_user_app_id, qt_token):
        ret = cls.validator(locals())
        if not ret.ok:
            return ret

        ret = cls.get_by_qt_user_app_id(qt_user_app_id)
        if ret.erroris(UserError.USER_NOT_FOUND):
            try:
                o_user = cls(
                    qt_user_app_id=qt_user_app_id,
                    qt_token=qt_token,
                )
                o_user.save()
            except Exception as err:
                return UserError.CREATE_USER
        else:
            o_user = ret.body
            o_user.qt_token = qt_token
            o_user.save()
        return o_user

    @Packing.pack
    def update(self):
        from Base.common import qt_manager
        ret = qt_manager.get_user_info(self.qt_token)
        if not ret.ok:
            return ret
        data = ret.body
        print(data)
        self.avatar = data['avatar']
        self.nickname = data['nickname']
        self.save()

    def _readable_user_id(self):
        return self.qt_user_app_id

    def d(self):
        return self.dictor(['nickname', 'avatar', 'user_id'])
