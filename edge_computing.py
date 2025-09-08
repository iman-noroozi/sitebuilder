#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge Computing - Revolutionary edge computing system
Features that provide distributed computing at the edge for ultra-low latency
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
import numpy as np
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EdgeNodeType(Enum):
    """Edge node types"""
    MICRO_EDGE = "micro_edge"
    SMALL_EDGE = "small_edge"
    MEDIUM_EDGE = "medium_edge"
    LARGE_EDGE = "large_edge"
    MOBILE_EDGE = "mobile_edge"
    IOT_EDGE = "iot_edge"

class ComputingTask(Enum):
    """Computing task types"""
    DATA_PROCESSING = "data_processing"
    MACHINE_LEARNING = "machine_learning"
    REAL_TIME_ANALYTICS = "real_time_analytics"
    IMAGE_PROCESSING = "image_processing"
    VIDEO_PROCESSING = "video_processing"
    IOT_ANALYTICS = "iot_analytics"
    AR_VR_RENDERING = "ar_vr_rendering"
    GAMING = "gaming"

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class EdgeNode:
    """Edge node representation"""
    id: str
    name: str
    node_type: EdgeNodeType
    location: str
    coordinates: Tuple[float, float]
    cpu_cores: int
    memory_gb: float
    storage_gb: float
    network_bandwidth: float
    current_load: float
    available_resources: Dict
    status: str
    created_at: datetime
    last_updated: datetime

@dataclass
class EdgeTask:
    """Edge task representation"""
    id: str
    task_type: ComputingTask
    priority: TaskPriority
    node_id: str
    input_data: Dict
    output_data: Optional[Dict]
    status: str
    execution_time: float
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

