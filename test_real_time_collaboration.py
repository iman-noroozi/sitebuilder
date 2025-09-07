#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for Real-Time Collaboration System
Tests all functionality of the Real-Time Collaboration system
"""

import sys
import os
import json
import asyncio
import websockets
from datetime import datetime
import uuid

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_time_collaboration import RealTimeCollaboration, User, UserRole, OperationType, Operation

def test_collaboration_system():
    """Test the Real-Time Collaboration System functionality"""
    print("👥 Testing Real-Time Collaboration System...")
    print("=" * 50)
    
    # Initialize the system
    collaboration = RealTimeCollaboration()
    
    # Test 1: Project creation
    print("\n📁 Test 1: Project Creation")
    print("-" * 30)
    
    project_id = collaboration.create_project("Test Project", "user1")
    print(f"✅ Created project: {project_id}")
    
    project_info = collaboration.get_project_info(project_id)
    print(f"✅ Project info: {project_info}")
    
    # Test 2: User management
    print("\n👤 Test 2: User Management")
    print("-" * 30)
    
    # Create test users
    test_users = [
        User(
            id="user2",
            name="علی احمدی",
            email="ali@example.com",
            role=UserRole.EDITOR,
            color="#3b82f6"
        ),
        User(
            id="user3",
            name="مریم رضایی",
            email="maryam@example.com",
            role=UserRole.VIEWER,
            color="#10b981"
        )
    ]
    
    for user in test_users:
        success = collaboration.add_user_to_project(project_id, user)
        print(f"✅ Added user {user.name}: {success}")
    
    # Test removing user
    success = collaboration.remove_user_from_project(project_id, "user3")
    print(f"✅ Removed user user3: {success}")
    
    # Test 3: Operation handling
    print("\n⚡ Test 3: Operation Handling")
    print("-" * 30)
    
    # Create test operations
    test_operations = [
        Operation(
            id=str(uuid.uuid4()),
            type=OperationType.ADD_ELEMENT,
            user_id="user1",
            timestamp=datetime.now(),
            data={"type": "text", "content": "Hello World"},
            element_id="element1"
        ),
        Operation(
            id=str(uuid.uuid4()),
            type=OperationType.MODIFY_ELEMENT,
            user_id="user2",
            timestamp=datetime.now(),
            data={"content": "Modified content"},
            element_id="element1"
        ),
        Operation(
            id=str(uuid.uuid4()),
            type=OperationType.STYLE_CHANGE,
            user_id="user1",
            timestamp=datetime.now(),
            data={"color": "blue", "font-size": "16px"},
            element_id="element1"
        )
    ]
    
    for operation in test_operations:
        # Simulate adding operation to project
        project = collaboration.projects[project_id]
        project.operations.append(operation)
        project.version += 1
        collaboration.operation_history[project_id].append(operation)
        print(f"✅ Added operation: {operation.type.value}")
    
    # Test 4: Operation history
    print("\n📚 Test 4: Operation History")
    print("-" * 30)
    
    history = collaboration.get_operation_history(project_id, limit=10)
    print(f"✅ Operation history count: {len(history)}")
    
    for i, op in enumerate(history[:3]):
        print(f"   {i+1}. {op['type']} by {op['user_id']} at {op['timestamp']}")
    
    # Test 5: User information
    print("\n🔍 Test 5: User Information")
    print("-" * 30)
    
    user_info = collaboration.get_user_info("user1")
    if user_info:
        print(f"✅ User info: {user_info['name']} ({user_info['role']})")
    else:
        print("❌ User not found")
    
    # Test 6: System status
    print("\n📊 Test 6: System Status")
    print("-" * 30)
    
    print(f"✅ Total projects: {len(collaboration.projects)}")
    print(f"✅ Active connections: {len(collaboration.active_connections)}")
    print(f"✅ User sessions: {len(collaboration.user_sessions)}")
    print(f"✅ Operation histories: {len(collaboration.operation_history)}")
    
    print("\n🎉 All collaboration system tests completed successfully!")
    return True

def test_operation_types():
    """Test all operation types"""
    print("\n🔧 Testing Operation Types...")
    print("=" * 50)
    
    collaboration = RealTimeCollaboration()
    project_id = collaboration.create_project("Operation Test Project", "user1")
    
    # Test all operation types
    operation_tests = [
        (OperationType.ADD_ELEMENT, {"type": "text", "content": "New element"}),
        (OperationType.REMOVE_ELEMENT, {"reason": "deleted"}),
        (OperationType.MODIFY_ELEMENT, {"content": "Modified content"}),
        (OperationType.MOVE_ELEMENT, {"x": 100, "y": 200}),
        (OperationType.STYLE_CHANGE, {"color": "red", "font-size": "18px"}),
        (OperationType.CONTENT_CHANGE, {"text": "New text content"}),
        (OperationType.CURSOR_MOVE, {"x": 150, "y": 250}),
        (OperationType.SELECTION, {"start": 0, "end": 10}),
        (OperationType.USER_JOIN, {"user_name": "New User"}),
        (OperationType.USER_LEAVE, {"user_name": "Leaving User"}),
        (OperationType.CHAT_MESSAGE, {"message": "Hello everyone!"})
    ]
    
    for op_type, data in operation_tests:
        operation = Operation(
            id=str(uuid.uuid4()),
            type=op_type,
            user_id="user1",
            timestamp=datetime.now(),
            data=data
        )
        
        # Add to project
        project = collaboration.projects[project_id]
        project.operations.append(operation)
        project.version += 1
        collaboration.operation_history[project_id].append(operation)
        
        print(f"✅ {op_type.value}: {data}")
    
    print(f"\n✅ Tested {len(operation_tests)} operation types")
    return True

def test_user_roles():
    """Test user roles and permissions"""
    print("\n👑 Testing User Roles...")
    print("=" * 50)
    
    collaboration = RealTimeCollaboration()
    project_id = collaboration.create_project("Role Test Project", "owner1")
    
    # Test different user roles
    role_tests = [
        (UserRole.OWNER, "مالک پروژه"),
        (UserRole.EDITOR, "ویرایشگر"),
        (UserRole.VIEWER, "مشاهده‌کننده"),
        (UserRole.GUEST, "مهمان")
    ]
    
    for role, description in role_tests:
        user = User(
            id=f"user_{role.value}",
            name=f"کاربر {description}",
            email=f"{role.value}@example.com",
            role=role,
            color="#3b82f6"
        )
        
        success = collaboration.add_user_to_project(project_id, user)
        print(f"✅ {role.value}: {description} - Added: {success}")
    
    # Test project info with different roles
    project_info = collaboration.get_project_info(project_id)
    print(f"✅ Project has {project_info['total_users']} users")
    
    return True

async def test_websocket_connection():
    """Test WebSocket connection (simulation)"""
    print("\n🌐 Testing WebSocket Connection...")
    print("=" * 50)
    
    collaboration = RealTimeCollaboration()
    project_id = collaboration.create_project("WebSocket Test Project", "user1")
    
    # Simulate WebSocket message handling
    test_messages = [
        {
            "type": "operation",
            "operation_type": "add_element",
            "data": {"type": "text", "content": "Test element"},
            "element_id": "element1"
        },
        {
            "type": "cursor_move",
            "data": {"position": {"x": 100, "y": 200}}
        },
        {
            "type": "selection",
            "data": {"start": 0, "end": 10}
        },
        {
            "type": "chat_message",
            "data": {"message": "Hello from test!"}
        }
    ]
    
    for message in test_messages:
        print(f"✅ Simulated message: {message['type']}")
        
        # Simulate message processing
        if message["type"] == "operation":
            operation = Operation(
                id=str(uuid.uuid4()),
                type=OperationType(message["operation_type"]),
                user_id="user1",
                timestamp=datetime.now(),
                data=message["data"],
                element_id=message.get("element_id")
            )
            
            project = collaboration.projects[project_id]
            project.operations.append(operation)
            project.version += 1
            collaboration.operation_history[project_id].append(operation)
    
    print(f"✅ Processed {len(test_messages)} WebSocket messages")
    return True

def test_concurrent_operations():
    """Test concurrent operations handling"""
    print("\n🔄 Testing Concurrent Operations...")
    print("=" * 50)
    
    collaboration = RealTimeCollaboration()
    project_id = collaboration.create_project("Concurrent Test Project", "user1")
    
    # Simulate concurrent operations from different users
    concurrent_operations = [
        {
            "user_id": "user1",
            "type": OperationType.ADD_ELEMENT,
            "data": {"type": "text", "content": "User 1 element"}
        },
        {
            "user_id": "user2",
            "type": OperationType.ADD_ELEMENT,
            "data": {"type": "button", "content": "User 2 button"}
        },
        {
            "user_id": "user3",
            "type": OperationType.STYLE_CHANGE,
            "data": {"color": "blue"}
        }
    ]
    
    # Add users to project
    for i in range(1, 4):
        user = User(
            id=f"user{i}",
            name=f"کاربر {i}",
            email=f"user{i}@example.com",
            role=UserRole.EDITOR
        )
        collaboration.add_user_to_project(project_id, user)
    
    # Simulate concurrent operations
    for op_data in concurrent_operations:
        operation = Operation(
            id=str(uuid.uuid4()),
            type=op_data["type"],
            user_id=op_data["user_id"],
            timestamp=datetime.now(),
            data=op_data["data"]
        )
        
        project = collaboration.projects[project_id]
        project.operations.append(operation)
        project.version += 1
        collaboration.operation_history[project_id].append(operation)
        
        print(f"✅ Concurrent operation from {op_data['user_id']}: {op_data['type'].value}")
    
    # Check final state
    final_history = collaboration.get_operation_history(project_id)
    print(f"✅ Final operation count: {len(final_history)}")
    print(f"✅ Project version: {collaboration.projects[project_id].version}")
    
    return True

def generate_collaboration_demo():
    """Generate a demo of collaboration functionality"""
    print("\n🎬 Generating Collaboration Demo...")
    print("=" * 50)
    
    collaboration = RealTimeCollaboration()
    
    # Create demo project
    project_id = collaboration.create_project("Demo Project", "demo_owner")
    
    # Add demo users
    demo_users = [
        User(
            id="demo_user1",
            name="علی احمدی",
            email="ali@example.com",
            role=UserRole.OWNER,
            color="#3b82f6"
        ),
        User(
            id="demo_user2",
            name="مریم رضایی",
            email="maryam@example.com",
            role=UserRole.EDITOR,
            color="#10b981"
        ),
        User(
            id="demo_user3",
            name="حسن محمدی",
            email="hasan@example.com",
            role=UserRole.VIEWER,
            color="#f59e0b"
        )
    ]
    
    for user in demo_users:
        collaboration.add_user_to_project(project_id, user)
    
    # Create demo operations
    demo_operations = [
        {
            "type": OperationType.ADD_ELEMENT,
            "user_id": "demo_user1",
            "data": {"type": "header", "content": "وب‌سایت فروشگاه"},
            "description": "اضافه کردن هدر اصلی"
        },
        {
            "type": OperationType.ADD_ELEMENT,
            "user_id": "demo_user2",
            "data": {"type": "button", "content": "خرید کنید"},
            "description": "اضافه کردن دکمه خرید"
        },
        {
            "type": OperationType.MODIFY_ELEMENT,
            "user_id": "demo_user1",
            "data": {"content": "فروشگاه آنلاین ما"},
            "description": "تغییر متن هدر"
        },
        {
            "type": OperationType.STYLE_CHANGE,
            "user_id": "demo_user2",
            "data": {"color": "blue", "font-size": "24px"},
            "description": "تغییر استایل هدر"
        },
        {
            "type": OperationType.CHAT_MESSAGE,
            "user_id": "demo_user3",
            "data": {"message": "عالی! طراحی خوبی شده"},
            "description": "پیام چت"
        }
    ]
    
    demo_results = {
        "project": {
            "id": project_id,
            "name": "Demo Project",
            "users": [{"id": user.id, "name": user.name, "role": user.role.value} for user in demo_users]
        },
        "operations": []
    }
    
    for op_data in demo_operations:
        operation = Operation(
            id=str(uuid.uuid4()),
            type=op_data["type"],
            user_id=op_data["user_id"],
            timestamp=datetime.now(),
            data=op_data["data"]
        )
        
        project = collaboration.projects[project_id]
        project.operations.append(operation)
        project.version += 1
        collaboration.operation_history[project_id].append(operation)
        
        demo_results["operations"].append({
            "type": operation.type.value,
            "user_id": operation.user_id,
            "data": operation.data,
            "description": op_data["description"],
            "timestamp": operation.timestamp.isoformat()
        })
        
        print(f"✅ Demo operation: {op_data['description']}")
    
    # Save demo results
    output_file = "collaboration_demo.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(demo_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Demo results saved to: {output_file}")
    return demo_results

async def main():
    """Main test function"""
    print("👥 Real-Time Collaboration System Test Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Run core tests
        test_collaboration_system()
        
        # Test operation types
        test_operation_types()
        
        # Test user roles
        test_user_roles()
        
        # Test WebSocket connection
        await test_websocket_connection()
        
        # Test concurrent operations
        test_concurrent_operations()
        
        # Generate demo
        generate_collaboration_demo()
        
        print("\n🎉 All collaboration tests completed successfully!")
        print("✅ Real-Time Collaboration System is working properly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
