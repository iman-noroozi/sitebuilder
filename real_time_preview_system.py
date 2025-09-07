#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-Time Preview System - Live preview and collaboration
Features that enable real-time preview and collaborative editing
"""

import json
import asyncio
import websockets
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import uuid
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreviewMode(Enum):
    """Preview modes"""
    DESKTOP = "desktop"
    TABLET = "tablet"
    MOBILE = "mobile"
    CUSTOM = "custom"

class PreviewEvent(Enum):
    """Preview events"""
    CONTENT_CHANGE = "content_change"
    STYLE_CHANGE = "style_change"
    LAYOUT_CHANGE = "layout_change"
    USER_JOIN = "user_join"
    USER_LEAVE = "user_leave"
    CURSOR_MOVE = "cursor_move"
    SELECTION_CHANGE = "selection_change"
    COMMENT_ADD = "comment_add"
    COMMENT_UPDATE = "comment_update"
    COMMENT_DELETE = "comment_delete"

@dataclass
class PreviewState:
    """Preview state"""
    content: str
    styles: Dict[str, Any]
    layout: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime
    user_id: str
    version: int

@dataclass
class PreviewEvent:
    """Preview event"""
    id: str
    type: PreviewEvent
    data: Dict[str, Any]
    user_id: str
    timestamp: datetime
    version: int

class RealTimePreviewSystem:
    """Real-time preview system for collaborative editing"""
    
    def __init__(self, port: int = 8765):
        self.port = port
        self.connected_clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.preview_states: Dict[str, PreviewState] = {}
        self.event_history: Dict[str, List[PreviewEvent]] = defaultdict(list)
        self.collaborators: Dict[str, Dict[str, Any]] = {}
        self.comments: Dict[str, List[Dict]] = defaultdict(list)
        self.cursors: Dict[str, Dict[str, Any]] = {}
        self.selections: Dict[str, Dict[str, Any]] = {}
        
        # Initialize preview system
        self._initialize_preview_modes()
        self._initialize_event_handlers()
        
        logger.info(f"Real-Time Preview System initialized on port {port}")
    
    def _initialize_preview_modes(self):
        """Initialize preview modes"""
        self.preview_modes = {
            PreviewMode.DESKTOP: {
                "width": 1920,
                "height": 1080,
                "scale": 1.0,
                "device_pixel_ratio": 1.0
            },
            PreviewMode.TABLET: {
                "width": 768,
                "height": 1024,
                "scale": 0.8,
                "device_pixel_ratio": 2.0
            },
            PreviewMode.MOBILE: {
                "width": 375,
                "height": 667,
                "scale": 0.6,
                "device_pixel_ratio": 3.0
            }
        }
    
    def _initialize_event_handlers(self):
        """Initialize event handlers"""
        self.event_handlers = {
            PreviewEvent.CONTENT_CHANGE: self._handle_content_change,
            PreviewEvent.STYLE_CHANGE: self._handle_style_change,
            PreviewEvent.LAYOUT_CHANGE: self._handle_layout_change,
            PreviewEvent.USER_JOIN: self._handle_user_join,
            PreviewEvent.USER_LEAVE: self._handle_user_leave,
            PreviewEvent.CURSOR_MOVE: self._handle_cursor_move,
            PreviewEvent.SELECTION_CHANGE: self._handle_selection_change,
            PreviewEvent.COMMENT_ADD: self._handle_comment_add,
            PreviewEvent.COMMENT_UPDATE: self._handle_comment_update,
            PreviewEvent.COMMENT_DELETE: self._handle_comment_delete
        }
    
    # 1. WebSocket Server
    async def start_server(self):
        """Start WebSocket server"""
        async def handle_client(websocket, path):
            client_id = str(uuid.uuid4())
            self.connected_clients[client_id] = websocket
            
            try:
                await self._handle_client_connection(client_id, websocket)
            except websockets.exceptions.ConnectionClosed:
                await self._handle_client_disconnection(client_id)
            except Exception as e:
                logger.error(f"Error handling client {client_id}: {e}")
                await self._handle_client_disconnection(client_id)
        
        server = await websockets.serve(handle_client, "localhost", self.port)
        logger.info(f"WebSocket server started on ws://localhost:{self.port}")
        
        # Keep server running
        await server.wait_closed()
    
    async def _handle_client_connection(self, client_id: str, websocket):
        """Handle new client connection"""
        logger.info(f"Client {client_id} connected")
        
        # Send initial state
        await self._send_initial_state(client_id, websocket)
        
        # Listen for messages
        async for message in websocket:
            await self._process_message(client_id, message)
    
    async def _handle_client_disconnection(self, client_id: str):
        """Handle client disconnection"""
        logger.info(f"Client {client_id} disconnected")
        
        # Remove from connected clients
        if client_id in self.connected_clients:
            del self.connected_clients[client_id]
        
        # Remove from collaborators
        if client_id in self.collaborators:
            del self.collaborators[client_id]
        
        # Remove cursor
        if client_id in self.cursors:
            del self.cursors[client_id]
        
        # Remove selection
        if client_id in self.selections:
            del self.selections[client_id]
        
        # Notify other clients
        await self._broadcast_user_leave(client_id)
    
    # 2. Message Processing
    async def _process_message(self, client_id: str, message: str):
        """Process incoming message"""
        try:
            data = json.loads(message)
            event_type = PreviewEvent(data.get("type"))
            event_data = data.get("data", {})
            
            # Create event
            event = PreviewEvent(
                id=str(uuid.uuid4()),
                type=event_type,
                data=event_data,
                user_id=client_id,
                timestamp=datetime.now(),
                version=self._get_next_version()
            )
            
            # Handle event
            await self._handle_event(event)
            
        except Exception as e:
            logger.error(f"Error processing message from {client_id}: {e}")
            await self._send_error(client_id, str(e))
    
    async def _handle_event(self, event: PreviewEvent):
        """Handle preview event"""
        # Store event in history
        self.event_history[event.user_id].append(event)
        
        # Execute event handler
        if event.type in self.event_handlers:
            await self.event_handlers[event.type](event)
        
        # Broadcast to other clients
        await self._broadcast_event(event)
    
    # 3. Event Handlers
    async def _handle_content_change(self, event: PreviewEvent):
        """Handle content change event"""
        content = event.data.get("content", "")
        element_id = event.data.get("element_id", "")
        
        # Update preview state
        if element_id in self.preview_states:
            state = self.preview_states[element_id]
            state.content = content
            state.timestamp = datetime.now()
            state.user_id = event.user_id
            state.version = event.version
        
        logger.info(f"Content changed for element {element_id} by user {event.user_id}")
    
    async def _handle_style_change(self, event: PreviewEvent):
        """Handle style change event"""
        styles = event.data.get("styles", {})
        element_id = event.data.get("element_id", "")
        
        # Update preview state
        if element_id in self.preview_states:
            state = self.preview_states[element_id]
            state.styles.update(styles)
            state.timestamp = datetime.now()
            state.user_id = event.user_id
            state.version = event.version
        
        logger.info(f"Styles changed for element {element_id} by user {event.user_id}")
    
    async def _handle_layout_change(self, event: PreviewEvent):
        """Handle layout change event"""
        layout = event.data.get("layout", {})
        element_id = event.data.get("element_id", "")
        
        # Update preview state
        if element_id in self.preview_states:
            state = self.preview_states[element_id]
            state.layout.update(layout)
            state.timestamp = datetime.now()
            state.user_id = event.user_id
            state.version = event.version
        
        logger.info(f"Layout changed for element {element_id} by user {event.user_id}")
    
    async def _handle_user_join(self, event: PreviewEvent):
        """Handle user join event"""
        user_info = event.data.get("user_info", {})
        self.collaborators[event.user_id] = {
            "name": user_info.get("name", "Anonymous"),
            "avatar": user_info.get("avatar", ""),
            "color": user_info.get("color", "#667eea"),
            "joined_at": datetime.now()
        }
        
        logger.info(f"User {user_info.get('name', 'Anonymous')} joined")
    
    async def _handle_user_leave(self, event: PreviewEvent):
        """Handle user leave event"""
        if event.user_id in self.collaborators:
            del self.collaborators[event.user_id]
        
        logger.info(f"User {event.user_id} left")
    
    async def _handle_cursor_move(self, event: PreviewEvent):
        """Handle cursor move event"""
        cursor_data = event.data.get("cursor", {})
        self.cursors[event.user_id] = {
            "position": cursor_data.get("position", {}),
            "element": cursor_data.get("element", ""),
            "timestamp": datetime.now()
        }
        
        # Broadcast cursor position to other clients
        await self._broadcast_cursor_update(event.user_id, cursor_data)
    
    async def _handle_selection_change(self, event: PreviewEvent):
        """Handle selection change event"""
        selection_data = event.data.get("selection", {})
        self.selections[event.user_id] = {
            "start": selection_data.get("start", {}),
            "end": selection_data.get("end", {}),
            "element": selection_data.get("element", ""),
            "timestamp": datetime.now()
        }
        
        # Broadcast selection to other clients
        await self._broadcast_selection_update(event.user_id, selection_data)
    
    async def _handle_comment_add(self, event: PreviewEvent):
        """Handle comment add event"""
        comment_data = event.data.get("comment", {})
        element_id = event.data.get("element_id", "")
        
        comment = {
            "id": str(uuid.uuid4()),
            "user_id": event.user_id,
            "element_id": element_id,
            "content": comment_data.get("content", ""),
            "position": comment_data.get("position", {}),
            "timestamp": datetime.now(),
            "replies": []
        }
        
        self.comments[element_id].append(comment)
        
        # Broadcast comment to all clients
        await self._broadcast_comment_add(comment)
    
    async def _handle_comment_update(self, event: PreviewEvent):
        """Handle comment update event"""
        comment_id = event.data.get("comment_id", "")
        content = event.data.get("content", "")
        
        # Find and update comment
        for element_id, comments in self.comments.items():
            for comment in comments:
                if comment["id"] == comment_id:
                    comment["content"] = content
                    comment["updated_at"] = datetime.now()
                    
                    # Broadcast update
                    await self._broadcast_comment_update(comment)
                    break
    
    async def _handle_comment_delete(self, event: PreviewEvent):
        """Handle comment delete event"""
        comment_id = event.data.get("comment_id", "")
        
        # Find and remove comment
        for element_id, comments in self.comments.items():
            for i, comment in enumerate(comments):
                if comment["id"] == comment_id:
                    del comments[i]
                    
                    # Broadcast deletion
                    await self._broadcast_comment_delete(comment_id)
                    break
    
    # 4. Broadcasting
    async def _broadcast_event(self, event: PreviewEvent):
        """Broadcast event to all connected clients"""
        message = {
            "type": "event",
            "event": asdict(event)
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_message(self, message: Dict):
        """Broadcast message to all connected clients"""
        if not self.connected_clients:
            return
        
        message_str = json.dumps(message, default=str)
        
        # Send to all connected clients
        disconnected_clients = []
        for client_id, websocket in self.connected_clients.items():
            try:
                await websocket.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client_id)
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Remove disconnected clients
        for client_id in disconnected_clients:
            await self._handle_client_disconnection(client_id)
    
    async def _broadcast_user_join(self, user_id: str):
        """Broadcast user join to other clients"""
        if user_id not in self.collaborators:
            return
        
        message = {
            "type": "user_join",
            "user": self.collaborators[user_id]
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_user_leave(self, user_id: str):
        """Broadcast user leave to other clients"""
        message = {
            "type": "user_leave",
            "user_id": user_id
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_cursor_update(self, user_id: str, cursor_data: Dict):
        """Broadcast cursor update to other clients"""
        message = {
            "type": "cursor_update",
            "user_id": user_id,
            "cursor": cursor_data
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_selection_update(self, user_id: str, selection_data: Dict):
        """Broadcast selection update to other clients"""
        message = {
            "type": "selection_update",
            "user_id": user_id,
            "selection": selection_data
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_comment_add(self, comment: Dict):
        """Broadcast comment add to all clients"""
        message = {
            "type": "comment_add",
            "comment": comment
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_comment_update(self, comment: Dict):
        """Broadcast comment update to all clients"""
        message = {
            "type": "comment_update",
            "comment": comment
        }
        
        await self._broadcast_message(message)
    
    async def _broadcast_comment_delete(self, comment_id: str):
        """Broadcast comment delete to all clients"""
        message = {
            "type": "comment_delete",
            "comment_id": comment_id
        }
        
        await self._broadcast_message(message)
    
    # 5. State Management
    async def _send_initial_state(self, client_id: str, websocket):
        """Send initial state to new client"""
        initial_state = {
            "type": "initial_state",
            "data": {
                "preview_states": {k: asdict(v) for k, v in self.preview_states.items()},
                "collaborators": self.collaborators,
                "comments": dict(self.comments),
                "cursors": self.cursors,
                "selections": self.selections
            }
        }
        
        await websocket.send(json.dumps(initial_state, default=str))
    
    def _get_next_version(self) -> int:
        """Get next version number"""
        return int(time.time() * 1000)
    
    # 6. Preview Modes
    def set_preview_mode(self, mode: PreviewMode, custom_dimensions: Dict = None):
        """Set preview mode"""
        if mode == PreviewMode.CUSTOM and custom_dimensions:
            self.current_preview_mode = {
                "mode": mode,
                "dimensions": custom_dimensions
            }
        else:
            self.current_preview_mode = {
                "mode": mode,
                "dimensions": self.preview_modes[mode]
            }
        
        # Broadcast preview mode change
        asyncio.create_task(self._broadcast_preview_mode_change())
    
    async def _broadcast_preview_mode_change(self):
        """Broadcast preview mode change"""
        message = {
            "type": "preview_mode_change",
            "mode": self.current_preview_mode
        }
        
        await self._broadcast_message(message)
    
    # 7. Collaboration Features
    def add_collaborator(self, user_id: str, user_info: Dict):
        """Add collaborator"""
        self.collaborators[user_id] = {
            "name": user_info.get("name", "Anonymous"),
            "avatar": user_info.get("avatar", ""),
            "color": user_info.get("color", "#667eea"),
            "role": user_info.get("role", "editor"),
            "permissions": user_info.get("permissions", ["edit", "comment"]),
            "joined_at": datetime.now()
        }
    
    def remove_collaborator(self, user_id: str):
        """Remove collaborator"""
        if user_id in self.collaborators:
            del self.collaborators[user_id]
    
    def get_collaborators(self) -> Dict[str, Dict]:
        """Get all collaborators"""
        return self.collaborators.copy()
    
    # 8. Comments System
    def add_comment(self, element_id: str, user_id: str, content: str, position: Dict):
        """Add comment to element"""
        comment = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "element_id": element_id,
            "content": content,
            "position": position,
            "timestamp": datetime.now(),
            "replies": []
        }
        
        self.comments[element_id].append(comment)
        return comment
    
    def get_comments(self, element_id: str) -> List[Dict]:
        """Get comments for element"""
        return self.comments.get(element_id, [])
    
    def update_comment(self, comment_id: str, content: str):
        """Update comment"""
        for element_id, comments in self.comments.items():
            for comment in comments:
                if comment["id"] == comment_id:
                    comment["content"] = content
                    comment["updated_at"] = datetime.now()
                    return comment
        return None
    
    def delete_comment(self, comment_id: str):
        """Delete comment"""
        for element_id, comments in self.comments.items():
            for i, comment in enumerate(comments):
                if comment["id"] == comment_id:
                    del comments[i]
                    return True
        return False
    
    # 9. Real-time Synchronization
    def sync_state(self, element_id: str, state: PreviewState):
        """Sync preview state"""
        self.preview_states[element_id] = state
        
        # Broadcast state change
        asyncio.create_task(self._broadcast_state_change(element_id, state))
    
    async def _broadcast_state_change(self, element_id: str, state: PreviewState):
        """Broadcast state change"""
        message = {
            "type": "state_change",
            "element_id": element_id,
            "state": asdict(state)
        }
        
        await self._broadcast_message(message)
    
    # 10. Performance Monitoring
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        return {
            "connected_clients": len(self.connected_clients),
            "active_collaborators": len(self.collaborators),
            "total_comments": sum(len(comments) for comments in self.comments.values()),
            "total_events": sum(len(events) for events in self.event_history.values()),
            "memory_usage": self._get_memory_usage(),
            "uptime": self._get_uptime()
        }
    
    def _get_memory_usage(self) -> Dict:
        """Get memory usage"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss,
            "vms": memory_info.vms,
            "percent": process.memory_percent()
        }
    
    def _get_uptime(self) -> float:
        """Get server uptime"""
        return time.time() - self.start_time if hasattr(self, 'start_time') else 0
    
    # 11. Error Handling
    async def _send_error(self, client_id: str, error_message: str):
        """Send error message to client"""
        if client_id in self.connected_clients:
            message = {
                "type": "error",
                "message": error_message
            }
            
            try:
                await self.connected_clients[client_id].send(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending error message to {client_id}: {e}")
    
    # 12. Server Control
    def start(self):
        """Start the preview server"""
        self.start_time = time.time()
        asyncio.run(self.start_server())
    
    def stop(self):
        """Stop the preview server"""
        # Close all connections
        for websocket in self.connected_clients.values():
            asyncio.create_task(websocket.close())
        
        self.connected_clients.clear()
        logger.info("Preview server stopped")

# Example usage and testing
if __name__ == "__main__":
    # Initialize real-time preview system
    preview_system = RealTimePreviewSystem(port=8765)
    
    print("🔄 Real-Time Preview System Demo")
    print("=" * 50)
    
    # Test preview modes
    print("\n1. Testing preview modes...")
    preview_system.set_preview_mode(PreviewMode.DESKTOP)
    print(f"✅ Desktop mode set: {preview_system.current_preview_mode}")
    
    preview_system.set_preview_mode(PreviewMode.MOBILE)
    print(f"✅ Mobile mode set: {preview_system.current_preview_mode}")
    
    # Test collaboration
    print("\n2. Testing collaboration...")
    preview_system.add_collaborator("user1", {
        "name": "John Doe",
        "avatar": "avatar1.jpg",
        "color": "#667eea",
        "role": "editor"
    })
    
    preview_system.add_collaborator("user2", {
        "name": "Jane Smith",
        "avatar": "avatar2.jpg",
        "color": "#764ba2",
        "role": "viewer"
    })
    
    collaborators = preview_system.get_collaborators()
    print(f"✅ Added {len(collaborators)} collaborators")
    
    # Test comments
    print("\n3. Testing comments...")
    comment1 = preview_system.add_comment("element1", "user1", "Great design!", {"x": 100, "y": 200})
    comment2 = preview_system.add_comment("element1", "user2", "I agree!", {"x": 150, "y": 250})
    
    comments = preview_system.get_comments("element1")
    print(f"✅ Added {len(comments)} comments")
    
    # Test state management
    print("\n4. Testing state management...")
    state = PreviewState(
        content="<h1>Hello World</h1>",
        styles={"color": "blue", "font-size": "24px"},
        layout={"width": "100%", "height": "auto"},
        metadata={"version": "1.0"},
        timestamp=datetime.now(),
        user_id="user1",
        version=1
    )
    
    preview_system.sync_state("element1", state)
    print(f"✅ State synced for element1")
    
    # Test performance metrics
    print("\n5. Testing performance metrics...")
    metrics = preview_system.get_performance_metrics()
    print(f"✅ Performance metrics:")
    print(f"   Connected clients: {metrics['connected_clients']}")
    print(f"   Active collaborators: {metrics['active_collaborators']}")
    print(f"   Total comments: {metrics['total_comments']}")
    print(f"   Total events: {metrics['total_events']}")
    
    print("\n🎉 Real-Time Preview System Demo completed!")
    print("=" * 50)
    print("To start the server, run: preview_system.start()")
