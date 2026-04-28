"""
SearXNG 搜索统计模块
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import json


@dataclass
class SearchMetrics:
    """搜索指标"""
    total_queries: int
    unique_queries: int
    avg_response_time: float
    success_rate: float
    top_engines: Dict[str, int]
    top_queries: List[Dict[str, int]]
    hourly_distribution: Dict[int, int]
    daily_distribution: Dict[str, int]


class SearchStats:
    """搜索统计"""
    
    def __init__(self):
        self.queries = []
        self.responses = []
        self.errors = []
    
    def record_query(self, query: str, engines: List[str], response_time: float, 
                    success: bool, results_count: int):
        """记录搜索查询"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "engines": engines,
            "response_time": response_time,
            "success": success,
            "results_count": results_count
        }
        
        self.queries.append(record)
        
        if not success:
            self.errors.append(record)
    
    def get_metrics(self, days: int = 7) -> SearchMetrics:
        """
        获取统计指标
        
        Args:
            days: 统计天数
        
        Returns:
            统计指标对象
        """
        # 过滤时间范围
        cutoff = datetime.now() - timedelta(days=days)
        recent_queries = [
            q for q in self.queries
            if datetime.fromisoformat(q["timestamp"]) > cutoff
        ]
        
        if not recent_queries:
            return SearchMetrics(
                total_queries=0,
                unique_queries=0,
                avg_response_time=0,
                success_rate=0,
                top_engines={},
                top_queries=[],
                hourly_distribution={},
                daily_distribution={}
            )
        
        # 计算指标
        total_queries = len(recent_queries)
        unique_queries = len(set(q["query"] for q in recent_queries))
        
        response_times = [q["response_time"] for q in recent_queries]
        avg_response_time = sum(response_times) / len(response_times)
        
        successful = sum(1 for q in recent_queries if q["success"])
        success_rate = successful / total_queries
        
        # 引擎统计
        engine_counts = defaultdict(int)
        for q in recent_queries:
            for engine in q["engines"]:
                engine_counts[engine] += 1
        top_engines = dict(sorted(engine_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # 查询统计
        query_counts = defaultdict(int)
        for q in recent_queries:
            query_counts[q["query"]] += 1
        top_queries = [
            {"query": q, "count": c}
            for q, c in sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # 小时分布
        hourly_distribution = defaultdict(int)
        for q in recent_queries:
            hour = datetime.fromisoformat(q["timestamp"]).hour
            hourly_distribution[hour] += 1
        
        # 日分布
        daily_distribution = defaultdict(int)
        for q in recent_queries:
            day = datetime.fromisoformat(q["timestamp"]).strftime("%Y-%m-%d")
            daily_distribution[day] += 1
        
        return SearchMetrics(
            total_queries=total_queries,
            unique_queries=unique_queries,
            avg_response_time=avg_response_time,
            success_rate=success_rate,
            top_engines=top_engines,
            top_queries=top_queries,
            hourly_distribution=dict(hourly_distribution),
            daily_distribution=dict(daily_distribution)
        )
    
    def export_json(self, filepath: str, days: int = 30) -> bool:
        """
        导出统计数据为JSON
        
        Args:
            filepath: 文件路径
            days: 统计天数
        
        Returns:
            是否成功
        """
        try:
            metrics = self.get_metrics(days)
            
            data = {
                "export_time": datetime.now().isoformat(),
                "period_days": days,
                "metrics": {
                    "total_queries": metrics.total_queries,
                    "unique_queries": metrics.unique_queries,
                    "avg_response_time": metrics.avg_response_time,
                    "success_rate": metrics.success_rate,
                    "top_engines": metrics.top_engines,
                    "top_queries": metrics.top_queries,
                    "hourly_distribution": metrics.hourly_distribution,
                    "daily_distribution": metrics.daily_distribution
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting stats: {e}")
            return False
    
    def get_engine_stats(self) -> Dict[str, Dict]:
        """
        获取引擎统计
        
        Returns:
            引擎统计字典
        """
        engine_stats = defaultdict(lambda: {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "total_response_time": 0
        })
        
        for query in self.queries:
            for engine in query["engines"]:
                stats = engine_stats[engine]
                stats["total"] += 1
                if query["success"]:
                    stats["successful"] += 1
                else:
                    stats["failed"] += 1
                stats["total_response_time"] += query["response_time"]
        
        # 计算平均值
        result = {}
        for engine, stats in engine_stats.items():
            result[engine] = {
                "total": stats["total"],
                "successful": stats["successful"],
                "failed": stats["failed"],
                "success_rate": stats["successful"] / stats["total"] if stats["total"] > 0 else 0,
                "avg_response_time": stats["total_response_time"] / stats["total"] if stats["total"] > 0 else 0
            }
        
        return result
