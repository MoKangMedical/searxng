#!/bin/bash
# SearXNG 备份脚本
# 用法: ./scripts/backup.sh [备份目录]
# 功能: 备份配置、数据、日志

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

BACKUP_DIR="${1:-$PROJECT_DIR/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="searxng_backup_$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo "=========================================="
echo "  SearXNG 备份脚本"
echo "  备份目录: $BACKUP_PATH"
echo "=========================================="

# 创建备份目录
mkdir -p "$BACKUP_PATH"

# 备份配置文件
echo "备份配置文件..."
cp -r "$PROJECT_DIR/config" "$BACKUP_PATH/"

# 备份docker-compose.yml
cp "$PROJECT_DIR/docker-compose.yml" "$BACKUP_PATH/"

# 备份管理脚本
cp "$PROJECT_DIR/manage.sh" "$BACKUP_PATH/"

# 备份Redis数据（如果存在）
if docker ps | grep -q searxng-redis; then
    echo "备份Redis数据..."
    docker exec searxng-redis redis-cli BGSAVE
    sleep 2
    docker cp searxng-redis:/data/dump.rdb "$BACKUP_PATH/redis_dump.rdb" 2>/dev/null || echo "Redis数据备份跳过"
fi

# 备份日志（如果存在）
if [ -d "$PROJECT_DIR/logs" ]; then
    echo "备份日志..."
    cp -r "$PROJECT_DIR/logs" "$BACKUP_PATH/"
fi

# 创建备份信息文件
cat > "$BACKUP_PATH/backup_info.txt" << INFOEOF
备份时间: $(date)
备份版本: 1.0
SearXNG状态: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/ || echo "不可用")
Redis状态: $(docker exec searxng-redis redis-cli ping 2>/dev/null || echo "不可用")
INFOEOF

# 压缩备份
echo "压缩备份..."
cd "$BACKUP_DIR"
tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"

# 清理旧备份（保留最近10个）
echo "清理旧备份..."
ls -t "$BACKUP_DIR"/searxng_backup_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm

echo "=========================================="
echo "  备份完成！"
echo "  备份文件: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo "=========================================="

# 显示备份列表
echo ""
echo "最近备份:"
ls -lh "$BACKUP_DIR"/searxng_backup_*.tar.gz 2>/dev/null | tail -5
