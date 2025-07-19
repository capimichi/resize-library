import json
import logging
import os

from injector import Injector
from dotenv import load_dotenv

from apprise import Apprise


class DefaultContainer:
    injector = None
    instance = None

    @staticmethod
    def getInstance():
        if DefaultContainer.instance is None:
            DefaultContainer.instance = DefaultContainer()
        return DefaultContainer.instance

    def __init__(self):
        self.injector = Injector()

        load_dotenv()

        self._init_environment_variables()
        self._init_directories()
        self._init_logging()
        self._init_bindings()

    def get(self, key):
        return self.injector.get(key)

    def get_var(self, key):
        return self.__dict__[key]

    def _init_directories(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # self.var_dir = os.path.join(self.root_dir, 'var')
        # os.makedirs(self.var_dir, exist_ok=True)
        # self.log_dir = os.path.join(self.var_dir, 'log')
        # os.makedirs(self.log_dir, exist_ok=True)
        # self.app_log_path = os.path.join(self.log_dir, 'app.log')

    def _init_environment_variables(self):
        self.apprise_streams = json.loads(os.environ.get('RESIZE_LIBRARY_APPRISE_STREAMS', '[]'))
        self.enable_logs = os.environ.get('RESIZE_LIBRARY_LOGS_ENABLE', 'false').lower() == 'true'
        self.log_dir = os.environ.get('RESIZE_LIBRARY_LOGS_DIR', os.path.join(self.var_dir, 'log'))

    def _init_logging(self):
        if self.enable_logs:
            os.makedirs(self.log_dir, exist_ok=True)
            self.app_log_path = os.path.join(self.log_dir, 'app.log')
            logging.basicConfig(
                filename=self.app_log_path,
                level=logging.INFO,
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S'
            )
        else:
            logging.basicConfig(level=logging.CRITICAL)  # Disable most logging if logs are not enabled

    def _init_bindings(self):
        # self.injector.binder.bind(PostDirVariable, PostDirVariable(self.post_dir))

        apprise = Apprise()
        for stream in self.apprise_streams:
            apprise.add(stream)
        self.injector.binder.bind(Apprise, apprise)
