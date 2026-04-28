"""
SearXNG 语义搜索模块
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class SemanticResult:
    """语义搜索结果"""
    text: str
    score: float
    source: str


class SemanticSearch:
    """语义搜索引擎"""
    
    def __init__(self):
        self.initialized = False
        self.embeddings = {}
    
    def initialize(self) -> bool:
        """初始化语义搜索"""
        # 这里可以加载向量模型
        self.initialized = True
        return True
    
    def encode(self, text: str) -> List[float]:
        """
        文本编码
        
        Args:
            text: 输入文本
        
        Returns:
            嵌入向量
        """
        # 简单的TF-IDF编码
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 归一化
        max_freq = max(word_freq.values()) if word_freq else 1
        vector = {word: freq / max_freq for word, freq in word_freq.items()}
        
        return vector
    
    def similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        计算相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
        
        Returns:
            相似度分数
        """
        # 余弦相似度
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def search(self, query: str, documents: List[str], top_k: int = 5) -> List[SemanticResult]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前k个结果
        
        Returns:
            语义搜索结果列表
        """
        if not self.initialized:
            return []
        
        # 编码查询
        query_vec = self.encode(query)
        
        # 计算相似度
        results = []
        
        for i, doc in enumerate(documents):
            doc_vec = self.encode(doc)
            score = self.similarity(query_vec, doc_vec)
            
            results.append(SemanticResult(
                text=doc,
                score=score,
                source=f"document_{i}"
            ))
        
        # 排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:top_k]
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 10) -> List[Dict]:
        """
        结果重排序
        
        Args:
            query: 查询文本
            results: 搜索结果列表
            top_k: 返回前k个结果
        
        Returns:
            重排序后的结果列表
        """
        if not self.initialized:
            return results
        
        # 编码查询
        query_vec = self.encode(query)
        
        # 计算每个结果的语义分数
        scored_results = []
        
        for result in results:
            title = result.get("title", "")
            content = result.get("content", "")
            text = f"{title} {content}"
            
            doc_vec = self.encode(text)
            semantic_score = self.similarity(query_vec, doc_vec)
            
            # 综合分数
            original_score = result.get("score", 0)
            combined_score = 0.7 * original_score + 0.3 * semantic_score
            
            scored_results.append({
                **result,
                "semantic_score": semantic_score,
                "combined_score": combined_score
            })
        
        # 排序
        scored_results.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return scored_results[:top_k]
    
    def find_similar(self, text: str, corpus: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        查找相似文本
        
        Args:
            text: 输入文本
            corpus: 语料库
            top_k: 返回前k个结果
        
        Returns:
            相似文本列表
        """
        results = self.search(text, corpus, top_k)
        
        return [(r.text, r.score) for r in results]
