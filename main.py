#!/bin/python

import json
import requests
import random
import asyncio

REPORT_FILE = "report.json"

class   ProxyRequest():
  report = []
  
  def __init__(self, report_file, use_top=10, use_detected=True):
    with open(report_file) as f:
      try:
        self.report = json.loads(f.read())
        self.report.sort(key=lambda x: x['time'])
        self.use_top = use_top
        self.use_detected = use_detected
      except ValueError as e:
        exit(e)

  def select_proxy(self):
    choice = random.choice(self.report[0:self.use_top])
    while choice['detected'] != self.use_detected:
      choice = random.choice(self.report[0:self.use_top])
    return choice
  
  def request(self, method, url, **kwargs):
    proxy = self.select_proxy()['proxy']
    print('using proxy %s' %proxy)
    http_proxy  = "http://%s" %proxy
    https_proxy = "https://%s" %proxy
    ftp_proxy   = "ftp://%s" %proxy
    proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
    }
    return requests.request(method=method, url=url, proxies=proxyDict, **kwargs)

  def get(self, url, **kwargs):
    return self.request("GET", url, **kwargs)

  def post(self, url, **kwargs):
    return self.request("POST", url, **kwargs)
  
def	main():
  url = "https://monip.org"
  request = ProxyRequest(REPORT_FILE, use_detected=False)
  r = request.get(url)
  print(r.text)
  return 0

if __name__ == '__main__':
  exit(main())
