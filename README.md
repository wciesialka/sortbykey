# sortbykey
Sort audio files by key.

Easily sort music files from one directory into another by key! Uses Camelot wheel notation. Uses symlinks to keep files where they're at, and to save on system space! Options to copy files included.

## Getting Started

### Pre-requisites

- [Python 3.13+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/)
- [Essentia](https://pypi.org/project/essentia/) >= 2.1b6.dev1389
- [mutagen](https://pypi.org/project/mutagen/) >= 1.47.0

See [requirements.txt](requirements.txt) for details. Python modules should be installed with `pip`.

### Installation

It is recommended that you install this package in a [Python Virtual Environment](https://docs.python.org/3/library/venv.html). This README will take you through how to do so:

1. [Create a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) using `python3 -m venv env/`
2. [Activate the virtual enviroment](https://docs.python.org/3/library/venv.html#how-venvs-work). POSIX Bash: `source env/bin/activate`. Windows PowerShell: `<venv>\Scripts\Activate.ps1`. Windows Batch: `<venv>\Scripts\activate.bat`.

This package is available on PyPi. To install it from PyPi, use `pip install sortbykey`.

Alternatively, to install it from this repository:

1. [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository), or otherwise download the source code.
2. Enter the directory created by cloning the repository.
3. [Create a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) using `python3 -m venv env/`
4. [Activate the virtual enviroment](https://docs.python.org/3/library/venv.html#how-venvs-work). POSIX Bash: `source env/bin/activate`. Windows PowerShell: `<venv>\Scripts\Activate.ps1`. Windows Batch: `<venv>\Scripts\activate.bat`.
5. [Install the package](https://pip.pypa.io/en/stable/user_guide/#installing-packages) using `python3 -m pip install .`.

## Usage

This package contains several commands. Several commands have flags for atonality/ametric strength; it is important to note that strength is determined by how well an audio file fits to the given data, not how confident the analyzer is. Below are the usage guides for all commands:

### sortbykey

```bash
usage: sortbykey [-h] -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY [-j NUM_CORES]
                 [-a ATONALITY_STRENGTH_LIMIT] [-c]

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
  -a, --atonality ATONALITY_STRENGTH_LIMIT
                        If the strength of the key is below this limit, the
                        audio file will be labeled atonal. Defaults to 0.2.
  -c, --copy            Optional. Specify this flag to copy files instead of
                        creating links to them.

Supported filetypes are: .wav, .aiff, .flac, .ogg, .mp3

```

### sortbytempo

```bash
usage: sortbytempo [-h] -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY [-j NUM_CORES]
                   [-a AMETRIC_STRENGTH_LIMIT] [-w TEMPO_BIN_WIDTH] [-c]

Sort audio files by tempo.

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
  -a, --ametric AMETRIC_STRENGTH_LIMIT
                        If the strength of the bpm is below this limit, the
                        audio file will be considered ametric. Defaults to
                        0.2.
  -w, --binwidth TEMPO_BIN_WIDTH
                        The width of bins to sort audio files into, in beats
                        per minute. Defaults to 1.0 bpm.
  -c, --copy            Optional. Specify this flag to copy files instead of
                        creating links to them.

Supported filetypes are: .wav, .aiff, .flac, .ogg, .mp3
```

### trackannotate

```bash
usage: trackannotate [-h] [-a ATONALITY_CONFIDENCE_LIMIT]
                     [-b BPM_CONFIDENCE_LIMIT]
                     INPUT_FILE

Add key and bpm metadata to a music file.

positional arguments:
  INPUT_FILE            Required. Filepath for the untagged audio file.

options:
  -h, --help            show this help message and exit
  -a, --atonality ATONALITY_CONFIDENCE_LIMIT
                        If the strength of the key is less than this, the
                        tagger won't write key metadata. Defaults to 0.2.
  -b, --ametric BPM_CONFIDENCE_LIMIT
                        If the strength of the tempo is less than this, the
                        tagger won't write tempo metadata. Defaults to 0.2.

Supported filetypes are: .aiff, .mp3, .aif, .flac, .ogg, .opus

```

### audiotags

```bash
usage: audiotags [-h] [--json] INPUT_FILE

Read key and bpm metadata from a music file.

positional arguments:
  INPUT_FILE  Required. Filepath to an audio file.

options:
  -h, --help  show this help message and exit
  --json      Output data in JSON format.

Supported filetypes are: .aiff, .mp3, .aif, .flac, .ogg, .opus
```

## Authors

- Willow Ciesialka

## License

Licensed under GNU AFFERO GENERAL PUBLIC LICENSE Version 3. See [LICENSE](LICENSE) for details.

## Thanks to...

- Dakota Price
- Essentia team
- Mutagen team
