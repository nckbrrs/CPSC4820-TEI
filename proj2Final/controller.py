from kivy.core.window import Window
import sys
from ui import UI
from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class Controller():
    def __init__(self, **kwargs):
        self.ip = "127.0.0.1"
        self.recvPort = 5000
	self.sendPort = 5001
        self.renderer = kwargs['renderer']

        oscAPI.init()  
        dialOSC = oscAPI.listen(ipAddr=self.ip, port=self.recvPort) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(dialOSC), 0)
        oscAPI.bind(dialOSC, self.dialListener, '/tuios/tok')   

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY

    def zoom(self, scale):
	xyz = self.renderer.scale.xyz
	if (xyz[0] + scale > 0):
		self.renderer.scale.xyz = tuple(p + scale for p in xyz)

    def reset(self):
	self.renderer.rotx.angle = 0
	self.renderer.roty.angle = 0
	self.renderer.scale.xyz = (1,1,1)

    def setSlide(self, angle):
	if (angle > -1 and angle < 121):
		self.renderer.roty.angle = 0
		slide = 1
	if (angle > 120 and angle < 241):
		slide = 2
	if (angle > 240 and angle < 361):
		slide = 3

        oscAPI.sendMsg('/tuios/tok', [slide], ipAddr= self.ip, port=self.sendPort)

    def dialListener(self, value, instance):
        angle = (value[7])
	self.setSlide(angle)
