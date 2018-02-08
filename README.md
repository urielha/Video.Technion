# Video.Technion
Download videos from Technion Panopto like a boss

You can find an executable version at [Video.Technion/releases](https://github.com/urielha/Video.Technion/releases).

Use https://github.com/Krumpet/OVSDownloader-GUI to download from the **old** server.

# Usage

Just open the download_panopto and follow instructions.

Pay attention to run the [excutable](https://github.com/urielha/Video.Technion/releases) or run the script with **Python3**.

If you are using the executable make sure to extract all files from the **download_panopto_exe.zip** 

##### Hebrew note

> If you want to change the output path (or any other parameter) to a path that contains **Hebrew** please specify it as argument with quotation marks and not at the input prompt itself.

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
| -s, --startIndex *num* | index of the first video to download |
| -e, --endIndex *num* | index of the last video |
| -o, --output *output_dir* | output directory |
| -p, --prefix *prefix* | prefix of the filename |

