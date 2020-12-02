import logging

from tornado.ioloop import IOLoop

from tfw.config import TFWENV
from tfw.components.pipe_io import PipeIOHandler, ProxyPipeConnectorHandler
from tfw.main import EventHandlerFactory, setup_logger, setup_signal_handlers

LOG = logging.getLogger(__name__)


def main():
    # pylint: disable=unused-variable
    setup_logger(__file__)

    eh_factory = EventHandlerFactory()

    json_pipe_eh = eh_factory.build(PipeIOHandler(
        '/tmp/tfw_send',
        '/tmp/tfw_recv',
        permissions=0o666
    ))
    proxy_pipe_eh = eh_factory.build(ProxyPipeConnectorHandler(TFWENV.PIPES_DIR))

    setup_signal_handlers()
    IOLoop.current().start()


if __name__ == '__main__':
    main()
