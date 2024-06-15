## 创建商铺

#### URL

POST http://[address]/seller/create_store

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "user_id": "$seller id$",
  "store_id": "$store id$"
}
```

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 卖家用户ID | N
store_id | string | 商铺ID | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 创建商铺成功
5XX | 商铺ID已存在

## 删除商铺（New）

#### URL

POST http://[address]/seller/delete_store

#### Request

Headers:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

Body:

```json
{
  "user_id": "$seller id$",
  "store_id": "$store id$",
  "password": "$password$"
}
```

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 卖家用户ID | N          |
| store_id | string | 商铺ID     | N          |
| password | string | 用户ID密码 | N          |

#### Response

Status Code:

| 码   | 描述         |
| ---- | ------------ |
| 200  | 删除商铺成功 |
| 5XX  | 商铺ID不存在 |

## 商家添加书籍至库存（Modified）

#### URL：
POST http://[address]/seller/add_book

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "user_id": "$seller user id$",
  "store_id": "$store id$",
  "book_info": "$book info$",
  "stock_level": 0
}

```

属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 卖家用户ID | N
store_id | string | 商铺ID | N
book_info | dict | 书籍详细信息 | N
stock_level | int | 初始库存，大于等于0 | N

#### Response

Status Code:

| 码   | 描述             |
| ---- | ---------------- |
| 200  | 添加图书信息成功 |
| 5XX  | 卖家用户ID不存在 |
| 5XX  | 商铺ID不存在     |
| 5XX  | 图书ID已存在     |

## 添加书籍至书籍库（New）

#### URL：

POST http://[address]/seller/add_book_info

#### Request

Body:

```json
{
  "book_info_json": {
      "book_id": "$id$",
      "title": "$title$",
      "author": "$author$",
      "publisher": "$publisher$",
      "original_title": "$original_title$",
      "translator": [
          "$translator1$",
          ....
      ],
      "pub_time": "$pub_time$",
      "pages": "$pages$",
      "price": "$price$",
      "currency_unit": "$currency_unit$",
      "binding": "$binding$",
      "isbn": "$isbn$",
      "author_intro": "$author_intro$",
      "book_intro": "$book_intro$",
      "pictures": [
          "$pic_bytes1",
          ....
      ]
  }
}

```

属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 书籍ID | N
title | string | 书籍题目 | N
author | string | 作者 | Y
publisher | string | 出版社 | Y
original_title | string | 原书题目 | Y
translator | array | 译者 | Y
pub_time | string | 出版年月，如"2002-9-1" | Y
pages | int | 页数 | Y
price | float | 价格 | N
currency_unit | string | 货币单位 | Y 
binding | string | 装帧，精状/平装 | Y
isbn | string | ISBN号 | Y
author_intro | string | 作者简介 | Y
book_intro | string | 书籍简介 | Y
 pictures       | array  | 照片                   | Y          

    picture 中每个数组元素都是string（base64表示的bytes array）类型


#### Response

Status Code:

码 | 描述
--- | ---
200 | 添加图书信息成功
406 | 信息不完整 
5XX | 卖家用户ID不存在
5XX | 商铺ID不存在
516 | 图书ID已存在，请使用更新书籍库 

## 更新书籍库书籍（New）

#### URL：

POST http://[address]/seller/update_book_info

#### Request

Body:

```json
{
  "book_info_json": {
      "book_id": "$id$",
      "title": "$title$",
      "author": "$author$",
      "publisher": "$publisher$",
      "original_title": "$original_title$",
      "translator": [
          "$translator1$",
          ....
      ],
      "pub_time": "$pub_time$",
      "pages": "$pages$",
      "price": "$price$",
      "currency_unit": "$currency_unit$",
      "binding": "$binding$",
      "isbn": "$isbn$",
      "author_intro": "$author_intro$",
      "book_intro": "$book_intro$",
      "pictures": [
          "$pic_bytes1",
          ....
      ]
  }
}

```

属性说明：

