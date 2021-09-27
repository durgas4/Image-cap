from flask import Flask, render_template, Response, request
import cv2
import datetime, time
#import sys
global capture,rec_frame,rec, out 
capture=0
switch=1
rec=0

#instatiate flask app  
global app
app = Flask(__name__, template_folder='./templates')
camera = cv2.VideoCapture(0)

def record(out):
    
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def gen_frames():
    global out, rec_frame
    # generate frames
    
    while True:
        success, frame = camera.read() 
        if success:
           
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Shots begin...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
 
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests',methods=['POST','GET'])
def tasks():
    global out
   
    if request.method == 'POST':

        if  request.form.get('rec') == 'Start Recording':
            global rec
            rec= not rec
            capture_duration=1
            cap = cv2.VideoCapture(0)
            rec, frame = cap.read()
            start_time = time.time()
            count=0
            #while( int(time.time() - start_time) < capture_duration ):
            if(rec):
                while( int(time.time() - start_time) < capture_duration ):                   
                    rec, frame = cap.read()
                    now=datetime.datetime.now()
                    out = cv2.imwrite('img_{}.jpg'.format(str(now).replace(":",'')),frame)
                    #out = cv2.imwrite('img%d.jpg'%count,frame)
                    count+=1
        camera.release()
    return 'Task Done!'


# main program                

if __name__ == '__main__':
    app.run()


