import logging
import unittest
import time
#from programmingtheiot.common.ConfigConst import ConfigConst
from time import sleep
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData 
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData 
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

class MqttClientControlPacketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Executing the MqttClientControlPacketTest class...")

    def setUp(self):
        self.mqttClient = MqttClientConnector(clientID="MyTestMqttClient")
        self.mqttClient.connectClient()
        self.mqttClient.subscribeToTopic("lab6", qos=1)

    def tearDown(self):
        self.mqttClient.unsubscribeFromTopic("lab6")
        self.mqttClient.disconnectClient()

    def testConnectAndDisconnect(self):
        # Test connecting and disconnecting from the broker
        self.assertTrue(self.mqttClient.isConnected())
        self.mqttClient.disconnectClient()
        self.assertFalse(self.mqttClient.isConnected())

    def testServerPing(self):
        # Test sending a PING request to the server
        self.assertTrue(self.mqttClient.pingBroker())

    def testPubSub(self):
        # Test publishing and subscribing with different QoS levels
        topic = "lab6"
        payload = "payload"
        qos_levels = [0, 1, 2]

        for qos in qos_levels:
            self.mqttClient.publishMessage(topic, payload, qos=qos)
            time.sleep(2)  # Wait for the message to be delivered

        # Ensure that messages were received with the expected QoS levels
        for qos in qos_levels:
            message = self.mqttClient.getLastMessage()
            self.assertIsNotNone(message)
            self.assertEqual(message.qos, qos)
            self.assertEqual(message.topic, topic)
            self.assertEqual(message.payload, payload)
