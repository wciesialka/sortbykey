import asyncio
import logging
from time import sleep
from addbpm import cli

def main():
    args = cli.parse_args()
    input_dir = args.input
    num_workers = args.jobs
    logging.info("Hello!")
    sleep(1)
    logging.info("Finished!")

if __name__ == "__main__":
    main()