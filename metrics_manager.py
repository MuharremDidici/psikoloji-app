from prometheus_client import Counter, Gauge, Histogram, start_http_server
import logging
import time

logger = logging.getLogger(__name__)

class MetricsManager:
    def __init__(self, port: int = 9090):
        # Counters
        self.room_created = Counter(
            'video_room_created_total',
            'Total number of video rooms created'
        )
        self.participant_joined = Counter(
            'participant_joined_total',
            'Total number of participants joined'
        )
        self.connection_errors = Counter(
            'connection_errors_total',
            'Total number of connection errors',
            ['error_type']
        )
        
        # Gauges
        self.active_rooms = Gauge(
            'active_rooms',
            'Number of currently active rooms'
        )
        self.active_participants = Gauge(
            'active_participants',
            'Number of currently active participants'
        )
        self.cpu_usage = Gauge(
            'app_cpu_usage',
            'Application CPU usage'
        )
        self.memory_usage = Gauge(
            'app_memory_usage',
            'Application memory usage in MB'
        )
        
        # Histograms
        self.connection_setup_duration = Histogram(
            'connection_setup_duration_seconds',
            'Time taken to setup WebRTC connection',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
        )
        self.video_processing_latency = Histogram(
            'video_processing_latency_seconds',
            'Video processing latency',
            buckets=[0.05, 0.1, 0.2, 0.5, 1.0]
        )
        
        try:
            start_http_server(port)
            logger.info(f"Metrics server started on port {port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
    
    def track_connection_setup(self):
        """Context manager to track connection setup time"""
        class Timer:
            def __init__(self, histogram):
                self.histogram = histogram
                
            def __enter__(self):
                self.start = time.time()
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                duration = time.time() - self.start
                self.histogram.observe(duration)
                
        return Timer(self.connection_setup_duration)
    
    def update_resource_metrics(self, cpu_percent: float, memory_mb: float):
        """Update resource usage metrics"""
        self.cpu_usage.set(cpu_percent)
        self.memory_usage.set(memory_mb)
    
    def record_error(self, error_type: str):
        """Record a connection error"""
        self.connection_errors.labels(error_type=error_type).inc()

# Global Metrics Manager instance
metrics_manager = MetricsManager()
