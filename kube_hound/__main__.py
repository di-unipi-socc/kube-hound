import argparse
from pathlib import Path
import sys

from kube_hound.hound import Hound
from loguru import logger


def main():
    parser = argparse.ArgumentParser(
        prog='kube-hound', description='kube-hound: detect security'
        'smells in kubernetes based applications')

    parser.add_argument('-c', '--context', dest='context', default='.',
                        help='path to the application context')
    parser.add_argument('-d', action='store_true',
                        help='run only dynamic analyses')
    parser.add_argument('-s', action='store_true',
                        help='run only static analyses')
    parser.add_argument('-l', dest='analysis_list', default='',
                        help='comma separated list of analysis to run (default all available)')
    parser.add_argument('--json', action='store_true',
                        help='output results in a json object')
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

    hound = Hound(Path(args.context))
    hound.set_config_path(Path(args.config_file))
    hound.aquire_application()
    hound.parse_application()

    # parse analysis types
    if args.s:
        hound.run_dynamic = False
        hound.run_static = True
    elif args.d:
        hound.run_dynamic = True
        hound.run_static = False

    if hound.run_dynamic:
        hound.load_kubernetes_cluster_config()

    if args.analysis_list != '':
        analyses_to_run = args.analysis_list.split(',')
        hound.run_analyses(analyses_to_run)
    else:
        hound.run_analyses()

    hound.show_results(json_output=args.json)


if __name__ == '__main__':
    main()
