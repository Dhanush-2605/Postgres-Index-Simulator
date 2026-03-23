import psycopg2
import time

DB_CONFIG = {
    "dbname": "<DATABASE_NAME>", 
    "user": "<USERNAME>",      

    "password": "<PASSWORD>",
    "host": "localhost",
    "port": "5432"
}

NUM_ROWS = 1000000  # 1 Million rows for a noticeable performance difference

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def setup_database(conn):
    print(f"[*] Setting up database with {NUM_ROWS:,} rows... (This may take a minute)")
    with conn.cursor() as cur:
        # Clean up previous runs
        cur.execute("DROP TABLE IF EXISTS users;")
        
        # Create table
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                age INT
            );
        """)
        
        # Insert dummy data using generate_series
        cur.execute(f"""
            INSERT INTO users (name, age)
            SELECT 
                'User_' || i, 
                floor(random() * 80 + 18)::int  
            FROM generate_series(1, {NUM_ROWS}) AS i;
        """)
    conn.commit()
    print("[+] Database setup complete.\n")

# print(get_connection())

conn = get_connection()


def run_benchmark(conn, label, iterations):
    print(f"--- Running Benchmark: {label} ---")
    query = "SELECT * FROM users WHERE age = 25;" 
    
    with conn.cursor() as cur:
        # Start the high-resolution timer
        start_time = time.perf_counter()
        
        # Run the query repeatedly to get a measurable chunk of time
        for _ in range(iterations):
            cur.execute(query)
            cur.fetchall()
            
        end_time = time.perf_counter()
        
    total_time = end_time - start_time
    avg_time_ms = (total_time / iterations) * 1000
    
    print(f"Total time for {iterations:,} queries: {total_time:.4f} seconds")
    print(f"Average time per query: {avg_time_ms:.4f} ms\n")
    return avg_time_ms

def manage_index(conn, action):
    with conn.cursor() as cur:
        if action == "create":
            print("[*] Creating B-Tree Index on 'age' column...")
            cur.execute("CREATE INDEX idx_users_age ON users(age);")
    conn.commit()
    print("[+] Index operation complete.\n")

def main():
    try:
        # Connect to the database
        conn = get_connection()
        
        # 1. Setup Phase
        setup_database(conn)
        
        # 2. Baseline Test (No Index)
        # We run fewer iterations here because full table scans are slow
        unindexed_time = run_benchmark(conn, "Baseline (Full Table Scan)", iterations=100)
        
        # 3. Apply Optimization (Indexing)
        manage_index(conn, "create")
        
        # 4. Optimized Test (With Index)
        # We run many more iterations because index lookups are lightning fast
        indexed_time = run_benchmark(conn, "Optimized (B-Tree Index)", iterations=10000) 
        
        # 5. Calculate and print the results
        speedup = unindexed_time / indexed_time if indexed_time > 0 else float('inf')
        print("=== FINAL RESULTS ===")
        print(f"Baseline Latency: {unindexed_time:.4f} ms per query")
        print(f"Indexed Latency:  {indexed_time:.4f} ms per query")
        print(f"Performance Gain: The query is approximately {speedup:,.0f}x faster with an index!")
        
    except psycopg2.Error as e:
        print(f"\n[!] Database Error: {e}")
        print("Check your password, and make sure the 'db_perf_project' database exists.")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    main()




# BELOW FUNCTINO ARE JUST TO FETCH AND COUNT DATA, NOT PART OF THE BENCHMARKING. YOU CAN RUN THESE SEPARATELY TO VERIFY YOUR DATA.

def count_total_rows():
    try:
        # 1. Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 2. Write the SQL Query to count all rows
        query = "SELECT COUNT(*) FROM users;"
        print("Calculating total rows...\n")
        
        cursor.execute(query)

        # 3. Fetch the single result
        # fetchone() returns a tuple like (1000000,) so we grab the first item [0]
        result = cursor.fetchone()
        row_count = result[0]

        # 4. Print the formatted result
        # The :, format specifier automatically adds commas to large numbers
        print(f"Total rows in the 'users' table: {row_count:,}")

    except psycopg2.Error as e:
        print(f"[!] Database Error: {e}")
    finally:
        # 5. Clean up connections
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()



        # 1. Setup Phase

def fetch_sample_data():
    try:
        # 1. Connect to the database
        # conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 2. Write your SQL Query (Using LIMIT to stay safe)
        query = "SELECT id, name, age FROM users LIMIT 5;"
        print(f"Executing Query: {query}\n")
        
        cursor.execute(query)

        # 3. Fetch the results
        # fetchall() returns a list of tuples containing your data
        records = cursor.fetchall()

        # 4. Loop through and print the data
        print("--- Results ---")
        for row in records:
            # row[0] is id, row[1] is name, row[2] is age
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]}")

    except psycopg2.Error as e:
        print(f"[!] Database Error: {e}")
    finally:
        # 5. Always close your cursor and connection when done
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()



