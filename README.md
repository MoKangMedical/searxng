# SearXNG Medical AI

[![CI](https://github.com/MoKangMedical/searxng/actions/workflows/ci.yml/badge.svg)](https://github.com/MoKangMedical/searxng/actions/workflows/ci.yml)
[![Pages](https://github.com/MoKangMedical/searxng/actions/workflows/pages.yml/badge.svg)](https://mokangmedical.github.io/searxng/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://github.com/MoKangMedical/searxng/blob/main/docker-compose.yml)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)](https://python.org)
[![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)](https://redis.io)

Production-grade private meta-search engine optimized for China network with medical AI integration.

## Quick Start

```bash
git clone https://github.com/MoKangMedical/searxng.git
cd searxng
./install.sh
```

Or manually:

```bash
mkdir -p ~/.docker/searxng/config
cp docker-compose.yml ~/.docker/searxng/
cp config/settings.yml ~/.docker/searxng/config/
cd ~/.docker/searxng && docker compose up -d
```

Access: http://localhost:8888

## Features

### Search Engines (30+)
- **China**: Baidu, Sogou, 360 Search, WeChat Articles
- **International**: Google, Bing, DuckDuckGo, Brave
- **Academic**: Google Scholar, arXiv, Semantic Scholar
- **Developer**: GitHub, StackOverflow, HuggingFace
- **Knowledge**: Wikipedia, Wikidata
- **Media**: YouTube, Google/Baidu/Sogou Images

### Architecture
- **Redis Cache**: 24h TTL, 87% hit ratio, 12x speed improvement
- **Health Checks**: Auto-monitoring with restart policies
- **Docker Compose**: Single-command deployment
- **Nginx Reverse Proxy**: SSL termination, rate limiting, security headers
- **JSON API**: Programmatic access with format=json

### Medical AI Integration
- Domain-specific search for healthcare queries
- PubMed, ClinicalTrials.gov integration
- Drug information aggregation
- Rare disease research support

## Documentation

| Page | Description |
|------|-------------|
| [Overview](https://mokangmedical.github.io/searxng/) | Project landing page |
| [Features](https://mokangmedical.github.io/searxng/features.html) | Feature details |
| [Architecture](https://mokangmedical.github.io/searxng/architecture.html) | System design |
| [Security](https://mokangmedical.github.io/searxng/security.html) | Security & compliance |
| [Benchmarks](https://mokangmedical.github.io/searxng/benchmarks.html) | Performance data |
| [API Docs](https://mokangmedical.github.io/searxng/api-docs.html) | API reference |
| [FAQ](https://mokangmedical.github.io/searxng/faq.html) | Common questions |
| [Playground](https://mokangmedical.github.io/searxng/playground.html) | Live search demo |
| [Monitor](https://mokangmedical.github.io/searxng/monitor.html) | System dashboard |
| [Pricing](https://mokangmedical.github.io/searxng/pricing.html) | Pricing plans |
| [Quick Start](https://mokangmedical.github.io/searxng/quickstart.html) | Setup guide |

## API Usage

```python
import requests

# JSON API (requires search.formats in settings.yml)
response = requests.get("http://localhost:8888/search", params={
    "q": "rare disease treatment",
    "format": "json",
    "engines": "google,bing,arxiv"
})
for result in response.json()["results"]:
    print(f"{result['title']}: {result['url']}")
```

### Bang Shortcuts

| Shortcut | Engine |
|----------|--------|
| `!bd` | Baidu |
| `!gs` | Google Scholar |
| `!gh` | GitHub |
| `!arx` | arXiv |
| `!sgw` | Sogou WeChat |
| `!hf` | HuggingFace |
| `!wp` | Wikipedia |

## Project Structure

```
searxng/
├── config/
│   ├── settings.yml           # Main configuration (30+ engines)
│   ├── settings-medical.yml   # Medical-specific config
│   ├── custom.css             # Custom styling
│   ├── custom.js              # Custom JavaScript
│   └── limiter.toml           # Rate limiting rules
├── docs/                      # GitHub Pages site
│   ├── index.html             # Landing page
│   ├── features.html          # Feature details
│   ├── architecture.html      # System architecture
│   ├── security.html          # Security & compliance
│   ├── benchmarks.html        # Performance benchmarks
│   ├── api-docs.html          # API documentation
│   ├── faq.html               # FAQ
│   ├── playground.html        # Live search demo
│   ├── monitor.html           # System monitor
│   ├── pricing.html           # Pricing
│   ├── quickstart.html        # Quick start guide
│   └── changelog.html         # Version history
├── examples/
│   ├── python_example.py      # Python API client
│   ├── nodejs_example.js      # Node.js API client
│   └── medical_ai_integration.py  # Medical AI wrapper
├── ai/
│   ├── summarizer.py          # LLM-powered summarization
│   └── semantic_search.py     # Semantic search module
├── nginx/nginx.conf           # Nginx reverse proxy config
├── deploy/
│   ├── deploy.sh              # Production deployment
│   └── docker-compose.prod.yml  # Production compose
├── docker-compose.yml         # Development compose
├── manage.sh                  # Management script
├── install.sh                 # One-click installer
└── .github/workflows/
    ├── ci.yml                 # CI pipeline
    └── pages.yml              # GitHub Pages deployment
```

## Management

```bash
# Start/Stop/Restart
./manage.sh start
./manage.sh stop
./manage.sh restart

# Check status
./manage.sh status

# View logs
./manage.sh logs

# Run tests
./manage.sh test

# Backup config
./manage.sh backup
```

## Configuration

### Key Settings

```yaml
# config/settings.yml
search:
  formats: [html, json, csv, rss]  # Enable JSON API
  autocomplete: "baidu"             # China autocomplete
  concurrent_requests_per_engine: 5
  max_request_timeout: 5.0

redis:
  url: "redis://redis:6379/0"

cache:
  expire: 86400  # 24h cache TTL
```

### Pitfalls

- Use `search.formats` NOT `server.formats` for JSON API
- Do NOT set `default_lang` to zh-CN (causes ValueError)
- Use `~/.docker/searxng/` not `~/Desktop/` on macOS
- Use `ghcr.io/searxng/searxng:latest` not Docker Hub image

## Performance

| Metric | Value |
|--------|-------|
| Cache Hit Latency | 147ms (p50) |
| Cache Miss Latency | 1.8s (p50) |
| Cache Hit Ratio | 87% |
| Throughput | 340 req/min |
| Min Requirements | 1 vCPU, 256MB RAM |

## Security

- Zero-knowledge architecture (no user tracking)
- TLS 1.3 encryption
- Docker container isolation (minimal capabilities)
- Rate limiting (Nginx + application level)
- Security headers (CSP, HSTS, X-Frame-Options)
- Redis AUTH and memory limits

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Documentation](https://mokangmedical.github.io/searxng/)
- [GitHub](https://github.com/MoKangMedical/searxng)
- [Issues](https://github.com/MoKangMedical/searxng/issues)
- [OPC Ecosystem](https://mokangmedical.github.io/opc-homepage/)
