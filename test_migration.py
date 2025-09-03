#!/usr/bin/env python3
"""
Test script to verify migration setup
Run this to check if your database and migrations are working properly
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings


def test_database_connection():
    """Test database connection"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Database connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_migration_status():
    """Test migration status"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            has_alembic = result.scalar()
            
            if has_alembic:
                # Get current migration version
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                version = result.scalar()
                print(f"✅ Alembic migrations found!")
                print(f"📋 Current migration version: {version}")
            else:
                print("⚠️  No Alembic migrations found. Run 'alembic upgrade head' first.")
            
            return True
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        return False


def test_tables_exist():
    """Test if all required tables exist"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            tables = ['organizations', 'users', 'notes', 'todos']
            existing_tables = []
            
            for table in tables:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """))
                if result.scalar():
                    existing_tables.append(table)
            
            print(f"✅ Found {len(existing_tables)}/{len(tables)} tables:")
            for table in existing_tables:
                print(f"   - {table}")
            
            missing_tables = set(tables) - set(existing_tables)
            if missing_tables:
                print(f"❌ Missing tables: {', '.join(missing_tables)}")
                print("   Run 'alembic upgrade head' to create missing tables.")
            
            return len(missing_tables) == 0
    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Testing FastAPI Backend Migration Setup")
    print("=" * 50)
    
    # Test database connection
    print("\n1. Testing database connection...")
    db_ok = test_database_connection()
    
    if not db_ok:
        print("\n❌ Cannot proceed without database connection!")
        return False
    
    # Test migration status
    print("\n2. Testing migration status...")
    migration_ok = test_migration_status()
    
    # Test tables
    print("\n3. Testing table existence...")
    tables_ok = test_tables_exist()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Database Connection: {'✅' if db_ok else '❌'}")
    print(f"   Migration Status: {'✅' if migration_ok else '❌'}")
    print(f"   Tables: {'✅' if tables_ok else '❌'}")
    
    if db_ok and migration_ok and tables_ok:
        print("\n🎉 All tests passed! Your backend is ready to use.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
