from QitianSDK import QitianManager

from Config.models import Config, CI

QITIAN_APP_ID = Config.get_value_by_key(CI.QITIAN_APP_ID)
QITIAN_APP_SECRET = Config.get_value_by_key(CI.QITIAN_APP_SECRET)

SECRET_KEY = Config.get_value_by_key(CI.PROJECT_SECRET_KEY)
JWT_ENCODE_ALGO = Config.get_value_by_key(CI.JWT_ENCODE_ALGO)

qt_manager = QitianManager(QITIAN_APP_ID, QITIAN_APP_SECRET)
