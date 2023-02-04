from .server import ServerMixin
from .localstack import LocalStackMixin


class BaseMixin(ServerMixin, LocalStackMixin):
    pass
