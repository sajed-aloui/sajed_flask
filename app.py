import random
import requests
import time
from flask import Flask, render_template

app = Flask(__name__)

def get_random_meme():
  url = "https://www.reddit.com/r/memes/random.json"
  headers = {'User-Agent': 'Random Meme Generator'}
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    data = response.json()
    meme_url = data[0]['data']['children'][0].get('url')
    if meme_url and meme_url.endswith(('.jpg', '.png', '.gif')):  # Optional filtering for image formats
      return meme_url
    else:
      print("Retrieved meme doesn't have a valid image URL")
      return None
  except requests.exceptions.RequestException as e:
    print(f"Error making request to Reddit: {e}")
    return None
  except KeyError as e:
    print(f"Error parsing JSON data: Missing key '{e}'")
    return None
  except Exception as e:
    print(f"Unexpected error: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_meme')
def random_meme():
    meme_url = get_random_meme()
    return render_template('random_meme.html', meme_url=meme_url)

if __name__ == '__main__':
    app.run(debug=True)
