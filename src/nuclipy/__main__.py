from .colors import Colors
from .scanner import Scanner
from argparse import ArgumentParser, FileType

def parse_args():
    parser = ArgumentParser()
    parser.prog = __package__
    parser.add_argument('-u', "--hostname", help="Hostname to scan for vulnerabilities")
    parser.add_argument('-U', "--hostnames", help="File containing target hostnames", type=FileType('r'))
    parser.add_argument('-t', "--template", help="Path or id of the template", required=True)
    parser.add_argument('-T', "--threads", help="Number of threads (default=10)", default=10)
    parser.add_argument('-o', "--output", help="Output file", type=FileType('w'))
    return parser.parse_args()

def main():
    args = parse_args()
    if not (args.hostname or args.hostnames):
        print("Error: either -u/--hostname or -U/--hostnames is required")
        exit(0)
    Scanner(args)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
