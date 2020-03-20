from flask import Flask, render_template, url_for
import digest_utils
from loguru import logger

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
)
logger.debug(f'Flask config:\n{app.config}')

@app.route('/', methods=['GET'])
def kindle_digest(name=None):
    kindle_notes = digest_utils.get_kindle_clips(use_cache=True)
    # digest_utils.cache_kindle_clips(kindle_notes)
    digest_utils.clips_to_html(path='templates/index.html', clips=kindle_notes)

    url_for('static', filename='style.css')
    return render_template('index.html', name=name)
