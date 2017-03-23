# Video.Technion
Download videos from Technion servers like a boss

## download_panopto

usage: download_panopto.py [-h] [-i num] [-d num] [-o output_dir]
                           rssURL [prefix]

Download videos one by one from panopto.

### positional arguments:

| Argument | Description |
| -------- | ----------- |
|  rssURL  | the RSS url of the Course in the Panopto |
|  prefix  | prefix of the filename |

### optional arguments:
| Argument | Description |
| -------- | ----------- |
| -h, --help | show this help message and exit |
|  -i num, --ignore num | ignore x videos from the start (will automaticly ignore files that already exist) |
|  -d num, --download num | download x videos and stop (default is download all) |
|  -o output_dir, --output output_dir | output directory (default is current) |


