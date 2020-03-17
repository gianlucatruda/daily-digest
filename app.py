from flask import Flask, render_template, url_for
from digest_utils import clips_to_html

app = Flask(__name__)

@app.route('/', methods=['GET'])
def kindle_digest(name=None):
    url_for('static', filename='style.css')
    return render_template('index.html', name=name)
