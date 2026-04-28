# SearXNG Medical AI 使用场景

## 1. 医疗AI研究

### 场景描述
医疗AI研究人员需要搜索最新的学术文献、临床试验数据、药物研发进展。

### 使用方法
```python
from examples.medical_search_pro import MedicalSearchPro

engine = MedicalSearchPro()

# 搜索最新研究
results = engine.search_medical_literature("transformer healthcare", year_from=2023)

# 搜索临床试验
results = engine.search_drug_info("PD-1抑制剂", depth="comprehensive")
```

### 快捷键
- `!gs 人工智能 医疗` - Google Scholar学术搜索
- `!arx machine learning healthcare` - arXiv预印本搜索
- `!pm clinical trial` - PubMed医学文献

---

## 2. 药品信息查询

### 场景描述
医生、药师需要查询药品说明书、药物相互作用、不良反应等信息。

### 使用方法
```python
from examples.medical_search_pro import MedicalSearchPro

engine = MedicalSearchPro()

# 查询药品信息
drug_info = engine.search_drug_info("阿司匹林", depth="comprehensive")

# 查询药物相互作用
interaction = engine.search_drug_interactions("阿司匹林", "华法林")
```

### 快捷键
- `!bd 阿司匹林 说明书` - 百度搜索药品信息
- `!bd 药物相互作用` - 搜索药物相互作用

---

## 3. 罕见病诊疗

### 场景描述
罕见病患者、家属、医生需要查询疾病信息、治疗方案、患者社区。

### 使用方法
```python
from examples.medical_search_pro import MedicalSearchPro

engine = MedicalSearchPro()

# 查询罕见病信息
rare_info = engine.search_rare_disease("渐冻症")

# 查询临床指南
guidelines = engine.search_clinical_guidelines("渐冻症", country="all")
```

### 快捷键
- `!bd 渐冻症 罕见病` - 百度搜索罕见病信息
- `!sgw 渐冻症 患者` - 微信搜索患者社区

---

## 4. 学术文献检索

### 场景描述
研究生、学者需要检索学术文献、综述、Meta分析。

### 使用方法
```python
from api.searxng_api import SearXNGClient

client = SearXNGClient()

# 学术搜索
results = client.search_academic("systematic review diabetes treatment")

# arXiv搜索
results = client.search_academic("transformer model arxiv")
```

### 快捷键
- `!gs systematic review` - Google Scholar搜索
- `!arx deep learning` - arXiv搜索
- `!ss semantic scholar` - Semantic Scholar搜索

---

## 5. 开发者资源搜索

### 场景描述
开发者需要搜索代码、技术文档、开源项目。

### 使用方法
```python
from api.searxng_api import SearXNGClient

client = SearXNGClient()

# GitHub搜索
results = client.search_dev("medical AI python")

# StackOverflow搜索
results = client.search_dev("docker compose tutorial")
```

### 快捷键
- `!gh medical AI` - GitHub代码搜索
- `!st docker tutorial` - StackOverflow技术问答
- `!hf transformers` - HuggingFace模型搜索

---

## 6. 医疗新闻监控

### 场景描述
医疗行业从业者需要监控最新的医疗新闻、政策法规。

### 使用方法
```python
from api.searxng_api import SearXNGClient

client = SearXNGClient()

# 微信公众号搜索
results = client.search_wechat("医疗AI政策")

# 新闻搜索
results = client.search("医疗改革 新闻", engines=["baidu", "sogou"])
```

### 快捷键
- `!sgw 医疗AI` - 微信公众号搜索
- `!bd 医疗新闻` - 百度新闻搜索

---

## 7. 企业内部搜索

### 场景描述
企业需要搭建私有搜索服务，保护商业机密。

### 部署方法
```bash
# 一键部署
./scripts/deploy.sh prod 8888

# 配置HTTPS
# 编辑 nginx/nginx.conf

# 配置访问控制
# 编辑 config/settings.yml
```

---

## 8. 教育科研

### 场景描述
高校、科研机构需要为师生提供学术搜索服务。

### 部署方法
```bash
# 部署到校园网
./scripts/deploy.sh prod 8888

# 配置学术搜索引擎
# 编辑 config/settings-medical.yml
```

---

## 9. 个人隐私搜索

### 场景描述
注重隐私的用户需要无追踪的搜索服务。

### 使用方法
- 访问 http://localhost:8888
- 所有搜索不记录、不追踪
- 支持暗黑模式保护眼睛

---

## 10. API集成

### 场景描述
第三方应用需要集成搜索功能。

### API调用
```python
import requests

# JSON格式搜索
response = requests.get("http://localhost:8888/search", params={
    "q": "医疗AI",
    "format": "json",
    "engines": "baidu,google"
})

data = response.json()
print(f"结果数: {len(data['results'])}")
```

---

## 商业价值

### 1. 降低搜索成本
- 自建搜索引擎，无需付费API
- 聚合多个免费搜索引擎

### 2. 保护数据隐私
- 零追踪、零记录
- 符合GDPR/HIPAA合规要求

### 3. 提升搜索效率
- 多源聚合，一次搜索获取全网结果
- 专业医疗搜索引擎优化

### 4. 支持AI应用
- JSON API接口
- 支持RAG架构集成

### 5. 可定制化
- 开源代码，可自由修改
- 支持自定义搜索引擎
