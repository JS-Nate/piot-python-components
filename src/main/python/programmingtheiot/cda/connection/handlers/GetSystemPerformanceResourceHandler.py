#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener 
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener

from programmingtheiot.data.DataUtil import DataUtil

# NOTE: the next import is only needed for GetTelemetryResourceHandler
from programmingtheiot.data.SensorData import SensorData

# NOTE: the next import is only needed for GetSystemPerformanceResourceHandler
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
import aiocoap

from aiocoap import Code
from aiocoap.resource import ObservableResource
from coapthon import defines
from coapthon.resources.resource import Resource



class GetSystemPerformanceResourceHandler(ObservableResource, ISystemPerformanceDataListener):
    def __init__(self, name: str = ConfigConst.SYSTEM_PERF_MSG, coap_server=None):
        super(GetSystemPerformanceResourceHandler, self).__init__()

        self.path = name
        self.visible = True
        self.observable = True
        self.coap_server = coap_server

        self.pollCycles = ConfigUtil().getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
        )

        self.dataUtil = DataUtil()
        self.sysPerfData = None

        # for testing
        self.payload = "GetSysPerfData"

    def onSystemPerformanceDataUpdate(self, data: SystemPerformanceData) -> bool:
        pass

    async def render_get(self, request):
        responseCode = Code.CONTENT  # TODO: change to appropriate value

        if not self.sysPerfData:
            self.sysPerfData = SystemPerformanceData()

        jsonData = self.dataUtil.systemPerformanceDataToJson(self.sysPerfData)

        return aiocoap.Message(code=responseCode, payload=jsonData.encode('ascii'))
	
	
	