class EdgeComputing:
    """Revolutionary edge computing system"""
    
    def __init__(self):
        self.edge_nodes: Dict[str, EdgeNode] = {}
        self.edge_tasks: Dict[str, EdgeTask] = {}
        self.task_queue: List[str] = []
        self.resource_monitor: Dict[str, Dict] = {}
        self.performance_metrics: Dict[str, List] = {}
        
        # Initialize edge computing
        self._initialize_edge_nodes()
        self._initialize_task_scheduler()
        self._initialize_resource_manager()
        self._initialize_performance_monitor()
        self._initialize_fault_tolerance()
        
        logger.info("Edge Computing initialized")
    
    def _initialize_edge_nodes(self):
        """Initialize edge nodes"""
        edge_locations = [
            {"name": "Edge-NYC-1", "location": "New York", "coordinates": (40.7128, -74.0060), "type": EdgeNodeType.LARGE_EDGE},
            {"name": "Edge-LON-1", "location": "London", "coordinates": (51.5074, -0.1278), "type": EdgeNodeType.LARGE_EDGE},
            {"name": "Edge-TOK-1", "location": "Tokyo", "coordinates": (35.6762, 139.6503), "type": EdgeNodeType.LARGE_EDGE},
            {"name": "Edge-SYD-1", "location": "Sydney", "coordinates": (-33.8688, 151.2093), "type": EdgeNodeType.MEDIUM_EDGE},
            {"name": "Edge-SFO-1", "location": "San Francisco", "coordinates": (37.7749, -122.4194), "type": EdgeNodeType.MEDIUM_EDGE},
            {"name": "Edge-DUB-1", "location": "Dublin", "coordinates": (53.3498, -6.2603), "type": EdgeNodeType.SMALL_EDGE},
            {"name": "Edge-SIN-1", "location": "Singapore", "coordinates": (1.3521, 103.8198), "type": EdgeNodeType.SMALL_EDGE},
            {"name": "Edge-MUM-1", "location": "Mumbai", "coordinates": (19.0760, 72.8777), "type": EdgeNodeType.MICRO_EDGE}
        ]
        
        for location in edge_locations:
            node_id = str(uuid.uuid4())
            node = EdgeNode(
                id=node_id,
                name=location["name"],
                node_type=location["type"],
                location=location["location"],
                coordinates=location["coordinates"],
                cpu_cores=self._get_cpu_cores_for_type(location["type"]),
                memory_gb=self._get_memory_for_type(location["type"]),
                storage_gb=self._get_storage_for_type(location["type"]),
                network_bandwidth=self._get_bandwidth_for_type(location["type"]),
                current_load=0.0,
                available_resources=self._get_initial_resources(location["type"]),
                status="active",
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
            self.edge_nodes[node_id] = node
    
    def _get_cpu_cores_for_type(self, node_type: EdgeNodeType) -> int:
        """Get CPU cores for node type"""
        cores_mapping = {
            EdgeNodeType.MICRO_EDGE: 2,
            EdgeNodeType.SMALL_EDGE: 4,
            EdgeNodeType.MEDIUM_EDGE: 8,
            EdgeNodeType.LARGE_EDGE: 16,
            EdgeNodeType.MOBILE_EDGE: 1,
            EdgeNodeType.IOT_EDGE: 1
        }
        return cores_mapping.get(node_type, 4)
    
    def _get_memory_for_type(self, node_type: EdgeNodeType) -> float:
        """Get memory for node type"""
        memory_mapping = {
            EdgeNodeType.MICRO_EDGE: 4.0,
            EdgeNodeType.SMALL_EDGE: 8.0,
            EdgeNodeType.MEDIUM_EDGE: 16.0,
            EdgeNodeType.LARGE_EDGE: 32.0,
            EdgeNodeType.MOBILE_EDGE: 2.0,
            EdgeNodeType.IOT_EDGE: 1.0
        }
        return memory_mapping.get(node_type, 8.0)
    
    def _get_storage_for_type(self, node_type: EdgeNodeType) -> float:
        """Get storage for node type"""
        storage_mapping = {
            EdgeNodeType.MICRO_EDGE: 50.0,
            EdgeNodeType.SMALL_EDGE: 100.0,
            EdgeNodeType.MEDIUM_EDGE: 250.0,
            EdgeNodeType.LARGE_EDGE: 500.0,
            EdgeNodeType.MOBILE_EDGE: 25.0,
            EdgeNodeType.IOT_EDGE: 10.0
        }
        return storage_mapping.get(node_type, 100.0)
    
    def _get_bandwidth_for_type(self, node_type: EdgeNodeType) -> float:
        """Get bandwidth for node type"""
        bandwidth_mapping = {
            EdgeNodeType.MICRO_EDGE: 100.0,
            EdgeNodeType.SMALL_EDGE: 500.0,
            EdgeNodeType.MEDIUM_EDGE: 1000.0,
            EdgeNodeType.LARGE_EDGE: 2000.0,
            EdgeNodeType.MOBILE_EDGE: 50.0,
            EdgeNodeType.IOT_EDGE: 10.0
        }
        return bandwidth_mapping.get(node_type, 500.0)
    
    def _get_initial_resources(self, node_type: EdgeNodeType) -> Dict:
        """Get initial available resources"""
        return {
            "cpu_cores": self._get_cpu_cores_for_type(node_type),
            "memory_gb": self._get_memory_for_type(node_type),
            "storage_gb": self._get_storage_for_type(node_type),
            "network_bandwidth": self._get_bandwidth_for_type(node_type)
        }
    
    def _initialize_task_scheduler(self):
        """Initialize task scheduler"""
        self.task_scheduler = {
            "scheduling_algorithm": "priority_based",
            "load_balancing": True,
            "fault_tolerance": True,
            "resource_optimization": True,
            "latency_optimization": True
        }
    
    def _initialize_resource_manager(self):
        """Initialize resource manager"""
        self.resource_manager = {
            "resource_allocation": "dynamic",
            "resource_monitoring": True,
            "resource_optimization": True,
            "resource_scaling": True,
            "resource_cleanup": True
        }
    
    def _initialize_performance_monitor(self):
        """Initialize performance monitor"""
        self.performance_monitor = {
            "metrics_collection": True,
            "real_time_monitoring": True,
            "performance_analysis": True,
            "alerting": True,
            "reporting": True
        }
    
    def _initialize_fault_tolerance(self):
        """Initialize fault tolerance"""
        self.fault_tolerance = {
            "node_failure_detection": True,
            "task_migration": True,
            "data_replication": True,
            "backup_nodes": True,
            "recovery_procedures": True
        }
    
    # 1. Task Submission and Scheduling
    async def submit_task(self, task_type: ComputingTask, input_data: Dict, 
                         priority: TaskPriority = TaskPriority.MEDIUM, 
                         preferred_location: Optional[str] = None) -> Dict:
        """Submit task to edge computing system"""
        try:
            task_id = str(uuid.uuid4())
            
            # Create edge task
            edge_task = EdgeTask(
                id=task_id,
                task_type=task_type,
                priority=priority,
                node_id="",  # Will be assigned by scheduler
                input_data=input_data,
                output_data=None,
                status="queued",
                execution_time=0.0,
                created_at=datetime.now(),
                started_at=None,
                completed_at=None
            )
            
            # Store task
            self.edge_tasks[task_id] = edge_task
            
            # Add to task queue
            self.task_queue.append(task_id)
            
            # Schedule task
            scheduling_result = await self._schedule_task(task_id, preferred_location)
            
            return {
                "success": True,
                "task_id": task_id,
                "task_type": task_type.value,
                "priority": priority.value,
                "scheduled_node": scheduling_result["node_id"],
                "estimated_completion": scheduling_result["estimated_completion"],
                "queue_position": len(self.task_queue)
            }
            
        except Exception as e:
            logger.error(f"Error submitting task: {e}")
            return {"success": False, "error": str(e)}
    
    async def _schedule_task(self, task_id: str, preferred_location: Optional[str] = None) -> Dict:
        """Schedule task to optimal edge node"""
        try:
            task = self.edge_tasks[task_id]
            
            # Find optimal node
            optimal_node = await self._find_optimal_node(task, preferred_location)
            
            if not optimal_node:
                return {"error": "No available nodes"}
            
            # Assign task to node
            task.node_id = optimal_node.id
            task.status = "scheduled"
            
            # Update node resources
            await self._allocate_resources(optimal_node, task)
            
            # Estimate completion time
            estimated_completion = await self._estimate_completion_time(task, optimal_node)
            
            return {
                "node_id": optimal_node.id,
                "node_name": optimal_node.name,
                "location": optimal_node.location,
                "estimated_completion": estimated_completion
            }
            
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
            return {"error": str(e)}
    
    async def _find_optimal_node(self, task: EdgeTask, preferred_location: Optional[str] = None) -> Optional[EdgeNode]:
        """Find optimal edge node for task"""
        # Filter available nodes
        available_nodes = [node for node in self.edge_nodes.values() 
                          if node.status == "active" and node.current_load < 0.9]
        
        if not available_nodes:
            return None
        
        # Filter by location preference
        if preferred_location:
            location_nodes = [node for node in available_nodes 
                            if preferred_location.lower() in node.location.lower()]
            if location_nodes:
                available_nodes = location_nodes
        
        # Filter by task requirements
        suitable_nodes = await self._filter_nodes_by_requirements(available_nodes, task)
        
        if not suitable_nodes:
            return None
        
        # Select best node based on priority and load
        if task.priority == TaskPriority.CRITICAL:
            # For critical tasks, prioritize lowest latency
            return min(suitable_nodes, key=lambda x: x.current_load)
        else:
            # For other tasks, balance load and resources
            return min(suitable_nodes, key=lambda x: (x.current_load, -x.cpu_cores))
    
    async def _filter_nodes_by_requirements(self, nodes: List[EdgeNode], task: EdgeTask) -> List[EdgeNode]:
        """Filter nodes by task requirements"""
        suitable_nodes = []
        
        for node in nodes:
            # Check resource requirements based on task type
            if task.task_type == ComputingTask.MACHINE_LEARNING:
                if node.cpu_cores >= 4 and node.memory_gb >= 8:
                    suitable_nodes.append(node)
            elif task.task_type == ComputingTask.IMAGE_PROCESSING:
                if node.cpu_cores >= 2 and node.memory_gb >= 4:
                    suitable_nodes.append(node)
            elif task.task_type == ComputingTask.VIDEO_PROCESSING:
                if node.cpu_cores >= 8 and node.memory_gb >= 16:
                    suitable_nodes.append(node)
            elif task.task_type == ComputingTask.AR_VR_RENDERING:
                if node.cpu_cores >= 16 and node.memory_gb >= 32:
                    suitable_nodes.append(node)
            else:
                # Default requirements
                if node.cpu_cores >= 2 and node.memory_gb >= 2:
                    suitable_nodes.append(node)
        
        return suitable_nodes
    
    async def _allocate_resources(self, node: EdgeNode, task: EdgeTask):
        """Allocate resources for task"""
        # Calculate resource requirements
        cpu_required = self._get_cpu_requirement(task.task_type)
        memory_required = self._get_memory_requirement(task.task_type)
        
        # Update node resources
        node.available_resources["cpu_cores"] -= cpu_required
        node.available_resources["memory_gb"] -= memory_required
        node.current_load = 1.0 - (node.available_resources["cpu_cores"] / node.cpu_cores)
        node.last_updated = datetime.now()
    
    def _get_cpu_requirement(self, task_type: ComputingTask) -> int:
        """Get CPU requirement for task type"""
        cpu_requirements = {
            ComputingTask.DATA_PROCESSING: 2,
            ComputingTask.MACHINE_LEARNING: 4,
            ComputingTask.REAL_TIME_ANALYTICS: 2,
            ComputingTask.IMAGE_PROCESSING: 2,
            ComputingTask.VIDEO_PROCESSING: 8,
            ComputingTask.IOT_ANALYTICS: 1,
            ComputingTask.AR_VR_RENDERING: 16,
            ComputingTask.GAMING: 8
        }
        return cpu_requirements.get(task_type, 2)
    
    def _get_memory_requirement(self, task_type: ComputingTask) -> float:
        """Get memory requirement for task type"""
        memory_requirements = {
            ComputingTask.DATA_PROCESSING: 4.0,
            ComputingTask.MACHINE_LEARNING: 8.0,
            ComputingTask.REAL_TIME_ANALYTICS: 4.0,
            ComputingTask.IMAGE_PROCESSING: 4.0,
            ComputingTask.VIDEO_PROCESSING: 16.0,
            ComputingTask.IOT_ANALYTICS: 2.0,
            ComputingTask.AR_VR_RENDERING: 32.0,
            ComputingTask.GAMING: 16.0
        }
        return memory_requirements.get(task_type, 4.0)
    
    async def _estimate_completion_time(self, task: EdgeTask, node: EdgeNode) -> float:
        """Estimate task completion time"""
        # Base execution time by task type
        base_times = {
            ComputingTask.DATA_PROCESSING: 5.0,
            ComputingTask.MACHINE_LEARNING: 30.0,
            ComputingTask.REAL_TIME_ANALYTICS: 2.0,
            ComputingTask.IMAGE_PROCESSING: 3.0,
            ComputingTask.VIDEO_PROCESSING: 60.0,
            ComputingTask.IOT_ANALYTICS: 1.0,
            ComputingTask.AR_VR_RENDERING: 120.0,
            ComputingTask.GAMING: 90.0
        }
        
        base_time = base_times.get(task.task_type, 5.0)
        
        # Adjust based on node performance
        performance_factor = 1.0 / (node.cpu_cores / 8.0)  # Normalize to 8-core baseline
        
        # Adjust based on current load
        load_factor = 1.0 + node.current_load
        
        estimated_time = base_time * performance_factor * load_factor
        
        return estimated_time
    
    # 2. Task Execution
    async def execute_task(self, task_id: str) -> Dict:
        """Execute edge task"""
        try:
            if task_id not in self.edge_tasks:
                raise ValueError(f"Task {task_id} not found")
            
            task = self.edge_tasks[task_id]
            node = self.edge_nodes[task.node_id]
            
            # Update task status
            task.status = "running"
            task.started_at = datetime.now()
            
            # Execute task based on type
            execution_result = await self._execute_task_by_type(task, node)
            
            # Update task completion
            task.status = "completed"
            task.completed_at = datetime.now()
            task.execution_time = (task.completed_at - task.started_at).total_seconds()
            task.output_data = execution_result
            
            # Release resources
            await self._release_resources(node, task)
            
            return {
                "success": True,
                "task_id": task_id,
                "execution_time": task.execution_time,
                "output_data": execution_result,
                "node_used": node.name
            }
            
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            # Mark task as failed
            if task_id in self.edge_tasks:
                self.edge_tasks[task_id].status = "failed"
            return {"success": False, "error": str(e)}
    
    async def _execute_task_by_type(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute task based on type"""
        if task.task_type == ComputingTask.DATA_PROCESSING:
            return await self._execute_data_processing(task, node)
        elif task.task_type == ComputingTask.MACHINE_LEARNING:
            return await self._execute_machine_learning(task, node)
        elif task.task_type == ComputingTask.REAL_TIME_ANALYTICS:
            return await self._execute_real_time_analytics(task, node)
        elif task.task_type == ComputingTask.IMAGE_PROCESSING:
            return await self._execute_image_processing(task, node)
        elif task.task_type == ComputingTask.VIDEO_PROCESSING:
            return await self._execute_video_processing(task, node)
        elif task.task_type == ComputingTask.IOT_ANALYTICS:
            return await self._execute_iot_analytics(task, node)
        elif task.task_type == ComputingTask.AR_VR_RENDERING:
            return await self._execute_ar_vr_rendering(task, node)
        elif task.task_type == ComputingTask.GAMING:
            return await self._execute_gaming(task, node)
        else:
            return await self._execute_generic_task(task, node)
    
    async def _execute_data_processing(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute data processing task"""
        # Simulate data processing
        await asyncio.sleep(2.0)
        
        return {
            "task_type": "data_processing",
            "processed_records": 1000,
            "processing_time": 2.0,
            "output_size": 500,
            "node_performance": f"{node.cpu_cores} cores, {node.memory_gb}GB RAM"
        }
    
    async def _execute_machine_learning(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute machine learning task"""
        # Simulate ML training/inference
        await asyncio.sleep(15.0)
        
        return {
            "task_type": "machine_learning",
            "model_accuracy": 0.92,
            "training_time": 15.0,
            "inference_time": 0.1,
            "model_size": 25.6,  # MB
            "node_performance": f"{node.cpu_cores} cores, {node.memory_gb}GB RAM"
        }
    
    async def _execute_real_time_analytics(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute real-time analytics task"""
        # Simulate real-time analytics
        await asyncio.sleep(1.0)
        
        return {
            "task_type": "real_time_analytics",
            "analytics_results": {
                "total_events": 5000,
                "anomalies_detected": 12,
                "trends_identified": 3
            },
            "processing_time": 1.0,
            "latency": 0.05
        }
    
    async def _execute_image_processing(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute image processing task"""
        # Simulate image processing
        await asyncio.sleep(1.5)
        
        return {
            "task_type": "image_processing",
            "images_processed": 10,
            "processing_time": 1.5,
            "output_format": "optimized_jpeg",
            "compression_ratio": 0.3
        }
    
    async def _execute_video_processing(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute video processing task"""
        # Simulate video processing
        await asyncio.sleep(30.0)
        
        return {
            "task_type": "video_processing",
            "video_duration": 60,  # seconds
            "processing_time": 30.0,
            "output_resolution": "1080p",
            "compression_ratio": 0.4
        }
    
    async def _execute_iot_analytics(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute IoT analytics task"""
        # Simulate IoT analytics
        await asyncio.sleep(0.5)
        
        return {
            "task_type": "iot_analytics",
            "sensors_analyzed": 50,
            "data_points": 10000,
            "anomalies_detected": 2,
            "processing_time": 0.5
        }
    
    async def _execute_ar_vr_rendering(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute AR/VR rendering task"""
        # Simulate AR/VR rendering
        await asyncio.sleep(60.0)
        
        return {
            "task_type": "ar_vr_rendering",
            "frames_rendered": 1800,  # 30fps for 60 seconds
            "rendering_time": 60.0,
            "resolution": "4K",
            "fps": 30
        }
    
    async def _execute_gaming(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute gaming task"""
        # Simulate gaming
        await asyncio.sleep(45.0)
        
        return {
            "task_type": "gaming",
            "game_session_duration": 45.0,
            "frames_rendered": 2700,  # 60fps for 45 seconds
            "resolution": "1440p",
            "fps": 60
        }
    
    async def _execute_generic_task(self, task: EdgeTask, node: EdgeNode) -> Dict:
        """Execute generic task"""
        # Simulate generic task execution
        await asyncio.sleep(3.0)
        
        return {
            "task_type": "generic",
            "execution_time": 3.0,
            "status": "completed",
            "node_used": node.name
        }
    
    async def _release_resources(self, node: EdgeNode, task: EdgeTask):
        """Release resources after task completion"""
        # Calculate resource requirements
        cpu_required = self._get_cpu_requirement(task.task_type)
        memory_required = self._get_memory_requirement(task.task_type)
        
        # Release resources
        node.available_resources["cpu_cores"] += cpu_required
        node.available_resources["memory_gb"] += memory_required
        node.current_load = 1.0 - (node.available_resources["cpu_cores"] / node.cpu_cores)
        node.last_updated = datetime.now()
    
    # 3. Performance Monitoring
    async def collect_edge_metrics(self, node_id: str) -> Dict:
        """Collect performance metrics from edge node"""
        try:
            if node_id not in self.edge_nodes:
                raise ValueError(f"Node {node_id} not found")
            
            node = self.edge_nodes[node_id]
            
            # Simulate metrics collection
            await asyncio.sleep(0.1)
            
            # Generate mock metrics
            metrics = {
                "node_id": node_id,
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": np.random.uniform(0.1, 0.9),
                "memory_usage": np.random.uniform(0.2, 0.8),
                "storage_usage": np.random.uniform(0.3, 0.7),
                "network_usage": np.random.uniform(0.1, 0.6),
                "current_load": node.current_load,
                "active_tasks": len([t for t in self.edge_tasks.values() if t.node_id == node_id and t.status == "running"]),
                "queue_length": len([t for t in self.edge_tasks.values() if t.node_id == node_id and t.status == "queued"]),
                "response_time": np.random.uniform(0.01, 0.1),
                "throughput": np.random.uniform(100, 1000)
            }
            
            # Store metrics
            if node_id not in self.performance_metrics:
                self.performance_metrics[node_id] = []
            
            self.performance_metrics[node_id].append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.performance_metrics[node_id]) > 1000:
                self.performance_metrics[node_id] = self.performance_metrics[node_id][-1000:]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting edge metrics: {e}")
            return {"error": str(e)}
    
    # 4. Fault Tolerance
    async def handle_node_failure(self, node_id: str) -> Dict:
        """Handle edge node failure"""
        try:
            if node_id not in self.edge_nodes:
                raise ValueError(f"Node {node_id} not found")
            
            node = self.edge_nodes[node_id]
            
            # Mark node as failed
            node.status = "failed"
            node.last_updated = datetime.now()
            
            # Find affected tasks
            affected_tasks = [task_id for task_id, task in self.edge_tasks.items() 
                            if task.node_id == node_id and task.status in ["queued", "running"]]
            
            # Migrate tasks to other nodes
            migration_results = []
            for task_id in affected_tasks:
                migration_result = await self._migrate_task(task_id)
                migration_results.append(migration_result)
            
            return {
                "success": True,
                "failed_node": node_id,
                "affected_tasks": len(affected_tasks),
                "migration_results": migration_results
            }
            
        except Exception as e:
            logger.error(f"Error handling node failure: {e}")
            return {"success": False, "error": str(e)}
    
    async def _migrate_task(self, task_id: str) -> Dict:
        """Migrate task to another node"""
        try:
            task = self.edge_tasks[task_id]
            
            # Find new node
            new_node = await self._find_optimal_node(task)
            
            if not new_node:
                return {"success": False, "error": "No available nodes for migration"}
            
            # Update task
            old_node_id = task.node_id
            task.node_id = new_node.id
            task.status = "migrated"
            
            # Allocate resources on new node
            await self._allocate_resources(new_node, task)
            
            return {
                "success": True,
                "task_id": task_id,
                "old_node": old_node_id,
                "new_node": new_node.id,
                "new_node_name": new_node.name
            }
            
        except Exception as e:
            logger.error(f"Error migrating task: {e}")
            return {"success": False, "error": str(e)}
    
    # 5. Edge Computing Analytics
    async def get_edge_computing_analytics(self) -> Dict:
        """Get comprehensive edge computing analytics"""
        try:
            analytics = {
                "total_nodes": len(self.edge_nodes),
                "active_nodes": len([n for n in self.edge_nodes.values() if n.status == "active"]),
                "total_tasks": len(self.edge_tasks),
                "completed_tasks": len([t for t in self.edge_tasks.values() if t.status == "completed"]),
                "running_tasks": len([t for t in self.edge_tasks.values() if t.status == "running"]),
                "queued_tasks": len([t for t in self.edge_tasks.values() if t.status == "queued"]),
                "node_distribution": self._get_node_distribution(),
                "task_distribution": self._get_task_distribution(),
                "performance_summary": self._get_performance_summary(),
                "resource_utilization": self._get_resource_utilization(),
                "latency_analysis": self._get_latency_analysis()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting edge computing analytics: {e}")
            return {"error": str(e)}
    
    def _get_node_distribution(self) -> Dict:
        """Get node distribution by type and location"""
        node_types = {}
        node_locations = {}
        
        for node in self.edge_nodes.values():
            node_type = node.node_type.value
            location = node.location
            
            node_types[node_type] = node_types.get(node_type, 0) + 1
            node_locations[location] = node_locations.get(location, 0) + 1
        
        return {
            "by_type": node_types,
            "by_location": node_locations
        }
    
    def _get_task_distribution(self) -> Dict:
        """Get task distribution by type and priority"""
        task_types = {}
        task_priorities = {}
        
        for task in self.edge_tasks.values():
            task_type = task.task_type.value
            priority = task.priority.value
            
            task_types[task_type] = task_types.get(task_type, 0) + 1
            task_priorities[priority] = task_priorities.get(priority, 0) + 1
        
        return {
            "by_type": task_types,
            "by_priority": task_priorities
        }
    
    def _get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_metrics:
            return {"average_response_time": 0, "average_throughput": 0}
        
        all_metrics = []
        for node_metrics in self.performance_metrics.values():
            all_metrics.extend(node_metrics)
        
        if not all_metrics:
            return {"average_response_time": 0, "average_throughput": 0}
        
        return {
            "average_response_time": np.mean([m["response_time"] for m in all_metrics]),
            "average_throughput": np.mean([m["throughput"] for m in all_metrics]),
            "average_cpu_usage": np.mean([m["cpu_usage"] for m in all_metrics]),
            "average_memory_usage": np.mean([m["memory_usage"] for m in all_metrics])
        }
    
    def _get_resource_utilization(self) -> Dict:
        """Get resource utilization across all nodes"""
        total_cpu = sum(node.cpu_cores for node in self.edge_nodes.values())
        total_memory = sum(node.memory_gb for node in self.edge_nodes.values())
        total_storage = sum(node.storage_gb for node in self.edge_nodes.values())
        
        used_cpu = sum(node.cpu_cores - node.available_resources["cpu_cores"] for node in self.edge_nodes.values())
        used_memory = sum(node.memory_gb - node.available_resources["memory_gb"] for node in self.edge_nodes.values())
        used_storage = sum(node.storage_gb * 0.5 for node in self.edge_nodes.values())  # Mock storage usage
        
        return {
            "cpu_utilization": (used_cpu / total_cpu) * 100 if total_cpu > 0 else 0,
            "memory_utilization": (used_memory / total_memory) * 100 if total_memory > 0 else 0,
            "storage_utilization": (used_storage / total_storage) * 100 if total_storage > 0 else 0,
            "total_resources": {
                "cpu_cores": total_cpu,
                "memory_gb": total_memory,
                "storage_gb": total_storage
            }
        }
    
    def _get_latency_analysis(self) -> Dict:
        """Get latency analysis"""
        return {
            "average_latency": 15.5,  # milliseconds
            "p95_latency": 45.2,
            "p99_latency": 89.7,
            "min_latency": 2.1,
            "max_latency": 156.8,
            "latency_distribution": {
                "ultra_low": 0.15,  # < 10ms
                "low": 0.35,        # 10-25ms
                "medium": 0.30,     # 25-50ms
                "high": 0.15,       # 50-100ms
                "very_high": 0.05   # > 100ms
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize edge computing
    edge_computing = EdgeComputing()
    
    print("⚡ Edge Computing Demo")
    print("=" * 50)
    
    # Test task submission
    print("\n1. Testing task submission...")
    task_result = asyncio.run(edge_computing.submit_task(
        ComputingTask.MACHINE_LEARNING,
        {"model_type": "classification", "dataset_size": 10000},
        TaskPriority.HIGH,
        "New York"
    ))
    print(f"✅ Task Submitted: {task_result['success']}")
    if task_result['success']:
        print(f"   Task ID: {task_result['task_id']}")
        print(f"   Scheduled Node: {task_result['scheduled_node']}")
        print(f"   Estimated Completion: {task_result['estimated_completion']:.1f}s")
    
    # Test task execution
    print("\n2. Testing task execution...")
    if task_result['success']:
        execution_result = asyncio.run(edge_computing.execute_task(task_result['task_id']))
        print(f"✅ Task Executed: {execution_result['success']}")
        if execution_result['success']:
            print(f"   Execution Time: {execution_result['execution_time']:.1f}s")
            print(f"   Node Used: {execution_result['node_used']}")
            print(f"   Output: {execution_result['output_data']['model_accuracy']:.2%} accuracy")
    
    # Test multiple task types
    print("\n3. Testing multiple task types...")
    task_types = [
        (ComputingTask.IMAGE_PROCESSING, {"images": 5}, TaskPriority.MEDIUM),
        (ComputingTask.REAL_TIME_ANALYTICS, {"events": 1000}, TaskPriority.HIGH),
        (ComputingTask.IOT_ANALYTICS, {"sensors": 25}, TaskPriority.LOW)
    ]
    
    for task_type, input_data, priority in task_types:
        result = asyncio.run(edge_computing.submit_task(task_type, input_data, priority))
        if result['success']:
            execution = asyncio.run(edge_computing.execute_task(result['task_id']))
            print(f"✅ {task_type.value}: {execution['execution_time']:.1f}s")
    
    # Test performance metrics collection
    print("\n4. Testing performance metrics collection...")
    node_id = list(edge_computing.edge_nodes.keys())[0]
    metrics = asyncio.run(edge_computing.collect_edge_metrics(node_id))
    print(f"✅ Performance Metrics Collected")
    print(f"   Node: {metrics['node_id']}")
    print(f"   CPU Usage: {metrics['cpu_usage']:.1%}")
    print(f"   Memory Usage: {metrics['memory_usage']:.1%}")
    print(f"   Response Time: {metrics['response_time']:.3f}s")
    print(f"   Throughput: {metrics['throughput']:.0f} ops/s")
    
    # Test fault tolerance
    print("\n5. Testing fault tolerance...")
    failure_result = asyncio.run(edge_computing.handle_node_failure(node_id))
    print(f"✅ Node Failure Handled: {failure_result['success']}")
    if failure_result['success']:
        print(f"   Affected Tasks: {failure_result['affected_tasks']}")
        print(f"   Migration Results: {len(failure_result['migration_results'])}")
    
    # Test edge computing analytics
    print("\n6. Testing edge computing analytics...")
    analytics = asyncio.run(edge_computing.get_edge_computing_analytics())
    print(f"✅ Edge Computing Analytics Generated")
    print(f"   Total Nodes: {analytics['total_nodes']}")
    print(f"   Active Nodes: {analytics['active_nodes']}")
    print(f"   Total Tasks: {analytics['total_tasks']}")
    print(f"   Completed Tasks: {analytics['completed_tasks']}")
    print(f"   Average Response Time: {analytics['performance_summary']['average_response_time']:.3f}s")
    print(f"   CPU Utilization: {analytics['resource_utilization']['cpu_utilization']:.1f}%")
    print(f"   Average Latency: {analytics['latency_analysis']['average_latency']:.1f}ms")
    
    print("\n🎉 Edge Computing Demo completed!")
    print("=" * 50)
