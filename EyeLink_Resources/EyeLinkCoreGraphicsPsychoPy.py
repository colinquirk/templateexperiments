# Copyright (C) 2011 Jason Locklin
# Copyright (C) 2016 Zhiguo Wang
# Distributed under the terms of the GNU General Public License (GPL).

# Modified by Colin Quirk - 8/9/2018

# Issues to solve
# 1. The most recent version of Psychopy switched from PIL to the Pillow (a PIL fork)

from psychopy import visual, monitors, event, core, sound
from numpy import linspace
from math import sin, cos, pi
from PIL import Image
import array, string, pylink, psychopy

class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self, tracker, win):
        '''Initialize a Custom EyeLinkCoreGraphics  
        tracker: an eye-tracker instance() 
        win:     the Psychopy display 
            '''
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.display = win
        #self.__target_beep__ = sound.Sound('type.wav')
        #self.__target_beep__done__ = sound.Sound('qbeep.wav')
        #self.__target_beep__error__ = sound.Sound('error.wav')
        self.imgBuffInitType = 'I'
        self.imagebuffer = array.array(self.imgBuffInitType)
        self.pal = None	
        self.size = (384,320)
        self.bg_color = [0, 0, 0]
        self.sizeX = win.size[0]
        self.sizeY = win.size[1]

        # check psychopy version
        self.psychopyVer = psychopy.__version__
        
        # check the screen units of Psychopy and make all necessary conversions for the drawing functions
        self.units = win.units
        self.monWidthCm  = win.monitor.getWidth()
        self.monViewDist = win.monitor.getDistance()
        self.monSizePix  = win.monitor.getSizePix()
        print self.monSizePix
                
        # a conversiont factor to make the screen units right for Psychopy
        self.cfX = 1.0 
        self.cfY = 1.0
        if self.units == 'pix': pass 
        elif self.units == 'height':
            self.cfX = 1.0/self.monSizePix[1]
            self.cfY = 1.0/self.monSizePix[1]
        elif self.units == 'norm':
            self.cfX = 2.0/self.monSizePix[0]
            self.cfY = 2.0/self.monSizePix[1]
        elif self.units == 'cm':
            self.cfX = self.monWidthCm*1.0/self.monSizePix[0]
            self.cfY = self.cfX         
        else: # here comes the 'deg*' units
            self.cfX = self.monWidthCm/self.monViewDist/pi*180.0/self.monSizePix[0]
            self.cfY = self.cfX
            
        # initial setup for the mouse
        self.display.mouseVisible = False
        self.mouse = event.Mouse(visible=False)
        self.mouse.setPos([0,0]) # make the mouse appear at the center of the camera image
        self.last_mouse_state = -1

        # image title
        self.msgHeight = self.size[1]/20.0*self.cfY
        self.title = visual.TextStim(self.display,'', height=self.msgHeight)
        # lines
        self.line = visual.Line(self.display, start=(0, 0), end=(0,0),
                           lineWidth=1.0, lineColor=[0,0,0])
        
    def setTracker(self, tracker):
        self.tracker = tracker
        self.tracker_version = tracker.getTrackerVersion()
        if self.tracker_version >=3:
            self.tracker.sendCommand("enable_search_limits=YES")
            self.tracker.sendCommand("track_search_limits=YES")
            self.tracker.sendCommand("autothreshold_click=YES")
            self.tracker.sendCommand("autothreshold_repeat=YES")
            self.tracker.sendCommand("enable_camera_position_detect=YES")
 
    def setup_cal_display(self):#
        '''This function is called just before entering calibration or validation modes'''
        self.display.color = self.bg_color
        self.title.autoDraw = False
        self.display.flip()

    def clear_cal_display(self):#
        '''Clear the calibration display'''
        self.display.color = self.bg_color
        
    def exit_cal_display(self):#
        '''This function is called just before exiting calibration/validation mode'''
        self.clear_cal_display()

    def record_abort_hide(self):#
        '''This function is called if aborted'''
        pass

    def erase_cal_target(self):#
        '''Erase the calibration or validation target drawn by previous call to draw_cal_target()'''
        self.display.color = self.bg_color
        self.display.flip()

    def draw_cal_target(self, x, y):#
        '''Draw calibration/validation target'''
        xVis = (x - self.sizeX/2)*self.cfX
        yVis = (self.sizeY/2 - y)*self.cfY
        cal_target_out = visual.GratingStim(self.display, tex='none', mask='circle', size=2.0/100*self.sizeX*self.cfX, color=[1.0,1.0,1.0])
        cal_target_in  = visual.GratingStim(self.display, tex='none', mask='circle', size=2.0/300*self.sizeX*self.cfX, color=[-1.0,-1.0,-1.0])
        cal_target_out.setPos((xVis, yVis))
        cal_target_in.setPos((xVis, yVis))
        cal_target_out.draw()
        cal_target_in.draw()
        self.display.flip()


    def play_beep(self, beepid):#
        ''' Play a sound during calibration/drift correct.'''
        pass
        #if beepid == pylink.CAL_TARG_BEEP or beepid == pylink.DC_TARG_BEEP:
        #    self.__target_beep__.play()
        #if beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
        #    self.__target_beep__error__.play()
        #if beepid in [pylink.CAL_GOOD_BEEP, pylink.DC_GOOD_BEEP]:
        #    self.__target_beep__done__.play()

    def getColorFromIndex(self, colorindex):
         '''Return psychopy colors for varius objects'''
         if colorindex    ==  pylink.CR_HAIR_COLOR:         return (1, 1, 1)
         elif colorindex ==  pylink.PUPIL_HAIR_COLOR:       return (1, 1, 1)
         elif colorindex ==  pylink.PUPIL_BOX_COLOR:        return (-1, 1, -1)
         elif colorindex ==  pylink.SEARCH_LIMIT_BOX_COLOR: return (1, -1, -1)
         elif colorindex ==  pylink.MOUSE_CURSOR_COLOR:     return (1, -1, -1)
         else:                                              return (0,0,0)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        '''Draw a line to the display screen. This is used for drawing crosshairs'''
        y1 = (y1 * -1 + self.size[1]/2)*self.cfY
        x1 = (x1 * 1  - self.size[0]/2)*self.cfX
        y2 = (y2 * -1 + self.size[1]/2)*self.cfY
        x2 = (x2 * 1  - self.size[0]/2)*self.cfX

        color = self.getColorFromIndex(colorindex)
        self.line.start     = (x1, y1)
        self.line.end       = (x2, y2)
        self.line.lineColor = color
        self.line.draw()

    def draw_lozenge(self, x, y, width, height, colorindex):
        y = (y * -1 + self.size[1] - self.size[1]/2)*self.cfY
        x = (x * 1  - self.size[0]/2)*self.cfX
        width = width*self.cfX; height = height*self.cfY
        color = self.getColorFromIndex(colorindex)
        
        if width > height:
            rad = height / 2
            if rad == 0: 
                return #cannot draw sthe circle with 0 radius
            #draw the lines
            line1 = visual.Line(self.display, lineColor=color, start=(x + rad, y), end=(x + width - rad, y))
            line2 = visual.Line(self.display, lineColor=color, start=(x + rad, y - height), end=(x + width - rad, y - height))
            
            #draw semicircles
            Xs1 = [rad*cos(t) + x + rad for t in linspace(pi/2, pi/2+pi, 72)]
            Ys1 = [rad*sin(t) + y - rad for t in linspace(pi/2, pi/2+pi, 72)]

            Xs2 = [rad*cos(t) + x - rad + width for t in linspace(pi/2+pi, pi/2+2*pi, 72)]
            Ys2 = [rad*sin(t) + y - rad for t in linspace(pi/2+pi, pi/2+2*pi, 72)]          
            lozenge1 = visual.ShapeStim(self.display, vertices = zip(Xs1, Ys1),
                lineWidth=1.0, lineColor=color, closeShape=False)
            lozenge2 = visual.ShapeStim(self.display, vertices = zip(Xs2, Ys2),
                lineWidth=1.0, lineColor=color, closeShape=False)
        else:
            rad = width / 2

            #draw the lines
            line1 = visual.Line(self.display, lineColor=color, start=(x, y - rad), end=(x, y - height + rad))
            line2 = visual.Line(self.display, lineColor=color, start=(x + width, y - rad), end=(x + width, y - height + rad))

            #draw semicircles
            if rad == 0: 
                return #cannot draw sthe circle with 0 radius

            Xs1 = [rad*cos(t) + x + rad for t in linspace(0, pi, 72)]
            Ys1 = [rad*sin(t) + y - rad for t in linspace(0, pi, 72)]

            Xs2 = [rad*cos(t) + x + rad for t in linspace(pi, 2*pi, 72)]
            Ys2 = [rad*sin(t) + y + rad - height for t in linspace(pi, 2*pi, 72)]

            lozenge1 = visual.ShapeStim(self.display, vertices = zip(Xs1, Ys1),
                lineWidth=1.0, lineColor=color, closeShape=False)
            lozenge2 = visual.ShapeStim(self.display, vertices = zip(Xs2, Ys2),
                lineWidth=1.0, lineColor=color, closeShape=False)    
        lozenge1.draw()
        lozenge2.draw()
        line1.draw()
        line2.draw()

    def get_mouse_state(self):#
        '''Get the current mouse position and status'''
        X, Y = self.mouse.getPos()
        mX = self.size[0]/2 + X*1.0/self.cfX  
        mY = self.size[1]/2 - Y*1.0/self.cfY
        if mX <=0: mX =  0
        if mX > self.size[0]: mX = self.size[0]
        if mY < 0: mY =  0
        if mY > self.size[1]: mY = self.size[1]
        state = self.mouse.getPressed()[0]
        # manually set the mouse position
        newPos = ((mX-self.size[0]/2.0)*self.cfX, (self.size[1]/2.0-mY)*self.cfY)
        print newPos
        self.mouse.setPos(newPos)
        return ((mX, mY), state)


    #the newest function of getting key fron jiye
    def get_input_key(self):
        ky=[]
        for keycode, modifier in event.getKeys(modifiers=True):
            k= pylink.JUNK_KEY
            if keycode   == 'f1': k = pylink.F1_KEY
            elif keycode == 'f2': k = pylink.F2_KEY
            elif keycode == 'f3': k = pylink.F3_KEY
            elif keycode == 'f4': k = pylink.F4_KEY
            elif keycode == 'f5': k = pylink.F5_KEY
            elif keycode == 'f6': k = pylink.F6_KEY
            elif keycode == 'f7': k = pylink.F7_KEY
            elif keycode == 'f8': k = pylink.F8_KEY
            elif keycode == 'f9': k = pylink.F9_KEY
            elif keycode == 'f10': k = pylink.F10_KEY
            elif keycode == 'pageup': k = pylink.PAGE_UP
            elif keycode == 'pagedown': k = pylink.PAGE_DOWN
            elif keycode == 'up': k = pylink.CURS_UP
            elif keycode == 'down': k = pylink.CURS_DOWN
            elif keycode == 'left': k = pylink.CURS_LEFT
            elif keycode == 'right': k = pylink.CURS_RIGHT
            elif keycode == 'backspace': k = ord('\b')
            elif keycode == 'return': k = pylink.ENTER_KEY
            elif keycode == 'space': k = ord(' ')
            elif keycode == 'escape': k = pylink.ESC_KEY
            elif keycode == 'tab': k = ord('\t')
            elif keycode in string.ascii_letters: k = ord(keycode)
            elif k== pylink.JUNK_KEY: key = 0

            if modifier['alt']==True: mod = 256
            else: mod = 0
            
            ky.append(pylink.KeyInput(k, mod))
        return ky

    def exit_image_display(self):#
        '''Called to end camera display'''
        self.clear_cal_display()
        self.display.flip()

    def alert_printf(self,msg):#
        '''Print error messages.'''
        print "alert_printf, " + msg

    def setup_image_display(self, width, height): # 384 x 320 pixels
        self.size = (width,height)
        #self.clear_cal_display()
        self.title.autoDraw = True
        self.last_mouse_state = -1

    def image_title(self, text):#
        '''Draw title text at the bottom of the screen for camera setup'''
        self.title.text = text
        title_pos = (0, 0-self.size[0]/2.0*self.cfY-self.msgHeight)
        self.title.pos = title_pos
        
        
    def draw_image_line(self, width, line, totlines, buff):#
        '''Display image given pixel by pixel'''
        i =0
        while i <width:
            try:
                self.imagebuffer.append(self.pal[buff[i]])
            except:
                break
            i= i+1
                    
        if line == totlines:
            bufferv = self.imagebuffer.tostring()
            if float(self.psychopyVer[:4])<1.83:
                img = Image.fromstring("RGBX", (width, totlines), bufferv)
            else:
                img = Image.frombytes("RGBX", (width, totlines), bufferv)

            imgResize = img.resize((self.size[0], self.size[1]))       
            imgResizeVisual = visual.ImageStim(self.display, image=imgResize)
            
            imgResizeVisual.draw()
            self.draw_cross_hair()    
            self.display.flip()
           
            self.imagebuffer = array.array(self.imgBuffInitType)
            
    def set_image_palette(self, r,g,b): #
        '''Given a set of RGB colors, create a list of 24bit numbers representing the pallet.
        I.e., RGB of (1,64,127) would be saved as 82047, or the number 00000001 01000000 011111111'''
        self.imagebuffer = array.array(self.imgBuffInitType)
        #self.clear_cal_display()
        sz = len(r)
        i =0
        self.pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self.pal.append((rf<<16) | (gf<<8) | (bf))
            i = i+1



