import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def deteksi_otomatis(img_path):
    img = cv2.imread(img_path)
    if img is None: return "Gambar Gagal Dibaca"
    
    # Kecilkan gambar biar robot fokus ke warna utamanya aja
    img_small = cv2.resize(img, (50, 50))
    avg_color = np.average(np.average(img_small, axis=0), axis=0)
    b, g, r = avg_color[0], avg_color[1], avg_color[2]

    # --- LOGIKA ANTI KEBALIK (Sudah Diperbaiki) ---
    
    # 1. Kalau dominan Putih,Pink = Kertas
    if b > r and b > g:
        return "Sampah Kertas"
    
    # 2. Kalau dominan Hijau,Oranye,hitam = Botol Kaca (seperti botol minuman dingin)
    elif g > r and g > b:
        return "Sampah Botol Kaca"
    
    # 3. Kalau dominan Kuning,Merah,Biru = Plastik
    elif r > b and r > g:
        return "Sampah Plastik"
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        hasil = deteksi_otomatis(filepath)
        return render_template('result.html', result=hasil)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
