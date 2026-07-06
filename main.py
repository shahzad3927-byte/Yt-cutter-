from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# सुंदर डार्क थीम डिज़ाइन जिसमें इंस्टाग्राम आईडी और क्वालिटी के सारे ऑप्शंस हैं
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Cutter Ultra Pro</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: radial-gradient(circle at center, #00111a 0%, #020508 100%); color: #fff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
        .card { background: rgba(10, 20, 30, 0.95); border-radius: 24px; border: 2px solid #00f0ff; width: 100%; max-width: 430px; padding: 30px; box-shadow: 0 0 35px #00f0ff; position: relative; }
        h1 { color: #fff; text-align: center; font-size: 26px; text-shadow: 0 0 10px #00f0ff; margin-bottom: 25px; }
        input, select { width: 100%; padding: 13px; margin-bottom: 15px; background: #050b11; border: 1px solid #00f0ff; color: #fff; border-radius: 10px; box-sizing: border-box; text-align: center; font-size: 14px; }
        .time-container { display: flex; gap: 10px; margin-bottom: 15px; }
        .time-box { width: 50%; }
        .time-box label { display: block; font-size: 12px; color: #00f0ff; margin-bottom: 5px; text-align: left; padding-left: 5px; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #ff003c 0%, #990024 100%); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 0 15px rgba(255, 0, 60, 0.4); margin-top: 10px; }
        .instagram-uid { margin-top: 25px; font-size: 14px; color: #ff007f; font-weight: bold; text-shadow: 0 0 8px rgba(255,0,127,0.6); text-align: center; }
        .timer-display { display: none; text-align: center; color: #ff003c; margin-top: 15px; font-weight: bold; }
        .player-container { display: none; margin-top: 20px; text-align: center; }
        video { width: 100%; border-radius: 10px; border: 1px solid #00f0ff; }
        .error-msg { display: none; background: rgba(255, 0, 60, 0.2); border: 2px dashed #ff003c; color: #ff3366; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>YT Cutter Ultra Pro</h1>
        <div id="error-box" class="error-msg"></div>
        
        <div id="player-box" class="player-container">
            <video id="video-player" controls></video>
            <br><br>
            <a href="/download_file" style="color: #00f0ff; font-weight: bold; text-decoration: none; font-size: 16px;">📥 वीडियो डाउनलोड करें</a>
        </div>

        <form id="cut-form">
            <input type="text" id="url" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            
            <div class="time-container">
                <div class="time-box">
                    <label><i class="fa-solid fa-play"></i> Start Time (Min:Sec)</label>
                    <input type="text" name="start_time" placeholder="0:00" value="0:00" required>
                </div>
                <div class="time-box">
                    <label><i class="fa-solid fa-stop"></i> End Time (Min:Sec)</label>
                    <input type="text" name="end_time" placeholder="0:15" value="0:15" required>
                </div>
            </div>
            
            <select name="quality">
                <option value="best">Video Quality: HD (Best)</option>
                <option value="1080p">1080p Full HD</option>
                <option value="720p">720p HD</option>
                <option value="480p">480p Medium</option>
            </select>

            <button type="submit" id="submit-btn">💥 प्रोसेस और डाउनलोड</button>
            <div id="timer" class="timer-display">⏳ वीडियो प्रोसेस हो रहा है, कृपया प्रतीक्षा करें...</div>
        </form>
        
        <div class="instagram-uid"><i class="fa-brands fa-instagram"></i> Created by: @shahzad3927</div>
    </div>

    <script>
        document.getElementById('cut-form').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('submit-btn').style.display = "none";
            document.getElementById('timer').style.display = "block";
            document.getElementById('error-box').style.display = "none";
            document.getElementById('player-box').style.display = "none";
            
            fetch('/cut', { method: 'POST', body: new FormData(this) })
            .then(r => r.json())
            .then(data => {
                document.getElementById('submit-btn').style.display = "block";
                document.getElementById('timer').style.display = "none";
                if (data.status === 'success') {
                    document.getElementById('video-player').src = "/stream_video?t=" + new Date().getTime();
                    document.getElementById('player-box').style.display = "block";
                } else {
                    document.getElementById('error-box').innerText = "❌ " + data.message;
                    document.getElementById('error-box').style.display = "block";
                }
            }).catch(err => {
                document.getElementById('submit-btn').style.display = "block";
                document.getElementById('timer').style.display = "none";
                document.getElementById('error-box').innerText = "❌ सर्वर एरर आया!";
                document.getElementById('error-box').style.display = "block";
            });
        });
    </script>
</body>
</html>
"""

def parse_time(time_str):
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            return int(parts[0]) * 60 + int(parts[1])
        return int(time_str)
    except:
        return 0

@app.route('/')
def home(): 
    return render_template_string(HTML)

@app.route('/cut', methods=['POST'])
def cut():
    url = request.form.get('url', '').strip()
    start_str = request.form.get('start_time', '0:00')
    end_str = request.form.get('end_time', '0:15')
    quality_choice = request.form.get('quality', 'best')
    
    start_sec = parse_time(start_str)
    end_sec = parse_time(end_str)
    
    try:
        output = "final_output.mp4"
        if os.path.exists(output): os.remove(output)
        
        fmt = 'best[ext=mp4]'
        if quality_choice == '1080p': fmt = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'
        elif quality_choice == '720p': fmt = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'
        elif quality_choice == '480p': fmt = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]'

        ydl_opts = {
            'format': fmt,
            'outtmpl': output,
            'download_ranges': lambda info, ydl: [{'start_time': start_sec, 'end_time': end_sec}],
            'quiet': True,
            'force_keyframes_at_cuts': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([url])
        return jsonify({'status': 'success'})
    except Exception as e: 
        return jsonify({'status': 'error', 'message': 'वीडियो डाउनलोड या कट करने में दिक्कत आई!'})

@app.route('/stream_video')
def stream_video(): 
    return send_file("final_output.mp4")

@app.route('/download_file')
def download_file(): 
    return send_file("final_output.mp4", as_attachment=True)

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
    
