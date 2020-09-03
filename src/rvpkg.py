import argparse
import re
import sys

from package import Package

# global configuration
verbose = False
no_confirm = False
default_yes = True

def main() :
    # argparse setup
    global verbose, no_confirm

    parser = argparse.ArgumentParser(prog='rvpkg')
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        dest='verbose',
        default=False,
        help='Displays additional information'
    )
    parser.add_argument(
        '-n',
        '--no-confirm',
        action="store_true",
        dest='no_confirm',
        default=False,
        help='Accepts changes without prompting for confirmation'
    )

    # actions = parser.add_mutually_exclusive_group(required=True)
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    parser_add = subparsers.add_parser(
        'add',
        help='Adds package(s) to the system package list'
    )
    parser_check = subparsers.add_parser(
        'check',
        help='Displays information about package(s)'
    )
    parser_count = subparsers.add_parser(
        'count',
        help='Displays the number of installed packages'
    )
    parser_list = subparsers.add_parser(
        'list',
        help='Displays the list of installed packages'
    )
    parser_remove = subparsers.add_parser(
        'remove',
        help='Removes package(s) from the system package list'
    )
    parser_update = subparsers.add_parser(
        'update',
        help='Updates a package to reflect currently installed dependencies'
    )

    parser_add.add_argument('packages', type=str, action='append', nargs='+')
    parser_check.add_argument('packages', type=str, action='append', nargs='+')
    parser_remove.add_argument('packages', type=str, action='append', nargs='+')
    parser_update.add_argument('package', type=str)

    args = parser.parse_args()
    
    verbose, no_confirm = args.verbose, args.no_confirm
    command = args.command

    if command == 'update':
        packages = args.package
    elif command in ['add', 'check', 'remove']:
        packages = args.packages[0]
    else:
        packages = None

    print(f'verbose: {verbose}, no_confirm: {no_confirm}')
    print(f'command: {command}, packages: {packages}')

if __name__ == '__main__':
    main()

# Add multiple packages to the package list
def add_packages(packages):
    pass  # TODO: add packages

# Add package to the package list
def add_package(package):
    pass  # TODO: add package

# Show information about multiple packages
def check_packages(packages):
    pass  # TODO: check packages

# Show information about a package
def check_package(package):
    pass  # TODO: check package

# Displays number of installed packages
def count():
    pass  # TODO: count

# Displays list of installed packages
def list():
    pass  # TODO: list

# Remove multiple packages from the package list
def remove_packages(packages):
    pass  # TODO: remove packages

# Remove a package from the package list
def remove_package(package):
    pass  # TODO: remove package

# Update a package to reflect currently installed dependencies
def update_package(packages):
    pass  # TODO: update package

# Read package dependecies from packages db
def get_deps(package):
    pass  # TODO: get deps

# Read installed dependencies from package log
def get_installed_deps(package):
    pass  # TODO: get installed deps

# Display a package and details to the screen
def print_package(package, is_dep):
    pass  # TODO: print package

def print_header():
    print(
        "Package Name\t\tVersion\tReq. Deps\tRec. Deps\tOpt. Deps\n\
        -----------------------------------------------------------------------------\n"
    )

def print_footer():
    pass  # TODO: print footer

# Prompt for confirmation
def confirm():
    if not no_confirm:
        print('Do you want to continue? {}'.format('[Y/n]' if default_yes else '[y/N]'), end='')
        response = input()

        if not (response.to_lowercase() == "y" or (input == "" and default_yes)):
            print("Operation cancelled", file=sys.stderr)
            sys.exit(1)

def name_ver_split(entry):
    pattern = re.compile(r'(.*)-((\d+.)*\d+(\w+)?)')
    match = pattern.search(entry)

    if match is None:
        print('Package "{entry}" not recognized! Must match format "<name>-<version>"', file=sys.stderr)
        sys.exit(1)

    return (match.group(1), match.group(2))
