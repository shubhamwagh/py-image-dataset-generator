import argparse
from image_grabber import image_downloader
from image_grabber.grab_settings import *
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    def tuple_arg(s):
        try:
            x, y = map(int, s.split(','))
            return x, y
        except:
            raise argparse.ArgumentTypeError(
                "Parameter '-resize' not valid. ecific size. Example: --resize=32,32"
                "32 will output a 32px x 32px file")

    parser.add_argument('image_keyword',
                        nargs=1,
                        help='keyword to search')

    parser.add_argument('-dest',
                        '-d',
                        help='Folder destination (default: %s/). A sub folder is created for each keywords'
                             % DEFAULT_DESTINATION_FOLDER
                        )

    parser.add_argument('-limit',
                        '-l',
                        help='Number of files to download (default: %s)'
                             % DEFAULT_DOWNLOAD_LIMIT,
                        type=int)

    possible_sizes = ','.join([e.value for e in ImageSize])
    parser.add_argument('-size',
                        '-s',
                        help='Size of source image to download : %s (default: %s)'
                             % (possible_sizes, DEFAULT_IMAGE_SIZE))

    parser.add_argument('-resize',
                        dest="resize",
                        default=None,
                        type=tuple_arg,
                        help='Resize the downloaded image in a specific size. Example: --resize=32,'
                             "32 will output a 32px x 32px file")

    possible_datasources = ', '.join([e.value for e in GrabSourceType])
    parser.add_argument('-source',
                        '-src',
                        help='Data source for download : %s (default: %s)'
                             % (possible_datasources, DEFAULT_GRAB_SOURCE_TYPE),
                        action='append',
                        dest='sources')

    parser.add_argument('-allsources',
                        '-as',
                        action="store_true", default=False,
                        help='If you want your images mixed from all download sources : %s'
                             % (possible_datasources))

    args = parser.parse_args()

    # print(args)

    downloader = image_downloader.ImageDownloader()

    if args.dest is not None:
        downloader.destination = args.dest

    if args.limit is not None:
        downloader.limit = int(args.limit)

    if args.size is not None:
        downloader.image_size = args.size

    if args.allsources is True:
        downloader.sources = [ALL_SOURCE]
    elif args.sources is not None:
        downloader.sources = args.sources

    if args.resize is not None:
        downloader.resize = args.resize

    keyword = args.image_keyword[0]
    downloader.download_images(keyword)
