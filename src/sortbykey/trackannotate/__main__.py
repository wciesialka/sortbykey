import asyncio
import logging
import sortbykey.trackannotate.cli as cli
from time import sleep
from sortbykey.trackannotate.tagger import Tagger

def main():
    args = cli.parse_args()
    input_dir = args.input
    num_workers = args.jobs
    atonality = args.atonality

    tagger = Tagger(input_dir, atonality=atonality)
    logging.info(f"Analyzing files \"{input_dir}\" w/ {num_workers} jobs (atonality confidence limit={atonality}).")
    asyncio.run(tagger.start_work(num_workers))
    logging.info("Sleeping for one second to make sure everyone closes the door behind themselves...")
    sleep(1)
    logging.info("Finished!")

if __name__ == "__main__":
    main()