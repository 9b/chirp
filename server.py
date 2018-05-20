"""Run the server and begin hosting."""

from app import create_app
from argparse import ArgumentParser

parser = ArgumentParser()
subs = parser.add_subparsers(dest='cmd')
setup_parser = subs.add_parser('run')
setup_parser.add_argument('--debug', action='store_true',
                          help='Run in debug mode.')
args = parser.parse_args()
kwargs = {'debug': args.debug}
app = create_app(**kwargs)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
