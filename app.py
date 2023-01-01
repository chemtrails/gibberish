from flask import render_template, send_from_directory, Flask
from mod import font_mod

app = Flask(__name__)

app.config['FONT_FILE'] = ''

@app.route('/font')
def serve_font():
    return send_from_directory('output', f'{app.config["FONT_FILE"]}.ttf')

@app.route('/')
def index():
    with open('sample_text.txt', 'r') as f:
        content = f.read()
        new_text, random_string = font_mod(content)
        app.config['FONT_FILE'] = random_string
    
    return render_template(
        'index.html', 
        original_text = content,
        new_text = new_text,
        random_string = random_string
    )

app.run(debug=True)