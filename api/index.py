from flask import Flask,jsonify, render_template,request
from pytube import YouTube
import io
import base64

app = Flask(__name__)


data = {
    "readable": False,
    "data":[]
}

@app.route('/')
def home():
    return render_template('youtube-video-download-online.html')

@app.route('/instagram-reel-download-online')
def instagram():
    return render_template('comingsoon.html')

@app.route('/youtube-reel-download-online')
def ytreel():
    return render_template('youtube-reel-download-online.html')

@app.route('/youtube-video-download-online')
def ytvideo():
    return render_template('youtube-video-download-online.html')

@app.route('/getVideo',methods=['POST'])
def getVideo():
    if request.method == 'POST':
        try:
            payload = request.get_json()
            url = payload.get('requestedUrl')
            # url = 'https://www.youtube.com/watch?v=K4TOrB7at0Y'
            
            if url.count('youtube') == 1:
                yt = YouTube(url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4')[0] #.order_by('resolution').desc().first()

                # Stream the video content directly to the client
                # def generate():
                #     for chunk in stream.iterable:
                #         yield chunk

                video_buffer = io.BytesIO()
                stream.stream_to_buffer(video_buffer)
                video_buffer.seek(0)
                video_data = video_buffer.read()

                # Convert the video data to Base64
                video_base64 = base64.b64encode(video_data).decode('utf-8')

                # response = Response(video_buffer.read(), content_type='video/mp4')
                # response.headers['Cache-Control'] = 'no-cache'
                # response.headers['Content-Disposition'] = 'attachment; filename="video.mp4"'

                return jsonify({
                    'videoBase64':video_base64
                })
                    
            # return jsonify({
            #     'result':'you got it man!'
            # })
        except Exception as err:
            return jsonify({
                'result':str(err)
            })
