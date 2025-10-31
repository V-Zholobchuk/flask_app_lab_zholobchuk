from loguru import logger

logger.add(
    "logs/contact_form.log",      
    level="INFO",                 
    rotation="10 MB",             
    compression="zip",           
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}" 
)

contact_logger = logger