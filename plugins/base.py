"""
SearXNG 插件基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    version: str
    description: str
    author: str
    enabled: bool = True
    dependencies: List[str] = None
    hooks: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.hooks is None:
            self.hooks = []


class Plugin(ABC):
    """插件基类"""
    
    def __init__(self):
        self._info = self.get_info()
        self._enabled = True
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """获取插件信息"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化插件"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """清理插件"""
        pass
    
    def on_search(self, query: str, results: List[Dict]) -> List[Dict]:
        """搜索钩子"""
        return results
    
    def on_result(self, result: Dict) -> Dict:
        """结果钩子"""
        return result
    
    def on_error(self, error: Exception) -> Optional[Dict]:
        """错误钩子"""
        return None
    
    @property
    def info(self) -> PluginInfo:
        return self._info
    
    @property
    def enabled(self) -> bool:
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value


class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._hooks: Dict[str, List[Plugin]] = {}
    
    def register(self, plugin: Plugin) -> bool:
        """注册插件"""
        try:
            info = plugin.get_info()
            
            # 检查依赖
            for dep in info.dependencies:
                if dep not in self._plugins:
                    print(f"Missing dependency: {dep}")
                    return False
            
            # 初始化插件
            if not plugin.initialize():
                print(f"Failed to initialize plugin: {info.name}")
                return False
            
            # 注册插件
            self._plugins[info.name] = plugin
            
            # 注册钩子
            for hook in info.hooks:
                if hook not in self._hooks:
                    self._hooks[hook] = []
                self._hooks[hook].append(plugin)
            
            print(f"Registered plugin: {info.name} v{info.version}")
            return True
            
        except Exception as e:
            print(f"Error registering plugin: {e}")
            return False
    
    def unregister(self, name: str) -> bool:
        """注销插件"""
        if name not in self._plugins:
            return False
        
        plugin = self._plugins[name]
        
        # 清理插件
        plugin.cleanup()
        
        # 移除钩子
        for hook_plugins in self._hooks.values():
            if plugin in hook_plugins:
                hook_plugins.remove(plugin)
        
        # 移除插件
        del self._plugins[name]
        
        print(f"Unregistered plugin: {name}")
        return True
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """获取插件"""
        return self._plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, Plugin]:
        """获取所有插件"""
        return self._plugins.copy()
    
    def enable_plugin(self, name: str) -> bool:
        """启用插件"""
        plugin = self.get_plugin(name)
        if plugin:
            plugin.enabled = True
            return True
        return False
    
    def disable_plugin(self, name: str) -> bool:
        """禁用插件"""
        plugin = self.get_plugin(name)
        if plugin:
            plugin.enabled = False
            return True
        return False
    
    def call_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """调用钩子"""
        if hook_name not in self._hooks:
            return None
        
        result = None
        for plugin in self._hooks[hook_name]:
            if not plugin.enabled:
                continue
            
            try:
                hook_func = getattr(plugin, hook_name, None)
                if hook_func:
                    result = hook_func(*args, **kwargs)
            except Exception as e:
                print(f"Error in plugin {plugin.info.name}: {e}")
                plugin.on_error(e)
        
        return result
    
    def call_hook_chain(self, hook_name: str, initial_value: Any, *args, **kwargs) -> Any:
        """调用钩子链"""
        result = initial_value
        
        if hook_name not in self._hooks:
            return result
        
        for plugin in self._hooks[hook_name]:
            if not plugin.enabled:
                continue
            
            try:
                hook_func = getattr(plugin, hook_name, None)
                if hook_func:
                    result = hook_func(result, *args, **kwargs)
            except Exception as e:
                print(f"Error in plugin {plugin.info.name}: {e}")
                plugin.on_error(e)
        
        return result


# 全局插件管理器
plugin_manager = PluginManager()
