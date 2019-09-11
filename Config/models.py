from SmartDjango import ErrorCenter, models, Excp, E


class ConfigError(ErrorCenter):
    CREATE_CONFIG = E("更新配置错误", hc=500)
    CONFIG_NOT_FOUND = E("不存在的配置", hc=404)


ConfigError.register()


class Config(models.Model):
    MAX_L = {
        'key': 100,
        'value': 255,
    }

    key = models.CharField(
        max_length=MAX_L['key'],
        unique=True,
    )

    value = models.CharField(
        max_length=MAX_L['value'],
    )

    @classmethod
    @Excp.pack
    def get_config_by_key(cls, key):
        cls.validator(locals())

        try:
            o_config = cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            return ConfigError.CONFIG_NOT_FOUND

        return o_config

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            config = cls.get_config_by_key(key)
            return config.value
        except Exception:
            return default

    @classmethod
    @Excp.pack
    def update_value(cls, key, value):
        cls.validator(locals())

        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except Excp as excp:
            if excp.erroris(ConfigError.CONFIG_NOT_FOUND):
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception:
                    return ConfigError.CREATE_CONFIG
            else:
                return ConfigError.CREATE_CONFIG


class ConfigInstance:
    JWT_ENCODE_ALGO = 'jwt-encode-algo'
    PROJECT_SECRET_KEY = 'project-secret-key'

    HOST = 'host'
    QITIAN_APP_ID = 'qt-app-id'
    QITIAN_APP_SECRET = 'qt-app-secret'


CI = ConfigInstance
