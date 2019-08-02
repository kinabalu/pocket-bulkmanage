import requests
import click
import os 
import os.path
import sys

from settings import *

@click.group()
def main():
    """
    Simple CLI for managing your pocket queue
    """
    pass

def _authorize():
    if not CONSUMER_KEY:
        click.echo("CONSUMER_KEY must be defined in a local_settings.py file")
        sys.exit(1)

    r = requests.post('%s/v3/oauth/request' % (API_URL),
        data = {
            'consumer_key': CONSUMER_KEY,
            'redirect_uri': 'https://mysticcoders.com'
        },
        headers = {
            'Host': 'getpocket.com',
            # 'Content-Type': 'application/json; charset=UTF-8',
            'X-Accept': 'application/json'
        }
    )
    
    request_resp = r.json()
    code = request_resp['code']

    print("Visit the following URL: %s/auth/authorize?request_token=%s&redirect_uri=https://mysticcoders.com" % (API_URL, code,))

    input("Press Enter when you've completed the above step...")

    r = requests.post('%s/v3/oauth/authorize' % (API_URL),
        data = {
            'consumer_key': CONSUMER_KEY,
            'code': code,
        },
        headers = {
            'Host': 'getpocket.com',
            # 'Content-Type': 'application/json; charset=UTF-8',
            'X-Accept': 'application/json'
        }
    )
    auth_resp = r.json()

    return auth_resp['access_token']


@main.command()
@click.option('-f', help='File to load from for processing')
def get(f):
    if f and os.path.isfile(f):
        click.echo("Cool")
        return
    else:
        if not ACCESS_TOKEN:
            access_token = _authorize()

        r = requests.get('%s/v3/get' % (API_URL,),
            params = {
                'consumer_key': CONSUMER_KEY,
                'access_token': access_token,
                'contentType': 'article',
            },
            headers = {
                'Host': 'getpocket.com',
                # 'Content-Type': 'application/json; charset=UTF-8',
                'X-Accept': 'application/json'
            }
        )

        print(r.text)

if __name__ == '__main__':
    main()
