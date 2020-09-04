import argparse
import os
import re
import sys
import yaml

from package import Package

# global configuration
verbose = False
no_confirm = False
default_yes = True
color = True

debug = True
prefix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fs') if debug else '/'
config_path = os.path.join(prefix, 'etc', 'rvpkg.yaml')
db_path = os.path.join(prefix, 'usr', 'share', 'packages.yaml')
log_path = os.path.join(prefix, 'var', 'lib', 'rvpkg', 'packages.log')

def load_config():
    global verbose, default_yes, no_confirm, color

    with open(config_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        
        verbose = data['config']['verbose']
        default_yes = data['config']['default_yes']
        no_confirm = data['config']['no_confirm']
        # color = data['config']['color']

def parse_args():
    # argparse setup
    global verbose, no_confirm, color

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
    '''
    parser.add_argument(
        '-c',
        '--color',
        action="store_true",
        dest='color',
        default=False,
        help='Prints output with color'
    )
    '''

    subparsers = parser.add_subparsers(help='rvpkg subcommands:')
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
    
    verbose = verbose or args.verbose
    no_confirm = no_confirm or args.no_confirm
    # color = color or args.color

    command = args.command

    if command == 'update':
        packages = [args.package]
    elif command in ['add', 'check', 'remove']:
        packages = args.packages[0]
    else:
        packages = None

    return command, packages

# Convert package strings to package objects
def parse_pkgs(pkgs):
    output = []
    data = None

    with open(db_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    for pkg in pkgs:
        name, ver = name_ver_split(pkg)
        package = Package(name, ver)

        if not package.entry in data['packages']:
            print(f'Package "{package.entry}" not found in database. Exiting...')
            sys.exit(1)

        package.installed = is_installed(package.entry)

        package.req_deps = data['packages'][package.entry].get('req_deps', [])
        package.rec_deps = data['packages'][package.entry].get('rec_deps', [])
        package.opt_deps = data['packages'][package.entry].get('opt_deps', [])
        package.req_run_deps = data['packages'][package.entry].get('req_run_deps', [])
        package.rec_run_deps = data['packages'][package.entry].get('rec_run_deps', [])
        package.opt_run_deps = data['packages'][package.entry].get('opt_run_deps', [])
        
        package.has_req_deps = is_installed_before(package.entry, package.req_deps)
        package.has_rec_deps = is_installed_before(package.entry, package.rec_deps)
        package.has_opt_deps = is_installed_before(package.entry, package.opt_deps)
        package.has_req_run_deps = is_installed_before(package.entry, package.req_run_deps)
        package.has_rec_run_deps = is_installed_before(package.entry, package.rec_run_deps)
        package.has_opt_run_deps = is_installed_before(package.entry, package.opt_run_deps)

        output.append(package)

    return output


# Add packages to the package list
def add_pkgs(pkgs):
    print_header()
    print_pkgs(pkgs, True)
    print_footer()

    confirm()

    with open(log_path, 'a+') as file:
        for pkg in pkgs:
            file.write(f'{pkg.entry}\n')

    print('Packages successfully added!')


# Show information about multiple packages
def check_pkgs(pkgs):
    print_header()
    print_pkgs(pkgs, True)
    print_footer()

# Displays number of installed packages
def count_pkgs():
    log = get_log()

    uniq_log = list(set(log))

    if verbose:
        print(f'{len(uniq_log)} packages currently installed')
    else:
        print(len(uniq_log))

# Displays list of installed packages
def list_pkgs():
    pkgs = list(set(get_log()))
    pkgs.sort()
    for item in pkgs:
        print(item)

# Remove packages from the package list
def remove_pkgs(pkgs):
    pass  # TODO: remove packages

# Update a package to reflect currently installed dependencies
def update_pkg(pkgs):
    pass  # TODO: update package

def get_log():
    with open(log_path, 'r') as file:
        log = file.readlines()

    new_log = []
    for line in log:
        new_log.append(line.rstrip('\n'))

    log, new_log = new_log, None

    return log

def is_installed_before(pkg, dep_pkgs):
    reverse_log = reversed(get_log())

    new_log = []
    for item, i in enumerate(reverse_log):
        if item == 'pkg':
            new_log = reversed(reverse_log[i:])

    count = 0
    for pkg in dep_pkgs:
        if pkg in new_log:
            count += 1
    
    if count == len(dep_pkgs):
        return 'All'
    elif 0 < count < len(dep_pkgs):
        return 'Some'
    else:
        return 'None'
    
def is_installed(pkg):
    return pkg in get_log()

# Display a package and details to the screen
def print_pkgs(pkgs, print_deps=False):
    # TODO: print package
    
    for pkg in pkgs:
        print('{0:<24}{1:<16}{2:<16}{3:<16}{4:<16}{5:<16}'.format(
            pkg.name,
            pkg.version,
            'Yes' if pkg.installed else 'No',
            pkg.has_req_deps,
            pkg.has_rec_deps, 
            pkg.has_opt_deps
        ))
        if print_deps and len(pkg.req_deps + pkg.rec_deps + pkg.opt_deps) > 0:
            print(f'{pkg.name} build dependencies:')
            for item in (pkg.req_deps + pkg.rec_deps + pkg.opt_deps):
                name, version = name_ver_split(item)
                print('  {0:<22}{1:<16}{2:<16}'.format(
                    name,
                    version,
                    'Yes' if is_installed(item) else 'No'
                ))

def print_header():
    print('Package Name\t\tVersion\t\tInstalled\tReq. Deps\tRec. Deps\tOpt. Deps')
    print('-------------------------------------------------------------------------------------------------')

def print_footer():
    print('-------------------------------------------------------------------------------------------------')

# Prompt for confirmation
def confirm():
    if not no_confirm:
        print('Do you want to continue? {}: '.format('[Y/n]' if default_yes else '[y/N]'), end='')
        response = input()

        if not (response.lower() == "y" or (response == "" and default_yes)):
            print("Operation cancelled", file=sys.stderr)
            sys.exit(1)

def name_ver_split(entry):
    pattern = re.compile(r'(.*)-((\d+.)*\d+(\w+)?)')
    match = pattern.search(entry)

    if match is None:
        print(f'Package "{entry}" not recognized! Must match format "<name>-<version>"', file=sys.stderr)
        sys.exit(1)

    return match.group(1), match.group(2)


def main():
    load_config()
    cmd, pkgs = parse_args()

    if pkgs:
        pkgs = parse_pkgs(pkgs)

    if cmd == 'add':
        add_pkgs(pkgs)
    elif cmd == 'check':
        check_pkgs(pkgs)
    elif cmd == 'count':
        count_pkgs()
    elif cmd == 'list':
        list_pkgs()
    

if __name__ == '__main__':
    main()
