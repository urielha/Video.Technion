# Video.Technion
Download videos from Technion Panopto like a boss

You can find an executable version at [Video.Technion/releases](https://github.com/urielha/Video.Technion/releases).

Use [OVSDownloader](https://github.com/Krumpet/OVSDownloader) to download from the **old** server.

## download_panopto

usage: download_panopto.py \[-h\] rssURL \[prefix\] \[-i num\] \[-d num\] \[-o output_dir\]

Download videos one by one from panopto.

### positional arguments:

| Argument | Description |
| -------- | ----------- |
|  rssURL  | the RSS url of the Course in the Panopto |
|  prefix  (optional) | prefix of the filename |

### optional arguments:
| Argument | Description |
| -------- | ----------- |
| -h, --help | show this help message and exit |
|  -i, --ignore *num* | ignore x videos from the start (will automaticly ignore files that already exist) |
|  -d, --download *num* | download x videos and stop (default is download all) |
|  -o, --output *output_dir* | output directory (default is current) |


