#!/usr/bin/env python3
"""
SearXNG API 认证和速率限制模块
功能: API Key认证、速率限制、使用统计
"""

import time
import json
import hashlib
import secrets
from typing import Optional, Dict, Any
from collections import defaultdict
import threading

class APIAuth:
    """API认证管理器"""
    
    def __init__(self):
        self.api_keys = {}
        self.lock = threading.Lock()
    
    def generate_api_key(self, name: str, permissions: list = None) -> str:
        """生成API Key"""
        api_key = f"sk-{secrets.token_hex(32)}"
        
        with self.lock:
            self.api_keys[api_key] = {
                "name": name,
                "permissions": permissions or ["search"],
                "created_at": time.time(),
                "last_used": None,
                "request_count": 0
            }
        
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """验证API Key"""
        with self.lock:
            if api_key in self.api_keys:
                self.api_keys[api_key]["last_used"] = time.time()
                self.api_keys[api_key]["request_count"] += 1
                return self.api_keys[api_key]
        return None
    
    def revoke_api_key(self, api_key: str) -> bool:
        """撤销API Key"""
        with self.lock:
            if api_key in self.api_keys:
                del self.api_keys[api_key]
                return True
        return False
    
    def list_api_keys(self) -> Dict[str, Dict[str, Any]]:
        """列出所有API Key"""
        with self.lock:
            return {k: {**v, "api_key": k[:12] + "..."} for k, v in self.api_keys.items()}


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, client_id: str) -> Dict[str, Any]:
        """检查是否允许请求"""
        now = time.time()
        
        with self.lock:
            # 清理过期记录
            self.requests[client_id] = [
                t for t in self.requests[client_id]
                if now - t < 3600  # 保留1小时内的记录
            ]
            
            # 检查每分钟限制
            minute_requests = [
                t for t in self.requests[client_id]
                if now - t < 60
            ]
            
            if len(minute_requests) >= self.requests_per_minute:
                return {
                    "allowed": False,
                    "reason": "每分钟请求次数超限",
                    "retry_after": 60 - (now - minute_requests[0])
                }
            
            # 检查每小时限制
            if len(self.requests[client_id]) >= self.requests_per_hour:
                return {
                    "allowed": False,
                    "reason": "每小时请求次数超限",
                    "retry_after": 3600 - (now - self.requests[client_id][0])
                }
            
            # 允许请求
            self.requests[client_id].append(now)
            
            return {
                "allowed": True,
                "remaining_minute": self.requests_per_minute - len(minute_requests) - 1,
                "remaining_hour": self.requests_per_hour - len(self.requests[client_id])
            }
    
    def get_usage_stats(self, client_id: str) -> Dict[str, Any]:
        """获取使用统计"""
        now = time.time()
        
        with self.lock:
            minute_requests = [
                t for t in self.requests.get(client_id, [])
                if now - t < 60
            ]
            
            hour_requests = [
                t for t in self.requests.get(client_id, [])
                if now - t < 3600
            ]
            
            return {
                "requests_last_minute": len(minute_requests),
                "requests_last_hour": len(hour_requests),
                "limit_per_minute": self.requests_per_minute,
                "limit_per_hour": self.requests_per_hour
            }


class UsageTracker:
    """使用统计追踪器"""
    
    def __init__(self):
        self.stats = defaultdict(lambda: {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_response_time": 0,
            "engines_used": defaultdict(int),
            "queries": []
        })
        self.lock = threading.Lock()
    
    def track_request(self, client_id: str, query: str, engines: list, 
                     response_time: float, success: bool):
        """追踪请求"""
        with self.lock:
            stats = self.stats[client_id]
            stats["total_requests"] += 1
            
            if success:
                stats["successful_requests"] += 1
            else:
                stats["failed_requests"] += 1
            
            stats["total_response_time"] += response_time
            
            for engine in engines:
                stats["engines_used"][engine] += 1
            
            # 保留最近100个查询
            stats["queries"].append({
                "query": query,
                "timestamp": time.time(),
                "engines": engines,
                "response_time": response_time,
                "success": success
            })
            
            if len(stats["queries"]) > 100:
                stats["queries"] = stats["queries"][-100:]
    
    def get_stats(self, client_id: str) -> Dict[str, Any]:
        """获取统计信息"""
        with self.lock:
            stats = self.stats.get(client_id, {})
            
            if not stats:
                return {
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                    "average_response_time": 0,
                    "success_rate": 0,
                    "engines_used": {},
                    "recent_queries": []
                }
            
            total = stats["total_requests"]
            successful = stats["successful_requests"]
            
            return {
                "total_requests": total,
                "successful_requests": successful,
                "failed_requests": stats["failed_requests"],
                "average_response_time": stats["total_response_time"] / total if total > 0 else 0,
                "success_rate": (successful / total * 100) if total > 0 else 0,
                "engines_used": dict(stats["engines_used"]),
                "recent_queries": stats["queries"][-10:]  # 最近10个查询
            }


# 全局实例
api_auth = APIAuth()
rate_limiter = RateLimiter()
usage_tracker = UsageTracker()


def require_auth(f):
    """认证装饰器"""
    def wrapper(*args, **kwargs):
        # 从请求中获取API Key
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return {"error": "缺少API Key"}, 401
        
        # 验证API Key
        key_info = api_auth.validate_api_key(api_key)
        if not key_info:
            return {"error": "无效的API Key"}, 401
        
        # 检查权限
        if "search" not in key_info.get("permissions", []):
            return {"error": "无搜索权限"}, 403
        
        return f(*args, **kwargs)
    
    return wrapper


def check_rate_limit(client_id: str) -> Optional[Dict[str, Any]]:
    """检查速率限制"""
    result = rate_limiter.is_allowed(client_id)
    
    if not result["allowed"]:
        return {
            "error": "请求过于频繁",
            "reason": result["reason"],
            "retry_after": result["retry_after"]
        }
    
    return None


def get_client_id(request) -> str:
    """获取客户端ID"""
    # 优先使用API Key
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    if api_key:
        return f"api_key:{api_key[:12]}"
    
    # 使用IP地址
    return f"ip:{request.remote_addr}"


def main():
    """测试函数"""
    print("=== API认证和速率限制测试 ===\n")
    
    # 测试API Key生成
    print("1. 生成API Key:")
    api_key = api_auth.generate_api_key("测试应用", ["search"])
    print(f"   API Key: {api_key}")
    
    # 测试API Key验证
    print("\n2. 验证API Key:")
    key_info = api_auth.validate_api_key(api_key)
    print(f"   验证结果: {key_info}")
    
    # 测试速率限制
    print("\n3. 速率限制测试:")
    for i in range(5):
        result = rate_limiter.is_allowed("test_client")
        print(f"   请求 {i+1}: {result}")
    
    # 测试使用统计
    print("\n4. 使用统计测试:")
    usage_tracker.track_request(
        "test_client",
        "医疗AI",
        ["baidu", "google"],
        0.5,
        True
    )
    
    stats = usage_tracker.get_stats("test_client")
    print(f"   统计信息: {stats}")
    
    # 列出所有API Key
    print("\n5. API Key列表:")
    keys = api_auth.list_api_keys()
    for key, info in keys.items():
        print(f"   {key}: {info}")


if __name__ == "__main__":
    main()
