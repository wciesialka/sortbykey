import asyncio
import logging
import sortbykey.trackannotate.cli as cli
from time import sleep
from sortbykey.trackannotate.tagger import Tagger

def main():
    args = cli.parse_args()
    input_file = args.input
    atonality = args.atonality
    bpm_confidence = args.ametric

    tagger = Tagger(input_file, atonality=atonality, bpm_confidence=bpm_confidence)
    tagger.tag()

    logging.info("Finished!")

if __name__ == "__main__":
    main()