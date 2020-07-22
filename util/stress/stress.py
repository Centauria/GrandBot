import psutil
from util.base.singleton import  Singleton

@Singleton
class StressTest():

	def __init__(self):
		self.test_time = 0

	#function of Get cpu state
	def getCPUstate(self, interval=1):
		return psutil.cpu_percent(interval)

	def getMemorystate(self):
		phymem = psutil.virtual_memory()
		return (phymem.used/1024/1024) / (phymem.total/1024/1024)

	def test(self):
		self.test_time += 1
		return self.test_time
