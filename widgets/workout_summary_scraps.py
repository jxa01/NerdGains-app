<ExerSum>:
	orientation: 'horizontal'
	canvas.before:
		Color:
			rgba: [0.082, 0.047, 0.46, 1]
		RoundedRectangle:
			radius: (30,)
			pos: self.pos
			size: self.size
			
	Label: 
		text: root.t1_txt
	BoxLayout:
		orientation: 'vertical'
		Label: 
			text: root.t2_txt
		Label: 
			text: root.d1_txt
	BoxLayout:
		orientation: 'vertical'
		Label: 
			text: root.t3_txt
		Label: 
			text: root.d2_txt			
	
	ExerRv:
		viewclass: 'ExerSum'
		RecycleBoxLayout:
			orientation: 'vertical'
			spacing: 20
			padding: 100
			size_hint_y: None
			height: self.minimum_height
			default_size: None, dp(90)
			default_size_hint: 1, None
			

#.py file			
#exercise summary widget for the recycleview to populate
class ExerSum(BoxLayout):
	t1_txt = StringProperty("exercise")
	t2_txt = StringProperty("set count")
	t3_txt = StringProperty("intensity")
	d1_txt = StringProperty("data")
	d2_txt = StringProperty("data")
	
#a recycleview of all the exercise summaries for the session
class ExerRv(RecycleView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		list = [{'t1_txt': f'exercise {x}', 'd1_txt': f'{x}'} for x in range(30)]
		self.data = list