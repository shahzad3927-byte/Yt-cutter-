from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import os
import re

app = Flask(__name__)

# Premium Ultra Glow Dark Theme (Sabhie Options aur @mr_afsar0000 ID ke saath)
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Cutter Ultra Pro</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { 
            background: radial-gradient(circle at center, #08121f 0%, #02070e 100%); 
            color: #ffffff; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px;
        }
        .card { 
            background: rgba(11, 22, 39, 0.9); 
            border-radius: 24px; 
            border: 2px solid #00f0ff; 
            width: 100%; 
            max-width: 420px; 
            padding: 35px 30px; 
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.25); 
            box-sizing: border-box;
        }
        h1 { 
            color: #ffffff; 
            text-align: center; 
            font-size: 28px; 
            margin-top: 0;
            margin-bottom: 30px; 
            text-shadow: 0 0 12px rgba(0, 240, 255, 0.6);
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .input-group {
            position: relative;
            margin-bottom: 20px;
        }
        .input-group i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #00f0ff;
            font-size: 16px;
        }
        input, select { 
            width: 100%; 
            padding: 14px 14px 14px 45px; 
            background: #050d1a; 
            border: 1px solid #00f0ff; 
            color: #ffffff; 
            border-radius: 12px; 
            box-sizing: border-box; 
            font-size: 14px;
            transition: all 0.3s ease;
        }
        input:focus, select:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            background: #071529;
        }
        select {
            padding-left: 45px;
            cursor: pointer;
            appearance: none;
            -webkit-appearance: none;
        }
        .select-wrapper {
            position: relative;
        }
        .select-wrapper::after {
            content: '\\f107';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #00f0ff;
            pointer-events: none;
        }
        .time-row { 
            display: flex; 
            gap: 15px; 
            margin-bottom: 5px;
        }
        .time-col { 
            width: 50%; 
        }
        .time-col label { 
            display: block; 
            font-size: 12px; 
            color: #00f0ff; 
            margin-bottom: 6px; 
            text-align: left; 
            padding-left: 2px;
            font-weight: 600;
        }
        button { 
            width: 100%; 
            padding: 16px; 
            background: linear-gradient(135deg, #ff0055 0%, #b3003b 100%); 
            border: none; 
            border-radius: 14px; 
            color: white; 
            font-weight: bold; 
            font-size: 16px; 
            cursor: pointer; 
            margin-top: 15px;
            box-shadow: 0 4px 15px rgba(255, 0, 85, 0.35);
            transition: all 0.3s ease;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 0, 85, 0.5);
        }
        .instagram-uid { 
            margin-top: 30px; 
            font-size: 14px; 
            color: #ff007f; 
            font-weight: bold; 
            text-shadow: 0 0 8px rgba(255, 0, 127, 0.5); 
            text-align: center; 
        }
        .instagram-uid a {
            color: #ff007f;
            text-decoration: none;
        }
        .status-msg { 
            display: none; 
            text-align: center; 
            margin-top: 15px; 
            font-weight: 600; 
            font-size: 14px;
        }
        #loading { color: #00f0ff; text-shadow: 0 0 5px rgba(0,240,255,0.4); }
        #error-box { 
            background: rgba(255, 0, 85, 0.1); 
            border: 1px dashed #ff0055; 
            color: #ff4d88; 
            padding: 12px; 
            border-radius: 10px; 
            margin-bottom: 20px;
        }
        .download-box { 
            display: none; 
            margin-top: 25px; 
            text-align: center; 
            background: rgba(0, 240, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(0, 240, 255, 0.2);
        }
        .download-btn {
            display: inline-block;
            background: linear-gradient(135deg, #00f0ff 0%, #00a8ff 100%);
            color: #02070e;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 15px;
            box-shadow: 0 4px 12px rgba(0, 240, 255, 0.3);
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>YT Cutter Ultra Pro</h1>
        
        <div id="error-box" class="status-msg"></div>
        
        <form id="cutter-form">
            <div class="input-group">
                <i class="fa-solid fa-link"></i>
                <input type="text" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            </div>
            
            <div class="time-row">
                <div class="time-col">
                    <label><i class="fa-solid fa-play"></i> Start Time</label>
                    <div class="input-group" style="margin-bottom:0;">
                        <i class="fa-regular fa-clock"></i>
                        <input type="text" name="start_time" placeholder="0:00" value="0:00" required>
                    </div>
                </div>
                <div class="time-col">
                    <label><i class="fa-solid fa-stop"></i> End Time</label>
                    <div class="input-group" style="margin-bottom:0;">
                        <i class="fa-regular fa-clock"></i>
                        <input type="text" name="end_time" placeholder="0:15" value="0:15" required>
                    </div>
                </div>
            </div>
            
            <div class="select-wrapper">
                <i class="fa-solid fa-sliders" style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #00f0ff; z-index: 10;"></i>
                <select name="quality">
                    <option value="best">Video Quality: HD (Best)</option>
                    <option value="1080p">1080p Full HD</option>
                    <option value="720p">720p HD</option>
                    <option value="480p">480p Medium</option>
                </select>
            </div>

            <button type="submit" id="submit-btn">💥 प्रोसेस और डाउनलोड</button>
            <div id="loading" class="status-msg">⏳ वीडियो प्रोसेस हो रहा है, कृपया प्रतीक्षा करें...</div>
        </form>

        <div id="download-section" class="download-box">
            <h4 style="color: #00f0ff; margin: 0 0 10px 0;">🎉 वीडियो सफलतापूर्वक कट हो गया है!</h4>
            <a id="dl-link" href="/download_file" class="download-btn">📥 वीडियो डाउनलोड करें</a>
        </div>
        
        <div class="instagram-uid">
            <i class="fa-brands fa-instagram"></i> Created by: <a href="https://instagram.com/mr_afsar0000" target="_blank">@mr_afsar0000</a>
        </div>
    </div>

    <script>
        document.getElementById('cutter-form').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('submit-btn').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error-box').style.display = 'none';
            document.getElementById('download-section').style.display = 'none';

            fetch('/cut', { method: 'POST', body: new FormData(this) })
            .then(res => res.json())
            .then(data => {
                document.getElementById('submit-btn').style.display = 'block';
                document.getElementById('loading').style.display = 'none';
                if(data.status === 'success') {
                    document.getElementById('download-section').style.display = 'block';
                } else {
                    document.getElementById('error-box').innerText = "❌ " + data.message;
                    document.getElementById('error-box').style.display = 'block';
                }
            }).catch(() => {
                document.getElementById('submit-btn').style.display = 'block';
                document.getElementById('loading').style.display = 'none';
                document.getElementById('error-box').innerText = "❌ सर्वर कनेक्शन एरर!";
                document.getElementById('error-box').style.display = 'block';
            });
        });
    </script>
</body>
</html>
"""

def parse_time(time_str):
    try:
        time_str = time_str.strip()
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
    
    output = "/tmp/final_output.mp4"
    if os.path.exists(output):
        try: os.remove(output)
        except: pass
        
    fmt = 'best[ext=mp4]/best'
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
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([url])
        if os.path.exists(output) and os.path.getsize(output) > 0:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Video cut nahi ho paya, link check karein.'})
    except Exception as e: 
        return jsonify({'status': 'error', 'message': 'Download failed! Link ya server issue hai.'})

@app.route('/download_file')
def download_file(): 
    output = "/tmp/final_output.mp4"
    if os.path.exists(output):
        return send_file(output, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__': 
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            
