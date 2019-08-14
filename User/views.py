from SmartDjango import Packing, Analyse, Param
from django.views import View

from Base.auth import Auth
from User.models import User
from Base.common import qt_manager


class OAuthView(View):
    @staticmethod
    @Packing.http_pack
    @Analyse.r([Param('code', '授权码')])
    def post(r):
        """POST /user/oauth

        打通齐天簿OAuth
        """
        code = r.d.code
        ret = qt_manager.get_token(code)
        if not ret.ok:
            return ret
        qt_token = ret.body['token']
        qt_user_app_id = ret.body['user_app_id']

        ret = User.create(qt_user_app_id, qt_token)
        if not ret.ok:
            return ret
        o_user = ret.body

        ret = o_user.update()
        if not ret.ok:
            return ret

        return Auth.get_login_token(o_user)


class BaseView(View):
    @staticmethod
    @Packing.http_pack
    @Auth.require_login
    def get(r):
        """GET /user/

        获取用户基本信息
        """
        return r.user.d()
