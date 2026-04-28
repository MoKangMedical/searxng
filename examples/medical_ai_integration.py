#!/usr/bin/env python3
"""
SearXNG 医疗AI集成模块
用于MediChat-RD、DrugMind等医疗AI项目
支持JSON API
"""

import sys
import os
import json
from typing import Dict, List, Any, Optional

# 添加API目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from searxng_api import SearXNGClient


class MedicalSearchEngine:
    """医疗搜索引擎"""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        """
        初始化医疗搜索引擎
        
        Args:
            base_url: SearXNG服务地址
        """
        self.client = SearXNGClient(base_url)
    
    def search_drug_info(self, drug_name: str) -> Dict[str, Any]:
        """
        搜索药品信息
        
        Args:
            drug_name: 药品名称
        
        Returns:
            药品信息字典
        """
        results = {
            'drug_name': drug_name,
            'baidu': [],
            'academic': [],
            'official': []
        }
        
        # 百度搜索药品说明书
        baidu_results = self.client.search_baidu(f"{drug_name} 药品说明书")
        results['baidu'] = baidu_results.get('results', [])[:5]
        
        # 学术搜索药品研究
        academic_results = self.client.search_academic(f"{drug_name} clinical trial")
        results['academic'] = academic_results.get('results', [])[:5]
        
        # 微信搜索药品资讯
        wechat_results = self.client.search_wechat(f"{drug_name} 药品")
        results['official'] = wechat_results.get('results', [])[:5]
        
        return results
    
    def search_disease_info(self, disease_name: str) -> Dict[str, Any]:
        """
        搜索疾病信息
        
        Args:
            disease_name: 疾病名称
        
        Returns:
            疾病信息字典
        """
        results = {
            'disease_name': disease_name,
            'baidu': [],
            'academic': [],
            'treatment': []
        }
        
        # 百度搜索疾病信息
        baidu_results = self.client.search_baidu(f"{disease_name} 症状 治疗")
        results['baidu'] = baidu_results.get('results', [])[:5]
        
        # 学术搜索疾病研究
        academic_results = self.client.search_academic(f"{disease_name} treatment")
        results['academic'] = academic_results.get('results', [])[:5]
        
        # 微信搜索治疗方案
        wechat_results = self.client.search_wechat(f"{disease_name} 治疗方案")
        results['treatment'] = wechat_results.get('results', [])[:5]
        
        return results
    
    def search_rare_disease(self, disease_name: str) -> Dict[str, Any]:
        """
        搜索罕见病信息（用于MediChat-RD）
        
        Args:
            disease_name: 罕见病名称
        
        Returns:
            罕见病信息字典
        """
        results = {
            'disease_name': disease_name,
            'baidu': [],
            'academic': [],
            'patient_community': [],
            'clinical_trials': []
        }
        
        # 百度搜索罕见病信息
        baidu_results = self.client.search_baidu(f"{disease_name} 罕见病")
        results['baidu'] = baidu_results.get('results', [])[:5]
        
        # 学术搜索罕见病研究
        academic_results = self.client.search_academic(f"{disease_name} rare disease")
        results['academic'] = academic_results.get('results', [])[:5]
        
        # 微信搜索患者社区
        wechat_results = self.client.search_wechat(f"{disease_name} 患者")
        results['patient_community'] = wechat_results.get('results', [])[:5]
        
        # 搜索临床试验
        clinical_results = self.client.search_academic(f"{disease_name} clinical trial")
        results['clinical_trials'] = clinical_results.get('results', [])[:5]
        
        return results
    
    def search_medical_literature(self, topic: str) -> Dict[str, Any]:
        """
        搜索医学文献
        
        Args:
            topic: 研究主题
        
        Returns:
            文献信息字典
        """
        results = {
            'topic': topic,
            'arxiv': [],
            'google_scholar': []
        }
        
        # arXiv搜索
        arxiv_results = self.client.search_academic(f"{topic} arxiv")
        results['arxiv'] = arxiv_results.get('results', [])[:5]
        
        # 综合学术搜索
        academic_results = self.client.search_academic(topic)
        results['google_scholar'] = academic_results.get('results', [])[:5]
        
        return results
    
    def search_clinical_guidelines(self, condition: str) -> Dict[str, Any]:
        """
        搜索临床指南
        
        Args:
            condition: 疾病/症状
        
        Returns:
            临床指南信息字典
        """
        results = {
            'condition': condition,
            'chinese_guidelines': [],
            'international_guidelines': []
        }
        
        # 搜索中国临床指南
        chinese_results = self.client.search_baidu(f"{condition} 临床指南 诊疗规范")
        results['chinese_guidelines'] = chinese_results.get('results', [])[:5]
        
        # 搜索国际临床指南
        international_results = self.client.search_academic(f"{condition} clinical guideline")
        results['international_guidelines'] = international_results.get('results', [])[:5]
        
        return results
    
    def search_drug_interactions(self, drug1: str, drug2: str) -> Dict[str, Any]:
        """
        搜索药物相互作用
        
        Args:
            drug1: 药物1
            drug2: 药物2
        
        Returns:
            药物相互作用信息
        """
        results = {
            'drug1': drug1,
            'drug2': drug2,
            'baidu': [],
            'academic': []
        }
        
        # 百度搜索药物相互作用
        baidu_results = self.client.search_baidu(f"{drug1} {drug2} 相互作用")
        results['baidu'] = baidu_results.get('results', [])[:5]
        
        # 学术搜索药物相互作用
        academic_results = self.client.search_academic(f"{drug1} {drug2} drug interaction")
        results['academic'] = academic_results.get('results', [])[:5]
        
        return results


def main():
    """示例用法"""
    print("=== SearXNG 医疗AI集成示例 ===\n")
    
    # 检查服务状态
    engine = MedicalSearchEngine()
    if not engine.client.health_check():
        print("SearXNG服务不可用，请先启动服务")
        return
    
    print("SearXNG服务正常\n")
    
    # 搜索药品信息
    print("1. 搜索药品信息：阿司匹林")
    drug_results = engine.search_drug_info("阿司匹林")
    print(f"   百度结果: {len(drug_results['baidu'])} 条")
    print(f"   学术结果: {len(drug_results['academic'])} 条")
    print(f"   资讯结果: {len(drug_results['official'])} 条")
    
    # 搜索疾病信息
    print("\n2. 搜索疾病信息：糖尿病")
    disease_results = engine.search_disease_info("糖尿病")
    print(f"   百度结果: {len(disease_results['baidu'])} 条")
    print(f"   学术结果: {len(disease_results['academic'])} 条")
    print(f"   治疗方案: {len(disease_results['treatment'])} 条")
    
    # 搜索罕见病信息
    print("\n3. 搜索罕见病信息：渐冻症")
    rare_results = engine.search_rare_disease("渐冻症")
    print(f"   百度结果: {len(rare_results['baidu'])} 条")
    print(f"   学术结果: {len(rare_results['academic'])} 条")
    print(f"   患者社区: {len(rare_results['patient_community'])} 条")
    print(f"   临床试验: {len(rare_results['clinical_trials'])} 条")
    
    # 搜索药物相互作用
    print("\n4. 搜索药物相互作用：阿司匹林 + 华法林")
    interaction_results = engine.search_drug_interactions("阿司匹林", "华法林")
    print(f"   百度结果: {len(interaction_results['baidu'])} 条")
    print(f"   学术结果: {len(interaction_results['academic'])} 条")
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()
