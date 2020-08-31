from multiprocessing import Process,Manager
from flask import Flask,request,render_template
from led_control import LedControl
import time
import os
LED_COUNT = 70

app = Flask(__name__)
cmd_queue = Manager().Queue()
led_control = LedControl(7,10,3,21)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/led')
def led():
    mod = request.args.get('m', '0')
    function = request.args.get('f','0')
    led_row = request.args.get('r','0')
    led_column = request.args.get('c','0')
    cycle = request.args.get('k','30')
    delay = request.args.get('d','10')
    data = {"mod":int(mod),"function":int(function),"led_row":int(led_row),
            "led_column":int(led_column),"cycle":int(cycle),"delay":int(delay),
            "time":time.time()}
    
    if(led_control.dynamic==False):
        cmd_queue.put(data)
    return "recieve"

@app.route('/color',methods = ['POST', 'GET'])
def color():
    rows =led_control.rows
    cols = led_control.columns
    if request.method == 'POST':
        result = request.form
        colors = []
        for value in result.values():
            colors.append(value)
        return render_template("color.html",rows=rows,cols=cols,colors=colors)
    else:
        colors = ["#D43B5E","#C54269","#B84873","#A55182","#7268A7",
                "#5378C0","#3784D4","#1B91EA","#099BF8","#019FFF"]
        result = request.args
        if(len(result)>0):
            colors = []
           
        for key,value in result.items():
            colors.append(value)
       
        for row in range(0,rows):
            for col in range(0,cols):
                data = {"mod":2,"color":colors[row],"led_row":row,"led_column":col}
                cmd_queue.put(data)    
        data = {"mod":99}
        cmd_queue.put(data) 
        return render_template("color.html",rows=rows,cols=cols,colors=colors)

def _light(cmd_queue):
    
    while(True):
        led_control.light()
        try:
            data = cmd_queue.get(True,0.01)
        except:
            pass
        else:
            print("get data:",data)
            if(time.time()-data["time"]<2):
                print("处理")
                led_control.del_cmd(data)
            else:
                print("超时不处理")
            
def _play_music():
    os.system("mplayer -af volume=10  -loop 0 /home/pi/ledcontrol/dabeizhou1.mp3")

if __name__ == '__main__':

 #   data = {"mod":1,"function":7, "cycle":1,"delay":1}
 #   cmd_queue.put(data)
 #   data = {"mod":1,"function":6, "cycle":1,"delay":1}
 #   cmd_queue.put(data)
 #   data = {"mod":1,"function":5, "cycle":1,"delay":1}
 #   cmd_queue.put(data)
 #   data = {"mod":1,"function":4, "cycle":1,"delay":1}
  #  cmd_queue.put(data)
 #   data = {"mod":1,"function":3, "cycle":1,"delay":1}
 #   cmd_queue.put(data)
 #   data = {"mod":1,"function":2, "cycle":1,"delay":1}
 #   cmd_queue.put(data)
 #   data = {"mod":1,"function":1, "cycle":1,"delay":1}
#    cmd_queue.put(data)
    data = {"mod":0,"function":0,"led_row":-1,
        "led_column":-1,"cycle":60,"delay":10,"time":time.time()}
    cmd_queue.put(data)
    
    p = Process(target=_play_music)
    p.daemon = True
    p.start()


    process = Process(target=_light,args=(cmd_queue,))
    process.daemon = True
    process.start()
    app.run(host='0.0.0.0')

   