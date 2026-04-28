"""
SearXNG 插件系统
"""

from .base import Plugin, PluginManager
from .registry import PluginRegistry

__version__ = "1.0.0"
__all__ = ["Plugin", "PluginManager", "PluginRegistry"]
