import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

# Function to remove specific columns from all tables
def remove_columns():
    columns_to_remove = ["_airbyte_raw_id", "_airbyte_extracted_at", "_airbyte_meta"]
    
    try:
        # Connect to the database
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True  # Enable auto-commit
        cursor = connection.cursor()
        
        # Query to get all table names
        table_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        
        # Execute the table query
        cursor.execute(table_query)
        tables = cursor.fetchall()
        
        # Loop through tables and remove specified columns
        for table in tables:
            table_name = table[0]
            for column in columns_to_remove:
                # Check if the column exists in the table
                column_exists_query = sql.SQL("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = %s;
                """)
                cursor.execute(column_exists_query, (table_name, column))
                if cursor.fetchone():
                    # Remove the column if it exists
                    drop_column_query = sql.SQL("ALTER TABLE {} DROP COLUMN {};").format(
                        sql.Identifier(table_name),
                        sql.Identifier(column)
                    )
                    try:
                        cursor.execute(drop_column_query)
                        print(f"Removed column {column} from table {table_name}")
                    except Exception as e:
                        print(f"Error removing column {column} from table {table_name}: {e}")
    
    except Exception as error:
        print(f"Error: {error}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Main function to handle user input
def main():
    while True:
        print("\nSelect an option:")
        print("1. Remove specific columns from all tables")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            remove_columns()
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
