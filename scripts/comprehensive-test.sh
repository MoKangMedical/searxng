#!/bin/bash
# SearXNG 全面测试脚本
# 用法: ./scripts/comprehensive-test.sh

echo "=========================================="
echo "  SearXNG 全面功能测试"
echo "=========================================="

# 测试计数器
PASS=0
FAIL=0

test_case() {
    local name="$1"
    local result="$2"
    
    if [ "$result" = "0" ]; then
        echo "✓ $name"
        PASS=$((PASS + 1))
    else
        echo "✗ $name"
        FAIL=$((FAIL + 1))
    fi
}

# 1. Docker状态检查
echo ""
echo "=== Docker状态检查 ==="
docker info &>/dev/null
test_case "Docker服务运行" "$?"

# 2. 容器状态检查
echo ""
echo "=== 容器状态检查 ==="
docker ps | grep -q "searxng"
test_case "SearXNG容器运行" "$?"

docker ps | grep -q "searxng-redis"
test_case "Redis容器运行" "$?"

# 3. 服务健康检查
echo ""
echo "=== 服务健康检查 ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/)
[ "$HTTP_CODE" = "200" ]
test_case "Web界面可访问" "$?"

REDIS_RESULT=$(docker exec searxng-redis redis-cli ping 2>/dev/null)
[ "$REDIS_RESULT" = "PONG" ]
test_case "Redis连接正常" "$?"

# 4. 搜索功能测试
echo ""
echo "=== 搜索功能测试 ==="
RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" | grep -c "result")
[ "$RESULT_COUNT" -gt 0 ]
test_case "通用搜索功能" "$?"

RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=!gs+artificial+intelligence" | grep -c "result")
[ "$RESULT_COUNT" -gt 0 ]
test_case "学术搜索功能" "$?"

RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=!sgw+医疗AI" | grep -c "result")
[ "$RESULT_COUNT" -gt 0 ]
test_case "微信搜索功能" "$?"

# 5. JSON API测试
echo ""
echo "=== JSON API测试 ==="
JSON_RESULT=$(curl -s "http://localhost:8888/search?q=test&format=json" | grep -c "results")
[ "$JSON_RESULT" -gt 0 ]
test_case "JSON API功能" "$?"

# 6. 响应时间测试
echo ""
echo "=== 响应时间测试 ==="
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8888/)
echo "   响应时间: ${RESPONSE_TIME}s"
if (( $(echo "$RESPONSE_TIME < 2.0" | bc -l) )); then
    test_case "响应时间 < 2秒" "0"
else
    test_case "响应时间 < 2秒" "1"
fi

# 7. 项目文件检查
echo ""
echo "=== 项目文件检查 ==="
for file in "manage.sh" "README.md" ".gitignore" "docker-compose.yml" "install.sh" "Dockerfile" "docker-compose.prod.yml" ".env.example" "QUICKSTART.md" "PROJECT_STATUS.md" "CHANGELOG.md"; do
    [ -f "$file" ]
    test_case "$file 存在" "$?"
done

# 8. 目录检查
echo ""
echo "=== 目录检查 ==="
for dir in "scripts" "api" "examples" "templates" "nginx" "config" "docs"; do
    [ -d "$dir" ]
    test_case "$dir/ 目录存在" "$?"
done

# 9. 脚本权限检查
echo ""
echo "=== 脚本权限检查 ==="
for file in "manage.sh" "install.sh" "scripts/status.sh" "scripts/full-test.sh" "scripts/comprehensive-test.sh" "api/searxng_api.py" "examples/medical_ai_integration.py"; do
    [ -x "$file" ]
    test_case "$file 可执行" "$?"
done

# 10. 配置文件检查
echo ""
echo "=== 配置文件检查 ==="
[ -f "config/settings.yml" ]
test_case "config/settings.yml 存在" "$?"

[ -f "config/limiter.toml" ]
test_case "config/limiter.toml 存在" "$?"

[ -f "config/custom.css" ]
test_case "config/custom.css 存在" "$?"

[ -f "config/custom_header.html" ]
test_case "config/custom_header.html 存在" "$?"

# 11. API客户端检查
echo ""
echo "=== API客户端检查 ==="
[ -f "api/searxng_api.py" ]
test_case "Python API客户端存在" "$?"

[ -f "api/searxng.js" ]
test_case "JavaScript API客户端存在" "$?"

# 12. 示例文件检查
echo ""
echo "=== 示例文件检查 ==="
[ -f "examples/python_example.py" ]
test_case "Python示例存在" "$?"

[ -f "examples/nodejs_example.js" ]
test_case "Node.js示例存在" "$?"

[ -f "examples/medical_ai_integration.py" ]
test_case "医疗AI集成示例存在" "$?"

# 13. Git状态检查
echo ""
echo "=== Git状态检查 ==="
[ -d ".git" ]
test_case "Git仓库已初始化" "$?"

# 输出测试结果
echo ""
echo "=========================================="
echo "  测试结果"
echo "  通过: $PASS"
echo "  失败: $FAIL"
echo "  总计: $((PASS + FAIL))"
echo "=========================================="

if [ "$FAIL" -gt 0 ]; then
    echo "  存在失败的测试项，请检查！"
    exit 1
else
    echo "  所有测试通过！"
    exit 0
fi
