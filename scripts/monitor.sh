#!/bin/bash
# SearXNG 监控脚本
# 用法: ./scripts/monitor.sh [间隔秒数]
# 功能: 健康检查、性能监控、日志记录

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

INTERVAL="${1:-60}"
LOG_FILE="$PROJECT_DIR/logs/monitor.log"
ALERT_FILE="$PROJECT_DIR/logs/alerts.log"

mkdir -p "$PROJECT_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $1" | tee -a "$ALERT_FILE" | tee -a "$LOG_FILE"
}

check_service() {
    local service_name="$1"
    local url="$2"
    local timeout=10
    
    if curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" | grep -q "200"; then
        return 0
    else
        return 1
    fi
}

check_redis() {
    if docker exec searxng-redis redis-cli ping | grep -q "PONG"; then
        return 0
    else
        return 1
    fi
}

get_stats() {
    local port="${1:-8888}"
    
    # 获取响应时间
    local response_time=$(curl -s -o /dev/null -w "%{time_total}" --max-time 10 "http://localhost:$port/")
    
    # 获取搜索结果数
    local result_count=$(curl -s --max-time 10 "http://localhost:$port/search?q=test" | grep -c "result" || echo "0")
    
    # 获取Redis内存使用
    local redis_memory=$(docker exec searxng-redis redis-cli info memory 2>/dev/null | grep "used_memory_human" | cut -d: -f2 | tr -d '\r' || echo "N/A")
    
    echo "$response_time,$result_count,$redis_memory"
}

main() {
    log "开始监控 SearXNG..."
    log "监控间隔: ${INTERVAL}秒"
    
    while true; do
        # 检查SearXNG服务
        if ! check_service "searxng" "http://localhost:8888/"; then
            alert "SearXNG服务不可用"
            # 尝试重启
            log "尝试重启服务..."
            cd "$PROJECT_DIR" && docker compose restart searxng
            sleep 10
            if check_service "searxng" "http://localhost:8888/"; then
                log "服务重启成功"
            else
                alert "服务重启失败，需要人工干预"
            fi
        fi
        
        # 检查Redis服务
        if ! check_redis; then
            alert "Redis服务不可用"
            log "尝试重启Redis..."
            cd "$PROJECT_DIR" && docker compose restart redis
            sleep 5
            if check_redis; then
                log "Redis重启成功"
            else
                alert "Redis重启失败，需要人工干预"
            fi
        fi
        
        # 获取统计数据
        stats=$(get_stats 8888)
        response_time=$(echo "$stats" | cut -d, -f1)
        result_count=$(echo "$stats" | cut -d, -f2)
        redis_memory=$(echo "$stats" | cut -d, -f3)
        
        log "状态: 正常 | 响应时间: ${response_time}s | 结果数: $result_count | Redis内存: $redis_memory"
        
        # 检查响应时间是否过长
        if (( $(echo "$response_time > 5.0" | bc -l 2>/dev/null || echo 0) )); then
            alert "响应时间过长: ${response_time}s"
        fi
        
        sleep "$INTERVAL"
    done
}

# 显示帮助
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "SearXNG 监控脚本"
    echo ""
    echo "用法: $0 [间隔秒数]"
    echo ""
    echo "参数:"
    echo "  间隔秒数  监控检查间隔（默认60秒）"
    echo ""
    echo "功能:"
    echo "  - 服务健康检查"
    echo "  - 自动重启失败的服务"
    echo "  - 性能监控（响应时间、结果数、内存使用）"
    echo "  - 日志记录和告警"
    echo ""
    echo "日志文件:"
    echo "  $LOG_FILE"
    echo "  $ALERT_FILE"
    exit 0
fi

main
