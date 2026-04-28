#!/bin/bash
# SearXNG 一键部署脚本
# 用法: ./scripts/deploy.sh [环境] [端口]
# 环境: dev (默认), prod
# 端口: 8888 (默认)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 默认参数
ENV="${1:-dev}"
PORT="${2:-8888}"

echo "=========================================="
echo "  SearXNG 部署脚本"
echo "  环境: $ENV"
echo "  端口: $PORT"
echo "=========================================="

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "错误: 未安装Docker"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "错误: Docker服务未启动"
    exit 1
fi

# 创建配置目录
mkdir -p "$PROJECT_DIR/config"

# 根据环境选择配置
if [ "$ENV" = "prod" ]; then
    echo "生产环境配置..."
    cp "$PROJECT_DIR/templates/settings.prod.yml" "$PROJECT_DIR/config/settings.yml"
else
    echo "开发环境配置..."
    cp "$PROJECT_DIR/templates/settings.dev.yml" "$PROJECT_DIR/config/settings.yml"
fi

# 更新端口
sed -i '' "s/ports:/ports:\n      - \"$PORT:8080\"/" "$PROJECT_DIR/docker-compose.yml"

# 启动服务
echo "启动服务..."
cd "$PROJECT_DIR"
docker compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/" | grep -q "200"; then
    echo "✓ 服务启动成功"
    echo "  访问地址: http://localhost:$PORT"
else
    echo "✗ 服务启动失败"
    echo "  查看日志: docker logs searxng"
    exit 1
fi

# 测试搜索功能
echo "测试搜索功能..."
RESULT_COUNT=$(curl -s "http://localhost:$PORT/search?q=test" | grep -c "result" || echo "0")
if [ "$RESULT_COUNT" -gt 0 ]; then
    echo "✓ 搜索功能正常 (结果数: $RESULT_COUNT)"
else
    echo "✗ 搜索功能异常"
fi

echo "=========================================="
echo "  部署完成！"
echo "  管理命令: ./manage.sh {start|stop|restart|status}"
echo "=========================================="
