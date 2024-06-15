## 获取书籍信息

#### URL

GET `http://[address]/info/book/<id>`

#### Request

Headers:

| 键    | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | 否         |

Url args:

| 变量名 | 类型   | 描述   | 是否可为空 |
| ------ | ------ | ------ | ---------- |
| id     | string | 书籍ID | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 请求成功       |
| 301  | 登录过期       |
| 528  | 数据库异常     |
| 530  | 服务器内部错误 |

Body:

```json
{
  "message": "$error message$",
  "book_info": {
    ....// 包含书籍信息的JSON对象
  }
}
```

## 获取用户信息

#### URL

GET `http://[address]/info/user/<id>`

#### Request

Headers:

| 键    | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | 否         |

Url args:

| 变量名 | 类型   | 描述   | 是否可为空 |
| ------ | ------ | ------ | ---------- |
| id     | string | 用户ID | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 请求成功       |
| 301  | 登录过期       |
| 528  | 数据库异常     |
| 530  | 服务器内部错误 |

Body:

```json
{
  "message": "$error message$",
  "user_info": {
    ....// 包含用户信息的JSON对象
  }
}
```

## 获取订单信息

#### URL

GET `http://[address]/info/order/<id>`

#### Request

Headers:

| 键    | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | 否         |

Url args:

| 变量名 | 类型   | 描述   | 是否可为空 |
| ------ | ------ | ------ | ---------- |
| id     | string | 订单ID | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 请求成功       |
| 301  | 登录过期       |
| 528  | 数据库异常     |
| 530  | 服务器内部错误 |

Body:

```json
{
  "message": "$error message$",
  "order_info": {
    "order_id": "$order_id$",
    "user_id": "$user_id$",
    "store_id": "$store_id$",
    "statecode": "$state$",
    "timestamp": "$last modified time$",
    "history": [
        {
            "statecode": "$state$",
            "timestamp": "$last modified time$",
        },
        ....
    ],
    "order_detail": {
      "book_id": "$book_id$",
      "count": "$count$",
      "price": "$price$"
    }
  }
}
```

## 获取商铺信息

#### URL

GET `http://[address]/info/store/<id>`

#### Request

Headers:

| 键    | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | 否         |

Url args:

| 变量名 | 类型   | 描述   | 是否可为空 |
| ------ | ------ | ------ | ---------- |
| id     | string | 商铺ID | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 请求成功       |
| 301  | 登录过期       |
| 528  | 数据库异常     |
| 530  | 服务器内部错误 |

Body:

```json
{
  "message": "$error message$",
  "store_info": {
      // 商铺信息
    }
  }
}
```

## 获取用户商铺信息

#### URL

GET `http://[address]/info/user/<id>/stores`

#### Request

Headers:

| 键    | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | 否         |

Url args:

| 变量名 | 类型   | 描述   | 是否可为空 |
| ------ | ------ | ------ | ---------- |
| id     | string | 用户ID | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 请求成功       |
| 301  | 登录过期       |
| 528  | 数据库异常     |
| 530  | 服务器内部错误 |

Body:

```json
{
  "message": "$error message$",
  "store_infos": [
      {$store_info$},
      ....
  ]
}
```

