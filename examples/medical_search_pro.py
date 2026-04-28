#!/usr/bin/env python3
"""
SearXNG 医疗AI专业搜索模块 v2.0
功能: 药品信息、临床指南、学术文献、罕见病、药物相互作用
借鉴: PubMed, UpToDate, Epocrates, Semantic Scholar
"""

import sys
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 添加API目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from searxng_api import SearXNGClient


@dataclass
class SearchResult:
    """搜索结果数据类"""
    title: str
    url: str
    content: str
    source: str
    relevance_score: float = 0.0
    timestamp: str = ""


class MedicalSearchPro:
    """医疗AI专业搜索引擎"""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        """
        初始化医疗搜索引擎
        
        Args:
            base_url: SearXNG服务地址
        """
        self.client = SearXNGClient(base_url)
        
        # 医学术语同义词表
        self.medical_synonyms = {
            "心肌梗死": ["心脏病发作", "心梗", "myocardial infarction", "MI"],
            "糖尿病": ["消渴症", "diabetes", "diabetes mellitus"],
            "高血压": ["血压高", "hypertension", "high blood pressure"],
            "阿尔茨海默症": ["老年痴呆", "Alzheimer's disease", "AD"],
            "帕金森病": ["震颤麻痹", "Parkinson's disease", "PD"],
            "肺癌": ["肺部肿瘤", "lung cancer", "pulmonary carcinoma"],
            "乳腺癌": ["乳癌", "breast cancer", "mammary carcinoma"],
            "艾滋病": ["获得性免疫缺陷综合征", "AIDS", "HIV"],
            "新冠肺炎": ["COVID-19", "新冠病毒", "SARS-CoV-2"],
            "抑郁症": ["忧郁症", "depression", "major depressive disorder"]
        }
        
        # 药物分类
        self.drug_categories = {
            "心血管药物": ["阿司匹林", "氯吡格雷", "他汀类", "ACE抑制剂", "β受体阻滞剂"],
            "抗肿瘤药物": ["化疗药", "靶向药", "免疫治疗", "PD-1抑制剂"],
            "神经系统药物": ["抗抑郁药", "抗精神病药", "抗癫痫药", "镇静催眠药"],
            "抗感染药物": ["抗生素", "抗病毒药", "抗真菌药", "抗寄生虫药"],
            "内分泌药物": ["胰岛素", "口服降糖药", "甲状腺激素", "糖皮质激素"]
        }
    
    def search_drug_info(self, drug_name: str, depth: str = "standard") -> Dict[str, Any]:
        """
        搜索药品信息
        
        Args:
            drug_name: 药品名称
            depth: 搜索深度 (basic/standard/comprehensive)
        
        Returns:
            药品信息字典
        """
        results = {
            'drug_name': drug_name,
            'basic_info': [],
            'clinical_studies': [],
            'adverse_effects': [],
            'interactions': [],
            'guidelines': []
        }
        
        # 基本信息
        basic_queries = [
            f"{drug_name} 药品说明书",
            f"{drug_name} 适应症 用法用量",
            f"{drug_name} 药理作用 作用机制"
        ]
        
        for query in basic_queries:
            search_results = self.client.search_baidu(query)
            results['basic_info'].extend(search_results.get('results', [])[:3])
        
        # 临床研究
        if depth in ["standard", "comprehensive"]:
            clinical_queries = [
                f"{drug_name} clinical trial",
                f"{drug_name} 临床研究",
                f"{drug_name} efficacy safety"
            ]
            
            for query in clinical_queries:
                search_results = self.client.search_academic(query)
                results['clinical_studies'].extend(search_results.get('results', [])[:3])
        
        # 不良反应
        if depth == "comprehensive":
            adverse_queries = [
                f"{drug_name} 不良反应 副作用",
                f"{drug_name} adverse effects",
                f"{drug_name} 药物警戒"
            ]
            
            for query in adverse_queries:
                search_results = self.client.search_baidu(query)
                results['adverse_effects'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
        return results
    
    def search_disease_info(self, disease_name: str, depth: str = "standard") -> Dict[str, Any]:
        """
        搜索疾病信息
        
        Args:
            disease_name: 疾病名称
            depth: 搜索深度 (basic/standard/comprehensive)
        
        Returns:
            疾病信息字典
        """
        results = {
            'disease_name': disease_name,
            'overview': [],
            'diagnosis': [],
            'treatment': [],
            'prevention': [],
            'research': []
        }
        
        # 获取同义词
        synonyms = self.medical_synonyms.get(disease_name, [disease_name])
        
        # 概述
        overview_queries = [
            f"{disease_name} 疾病概述",
            f"{disease_name} 症状 病因",
            f"{disease_name} 流行病学"
        ]
        
        for query in overview_queries:
            search_results = self.client.search_baidu(query)
            results['overview'].extend(search_results.get('results', [])[:3])
        
        # 诊断
        if depth in ["standard", "comprehensive"]:
            diagnosis_queries = [
                f"{disease_name} 诊断标准",
                f"{disease_name} 检查方法",
                f"{disease_name} diagnosis criteria"
            ]
            
            for query in diagnosis_queries:
                search_results = self.client.search_baidu(query)
                results['diagnosis'].extend(search_results.get('results', [])[:3])
        
        # 治疗
        treatment_queries = [
            f"{disease_name} 治疗方案",
            f"{disease_name} 治疗指南",
            f"{disease_name} treatment guidelines"
        ]
        
        for query in treatment_queries:
            search_results = self.client.search_baidu(query)
            results['treatment'].extend(search_results.get('results', [])[:3])
        
        # 最新研究
        if depth == "comprehensive":
            research_queries = [
                f"{disease_name} 最新研究",
                f"{disease_name} research breakthrough",
                f"{disease_name} 2024 2025"
            ]
            
            for query in research_queries:
                search_results = self.client.search_academic(query)
                results['research'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
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
            'overview': [],
            'genetics': [],
            'patient_resources': [],
            'clinical_trials': [],
            'advocacy': []
        }
        
        # 概述
        overview_queries = [
            f"{disease_name} 罕见病",
            f"{disease_name} orphan disease",
            f"{disease_name} 发病率 患病率"
        ]
        
        for query in overview_queries:
            search_results = self.client.search_baidu(query)
            results['overview'].extend(search_results.get('results', [])[:3])
        
        # 遗传学信息
        genetics_queries = [
            f"{disease_name} 基因突变",
            f"{disease_name} genetics",
            f"{disease_name} 遗传方式"
        ]
        
        for query in genetics_queries:
            search_results = self.client.search_academic(query)
            results['genetics'].extend(search_results.get('results', [])[:3])
        
        # 患者资源
        patient_queries = [
            f"{disease_name} 患者组织",
            f"{disease_name} patient support",
            f"{disease_name} 病友群"
        ]
        
        for query in patient_queries:
            search_results = self.client.search_wechat(query)
            results['patient_resources'].extend(search_results.get('results', [])[:3])
        
        # 临床试验
        trial_queries = [
            f"{disease_name} clinical trial",
            f"{disease_name} 临床试验",
            f"{disease_name} 新药研发"
        ]
        
        for query in trial_queries:
            search_results = self.client.search_academic(query)
            results['clinical_trials'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
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
            'interactions': [],
            'clinical_significance': [],
            'management': []
        }
        
        # 相互作用信息
        interaction_queries = [
            f"{drug1} {drug2} 相互作用",
            f"{drug1} {drug2} drug interaction",
            f"{drug1} {drug2} 配伍禁忌"
        ]
        
        for query in interaction_queries:
            search_results = self.client.search_baidu(query)
            results['interactions'].extend(search_results.get('results', [])[:3])
        
        # 临床意义
        clinical_queries = [
            f"{drug1} {drug2} 临床意义",
            f"{drug1} {drug2} clinical significance",
            f"{drug1} {drug2} 安全性"
        ]
        
        for query in clinical_queries:
            search_results = self.client.search_academic(query)
            results['clinical_significance'].extend(search_results.get('results', [])[:3])
        
        # 管理建议
        management_queries = [
            f"{drug1} {drug2} 管理建议",
            f"{drug1} {drug2} management",
            f"{drug1} {drug2} 替代方案"
        ]
        
        for query in management_queries:
            search_results = self.client.search_baidu(query)
            results['management'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
        return results
    
    def search_clinical_guidelines(self, condition: str, country: str = "all") -> Dict[str, Any]:
        """
        搜索临床指南
        
        Args:
            condition: 疾病/症状
            country: 国家/地区 (all/china/us/eu/who)
        
        Returns:
            临床指南信息
        """
        results = {
            'condition': condition,
            'chinese_guidelines': [],
            'international_guidelines': [],
            'evidence_levels': []
        }
        
        # 中国指南
        if country in ["all", "china"]:
            chinese_queries = [
                f"{condition} 临床指南 中国",
                f"{condition} 诊疗规范",
                f"{condition} 专家共识"
            ]
            
            for query in chinese_queries:
                search_results = self.client.search_baidu(query)
                results['chinese_guidelines'].extend(search_results.get('results', [])[:3])
        
        # 国际指南
        if country in ["all", "us", "eu", "who"]:
            international_queries = [
                f"{condition} clinical guideline",
                f"{condition} NICE guideline",
                f"{condition} WHO guideline",
                f"{condition} practice parameter"
            ]
            
            for query in international_queries:
                search_results = self.client.search_academic(query)
                results['international_guidelines'].extend(search_results.get('results', [])[:3])
        
        # 证据等级
        evidence_queries = [
            f"{condition} 证据等级",
            f"{condition} evidence level",
            f"{condition} meta-analysis"
        ]
        
        for query in evidence_queries:
            search_results = self.client.search_academic(query)
            results['evidence_levels'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
        return results
    
    def search_medical_literature(self, topic: str, year_from: int = None, 
                                 year_to: int = None) -> Dict[str, Any]:
        """
        搜索医学文献
        
        Args:
            topic: 研究主题
            year_from: 起始年份
            year_to: 结束年份
        
        Returns:
            文献信息字典
        """
        results = {
            'topic': topic,
            'pubmed': [],
            'arxiv': [],
            'google_scholar': [],
            'recent_reviews': []
        }
        
        # PubMed搜索
        pubmed_queries = [
            f"{topic} pubmed",
            f"{topic} systematic review",
            f"{topic} meta-analysis"
        ]
        
        for query in pubmed_queries:
            search_results = self.client.search_academic(query)
            results['pubmed'].extend(search_results.get('results', [])[:3])
        
        # arXiv搜索（AI/机器学习相关）
        arxiv_queries = [
            f"{topic} arxiv",
            f"{topic} machine learning",
            f"{topic} deep learning"
        ]
        
        for query in arxiv_queries:
            search_results = self.client.search_academic(query)
            results['arxiv'].extend(search_results.get('results', [])[:3])
        
        # Google Scholar搜索
        scholar_queries = [
            f"{topic} research",
            f"{topic} study",
            f"{topic} clinical trial"
        ]
        
        for query in scholar_queries:
            search_results = self.client.search_academic(query)
            results['google_scholar'].extend(search_results.get('results', [])[:3])
        
        # 最新综述
        review_queries = [
            f"{topic} review 2024",
            f"{topic} recent advances",
            f"{topic} current status"
        ]
        
        for query in review_queries:
            search_results = self.client.search_academic(query)
            results['recent_reviews'].extend(search_results.get('results', [])[:3])
        
        # 去重
        for key in results:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
        return results
    
    def get_drug_category_info(self, category: str) -> Dict[str, Any]:
        """
        获取药物分类信息
        
        Args:
            category: 药物分类
        
        Returns:
            药物分类信息
        """
        results = {
            'category': category,
            'drugs': [],
            'overview': [],
            'mechanisms': []
        }
        
        # 获取该分类下的药物
        drugs = self.drug_categories.get(category, [])
        
        # 搜索分类概述
        overview_queries = [
            f"{category} 药物分类",
            f"{category} overview",
            f"{category} 作用机制"
        ]
        
        for query in overview_queries:
            search_results = self.client.search_baidu(query)
            results['overview'].extend(search_results.get('results', [])[:3])
        
        # 搜索各药物信息
        for drug in drugs[:5]:  # 限制搜索前5个药物
            drug_info = self.search_drug_info(drug, depth="basic")
            results['drugs'].append({
                'name': drug,
                'info': drug_info['basic_info'][:2]
            })
        
        # 去重
        for key in ['overview', 'mechanisms']:
            if isinstance(results[key], list):
                results[key] = self._deduplicate_results(results[key])
        
        return results
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """去重搜索结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def format_results_markdown(self, results: Dict[str, Any], title: str = "") -> str:
        """
        格式化搜索结果为Markdown
        
        Args:
            results: 搜索结果
            title: 标题
        
        Returns:
            Markdown格式的结果
        """
        md = f"# {title}\n\n" if title else ""
        
        for key, value in results.items():
            if isinstance(value, list) and value:
                md += f"## {key}\n\n"
                for i, item in enumerate(value[:5], 1):
                    if isinstance(item, dict):
                        title = item.get('title', '无标题')
                        url = item.get('url', '')
                        content = item.get('content', '')[:200]
                        md += f"{i}. **[{title}]({url})**\n"
                        if content:
                            md += f"   {content}...\n"
                        md += "\n"
        
        return md


def main():
    """示例用法"""
    print("=== SearXNG 医疗AI专业搜索 v2.0 ===\n")
    
    # 检查服务状态
    engine = MedicalSearchPro()
    if not engine.client.health_check():
        print("SearXNG服务不可用，请先启动服务")
        return
    
    print("SearXNG服务正常\n")
    
    # 搜索药品信息
    print("1. 搜索药品信息：阿司匹林")
    drug_results = engine.search_drug_info("阿司匹林", depth="standard")
    print(f"   基本信息: {len(drug_results['basic_info'])} 条")
    print(f"   临床研究: {len(drug_results['clinical_studies'])} 条")
    
    # 搜索疾病信息
    print("\n2. 搜索疾病信息：糖尿病")
    disease_results = engine.search_disease_info("糖尿病", depth="standard")
    print(f"   概述: {len(disease_results['overview'])} 条")
    print(f"   诊断: {len(disease_results['diagnosis'])} 条")
    print(f"   治疗: {len(disease_results['treatment'])} 条")
    
    # 搜索罕见病信息
    print("\n3. 搜索罕见病信息：渐冻症")
    rare_results = engine.search_rare_disease("渐冻症")
    print(f"   概述: {len(rare_results['overview'])} 条")
    print(f"   遗传学: {len(rare_results['genetics'])} 条")
    print(f"   患者资源: {len(rare_results['patient_resources'])} 条")
    print(f"   临床试验: {len(rare_results['clinical_trials'])} 条")
    
    # 搜索药物相互作用
    print("\n4. 搜索药物相互作用：阿司匹林 + 华法林")
    interaction_results = engine.search_drug_interactions("阿司匹林", "华法林")
    print(f"   相互作用: {len(interaction_results['interactions'])} 条")
    print(f"   临床意义: {len(interaction_results['clinical_significance'])} 条")
    
    # 搜索临床指南
    print("\n5. 搜索临床指南：高血压")
    guideline_results = engine.search_clinical_guidelines("高血压", country="all")
    print(f"   中国指南: {len(guideline_results['chinese_guidelines'])} 条")
    print(f"   国际指南: {len(guideline_results['international_guidelines'])} 条")
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()
