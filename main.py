From flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Cutter Ultra Pro v8.5</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: radial-gradient(circle at center, #00111a 0%, #020508 100%); color: #fff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
        *, *::before, *::after { box-sizing: border-box; }
        .card { background: rgba(10, 20, 30, 0.95); border-radius: 24px; border: 2px solid #00f0ff; width: 100%; max-width: 430px; padding: 30px; box-shadow: 0 0 35px #00f0ff, inset 0 0 15px rgba(0, 240, 255, 0.2); }
        .insta-branding { display: flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); padding: 12px; border-radius: 50px; margin-bottom: 20px; box-shadow: 0 0 15px rgba(220, 39, 67, 0.6); text-decoration: none; color: #fff; font-weight: bold; }
        .insta-branding i { font-size: 20px; margin-right: 10px; }
        h1 { color: #fff; text-align: center; margin-top: 0; margin-bottom: 25px; font-size: 26px; text-shadow: 0 0 10px #00f0ff, 0 0 20px #ff003c; font-weight: 900; }
        .section-title { font-size: 12px; color: #00f0ff; margin-top: 15px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; text-shadow: 0 0 5px rgba(0, 240, 255, 0.5); }
        input, select { width: 100%; padding: 13px; margin-bottom: 5px; background: #050b11; border: 1px solid #00f0ff; color: #fff; border-radius: 10px; font-size: 14px; }
        input:focus, select:focus { border-color: #ff003c; box-shadow: 0 0 15px #ff003c; outline: none; }
        .timer-display { display: none; text-align: center; font-size: 16px; color: #ff003c; font-weight: bold; margin-top: 15px; margin-bottom: 10px; text-shadow: 0 0 10px #ff003c; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #ff003c 0%, #990024 100%); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 0 20px #ff003c; text-transform: uppercase; margin-top: 15px; }
        .player-container { margin-top: 5px; margin-bottom: 25px; text-align: center; border: 2px dashed #ff003c; padding: 15px; border-radius: 14px; background: #050002; box-shadow: 0 0 20px rgba(255, 0, 60, 0.4); }
        video { width: 100%; border-radius: 10px; border: 1px solid #ff003c; }
        .help-btn { position: fixed; bottom: 20px; right: 20px; background: #ff003c; color: #fff; padding: 12px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; z-index: 9999; }
        
        .error-msg { background: rgba(255, 0, 60, 0.15); border: 2px dashed #ff003c; color: #ff3366; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; font-size: 14px; }
        
        .spinner { display: inline-block; width: 22px; height: 22px; border: 3px solid rgba(255,0,60,.3); border-radius: 50%; border-top-color: #ff003c; animation: spin 0.8s linear infinite; margin-right: 10px; vertical-align: middle; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="card">
        <a href="https://instagram.com/mr_afsar0000" target="_blank" class="insta-branding">
            <i class="fab fa-instagram"></i> Follow Me: @mr_afsar0000
        </a>
        <h1>YT Cutter Ultra Pro</h1>
        
        {% if error_text %}
        <div class="error-msg">❌ {{ error_text }}</div>
        {% endif %}

        {% if video_ready %}
        <div class="player-container">
            <div class="section-title" style="color: #ff003c; font-weight: bold;">📺 आपका वीडियो तैयार है 👇</div>
            <video controls autoplay><source src="/stream_video" type="video/mp4"></video>
            <br><br>
            <a href="/download_file" style="color: #00f0ff; text-decoration: underline; font-weight: bold;">📥 फ़ोन गैलरी में डाउनलोड करें</a>
        </div>
        {% endif %}

        <form action="/cut" method="POST" onsubmit="startTimer()">
            <input type="text" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            
            <div class="section-title">शुरुआत का समय (Start Time)</div>
            <div style="display:flex; gap:10px;">
                <input type="number" name="start_min" placeholder="Min" value="0">
                <input type="number" name="start_sec" placeholder="Sec" value="0">
            </div>
            
            <div class="section-title">समाप्ति का समय (End Time)</div>
            <div style="display:flex; gap:10px;">
                <input type="number" name="end_min" placeholder="Min" value="0">
                <input type="number" name="end_sec" placeholder="Sec" value="15">
            </div>
            
            <div class="section-title">वीडियो क्वालिटी</div>
            <select name="quality">
                <option value="best">⚡ Superfast Cloud Quality (Fastest)</option>
                <option value="1080">1080p Full HD (Takes Time)</option>
                <option value="720">720p HD</option>
                <option value="480">480p Medium</option>
            </select>
            
            <div class="section-title">वीडियो का साइज</div>
            <select name="ratio">
                <option value="none">Original Size</option>
                <option value="16:9">Widescreen 16:9</option>
                <option value="9:16">Shorts 9:16</option>
            </select>
            
            <div id="timer" class="timer-display">
                <div class="spinner"></div>वीडियो प्रोसेस हो रहा है, कृपया प्रतीक्षा करें...
            </div>
            <button type="submit" id="submit-btn">💥 प्रोसेस और डाउनलोड</button>
        </form>
    </div>
    <a href="mailto:khanshazad3927@gmail.com" class="help-btn">🚨 Help</a>

    <script>
        function startTimer() {
            document.getElementById('submit-btn').style.display = "none";
            document.getElementById('timer').style.display = "block";
        }
        
        // जादू: अगर पेज पर एरर मैसेज मौजूद है, तो स्पिनर को छुपाओ और बटन को वापस दिखाओ!
        window.onload = function() {
            if (document.querySelector('.error-msg')) {
                document.getElementById('submit-btn').style.display = "block";
                document.getElementById('timer').style.display = "none";
            }
        }
    </script>
</body>
</html>
"""

def safe_int(val, default=0):
    if not val or str(val).strip() == "": return default
    try: return int(val)
    except: return default

@app.route('/')
def home(): return render_template_string(HTML, video_ready=False, error_text=None)

@app.route('/cut', methods=['POST'])
def cut():
    url = request.form.get('url', '').strip()
    
    if not url or ("youtube.com" not in url and "youtu.be" not in url):
        return render_template_string(HTML, video_ready=False, error_text="गलत यूआरएल! कृपया सही यूट्यूब लिंक डालें।")
    
    start_min = safe_int(request.form.get('start_min'), 0)
    start_sec = safe_int(request.form.get('start_sec'), 0)
    end_min = safe_int(request.form.get('end_min'), 0)
    end_sec = safe_int(request.form.get('end_sec'), 15)
    
    start_time = (start_min * 60) + start_sec
    end_time = (end_min * 60) + end_sec
    
    quality = request.form.get('quality')
    ratio = request.form.get('ratio')
    
    output_dir = "/sdcard/YT_Cuts"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output = os.path.join(output_dir, "final_output.mp4")
    if os.path.exists(output):
        try: os.remove(output)
        except: pass
    
    if quality == 'best':
        format_set = 'best'
    else:
        format_set = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    ydl_opts = {
        'format': format_set,
        'outtmpl': output,
        'download_ranges': lambda info, ydl: [{'start_time': start_time, 'end_time': end_time}],
        'force_keyframes_at_cuts': True,
        'merge_output_format': 'mp4',
        'quiet': True
    }
    
    if ratio != 'none':
        ydl_opts['postprocessor_args'] = ['-vf', f'crop={"in_h*16/9:in_h" if ratio=="16:9" else "in_w:in_w*16/9"}']
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([url])
        return render_template_string(HTML, video_ready=True, error_text=None)
    except Exception as e: 
        return render_template_string(HTML, video_ready=False, error_text="डाउनलोड फेल! लिंक काम नहीं कर रहा है, दोबारा सही यूआरएल डालें।")

@app.route('/stream_video')
def stream_video(): return send_file("/sdcard/YT_Cuts/final_output.mp4")

@app.route('/download_file')
def download_file(): return send_file("/sdcard/YT_Cuts/final_output.mp4", as_attachment=True)

if __name__ == '__main__': app.run(host='0.0.0.0', port=8080)
