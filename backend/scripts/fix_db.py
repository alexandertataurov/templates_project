"""
Script to fix the database schema by adding only missing columns.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import AsyncSessionLocal

async def fix_db():
    """Fix the database schema by adding only missing columns."""
    async with AsyncSessionLocal() as session:
        try:
            # Check if templates table exists
            result = await session.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'templates')"
            ))
            table_exists = result.scalar()
            
            if not table_exists:
                print("Templates table doesn't exist, creating it...")
                await session.execute(text("""
                    CREATE TABLE templates (
                        id SERIAL PRIMARY KEY,
                        template_type VARCHAR NOT NULL DEFAULT 'default',
                        display_name VARCHAR NOT NULL DEFAULT 'Untitled',
                        fields JSONB,
                        file_path VARCHAR,
                        user_id INTEGER,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                await session.commit()
                print("Created templates table successfully")
                return
            
            print("Templates table exists, checking columns...")
            
            # Check each column individually
            columns_to_check = [
                ("template_type", "VARCHAR NOT NULL DEFAULT 'default'"),
                ("display_name", "VARCHAR NOT NULL DEFAULT 'Untitled'"),
                ("fields", "JSONB"),
                ("file_path", "VARCHAR"),
                ("user_id", "INTEGER"),
                ("created_at", "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"),
                ("updated_at", "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
            ]
            
            for column_name, column_type in columns_to_check:
                result = await session.execute(text(
                    f"SELECT EXISTS (SELECT FROM information_schema.columns "
                    f"WHERE table_name = 'templates' AND column_name = '{column_name}')"
                ))
                column_exists = result.scalar()
                
                if column_exists:
                    print(f"Column '{column_name}' already exists")
                else:
                    print(f"Adding missing column '{column_name}'...")
                    await session.execute(text(
                        f"ALTER TABLE templates ADD COLUMN {column_name} {column_type}"
                    ))
            
            await session.commit()
            print("Database schema fixed successfully")
            
        except Exception as e:
            await session.rollback()
            print(f"Error fixing database: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(fix_db()) 