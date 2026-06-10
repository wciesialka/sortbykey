import asyncio
import logging
import sortbykey.trackannotate.cli as cli
from time import sleep
from sortbykey.trackannotate.tagger import analyze_and_annotate

def main():
    args = cli.parse_args()
    input_file = args.input
    atonality = args.atonality
    bpm_confidence = args.bpmconf

    analyze_and_annotate(input_file, atonality=atonality, bpm_confidence=bpm_confidence)

    logging.info("Finished!")

if __name__ == "__main__":
    main()