# lakehouse_manager.py
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
import duckdb
import pandas as pd
import glob
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from digital_twin.database import engine

storage_base_path = "/app/lakehouse_data"

class LakehouseManager:
    def __init__(self, storage_base_path):
        self.metadata_engine = engine
        self.storage_path = Path(storage_base_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.duckdb_conn = duckdb.connect(':memory:')
    
    def register_table(self, schema_name, table_name, location, schema_def, partitions):
        """Register a new table in the metadata cattalog"""
        table_id = f"{schema_name}.{table_name}"
        
        with self.metadata_engine.connect() as conn:
            conn.execute(text("""
            INSERT INTO tables (table_id, name, schema_name, location, format, 
                        schema_definition, partitions, properties)
            VALUES (:table_id, :table_name, :schema_name, :location, 'parquet',
                :schema_def, :partitions, :properties)
            ON CONFLICT (table_id) DO UPDATE SET
                location = EXCLUDED.location,
                schema_definition = EXCLUDED.schema_definition,
                updated_at = CURRENT_TIMESTAMP
            """), {
            'table_id': table_id,
            'table_name': table_name,
            'schema_name': schema_name,
            'location': location,
            'schema_def': json.dumps(schema_def),
            'partitions': json.dumps(partitions or []),
            'properties': json.dumps(partitions or [])
            })
            conn.commit()
    
    def discover_partitions(self, table_id):
        """Discover all partitions for a table"""

        with self.metadata_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT location, partitions FROM tables WHERE table_id = :table_id
            """), {'table_id': table_id}).fetchone()
            
            if not result:
                raise ValueError(f"Table {table_id} not found")
            
            location = Path(result[0])
            partition_cols = result[1] if result[1] else []

            
            # Discover partition files
            partitions = []
            if location.exists():
                for partition_dir in location.rglob('*.parquet'):
                    rel_path = partition_dir.relative_to(location)
                    partitions.append(str(partition_dir))
            
            return partitions
    
    def query_table(self, table_id, query=None):
        """Query a table using DuckDB"""
        partitions = self.discover_partitions(table_id)
        
        if not partitions:
            raise ValueError(f"No data found for table {table_id}")
        
        # Create temporary view in DuckDB
        table_location = Path(partitions[0]).parent.parent  # top folder above partitions

        view_sql = f"""
            CREATE OR REPLACE VIEW {table_id.replace('.', '_')} AS
            SELECT * FROM read_parquet('{table_location}')
        """
        self.duckdb_conn.execute(view_sql)
        
        # Execute query
        if query:
            result = self.duckdb_conn.execute(query).fetchdf()
        else:
            result = self.duckdb_conn.execute(f"SELECT * FROM {table_id.replace('.', '_')} LIMIT 10").fetchdf()
        
        return result
    
    def begin_transaction(self, table_id, operation):
        """Begin ACID transaction"""
        transaction_id = str(uuid.uuid4())
        
        with self.metadata_engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO transaction_log (transaction_id, table_id, operation, status)
                VALUES (:tx_id, :table_id, :operation, 'PENDING')
            """), {
                'tx_id': transaction_id,
                'table_id': table_id,
                'operation': operation
            })
            # conn.commit() chagpt didnt like it
        
        return transaction_id
    
    def convert_json_to_partitioned_parquet(self, source_folder, target_folder, table_name, 
                                            partition_order="timestamp_first"):
        """
        Converts JSON files into partitioned Parquet files.
        Partitions by timestamp and the first word of the 'event' field.
        
        partition_order: "timestamp_first" or "event_first"
        """

        os.makedirs(target_folder, exist_ok=True)
        json_files = glob.glob(os.path.join(source_folder, "**", "*.json"), recursive=True)

        if not json_files:
            print(f"No JSON files found in {source_folder}")
            return None

        # Load all JSONs
        df = pd.concat([pd.read_json(f, lines=True) for f in json_files], ignore_index=True)

        # --- Extract event prefix ---
        df["event_prefix"] = df["event"].apply(lambda x: x.split("_")[0] if isinstance(x, str) else "unknown")

        # --- Validate timestamp column ---
        if "timestamp" not in df.columns:
            raise ValueError("Missing 'timestamp' field in JSON files — required for partitioning")

        # --- Build partition order ---
        if partition_order == "timestamp_first":
            partition_cols = ["timestamp", "event_prefix"]
        else:
            partition_cols = ["event_prefix", "timestamp"]

        # --- Write Parquet files with partitioning ---
        con = duckdb.connect()
        con.register("input_df", df)

        parquet_path = os.path.join(target_folder, table_name)
        partition_clause = f"PARTITION_BY ({', '.join(partition_cols)})"

        sql = f"""
            COPY input_df TO '{parquet_path}' (FORMAT PARQUET, {partition_clause}, OVERWRITE);
        """
        con.execute(sql)
        con.close()

        print(f"✅ Created partitioned Parquet for {table_name} at {parquet_path}")
        print(f"   Partitioned by {partition_cols}")

        return parquet_path

    def update_metadata(self, table_name, path, columns):
        # Update Postgres metadata table
        with self.metadata_engine.connect() as conn:
            conn.execute(text(
                "INSERT INTO table_metadata (table_name, path, columns) VALUES (:t, :p, :c) ON CONFLICT DO NOTHING"),
                {"t": table_name, "p": path, "c": ",".join(columns)}
            )

def main():
    manager = LakehouseManager(storage_base_path)
    manager.convert_json_to_partitioned_parquet("/app/lakehouse_data/endpoints", "/app/lakehouse_data/parquet_data", "test_table")

    schema_def = {}
    partitions = ["timestamp", "event_prefix"]


    manager.register_table(
        schema_name="silver",
        table_name="test_table",
        location="/app/lakehouse_data/parquet_data/test_table",
        schema_def=schema_def,
        partitions=partitions
    )
    
    df = manager.query_table('silver.test_table')
    print(df)


    



if __name__ == "__main__":
    main()