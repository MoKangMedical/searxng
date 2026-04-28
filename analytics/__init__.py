"""
SearXNG 数据分析模块
"""

from .stats import SearchStats
from .visualizer import Visualizer
from .report import ReportGenerator

__version__ = "1.0.0"
__all__ = ["SearchStats", "Visualizer", "ReportGenerator"]
