from .server import ServerMixin
from .localstack import LocalStackMixin


class BaseMixin(ServerMixin, LocalStackMixin):
    """
    Creates the base mixin class to be used for tests.

    Note that the order of inheritance IS IMPORTANT. This order will guarantee
    that LocalStackMixin executes its setup before the ServerMixin. We need
    that to occur because, if we are using any AWS services, uvicorn, on start,
    will try to execute the startup/shutdown functions for those services. When
    testing, those functions will fail without the proper LocalStack
    configuration in place
    """
    pass
