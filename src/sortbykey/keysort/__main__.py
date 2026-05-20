import asyncio
import logging
import sortbykey.keysort.cli as cli
from time import sleep
from sortbykey.sorter import Sorter

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    copy = args.copy
    atonality = args.atonality

    sorter = Sorter(input_dir, output_dir, atonality=atonality, copy_files=copy)
    logging.info(f"Analyzing files \"{input_dir}\" -> \"{output_dir}\" w/ {num_workers} jobs (copy {"on" if copy else "off"}, atonality confidence limit={atonality}).")
    asyncio.run(sorter.start_work(num_workers))
    logging.info("Sleeping for one second to make sure everyone closes the door behind themselves...")
    sleep(1)
    logging.info("Finished!")
    sorter.close()

if __name__ == "__main__":
    main()