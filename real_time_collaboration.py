#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-Time Collaboration System - Advanced Multi-User Editing
Supports real-time collaboration with WebSocket connections
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from collections import defaultdict
import redis
import websockets
from websockets.server import WebSocketServerProtocol
import jwt
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles in collaboration"""
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"

class OperationType(Enum):
    """Types of operations in collaboration"""
    ADD_ELEMENT = "add_element"
    REMOVE_ELEMENT = "remove_element"
    MODIFY_ELEMENT = "modify_element"
    MOVE_ELEMENT = "move_element"
    STYLE_CHANGE = "style_change"
    CONTENT_CHANGE = "content_change"
    CURSOR_MOVE = "cursor_move"
    SELECTION = "selection"
    USER_JOIN = "user_join"
    USER_LEAVE = "user_leave"
    CHAT_MESSAGE = "chat_message"

@dataclass
class User:
    """User information for collaboration"""
    id: str
    name: str
    email: str
    role: UserRole
    avatar_url: Optional[str] = None
    color: str = "#3b82f6"
    is_online: bool = True
    last_seen: datetime = None
    cursor_position: Dict = None
    selection: Dict = None

@dataclass
class Operation:
    """Operation in collaboration"""
    id: str
    type: OperationType
    user_id: str
    timestamp: datetime
    data: Dict
    element_id: Optional[str] = None
    version: int = 0

@dataclass
class Project:
    """Project for collaboration"""
    id: str
    name: str
    owner_id: str
    created_at: datetime
    last_modified: datetime
    version: int = 0
    users: Dict[str, User] = None
    operations: List[Operation] = None
    is_active: bool = True

class RealTimeCollaboration:
    """Real-time collaboration system with WebSocket support"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.active_connections: Dict[str, Set[WebSocketServerProtocol]] = defaultdict(set)
        self.user_sessions: Dict[str, Dict] = {}
        self.projects: Dict[str, Project] = {}
        self.operation_history: Dict[str, List[Operation]] = defaultdict(list)
        self.cursors: Dict[str, Dict] = defaultdict(dict)
        self.selections: Dict[str, Dict] = defaultdict(dict)
        
        # JWT secret for authentication
        self.jwt_secret = "your-secret-key"  # Should be from environment
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample projects and users"""
        # Sample users
        sample_users = [
            User(
                id="user1",
                name="علی احمدی",
                email="ali@example.com",
                role=UserRole.OWNER,
                color="#3b82f6"
            ),
            User(
                id="user2",
                name="مریم رضایی",
                email="maryam@example.com",
                role=UserRole.EDITOR,
                color="#10b981"
            ),
            User(
                id="user3",
                name="حسن محمدی",
                email="hasan@example.com",
                role=UserRole.VIEWER,
                color="#f59e0b"
            )
        ]
        
        # Sample project
        sample_project = Project(
            id="project1",
            name="وب‌سایت فروشگاه",
            owner_id="user1",
            created_at=datetime.now(),
            last_modified=datetime.now(),
            users={user.id: user for user in sample_users},
            operations=[]
        )
        
        self.projects["project1"] = sample_project
        
        logger.info("Sample data initialized")
    
    def authenticate_user(self, token: str) -> Optional[User]:
        """Authenticate user from JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            # Find user in projects
            for project in self.projects.values():
                if user_id in project.users:
                    return project.users[user_id]
            
            return None
        except jwt.InvalidTokenError:
            return None
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connection"""
        try:
            # Extract project ID and token from path
            path_parts = path.strip('/').split('/')
            if len(path_parts) < 2:
                await websocket.close(code=1008, reason="Invalid path")
                return
            
            project_id = path_parts[0]
            token = path_parts[1] if len(path_parts) > 1 else None
            
            # Authenticate user
            user = self.authenticate_user(token) if token else None
            if not user:
                await websocket.close(code=1008, reason="Authentication failed")
                return
            
            # Check if project exists
            if project_id not in self.projects:
                await websocket.close(code=1008, reason="Project not found")
                return
            
            project = self.projects[project_id]
            
            # Check if user has access to project
            if user.id not in project.users:
                await websocket.close(code=1008, reason="Access denied")
                return
            
            # Add connection to active connections
            self.active_connections[project_id].add(websocket)
            self.user_sessions[websocket.id] = {
                "user": user,
                "project_id": project_id,
                "connected_at": datetime.now()
            }
            
            logger.info(f"User {user.name} connected to project {project_id}")
            
            # Notify other users about new connection
            await self._broadcast_user_join(project_id, user, websocket)
            
            # Send current project state to new user
            await self._send_project_state(websocket, project)
            
            # Handle messages
            async for message in websocket:
                await self._handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
        finally:
            await self._handle_disconnection(websocket)
    
    async def _handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            session = self.user_sessions.get(websocket.id)
            if not session:
                return
            
            user = session["user"]
            project_id = session["project_id"]
            
            if message_type == "operation":
                await self._handle_operation(websocket, data, user, project_id)
            elif message_type == "cursor_move":
                await self._handle_cursor_move(websocket, data, user, project_id)
            elif message_type == "selection":
                await self._handle_selection(websocket, data, user, project_id)
            elif message_type == "chat_message":
                await self._handle_chat_message(websocket, data, user, project_id)
            elif message_type == "ping":
                await self._send_pong(websocket)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _handle_operation(self, websocket: WebSocketServerProtocol, data: Dict, user: User, project_id: str):
        """Handle operation from user"""
        try:
            operation_data = data.get("data", {})
            operation_type = OperationType(data.get("operation_type"))
            element_id = data.get("element_id")
            
            # Create operation
            operation = Operation(
                id=str(uuid.uuid4()),
                type=operation_type,
                user_id=user.id,
                timestamp=datetime.now(),
                data=operation_data,
                element_id=element_id,
                version=self.projects[project_id].version + 1
            )
            
            # Add to project
            project = self.projects[project_id]
            project.operations.append(operation)
            project.version += 1
            project.last_modified = datetime.now()
            
            # Add to operation history
            self.operation_history[project_id].append(operation)
            
            # Broadcast to other users
            await self._broadcast_operation(project_id, operation, websocket)
            
            logger.info(f"Operation {operation.type.value} from {user.name} in project {project_id}")
            
        except Exception as e:
            logger.error(f"Error handling operation: {e}")
    
    async def _handle_cursor_move(self, websocket: WebSocketServerProtocol, data: Dict, user: User, project_id: str):
        """Handle cursor movement"""
        try:
            cursor_data = data.get("data", {})
            self.cursors[project_id][user.id] = {
                "position": cursor_data.get("position"),
                "timestamp": datetime.now(),
                "user": user
            }
            
            # Broadcast cursor position to other users
            await self._broadcast_cursor_move(project_id, user, cursor_data, websocket)
            
        except Exception as e:
            logger.error(f"Error handling cursor move: {e}")
    
    async def _handle_selection(self, websocket: WebSocketServerProtocol, data: Dict, user: User, project_id: str):
        """Handle text/element selection"""
        try:
            selection_data = data.get("data", {})
            self.selections[project_id][user.id] = {
                "selection": selection_data,
                "timestamp": datetime.now(),
                "user": user
            }
            
            # Broadcast selection to other users
            await self._broadcast_selection(project_id, user, selection_data, websocket)
            
        except Exception as e:
            logger.error(f"Error handling selection: {e}")
    
    async def _handle_chat_message(self, websocket: WebSocketServerProtocol, data: Dict, user: User, project_id: str):
        """Handle chat message"""
        try:
            message_data = data.get("data", {})
            
            chat_message = {
                "id": str(uuid.uuid4()),
                "user_id": user.id,
                "user_name": user.name,
                "message": message_data.get("message"),
                "timestamp": datetime.now(),
                "type": "chat"
            }
            
            # Broadcast chat message to all users
            await self._broadcast_chat_message(project_id, chat_message)
            
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
    
    async def _broadcast_operation(self, project_id: str, operation: Operation, exclude_websocket: WebSocketServerProtocol = None):
        """Broadcast operation to all connected users"""
        message = {
            "type": "operation",
            "data": asdict(operation)
        }
        
        await self._broadcast_to_project(project_id, message, exclude_websocket)
    
    async def _broadcast_cursor_move(self, project_id: str, user: User, cursor_data: Dict, exclude_websocket: WebSocketServerProtocol = None):
        """Broadcast cursor movement to other users"""
        message = {
            "type": "cursor_move",
            "data": {
                "user_id": user.id,
                "user_name": user.name,
                "user_color": user.color,
                "position": cursor_data.get("position"),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self._broadcast_to_project(project_id, message, exclude_websocket)
    
    async def _broadcast_selection(self, project_id: str, user: User, selection_data: Dict, exclude_websocket: WebSocketServerProtocol = None):
        """Broadcast selection to other users"""
        message = {
            "type": "selection",
            "data": {
                "user_id": user.id,
                "user_name": user.name,
                "user_color": user.color,
                "selection": selection_data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self._broadcast_to_project(project_id, message, exclude_websocket)
    
    async def _broadcast_chat_message(self, project_id: str, chat_message: Dict):
        """Broadcast chat message to all users"""
        message = {
            "type": "chat_message",
            "data": chat_message
        }
        
        await self._broadcast_to_project(project_id, message)
    
    async def _broadcast_user_join(self, project_id: str, user: User, exclude_websocket: WebSocketServerProtocol = None):
        """Broadcast user join to other users"""
        message = {
            "type": "user_join",
            "data": {
                "user_id": user.id,
                "user_name": user.name,
                "user_color": user.color,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self._broadcast_to_project(project_id, message, exclude_websocket)
    
    async def _broadcast_user_leave(self, project_id: str, user: User):
        """Broadcast user leave to other users"""
        message = {
            "type": "user_leave",
            "data": {
                "user_id": user.id,
                "user_name": user.name,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self._broadcast_to_project(project_id, message)
    
    async def _broadcast_to_project(self, project_id: str, message: Dict, exclude_websocket: WebSocketServerProtocol = None):
        """Broadcast message to all users in a project"""
        if project_id not in self.active_connections:
            return
        
        disconnected = set()
        
        for websocket in self.active_connections[project_id]:
            if websocket == exclude_websocket:
                continue
            
            try:
                await websocket.send(json.dumps(message, default=str))
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(websocket)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.add(websocket)
        
        # Remove disconnected websockets
        self.active_connections[project_id] -= disconnected
    
    async def _send_project_state(self, websocket: WebSocketServerProtocol, project: Project):
        """Send current project state to user"""
        try:
            # Get recent operations
            recent_operations = self.operation_history[project.id][-50:]  # Last 50 operations
            
            # Get current cursors and selections
            current_cursors = self.cursors[project.id]
            current_selections = self.selections[project.id]
            
            # Get online users
            online_users = []
            for connection in self.active_connections[project.id]:
                session = self.user_sessions.get(connection.id)
                if session:
                    online_users.append(session["user"])
            
            state_message = {
                "type": "project_state",
                "data": {
                    "project": {
                        "id": project.id,
                        "name": project.name,
                        "version": project.version,
                        "last_modified": project.last_modified.isoformat()
                    },
                    "users": [asdict(user) for user in project.users.values()],
                    "online_users": [asdict(user) for user in online_users],
                    "recent_operations": [asdict(op) for op in recent_operations],
                    "cursors": {user_id: cursor for user_id, cursor in current_cursors.items()},
                    "selections": {user_id: selection for user_id, selection in current_selections.items()}
                }
            }
            
            await websocket.send(json.dumps(state_message, default=str))
            
        except Exception as e:
            logger.error(f"Error sending project state: {e}")
    
    async def _send_pong(self, websocket: WebSocketServerProtocol):
        """Send pong response to ping"""
        try:
            pong_message = {
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(pong_message))
        except Exception as e:
            logger.error(f"Error sending pong: {e}")
    
    async def _handle_disconnection(self, websocket: WebSocketServerProtocol):
        """Handle user disconnection"""
        try:
            session = self.user_sessions.get(websocket.id)
            if session:
                user = session["user"]
                project_id = session["project_id"]
                
                # Remove from active connections
                if project_id in self.active_connections:
                    self.active_connections[project_id].discard(websocket)
                
                # Remove from user sessions
                del self.user_sessions[websocket.id]
                
                # Remove cursors and selections
                if project_id in self.cursors:
                    self.cursors[project_id].pop(user.id, None)
                if project_id in self.selections:
                    self.selections[project_id].pop(user.id, None)
                
                # Notify other users
                await self._broadcast_user_leave(project_id, user)
                
                logger.info(f"User {user.name} disconnected from project {project_id}")
                
        except Exception as e:
            logger.error(f"Error handling disconnection: {e}")
    
    def get_project_info(self, project_id: str) -> Optional[Dict]:
        """Get project information"""
        if project_id not in self.projects:
            return None
        
        project = self.projects[project_id]
        online_users = []
        
        for connection in self.active_connections[project_id]:
            session = self.user_sessions.get(connection.id)
            if session:
                online_users.append(session["user"])
        
        return {
            "id": project.id,
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at.isoformat(),
            "last_modified": project.last_modified.isoformat(),
            "version": project.version,
            "total_users": len(project.users),
            "online_users": len(online_users),
            "is_active": project.is_active
        }
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        for project in self.projects.values():
            if user_id in project.users:
                user = project.users[user_id]
                return asdict(user)
        return None
    
    def get_operation_history(self, project_id: str, limit: int = 100) -> List[Dict]:
        """Get operation history for a project"""
        if project_id not in self.operation_history:
            return []
        
        operations = self.operation_history[project_id][-limit:]
        return [asdict(op) for op in operations]
    
    def create_project(self, name: str, owner_id: str) -> str:
        """Create a new project"""
        project_id = str(uuid.uuid4())
        
        # Create owner user (simplified)
        owner = User(
            id=owner_id,
            name="Project Owner",
            email="owner@example.com",
            role=UserRole.OWNER
        )
        
        project = Project(
            id=project_id,
            name=name,
            owner_id=owner_id,
            created_at=datetime.now(),
            last_modified=datetime.now(),
            users={owner_id: owner},
            operations=[]
        )
        
        self.projects[project_id] = project
        self.operation_history[project_id] = []
        
        logger.info(f"Created project {name} with ID {project_id}")
        return project_id
    
    def add_user_to_project(self, project_id: str, user: User) -> bool:
        """Add user to project"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        project.users[user.id] = user
        
        logger.info(f"Added user {user.name} to project {project_id}")
        return True
    
    def remove_user_from_project(self, project_id: str, user_id: str) -> bool:
        """Remove user from project"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        if user_id in project.users:
            del project.users[user_id]
            
            # Remove from cursors and selections
            if project_id in self.cursors:
                self.cursors[project_id].pop(user_id, None)
            if project_id in self.selections:
                self.selections[project_id].pop(user_id, None)
            
            logger.info(f"Removed user {user_id} from project {project_id}")
            return True
        
        return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize collaboration system
    collaboration = RealTimeCollaboration()
    
    # Create a sample project
    project_id = collaboration.create_project("Test Project", "user1")
    print(f"Created project: {project_id}")
    
    # Get project info
    project_info = collaboration.get_project_info(project_id)
    print(f"Project info: {project_info}")
    
    # Start WebSocket server
    async def main():
        print("🚀 Starting Real-Time Collaboration Server...")
        print("📡 WebSocket server will be available at ws://localhost:8765")
        
        server = await websockets.serve(
            collaboration.handle_connection,
            "localhost",
            8765
        )
        
        print("✅ Server started successfully!")
        print("🔗 Connect to: ws://localhost:8765/{project_id}/{token}")
        
        await server.wait_closed()
    
    # Run the server
    asyncio.run(main())
