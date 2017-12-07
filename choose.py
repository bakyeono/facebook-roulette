ABOUT  = 'Choose n items from sample data.'
AUTHOR = 'Bak Yeon O (bakyeono@gmail.com)'
SITE   = 'https://bakyeono.net'

import random
import argparse
from sys import stderr


def parse_args():
    """실행 인자를 해석한다."""
    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument(dest='filename', help='source filename of candidates')
    parser.add_argument(dest='n', type=int, help='number of items to be picked')
    args = parser.parse_args()
    return args


def read_candidates(filename):
    """파일에서 후보군을 읽어들인다."""
    try:
        with open(filename) as f:
            data = f.readlines()
    except OSError:
        print('[ERROR] Can\'t read file: {filename}', file=stderr)
        data = []
    return data


def choose(candidates, n):
    """후보군에서 n개를 임의로 선택해 반환한다."""
    try:
        winners = random.sample(candidates, n)
    except ValueError as e:
        print(str(e), file=stderr)
        exit(-1)
    return winners


def print_winners(winners):
    """당첨자 명단을 출력한다."""
    for winner in winners:
        print(winner, end='')


if __name__ == '__main__':
    args = parse_args()
    candidates = read_candidates(args.filename)
    winners = choose(candidates, args.n)
    print_winners(winners)
    exit(0)

