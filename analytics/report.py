"""
SearXNG 报表生成模块
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import json


@dataclass
class Report:
    """报表数据"""
    title: str
    generated_at: str
    period: str
    summary: Dict
    details: Dict
    recommendations: List[str]


class ReportGenerator:
    """报表生成器"""
    
    def __init__(self):
        pass
    
    def generate_daily_report(self, stats: Dict, date: str = None) -> Report:
        """
        生成日报
        
        Args:
            stats: 统计数据
            date: 日期
        
        Returns:
            报表对象
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        summary = {
            "total_queries": stats.get("total_queries", 0),
            "success_rate": stats.get("success_rate", 0),
            "avg_response_time": stats.get("avg_response_time", 0),
            "top_engine": list(stats.get("top_engines", {}).keys())[0] if stats.get("top_engines") else "N/A"
        }
        
        recommendations = []
        
        if summary["success_rate"] < 0.95:
            recommendations.append("成功率较低，建议检查搜索引擎状态")
        
        if summary["avg_response_time"] > 2.0:
            recommendations.append("响应时间较长，建议优化缓存配置")
        
        return Report(
            title=f"SearXNG 日报 - {date}",
            generated_at=datetime.now().isoformat(),
            period=date,
            summary=summary,
            details=stats,
            recommendations=recommendations
        )
    
    def generate_weekly_report(self, stats: Dict, week: str = None) -> Report:
        """
        生成周报
        
        Args:
            stats: 统计数据
            week: 周标识
        
        Returns:
            报表对象
        """
        if week is None:
            week = datetime.now().strftime("%Y-W%W")
        
        summary = {
            "total_queries": stats.get("total_queries", 0),
            "unique_queries": stats.get("unique_queries", 0),
            "avg_success_rate": stats.get("success_rate", 0),
            "avg_response_time": stats.get("avg_response_time", 0)
        }
        
        recommendations = []
        
        # 分析趋势
        if stats.get("total_queries", 0) > 1000:
            recommendations.append("查询量较大，建议增加缓存容量")
        
        return Report(
            title=f"SearXNG 周报 - {week}",
            generated_at=datetime.now().isoformat(),
            period=week,
            summary=summary,
            details=stats,
            recommendations=recommendations
        )
    
    def export_report(self, report: Report, format: str = "json") -> str:
        """
        导出报表
        
        Args:
            report: 报表对象
            format: 导出格式
        
        Returns:
            导出内容
        """
        if format == "json":
            return json.dumps({
                "title": report.title,
                "generated_at": report.generated_at,
                "period": report.period,
                "summary": report.summary,
                "details": report.details,
                "recommendations": report.recommendations
            }, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            md = f"# {report.title}\n\n"
            md += f"**生成时间**: {report.generated_at}\n"
            md += f"**统计周期**: {report.period}\n\n"
            
            md += "## 摘要\n\n"
            for key, value in report.summary.items():
                md += f"- **{key}**: {value}\n"
            
            md += "\n## 建议\n\n"
            for rec in report.recommendations:
                md += f"- {rec}\n"
            
            return md
        
        else:
            return str(report)
