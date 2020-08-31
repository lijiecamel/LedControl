import time
import random
from multiprocessing import Process
import threading
from rpi_ws281x import PixelStrip, Color
from led import LED
import tts

wanFive = [[1, 1, 1, 0, 1],
           [0, 0, 1, 0, 1],
           [1, 1, 1, 1, 1],
           [1, 0, 1, 0, 0],
           [1, 0, 1, 1, 1]]

wanSeven = [[1, 1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 1, 1]]


sanjiaobo = [[0,0,1,0,0],
             [0,1,0,1,0],
             [1,0,0,0,1]
            ]

rect1 = [[1,1,1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1,1,1]]

rect2 = [[0,0,0,0,0,0,0,0,0,0],
         [0,1,1,1,1,1,1,1,1,0],
         [0,1,0,0,0,0,0,0,1,0],
         [0,1,0,0,0,0,0,0,1,0],
         [0,1,0,0,0,0,0,0,1,0],
         [0,1,1,1,1,1,1,1,1,0],
         [0,0,0,0,0,0,0,0,0,0]]

rect3 = [[0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,1,1,1,1,1,1,0,0],
         [0,0,1,0,0,0,0,1,0,0],
         [0,0,1,1,1,1,1,1,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0]]

rect4 = [[0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,1,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0]]            

