#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global CDN - Revolutionary global content delivery network
Features that provide worldwide content distribution and optimization
"""

import json
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import hashlib
import requests
import aiohttp
from PIL import Image
import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CDNProvider(Enum):
    """CDN providers"""
    CLOUDFLARE = "cloudflare"
    AWS_CLOUDFRONT = "aws_cloudfront"
    GOOGLE_CLOUD_CDN = "google_cloud_cdn"
    AZURE_CDN = "azure_cdn"
    MAXCDN = "maxcdn"
    KEYCDN = "keycdn"
    CUSTOM = "custom"

class ContentType(Enum):
    """Content types"""
    STATIC = "static"
    DYNAMIC = "dynamic"
    STREAMING = "streaming"
    API = "api"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class OptimizationLevel(Enum):
    """Optimization levels"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    PREMIUM = "premium"

@dataclass
class CDNNode:
    """CDN node representation"""
    id: str
    name: str
    location: str
    country: str
    region: str
    provider: CDNProvider
    status: str
    capacity: int
    current_load: float
    latency: float
    bandwidth: float
    created_at: datetime
    last_updated: datetime

@dataclass
class ContentCache:
    """Content cache representation"""
    id: str
    content_url: str
    content_type: ContentType
    size: int
    cache_key: str
    ttl: int
    hit_count: int
    miss_count: int
    last_accessed: datetime
    created_at: datetime

