from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# बिल्कुल तुम्हारी पसंद का पुराना सिंपल डिज़ाइन (Instagram: @mr_afsar0000 के साथ)
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT CUTTER</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px 20px; 
            background-color: #f4f4f9;
            color: #333;
        }
        .container { 
            max-width: 400px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        }
        h1 { color: #ff0000; margin-bottom: 20px; font-size: 28px; font-weight: bold; }
        input, select { 
            width: 100%; 
            padding: 12px; 
            margin: 10px 0; 
            border: 1px solid #ccc; 
            border-radius: 5px; 
            box-sizing: border-box;
            font-size: 14px;
        }
        button { 
            background-color: #ff0000; 
            color: white; 
            border: none; 
            padding: 14px; 
            width: 100%; 
            border-radius: 5px; 
            font-size: 16px; 
            font-weight: bold;
            cursor: pointer; 
            margin-top: 10px;
        }
        button:hover { background-color: #cc0000; }
        .instagram { 
            margin-top: 25px; 
            font-size: 14px; 
            color: #555; 
            font-weight: bold;
        }
        .status { display: none; margin-top: 15px; font-weight: bold; color: #ff0000; }
        .download-box { display: none; margin-top: 20px; }
        video { width: 100%; border-radius: 5px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>YT CUTTER</h1>
        
        <div id="download-section" class="download-box">
            <video id="player" controls></video>
            <br>
            <a id="dl-link" href="/download_file" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; margin-top: 10px;">📥 वीडियो डाउनलोड करें</a>
        </div>

        <form id="cutter-form">
            <input type="text" name="url" placeholder="यूट्यूब लिंक पेस्ट करें..." required>
            <input type="text" name="start_time" placeholder="Start Time (जैसे 0:00)" required>
            <input type="text" name="end_time" placeholder="End Time (जैसे 0:15)" required>
            
            <select name="quality">
                <option value="best">Video Quality: HD (Best)</option>
                <option value="1080p">1080p Full HD</option>
                <option value="720p">720p HD</option>
                <option value="480p">480p Medium</option>
            </select>

            <button type="submit" id="btn">💥 प्रोसेस और डाउनलोड</button>
            <div id="loading" class="status">⏳ वीडियो प्रोसेस हो रहा है, कृपया रुकें...</div>
            <div id="error" class="status" style="color: red;"></div>
        </form>
        
        <div class="instagram">Instagram: @mr_afsar0000</div>
    </div>

    <script>
        document.getElementById('cutter-form').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('btn').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('download-section').style.display = 'none';

            fetch('/cut', { method: 'POST', body: new FormData(this) })
            .then(res => res.json())
            .then(data => {
                document.getElementById('btn').style.style.display = 'block';
                document.getElementById('loading').style.display = 'none';
                if(data.status === 'success') {
                    document.getElementById('player').src = "/stream_video?t=" + new Date().getTime();
                    document.getElementById('download-section').style.display = 'block';
                } else {
                    document.getElementById('error').innerText = "❌ " + data.message;
                    document.getElementById('error').style.display = 'block';
                }
            }).catch(() => {
                document.getElementById('btn').style.display = 'block';
                document.getElementById('loading').style.display = 'none';
                document.getElementById('error').innerText = "❌ सर्वर एरर आया!";
                document.getElementById('error').style.display = 'block';
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
        return jsonify({'status': 'error', 'message': 'वीडियो डाउनलोड करने में दिक्कत आई!'})

@app.route('/stream_video')
def stream_video(): 
    return send_file("final_output.mp4")

@app.route('/download_file')
def download_file(): 
    return send_file("final_output.mp4", as_attachment=True)

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
    
