import argparse
import os


def get_param():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=str, help='ROOTDIR', default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('-c', type=int, help='NCPU', default=1)
    args = parser.parse_args()
    return args.r, args.c

