from be.model.mongo_classes import (
    BookInfoMongo
)
from be.model.mongo_conn import connect_mongo

from bs4 import BeautifulSoup
import requests, random, time, re
import sqlite3
import logging, traceback, os, sys
import mongoengine
import mongoengine.errors

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
    "Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
    "Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR "
    "3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
    "Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET "
    "CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) "
    "Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) "
    "AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) "
    "Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 "
    "Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) "
    "wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) "
    "AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 "
    "Mobile/10A5376e Safari/8536.25",
]

def get_user_agent():
    headers = {"User-Agent": random.choice(user_agent)}
    return headers

class DoubanTagScraper:
    def __init__(self, mongodb=False):
        self.database = 'scraper.db'
        self.mongodb = mongodb
        logging.basicConfig(filename="scraper.log", level=logging.ERROR)
        print('Scraper in progress. Check scraper.log for details.')
    def save_current_progress(self, current_tag, current_page):
        conn = sqlite3.connect(self.database)
        conn.execute(
            "UPDATE progress set tag = '{}', page = {} where id = '0'".format(
                current_tag, current_page
            )
        )
        conn.commit()
        conn.close()
    def get_current_progress(self) -> tuple:
        conn = sqlite3.connect(self.database)
        results = conn.execute("SELECT tag, page from progress where id = '0'")
        for row in results:
            return row[0], row[1]
        return "", 0
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        try:
            conn.execute("CREATE TABLE tags (tag TEXT PRIMARY KEY)")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(str(e))
            conn.rollback()

        try:
            conn.execute(
                "CREATE TABLE book ("
                "id TEXT PRIMARY KEY, title TEXT, author TEXT, "
                "publisher TEXT, original_title TEXT, "
                "translator TEXT, pub_year TEXT, pages INTEGER, "
                "price INTEGER, currency_unit TEXT, binding TEXT, "
                "isbn TEXT, author_intro TEXT, book_intro text, "
                "picture BLOB)"
            )
            conn.commit()
        except sqlite3.Error as e:
            logging.error(str(e))
            conn.rollback()

        try:
            conn.execute(
                "CREATE TABLE progress (id TEXT PRIMARY KEY, tag TEXT, page integer )"
            )
            conn.execute("INSERT INTO progress values('0', '', 0)")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(str(e))
            conn.rollback()
    def get_tag_list(self):
        ret = []
        conn = sqlite3.connect(self.database)
        results = conn.execute(
            "SELECT tags.tag from tags join progress where tags.tag >= progress.tag"
        )
        for row in results:
            ret.append(row[0])
        return ret
    
    def grab_tag(self):
        url = "https://book.douban.com/tag/?view=cloud"
        r = requests.get(url, headers=get_user_agent())
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = [tag['href'].strip("/tag") for tag in soup.select('td a[href^="/tag"]')]
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        try:
            for tag in tags:
                c.execute("INSERT INTO tags VALUES (?)", (tag,))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(str(e))
            conn.rollback()
            return False
        finally:
            c.close()
            conn.close()
        return True
    
    def grab_book_list(self, tag="小说", pageno=1) -> bool:
        logging.info(f"start to grab tag {tag} page {pageno}...")
        self.save_current_progress(tag, pageno)
        url = f"https://book.douban.com/tag/{tag}?start={(pageno-1)*20}&type=T"
        r = requests.get(url, headers=get_user_agent())
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, 'html.parser')

        li_list = [a['href'] for a in soup.select('li div.info h2 a')]
        has_next = bool(soup.select('span.next a'))

        if not li_list:
            return False

        for li in li_list:
            book_id = li.strip("/").split("/")[-1]
            try:
                delay = float(random.randint(0, 200)) / 100.0
                time.sleep(delay)
                self.crow_book_info(book_id)
            except Exception as e:
                logging.error(f"error when scrape {book_id}, {str(e)}")
                _, file = os.path.split(os.path.abspath(__file__))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                for frame in traceback.extract_tb(exc_traceback):
                    if file in frame.filename:
                        logging.error(f"Error in file: {frame.filename}, line: {frame.lineno}")
        return has_next
    
    def crow_book_info(self, book_id) -> bool:
        logging.info(f'Start to grab book: {book_id}')
        if self.mongodb:
            book = BookInfoMongo.objects(book_id=book_id).first()
            if book:
                logging.warning(f"book {book_id} already exists")
                return
        else:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute("SELECT id from book where id = ?", (book_id,))
            if c.fetchone():
                c.close()
                logging.warning(f"book {book_id} already exists")
                return 

        url = f"https://book.douban.com/subject/{book_id}/"
        retries = 0
        while retries < 5:
            try:
                r = requests.get(url, headers=get_user_agent())
                r.encoding = "utf-8"
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.select_one('h1 span').text if soup.select_one('h1 span') else None
                assert title
                break
            except requests.RequestException as e:
                retries += 1
                logging.warning(f"error when request {url}, retry {retries}, {str(e)}")
                time.sleep(1)
            except Exception as e:
                retries += 1
                logging.warning(f"error when request {url}, retry {retries}, {str(e)}")
                time.sleep(1)
        else:
            logging.error(f"request {url} failed after 5 retries")
            return False
        
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.select_one('h1 span').text if soup.select_one('h1 span') else None
        if not title:
            logging.error(f"book {book_id} not found")
            return False

        # 抓取书籍简介、作者简介、目录和标签
        book_intro = '\n'.join([p.text.strip() for p in soup.select('#link-report .intro p')]) ## ok
        author_intro = '\n'.join([p.text.strip() for p in soup.select('.indent .intro p')]) ## ok
        # content = '\n'.join([p.text.strip() for p in soup.select('#dir_' + book_id + '_full p')])
        # tags = '\n'.join([a.text.strip() for a in soup.select('#db-tags-section .indent span a')])

        # 抓取书籍图片
        section = soup.select('#mainpic a')
        pictures = []
        for x in section:
            pic_href = x['href']
            pictures.append(requests.get(pic_href).content)

        # 抓取书籍信息
        info_text = soup.select_one('#info').get_text()
        book_info = self.parse_info(info_text)
        author = book_info.get("作者")
        publisher = book_info.get("出版社")
        original_title = book_info.get("原作名")
        translator = book_info.get("译者")
        pub_time = book_info.get("出版年")
        pages = book_info.get("页数")
        match = re.compile(r'\d+\.?\d*').search(pages) if pages else None
        if match:
            pages = int(match.group())
        else:
            pages = random.randint(20, 500)
            logging.warning(f"page number not found, randomly set to {pages}")
        try:
            price, currency_unit = self.parse_price(book_info.get("定价"))
        except TypeError:
            price = random.randint(10, 100)
            currency_unit = '元'
            logging.warning(f"price not found, randomly set to {price}")
        binding = book_info.get("装帧")
        isbn = book_info.get("ISBN")

        # 构建 SQL 插入语句
        sql = """
        INSERT INTO book(
            id, title, author, 
            publisher, original_title, translator, 
            pub_time, pages, price, 
            currency_unit, binding, isbn, 
            author_intro, book_intro, pictures)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """

        try:
            if self.mongodb:
                translator = translator.split('/') if translator else ['未知']
                book = BookInfoMongo(
                    book_id=book_id, title=title, author=author,
                    publisher=publisher, original_title=original_title, translator=translator,
                    pub_time=pub_time, pages=pages, price=price,
                    currency_unit=currency_unit, binding=binding, isbn=isbn,
                    author_intro=author_intro, book_intro=book_intro, pictures=pictures
                )
                book.save(force_insert=True)
            else:
                c.execute(sql, (
                    book_id, title, author,
                    publisher, original_title, translator,
                    pub_time, pages, price,
                    currency_unit, binding, isbn,
                    author_intro, book_intro, pictures
                ))
                conn.commit()
            logging.info( f'Write to {"mongodb" if self.mongodb else self.database} Success!\n',
                # book_id, title, author,
                # publisher, original_title, translator,
                # pub_time, pages, price,
                # currency_unit, binding, isbn,
                # author_intro[:10] if author_intro is not None else 'None', 
                # book_intro[:10] if book_intro is not None else 'None', 'Has picture:',
                # picture != None
            )
        except sqlite3.Error as e:
            logging.error(str(e))
            logging.error('Failed to write to SQLite')
            conn.rollback()
            return False
        except mongoengine.errors.MongoEngineException as e:
            logging.error(str(e))
            logging.error('Failed to write to MongoDB')
            return False
        finally:
            if self.mongodb:
                pass
            else:
                c.close()
                conn.close()
        return True

    def parse_info(self, info_text):
        info_lines = info_text.strip().split('\n')
        info_lines = [line.strip() for line in info_lines if line.strip() != '']
        book_info = {}
        old_info_lines = list(info_lines)
        info_lines = []
        for x in old_info_lines:
            if ':' not in x:
                info_lines[-1] += x
            else:
                info_lines.append(x)
        for line in info_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                book_info[key] = value
        return book_info

    def parse_price(self, price_str):
        # 解析价格
        if price_str:
            match = re.compile(r'\d+\.?\d*').search(price_str)
            if match:
                return float(match.group()), re.sub(r'\d+\.?\d*', '', price_str)
        return None
    
    def start_grab(self) -> bool:
        self.create_tables()
        scraper.grab_tag()
        current_tag, current_page = self.get_current_progress()
        tags = self.get_tag_list()
        if self.mongodb and not connect_mongo():
            print('Failed to connect to MongoDB')
            return False
        for i in range(0, len(tags)):
            no = 0
            if i == 0 and current_tag == tags[i]:
                no = current_page
            while self.grab_book_list(tags[i], no):
                no = no + 20
        return True

scraper = DoubanTagScraper(True)
scraper.start_grab()
