"""
SearXNG 插件注册表
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path


class PluginRegistry:
    """插件注册表"""
    
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            registry_path = os.path.join(os.path.dirname(__file__), "registry.json")
        
        self.registry_path = Path(registry_path)
        self.plugins: Dict[str, Dict] = {}
        self.load()
    
    def load(self) -> bool:
        """加载注册表"""
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    self.plugins = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading registry: {e}")
            return False
    
    def save(self) -> bool:
        """保存注册表"""
        try:
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.plugins, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving registry: {e}")
            return False
    
    def register(self, name: str, info: Dict) -> bool:
        """注册插件"""
        self.plugins[name] = {
            **info,
            "registered_at": str(datetime.now()),
            "enabled": True
        }
        return self.save()
    
    def unregister(self, name: str) -> bool:
        """注销插件"""
        if name in self.plugins:
            del self.plugins[name]
            return self.save()
        return False
    
    def get(self, name: str) -> Optional[Dict]:
        """获取插件信息"""
        return self.plugins.get(name)
    
    def get_all(self) -> Dict[str, Dict]:
        """获取所有插件"""
        return self.plugins.copy()
    
    def enable(self, name: str) -> bool:
        """启用插件"""
        if name in self.plugins:
            self.plugins[name]["enabled"] = True
            return self.save()
        return False
    
    def disable(self, name: str) -> bool:
        """禁用插件"""
        if name in self.plugins:
            self.plugins[name]["enabled"] = False
            return self.save()
        return False
    
    def search(self, query: str) -> List[Dict]:
        """搜索插件"""
        results = []
        query_lower = query.lower()
        
        for name, info in self.plugins.items():
            if (query_lower in name.lower() or
                query_lower in info.get("description", "").lower() or
                query_lower in info.get("author", "").lower()):
                results.append({"name": name, **info})
        
        return results


# 示例插件
class CalculatorPlugin(Plugin):
    """计算器插件"""
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="calculator",
            version="1.0.0",
            description="计算器功能插件",
            author="SearXNG Team",
            hooks=["on_search"]
        )
    
    def initialize(self) -> bool:
        print("Calculator plugin initialized")
        return True
    
    def cleanup(self) -> bool:
        print("Calculator plugin cleaned up")
        return True
    
    def on_search(self, query: str, results: List[Dict]) -> List[Dict]:
        """处理计算器查询"""
        import re
        
        # 检查是否是数学表达式
        if re.match(r'^[\d\s\+\-\*\/\(\)\.\%\^]+$', query):
            try:
                # 安全计算
                result = eval(query)
                results.insert(0, {
                    "title": f"计算结果: {query} = {result}",
                    "content": f"{query} = {result}",
                    "url": "#",
                    "engine": "calculator"
                })
            except:
                pass
        
        return results


class UnitConverterPlugin(Plugin):
    """单位转换插件"""
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="unit_converter",
            version="1.0.0",
            description="单位转换功能插件",
            author="SearXNG Team",
            hooks=["on_search"]
        )
    
    def initialize(self) -> bool:
        print("Unit converter plugin initialized")
        return True
    
    def cleanup(self) -> bool:
        print("Unit converter plugin cleaned up")
        return True
    
    def on_search(self, query: str, results: List[Dict]) -> List[Dict]:
        """处理单位转换查询"""
        import re
        
        # 单位转换映射
        conversions = {
            "km": {"mi": 0.621371, "m": 1000, "ft": 3280.84},
            "mi": {"km": 1.60934, "m": 1609.34, "ft": 5280},
            "kg": {"lbs": 2.20462, "g": 1000, "oz": 35.274},
            "lbs": {"kg": 0.453592, "g": 453.592, "oz": 16},
            "celsius": {"fahrenheit": lambda x: x * 9/5 + 32, "kelvin": lambda x: x + 273.15},
            "fahrenheit": {"celsius": lambda x: (x - 32) * 5/9, "kelvin": lambda x: (x - 32) * 5/9 + 273.15}
        }
        
        # 检查是否是单位转换查询
        pattern = r'(\d+)\s*(km|mi|kg|lbs|celsius|fahrenheit)\s*(to|in)\s*(km|mi|kg|lbs|celsius|fahrenheit)'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if match:
            value = float(match.group(1))
            from_unit = match.group(2).lower()
            to_unit = match.group(4).lower()
            
            if from_unit in conversions and to_unit in conversions[from_unit]:
                conversion = conversions[from_unit][to_unit]
                if callable(conversion):
                    result = conversion(value)
                else:
                    result = value * conversion
                
                results.insert(0, {
                    "title": f"单位转换: {value} {from_unit} = {result:.2f} {to_unit}",
                    "content": f"{value} {from_unit} = {result:.2f} {to_unit}",
                    "url": "#",
                    "engine": "unit_converter"
                })
        
        return results
