#!/bin/bash
# SearXNG 安装脚本
# 用法: ./install.sh

set -e

echo "=========================================="
echo "  SearXNG 安装脚本"
echo "=========================================="

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "错误: 未安装Docker"
    echo "请先安装Docker Desktop for Mac"
    echo "下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "错误: Docker服务未启动"
    echo "请启动Docker Desktop"
    exit 1
fi

echo "✓ Docker已安装并运行"

# 创建必要的目录
echo "创建目录结构..."
mkdir -p config logs backups templates scripts api examples docs nginx/ssl

# 复制配置文件
echo "复制配置文件..."
if [ ! -f config/settings.yml ]; then
    cp templates/settings.dev.yml config/settings.yml
    echo "  创建开发环境配置"
fi

# 设置执行权限
echo "设置执行权限..."
chmod +x manage.sh
chmod +x scripts/*.sh
chmod +x api/*.py
chmod +x examples/*.py

# 创建环境变量文件
if [ ! -f .env ]; then
    echo "创建环境变量文件..."
    cp .env.example .env
    echo "  请编辑 .env 文件设置密钥"
fi

# 启动服务
echo "启动服务..."
docker compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/ | grep -q "200"; then
    echo "✓ 服务启动成功"
    echo "  访问地址: http://localhost:8888"
else
    echo "✗ 服务启动失败"
    echo "  查看日志: docker logs searxng"
    exit 1
fi

# 测试搜索功能
echo "测试搜索功能..."
RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" | grep -c "result" || echo "0")
if [ "$RESULT_COUNT" -gt 0 ]; then
    echo "✓ 搜索功能正常 (结果数: $RESULT_COUNT)"
else
    echo "✗ 搜索功能异常"
fi

echo ""
echo "=========================================="
echo "  安装完成！"
echo ""
echo "  管理命令:"
echo "    ./manage.sh start    启动服务"
echo "    ./manage.sh stop     停止服务"
echo "    ./manage.sh status   查看状态"
echo "    ./manage.sh test     测试服务"
echo ""
echo "  快捷搜索:"
echo "    !bd 关键词  百度搜索"
echo "    !sg 关键词  搜狗搜索"
echo "    !360 关键词 360搜索"
echo "    !sgw 关键词 微信搜索"
echo ""
echo "  API接口:"
echo "    Python: from api.searxng_api import SearXNGClient"
echo "    JavaScript: const client = new SearXNGClient()"
echo "=========================================="
