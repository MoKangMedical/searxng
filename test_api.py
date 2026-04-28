#!/usr/bin/env python3
"""
SearXNG API 测试脚本
"""

import sys
import os

# 添加API目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from searxng_api import SearXNGClient


def test_health_check():
    """测试健康检查"""
    client = SearXNGClient()
    assert client.health_check() == True, "健康检查失败"
    print("✓ 健康检查通过")


def test_search_baidu():
    """测试百度搜索"""
    client = SearXNGClient()
    results = client.search_baidu("test")
    assert len(results.get('results', [])) > 0, "百度搜索无结果"
    print(f"✓ 百度搜索通过 (结果数: {len(results.get('results', []))})")


def test_search_sogou():
    """测试搜狗搜索"""
    client = SearXNGClient()
    results = client.search_sogou("test")
    assert len(results.get('results', [])) > 0, "搜狗搜索无结果"
    print(f"✓ 搜狗搜索通过 (结果数: {len(results.get('results', []))})")


def test_search_360():
    """测试360搜索"""
    client = SearXNGClient()
    results = client.search_360("test")
    assert len(results.get('results', [])) > 0, "360搜索无结果"
    print(f"✓ 360搜索通过 (结果数: {len(results.get('results', []))})")


def test_search_academic():
    """测试学术搜索"""
    client = SearXNGClient()
    results = client.search_academic("artificial intelligence")
    assert len(results.get('results', [])) > 0, "学术搜索无结果"
    print(f"✓ 学术搜索通过 (结果数: {len(results.get('results', []))})")


def test_search_wechat():
    """测试微信搜索"""
    client = SearXNGClient()
    results = client.search_wechat("test")
    assert len(results.get('results', [])) > 0, "微信搜索无结果"
    print(f"✓ 微信搜索通过 (结果数: {len(results.get('results', []))})")


def main():
    """主测试函数"""
    print("=== SearXNG API 测试 ===")
    
    try:
        test_health_check()
        test_search_baidu()
        test_search_sogou()
        test_search_360()
        test_search_academic()
        test_search_wechat()
        
        print("\n=== 所有测试通过 ===")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
