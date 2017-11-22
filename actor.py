# coding: utf-8
import time
import resources

def get_article_url_list(query):
    return resources.get_article_url_list(query)

def save_to_pdf(cont_id, directory='./pdfs', title=None):
    return resources.save_to_pdf(cont_id, directory, title=title)

def main():
    l = get_article_url_list('미술+그림')
    for content in l:
        content_id = content.get('CONTID').encode('utf-8')
        title = resources.strip_tags(content.get('TITLE').encode('utf-8') + '_')
        print '[TITLE] {}'.format(title)
        try:
            r = save_to_pdf(cont_id=content_id, title=title)
            if r is True:
                time.sleep(2.4)
            else:
                continue
        except (IOError, UnicodeDecodeError) as e:
            print '[ERROR]', e
            continue

if __name__ == '__main__':
    main()
    print '<./actor.py> 종료'
