import logging

__VERSION_INFO = (2026, 1, 12)
__version__ = ".".join(str(x) for x in __VERSION_INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)