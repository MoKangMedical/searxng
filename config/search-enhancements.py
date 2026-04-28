#!/usr/bin/env python3
"""
SearXNG 搜索增强模块
功能: 搜索建议、自动补全、高级搜索语法
"""

import json
import re
from typing import List, Dict, Any

class SearchEnhancer:
    """搜索增强器"""
    
    # 医疗AI常用搜索词
    MEDICAL_TERMS = [
        "医疗AI", "人工智能医疗", "AI诊断", "医疗大数据",
        "药物研发", "临床试验", "基因组学", "精准医疗",
        "医学影像", "病理分析", "健康管理", "远程医疗",
        "医疗机器人", "智能问诊", "电子病历", "医疗知识图谱"
    ]
    
    # 常用搜索引擎快捷键
    ENGINE_SHORTCUTS = {
        "!bd": "百度搜索",
        "!sg": "搜狗搜索",
        "!360": "360搜索",
        "!go": "Google搜索",
        "!ddg": "DuckDuckGo搜索",
        "!bi": "Bing搜索",
        "!br": "Brave搜索",
        "!gs": "Google Scholar学术搜索",
        "!arx": "arXiv学术搜索",
        "!sgw": "搜狗微信搜索",
        "!gh": "GitHub代码搜索",
        "!st": "StackOverflow技术问答",
        "!hf": "HuggingFace AI模型搜索",
        "!bdi": "百度图片搜索",
        "!sgi": "搜狗图片搜索",
        "!gis": "Google图片搜索",
        "!360v": "360视频搜索",
        "!sgv": "搜狗视频搜索",
        "!yt": "YouTube视频搜索"
    }
    
    # 高级搜索语法
    ADVANCED_SYNTAX = {
        "site:": "搜索特定网站 (例: site:github.com)",
        "filetype:": "搜索特定文件类型 (例: filetype:pdf)",
        "intitle:": "搜索标题中包含的关键词 (例: intitle:医疗AI)",
        "inurl:": "搜索URL中包含的关键词 (例: inurl:medical)",
        "intext:": "搜索正文中包含的关键词 (例: intext:人工智能)",
        "related:": "搜索相关网站 (例: related:github.com)",
        "cache:": "查看网页缓存 (例: cache:github.com)",
        "define:": "查询定义 (例: define:人工智能)"
    }
    
    @staticmethod
    def get_suggestions(query: str) -> List[str]:
        """获取搜索建议"""
        suggestions = []
        
        # 匹配医疗AI术语
        for term in SearchEnhancer.MEDICAL_TERMS:
            if query.lower() in term.lower():
                suggestions.append(term)
        
        # 匹配搜索引擎快捷键
        for shortcut, desc in SearchEnhancer.ENGINE_SHORTCUTS.items():
            if query.lower() in shortcut.lower() or query.lower() in desc.lower():
                suggestions.append(f"{shortcut} - {desc}")
        
        return suggestions[:10]  # 最多返回10个建议
    
    @staticmethod
    def parse_advanced_query(query: str) -> Dict[str, Any]:
        """解析高级搜索查询"""
        result = {
            "original": query,
            "clean_query": query,
            "filters": {}
        }
        
        # 解析 site: 过滤器
        site_match = re.search(r'site:(\S+)', query)
        if site_match:
            result["filters"]["site"] = site_match.group(1)
            result["clean_query"] = query.replace(site_match.group(0), "").strip()
        
        # 解析 filetype: 过滤器
        filetype_match = re.search(r'filetype:(\w+)', query)
        if filetype_match:
            result["filters"]["filetype"] = filetype_match.group(1)
            result["clean_query"] = result["clean_query"].replace(filetype_match.group(0), "").strip()
        
        # 解析 intitle: 过滤器
        intitle_match = re.search(r'intitle:(\S+)', query)
        if intitle_match:
            result["filters"]["intitle"] = intitle_match.group(1)
            result["clean_query"] = result["clean_query"].replace(intitle_match.group(0), "").strip()
        
        # 解析时间范围过滤器
        time_match = re.search(r'after:(\d{4})', query)
        if time_match:
            result["filters"]["after_year"] = int(time_match.group(1))
            result["clean_query"] = result["clean_query"].replace(time_match.group(0), "").strip()
        
        time_match = re.search(r'before:(\d{4})', query)
        if time_match:
            result["filters"]["before_year"] = int(time_match.group(1))
            result["clean_query"] = result["clean_query"].replace(time_match.group(0), "").strip()
        
        return result
    
    @staticmethod
    def get_search_help() -> str:
        """获取搜索帮助信息"""
        help_text = """
# SearXNG 搜索帮助

## 基础搜索
直接输入关键词进行搜索

## 搜索引擎快捷键
"""
        for shortcut, desc in SearchEnhancer.ENGINE_SHORTCUTS.items():
            help_text += f"- `{shortcut}` - {desc}\n"
        
        help_text += """
## 高级搜索语法
"""
        for syntax, desc in SearchEnhancer.ADVANCED_SYNTAX.items():
            help_text += f"- `{syntax}` - {desc}\n"
        
        help_text += """
## 示例
- `医疗AI !gs` - 使用Google Scholar搜索医疗AI
- `site:github.com 机器学习` - 在GitHub上搜索机器学习
- `filetype:pdf 深度学习` - 搜索PDF格式的深度学习文档
- `intitle:医疗 人工智能` - 搜索标题中包含"医疗"且包含"人工智能"的页面
"""
        return help_text


def main():
    """测试函数"""
    enhancer = SearchEnhancer()
    
    # 测试搜索建议
    print("=== 搜索建议测试 ===")
    suggestions = enhancer.get_suggestions("医疗")
    for s in suggestions:
        print(f"  - {s}")
    
    # 测试高级查询解析
    print("\n=== 高级查询解析测试 ===")
    test_queries = [
        "site:github.com 机器学习",
        "filetype:pdf 深度学习",
        "intitle:医疗 人工智能",
        "after:2020 新冠疫苗"
    ]
    
    for query in test_queries:
        result = enhancer.parse_advanced_query(query)
        print(f"\n查询: {query}")
        print(f"  清理后: {result['clean_query']}")
        print(f"  过滤器: {result['filters']}")
    
    # 打印搜索帮助
    print("\n=== 搜索帮助 ===")
    print(enhancer.get_search_help())


if __name__ == "__main__":
    main()
