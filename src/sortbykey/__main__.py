import asyncio
import logging
from time import sleep
from sortbykey import cli
from sortbykey import workmanager
from sortbykey.sorter import Sorter

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    copy = args.copy

    sorter = Sorter(input_dir, output_dir, copy_files=copy)
    logging.info(f"Analyzing files \"{input_dir}\" -> \"{output_dir}\" w/ {num_workers} jobs (copy {"on" if copy else "off"}).")
    asyncio.run(workmanager.start_work(sorter, num_workers))
    sleep(1)
    logging.info("Finished!")
    sorter.close()

if __name__ == "__main__":
    main()