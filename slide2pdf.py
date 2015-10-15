#!/usr/bin/env python
import sys
import os
import subprocess
import urllib2
import time
from selenium import webdriver


def main():
    run_dir = os.getcwd()
    root_dir = os.path.join(run_dir, '_build', 'slides')
    print(root_dir)

    import SimpleHTTPServer
    import SocketServer
    PORT = 8000
    server = SocketServer.TCPServer(("", PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    import multiprocessing
    def httpd_server(root_dir):
        p = multiprocessing.current_process()
        os.chdir(root_dir)
        server.serve_forever()

    httpd = multiprocessing.Process(target=httpd_server, args=[root_dir])
    # httpd.daemon = True
    httpd.start()

    # Warm up
    timeout = 10
    while timeout > 0:
        try:
            urllib2.urlopen('http://localhost:8000/')
            break
        except urllib2.URLError:
            pass
        time.sleep(1)
        timeout -= 1

    # Capture
    phantomjs_path = os.path.join(os.getcwd(), 'node_modules/phantomjs/bin/phantomjs')
    print(phantomjs_path)
    driver = webdriver.PhantomJS(phantomjs_path)
    driver.set_window_size(1280, 720)
    for slide_idx in (1, 2):
        url_ = 'http://localhost:8000/index.html#' + str(slide_idx)
        FILENAME = os.path.join(os.getcwd(), "screen_{}.png".format(slide_idx))
        print(url_)
        print(FILENAME)

        # Open Web Browser & Resize 720P
        driver.get(url_)
        time.sleep(1)
        driver.refresh()
        time.sleep(1)

        # Get Screen Shot
        driver.save_screenshot(FILENAME)
    driver.close()

    # server.shutdown()
    httpd.terminate()
    while httpd.is_alive():
        time.sleep(1)

    # Merge

    # end


if __name__ == '__main__':
    main()