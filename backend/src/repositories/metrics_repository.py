from src.config.database import execute_query

class MetricsRepository:
    @staticmethod
    def setup_table():
        # Create table if not exists
        query = """
        CREATE TABLE IF NOT EXISTS environmental_metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            method VARCHAR(10),
            path VARCHAR(255),
            status_code INTEGER,
            bytes_transferred INTEGER,
            co2_estimated FLOAT,
            response_time_ms FLOAT
        );
        """
        execute_query(query)
        
    @staticmethod
    def reset_metrics():
        # Truncate table on startup
        execute_query("TRUNCATE TABLE environmental_metrics RESTART IDENTITY;")
        
    @staticmethod
    def insert_metric(method: str, path: str, status_code: int, bytes_transferred: int, co2_estimated: float, response_time_ms: float):
        query = """
        INSERT INTO environmental_metrics (method, path, status_code, bytes_transferred, co2_estimated, response_time_ms)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, [method, path, status_code, bytes_transferred, co2_estimated, response_time_ms])

    @staticmethod
    def get_global_metrics():
        query = """
        SELECT 
            COUNT(*) as total_requests,
            COALESCE(SUM(co2_estimated), 0) as total_co2,
            COALESCE(AVG(co2_estimated), 0) as avg_co2,
            COALESCE(SUM(bytes_transferred), 0) as total_bytes
        FROM environmental_metrics
        """
        result = execute_query(query)
        return result[0] if result else {}

    @staticmethod
    def get_endpoints_ranking():
        query = """
        SELECT 
            path,
            method,
            COUNT(*) as request_count,
            SUM(co2_estimated) as total_co2,
            AVG(response_time_ms) as avg_time
        FROM environmental_metrics
        GROUP BY path, method
        ORDER BY total_co2 DESC
        """
        return execute_query(query)

    @staticmethod
    def get_recent_metrics(limit: int = 100):
        query = """
        SELECT *
        FROM environmental_metrics
        ORDER BY timestamp DESC
        LIMIT %s
        """
        return execute_query(query, [limit])
