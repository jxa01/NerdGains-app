from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.app import App
import time

class StopWatch(Label):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.running = False
		self.start_time = None
		self.elap_time = 0
		self.text="00:00.0"
		
	def start(self):
		if not self.running:
			self.start_time = time.time() - self.elap_time
			self.running = True
			Clock.schedule_interval(self.update_time, 0.1)
		
	def stop(self):
		if self.running:
			Clock.unschedule(self.update_time)
			self.running = False
		
		
	def reset(self):
		self.stop()
		self.text = "00:00.0"
		self.elap_time = 0
		
	def update_time(self, dt):
		if self.running:
			self.elap_time = time.time() - self.start_time
			min, sec = divmod(self.elap_time, 60)
			self.text = f"{int(min):02}:{sec:04.1f}"

			
#test code below									
#class app(App):
#	def build(self):
#		sw = StopWatch(text="00:00.0")
#		sw.start()
#		return sw
#		
#app().run()