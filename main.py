from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

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
        .card { background: rgba(10, 20, 30, 0.95); border-radius: 24px; border: 2px solid #00f0ff; width: 100%; max-width: 430px; padding: 30px; box-shadow: 0 0 35px #00f0ff; }
        h1 { color: #fff; text-align: center; font-size: 26px; text-shadow: 0 0 10px #00f0ff; margin-bottom: 25px; }
        input, select { width: 100%; padding: 13px; margin-bottom: 10px; background: #050b11; border: 1px solid #00f0ff; color: #fff; border-radius: 10px; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #ff003c 0%, #990024 100%); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 16px; cursor: pointer; }
        .timer-display { display: none; text-align: center; color: #ff003c; margin-top: 15px; }
        .player-container { display: none; margin-top: 20px; text-align: center; }
        video { width: 100%; border-radius: 10px; }
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
            <a href="/download_file" style="color: #00f0ff; font-weight: bold;">📥 डाउनलोड करें</a>
        </div>
        <form id="cut-form">
            <input type="text" id="url" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            <input type="number" name="start_min" placeholder="Start Min" value="0">
            <input type="number" name="start_sec" placeholder="Start Sec" value="0">
            <input type="number" name="end_min" placeholder="End Min" value="0">
            <input type="number" name="end_sec" placeholder="End Sec" value="15">
            <button type="submit" id="submit-btn">💥 प्रोसेस और डाउनलोड</button>
            <div id="timer" class="timer-display">वीडियो प्रोसेस हो रहा है...</div>
        </form>
    </div>
    <script>
        document.getElementById('cut-form').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('submit-btn').style.display = "none";
            document.getElementById('timer').style.display = "block";
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
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/cut', methods=['POST'])
def cut():
    url = request.form.get('url', '').strip()
    try:
        output = "final_output.mp4"
        if os.path.exists(output): os.remove(output)
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': output,
            'download_ranges': lambda info, ydl: [{'start_time': (int(request.form['start_min'])*60)+int(request.form['start_sec']), 
                                                   'end_time': (int(request.form['end_min'])*60)+int(request.form['end_sec'])}],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        return jsonify({'status': 'success'})
    except: return jsonify({'status': 'error', 'message': 'लिंक गलत है!'})

@app.route('/stream_video')
def stream_video(): return send_file("final_output.mp4")

@app.route('/download_file')
def download_file(): return send_file("final_output.mp4", as_attachment=True)

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
