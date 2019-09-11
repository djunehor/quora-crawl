# quora-crawl
A python module to search and crawl quora for specific keyword/phrase

== Installation ==
1. Run `git clone https://github.com/makinde2013/quora-crawl.git`
2. Run `pip install -r requirements.txt` to install packages
3. Download latest chrome driver here https://chromedriver.chromium.org/
4. Unzip and place the desired path
5. Open utils/browser.py and edit the GOOGLE_CHROME_PATH if you're on linux, and CHROMEDRIVER_PATH if you're on windows
6. Run the script `py __init__.py [keyword]` e.g py __init__.py naira
7. You can also use the module in your script by doing `from quora import main as quora_crawl`. Then you can use like `quora_crawl(keyword)` e.g fetched_date = quora_crawl('Naira')
