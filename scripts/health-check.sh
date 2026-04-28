#!/bin/bash
# SearXNG 健康检查脚本
# 用法: ./scripts/health-check.sh

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查函数
check_service() {
    local name="$1"
    local url="$2"
    local timeout=10
    
    if curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" | grep -q "200"; then
        echo -e "${GREEN}✓${NC} $name: 正常"
        return 0
    else
        echo -e "${RED}✗${NC} $name: 异常"
        return 1
    fi
}

check_docker() {
    local name="$1"
    
    if docker ps | grep -q "$name"; then
        echo -e "${GREEN}✓${NC} $name: 运行中"
        return 0
    else
        echo -e "${RED}✗${NC} $name: 未运行"
        return 1
    fi
}

check_redis() {
    if docker exec searxng-redis redis-cli ping | grep -q "PONG"; then
        echo -e "${GREEN}✓${NC} Redis: 正常"
        return 0
    else
        echo -e "${RED}✗${NC} Redis: 异常"
        return 1
    fi
}

# 主检查流程
echo "=========================================="
echo "  SearXNG 健康检查"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

ERRORS=0

# 检查Docker
echo ""
echo "=== Docker状态 ==="
check_docker "searxng" || ((ERRORS++))
check_docker "searxng-redis" || ((ERRORS++))

# 检查服务
echo ""
echo "=== 服务状态 ==="
check_service "Web界面" "http://localhost:8888/" || ((ERRORS++))
check_redis || ((ERRORS++))

# 检查搜索功能
echo ""
echo "=== 功能测试 ==="
RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" | grep -c "result" || echo "0")
if [ "$RESULT_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} 搜索功能: 正常 (结果数: $RESULT_COUNT)"
else
    echo -e "${RED}✗${NC} 搜索功能: 异常"
    ((ERRORS++))
fi

# 检查JSON API
JSON_RESULT=$(curl -s "http://localhost:8888/search?q=test&format=json" | grep -c "results" || echo "0")
if [ "$JSON_RESULT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} JSON API: 正常"
else
    echo -e "${RED}✗${NC} JSON API: 异常"
    ((ERRORS++))
fi

# 检查响应时间
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8888/)
if (( $(echo "$RESPONSE_TIME < 2.0" | bc -l) )); then
    echo -e "${GREEN}✓${NC} 响应时间: ${RESPONSE_TIME}s"
else
    echo -e "${YELLOW}⚠${NC} 响应时间: ${RESPONSE_TIME}s (较慢)"
fi

# 检查资源使用
echo ""
echo "=== 资源使用 ==="
DOCKER_STATS=$(docker stats --no-trunc --format "{{.Container}}: CPU={{.CPUPerc}} MEM={{.MemUsage}}" | grep searxng)
echo "$DOCKER_STATS"

# 总结
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 所有检查通过${NC}"
    exit 0
else
    echo -e "${RED}✗ 发现 $ERRORS 个问题${NC}"
    exit 1
fi
