import os
import json

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from tfw.event_handlers import FSMAwareEventHandler
from tfw.main import EventHandlerFactory, setup_signal_handlers


class ControllerPostHandler(RequestHandler):
    # pylint: disable=abstract-method,attribute-defined-outside-init,unused-argument
    def initialize(self, **kwargs):
        self.controller = kwargs['controller']

    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'solved': self.controller.fsm_in_accepted_state
        }))


if __name__ == '__main__':
    controller_eh = EventHandlerFactory().build(
        lambda *_: None,
        event_handler_type=FSMAwareEventHandler
    )

    route = os.environ['SECRET'].rstrip('/')
    application = Application([(
        f'/{route}/?',
        ControllerPostHandler,
        {'controller': controller_eh}
    )])
    application.listen(os.environ['CONTROLLER_PORT'])

    setup_signal_handlers()
    IOLoop.current().start()