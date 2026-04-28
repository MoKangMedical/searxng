#!/usr/bin/env python3
"""
SearXNG API 单元测试
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from searxng_api import SearXNGClient


class TestSearXNGClient:
    """SearXNG客户端测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return SearXNGClient("http://localhost:8888")
    
    def test_health_check(self, client):
        """测试健康检查"""
        # 注意：这个测试需要SearXNG服务运行
        result = client.health_check()
        assert isinstance(result, bool)
    
    def test_search_basic(self, client):
        """测试基础搜索"""
        if not client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = client.search("test")
        assert "results" in result
        assert isinstance(result["results"], list)
    
    def test_search_baidu(self, client):
        """测试百度搜索"""
        if not client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = client.search_baidu("医疗AI")
        assert "results" in result
    
    def test_search_academic(self, client):
        """测试学术搜索"""
        if not client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = client.search_academic("artificial intelligence")
        assert "results" in result
    
    def test_search_wechat(self, client):
        """测试微信搜索"""
        if not client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = client.search_wechat("医疗AI")
        assert "results" in result


class TestSearchEnhancer:
    """搜索增强器测试类"""
    
    def test_medical_terms(self):
        """测试医疗术语"""
        from search_enhancements import SearchEnhancer
        
        suggestions = SearchEnhancer.get_suggestions("医疗")
        assert len(suggestions) > 0
    
    def test_engine_shortcuts(self):
        """测试搜索引擎快捷键"""
        from search_enhancements import SearchEnhancer
        
        suggestions = SearchEnhancer.get_suggestions("!bd")
        assert any("!bd" in s for s in suggestions)
    
    def test_advanced_query_parsing(self):
        """测试高级查询解析"""
        from search_enhancements import SearchEnhancer
        
        result = SearchEnhancer.parse_advanced_query("site:github.com 机器学习")
        assert result["filters"]["site"] == "github.com"
        assert "机器学习" in result["clean_query"]


class TestMedicalSearch:
    """医疗搜索测试类"""
    
    @pytest.fixture
    def engine(self):
        """创建医疗搜索引擎"""
        from medical_ai_integration import MedicalSearchEngine
        return MedicalSearchEngine()
    
    def test_drug_info_search(self, engine):
        """测试药品信息搜索"""
        if not engine.client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = engine.search_drug_info("阿司匹林")
        assert "drug_name" in result
        assert result["drug_name"] == "阿司匹林"
    
    def test_disease_info_search(self, engine):
        """测试疾病信息搜索"""
        if not engine.client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = engine.search_disease_info("糖尿病")
        assert "disease_name" in result
        assert result["disease_name"] == "糖尿病"
    
    def test_rare_disease_search(self, engine):
        """测试罕见病信息搜索"""
        if not engine.client.health_check():
            pytest.skip("SearXNG服务未运行")
        
        result = engine.search_rare_disease("渐冻症")
        assert "disease_name" in result
        assert result["disease_name"] == "渐冻症"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
