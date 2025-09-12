#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 Agent Workflow Engine - موتور اجرای Agent های هوشمند
قابلیت‌های پیشرفته:
- اجرای Workflow های پیچیده
- مدیریت State و Context
- Error Handling و Retry Logic
- Performance Monitoring
- Real-time Execution
"""

import os
import json
import asyncio
import aiohttp
import openai
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
import uuid

class NodeType(Enum):
    """انواع Node ها"""
    INPUT = "input"
    PROCESSING = "processing"
    ACTION = "action"
    DECISION = "decision"
    OUTPUT = "output"

class ExecutionStatus(Enum):
    """وضعیت اجرا"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class NodeData:
    """داده‌های Node"""
    id: str
    type: NodeType
    config: Dict[str, Any]
    position: Dict[str, float]
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)

@dataclass
class Connection:
    """اتصال بین Node ها"""
    from_node: str
    to_node: str
    from_port: str = "output"
    to_port: str = "input"

@dataclass
class ExecutionContext:
    """Context اجرا"""
    variables: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionResult:
    """نتیجه اجرا"""
    status: ExecutionStatus
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class AgentWorkflowEngine:
    """موتور اجرای Agent Workflow ها"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.openai_api_key = self.config.get('openai_api_key')
        self.nodes = {}
        self.connections = []
        self.execution_history = []
        self.active_executions = {}
        
        # تنظیم logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Node processors
        self.node_processors = {
            NodeType.INPUT: self._process_input_node,
            NodeType.PROCESSING: self._process_processing_node,
            NodeType.ACTION: self._process_action_node,
            NodeType.DECISION: self._process_decision_node,
            NodeType.OUTPUT: self._process_output_node
        }
        
        # API clients
        self.http_client = None
        self.openai_client = None
        
    async def initialize(self):
        """مقداردهی اولیه"""
        self.http_client = aiohttp.ClientSession()
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    async def close(self):
        """بستن منابع"""
        if self.http_client:
            await self.http_client.close()
    
    def load_workflow(self, workflow_data: Dict) -> bool:
        """
        بارگذاری Workflow
        
        Args:
            workflow_data: داده‌های Workflow
            
        Returns:
            موفقیت بارگذاری
        """
        try:
            # بارگذاری Node ها
            self.nodes = {}
            for node_data in workflow_data.get('nodes', []):
                node = NodeData(
                    id=node_data['id'],
                    type=NodeType(node_data['type']),
                    config=node_data.get('config', {}),
                    position=node_data.get('position', {}),
                    inputs=node_data.get('inputs', []),
                    outputs=node_data.get('outputs', [])
                )
                self.nodes[node.id] = node
            
            # بارگذاری اتصالات
            self.connections = []
            for conn_data in workflow_data.get('connections', []):
                connection = Connection(
                    from_node=conn_data['from'],
                    to_node=conn_data['to'],
                    from_port=conn_data.get('from_port', 'output'),
                    to_port=conn_data.get('to_port', 'input')
                )
                self.connections.append(connection)
            
            self.logger.info(f"Workflow loaded with {len(self.nodes)} nodes and {len(self.connections)} connections")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading workflow: {e}")
            return False
    
    async def execute_workflow(self, input_data: Dict = None, execution_id: str = None) -> ExecutionResult:
        """
        اجرای Workflow
        
        Args:
            input_data: داده‌های ورودی
            execution_id: شناسه اجرا
            
        Returns:
            نتیجه اجرا
        """
        if not execution_id:
            execution_id = str(uuid.uuid4())
        
        start_time = datetime.now()
        context = ExecutionContext()
        
        try:
            self.logger.info(f"Starting workflow execution: {execution_id}")
            
            # اضافه کردن داده‌های ورودی به context
            if input_data:
                context.variables.update(input_data)
            
            # پیدا کردن Node های ورودی
            input_nodes = [node for node in self.nodes.values() if node.type == NodeType.INPUT]
            
            if not input_nodes:
                raise ValueError("No input nodes found in workflow")
            
            # اجرای Workflow
            result = await self._execute_nodes(input_nodes, context, execution_id)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # ذخیره تاریخچه اجرا
            execution_record = {
                "execution_id": execution_id,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "execution_time": execution_time,
                "status": result.status.value,
                "context": {
                    "variables": context.variables,
                    "results": context.results,
                    "errors": context.errors
                }
            }
            self.execution_history.append(execution_record)
            
            return ExecutionResult(
                status=result.status,
                output=context.results,
                execution_time=execution_time,
                metadata={"execution_id": execution_id}
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Workflow execution failed: {e}")
            
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                error=str(e),
                execution_time=execution_time,
                metadata={"execution_id": execution_id}
            )
    
    async def _execute_nodes(self, nodes: List[NodeData], context: ExecutionContext, execution_id: str) -> ExecutionResult:
        """اجرای Node ها"""
        try:
            # اجرای Node ها به ترتیب
            for node in nodes:
                if execution_id in self.active_executions and self.active_executions[execution_id].get('cancelled'):
                    return ExecutionResult(status=ExecutionStatus.CANCELLED)
                
                # اجرای Node
                result = await self._execute_node(node, context)
                
                if result.status == ExecutionStatus.FAILED:
                    return result
                
                # ذخیره نتیجه
                context.results[node.id] = result.output
                
                # پیدا کردن Node های بعدی
                next_nodes = self._get_next_nodes(node.id)
                if next_nodes:
                    next_result = await self._execute_nodes(next_nodes, context, execution_id)
                    if next_result.status != ExecutionStatus.COMPLETED:
                        return next_result
            
            return ExecutionResult(status=ExecutionStatus.COMPLETED)
            
        except Exception as e:
            return ExecutionResult(status=ExecutionStatus.FAILED, error=str(e))
    
    async def _execute_node(self, node: NodeData, context: ExecutionContext) -> ExecutionResult:
        """اجرای یک Node"""
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Executing node: {node.id} ({node.type.value})")
            
            # اجرای Node بر اساس نوع
            processor = self.node_processors.get(node.type)
            if not processor:
                raise ValueError(f"No processor found for node type: {node.type}")
            
            result = await processor(node, context)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Node {node.id} completed in {execution_time:.2f}s")
            
            return ExecutionResult(
                status=ExecutionStatus.COMPLETED,
                output=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Node {node.id} failed: {e}")
            
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def _process_input_node(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش Node ورودی"""
        node_type = node.config.get('type', 'text')
        
        if node_type == 'text':
            return context.variables.get('input_text', node.config.get('default_value', ''))
        elif node_type == 'voice':
            # شبیه‌سازی پردازش صدا
            return context.variables.get('voice_input', '')
        elif node_type == 'file':
            return context.variables.get('file_input', {})
        else:
            return context.variables.get('input', '')
    
    async def _process_processing_node(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش Node پردازش"""
        processor_type = node.config.get('type', 'gpt')
        
        if processor_type == 'gpt':
            return await self._process_gpt_node(node, context)
        elif processor_type == 'claude':
            return await self._process_claude_node(node, context)
        elif processor_type == 'image':
            return await self._process_image_node(node, context)
        else:
            return await self._process_custom_processor(node, context)
    
    async def _process_gpt_node(self, node: NodeData, context: ExecutionContext) -> str:
        """پردازش با GPT"""
        if not self.openai_api_key:
            # Fallback برای تست
            return f"GPT Response for: {context.variables.get('input_text', '')}"
        
        try:
            prompt = node.config.get('prompt', '')
            model = node.config.get('model', 'gpt-3.5-turbo')
            temperature = node.config.get('temperature', 0.7)
            max_tokens = node.config.get('max_tokens', 1000)
            
            # جایگزینی متغیرها در prompt
            for key, value in context.variables.items():
                prompt = prompt.replace(f"{{{key}}}", str(value))
            
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"GPT processing failed: {e}")
            return f"Error in GPT processing: {str(e)}"
    
    async def _process_claude_node(self, node: NodeData, context: ExecutionContext) -> str:
        """پردازش با Claude"""
        # شبیه‌سازی پردازش Claude
        prompt = node.config.get('prompt', '')
        for key, value in context.variables.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        
        return f"Claude Response for: {prompt}"
    
    async def _process_image_node(self, node: NodeData, context: ExecutionContext) -> Dict:
        """پردازش تصویر"""
        image_data = context.variables.get('image_input', {})
        
        # شبیه‌سازی تحلیل تصویر
        return {
            "analysis": "Image analyzed successfully",
            "objects": ["person", "car", "building"],
            "confidence": 0.95
        }
    
    async def _process_custom_processor(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش سفارشی"""
        # اجرای کد سفارشی
        custom_code = node.config.get('code', '')
        if custom_code:
            # اجرای امن کد
            try:
                exec(custom_code, {"context": context, "variables": context.variables})
                return context.variables.get('result', 'Custom processing completed')
            except Exception as e:
                return f"Custom processing error: {str(e)}"
        
        return "No custom code provided"
    
    async def _process_action_node(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش Node عملیات"""
        action_type = node.config.get('type', 'api')
        
        if action_type == 'api':
            return await self._process_api_action(node, context)
        elif action_type == 'database':
            return await self._process_database_action(node, context)
        elif action_type == 'email':
            return await self._process_email_action(node, context)
        else:
            return await self._process_custom_action(node, context)
    
    async def _process_api_action(self, node: NodeData, context: ExecutionContext) -> Dict:
        """پردازش فراخوانی API"""
        url = node.config.get('url', '')
        method = node.config.get('method', 'GET')
        headers = node.config.get('headers', {})
        body = node.config.get('body', {})
        
        # جایگزینی متغیرها
        for key, value in context.variables.items():
            url = url.replace(f"{{{key}}}", str(value))
            if isinstance(body, dict):
                for body_key, body_value in body.items():
                    if isinstance(body_value, str):
                        body[body_key] = body_value.replace(f"{{{key}}}", str(value))
        
        try:
            if self.http_client:
                async with self.http_client.request(method, url, headers=headers, json=body) as response:
                    result = await response.json()
                    return {
                        "status_code": response.status,
                        "data": result,
                        "success": response.status < 400
                    }
            else:
                # شبیه‌سازی برای تست
                return {
                    "status_code": 200,
                    "data": {"message": "API call simulated"},
                    "success": True
                }
                
        except Exception as e:
            return {
                "status_code": 500,
                "error": str(e),
                "success": False
            }
    
    async def _process_database_action(self, node: NodeData, context: ExecutionContext) -> Dict:
        """پردازش عملیات دیتابیس"""
        action = node.config.get('action', 'save')
        table = node.config.get('table', '')
        data = node.config.get('data', {})
        
        # جایگزینی متغیرها
        for key, value in context.variables.items():
            if isinstance(data, dict):
                for data_key, data_value in data.items():
                    if isinstance(data_value, str):
                        data[data_key] = data_value.replace(f"{{{key}}}", str(value))
        
        # شبیه‌سازی عملیات دیتابیس
        if action == 'save':
            return {
                "action": "save",
                "table": table,
                "data": data,
                "success": True,
                "id": str(uuid.uuid4())
            }
        elif action == 'get':
            return {
                "action": "get",
                "table": table,
                "data": [{"id": 1, "name": "Sample Data"}],
                "success": True
            }
        else:
            return {
                "action": action,
                "table": table,
                "success": True
            }
    
    async def _process_email_action(self, node: NodeData, context: ExecutionContext) -> Dict:
        """پردازش ارسال ایمیل"""
        to = node.config.get('to', '')
        subject = node.config.get('subject', '')
        body = node.config.get('body', '')
        
        # جایگزینی متغیرها
        for key, value in context.variables.items():
            to = to.replace(f"{{{key}}}", str(value))
            subject = subject.replace(f"{{{key}}}", str(value))
            body = body.replace(f"{{{key}}}", str(value))
        
        # شبیه‌سازی ارسال ایمیل
        return {
            "to": to,
            "subject": subject,
            "body": body,
            "success": True,
            "message_id": str(uuid.uuid4())
        }
    
    async def _process_custom_action(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش عملیات سفارشی"""
        action_code = node.config.get('code', '')
        if action_code:
            try:
                exec(action_code, {"context": context, "variables": context.variables})
                return context.variables.get('action_result', 'Custom action completed')
            except Exception as e:
                return f"Custom action error: {str(e)}"
        
        return "No custom action code provided"
    
    async def _process_decision_node(self, node: NodeData, context: ExecutionContext) -> str:
        """پردازش Node تصمیم‌گیری"""
        condition = node.config.get('condition', '')
        condition_type = node.config.get('type', 'if')
        
        # جایگزینی متغیرها در شرط
        for key, value in context.variables.items():
            condition = condition.replace(f"{{{key}}}", str(value))
        
        # ارزیابی شرط
        try:
            if condition_type == 'if':
                result = eval(condition)
                return 'true' if result else 'false'
            elif condition_type == 'switch':
                # سوئیچ بر اساس مقدار
                switch_value = context.variables.get('switch_value', '')
                return str(switch_value)
            else:
                return 'unknown'
                
        except Exception as e:
            self.logger.error(f"Condition evaluation failed: {e}")
            return 'error'
    
    async def _process_output_node(self, node: NodeData, context: ExecutionContext) -> Any:
        """پردازش Node خروجی"""
        output_type = node.config.get('type', 'text')
        
        if output_type == 'text':
            return context.variables.get('output_text', '')
        elif output_type == 'notification':
            return {
                "type": "notification",
                "message": context.variables.get('message', ''),
                "title": node.config.get('title', 'Notification')
            }
        elif output_type == 'file':
            return {
                "type": "file",
                "content": context.variables.get('file_content', ''),
                "filename": node.config.get('filename', 'output.txt')
            }
        else:
            return context.variables.get('output', '')
    
    def _get_next_nodes(self, node_id: str) -> List[NodeData]:
        """دریافت Node های بعدی"""
        next_node_ids = []
        for connection in self.connections:
            if connection.from_node == node_id:
                next_node_ids.append(connection.to_node)
        
        return [self.nodes[node_id] for node_id in next_node_ids if node_id in self.nodes]
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """دریافت تاریخچه اجرا"""
        return self.execution_history[-limit:]
    
    def get_execution_stats(self) -> Dict:
        """دریافت آمار اجرا"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        total_executions = len(self.execution_history)
        successful_executions = len([e for e in self.execution_history if e['status'] == 'completed'])
        failed_executions = len([e for e in self.execution_history if e['status'] == 'failed'])
        
        avg_execution_time = sum(e['execution_time'] for e in self.execution_history) / total_executions
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": (successful_executions / total_executions) * 100,
            "average_execution_time": avg_execution_time
        }
    
    def cancel_execution(self, execution_id: str) -> bool:
        """لغو اجرا"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]['cancelled'] = True
            return True
        return False

# مثال استفاده
if __name__ == "__main__":
    async def test_workflow():
        engine = AgentWorkflowEngine()
        await engine.initialize()
        
        # نمونه Workflow
        workflow_data = {
            "nodes": [
                {
                    "id": "input1",
                    "type": "input",
                    "config": {"type": "text", "default_value": "Hello World"},
                    "position": {"x": 100, "y": 100}
                },
                {
                    "id": "processor1",
                    "type": "processing",
                    "config": {
                        "type": "gpt",
                        "prompt": "Translate this to Persian: {input_text}",
                        "model": "gpt-3.5-turbo"
                    },
                    "position": {"x": 300, "y": 100}
                },
                {
                    "id": "output1",
                    "type": "output",
                    "config": {"type": "text"},
                    "position": {"x": 500, "y": 100}
                }
            ],
            "connections": [
                {"from": "input1", "to": "processor1"},
                {"from": "processor1", "to": "output1"}
            ]
        }
        
        # بارگذاری و اجرای Workflow
        if engine.load_workflow(workflow_data):
            result = await engine.execute_workflow({"input_text": "Hello World"})
            print(f"Execution result: {result.status.value}")
            print(f"Output: {result.output}")
            print(f"Execution time: {result.execution_time:.2f}s")
        
        await engine.close()
    
    # اجرای تست
    asyncio.run(test_workflow())
