import json

class GASearchVariantsRequest:

	def __init__(self, start, end, referenceName, variantSetIds = [""], callSetIds = None, pageSize = None, pageToken = None):
		
		self.GASearchVariantsRequest = {'start': start, 'end': end, 'referenceName': referenceName, 'pageSize': pageSize, 'pageToken': pageToken, 'callSetIds': callSetIds, 'variantSetIds': variantSetIds}


	def getJson(self):
		return json.dumps(self.GASearchVariantsRequest)