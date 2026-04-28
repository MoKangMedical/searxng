# SearXNG Medical AI API 文档

## 概述

SearXNG Medical AI 提供RESTful API接口，支持JSON格式的搜索请求。

## 基础URL

```
http://localhost:8888
```

## 认证

API支持两种认证方式：

### 1. API Key认证

在请求头中添加API Key：

```bash
curl -H "X-API-Key: your-api-key" "http://localhost:8888/search?q=test&format=json"
```

### 2. 查询参数认证

```bash
curl "http://localhost:8888/search?q=test&format=json&api_key=your-api-key"
```

## 端点

### 搜索

```
GET /search
```

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| q | string | 是 | 搜索查询 |
| format | string | 否 | 返回格式 (json/csv/rss/html) |
| engines | string | 否 | 搜索引擎列表 (逗号分隔) |
| language | string | 否 | 搜索语言 |
| pageno | int | 否 | 页码 |
| time_range | string | 否 | 时间范围 (day/week/month/year) |
| safe_search | int | 否 | 安全搜索级别 (0/1/2) |

**示例：**

```bash
# 基础搜索
curl "http://localhost:8888/search?q=医疗AI&format=json"

# 指定搜索引擎
curl "http://localhost:8888/search?q=医疗AI&format=json&engines=baidu,google"

# 学术搜索
curl "http://localhost:8888/search?q=artificial+intelligence&format=json&engines=google_scholar,arxiv"
```

**响应：**

```json
{
  "query": "医疗AI",
  "number_of_results": 50,
  "results": [
    {
      "url": "https://example.com",
      "title": "医疗AI概述",
      "content": "医疗AI是指...",
      "engine": "google",
      "score": 0.95
    }
  ],
  "answers": [],
  "corrections": [],
  "infoboxes": [],
  "suggestions": []
}
```

### 配置

```
GET /config
```

返回搜索引擎配置信息。

### 统计

```
GET /stats
```

返回搜索引擎使用统计。

## 错误处理

### 错误响应格式

```json
{
  "error": "错误信息",
  "code": 400
}
```

### 错误代码

| 代码 | 描述 |
|------|------|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## 速率限制

- 默认限制：60请求/分钟
- 响应头包含限制信息：
  - `X-RateLimit-Limit`: 限制总数
  - `X-RateLimit-Remaining`: 剩余请求数
  - `X-RateLimit-Reset`: 重置时间

## SDK

### Python SDK

```python
from api.searxng_api import SearXNGClient

client = SearXNGClient("http://localhost:8888")
results = client.search("医疗AI", format="json")
```

### JavaScript SDK

```javascript
const client = new SearXNGClient('http://localhost:8888');
const results = await client.search('医疗AI');
```

## 示例

### Python示例

```python
import requests

# 搜索
response = requests.get("http://localhost:8888/search", params={
    "q": "医疗AI",
    "format": "json",
    "engines": "baidu,google"
})

data = response.json()
print(f"结果数: {len(data['results'])}")
```

### cURL示例

```bash
# 百度搜索
curl "http://localhost:8888/search?q=医疗AI&format=json&engines=baidu"

# 学术搜索
curl "http://localhost:8888/search?q=artificial+intelligence&format=json&engines=google_scholar,arxiv"

# 微信搜索
curl "http://localhost:8888/search?q=医疗AI&format=json&engines=sogou_wechat"
```
