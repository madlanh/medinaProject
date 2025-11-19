from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sejarah')
def sejarah():
    return render_template('sejarah.html')

@app.route('/visi-misi')
def visi_misi():
    return render_template('visi-misi.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)