from SmartDjango import Analyse, P
from django.views import View

from Base.auth import Auth
from User.models import User
from Base.common import qt_manager


class OAuthView(View):
    @staticmethod
    @Analyse.r([P('code', '授权码')])
    def post(r):
        """POST /user/oauth

        打通齐天簿OAuth
        """
        code = r.d.code
        data = qt_manager.get_token(code)
        qt_token = data['token']
        qt_user_app_id = data['user_app_id']

        user = User.create(qt_user_app_id, qt_token)
        user.update()

        return Auth.get_login_token(user)


class BaseView(View):
    @staticmethod
    @Auth.require_login
    def get(r):
        """GET /user/

        获取用户基本信息
        """
        r.user.update()
        return r.user.d()
