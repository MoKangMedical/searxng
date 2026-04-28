#!/bin/bash
# SearXNG 项目状态检查脚本
# 用法: ./scripts/status.sh

echo "=========================================="
echo "  SearXNG 项目状态"
echo "=========================================="

# 检查Docker状态
echo ""
echo "=== Docker状态 ==="
if docker info &>/dev/null; then
    echo "✓ Docker服务运行中"
else
    echo "✗ Docker服务未运行"
fi

# 检查容器状态
echo ""
echo "=== 容器状态 ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null | grep -E "(searxng|NAMES)" || echo "无SearXNG容器运行"

# 检查服务状态
echo ""
echo "=== 服务状态 ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Web界面正常 (HTTP $HTTP_CODE)"
else
    echo "✗ Web界面异常 (HTTP $HTTP_CODE)"
fi

# 检查Redis状态
echo ""
echo "=== Redis状态 ==="
REDIS_RESULT=$(docker exec searxng-redis redis-cli ping 2>/dev/null || echo "FAIL")
if [ "$REDIS_RESULT" = "PONG" ]; then
    echo "✓ Redis连接正常"
else
    echo "✗ Redis连接异常"
fi

# 检查搜索功能
echo ""
echo "=== 搜索功能 ==="
RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" 2>/dev/null | grep -c "result" || echo "0")
if [ "$RESULT_COUNT" -gt 0 ]; then
    echo "✓ 搜索功能正常 (结果数: $RESULT_COUNT)"
else
    echo "✗ 搜索功能异常"
fi

# 检查项目文件
echo ""
echo "=== 项目文件 ==="
for file in "manage.sh" "README.md" ".gitignore" "docker-compose.yml"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file"
    fi
done

# 检查目录
for dir in "scripts" "api" "examples" "templates"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir/"
    else
        echo "✗ $dir/"
    fi
done

# 检查Git状态
echo ""
echo "=== Git状态 ==="
if [ -d ".git" ]; then
    echo "✓ Git仓库已初始化"
    echo "  分支: $(git branch --show-current)"
    echo "  提交: $(git log --oneline -1)"
else
    echo "✗ Git仓库未初始化"
fi

echo ""
echo "=========================================="
echo "  状态检查完成"
echo "=========================================="
