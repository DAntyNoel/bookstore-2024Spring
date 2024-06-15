## Bookstore-2024Spring-SJTU-CS3952

Original source code from [shuishan online class, 2023_ECNU](https://www.shuishan.net.cn/mooc/course/1432511598644629505), and [DaSE-DBMS](https://github.com/DaSE-DBMS/bookstore.git).

So far, this reposit realize the functions only required by CDMS Project I, as the final project of SJTU-2023-2024-Spring-CS3952.

### Usage

- Clone this repo

- Create a venv or conda environment with python=3.7

- `pip install -r requirements.txt`

  Note: If specified version installation fails, please use `requirements0.txt` instead.

  Note: Strict requirements: Flask>=2.0, pymongo>=4.3

- Start up your local Mongo server, and copy the IP address into `be/model/config.yaml`

- (Use only) At root directory, run:

  ```
  PYTHONPATH=. python be/app.py
  ```

  You can find some interacting codes in `usertest` folder. Just run them on the other terminal. The usage of `usertest` can be found [below](#####Usage of usertest code).

- (Test only) At root directory, run:

  ```
  bash script/test.sh 
  ```

  Before you can successfully finished the test, please check the book database is correct (at `fe/data/` folders), **both** `book.db` and `book_lx.db` are required.

  In my test case, the `book.db` and `book_lx.db` are the same, you can change them with your own datasets, but must follows the form:
  
  ```
  TABLE book 
  (id TEXT PRIMARY KEY, title TEXT, author TEXT, publisher TEXT, original_title TEXT, translator TEXT, pub_year TEXT, pages INTEGER, price INTEGER, currency_unit TEXT, binding TEXT, isbn TEXT, author_intro TEXT, book_intro text, content TEXT, tags TEXT, picture BLOB)
  ```
  
  Note: You must double check if the backend has connected to Mongo server. Check the debugging info.
  
  <details>
      <summary>Examples</summary>
      <pre>
  Failed Example:
      <code>
  bookstore$ PYTHONPATH=. python be/app.py 
  Cannot connect to MongoDB. Please check your connection.
   * Serving Flask app 'be.serve'
  ...
  </code>
	Success Example:
  <code>
  bookstore$ PYTHONPATH=. python be/app.py 
  Connected to MongoDB!
   * Serving Flask app 'be.serve'
  ...
  </code></pre>
  </details>
  
- (Test only, Recommend) Before run the test bash code, it is highly recommended to start a backend in another terminal (introduced in `Use only` part). Afterwards running the test codes will automatically connect to the existing server and you can inspect the communications between them.

- (Test only) After running the test code, the backend server will **NOT** automatically stop since the shutdown method is deprecated (The shutdown function is therefore useless). Please press `Ctrl+C` manually in the backend server.

### Report

Instead of raw query languages provided by MongoDB, which is almost the same as a highly embedded python dict, I use the ORM of MongoDB pymongo and successfully transplant from sqlite to [pymongo](https://pypi.org/project/pymongo/). 

#### Databases

The [old scrawl script](./fe/data/scraper.py) has failed, and I write a [new scraper](./scraper_new.py) with BeautifulSoup. The new scraper script supports to get book information and save into MongoDB or SQLite, but modify or remove some columns such as `tags`, `pub_year`, `contents` due to the lack of such information, so it can not use directly in this test bash codes, which means you can **NOT** directly replace `fe/data/book_lx.db` with the new generated `scraper.db`. But to run the new scraper with param specified to write in MongoDB, the program can run successfully based on the newly scraped information of books.

The transform is under plan. If you really want to test with another database, please download from [baidu netdisk](https://pan.baidu.com/s/1bjCOW8Z5N_ClcqU54Pdt8g) with password `hj6q`.

#### Test Results

The last test results saved in [`./htmlcov-2024-6-8`](./htmlcov-2024-6-8/index.html). All tests pass but with a coverage rate only 50%. It is because I realized a lot of surrogate functions that will be use in order to function as a real bookstore system, such as `show user info`, `delete book info`, `update book info` and so on. Since it is not required in the homework, I just keep them here without test codes.

#### User Test

Every functions and statements have their usage documentation in [`doc` folder](./doc), and has a relative [`usertest` code](./usertest).

##### Usage of `usertest` code

- Change the directory to `usertest`

  ```
  cd usertest
  ```

- Test the whole function in it

  ```
  python test_user.py
  ```

  The test code does not go through the functions there in order, I have made some changes such that all the test results will be `200 OK` or some of deliberate errors (all the error code start with 5).

  <details>
      <summary>Examples</summary>
      <pre> Test user 
      <code>
  bookstore/usertest$ python test_user.py 
  register:       512 b'{"message":"exist user id admin"}\n'
  login:          200 b'{"message":"ok","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJ0ZXJtaW5hbCI6IiIsInRpbWVzdGFtcCI6MTcxNzgzMjg3Ny42MTA0NDh9.lJUftMSog9Vtlw_6r3zTbIs0SbG55f4whNALM1Im5Xk"}\n'
  change_password:200 b'{"message":"ok"}\n'
  login:          200 b'{"message":"ok","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJ0ZXJtaW5hbCI6IiIsInRpbWVzdGFtcCI6MTcxNzgzMjg3Ny42MjU2ODA3fQ.oTQyBgmqHwfoI14ro1QfX0rfwCvELN8Jr4WQ2Jc5czc"}\n'
  logout:         200 b'{"message":"ok"}\n'
  unregister:     200 b'{"message":"ok"}\n'
  </code>
  Test seller
  <code>
  bookstore/usertest$ python test_seller.py 
  _autologin:     200 b'{"message":"ok","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJ0ZXJtaW5hbCI6IiIsInRpbWVzdGFtcCI6MTcxNzgzMzI3OS41NzAxNjY4fQ.Am8mAkaoruXLcNwxAZ2eotKRriCzyYyw8f-0gPSCtg4"}\n'
  create_store:   200 b'{"message":"ok"}\n'
  get_store_info: 200 {'message': 'ok', 'store_infos': [{'books': [], 'store_id': 'store_1'}]}
  add_book:       530 b'{"message":"argument of type \'NoneType\' is not iterable"}\n'
  get_store_info: 200 {'message': 'ok', 'store_infos': [{'books': [], 'store_id': 'store_1'}]}
  add_stock_level:515 b'{"message":"non exist book id 10539399"}\n'
  get_store_info: 200 {'message': 'ok', 'store_infos': [{'books': [], 'store_id': 'store_1'}]}
  add_book_info:  200 b'{"message":"ok"}\n'
  get_book_info:  200 {'book_info': {'_id': '1145141919810', 'pictures': [], 'price': 666.0, 'title': 'test', 'translator': []}, 'message': 'ok'}
  update_book_info:
                  200 b'{"message":"ok"}\n'
  get_book_info:  200 {'book_info': {'_id': '1145141919810', 'pictures': [], 'price': 999.0, 'title': 'newtitle', 'translator': []}, 'message': 'ok'}
  delete_book_info:
                  200 b'{"message":"ok"}\n'
  get_book_info:  515 b'{"book_info":{},"message":"non exist book id 1145141919810"}\n'
  delete_store:   200 b'{"message":"ok"}\n'</code></pre>
  </details>

- Test some of the functions in it

  ```
  python test_user.py -f {functions}
  ```

  <details>
      <summary>Examples</summary>
      <pre>
  <code>bookstore/usertest$ python test_user.py -f login logout
  login:          200 b'{"message":"ok","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJ0ZXJtaW5hbCI6IiIsInRpbWVzdGFtcCI6MTcxNzgzMzUwNC40OTYwNDY1fQ.QRhDaERkyVlN0fso4-dszNE0vZJNEi_Kdj_oZQhcMMA"}\n'
  logout:         200 b'{"message":"ok"}\n'</code>
      </pre>
  </details>

#### Scheduled System

In [schedule.py](./be/model/schedule.py), I introduce a scheduler to automatically scan the database and check the state of orders. It can be extended further for future features.
