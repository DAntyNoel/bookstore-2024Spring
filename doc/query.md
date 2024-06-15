## 查询历史订单

#### URL

POST http://[address]/query/order

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "order_id": "$order_id$",
  "user_id": "$user_id$",
  "store_id": "$store_id$",
  "statecode": "$statecode",
  ....
}
```

key | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单用户ID | Y 
user_id | string | 卖家用户ID | Y
store_id | string | 商铺ID     | Y 
statecode | int | 订单状态   | Y 

在Body中给出的内容将作为MongoDB的查询条件。

#### Response

Status Code:

码 | 描述
--- | ---
200 | 查询成功 
528 | 查询条件存在问题 

## 查询图书信息

#### URL

POST http://[address]/query/book

#### Request

Headers:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

Body:

```json
{
  "price__gte": "$the minimum price$",
  "user_id": "$user_id$",
  "book_id": "$book_id$",
  ....
}
```

| key        | 类型   | 描述                          | 是否可为空 |
| ---------- | ------ | ----------------------------- | ---------- |
| price__gte | int    | 价格（允许使用Mongo运算语法） | Y          |
| user_id    | string | 卖家用户ID                    | Y          |
| book_id    | string | 书籍ID                        | Y          |

在Body中给出的内容将作为MongoDB的BookInfo查询条件。

- user_id除外，它将筛选指定用户的所有商家

#### Response

Status Code:

| 码   | 描述             |
| ---- | ---------------- |
| 200  | 查询成功         |
| 528  | 查询条件存在问题 |
