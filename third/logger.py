import sys

from loguru import logger

logger.remove()

logger.add(sys.stdout,
           format="{time:YYYY-MM-DD HH:mm:ss} | {process}:{thread.name} | {module}:{name}:{function}:{line} | {level} | {message}")

# logger.add("file.log",
#            format="{time:YYYY-MM-DD HH:mm:ss} | {process}:{thread.name} | {module}:{name}:{function}:{line} | {level} | {message}",
#            encoding='utf-8',
#            rotation="10 MB",
#            enqueue=True)
