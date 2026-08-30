import logging
import json
import contextvars
from datetime import datetime, timezone
import traceback

# Context variable to hold the request_id
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Inject request_id if available
        request_id = request_id_var.get()
        if request_id:
            log_record["request_id"] = request_id

        # Add any extra attributes passed via 'extra' dictionary
        if hasattr(record, "extra"):
            log_record.update(record.extra)

        # Include exception traceback if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

def setup_logger(name: str) -> logging.Logger:
    """Creates a structured JSON logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        # Prevent propagation to root logger to avoid duplicate standard format logs
        logger.propagate = False
        
    return logger
