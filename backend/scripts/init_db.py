"""
Script to initialize the database with the correct schema.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import AsyncSessionLocal

async def init_db():
    """Initialize the database with the correct schema."""
    async with AsyncSessionLocal() as session:
        try:
            # Check if templates table exists
            result = await session.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'templates')"
            ))
            table_exists = result.scalar()
            
            if table_exists:
                print("Templates table exists, checking columns...")
                
                # Check if template_type column exists
                result = await session.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.columns "
                    "WHERE table_name = 'templates' AND column_name = 'template_type')"
                ))
                column_exists = result.scalar()
                
                if column_exists:
                    print("template_type column already exists")
                else:
                    print("Adding missing columns to templates table...")
                    # Add missing columns
                    await session.execute(text(
                        "ALTER TABLE templates "
                        "ADD COLUMN template_type VARCHAR NOT NULL DEFAULT 'default', "
                        "ADD COLUMN display_name VARCHAR NOT NULL DEFAULT 'Untitled', "
                        "ADD COLUMN fields JSONB, "
                        "ADD COLUMN file_path VARCHAR, "
                        "ADD COLUMN user_id INTEGER"
                    ))
                    
                    # Check if timestamp columns exist
                    result = await session.execute(text(
                        "SELECT EXISTS (SELECT FROM information_schema.columns "
                        "WHERE table_name = 'templates' AND column_name = 'created_at')"
                    ))
                    timestamp_exists = result.scalar()
                    
                    if not timestamp_exists:
                        await session.execute(text(
                            "ALTER TABLE templates "
                            "ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, "
                            "ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                        ))
                    
                    await session.commit()
                    print("Added missing columns successfully")
            else:
                print("Creating templates table...")
                # Create the table with all required columns
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
                
            print("Database initialization complete")
            
        except Exception as e:
            await session.rollback()
            print(f"Error initializing database: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(init_db()) 