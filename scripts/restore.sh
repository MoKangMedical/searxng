#!/bin/bash
# SearXNG 恢复脚本
# 用法: ./scripts/restore.sh <备份文件>
# 功能: 从备份恢复配置和数据

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "错误: 请指定备份文件"
    echo "用法: $0 <备份文件>"
    echo ""
    echo "可用备份:"
    ls -lh "$PROJECT_DIR/backups"/searxng_backup_*.tar.gz 2>/dev/null || echo "  无备份文件"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件不存在: $BACKUP_FILE"
    exit 1
fi

echo "=========================================="
echo "  SearXNG 恢复脚本"
echo "  备份文件: $BACKUP_FILE"
echo "=========================================="

# 停止服务
echo "停止服务..."
cd "$PROJECT_DIR" && docker compose down

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "解压备份..."
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# 找到备份目录
BACKUP_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "searxng_backup_*" | head -1)

if [ -z "$BACKUP_DIR" ]; then
    echo "错误: 无效的备份文件"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 恢复配置
echo "恢复配置..."
if [ -d "$BACKUP_DIR/config" ]; then
    rm -rf "$PROJECT_DIR/config"
    cp -r "$BACKUP_DIR/config" "$PROJECT_DIR/"
fi

# 恢复docker-compose.yml
if [ -f "$BACKUP_DIR/docker-compose.yml" ]; then
    cp "$BACKUP_DIR/docker-compose.yml" "$PROJECT_DIR/"
fi

# 恢复Redis数据
if [ -f "$BACKUP_DIR/redis_dump.rdb" ]; then
    echo "恢复Redis数据..."
    # 启动Redis以便恢复数据
    cd "$PROJECT_DIR" && docker compose up -d redis
    sleep 5
    docker cp "$BACKUP_DIR/redis_dump.rdb" searxng-redis:/data/dump.rdb
    docker restart searxng-redis
fi

# 清理临时目录
rm -rf "$TEMP_DIR"

# 启动服务
echo "启动服务..."
cd "$PROJECT_DIR" && docker compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/ | grep -q "200"; then
    echo "✓ 服务恢复成功"
else
    echo "✗ 服务恢复失败"
    echo "  查看日志: docker logs searxng"
    exit 1
fi

echo "=========================================="
echo "  恢复完成！"
echo "=========================================="
