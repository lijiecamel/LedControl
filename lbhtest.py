import time
import random
from rpi_ws281x import PixelStrip, Color
from led import LED

wan = [ [1,1,1,0,1],
        [0,0,1,0,1],
        [1,1,1,1,1],
        [1,0,1,0,0],
        [1,0,1,1,1]]

zhong = [[0,0,1,0,0],
         [1,1,1,1,1],
         [1,0,1,0,1],
         [1,1,1,1,1],
         [0,0,1,0,0]]


#renamed to prevent unexpected errors
class lbhtest():


    def __init__(self,rows,columns,serial_type=1,led_pin=18):
        ## 
        # serial_type 信号线连接方式， 1表示弓字形连线，2表示Z字形连线
        ##
        self.rows = rows
        self.columns = columns
        self.led_numbers = rows*columns
        self._mod = 1
        self.leds = []
        for i in range(self.led_numbers):
            self.leds.append(LED(i))

        self.led_index = [[0 for i in range(self.columns)] for i in range(self.rows)]
        if(serial_type == 1):
            for i in range(0,rows,2):
                for j in range(0,self.columns):
                    self.led_index[i][j] = i*self.columns+j
            
            for i in range(1,rows,2):
                for j in range(0,self.columns):
                    self.led_index[i][j] = (i+1)*self.columns-(j+1)
        elif(serial_type==2):
            for i in range(0,rows):
                for j in range(0,columns):
                    self.led_index[i][j]= i*self.columns+j
            
        self.strip =  PixelStrip(self.led_numbers, led_pin)
        self.strip.begin()
        self.strip.setBrightness(255)  

    def del_cmd(self,paras):
        self._mod = paras["mod"]

        if(paras["mod"]==1): # 全体显示
            if(paras["function"]==0):
                self._symbolLeftToRight(wan,Color(100,100,0),500)
            elif(paras["function"]== 1):
                self._symbolRightToLeft(wan,Color(100,100,0),500)
            elif(paras["function"]==2):
                self._leftToRight(Color(100,100,0),50)
            elif(paras["function"]==3):
                self._symbolLeftToRight(zhong,Color(100,100,0),500)
            elif(paras["function"]==4):
                self._leftToRight(Color(100,100,0),50)
            elif(paras["function"]==5):
                self._rightToLeft(Color(100,100,0),50)
            elif(paras["function"]==6):
                self._bottomToTop(Color(100,100,0),50)
            elif(paras["function"]==7):
                self._topToBottom(Color(100,100,0),50)    
        elif(paras["mod"]==0): #单个显示
            row = paras["led_row"]-1
            col = paras["led_column"]-1
            led_index = self.led_index[row][col]
            self.leds[led_index]._set_color(0)
            self.leds[led_index]._set_cycle(paras["cycle"])
            self.leds[led_index]._set_delay(paras["delay"])

    def light(self):
        if(self._mod == 0): # 单个显示            
            for i in range(self.led_numbers):
                if(self.leds[i]._recycle>0):
                    color = self.leds[i].get_cur_color()
                    if(not color is None):
                        self.strip.setPixelColor(i,color)
                        print("第i个灯",i,color)
                        self.strip.show()
               

    def _showGivenSymbolAt(self,symbol,x,y,color,bgcolor=Color(0,0,0)):
        m = len(symbol)
        n = len(symbol[0])   
        for i in range(m):
            for j in range(n):
                if(symbol[i][j]==1):
                    self.strip.setPixelColor( self.led_index[i+x][j+y],color)
                else:
                    self.strip.setPixelColor(self.led_index[i+x][j+y],bgcolor)
        self.strip.show()
 

    def _colorWipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.led_numbers):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def _theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i + q, 0)


    def _wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def _rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.led_numbers):
                self.strip.setPixelColor(i, self._wheel((i + j) ))
                
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


    def _rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.led_numbers):
                self.strip.setPixelColor(i, self._wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def _theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i+q, self._wheel((i + j) ))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i+q, Color(0,0,0))
                self.strip.show()


    def _leftToRight(self,color,wait_ms=50):
        for j in range(self.columns):
            for i in range(self.rows):
                self.strip.setPixelColor(self.led_index[i][j],color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)


    def _rightToLeft(self,color,wait_ms=50):
        for j in reversed(range(self.columns)):
            for i in range(self.rows):
                self.strip.setPixelColor(self.led_index[i][j],color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def _topToBottom(self,color,wait_ms=50):
        for i in range(self.rows):
            for j in range(self.columns):
                self.strip.setPixelColor(self.led_index[i][j],color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def _bottomToTop(self,color,wait_ms=50):
        for i in reversed(range(self.rows)):
            for j in range(self.columns):
                self.strip.setPixelColor(self.led_index[i][j],color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def _symbolLeftToRight(self,symbol,color,wait_ms):
        for j in range(self.columns-len(symbol[0])):
            self._showGivenSymbolAt(symbol,0,j,color)
            time.sleep(wait_ms/1000.0)
            self._colorWipe(Color(0,0,0))

    def _symbolRightToLeft(self,symbol,color,wait_ms):
        for j in reversed(range(self.columns-len(symbol[0]))):
            self._showGivenSymbolAt(symbol,0,j,color)
            time.sleep(wait_ms/1000.0)
            self._colorWipe(Color(0,0,0))        

if __name__ == "__main__":
    lbhtest = lbhtest(1,36,1,21)
    lbhtest.strip.setBrightness(255)  
    lbhtest._colorWipe(Color(255,255,255))
    #GRB
    #time.sleep(1)
    #lbhtest.strip.setBrightness(200)
    #lbhtest._leftToRight(50)
    #time.sleep(0.5)    
    #lbhtest._colorWipe(Color(255,255,255))
    #time.sleep(1)
    #lbhtest._rightToLeft(80)
    #time.sleep(1)
    #lbhtest._rainbowCycle(20,50)
    #lbhtest._theaterChaseRainbow(50)
    

# 150  415W

