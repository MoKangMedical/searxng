#!/usr/bin/env python3
"""
SearXNG API 客户端
提供Python接口调用SearXNG搜索功能
支持JSON API和HTML解析两种模式
"""

import requests
import json
from typing import Optional, List, Dict, Any


class SearXNGClient:
    """SearXNG API 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        """
        初始化客户端
        
        Args:
            base_url: SearXNG服务地址
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearXNG-Python-Client/1.0'
        })
    
    def search(self, 
               query: str, 
               engines: Optional[List[str]] = None,
               language: str = "auto",
               page: int = 1,
               time_range: str = "",
               safe_search: int = 0,
               format: str = "json") -> Dict[str, Any]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            engines: 搜索引擎列表，如 ["baidu", "sogou"]
            language: 搜索语言，默认自动检测
            page: 页码
            time_range: 时间范围 (day, week, month, year)
            safe_search: 安全搜索级别 (0, 1, 2)
            format: 返回格式 (json 或 html)
        
        Returns:
            搜索结果字典
        """
        params = {
            "q": query,
            "format": format,
            "language": language,
            "pageno": page,
            "time_range": time_range,
            "safe_search": safe_search
        }
        
        if engines:
            params["engines"] = ",".join(engines)
        
        response = self.session.get(f"{self.base_url}/search", params=params)
        response.raise_for_status()
        
        if format == "json":
            return response.json()
        else:
            return {"html": response.text}
    
    def search_baidu(self, query: str, **kwargs) -> Dict[str, Any]:
        """百度搜索"""
        return self.search(query, engines=["baidu"], **kwargs)
    
    def search_sogou(self, query: str, **kwargs) -> Dict[str, Any]:
        """搜狗搜索"""
        return self.search(query, engines=["sogou"], **kwargs)
    
    def search_360(self, query: str, **kwargs) -> Dict[str, Any]:
        """360搜索"""
        return self.search(query, engines=["360search"], **kwargs)
    
    def search_google(self, query: str, **kwargs) -> Dict[str, Any]:
        """Google搜索"""
        return self.search(query, engines=["google"], **kwargs)
    
    def search_academic(self, query: str, **kwargs) -> Dict[str, Any]:
        """学术搜索"""
        return self.search(query, engines=["google_scholar", "arxiv"], **kwargs)
    
    def search_wechat(self, query: str, **kwargs) -> Dict[str, Any]:
        """微信搜索"""
        return self.search(query, engines=["sogou_wechat"], **kwargs)
    
    def search_dev(self, query: str, **kwargs) -> Dict[str, Any]:
        """开发者搜索"""
        return self.search(query, engines=["github", "stackoverflow", "huggingface"], **kwargs)
    
    def search_images(self, query: str, **kwargs) -> Dict[str, Any]:
        """图片搜索"""
        return self.search(query, engines=["baidu_images", "sogou_images", "google_images"], **kwargs)
    
    def search_videos(self, query: str, **kwargs) -> Dict[str, Any]:
        """视频搜索"""
        return self.search(query, engines=["360search_videos", "sogou_videos", "youtube_noapi"], **kwargs)
    
    def get_engines(self) -> List[Dict[str, Any]]:
        """获取可用的搜索引擎列表"""
        response = self.session.get(f"{self.base_url}/config")
        response.raise_for_status()
        config = response.json()
        return config.get("engines", [])
    
    def get_stats(self) -> Dict[str, Any]:
        """获取搜索引擎统计信息"""
        response = self.session.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False


def main():
    """示例用法"""
    client = SearXNGClient()
    
    # 健康检查
    if not client.health_check():
        print("SearXNG服务不可用")
        return
    
    print("SearXNG服务正常")
    
    # 百度搜索示例
    print("\n=== 百度搜索 ===")
    results = client.search_baidu("医疗AI")
    for result in results.get("results", [])[:3]:
        print(f"标题: {result.get('title')}")
        print(f"链接: {result.get('url')}")
        print()
    
    # 学术搜索示例
    print("\n=== 学术搜索 ===")
    results = client.search_academic("artificial intelligence healthcare")
    for result in results.get("results", [])[:3]:
        print(f"标题: {result.get('title')}")
        print(f"链接: {result.get('url')}")
        print()
    
    # 微信搜索示例
    print("\n=== 微信搜索 ===")
    results = client.search_wechat("医疗AI")
    for result in results.get("results", [])[:3]:
        print(f"标题: {result.get('title')}")
        print(f"链接: {result.get('url')}")
        print()


if __name__ == "__main__":
    main()
