#
#    Metrix++, Copyright 2009-2019, Metrix++ Project
#    Link: https://github.com/metrixplusplus/metrixplusplus
#
#    This file is a part of Metrix++ Tool.
#

import time
import sys
import logging
import os
import subprocess
import itertools
from pathlib import Path
import argparse

import mpp.log
import mpp.internal.loader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('metrixpp')


def execute_command(command: str, paths, args) -> int:
    loader = mpp.internal.loader.Loader()
    args = loader.load(command, paths, args)
    exit_code = loader.run(args)
    loader.unload()
    return exit_code


def main():

    parser = argparse.ArgumentParser(
        "metrixpp",
        description="Analyze C/C++ and Java code to determine code metrics")

    subparsers = parser.add_subparsers(required=True, dest='command')

    # collect
    parser_collect = subparsers.add_parser(
        "collect", help="collect code metrics")

    parser_collect.add_argument('metrics', metavar='m', type=str, nargs='+',
                                help='metrics to collect')

    # view
    parser_view = subparsers.add_parser(
        "view", help="view collected code metrics")

    # limit
    parser_limit = subparsers.add_parser(
        "limit", help="limit metrics")

    args = parser.parse_args()

    os.environ['METRIXPLUSPLUS_INSTALL_DIR'] = str(
        Path(__file__).parent.resolve())

    # exemode = None
    # exemode = '-R'

    # if len(sys.argv[1:]) != 0:
    #     exemode = sys.argv[1]

    # if exemode != "-R" and exemode != "-D":
    #     exemode = '-D'  # TODO implement install and release mode
    #     # inject '-D' or '-R' option
    #     #profile_args = ['-m', 'cProfile']
    #     profile_args = []
    #     exit(subprocess.call(itertools.chain(
    #         [sys.executable], profile_args, [sys.argv[0], '-D'], sys.argv[1:])))

    command = args.command
    args = args.metrics
    logger.info(f"program is executing command: {command}")

    mpp_paths = []

    exit_code = execute_command(command, mpp_paths, args)

    return exit_code


def start():
    ts = time.time()
    mpp.log.set_default_format()

    exit_code = main()
    time_spent = round((time.time() - ts), 2)
    if 'METRIXPLUSPLUS_TEST_GENERATE_GOLDS' in list(os.environ.keys()) and \
            os.environ['METRIXPLUSPLUS_TEST_GENERATE_GOLDS'] == "True":
        time_spent = 1  # Constant value if under tests
    logging.warning("Done (" + str(time_spent) +
                    " seconds). Exit code: " + str(exit_code))
    exit(exit_code)


if __name__ == '__main__':

    # init
    mpp.log.set_default_format()
    p = str(Path(__file__).parent.resolve())
    os.environ['METRIXPLUSPLUS_INSTALL_DIR'] = p

    metrics = ["--std.code.lines.code", "--std.code.complexity.cyclomatic"]
    # metrics = ["std.code.complexity.cyclomatic"]
    paths = []

    execute_command("collect", paths, metrics)
