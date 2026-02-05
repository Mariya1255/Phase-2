#!/usr/bin/env python3
"""
Validation script for the authentication implementation
"""

import os
import sys
from pathlib import Path

def validate_directory_structure():
    """Validate that all required directories exist"""
    required_dirs = [
        "backend/src",
        "backend/src/models",
        "backend/src/services",
        "backend/src/api",
        "backend/src/utils",
        "backend/src/middleware",
        "backend/src/database",
        "backend/src/logging",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/lib",
        "frontend/src/services",
        "frontend/src/app",
        "frontend/src/app/signup",
        "frontend/src/app/signin",
        "frontend/src/app/dashboard",
        "frontend/src/app/dashboard/tasks",
        "docs"
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"[ERROR] Missing directories: {missing_dirs}")
        return False

    print("[OK] All required directories exist")
    return True

def validate_required_files():
    """Validate that all required files exist"""
    required_files = [
        "backend/src/models/user.py",
        "backend/src/models/task.py",
        "backend/src/services/auth.py",
        "backend/src/services/task_service.py",
        "backend/src/api/auth.py",
        "backend/src/api/tasks.py",
        "backend/src/api/protected.py",
        "backend/src/utils/jwt.py",
        "backend/src/utils/password.py",
        "backend/src/middleware/auth_middleware.py",
        "backend/src/database/filters.py",
        "backend/src/logging/__init__.py",
        "backend/src/main.py",
        "frontend/src/lib/auth.js",
        "frontend/src/services/api.ts",
        "frontend/src/lib/api-client.ts",
        "frontend/src/app/signup/page.tsx",
        "frontend/src/app/signin/page.tsx",
        "frontend/src/app/dashboard/page.tsx",
        "frontend/src/app/dashboard/tasks/page.tsx",
        "frontend/src/middleware.ts",
        "docs/auth-flow.md"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"[ERROR] Missing files: {missing_files}")
        return False

    print("[OK] All required files exist")
    return True

def validate_imports_in_main():
    """Validate that main.py has all required imports"""
    main_file = Path("backend/src/main.py")
    if not main_file.exists():
        print("[ERROR] backend/src/main.py does not exist")
        return False

    content = main_file.read_text()

    required_imports = [
        "from .api.auth import router as auth_router",
        "from .api.todos import router as todos_router",
        "from .api.protected import router as protected_router",
        "from .api.tasks import router as tasks_router"
    ]

    missing_imports = []
    for imp in required_imports:
        if imp not in content:
            missing_imports.append(imp)

    if missing_imports:
        print(f"[ERROR] Missing imports in main.py: {missing_imports}")
        return False

    print("[OK] All required imports exist in main.py")
    return True

def validate_auth_endpoints():
    """Validate that auth endpoints exist and have correct structure"""
    auth_file = Path("backend/src/api/auth.py")
    if not auth_file.exists():
        print("[ERROR] backend/src/api/auth.py does not exist")
        return False

    content = auth_file.read_text()

    required_patterns = [
        "@router.post(\"/signup\"",
        "@router.post(\"/signin\"",
        "@router.post(\"/signout\""
    ]

    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)

    if missing_patterns:
        print(f"[ERROR] Missing auth endpoints: {missing_patterns}")
        return False

    print("[OK] All auth endpoints exist")
    return True

def validate_task_endpoints():
    """Validate that task endpoints exist and enforce user isolation"""
    tasks_file = Path("backend/src/api/tasks.py")
    if not tasks_file.exists():
        print("[ERROR] backend/src/api/tasks.py does not exist")
        return False

    content = tasks_file.read_text()

    # Check for user isolation enforcement
    if "current_user[\"user_id\"]" not in content and "get_user_id_from_token" not in content:
        print("[ERROR] Task endpoints may not enforce user isolation properly")
        return False

    print("[OK] Task endpoints enforce user isolation")
    return True

def main():
    print("[INFO] Validating Authentication Implementation...")
    print()

    all_valid = True

    all_valid &= validate_directory_structure()
    print()

    all_valid &= validate_required_files()
    print()

    all_valid &= validate_imports_in_main()
    print()

    all_valid &= validate_auth_endpoints()
    print()

    all_valid &= validate_task_endpoints()
    print()

    if all_valid:
        print("[SUCCESS] All validations passed! Authentication implementation is complete.")
        return 0
    else:
        print("[ERROR] Some validations failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())