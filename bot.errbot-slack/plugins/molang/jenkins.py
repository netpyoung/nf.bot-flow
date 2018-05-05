import requests
import json
import logging
import urllib

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


username = 'bot'
password = 'bot'
JENKINS_ADDR = '127.0.0.1:8080'
TOKEN = 'helloworld'


def build_and(country, stage):
    JOB_NAME = "BUILD_AND_DEV"
    job_parameters = {
        'token': TOKEN,
        'COUNTRY': country,
        "STAGE": stage,
    }
    data = urllib.parse.urlencode(job_parameters)
    request_url = f'http://{username}:{password}@{JENKINS_ADDR}/job/{JOB_NAME}/buildWithParameters?{data}'
    print(request_url)
    r = requests.get(request_url)
    print(r.raise_for_status())
    return r


def update_db(country, stage):
    JOB_NAME = "DB_DEV"
    job_parameters = {
        'token': TOKEN,
        'COUNTRY': country,
        "STAGE": stage,
    }
    data = urllib.parse.urlencode(job_parameters)
    request_url = f'http://{username}:{password}@{JENKINS_ADDR}/job/{JOB_NAME}/buildWithParameters?{data}'
    print(request_url)
    r = requests.get(request_url)
    print(r.raise_for_status())
    return r

def update_locale(country, stage):
    JOB_NAME = "LOCALE_DEV"
    job_parameters = {
        'token': TOKEN,
        'COUNTRY': country,
        "STAGE": stage,
    }
    data = urllib.parse.urlencode(job_parameters)
    request_url = f'http://{username}:{password}@{JENKINS_ADDR}/job/{JOB_NAME}/buildWithParameters?{data}'
    print(request_url)
    r = requests.get(request_url)
    print(r.raise_for_status())
    return r