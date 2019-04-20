#!/usr/bin/env python3

"""
linode_quota_monitor

Monitor your Linode network transfer pool, and shutdown if threshold exceeds limit
"""

import sys
import argparse
import subprocess
import json

DEFAULT_THRESHOLD = 50 #a percentage

def execute_cli(args):
    """execute linode-cli with args parameter values, returns a utf decoded json string"""
    args = ["linode-cli", "--json"] + args
    linode_cli = subprocess.Popen(args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

    (stdout, stderr) = linode_cli.communicate()
    linode_cli.wait() #wait for process to return
    if stderr:
        print("Error: %s" % stderr)
        sys.exit(1)

    return stdout.decode("utf-8")

def check_quota(linode_id, threshold):
    """check usage quota via linode-cli"""
    stdout = execute_cli(["account", "transfer"])
    output = json.loads(stdout)[0]

    percent_used = (output['used'] / output['quota']) * 100

    print("used: %s%% billable: %s actual used: %s quota: %s threshold: %s%%" %
          (round(percent_used, 2), output['billable'], output['used'], output['quota'], threshold),
          end='')

    if output['billable'] > 0:
        print("- alert, you're going to be billed :/", end='')
    print()

    if percent_used > threshold:
        print("%s/%s threshold met" % (percent_used, threshold))
        print("shutting down instance: %s", linode_id)

        stdout = execute_cli(["linodes", "shutdown", linode_id])


def main():
    """main function"""

    example = '''examples:
        ./linode_quota_monitor.py 12345678
        ./linode_quota_monitor.py 12345678 -t 90'''
    parser = argparse.ArgumentParser(description='Monitor your Linode network transfer pool, and shutdown if necessary',
                                     epilog=example,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('linode_id', nargs='?', help='the ID of the Linode to shutdown') #positional argument
    parser.add_argument("-t", "--threshold", help='threshold percentage') #argument without value

    args = parser.parse_args()

    if args.linode_id is None:
        parser.print_help()
        sys.exit(1)

    threshold = DEFAULT_THRESHOLD
    if args.threshold:
        threshold = args.threshold

    check_quota(args.linode_id, float(threshold))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
