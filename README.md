# sortbykey
Sort audio files by key

## Getting Started

### Pre-requisites

- [Python 3.13+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/)
- [Essentia](https://pypi.org/project/essentia/) >= 2.1b6.dev1389
- [xxhash](https://pypi.org/project/xxhash/) >= 3.6.0

See [requirements.txt](requirements.txt) for details. Python modules should be installed with `pip`.

### Installation

It is recommended that you install this package in a [Python Virtual Environment](https://docs.python.org/3/library/venv.html). This README will take you through how to do so. 

1. [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository), or otherwise download the source code.
2. [Create a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) using `python3 -m venv env/`
3. [Activate the virtual enviroment](https://docs.python.org/3/library/venv.html#how-venvs-work). POSIX Bash: `source env/bin/activate`. Windows PowerShell: `<venv>\Scripts\Activate.ps1`. Windows Batch: `<venv>\Scripts\activate.bat`.
4. [Install the package](https://pip.pypa.io/en/stable/user_guide/#installing-packages) using `python3 -m pip install .`.

## Usage

```bash
usage: sortbykey [-h] -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY [-j NUM_CORES]
                 [-a ATONALITY_CONFIDENCE_LIMIT] [-c]

Sort audio files by key.

options:
  -h, --help            show this help message and exit
  -i, --input INPUT_DIRECTORY
                        Required. Input directory for the unsorted audio
                        files.
  -o, --output OUTPUT_DIRECTORY
                        Required. Output directory for the sorted audio files.
  -j, --jobs NUM_CORES  Number of concurrent jobs to run for analyzing.
                        Defaults to all but one core on multi-core machines,
                        one core on single-core machines.
  -a, --atonality ATONALITY_CONFIDENCE_LIMIT
                        If the analyzer isn't confident of any key to this
                        percent, it will label the sample as atonal. Defaults
                        to 0.5.
  -c, --copy            Optional. Specify this flag to copy files instead of
                        creating links to them.

```

## Authors

- Willow Ciesialka

## License

Licensed under GNU AFFERO GENERAL PUBLIC LICENSE Version 3. See [LICENSE](LICENSE) for details.

## Thanks to...

- Dakota Price
- Essentia team
- xxhash team