from apps.scanner import Scanner
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="A template based vulnerability scanner (Inspired by ProjectDiscovery's Nuclei)")
    parser.add_argument('-u', "--hostname", help="Hostname to scan for vulnerabilities", required=True)
    parser.add_argument('-t', "--template", help="Path or id of the template", required=True)
    parser.add_argument('-T', "--threads", help="Number of threads (default=10)", default=10)
    return parser.parse_args()

def main():
    args = parse_args()
    sc = Scanner()
    if args.template == 'all':
        sc.check_all_templates(args.hostname)
    else:
        sc.check_template(args.template, args.hostname)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
