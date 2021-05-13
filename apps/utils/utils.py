import json

class SettingsSwitch:
    """
    Типа свитч для преобразования ответа настроек
    """
    @staticmethod
    def int_data(value):
        return int(value)

    @staticmethod
    def float_data(value):
        return float(value)

    @staticmethod
    def str_data(value):
        return str(value)

    @staticmethod
    def json_data(value):
        return json.loads(value)

    def dispatch(self, setting):
        method_name = str(type(setting).__name__) + '_data'
        return getattr(self, method_name)(setting)