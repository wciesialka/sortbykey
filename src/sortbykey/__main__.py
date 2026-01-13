import asyncio
import logging
from sortbykey import cli
from sortbykey import workmanager

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    logging.info(f"Analyzing files \"{input_dir}\" -> \"{output_dir}\" w/ {num_workers} jobs.")
    asyncio.run(workmanager.start_work(input_dir, output_dir, num_workers))

if __name__ == "__main__":
    main()