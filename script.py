#!/usr/bin/env/python

'''
Description: Gather the response time of a website.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from xvfbwrapper import Xvfb
import os
import unittest


def usage():
    msg = """
        About:
        A script that routes headless geckodriver requests through local proxy port 8888.
        Pre-requisite that Charles proxy configured to listen on 8888 inside com.xk72.charles.config.
        
        
        Usage:
            python/python3 script.py <charles format>
            
        Options:
            <charles format>    [ chls | csv | xml | json | trace | har ]

      """
    print(msg)

class Record(unittest.TestCase):
    PROXY = "127.0.0.1:8888"
    proxy_capability = webdriver.DesiredCapabilities.FIREFOX.copy()
    print(str(proxy_capability['marionette']))
    proxy_capability['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL"
    }
    
    browser = None
    
    # charles_port = "http://127.0.0.1:8888" -- sometimes 127.0.0.1 traffic is ignored so use localhost below
    charles_port = "http://localhost.charlesproxy.com:8888"
    charles_start = "http://control.charles/recording/start"
    charles_stop = "http://control.charles/recording/stop"
    charles_clear = "http://control.charles/session/clear"
    save_folder = "/home/ubuntu/"
    charles_download_chls = "http://control.charles/session/download"
    charles_download_csv = "http://control.charles/session/export-csv"
    charles_download_xml = "http://control.charles/session/export-xml"
    charles_download_json = "http://control.charles/session/export-json"
    charles_download_trace = "http://control.charles/session/export-trace"
    charles_download_har = "http://control.charles/session/export-har"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __del__(self):
        if self.browser is not None:
            self.browser.quit()
            
    def setUp(self):
        print("\n======= Start Recording ===========")
        os.system("curl -x " + self.charles_port + " " + self.charles_start + " > /dev/null")
        
    def tearDown(self):
        testName = "{}".format(self)
        save_file = testName.split(' ')[0] + ".chls"
        save_file_converted = save_file.replace(".chls", self.session_format)
        file_path = self.save_folder + save_file_converted
        try:
            print("\n======= Save Recording ===========")
            os.system("curl -o " + file_path + " -x " + self.charles_port + " http://control.charles/session/export-" + self.session_format)
            if self.browser is not None:
                print("\nClosing browser")
                self.browser.quit()
        except Exception as e:
            print(e)
            
    def test_allsides():
        print("\n Testing ..")
        try:
            with Xvfb() as xvfb:
                driver = webdriver.Firefox(capabilities=proxy_capability)
                driver.implicitly_wait(30)
                driver.delete_all_cookies()
                self.browser = driver
        except Exception as e:
            print("Error: loading firefox in virtual display")
            print(e)
        try:
            assert(self.browser is not None)
            driver.get("https://www.allsides.com/unbiased-balanced-news")
            print(driver.current_url)
        except Exception as e:
            print("Error during test")
            print(e)
    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        Record.session_format = sys.argv.pop()
        assert(Record.session_format in ["chls", "csv", "xml", "json", "trace", "har"])
        unittest.main()
    else:
        print("Incorrect CLI args")
        usage()
