
#
# PyGoWave Server - The Python Google Wave Server
# Copyright 2009 Patrick Schneider <patrick.p2k.schneider@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# This is PyGoWave's RPC script used for client-to-server communication only
# through RabbitMQ. This may be slightly faster than it's twisted-based cousin.

import sys, os, logging

sys.path.append(os.path.dirname(__file__))
if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
	os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from carrot.connection import AMQPConnection

from pygowave_rpc.amqp_client import AmqpMessageProcessor
import pygowave_rpc.logger

from django.conf import settings

logger = pygowave_rpc.logger.setupLogging()

if pygowave_rpc.logger.logMode() == "verbose":
	amqplogger = logging.getLogger("amqplib")
	amqplogger.setLevel(logging.DEBUG)
	amqplogger.addHandler(logging.StreamHandler())

logger.info("=> PyGoWave RPC Server starting <=")

import signal
# Python Ctrl-C handler
signal.signal(signal.SIGINT, signal.SIG_DFL)

try:
	amqpconn = AMQPConnection(
		hostname=getattr(settings, "RPC_SERVER", "localhost"),
		userid=getattr(settings, "RPC_USER", "pygowave_server"),
		password=getattr(settings, "RPC_PASSWORD", "pygowave_server"),
		virtual_host=getattr(settings, "AMQP_VHOST", "/"),
		port=getattr(settings, "AMQP_PORT", 5672)
	)
	omc = AmqpMessageProcessor(amqpconn)
	logger.info("=> PyGoWave RPC Server ready <=")
	omc.wait()
except:
	import traceback
	logger.critical("Crash!\n" + traceback.format_exc())
	sys.exit(1)
