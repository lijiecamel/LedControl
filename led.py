import time
from rpi_ws281x import  Color
# 颜色空间为 (G,R,B)
FiveColor= [Color(255,0,0),Color(100,165,0),Color(0,255,0),Color(100,100,0),Color(0,100,255)]
BaseColor = Color(100,165,0) #底色
ColorList = []
ColorList.append(FiveColor)

class LED():
    
    def __init__(self,id):
        self._led_id = id
        self._index_color_list = 0
        self._recycle = -1
        self._cur_color_index = 0
        self._last_time = 0
        self._on_delay = 10 #亮灯时间，以100ms为单位

    def _set_color(self,color_id):
        self._index_color_list = color_id
        self._last_time = time.time()

    def _set_cycle(self, cycle):
        self._recycle = cycle
        self._cur_color_index = -1
        self._last_time = 0
    
    def _set_delay(self,_on_delay):
        self._on_delay = _on_delay

    def get_cur_color(self):
        if(time.time()-self._last_time> 0.1*self._on_delay):
            self._last_time = time.time()
            self._cur_color_index +=1 

            if(self._cur_color_index>=len(ColorList[self._index_color_list])):
                self._cur_color_index = 0
                self._recycle -=1
            
            if self._recycle>0:
                
                return ColorList[self._index_color_list][self._cur_color_index]
            else:
                return BaseColor
        else:
            return None

            

         
