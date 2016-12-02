from flask import Flask, request
from flask_cache import Cache
import urllib
import subprocess

cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': '',
        'CACHE_REDIS_PASSWORD': ''
}
cache = Cache(config=cache_config)

class Colors(object):
    def __init__(self):
        self.cache = {}

    def compute(self, url):
        if url in self.cache:
            print "get from dict.."
            return self.cache[url]
        else:
            print "compute.."
            filename = url.split('/')[-1]
            urllib.urlretrieve(url, 'data/%s' % filename)

            k = subprocess.check_output("identify -format %k data/" + filename, shell=True)
            self.cache[url] = k
            return k


app = Flask(__name__)
cache.init_app(app)

worker = Colors()

def cache_key():
    url = request.args.get('src')
    return url


@app.route('/api/num_colors')
@cache.cached(timeout=60*60*24, key_prefix=cache_key)
def colors():
    url = request.args.get('src', None)
    if url is None:
        return ""
    print url
    return worker.compute(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
