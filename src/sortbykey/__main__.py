import asyncio
import logging
from time import sleep
from sortbykey import cli
from sortbykey import workmanager
from sortbykey import fs

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    copy = args.copy
    logging.info(f"Analyzing files \"{input_dir}\" -> \"{output_dir}\" w/ {num_workers} jobs.")
    asyncio.run(workmanager.start_work(input_dir, output_dir, num_workers, copy))
    sleep(1)
    logging.info("All async tasks are complete. Starting cleanup/finalization...")
    fs.cleanup(input_dir)
    logging.info("Finished!")

if __name__ == "__main__":
    main()