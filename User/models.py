from SmartDjango import models, Excp, ErrorCenter, E


class UserError(ErrorCenter):
    USER_NOT_FOUND = E("不存在的用户", hc=404)
    CREATE_USER = E("新建用户错误", hc=500)


UserError.register()


class User(models.Model):
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
        max_length=1024,
    )

    nickname = models.CharField(
        verbose_name='昵称',
        default=None,
        blank=True,
        null=True,
        max_length=10,
    )

    qt_user_app_id = models.CharField(
        verbose_name='齐天簿ID',
        max_length=16,
    )

    qt_token = models.CharField(
        verbose_name='齐天簿口令',
        max_length=256,
        min_length=4,
    )

    @staticmethod
    @Excp.pack
    def get_by_qt_user_app_id(qt_user_app_id):
        try:
            user = User.objects.get(qt_user_app_id=qt_user_app_id)
        except User.DoesNotExist as err:
            return UserError.USER_NOT_FOUND
        return user

    @classmethod
    @Excp.pack
    def create(cls, qt_user_app_id, qt_token):
        cls.validator(locals())

        try:
            user = cls.get_by_qt_user_app_id(qt_user_app_id)
            user.qt_token = qt_token
            user.save()
            return user
        except Excp as excp:
            if excp.erroris(UserError.USER_NOT_FOUND):
                try:
                    user = cls(
                        qt_user_app_id=qt_user_app_id,
                        qt_token=qt_token,
                    )
                    user.save()
                except Exception:
                    return UserError.CREATE_USER
            else:
                return UserError.CREATE_USER

    @Excp.pack
    def update(self):
        from Base.common import qt_manager
        data = qt_manager.get_user_info(self.qt_token)
        self.avatar = data['avatar']
        self.nickname = data['nickname']
        self.save()

    def _readable_user_id(self):
        return self.qt_user_app_id

    def d(self):
        return self.dictor(['nickname', 'avatar', 'user_id'])
