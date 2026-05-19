import logging

__VERSION_INFO = (2026, 5, 19, 2)
__version__ = ".".join(str(x) for x in __VERSION_INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)