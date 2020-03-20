import requests
import random
import json
import os
from secrets import TOKEN
from loguru import logger


def generate_options(clips) -> list:
    books = list(clips.keys())
    options = []
    for book in books:
        for pos in clips[book].keys():
            val = clips[book][pos]
            options.append(
                f"<h2>{book}</h2>\n<b>{val['date']}</b>\n\n<p>{val['content']}</p>\n\n")
    return options


def random_clips(clips, num=5):
    logger.debug(f'Generating {num} random clips...')
    options = generate_options(clips)
    choices = []
    for _ in range(num):
        choice = random.choice(options)
        choices.append(choice)
        options.remove(choice)
    return choices


def clips_to_html(path='index.html', *args, **kwargs):
    clips = random_clips(*args, **kwargs)
    out = '<link rel="stylesheet" type="text/css" href="static/style.css" media="screen"/>'
    out += '\n'.join(clips)
    with open(path, 'w') as f:
        f.write(out)


def get_kindle_clips(token=TOKEN, use_cache=False, cache_path='cache/clips.json'):
    if use_cache:
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as file:
                clips = json.load(file)
            logger.info(f'Using cached clips at {cache_path}')
            return clips
        else:
            logger.warning(f'Tried retrieving cache, but {cache_path} could not be found.')
    url = f'https://raw.githubusercontent.com/gianlucatruda/kindle-reading-notes/master/clips.json?token={TOKEN}'
    logger.info(f'Retrieving clips from {url}')
    req = requests.get(url)
    logger.debug(f'Request: {req}')
    if use_cache:
        cache_kindle_clips(req.json(), path=cache_path)
    return req.json()


def cache_kindle_clips(clips, path='cache/clips.json'):
    logger.debug(f'Writing clips to cache at {path}...')
    with open(path, 'w') as file:
        json.dump(clips, file)


if __name__ == "__main__":

    # Get latest data
    kindle_notes = get_kindle_clips()
    cache_kindle_clips(kindle_notes)
    # Wikipedia random article? Tweets from my history?

    # Produce page
    clips_to_html(path='templates/index.html', clips=kindle_notes)

    # Restart server?

    # Send link via mail or notification
