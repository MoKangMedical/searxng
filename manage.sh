#!/bin/bash
# SearXNG管理脚本 v2.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
    start)
        echo "启动SearXNG..."
        cd "$SCRIPT_DIR" && docker compose up -d
        echo "等待服务启动..."
        sleep 5
        echo "检查服务状态..."
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep searxng
        ;;
    stop)
        echo "停止SearXNG..."
        cd "$SCRIPT_DIR" && docker compose down
        ;;
    restart)
        echo "重启SearXNG..."
        cd "$SCRIPT_DIR" && docker compose restart
        echo "等待服务启动..."
        sleep 5
        echo "检查服务状态..."
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep searxng
        ;;
    status)
        echo "SearXNG状态:"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(searxng|NAMES)"
        echo ""
        echo "健康检查:"
        curl -s -o /dev/null -w "Web界面: %{http_code}\n" http://localhost:8888/
        ;;
    logs)
        echo "查看SearXNG日志:"
        docker logs searxng --tail 50
        ;;
    test)
        echo "测试SearXNG..."
        echo "1. Web界面状态:"
        curl -s -o /dev/null -w "   HTTP状态码: %{http_code}\n" http://localhost:8888/
        echo "2. 搜索功能测试:"
        RESULT_COUNT=$(curl -s "http://localhost:8888/search?q=test" | grep -c "result")
        echo "   搜索结果数: $RESULT_COUNT"
        echo "3. Redis连接测试:"
        docker exec searxng-redis redis-cli ping
        ;;
    update)
        echo "更新SearXNG配置..."
        cd "$SCRIPT_DIR" && docker compose down
        cd "$SCRIPT_DIR" && docker compose up -d
        echo "等待服务启动..."
        sleep 5
        echo "检查服务状态..."
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep searxng
        ;;
    backup)
        echo "备份SearXNG配置..."
        BACKUP_DIR="$SCRIPT_DIR/backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        cp -r "$SCRIPT_DIR/config" "$BACKUP_DIR/"
        cp "$SCRIPT_DIR/docker-compose.yml" "$BACKUP_DIR/"
        echo "备份完成: $BACKUP_DIR"
        ;;
    *)
        echo "SearXNG管理脚本 v2.0"
        echo "用法: $0 {start|stop|restart|status|logs|test|update|backup}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动SearXNG服务"
        echo "  stop    - 停止SearXNG服务"
        echo "  restart - 重启SearXNG服务"
        echo "  status  - 查看服务状态"
        echo "  logs    - 查看服务日志"
        echo "  test    - 测试服务是否正常"
        echo "  update  - 更新配置并重启服务"
        echo "  backup  - 备份当前配置"
        exit 1
        ;;
esac
