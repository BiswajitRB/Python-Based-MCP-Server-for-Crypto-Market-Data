import logging

logger = logging.getLogger('mcp')
if not logger.handlers:
    # basic console handler if not configured externally
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def safe_str(obj):
    try:
        return str(obj)
    except Exception:
        return '<unserializable>'
