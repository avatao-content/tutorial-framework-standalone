from tfw.components.frontend import ConsoleLogsHandler, MessageQueueHandler, FrontendConfigHandler
from tfw.components.process_management import ProcessHandler, ProcessLogHandler
from tfw.main import TFWUplinkConnector, EventHandlerFactory, setup_logger, setup_signal_handlers
from tfw.components.frontend import FrontendProxyHandler, FrontendReadyHandler
from tfw.components.ide import IdeHandler, DeployHandler
from tfw.components.terminal import TerminalHandler
from tfw.components.frontend import MessageSender
from tfw.event_handlers import FSMAwareEventHandler
from os.path import dirname, realpath, join
from tfw.components.fsm import FSMHandler
from tfw.config import TFWENV, TAOENV
from tornado.ioloop import IOLoop
from functools import partial
from app_fsm import App
import subprocess
import logging
import yaml

here = dirname(realpath(__file__))
LOG = logging.getLogger(__name__)



if __name__ == '__main__':
    # pylint: disable=unused-variable,too-many-locals
    setup_logger(__file__)

    eh_factory = EventHandlerFactory()
    # TFW builtin EventHandlers (required for their respective functionalities)
    # TFW FSM
    fsm_eh = eh_factory.build(FSMHandler(
        fsm_type=App
    ))
    with open(TFWENV.APP_YML) as f:
        config = yaml.safe_load(f.read())
    # Web IDE backend
    ide_eh = eh_factory.build(IdeHandler(
        patterns=config['ide']['patterns']
    ))

    terminal_eh = eh_factory.build(TerminalHandler(
        port=TFWENV.TERMINAL_PORT,
        user=TAOENV.USER,
        working_directory=config['terminal']['directory'],
        histfile=TFWENV.HISTFILE
    ))
    # Proxies frontend API calls to frontend
    frontendproxy_eh = eh_factory.build(FrontendProxyHandler())
    # Initiates first FSM step
    if config['dashboard']['stepToFirstStateAutomatically']:
        frontendready = FrontendReadyHandler('step_1')
    else:
        frontendready = FrontendReadyHandler('step_0')
    frontendready_eh = eh_factory.build(frontendready)
    frontendready.stop = frontendready_eh.stop
    # Configures frontend
    frontendconfig_eh = eh_factory.build(
        FrontendConfigHandler(join(here, 'frontend_config.yaml'))
    )
    # Manages message queues
    messagequeue_eh = eh_factory.build(MessageQueueHandler(config['dashboard']['messageSpeed']))
    
    # Writes live logs to console on frontend
    #console_logs_eh = eh_factory.build(ConsoleLogsHandler(stream='stdout'))
    #button_handler = eh_factory.build(ButtonClickHandler())
    #message_fsm_steps_eh = eh_factory.build(messageFSMStepsHandler, event_handler_type=FSMAwareEventHandler)

    setup_signal_handlers()
    IOLoop.current().start()
