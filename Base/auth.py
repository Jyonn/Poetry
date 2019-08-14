from functools import wraps

from SmartDjango import Packing, ErrorCenter, E

from Base.jtoken import JWT
from User.models import User


class AuthError(ErrorCenter):
    REQUIRE_LOGIN = E("需要登录", hc=401)
    TOKEN_MISS_PARAM = E("认证口令缺少参数{0}", E.PH_FORMAT, hc=400)


AuthError.register()


class Auth:
    @staticmethod
    @Packing.pack
    def validate_token(request):
        jwt_str = request.META.get('HTTP_TOKEN')
        if jwt_str is None:
            return AuthError.REQUIRE_LOGIN

        ret = JWT.decrypt(jwt_str)
        if not ret.ok:
            return ret
        dict_ = ret.body

        return dict_

    @staticmethod
    def get_login_token(user: User):
        token, _dict = JWT.encrypt(dict(
            user_id=user.qt_user_app_id,
        ))
        _dict['token'] = token
        _dict['user'] = user.d()
        return _dict

    @classmethod
    @Packing.pack
    def _extract_user(cls, r):
        r.user = None

        ret = cls.validate_token(r)
        if not ret.ok:
            return ret

        dict_ = ret.body
        user_id = dict_.get('user_id')
        if not user_id:
            return AuthError.TOKEN_MISS_PARAM('user_id')

        from User.models import User
        ret = User.get_by_qt_user_app_id(user_id)
        if not ret.ok:
            return ret
        r.user = ret.body

    @classmethod
    def require_login(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            ret = cls._extract_user(r)
            if not ret.ok:
                return ret
            return func(r, *args, **kwargs)
        return wrapper
