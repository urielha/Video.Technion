# Video.Technion
Download videos from Technion Panopto like a boss

You can find an executable version at [Video.Technion/releases](https://github.com/urielha/Video.Technion/releases).

Use [OVSDownloader](https://github.com/Krumpet/OVSDownloader) to download from the **old** server.

# Usage

## Simple Usage

Just open the download_panopto and follow instructions.

Pay attention to run the script with **Python 3.*** (or use the executable).

If you are using the executable make sure to extract all files from the **download_panopto.zip** 

### >Hebrew note
If you want to change the output path (or any other parameter) to a path that contains Hebrew please specify it as command parameter (see arguments below) with quotation marks and not at the input prompt itself.

## Usage with arguments

usage: download_panopto.py courseUrl \[-h\] \[-p PREFIX\] \[-s NUM\] \[-e NUM\] \[-o OUTPUT_DIR\]

#### positional arguments:

| Argument | Description |
| -------- | ----------- |
|  courseUrl  | the url of the Course in the Panopto (should contain "folderID") |

#### optional arguments:
| Argument | Description |
| -------- | ----------- |
| -h, --help | show this help message and exit |
| :new: -s, --startIndex *num* | index of the first video to download |
| :new: -e, --endIndex *num* | index of the last video |
| -o, --output *output_dir* | output directory |
| -p, --prefix *prefix* | prefix of the filename |

