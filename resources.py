# coding: utf-8
import os
import time
import random
import requests
import pdfkit
from HTMLParser import HTMLParser


class MLStripper(HTMLParser, object):
    def __init__(self):
        super(MLStripper, self).__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_article_url_list(query):
    return_list = []
    url = 'http://m.biz.chosun.com/svc/searchData.html?query={}'.format(query)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7',
    }
    r = requests.get(url, headers=headers)
    tot_article_count = int(r.json().get('TOTCNT'))
    for pn in range(1, tot_article_count / 10 + 2):
        # sleep for a range 1 ~ 4 secs
        _sleep_time = float(random.randrange(10, 40)) / 10
        print '[{}/{} waiting: {}s] 읽는 중입니다..'.format(pn,
                                                      tot_article_count / 10 + 1,
                                                      _sleep_time)
        time.sleep(_sleep_time)

        r = requests.get(url + '&pn={}'.format(pn), headers=headers)
        contents = r.json().get('CONTENT')
        if contents:
            return_list.extend(contents)
        else:
            print '[WARNING] no contents in {}&pn={}'.format(url, pn)
    return return_list


def save_to_pdf(cont_id, directory, title=None):
    # basic settings
    url = 'http://m.biz.chosun.com/svc/article.html?contid={}'.format(cont_id)
    options = {
        'page-size': 'A4',
        'margin-top': '0.40in',
        'margin-bottom': '0.0in',
        'margin-right': '0.40in',
        'margin-left': '0.40in',
        'encoding': "UTF-8",
        'no-outline': None,
        'dpi': 1000,
        'load-media-error-handling': 'ignore',
        'load-error-handling': 'ignore'
    }
    # if you need Table of Contents, then uncomment under 4 lines.
    toc = None
    # toc = {
    #     'load-media-error-handling': 'ignore',
    #     'load-error-handling': 'ignore'
    # }
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    if title is not None:
        # title strip
        file_name = title
    else:
        file_name = cont_id

    # if same file already exists,
    if os.path.exists('{}/{}.pdf'.format(directory, file_name)):
        print '[WARNING] file {}.pdf already exists.'.format(file_name)
        return False
    else:
        print '[NOTE] file {}.pdf ready to make..'.format(file_name)
    # html url to pdf file
    pdfkit.from_url(url=url,
                    configuration=config,
                    output_path='./{}/{}.pdf'.format(directory, file_name),
                    options=options,
                    toc=toc)
    return True