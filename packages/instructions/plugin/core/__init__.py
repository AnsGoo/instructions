from typing import TypeVar

from plugin.models import PluginModel

T = TypeVar('T')


class BasePlugin:
    def __init__(self, plugin_model: PluginModel):
        self.plugin_model = plugin_model
        self.plugin_code = plugin_model.code
        self.plugin_config = plugin_model.config
        self.plugin_status = plugin_model.status
        self.plugin_version = plugin_model.version
        self.plugin_author = plugin_model.author
        self.plugin_tags = plugin_model.tags

    def setup(self):
        raise NotImplementedError('must implement setup')

    def run(self, file_path: str) -> T:
        raise NotImplementedError('must implement run')

    def teardown(self):
        raise NotImplementedError('must implement teardown')


class StoreBasePlugin(BasePlugin):
    def __init__(self, plugin_model: PluginModel):
        super().__init__(plugin_model)

    def setup(self):
        return super().setup()

    def run(self, file_path: str) -> T:
        return super().run(file_path)

    def teardown(self):
        return super().teardown()
