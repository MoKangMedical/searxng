#!/usr/bin/env python3
"""
SearXNG Python 集成示例
演示如何在Python项目中使用SearXNG
"""

import sys
import os

# 添加API目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from searxng_api import SearXNGClient


def example_basic_search():
    """基础搜索示例"""
    print("=== 基础搜索示例 ===")
    
    client = SearXNGClient()
    
    # 检查服务状态
    if not client.health_check():
        print("SearXNG服务不可用，请先启动服务")
        return
    
    # 百度搜索
    results = client.search_baidu("医疗AI")
    print(f"百度搜索结果数: {len(results.get('results', []))}")
    
    # 搜狗搜索
    results = client.search_sogou("医疗AI")
    print(f"搜狗搜索结果数: {len(results.get('results', []))}")
    
    # 360搜索
    results = client.search_360("医疗AI")
    print(f"360搜索结果数: {len(results.get('results', []))}")


def example_academic_search():
    """学术搜索示例"""
    print("\n=== 学术搜索示例 ===")
    
    client = SearXNGClient()
    
    # 学术搜索
    results = client.search_academic("artificial intelligence healthcare")
    print(f"学术搜索结果数: {len(results.get('results', []))}")
    
    # 显示前3个结果
    for i, result in enumerate(results.get('results', [])[:3], 1):
        print(f"\n{i}. {result.get('title')}")
        print(f"   链接: {result.get('url')}")
        print(f"   来源: {result.get('engine', 'unknown')}")


def example_wechat_search():
    """微信搜索示例"""
    print("\n=== 微信搜索示例 ===")
    
    client = SearXNGClient()
    
    # 微信搜索
    results = client.search_wechat("医疗AI")
    print(f"微信搜索结果数: {len(results.get('results', []))}")
    
    # 显示前3个结果
    for i, result in enumerate(results.get('results', [])[:3], 1):
        print(f"\n{i}. {result.get('title')}")
        print(f"   链接: {result.get('url')}")
        print(f"   来源: {result.get('engine', 'unknown')}")


def example_dev_search():
    """开发者搜索示例"""
    print("\n=== 开发者搜索示例 ===")
    
    client = SearXNGClient()
    
    # 开发者搜索
    results = client.search_dev("machine learning")
    print(f"开发者搜索结果数: {len(results.get('results', []))}")
    
    # 显示前3个结果
    for i, result in enumerate(results.get('results', [])[:3], 1):
        print(f"\n{i}. {result.get('title')}")
        print(f"   链接: {result.get('url')}")
        print(f"   来源: {result.get('engine', 'unknown')}")


def example_custom_search():
    """自定义搜索示例"""
    print("\n=== 自定义搜索示例 ===")
    
    client = SearXNGClient()
    
    # 使用多个引擎搜索
    results = client.search(
        "医疗AI",
        engines=["baidu", "sogou", "google_scholar"],
        language="zh-CN",
        page=1
    )
    
    print(f"自定义搜索结果数: {len(results.get('results', []))}")
    
    # 按引擎分组显示
    engines = {}
    for result in results.get('results', []):
        engine = result.get('engine', 'unknown')
        if engine not in engines:
            engines[engine] = []
        engines[engine].append(result)
    
    for engine, engine_results in engines.items():
        print(f"\n{engine}: {len(engine_results)} 个结果")
        for result in engine_results[:2]:
            print(f"  - {result.get('title')}")


def main():
    """主函数"""
    print("SearXNG Python 集成示例")
    print("=" * 50)
    
    try:
        example_basic_search()
        example_academic_search()
        example_wechat_search()
        example_dev_search()
        example_custom_search()
        
        print("\n" + "=" * 50)
        print("所有示例执行完成！")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
