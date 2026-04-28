#!/bin/bash
# SearXNG 快速测试脚本
# 用法: ./scripts/quick-test.sh

echo "=== SearXNG 快速测试 ==="

# 检查服务状态
echo "1. 检查服务状态..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✓ Web界面正常 (HTTP $HTTP_CODE)"
else
    echo "   ✗ Web界面异常 (HTTP $HTTP_CODE)"
    exit 1
fi

# 检查Redis
echo "2. 检查Redis连接..."
REDIS_RESULT=$(docker exec searxng-redis redis-cli ping 2>/dev/null || echo "FAIL")
if [ "$REDIS_RESULT" = "PONG" ]; then
    echo "   ✓ Redis连接正常"
else
    echo "   ✗ Redis连接异常"
fi

# 测试搜索
echo "3. 测试搜索功能..."
RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" | grep -c "result" || echo "0")
if [ "$RESULT_COUNT" -gt 0 ]; then
    echo "   ✓ 搜索功能正常 (结果数: $RESULT_COUNT)"
else
    echo "   ✗ 搜索功能异常"
fi

# 测试响应时间
echo "4. 测试响应时间..."
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8888/)
echo "   响应时间: ${RESPONSE_TIME}s"

# 测试特定引擎
echo "5. 测试特定引擎..."
for engine in "bd" "sg" "360" "sgw"; do
    RESULT=$(curl -s "http://localhost:8888/search?q=!${engine}+test" | grep -c "result" || echo "0")
    if [ "$RESULT" -gt 0 ]; then
        echo "   ✓ !${engine} 引擎正常"
    else
        echo "   ✗ !${engine} 引擎异常"
    fi
done

echo ""
echo "=== 测试完成 ==="
