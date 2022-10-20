import argparse
from pathlib import Path
import sys

from k8spurifier.application import Application
from loguru import logger


def main():
    parser = argparse.ArgumentParser(
        prog='k8spurifier', description='k8spurifier: detect security'
        'smells in kubernetes based applications')

    parser.add_argument('-c', '--context', dest='context', default='.',
                        help='path to the application context')
    parser.add_argument('-d', action='store_true',
                        help='run only dynamic analyses')
    parser.add_argument('-s', action='store_true',
                        help='run only static analyses')
    parser.add_argument('-v', action='store_true',
                        help='verbose output')
    parser.add_argument('-vv', action='store_true',
                        help='more verbose output')
    parser.add_argument('config_file', help='path to the config file')
    args = parser.parse_args()

    # set logger level
    if args.vv:
        level = 'DEBUG'
    elif args.v:
        level = 'INFO'
    else:
        level = 'WARNING'

    logger.remove()
    logger.add(sys.stderr, level=level)

    app = Application(Path(args.context))
    app.set_config_path(Path(args.config_file))
    app.aquire_application()
    app.parse_application()

    # parse analysis types
    if args.s:
        app.run_dynamic = False
        app.run_static = True
    elif args.d:
        app.run_dynamic = True
        app.run_static = False

    if app.run_dynamic:
        app.load_kubernetes_cluster_config()

    app.run_analyses()
    app.show_results()


if __name__ == '__main__':
    main()
