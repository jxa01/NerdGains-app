from debug import log	
from kivy.app import App
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty, ListProperty, NumericProperty

class NavBar(BoxLayout):
	bar_title = StringProperty("[b]NerdGains[/b]")
		
class MyDropDownBase(DropDown):
	pass
		
class DropButton(Button):
	bg_color = ListProperty([1, 1, 1, 0])
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):		
			self.bg_color = App.get_running_app().Colors['secondary']
		return super().on_touch_down(touch)
		
	def on_touch_up(self, touch):
		if self.collide_point(*touch.pos):
			anim = Animation(bg_color=App.get_running_app().Colors['primary'], duration=0.1)
			anim.start(self)
		return super().on_touch_up(touch)
		
class MyDropDown(DropButton):	
	__events__ = ('on_select',)	
	values = ListProperty([])
	ddwidth = NumericProperty(dp(100))	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)		
		self.dd = MyDropDownBase()
		self.bind(ddwidth=lambda instance, value: setattr(self.dd, 'width', value))
		self.dd.width = self.ddwidth
		self.bind(on_release=lambda btn_inst: self.dd.open(btn_inst))
		self.dd.bind(on_select=lambda inst, value: self.dispatch("on_select", value))
			
		
	def on_values(self, instance, value):
		self.dd.clear_widgets()
		for val in self.values:
			btn = DropButton()
			btn.text = val
			btn.size_hint_y = None
			btn.height = App.get_running_app().Sizes['normal_line']
			btn.bind(on_release=lambda btn_inst, v=val: self.dd.select(v))
			self.dd.add_widget(btn)
			
	def on_select(self, value):
		pass