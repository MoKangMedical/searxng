#!/bin/bash
# SearXNG 配置验证脚本
# 用法: ./scripts/validate-config.sh

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  SearXNG 配置验证"
echo "=========================================="

ERRORS=0
WARNINGS=0

# 检查配置文件
echo ""
echo "=== 配置文件检查 ==="

# settings.yml
if [ -f "config/settings.yml" ]; then
    echo -e "${GREEN}✓${NC} config/settings.yml 存在"
    
    # 检查YAML语法
    if python3 -c "import yaml; yaml.safe_load(open('config/settings.yml'))" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} YAML语法正确"
    else
        echo -e "${RED}✗${NC} YAML语法错误"
        ((ERRORS++))
    fi
    
    # 检查必要配置
    if grep -q "search:" config/settings.yml; then
        echo -e "${GREEN}✓${NC} search配置存在"
    else
        echo -e "${RED}✗${NC} search配置缺失"
        ((ERRORS++))
    fi
    
    if grep -q "formats:" config/settings.yml; then
        echo -e "${GREEN}✓${NC} formats配置存在"
    else
        echo -e "${YELLOW}⚠${NC} formats配置缺失 (JSON API可能不可用)"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗${NC} config/settings.yml 不存在"
    ((ERRORS++))
fi

# limiter.toml
if [ -f "config/limiter.toml" ]; then
    echo -e "${GREEN}✓${NC} config/limiter.toml 存在"
else
    echo -e "${YELLOW}⚠${NC} config/limiter.toml 不存在 (将使用默认配置)"
    ((WARNINGS++))
fi

# custom.css
if [ -f "config/custom.css" ]; then
    echo -e "${GREEN}✓${NC} config/custom.css 存在"
else
    echo -e "${YELLOW}⚠${NC} config/custom.css 不存在 (将使用默认样式)"
    ((WARNINGS++))
fi

# custom.js
if [ -f "config/custom.js" ]; then
    echo -e "${GREEN}✓${NC} config/custom.js 存在"
else
    echo -e "${YELLOW}⚠${NC} config/custom.js 不存在 (高级功能不可用)"
    ((WARNINGS++))
fi

# docker-compose.yml
echo ""
echo "=== Docker配置检查 ==="

if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✓${NC} docker-compose.yml 存在"
    
    # 检查YAML语法
    if python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} YAML语法正确"
    else
        echo -e "${RED}✗${NC} YAML语法错误"
        ((ERRORS++))
    fi
    
    # 检查服务配置
    if grep -q "searxng:" docker-compose.yml; then
        echo -e "${GREEN}✓${NC} searxng服务配置存在"
    else
        echo -e "${RED}✗${NC} searxng服务配置缺失"
        ((ERRORS++))
    fi
    
    if grep -q "redis:" docker-compose.yml; then
        echo -e "${GREEN}✓${NC} redis服务配置存在"
    else
        echo -e "${RED}✗${NC} redis服务配置缺失"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} docker-compose.yml 不存在"
    ((ERRORS++))
fi

# 检查脚本权限
echo ""
echo "=== 脚本权限检查 ==="

for script in manage.sh install.sh scripts/*.sh; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo -e "${GREEN}✓${NC} $script: 可执行"
        else
            echo -e "${YELLOW}⚠${NC} $script: 不可执行"
            ((WARNINGS++))
        fi
    fi
done

# 检查端口占用
echo ""
echo "=== 端口检查 ==="

if lsof -i :8888 >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 端口8888: 已占用 (服务运行中)"
else
    echo -e "${YELLOW}⚠${NC} 端口8888: 未占用 (服务未运行)"
    ((WARNINGS++))
fi

# 总结
echo ""
echo "=========================================="
echo "错误: $ERRORS"
echo "警告: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 配置验证通过${NC}"
    exit 0
else
    echo -e "${RED}✗ 配置验证失败${NC}"
    exit 1
fi