class GlobalCDN:
    """Revolutionary global content delivery network system"""
    
    def __init__(self):
        self.cdn_nodes: Dict[str, CDNNode] = {}
        self.content_caches: Dict[str, ContentCache] = {}
        self.cdn_providers: Dict[CDNProvider, Dict] = {}
        self.optimization_rules: Dict[str, Dict] = {}
        self.performance_metrics: Dict[str, List] = {}
        
        # Initialize global CDN
        self._initialize_cdn_providers()
        self._initialize_global_nodes()
        self._initialize_optimization_engine()
        self._initialize_caching_system()
        self._initialize_monitoring_system()
        
        logger.info("Global CDN initialized")
    
    def _initialize_cdn_providers(self):
        """Initialize CDN providers"""
        self.cdn_providers = {
            CDNProvider.CLOUDFLARE: {
                "api_endpoint": "https://api.cloudflare.com/client/v4",
                "features": ["ssl", "compression", "minification", "image_optimization"],
                "pricing": "pay_as_you_go",
                "global_presence": 200
            },
            CDNProvider.AWS_CLOUDFRONT: {
                "api_endpoint": "https://cloudfront.amazonaws.com",
                "features": ["ssl", "compression", "lambda_edge", "field_level_encryption"],
                "pricing": "usage_based",
                "global_presence": 400
            },
            CDNProvider.GOOGLE_CLOUD_CDN: {
                "api_endpoint": "https://www.googleapis.com/compute/v1",
                "features": ["ssl", "compression", "cache_invalidation", "load_balancing"],
                "pricing": "usage_based",
                "global_presence": 130
            },
            CDNProvider.AZURE_CDN: {
                "api_endpoint": "https://management.azure.com",
                "features": ["ssl", "compression", "custom_domain", "https_redirect"],
                "pricing": "usage_based",
                "global_presence": 100
            }
        }
    
    def _initialize_global_nodes(self):
        """Initialize global CDN nodes"""
        global_locations = [
            {"name": "New York", "country": "US", "region": "North America", "latency": 5},
            {"name": "London", "country": "UK", "region": "Europe", "latency": 8},
            {"name": "Tokyo", "country": "JP", "region": "Asia", "latency": 12},
            {"name": "Sydney", "country": "AU", "region": "Oceania", "latency": 15},
            {"name": "São Paulo", "country": "BR", "region": "South America", "latency": 18},
            {"name": "Mumbai", "country": "IN", "region": "Asia", "latency": 20},
            {"name": "Dubai", "country": "AE", "region": "Middle East", "latency": 22},
            {"name": "Cape Town", "country": "ZA", "region": "Africa", "latency": 25}
        ]
        
        for i, location in enumerate(global_locations):
            node_id = str(uuid.uuid4())
            node = CDNNode(
                id=node_id,
                name=f"CDN-{location['name']}-{i+1}",
                location=location["name"],
                country=location["country"],
                region=location["region"],
                provider=CDNProvider.CLOUDFLARE,
                status="active",
                capacity=1000,  # GB
                current_load=0.0,
                latency=location["latency"],
                bandwidth=10000,  # Mbps
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
            self.cdn_nodes[node_id] = node
    
    def _initialize_optimization_engine(self):
        """Initialize optimization engine"""
        self.optimization_engine = {
            "image_optimization": {
                "formats": ["webp", "avif", "jpeg", "png"],
                "compression": True,
                "resizing": True,
                "lazy_loading": True
            },
            "content_compression": {
                "gzip": True,
                "brotli": True,
                "deflate": True,
                "compression_level": 6
            },
            "minification": {
                "html": True,
                "css": True,
                "javascript": True,
                "json": True
            },
            "caching_strategies": {
                "browser_cache": 31536000,  # 1 year
                "cdn_cache": 86400,  # 1 day
                "api_cache": 300,  # 5 minutes
                "dynamic_cache": 60  # 1 minute
            }
        }
    
    def _initialize_caching_system(self):
        """Initialize caching system"""
        self.caching_system = {
            "cache_layers": ["browser", "cdn", "origin"],
            "cache_policies": {
                "static_content": {"ttl": 31536000, "strategy": "cache_first"},
                "dynamic_content": {"ttl": 300, "strategy": "network_first"},
                "api_responses": {"ttl": 60, "strategy": "stale_while_revalidate"}
            },
            "invalidation": {
                "manual": True,
                "automatic": True,
                "tag_based": True,
                "time_based": True
            }
        }
    
    def _initialize_monitoring_system(self):
        """Initialize monitoring system"""
        self.monitoring_system = {
            "metrics": ["latency", "throughput", "hit_ratio", "error_rate", "bandwidth"],
            "alerting": True,
            "real_time_monitoring": True,
            "performance_analysis": True,
            "cost_tracking": True
        }
    
    # 1. Content Distribution
    async def distribute_content(self, content_url: str, content_type: ContentType, 
                               optimization_level: OptimizationLevel) -> Dict:
        """Distribute content across global CDN"""
        try:
            distribution_id = str(uuid.uuid4())
            
            # Optimize content
            optimized_content = await self._optimize_content(content_url, content_type, optimization_level)
            
            # Select optimal nodes
            optimal_nodes = await self._select_optimal_nodes(content_url, content_type)
            
            # Distribute to nodes
            distribution_result = await self._distribute_to_nodes(optimized_content, optimal_nodes)
            
            # Create cache entries
            cache_entries = await self._create_cache_entries(optimized_content, optimal_nodes)
            
            return {
                "success": True,
                "distribution_id": distribution_id,
                "content_url": content_url,
                "optimized_content": optimized_content,
                "distributed_nodes": len(optimal_nodes),
                "cache_entries": len(cache_entries),
                "estimated_latency": min(node.latency for node in optimal_nodes),
                "distribution_time": distribution_result["distribution_time"]
            }
            
        except Exception as e:
            logger.error(f"Error distributing content: {e}")
            return {"success": False, "error": str(e)}
    
    async def _optimize_content(self, content_url: str, content_type: ContentType, 
                              optimization_level: OptimizationLevel) -> Dict:
        """Optimize content for CDN delivery"""
        try:
            # Simulate content optimization
            await asyncio.sleep(0.5)
            
            optimized_content = {
                "original_url": content_url,
                "optimized_url": f"{content_url}?optimized=true",
                "content_type": content_type.value,
                "optimization_level": optimization_level.value,
                "size_reduction": 0.0,
                "optimizations_applied": []
            }
            
            # Apply optimizations based on content type
            if content_type == ContentType.IMAGE:
                optimized_content.update(await self._optimize_image(content_url, optimization_level))
            elif content_type == ContentType.STATIC:
                optimized_content.update(await self._optimize_static_content(content_url, optimization_level))
            elif content_type == ContentType.DYNAMIC:
                optimized_content.update(await self._optimize_dynamic_content(content_url, optimization_level))
            
            return optimized_content
            
        except Exception as e:
            logger.error(f"Error optimizing content: {e}")
            return {"original_url": content_url, "error": str(e)}
    
    async def _optimize_image(self, image_url: str, optimization_level: OptimizationLevel) -> Dict:
        """Optimize image content"""
        # Simulate image optimization
        await asyncio.sleep(0.3)
        
        optimizations = []
        size_reduction = 0.0
        
        if optimization_level in [OptimizationLevel.STANDARD, OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("format_conversion")
            optimizations.append("compression")
            size_reduction += 0.3
        
        if optimization_level in [OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("resizing")
            optimizations.append("lazy_loading")
            size_reduction += 0.2
        
        if optimization_level == OptimizationLevel.PREMIUM:
            optimizations.append("webp_conversion")
            optimizations.append("avif_conversion")
            size_reduction += 0.25
        
        return {
            "optimizations_applied": optimizations,
            "size_reduction": size_reduction,
            "formats": ["webp", "avif", "jpeg"] if optimization_level == OptimizationLevel.PREMIUM else ["jpeg", "png"]
        }
    
    async def _optimize_static_content(self, content_url: str, optimization_level: OptimizationLevel) -> Dict:
        """Optimize static content"""
        # Simulate static content optimization
        await asyncio.sleep(0.2)
        
        optimizations = []
        size_reduction = 0.0
        
        if optimization_level in [OptimizationLevel.STANDARD, OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("minification")
            optimizations.append("compression")
            size_reduction += 0.4
        
        if optimization_level in [OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("tree_shaking")
            optimizations.append("dead_code_elimination")
            size_reduction += 0.2
        
        return {
            "optimizations_applied": optimizations,
            "size_reduction": size_reduction
        }
    
    async def _optimize_dynamic_content(self, content_url: str, optimization_level: OptimizationLevel) -> Dict:
        """Optimize dynamic content"""
        # Simulate dynamic content optimization
        await asyncio.sleep(0.2)
        
        optimizations = []
        size_reduction = 0.0
        
        if optimization_level in [OptimizationLevel.STANDARD, OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("response_compression")
            optimizations.append("caching_headers")
            size_reduction += 0.2
        
        if optimization_level in [OptimizationLevel.ADVANCED, OptimizationLevel.PREMIUM]:
            optimizations.append("edge_caching")
            optimizations.append("stale_while_revalidate")
            size_reduction += 0.1
        
        return {
            "optimizations_applied": optimizations,
            "size_reduction": size_reduction
        }
    
    async def _select_optimal_nodes(self, content_url: str, content_type: ContentType) -> List[CDNNode]:
        """Select optimal CDN nodes for content distribution"""
        # Simulate node selection
        await asyncio.sleep(0.1)
        
        # Filter active nodes
        active_nodes = [node for node in self.cdn_nodes.values() if node.status == "active"]
        
        # Sort by latency and load
        optimal_nodes = sorted(active_nodes, key=lambda x: (x.latency, x.current_load))[:5]
        
        return optimal_nodes
    
    async def _distribute_to_nodes(self, optimized_content: Dict, nodes: List[CDNNode]) -> Dict:
        """Distribute content to selected nodes"""
        # Simulate content distribution
        await asyncio.sleep(1.0)
        
        distribution_results = []
        for node in nodes:
            # Update node load
            node.current_load += 0.1
            node.last_updated = datetime.now()
            
            distribution_results.append({
                "node_id": node.id,
                "node_name": node.name,
                "location": node.location,
                "distribution_time": 0.5,
                "status": "success"
            })
        
        return {
            "distribution_time": 1.0,
            "nodes_updated": len(nodes),
            "distribution_results": distribution_results
        }
    
    async def _create_cache_entries(self, optimized_content: Dict, nodes: List[CDNNode]) -> List[str]:
        """Create cache entries for distributed content"""
        cache_entries = []
        
        for node in nodes:
            cache_id = str(uuid.uuid4())
            cache_entry = ContentCache(
                id=cache_id,
                content_url=optimized_content["optimized_url"],
                content_type=ContentType(optimized_content["content_type"]),
                size=1000,  # Mock size
                cache_key=hashlib.md5(optimized_content["optimized_url"].encode()).hexdigest(),
                ttl=86400,  # 1 day
                hit_count=0,
                miss_count=0,
                last_accessed=datetime.now(),
                created_at=datetime.now()
            )
            
            self.content_caches[cache_id] = cache_entry
            cache_entries.append(cache_id)
        
        return cache_entries
    
    # 2. Cache Management
    async def get_cached_content(self, content_url: str, user_location: str) -> Dict:
        """Get cached content from nearest node"""
        try:
            # Find nearest node
            nearest_node = await self._find_nearest_node(user_location)
            
            # Check cache
            cache_hit = await self._check_cache(content_url, nearest_node)
            
            if cache_hit["found"]:
                # Update cache statistics
                cache_entry = self.content_caches[cache_hit["cache_id"]]
                cache_entry.hit_count += 1
                cache_entry.last_accessed = datetime.now()
                
                return {
                    "success": True,
                    "cache_hit": True,
                    "content_url": content_url,
                    "served_from": nearest_node.location,
                    "latency": nearest_node.latency,
                    "cache_key": cache_entry.cache_key,
                    "ttl_remaining": cache_entry.ttl
                }
            else:
                # Cache miss - fetch from origin
                origin_content = await self._fetch_from_origin(content_url)
                
                # Cache the content
                await self._cache_content(content_url, origin_content, nearest_node)
                
                return {
                    "success": True,
                    "cache_hit": False,
                    "content_url": content_url,
                    "served_from": "origin",
                    "latency": nearest_node.latency + 50,  # Higher latency for origin
                    "cached": True
                }
            
        except Exception as e:
            logger.error(f"Error getting cached content: {e}")
            return {"success": False, "error": str(e)}
    
    async def _find_nearest_node(self, user_location: str) -> CDNNode:
        """Find nearest CDN node to user location"""
        # Simulate nearest node finding
        await asyncio.sleep(0.05)
        
        # Mock location-based selection
        location_mapping = {
            "US": "New York",
            "UK": "London",
            "JP": "Tokyo",
            "AU": "Sydney",
            "BR": "São Paulo",
            "IN": "Mumbai",
            "AE": "Dubai",
            "ZA": "Cape Town"
        }
        
        target_location = location_mapping.get(user_location, "New York")
        
        # Find node with matching location
        for node in self.cdn_nodes.values():
            if target_location in node.location:
                return node
        
        # Fallback to first available node
        return list(self.cdn_nodes.values())[0]
    
    async def _check_cache(self, content_url: str, node: CDNNode) -> Dict:
        """Check if content is cached on node"""
        # Simulate cache check
        await asyncio.sleep(0.02)
        
        cache_key = hashlib.md5(content_url.encode()).hexdigest()
        
        # Find matching cache entry
        for cache_id, cache_entry in self.content_caches.items():
            if cache_entry.cache_key == cache_key:
                # Check if cache is still valid
                if datetime.now() - cache_entry.created_at < timedelta(seconds=cache_entry.ttl):
                    return {"found": True, "cache_id": cache_id}
                else:
                    # Cache expired
                    cache_entry.miss_count += 1
                    return {"found": False, "reason": "expired"}
        
        return {"found": False, "reason": "not_found"}
    
    async def _fetch_from_origin(self, content_url: str) -> Dict:
        """Fetch content from origin server"""
        # Simulate origin fetch
        await asyncio.sleep(0.5)
        
        return {
            "url": content_url,
            "content": "Mock content from origin",
            "size": 1000,
            "content_type": "text/html",
            "headers": {"cache-control": "max-age=3600"}
        }
    
    async def _cache_content(self, content_url: str, content: Dict, node: CDNNode) -> str:
        """Cache content on node"""
        # Simulate content caching
        await asyncio.sleep(0.1)
        
        cache_id = str(uuid.uuid4())
        cache_entry = ContentCache(
            id=cache_id,
            content_url=content_url,
            content_type=ContentType.STATIC,
            size=content["size"],
            cache_key=hashlib.md5(content_url.encode()).hexdigest(),
            ttl=3600,  # 1 hour
            hit_count=0,
            miss_count=0,
            last_accessed=datetime.now(),
            created_at=datetime.now()
        )
        
        self.content_caches[cache_id] = cache_entry
        return cache_id
    
    # 3. Cache Invalidation
    async def invalidate_cache(self, content_url: str, invalidation_type: str = "manual") -> Dict:
        """Invalidate cached content"""
        try:
            cache_key = hashlib.md5(content_url.encode()).hexdigest()
            invalidated_entries = []
            
            # Find and invalidate cache entries
            for cache_id, cache_entry in list(self.content_caches.items()):
                if cache_entry.cache_key == cache_key:
                    # Remove from cache
                    del self.content_caches[cache_id]
                    invalidated_entries.append(cache_id)
            
            return {
                "success": True,
                "content_url": content_url,
                "invalidation_type": invalidation_type,
                "invalidated_entries": len(invalidated_entries),
                "cache_entries": invalidated_entries
            }
            
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            return {"success": False, "error": str(e)}
    
    # 4. Performance Monitoring
    async def collect_performance_metrics(self, node_id: str) -> Dict:
        """Collect performance metrics from CDN node"""
        try:
            if node_id not in self.cdn_nodes:
                raise ValueError(f"Node {node_id} not found")
            
            node = self.cdn_nodes[node_id]
            
            # Simulate metrics collection
            await asyncio.sleep(0.1)
            
            # Generate mock metrics
            metrics = {
                "node_id": node_id,
                "timestamp": datetime.now().isoformat(),
                "latency": node.latency + np.random.uniform(-2, 2),
                "throughput": np.random.uniform(8000, 12000),  # Mbps
                "hit_ratio": np.random.uniform(0.85, 0.95),
                "error_rate": np.random.uniform(0.001, 0.01),
                "bandwidth_usage": np.random.uniform(0.6, 0.9),
                "active_connections": np.random.randint(100, 1000),
                "cache_size": np.random.uniform(0.7, 0.95)
            }
            
            # Update node metrics
            node.current_load = metrics["bandwidth_usage"]
            node.last_updated = datetime.now()
            
            # Store metrics
            if node_id not in self.performance_metrics:
                self.performance_metrics[node_id] = []
            
            self.performance_metrics[node_id].append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.performance_metrics[node_id]) > 1000:
                self.performance_metrics[node_id] = self.performance_metrics[node_id][-1000:]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
            return {"error": str(e)}
    
    # 5. Global CDN Analytics
    async def get_global_cdn_analytics(self) -> Dict:
        """Get comprehensive global CDN analytics"""
        try:
            analytics = {
                "total_nodes": len(self.cdn_nodes),
                "active_nodes": len([n for n in self.cdn_nodes.values() if n.status == "active"]),
                "total_cache_entries": len(self.content_caches),
                "global_coverage": self._get_global_coverage(),
                "performance_summary": self._get_performance_summary(),
                "cache_statistics": self._get_cache_statistics(),
                "bandwidth_usage": self._get_bandwidth_usage(),
                "cost_analysis": self._get_cost_analysis(),
                "optimization_impact": self._get_optimization_impact()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting global CDN analytics: {e}")
            return {"error": str(e)}
    
    def _get_global_coverage(self) -> Dict:
        """Get global coverage statistics"""
        regions = {}
        countries = {}
        
        for node in self.cdn_nodes.values():
            region = node.region
            country = node.country
            
            regions[region] = regions.get(region, 0) + 1
            countries[country] = countries.get(country, 0) + 1
        
        return {
            "regions_covered": len(regions),
            "countries_covered": len(countries),
            "regions": regions,
            "countries": countries,
            "global_presence": "95%"
        }
    
    def _get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_metrics:
            return {"average_latency": 0, "average_throughput": 0, "average_hit_ratio": 0}
        
        all_metrics = []
        for node_metrics in self.performance_metrics.values():
            all_metrics.extend(node_metrics)
        
        if not all_metrics:
            return {"average_latency": 0, "average_throughput": 0, "average_hit_ratio": 0}
        
        return {
            "average_latency": np.mean([m["latency"] for m in all_metrics]),
            "average_throughput": np.mean([m["throughput"] for m in all_metrics]),
            "average_hit_ratio": np.mean([m["hit_ratio"] for m in all_metrics]),
            "average_error_rate": np.mean([m["error_rate"] for m in all_metrics])
        }
    
    def _get_cache_statistics(self) -> Dict:
        """Get cache statistics"""
        if not self.content_caches:
            return {"total_entries": 0, "total_hits": 0, "total_misses": 0}
        
        total_hits = sum(cache.hit_count for cache in self.content_caches.values())
        total_misses = sum(cache.miss_count for cache in self.content_caches.values())
        total_requests = total_hits + total_misses
        
        return {
            "total_entries": len(self.content_caches),
            "total_hits": total_hits,
            "total_misses": total_misses,
            "hit_ratio": total_hits / total_requests if total_requests > 0 else 0,
            "average_ttl": np.mean([cache.ttl for cache in self.content_caches.values()])
        }
    
    def _get_bandwidth_usage(self) -> Dict:
        """Get bandwidth usage statistics"""
        total_bandwidth = sum(node.bandwidth for node in self.cdn_nodes.values())
        used_bandwidth = sum(node.bandwidth * node.current_load for node in self.cdn_nodes.values())
        
        return {
            "total_bandwidth": total_bandwidth,
            "used_bandwidth": used_bandwidth,
            "utilization_percentage": (used_bandwidth / total_bandwidth) * 100 if total_bandwidth > 0 else 0,
            "available_bandwidth": total_bandwidth - used_bandwidth
        }
    
    def _get_cost_analysis(self) -> Dict:
        """Get cost analysis"""
        return {
            "monthly_cost": 5000,  # USD
            "cost_per_gb": 0.05,  # USD
            "cost_per_request": 0.001,  # USD
            "savings_from_optimization": 1200,  # USD
            "roi": 2.4  # Return on investment
        }
    
    def _get_optimization_impact(self) -> Dict:
        """Get optimization impact"""
        return {
            "average_size_reduction": 0.35,  # 35%
            "latency_improvement": 0.6,  # 60%
            "bandwidth_savings": 0.4,  # 40%
            "user_experience_score": 0.92,  # 92%
            "seo_impact": "positive"
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize global CDN
    global_cdn = GlobalCDN()
    
    print("🌍 Global CDN Demo")
    print("=" * 50)
    
    # Test content distribution
    print("\n1. Testing content distribution...")
    distribution_result = asyncio.run(global_cdn.distribute_content(
        "https://example.com/image.jpg",
        ContentType.IMAGE,
        OptimizationLevel.PREMIUM
    ))
    print(f"✅ Content Distributed: {distribution_result['success']}")
    if distribution_result['success']:
        print(f"   Distribution ID: {distribution_result['distribution_id']}")
        print(f"   Nodes: {distribution_result['distributed_nodes']}")
        print(f"   Estimated Latency: {distribution_result['estimated_latency']}ms")
        print(f"   Optimizations: {distribution_result['optimized_content']['optimizations_applied']}")
    
    # Test cached content retrieval
    print("\n2. Testing cached content retrieval...")
    cache_result = asyncio.run(global_cdn.get_cached_content(
        "https://example.com/image.jpg",
        "US"
    ))
    print(f"✅ Cached Content Retrieved: {cache_result['success']}")
    if cache_result['success']:
        print(f"   Cache Hit: {cache_result['cache_hit']}")
        print(f"   Served From: {cache_result['served_from']}")
        print(f"   Latency: {cache_result['latency']}ms")
    
    # Test cache invalidation
    print("\n3. Testing cache invalidation...")
    invalidation_result = asyncio.run(global_cdn.invalidate_cache(
        "https://example.com/image.jpg",
        "manual"
    ))
    print(f"✅ Cache Invalidated: {invalidation_result['success']}")
    if invalidation_result['success']:
        print(f"   Invalidated Entries: {invalidation_result['invalidated_entries']}")
    
    # Test performance metrics collection
    print("\n4. Testing performance metrics collection...")
    node_id = list(global_cdn.cdn_nodes.keys())[0]
    metrics = asyncio.run(global_cdn.collect_performance_metrics(node_id))
    print(f"✅ Performance Metrics Collected")
    print(f"   Node: {metrics['node_id']}")
    print(f"   Latency: {metrics['latency']:.2f}ms")
    print(f"   Throughput: {metrics['throughput']:.0f} Mbps")
    print(f"   Hit Ratio: {metrics['hit_ratio']:.2%}")
    print(f"   Error Rate: {metrics['error_rate']:.3%}")
    
    # Test global CDN analytics
    print("\n5. Testing global CDN analytics...")
    analytics = asyncio.run(global_cdn.get_global_cdn_analytics())
    print(f"✅ Global CDN Analytics Generated")
    print(f"   Total Nodes: {analytics['total_nodes']}")
    print(f"   Active Nodes: {analytics['active_nodes']}")
    print(f"   Cache Entries: {analytics['total_cache_entries']}")
    print(f"   Global Coverage: {analytics['global_coverage']['global_presence']}")
    print(f"   Average Latency: {analytics['performance_summary']['average_latency']:.2f}ms")
    print(f"   Hit Ratio: {analytics['cache_statistics']['hit_ratio']:.2%}")
    print(f"   Bandwidth Utilization: {analytics['bandwidth_usage']['utilization_percentage']:.1f}%")
    
    print("\n🎉 Global CDN Demo completed!")
    print("=" * 50)
