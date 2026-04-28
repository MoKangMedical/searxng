# SearXNG 私有搜索引擎 - 医疗AI版

基于Docker部署的SearXNG私有元搜索引擎，针对中国网络环境优化，专为医疗AI项目设计。

## 特性

### 搜索引擎
- **国内搜索引擎**: 百度、搜狗、360搜索
- **学术搜索**: Google Scholar、arXiv
- **开发者资源**: GitHub、StackOverflow、HuggingFace
- **微信搜索**: 通过搜狗微信搜索公众号文章
- **图片搜索**: 百度图片、搜狗图片、Google图片
- **视频搜索**: 360视频、搜狗视频、YouTube

### 功能特性
- **JSON API**: 支持JSON格式API调用
- **Redis缓存**: 24小时缓存，避免重复请求
- **健康检查**: 自动监控服务状态
- **自动重启**: 服务异常时自动重启
- **备份恢复**: 完整的备份和恢复机制
- **医疗AI集成**: 支持MediChat-RD、DrugMind等项目
- **自定义界面**: 医疗AI品牌标识和样式

## 快速开始

### 一键安装

```bash
# 克隆项目
git clone https://github.com/MoKangMedical/searxng.git
cd searxng

# 运行安装脚本
./install.sh
```

### 手动安装

```bash
# 启动服务
./manage.sh start

# 查看状态
./manage.sh status

# 测试服务
./manage.sh test
```

## 项目结构

```
searxng/
├── config/                 # 配置文件
│   ├── settings.yml       # 主配置文件
│   ├── limiter.toml       # 限制器配置
│   ├── custom.css         # 自定义样式
│   └── custom_header.html # 自定义头部
├── scripts/               # 脚本目录
│   ├── deploy.sh          # 部署脚本
│   ├── monitor.sh         # 监控脚本
│   ├── backup.sh          # 备份脚本
│   ├── restore.sh         # 恢复脚本
│   ├── status.sh          # 状态检查
│   ├── full-test.sh       # 完整测试
│   └── quick-test.sh      # 快速测试
├── api/                   # API客户端
│   ├── searxng_api.py     # Python客户端
│   └── searxng.js         # JavaScript客户端
├── examples/              # 使用示例
│   ├── python_example.py  # Python示例
│   ├── nodejs_example.js  # Node.js示例
│   └── medical_ai_integration.py  # 医疗AI集成
├── templates/             # 配置模板
│   ├── settings.dev.yml   # 开发环境配置
│   └── settings.prod.yml  # 生产环境配置
├── nginx/                 # Nginx配置
│   └── nginx.conf         # Nginx配置文件
├── docker-compose.yml     # Docker Compose配置
├── manage.sh              # 管理脚本
├── install.sh             # 安装脚本
├── .env.example           # 环境变量模板
├── .gitignore             # Git忽略文件
└── README.md              # 项目说明
```

## 使用方法

### 管理命令

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

# 更新配置
./manage.sh update

# 备份配置
./manage.sh backup
```

### 状态检查

```bash
# 检查项目状态
./scripts/status.sh

# 运行完整测试
./scripts/full-test.sh
```

## API 接口

### Python API

```python
from api.searxng_api import SearXNGClient

# 创建客户端
client = SearXNGClient("http://localhost:8888")

# 百度搜索
results = client.search_baidu("医疗AI")

# 学术搜索
results = client.search_academic("artificial intelligence")

# 微信搜索
results = client.search_wechat("医疗AI")

# 自定义搜索
results = client.search(
    "医疗AI",
    engines=["baidu", "sogou", "google_scholar"],
    language="zh-CN"
)
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

# 搜索罕见病信息（用于MediChat-RD）
rare_disease_info = engine.search_rare_disease("渐冻症")

# 搜索药物相互作用
interaction_info = engine.search_drug_interactions("阿司匹林", "华法林")
```

### JavaScript API

```javascript
const SearXNGClient = require('./api/searxng');

// 创建客户端
const client = new SearXNGClient('http://localhost:8888');

// 百度搜索
const results = await client.searchBaidu('医疗AI');

// 学术搜索
const academicResults = await client.searchAcademic('artificial intelligence');

// 微信搜索
const wechatResults = await client.searchWechat('医疗AI');
```

### curl API

```bash
# JSON格式搜索
curl "http://localhost:8888/search?q=医疗AI&format=json"

