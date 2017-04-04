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
	self._prevKnob = [0., 0., 0., 0.]
        self._touches = []

        oscAPI.init()  
        dialOSC = oscAPI.listen(ipAddr=self.ip, port=self.recvPort) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(dialOSC), 0)
        oscAPI.bind(dialOSC, self.dialListener, '/tuios/tok')   

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY

#### MY VERSION, WORKS #####
#    def setRotationX(self, x):
#        self.renderer.rotx.angle = x

#    def setRotationY(self, y):
#        self.renderer.roty.angle = y
  
#    def setRotation(self, x, y):
#        self.renderer.rotx.angle = x
#        self.renderer.roty.angle = y

#    def zoom(self, zoom):
#        print self.renderer.camera_translate
#        if (self.renderer.camera_translate[2] + zoom < 30 and 
#                self.renderer.camera_translate[2] + zoom > 0):
#            self.renderer.camera_translate[2] += zoom


#    def setZoom(self, zoom):
#        self.renderer.camera_translate[2] = zoom

###### END COMMENTING #####

    def zoom(self, scale):
	xyz = self.renderer.scale.xyz
	if (xyz[0] + scale > 0):
		self.renderer.scale.xyz = tuple(p + scale for p in xyz)

    def reset(self):
	self.renderer.rotx.angle = 0
	self.renderer.roty.angle = 0
	self.renderer.scale.xyz = (1,1,1)

    def setSlide(self, slide):
        oscAPI.sendMsg('/tuios/tok', [slide], ipAddr= self.ip, port=self.sendPort)

    def dialListener(self, value, instance):
        # print ("value", value, "instance:", instance)
        knob = value[2] - 1
        angle = (value[7])

        if (value[8] == 1):
            self._prevKnob[knob] = -1.
            print "place"
        elif (self._prevKnob[knob] == -1.):
            self._prevKnob[knob] = angle
            print "set"
        else:
            delta = angle - self._prevKnob[knob]
            self._prevKnob[knob] = angle
            if (abs(delta) > 100):
                delta = 0
            print "move:", delta

            if (knob == 0):
                self.rotate(0,delta)
            elif (knob == 1):
                self.rotate(delta,0)
            elif (knob == 2):
                self.zoom(delta*.01)
            elif (knob == 3):
		print "\n\n\nslide knob\n\n\n"
		self.setSlide(angle)



### MY VERSION, WORKS #####
#    def dialListener(self, value, instance):
#        print ("value", value, "instance:", instance)
#        knob = value[2]
#        try:
#            angle = float(value[7])
#        except:
#            angle = 1
#        if (knob == 1):
#            self.setRotationX(angle)
#        elif (knob == 2):
#            self.setRotationY(angle)
#        elif (knob == 3):
#            self.setZoom(angle/360 * 30)
#        elif (knob == 4):
#            self.setSlide(angle)