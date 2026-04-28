# SearXNG 快速开始指南

## 5分钟快速上手

### 1. 启动服务

```bash
cd ~/Desktop/OPC/searxng
./manage.sh start
```

### 2. 检查状态

```bash
./scripts/status.sh
```

### 3. 访问搜索

打开浏览器访问: http://localhost:8888

### 4. 使用快捷键

在搜索框中输入：
- `!bd 医疗AI` - 百度搜索
- `!sg 医疗AI` - 搜狗搜索
- `!gs artificial intelligence` - 学术搜索
- `!sgw 医疗AI` - 微信搜索

## Python集成

### 安装依赖

```bash
pip install requests
```

### 基本使用

```python
from api.searxng_api import SearXNGClient

# 创建客户端
client = SearXNGClient()

# 百度搜索
results = client.search_baidu("医疗AI")
for result in results['results'][:3]:
    print(f"标题: {result['title']}")
    print(f"链接: {result['url']}")
```

### 医疗AI集成

```python
from examples.medical_ai_integration import MedicalSearchEngine

# 创建医疗搜索引擎
engine = MedicalSearchEngine()

# 搜索药品信息
drug_info = engine.search_drug_info("阿司匹林")

# 搜索疾病信息
disease_info = engine.search_disease_info("糖尿病")

# 搜索罕见病信息
rare_info = engine.search_rare_disease("渐冻症")

# 搜索药物相互作用
interaction_info = engine.search_drug_interactions("阿司匹林", "华法林")
```

## JSON API

### 使用curl

```bash
# JSON格式搜索
curl "http://localhost:8888/search?q=医疗AI&format=json"

# 百度搜索
curl "http://localhost:8888/search?q=医疗AI&format=json&engines=baidu"

# 学术搜索
curl "http://localhost:8888/search?q=artificial+intelligence&format=json&engines=google_scholar,arxiv"
```

### 使用Python

```python
import requests

# JSON格式搜索
response = requests.get("http://localhost:8888/search", params={
    "q": "医疗AI",
    "format": "json",
    "engines": "baidu"
})
data = response.json()
print(f"结果数: {len(data['results'])}")
```

## 常用命令

```bash
# 启动服务
./manage.sh start

# 停止服务
./manage.sh stop

# 重启服务
./manage.sh restart

# 查看状态
./manage.sh status

# 查看日志
./manage.sh logs

# 测试服务
./manage.sh test

# 备份配置
./manage.sh backup

# 检查状态
./scripts/status.sh

# 运行测试
./scripts/full-test.sh
```

## 搜索引擎列表

### 国内搜索引擎
| 快捷键 | 引擎 | 说明 |
|--------|------|------|
| `!bd` | 百度 | 通用搜索 |
| `!sg` | 搜狗 | 通用搜索 |
| `!360` | 360搜索 | 通用搜索 |
| `!bdi` | 百度图片 | 图片搜索 |
| `!sgi` | 搜狗图片 | 图片搜索 |
| `!360v` | 360视频 | 视频搜索 |
| `!sgv` | 搜狗视频 | 视频搜索 |
| `!sgw` | 搜狗微信 | 微信搜索 |
| `!bdk` | 百度开发者 | 开发者搜索 |

### 国际搜索引擎
| 快捷键 | 引擎 | 说明 |
|--------|------|------|
| `!go` | Google | 通用搜索 |
| `!ddg` | DuckDuckGo | 通用搜索 |
| `!bi` | Bing | 通用搜索 |
| `!br` | Brave | 通用搜索 |
| `!gs` | Google Scholar | 学术搜索 |
| `!arx` | arXiv | 学术搜索 |
| `!wp` | Wikipedia | 知识库 |
| `!gh` | GitHub | 代码搜索 |
| `!st` | StackOverflow | 技术问答 |
| `!hf` | HuggingFace | AI模型搜索 |

## 故障排除

### 服务无法启动

```bash
# 检查Docker
docker info

# 查看日志
docker logs searxng

# 重启服务
./manage.sh restart
```

### 搜索无结果

```bash
# 检查Redis
docker exec searxng-redis redis-cli ping

# 测试搜索
curl "http://localhost:8888/search?q=test"
```

### JSON API返回403

```bash
# 检查配置
grep -A 5 "formats:" ~/.docker/searxng/config/settings.yml

# 确保配置包含JSON格式
search:
  formats:
    - html
    - json
    - csv
    - rss

# 重启服务
docker restart searxng
```

## 获取帮助

- 查看完整文档: `cat README.md`
- 查看项目状态: `cat PROJECT_STATUS.md`
- 检查服务状态: `./scripts/status.sh`
