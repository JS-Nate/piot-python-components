#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
# import aiocoap
#
# from aiocoap import Code
from aiocoap.resource import Resource
# from coapthon import defines
# from coapthon.resources.resource import Resource

class UpdateActuatorResourceHandler(Resource):
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.dataMsgListener = dataMsgListener
		self.dataUtil = DataUtil()
		
		
	
	async def render_put(self, request):
		try:
			# TODO: validate the request!
			# Check payload
			# Check content-type (should be JSON)
			actuatorCmdData = self.dataUtil.jsonToActuatorData(request.payload)
			
			return self._createResponse(actuatorCmdData)
		except:
			logging.warning("Failed to validate and convert actuation command.")
			
		return aiocoap.Message(code = Code.NOT_ACCEPTABLE)
	
	
	
	
	def render_PUT_advanced(self, request, response):
		if request:
			# TODO: validate the request!
			# Check payload
			# Check content-type (should be JSON)
			requestPayload = request.get_payload()
			actuatorCmdData = self.dataUtil.jsonToActuatorData(requestPayload)
			
			response.payload = self._createResponse(response = response, data = actuatorCmdData)
			response.max_age = self.pollCycles
			
		return self, response
	
	def _createResponse(self, response = None, data: ActuatorData = None) -> str:
		actuatorResponseData = self.dataMsgListener.handleActuatorCommandMessage(data)
		
		if not actuatorResponseData:
			actuatorResponseData = ActuatorData()
			actuatorResponseData.updateData(data)
			actuatorResponseData.setAsResponse()
			actuatorResponseData.setStatusCode(-1)
			
			response.code = defines.Codes.PRECONDITION_FAILED.number
		else:
			response.code = defines.Codes.CHANGED.number
		
		# TODO: validate the data and convert to JSON
		
		# return the JSON data
		jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
	
		return (defines.Content_types["application/json"], jsonData)
		
	
	
	
	
	