class LedControl():


    def __init__(self,rows,columns,serial_type=1,led_pin=18):
        self.dynamic = False
        ## 
        # serial_type 信号线连接方式， 1表示弓字形连线，2表示Z字形连线
        # 3表示弓字形连线，线从左下角接入，左上角是第1行第1列
        ## 4表示弓字形连线，带背光，底座0-背光0-底座1-背光1---的顺序
        ##
        self.rows = rows
        self.columns = columns
        self.led_numbers = rows*columns
        if(serial_type==4):
            self.led_numbers = rows*columns*2
        self._mod = 1
        self._type = serial_type
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

        elif(serial_type==3):
            for i in range(rows-1,-1,-2):
                for j in range(0,columns):
                    self.led_index[i][j]=j

            for i in range(rows-2,-1,-2):
                for j in range(0,columns):
                    self.led_index[i][j]=columns-1-j
            
            for row in range(0,rows):
                for j in range(0,columns):
                    self.led_index[row][j] = (rows-row-1)*columns+self.led_index[row][j]
        elif(serial_type==4):
            self.led_index[0][0]=6
            self.led_index[0][1]=4
            self.led_index[1][0]=0
            self.led_index[1][1]=2
           
        self.strip =  PixelStrip(self.led_numbers, led_pin)
        self.strip.begin()
        self.strip.setBrightness(255)  

    def del_cmd(self,paras):
        print("deal cmd：",paras)
        self._mod = paras["mod"]

        if(paras["led_row"]<0):
            if(self.dynamic==False):
                self.dynamic = True
                self._start()
                self.dynamic=False
            return
            
        if(paras["mod"]==1): # 全体显示
            if(paras["function"]==0):
                self._symbolLeftToRight(wanFive,Color(100,100,0),500)
            elif(paras["function"]== 1):
                self._symbolRightToLeft(wanFive,Color(100,100,0),500)
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
            if(self._type==4):
                led_index = led_index+1
                self.leds[led_index]._set_color(0)
                self.leds[led_index]._set_cycle(paras["cycle"])
                self.leds[led_index]._set_delay(paras["delay"])

            t = threading.Thread(target=tts.tts,args=(row,col))
            t.start()
            
        elif(paras["mod"]==2): #指定颜色
            row = paras["led_row"]
            hex_color = paras['color']
            
            g = int(hex_color[1:3],16)
            r = int(hex_color[3:5],16)
            b = int(hex_color[5:7],16)
            print("led_control",row,hex_color,r,g,b)
            for col in range(self.columns):
                led_index = self.led_index[row][col]
                self.strip.setPixelColor(led_index,Color(r,g,b))
        elif(paras["mod"]==99):
            self.strip.show()

    def linearGradient(self,hex_color1,hex_color2,hex_color3,hex_color4,deg=0):
        pass
   
    def light(self):
        if(self._mod == 0): # 单个显示            
            for i in range(self.led_numbers):
                if(self.leds[i]._recycle>0):
                    color = self.leds[i].get_cur_color()
                    if(not color is None):
                        self.strip.setPixelColor(i,color)
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
                self.strip.setPixelColor(i, self._wheel((i + j) & 255))
                
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

    '''def _theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i+q, self._wheel((i + j) ))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.led_numbers, 3):
                    self.strip.setPixelColor(i+q, Color(0,0,0))
                self.strip.show()'''

    def _theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256*5):
            for q in range(10):
                for i in range(0, self.led_numbers, 10):
                    self.strip.setPixelColor(i+q, self._wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                
                for i in range(0, self.led_numbers+10, 10):
                    self.strip.setPixelColor(i+q-5, Color(0,0,0))
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

    def _showGivenSymbolAt(self,symbol,x,y,color,bgcolor=Color(0,0,0)):
        m = len(symbol)
        n = len(symbol[0])   
        if(m+x>self.rows):
            print('灯的行数太少，无法显示符号')
            return
        for i in range(m):
            for j in range(n):
                if(symbol[i][j]==1):
                    self.strip.setPixelColor( self.led_index[i+x][j+y],color)
                else:
                    self.strip.setPixelColor(self.led_index[i+x][j+y],bgcolor)
        self.strip.show()

    def _symbolLeftToRight(self,symbol,color,wait_ms):
        for j in range(self.columns-len(symbol[0])):
            self._showGivenSymbolAt(symbol,5,j,color)
            time.sleep(wait_ms/1000.0)
            self._colorWipe(Color(0,0,0))

    def _symbolRightToLeft(self,symbol,color,wait_ms):
        for j in reversed(range(self.columns-len(symbol[0]))):
            self._showGivenSymbolAt(symbol,5,j,color)
            time.sleep(wait_ms/1000.0)
            self._colorWipe(Color(0,0,0))        

    def _start(self,):  #全体动态效果
        self._colorWipe(Color(0,0,0))
        time.sleep(1)
        for row in range(self.rows):
            for col in range(self.columns):
                self.strip.setPixelColor(self.led_index[row][col],Color(100,165,0))
                #self.strip.setPixelColor(self.led_index[row][col]+1,Color(100,165,0))
                self.strip.show()
                time.sleep(0.2)

        self._colorWipe(Color(0,0,0))
        time.sleep(1)

        for col in range(self.columns):
            for row in range(self.rows):
                self.strip.setPixelColor(self.led_index[row][col],Color(100,165,0))
                #self.strip.setPixelColor(self.led_index[row][col]+1,Color(100,165,0))
            self.strip.show()
            time.sleep(0.2)

        self._colorWipe(Color(0,0,0))
        time.sleep(1)
        for row in range(self.rows):
            for col in range(self.columns):
                self._colorWipe(Color(0,0,0))
                self.strip.setPixelColor(self.led_index[row][col],Color(100,165,0))
                #self.strip.setPixelColor(self.led_index[row][col]+1,Color(100,165,0))
                self.strip.show()
                time.sleep(0.2)

        self._colorWipe(Color(100,165,0))        
    
        for kkk in range(2):
            self._colorWipe(Color(0,0,0))

            for kkkk in range(3):
                for i in range(4):
                    self._colorWipe(Color(0,0,0))
                    self._showGivenSymbolAt(wanFive,1,i,Color(100,165,0))
                    time.sleep(1)
            for kkkk in range(3):
                for i in range(4):
                    self._colorWipe(Color(0,0,0))
                    self._showGivenSymbolAt(wanSeven,0,i,Color(180,150,0))
                    time.sleep(1)
                
            self._colorWipe(Color(0,0,0))    
            index_list = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,
                69,68,67,66,65,64,63,62,61,51,41,31,21,11,12,13,14,
                15,16,17,18,19,29,39,49,59,58,57,56,55,54,53,52,42,
                32,22,23,24,25,26,27,28,38,48,47,46,45,44,43,33,34,35,36,37]
                
            
            for index in index_list:
                index = index -1
                row = int(index/10)
                col = int(index%10)
                #print("row,col:",row,col,self.led_index[row][col])
                self.strip.setPixelColor(self.led_index[row][col],Color(100,165,0))
                self.strip.show()
                time.sleep(0.2)
            for index in reversed(index_list):
                index = index -1
                row = int(index/10)
                col = int(index%10)
                #print("row,col:",row,col,self.led_index[row][col])
                self.strip.setPixelColor(self.led_index[row][col],Color(0,0,0))
                self.strip.show()
                time.sleep(0.2)

            for kkkkk in range(3):
                self._showGivenSymbolAt(rect1,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect2,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect3,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect4,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect3,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect2,0,0,Color(100,165,0))
                time.sleep(1)
                self._showGivenSymbolAt(rect1,0,0,Color(100,165,0))
                time.sleep(1)
            

            for i in range(self.rows):
                for j in range(self.columns):
                    self._colorWipe(Color(0,0,0))
                    self.strip.setPixelColor(self.led_index[i][j],Color(100,165,0))
                    self.strip.show()
                    time.sleep(0.2)
            
            for i in reversed(range(self.rows)):
                for j in reversed(range(self.columns)):
                    self._colorWipe(Color(0,0,0))
                    self.strip.setPixelColor(self.led_index[i][j],Color(100,165,0))
                    self.strip.show()
                    time.sleep(0.2)


            time.sleep(1)
            for i in range(self.rows):
                self._colorWipe(Color(0,0,0))
                for j in range(self.columns):
                    self.strip.setPixelColor(self.led_index[i][j],Color(50,255,50))
                self.strip.show()
                time.sleep(1)

            self._colorWipe(Color(0,0,0))
            time.sleep(1)
            self._topToBottom(Color(255,100,100),500)
            time.sleep(1)
            self._colorWipe(Color(0,0,0))
            self._bottomToTop(Color(100,165,0),500)

            self._colorWipe(Color(0,0,0))
            self._rainbowCycle()
            time.sleep(1)
            
            self._colorWipe(Color(0,0,0))
            self._theaterChaseRainbow(60)
            
            self._colorWipe(Color(0,0,0))
            for i in range(10):
                self._showGivenSymbolAt(wanSeven,0,2,Color(100,165,0))
                time.sleep(1)
                self._colorWipe(Color(0,0,0))
                time.sleep(1)

            
        # 颜色空间(G,R,B)
        self._colorWipe(Color(100,165,0))
    
if __name__ == "__main__":

    led_control = LedControl(7,10,3,21)
    led_control.strip.setBrightness(255)
    led_control._colorWipe(Color(0,0,0))
    led_control._start()

    #led_control._start()
    # 白光常亮
    # led_control._colorWipe(Color(255,255,255))
   
    # led_control._colorWipe(Color(255,0,255))
    # 佛像RGB(195,150,47)
    # led_control._colorWipe(Color(150, 195, 47))
    #led_control._rainbowCycle()
