import asyncio
import logging
import sortbykey.bpmsort.cli as cli
from time import sleep
from sortbykey.bpmsort.sorter import BPMSorter as Sorter

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    copy = args.copy
    bpm_confidence = args.bpmconf
    bin_width = args.binwidth

    sorter = Sorter(input_dir, output_dir, bpm_confidence=bpm_confidence, copy_files=copy, bin_width=bin_width)
    logging.info(f"Analyzing files \"{input_dir}\" -> \"{output_dir}\" w/ {num_workers} jobs (copy {"on" if copy else "off"}, bpm confidence limit={bpm_confidence}, bin width={bin_width}).")
    asyncio.run(sorter.start_work(num_workers))
    logging.info("Sleeping for one second to make sure everyone closes the door behind themselves...")
    sleep(1)
    logging.info("Finished!")
    sorter.close()

if __name__ == "__main__":
    main()