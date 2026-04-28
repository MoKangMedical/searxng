#!/bin/bash
# SearXNG 生产环境部署脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  SearXNG 生产环境部署"
echo "=========================================="

# 检查环境变量
if [ -z "$SEARXNG_SECRET" ]; then
    echo -e "${YELLOW}警告: 未设置SEARXNG_SECRET，将生成随机密钥${NC}"
    export SEARXNG_SECRET=$(openssl rand -hex 32)
fi

if [ -z "$REDIS_PASSWORD" ]; then
    echo -e "${YELLOW}警告: 未设置REDIS_PASSWORD，将生成随机密码${NC}"
    export REDIS_PASSWORD=$(openssl rand -hex 16)
fi

# 创建必要目录
echo "创建目录结构..."
mkdir -p "$SCRIPT_DIR/config"
mkdir -p "$SCRIPT_DIR/nginx/ssl"
mkdir -p "$SCRIPT_DIR/logs"

# 复制配置文件
echo "复制配置文件..."
cp "$PROJECT_DIR/config/settings.yml" "$SCRIPT_DIR/config/"
cp "$PROJECT_DIR/config/limiter.toml" "$SCRIPT_DIR/config/"

# 生成环境变量文件
echo "生成环境变量文件..."
cat > "$SCRIPT_DIR/.env" << EOF2
SEARXNG_SECRET=$SEARXNG_SECRET
REDIS_PASSWORD=$REDIS_PASSWORD
SEARXNG_BASE_URL=http://localhost:8080
GRAFANA_PASSWORD=admin
EOF2

# 启动服务
echo "启动服务..."
cd "$SCRIPT_DIR"
docker-compose -f docker-compose.prod.yml up -d

# 等待服务启动
echo "等待服务启动..."
sleep 30

# 检查服务状态
echo "检查服务状态..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ | grep -q "200"; then
    echo -e "${GREEN}✓ 部署成功${NC}"
    echo ""
    echo "访问地址:"
    echo "  - HTTP: http://localhost:8080"
    echo ""
    echo "管理地址:"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3000"
else
    echo -e "${RED}✗ 部署失败${NC}"
    echo "查看日志: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi
