from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.app import App
import time

class StopWatch(BoxLayout):
	extra_action = ObjectProperty(None)
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.running = False
		self.start_time = None
		self.elap_time = 0
		self.display = Label(text="00:00.0")
		self.start_stop_btn = Button(text="Start")
		self.add_widget(self.display)
		self.add_widget(self.start_stop_btn)

	def on_kv_post(self, instance):
		self.start_stop_btn.bind(on_release=self.start_stop_btn_action)

	def start_stop_btn_action(self, instance):
		if self.start_stop_btn.text == "Start":
			self.start_stop_btn.text = "Stop"
			self.start()
		else:
			self.start_stop_btn.text = "Start"
			self.stop()
		if self.extra_action:
			self.extra_action()

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
		self.display.text = "00:00.0"
		self.elap_time = 0

	def update_time(self, dt):
		if self.running:
			self.elap_time = time.time() - self.start_time
			min, sec = divmod(self.elap_time, 60)
			self.display.text = f"{int(min):02}:{sec:04.1f}"


#test code below
#class app(App):
#	def build(self):
#		sw = StopWatch(text="00:00.0")
#		sw.start()
#		return sw
#		
#app().run()