import requests
# helper to APIs.py


def _url(path):
    return 'http://deta224.cs.uky.edu' + path


def get_apis():
    return requests.get(_url('/api/'))


def describe_api(api_id):
    return requests.get(_url('/api/{:d}/'.format(api_id)))


def api_done(api_id):
    return requests.delete(_url('/api/{:d}/'.format(api_id)))
