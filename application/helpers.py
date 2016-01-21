class SiteConfig(object):
		def __init__(self, querydata):
			self.state = querydata[0].value
			self.food = querydata[1].value
			self.time = querydata[2].value
			self.arrivalmin = querydata[3].value.split()[0]
			self.arrivalmax = querydata[3].value.split()[1]