"""
SearXNG AI摘要器
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Summary:
    """摘要数据"""
    text: str
    sources: List[str]
    confidence: float
    key_points: List[str]


class Summarizer:
    """AI摘要器"""
    
    def __init__(self):
        self.initialized = False
    
    def initialize(self) -> bool:
        """初始化摘要器"""
        # 这里可以加载AI模型
        self.initialized = True
        return True
    
    def summarize(self, query: str, results: List[Dict]) -> Optional[Summary]:
        """
        生成搜索结果摘要
        
        Args:
            query: 搜索查询
            results: 搜索结果列表
        
        Returns:
            摘要对象
        """
        if not self.initialized:
            return None
        
        if not results:
            return None
        
        # 提取关键信息
        sources = []
        key_points = []
        
        for result in results[:5]:
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            
            if title:
                key_points.append(title)
            if url:
                sources.append(url)
        
        # 生成摘要
        summary_text = f"关于「{query}」的搜索结果摘要：\n\n"
        
        for i, point in enumerate(key_points[:3], 1):
            summary_text += f"{i}. {point}\n"
        
        summary_text += f"\n共找到 {len(results)} 条相关结果。"
        
        return Summary(
            text=summary_text,
            sources=sources[:3],
            confidence=0.85,
            key_points=key_points[:5]
        )
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        文本摘要
        
        Args:
            text: 原始文本
            max_length: 最大长度
        
        Returns:
            摘要文本
        """
        if len(text) <= max_length:
            return text
        
        # 简单截断
        return text[:max_length] + "..."
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """
        提取关键词
        
        Args:
            text: 文本
            top_k: 返回前k个关键词
        
        Returns:
            关键词列表
        """
        # 简单的关键词提取
        words = text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_k]]


class MedicalSummarizer(Summarizer):
    """医疗领域摘要器"""
    
    def __init__(self):
        super().__init__()
        self.medical_terms = {
            "心肌梗死": "心脏病发作，心肌缺血坏死",
            "糖尿病": "代谢性疾病，血糖水平异常",
            "高血压": "血压持续升高，心血管疾病风险因素",
            "肺癌": "肺部恶性肿瘤",
            "乳腺癌": "乳腺恶性肿瘤"
        }
    
    def summarize_medical(self, query: str, results: List[Dict]) -> Optional[Summary]:
        """
        医疗搜索结果摘要
        
        Args:
            query: 搜索查询
            results: 搜索结果列表
        
        Returns:
            医疗摘要对象
        """
        # 基础摘要
        summary = self.summarize(query, results)
        
        if not summary:
            return None
        
        # 添加医疗术语解释
        for term, explanation in self.medical_terms.items():
            if term in query:
                summary.key_points.insert(0, f"{term}: {explanation}")
                break
        
        return summary
    
    def extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """
        提取医疗实体
        
        Args:
            text: 文本
        
        Returns:
            医疗实体字典
        """
        entities = {
            "diseases": [],
            "drugs": [],
            "symptoms": [],
            "treatments": []
        }
        
        # 疾病关键词
        disease_keywords = ["病", "症", "肿瘤", "癌", "炎"]
        for keyword in disease_keywords:
            if keyword in text:
                # 简单提取
                idx = text.find(keyword)
                start = max(0, idx - 5)
                end = min(len(text), idx + 5)
                disease = text[start:end]
                entities["diseases"].append(disease)
        
        return entities
