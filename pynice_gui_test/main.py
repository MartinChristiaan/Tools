from copy import copy
import PIL
import numpy as np


time = np.arange(3000)
bbox_x = np.arange(3000)


import plotly.graph_objects as go
from nicegui import ui


fig = go.Figure(go.Scatter(x=time, y=bbox_x))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
plot = ui.plotly(fig).classes('w-full h-200')

def handle(x):
	fig_new = copy(fig)
	fig_new.add_vline(x=x.args['points'][0]['x'])
	plot.update_figure(fig_new)


image=  np.ones((100,100,3), np.uint8) * 128
image = PIL.Image.fromarray(image)
img = ui.image(image)

def on_click(x):

	image=  np.ones((100,100,3), np.uint8) * 0
	image = PIL.Image.fromarray(image)
	img.set_source(image)


plot.on('plotly_hover', handle)
plot.on('click', on_click)
ui.run()