| 变量名         | 类型   | 描述                   | 是否可为空 |
| -------------- | ------ | ---------------------- | ---------- |
| id             | string | 书籍ID                 | N          |
| title          | string | 书籍题目               | N          |
| author         | string | 作者                   | Y          |
| publisher      | string | 出版社                 | Y          |
| original_title | string | 原书题目               | Y          |
| translator     | array  | 译者                   | Y          |
| pub_time       | string | 出版年月，如"2002-9-1" | Y          |
| pages          | int    | 页数                   | Y          |
| price          | float  | 价格                   | N          |
| currency_unit  | string | 货币单位               | Y          |
| binding        | string | 装帧，精状/平装        | Y          |
| isbn           | string | ISBN号                 | Y          |
| author_intro   | string | 作者简介               | Y          |
| book_intro     | string | 书籍简介               | Y          |
| pictures       | array  | 照片                   | Y          |

    picture 中每个数组元素都是string（base64表示的bytes array）类型


#### Response

Status Code:

| 码   | 描述                           |
| ---- | ------------------------------ |
| 200  | 添加图书信息成功               |
| 406  | 信息不完整                     |
| 5XX  | 卖家用户ID不存在               |
| 5XX  | 商铺ID不存在                   |
| 515  | 图书ID不存在，请使用添加书籍库 |

## 商家添加书籍库存


#### URL

POST http://[address]/seller/add_stock_level

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "user_id": "$seller id$",
  "store_id": "$store id$",
  "book_id": "$book id$",
  "add_stock_level": 10
}
```
key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 卖家用户ID | N
store_id | string | 商铺ID | N
book_id | string | 书籍ID | N
add_stock_level | int | 增加的库存量 | N

#### Response

Status Code:

码 | 描述
--- | :--
200 | 创建商铺成功
5XX | 商铺ID不存在 
5XX | 图书ID不存在 

## 删除书籍信息（New）

#### URL

POST http://[address]/seller/delete_book_info

#### Request

Body:

```json
{
  "book_id": "$book id$"
}
```

| key     | 类型   | 描述   | 是否可为空 |
| ------- | ------ | ------ | ---------- |
| book_id | string | 书籍ID | N          |

#### Response

Status Code:

| 码   | 描述         |
| ---- | ------------ |
| 200  | 删除书籍成功 |
| 5XX  | 书籍ID不存在 |

## 查询商铺信息（New）

#### URL

GET/POST http://[address]/seller/get_store_info

#### Request

Headers:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

Body:

```json
{
  "user_id": "$user_id$"
}
```

| key     | 类型   | 描述   | 是否可为空 |
| ------- | ------ | ------ | ---------- |
| user_id | string | 用户ID | N          |

#### Response

Status Code:

| 码   | 描述         |
| ---- | ------------ |
| 200  | 查询成功     |
| 5XX  | 商铺ID不存在 |

Body:

```json
{
    "message":"$error message$",
    "store_infos": 
    [
        {
            "store_id": "$store_id$",
            "books": 
            [
                {
                    "book_id": "$book_id$",
                    "stock_level": "$stock_level$",
                    "book_info": 
                    {
                        ....
                    }
                },
                ....
            ]
        },
        ....
    ]
}
```

| 变量名     | 类型   | 描述                       | 是否可为空 |
| ---------- | ------ | -------------------------- | ---------- |
| message    | string | 返回错误消息，成功时为"ok" | N          |
| store_info | json   | 详细信息                   | Y          |

## 查询书籍信息（New）

#### URL

GET/POST http://[address]/seller/get_book_info

#### Request

Body:

```json
{
  "book_id": "$book id$"
}
```

| key     | 类型   | 描述   | 是否可为空 |
| ------- | ------ | ------ | ---------- |
| book_id | string | 书籍ID | N          |

#### Response

Status Code:

| 码   | 描述         |
| ---- | ------------ |
| 200  | 查询成功     |
| 5XX  | 书籍ID不存在 |

Body:

```json
{
    "message":"$error message$",
    "book_info":  
    {
        ....
    }
}
```

| 变量名    | 类型   | 描述                       | 是否可为空     |
| --------- | ------ | -------------------------- | -------------- |
| message   | string | 返回错误消息，成功时为"ok" | N              |
| book_info | json   | 详细信息                   | N (If success) |

```
book_info 字段中仅含有非空的键值对。否则将不会返回。
```

## 卖家取消订单（New）

#### URL：

POST http://[address]/seller/cancel_order

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | string | 订单ID     | N          |


Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 取消成功 |
| 400  | 操作失败 |
| 5XX  | 无效参数 |

## 卖家确认发货（New）

#### URL：

POST http://[address]/seller/ship_order

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | string | 订单ID     | N          |


Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 发货成功 |
| 400  | 操作失败 |
| 5XX  | 无效参数 |

