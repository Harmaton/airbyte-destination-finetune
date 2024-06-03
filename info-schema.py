import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

# Function to fetch database metadata
def fetch_database_metadata():
    try:
        # Connect to the database
        connection = psycopg2.connect(DATABASE_URL)
        
        # Create a cursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
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
        
        # Loop through tables and fetch their columns
        for table in tables:
            table_name = table['table_name']
            print(f"\nTable: {table_name}")
            
            # Query to get column information for the current table
            column_query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
            """
            
            # Execute the column query
            cursor.execute(column_query)
            columns = cursor.fetchall()
            
            # Print column details
            for column in columns:
                column_name = column['column_name']
                data_type = column['data_type']
                is_nullable = column['is_nullable']
                print(f"    Column: {column_name}, Type: {data_type}, Nullable: {is_nullable}")
    
    except Exception as error:
        print(f"Error fetching data: {error}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Placeholder for another function
def another_function():
    print("This is another function. Coming Soon - if need be!")

# Main function to handle user input
def main():
    while True:
        print("\nSelect an option:")
        print("1. Fetch database metadata")
        print("2. Another function")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            fetch_database_metadata()
        elif choice == "2":
            another_function()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
