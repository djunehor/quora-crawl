from utils import browser, scraper
from dotenv import load_dotenv
import os
import sys


def main():
    # secret info
    load_dotenv()
    user_email = os.getenv('QR_USERNAME')
    user_password = os.getenv('QR_PASSWORD')
    linux = os.getenv("LINUX")


    # Search Settings
    try:
        keyword = str(sys.argv[1])
    except:
        print('No keyword passed!')
        keyword = str(input('Enter Keyword: '))

        if not keyword:
            print('No keyword supplied')
            exit()

    # Browser Actions
    b = browser.Browser(linux)
    b.get_home()
    b.login(user_email, user_password)
    b.search_by(keyword)
    b.infinite_scroll()
    our_urls = b.get_urls()

    # Scraper Actions
    all_data = []
    for url in our_urls:
        print('Current URL: ', url)
        b.get_url(url+'/log')
        b.infinite_scroll()
        u = scraper.Scraper(html=b.get_source())
        # data['text'] = u.get_details()
        data = u.get_details()
        if 'url' in data['user']:
            b.get_url(data['user']['url'])
            v = scraper.Scraper(html=b.get_source())
            data['user']['followers'] = v.get_followers()

        all_data.append(data)

        b.get_url(url)
        b.infinite_scroll()
        # t = scraper.Scraper(html=b.get_source())
        dat = b.get_comments()
        for d in dat:
            all_data.append(d)

    return all_data


if __name__ == '__main__':
    response = main()
    print(response)