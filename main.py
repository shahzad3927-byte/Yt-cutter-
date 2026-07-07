from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# पूरा HTML डिज़ाइन वापस ला दिया है
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
        .card { background: rgba(10, 20, 30, 0.95); border-radius: 24px; border: 2px solid #00f0ff; width: 100%; max-width: 430px; padding: 30px; box-shadow: 0 0 35px #00f0ff, inset 0 0 15px rgba(0, 240, 255, 0.2); }
        .insta-branding { display: flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); padding: 12px; border-radius: 50px; margin-bottom: 20px; text-decoration: none; color: #fff; font-weight: bold; }
        h1 { color: #fff; text-align: center; margin-bottom: 25px; font-size: 26px; text-shadow: 0 0 10px #00f0ff; font-weight: 900; }
        .section-title { font-size: 12px; color: #00f0ff; margin-top: 15px; margin-bottom: 6px; text-transform: uppercase; }
        input, select { width: 100%; padding: 13px; margin-bottom: 5px; background: #050b11; border: 1px solid #00f0ff; color: #fff; border-radius: 10px; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #ff003c, #990024); border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; margin-top: 15px; }
        .player-container { margin-top: 5px; text-align: center; border: 2px dashed #ff003c; padding: 15px; border-radius: 14px; background: #050002; }
        .error-msg { background: rgba(255, 0, 60, 0.15); border: 2px dashed #ff003c; color: #ff3366; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <a href="https://instagram.com/mr_afsar0000" target="_blank" class="insta-branding"><i class="fab fa-instagram"></i> Follow Me: @mr_afsar0000</a>
        <h1>YT Cutter Ultra Pro</h1>
        {% if error_text %}<div class="error-msg">❌ {{ error_text }}</div>{% endif %}
        {% if video_ready %}
        <div class="player-container">
            <div style="color: #ff003c; font-weight: bold;">📺 आपका वीडियो तैयार है!</div>
            <br><a href="/download_file" style="color: #00f0ff; font-weight: bold;">📥 डाउनलोड करें</a>
        </div>
        {% endif %}
        <form action="/cut" method="POST">
            <input type="text" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            <div class="section-title">शुरुआत का समय (Start Time)</div>
            <div style="display:flex; gap:10px;"><input type="number" name="start_min" value="0"><input type="number" name="start_sec" value="0"></div>
            <div class="section-title">समाप्ति का समय (End Time)</div>
            <div style="display:flex; gap:10px;"><input type="number" name="end_min" value="0"><input type="number" name="end_sec" value="15"></div>
            <div class="section-title">वीडियो क्वालिटी</div>
            <select name="quality">
                <option value="best">⚡ Superfast Cloud Quality</option>
                <option value="1080">1080p Full HD</option>
                <option value="720">720p HD</option>
            </select>
            <button type="submit">💥 प्रोसेस और डाउनलोड</button>
        </form>
    </div>
</body>
</html>
"""

def safe_int(val, default=0):
    try: return int(val)
    except: return default

@app.route('/')
def home(): return render_template_string(HTML, video_ready=False, error_text=None)

@app.route('/cut', methods=['POST'])
def cut():
    url = request.form.get('url', '').strip()
    start_time = (safe_int(request.form.get('start_min')) * 60) + safe_int(request.form.get('start_sec'))
    end_time = (safe_int(request.form.get('end_min')) * 60) + safe_int(request.form.get('end_sec'))
    
    # क्लाउड पर काम करने के लिए फोल्डर
    output_dir = "downloads"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output = os.path.join(output_dir, "final_output.mp4")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output,
        'download_ranges': lambda info, ydl: [{'start_time': start_time, 'end_time': end_time}],
        'force_keyframes_at_cuts': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        return render_template_string(HTML, video_ready=True)
    except Exception as e:
        return render_template_string(HTML, error_text="डाउनलोड फेल! कृपया लिंक चेक करें।")

@app.route('/download_file')
def download_file(): return send_file("downloads/final_output.mp4", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
    
