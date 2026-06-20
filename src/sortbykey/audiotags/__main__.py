from json import dumps as json_dumps
from sortbykey.trackannotate.encoder import get_bpm_metadata, get_key_metadata
from sortbykey.audiotags.cli import parse_args

def main():
    args = parse_args()
    filepath = args.input
    as_json = args.json

    data = {
        "bpm": get_bpm_metadata(filepath),
        "key": get_key_metadata(filepath)
    }
    
    if as_json:
        print(json_dumps(data))
    else:
        print(f"Tags included in \033[96m{filepath}\033[0m ->")
        if data["key"]:
            print(f"\tKEY:\t{data["key"]}")
        if data["bpm"]:
            print(f"\tBPM:\t{data["bpm"]}")


if __name__ == "__main__":
    main()