# 百度搜索
curl "http://localhost:8888/search?q=医疗AI&format=json&engines=baidu"

# 学术搜索
curl "http://localhost:8888/search?q=artificial+intelligence&format=json&engines=google_scholar,arxiv"
```

## 集成到其他项目

### MediChat-RD 罕见病AI诊疗平台

```python
# 在MediChat-RD项目中使用SearXNG
from medical_ai_integration import MedicalSearchEngine

class RareDiseaseSearch:
    def __init__(self):
        self.engine = MedicalSearchEngine()
    
    def search_disease_info(self, disease_name):
        """搜索罕见病信息"""
        return self.engine.search_rare_disease(disease_name)
    
    def search_treatment_options(self, disease_name):
        """搜索治疗方案"""
        results = self.engine.search_clinical_guidelines(disease_name)
        return results

# 使用示例
rare_disease_search = RareDiseaseSearch()
results = rare_disease_search.search_disease_info("渐冻症")
```

### DrugMind 药物研发平台

```python
# 在DrugMind项目中使用SearXNG
from medical_ai_integration import MedicalSearchEngine

class DrugSearch:
    def __init__(self):
        self.engine = MedicalSearchEngine()
    
    def search_drug_info(self, drug_name):
        """搜索药品信息"""
        return self.engine.search_drug_info(drug_name)
    
    def search_clinical_trials(self, drug_name):
        """搜索临床试验"""
        results = self.engine.search_medical_literature(f"{drug_name} clinical trial")
        return results

# 使用示例
drug_search = DrugSearch()
results = drug_search.search_drug_info("阿司匹林")
```

## 搜索引擎快捷键

### 国内搜索引擎
- `!bd 关键词` - 百度搜索
- `!sg 关键词` - 搜狗搜索
- `!360 关键词` - 360搜索
- `!bdi 关键词` - 百度图片
- `!sgi 关键词` - 搜狗图片
- `!360v 关键词` - 360视频
- `!sgv 关键词` - 搜狗视频
- `!sgw 关键词` - 微信搜索
- `!bdk 关键词` - 百度开发者

### 国际搜索引擎
- `!go 关键词` - Google搜索
- `!ddg 关键词` - DuckDuckGo搜索
- `!bi 关键词` - Bing搜索
- `!br 关键词` - Brave搜索
- `!gs 关键词` - Google Scholar
- `!arx 关键词` - arXiv搜索
- `!wp 关键词` - Wikipedia
- `!gh 关键词` - GitHub搜索
- `!st 关键词` - StackOverflow
- `!hf 关键词` - HuggingFace
- `!gis 关键词` - Google图片
- `!bii 关键词` - Bing图片
- `!yt 关键词` - YouTube

## 配置说明

### 环境配置

- **开发环境**: `templates/settings.dev.yml`
  - 调试模式开启
  - 缓存时间较短（1小时）
  - 无请求限制

- **生产环境**: `templates/settings.prod.yml`
  - 调试模式关闭
  - 缓存时间较长（24小时）
  - 启用请求限制

### 自定义配置

编辑 `config/settings.yml` 文件：

```yaml
# 启用JSON API
search:
  formats:
    - html
    - json
    - csv
    - rss

# 修改自动补全
search:
  autocomplete: "baidu"

# 添加新的引擎
engines:
  - name: new_engine
    engine: new_engine
    shortcut: ne
    categories: [general]
    disabled: false
```

## 故障排除

### 服务无法启动

```bash
# 检查Docker状态
docker info

# 查看错误日志
docker logs searxng

# 重新构建
./manage.sh stop
./manage.sh start
```

### 搜索无结果

```bash
# 检查Redis连接
docker exec searxng-redis redis-cli ping

# 查看引擎状态
curl "http://localhost:8888/stats"

# 测试特定引擎
curl "http://localhost:8888/search?q=!bd+test"
```

### JSON API返回403

```bash
# 检查配置文件
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

## 相关链接

- [SearXNG官方文档](https://docs.searxng.org/)
- [SearXNG GitHub](https://github.com/searxng/searxng)
- [Docker文档](https://docs.docker.com/)
- [Redis文档](https://redis.io/documentation)

## 许可证

本项目基于MIT许可证开源。

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- GitHub: [MoKangMedical](https://github.com/MoKangMedical)
