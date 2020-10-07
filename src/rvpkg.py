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
runtime = False
show_deps = False

debug = True
prefix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fs') if debug else '/'
config_path = os.path.join(prefix, 'etc', 'rvpkg.yaml')
db_path = os.path.join(prefix, 'usr', 'share', 'rvpkg', 'packages.yaml')
log_path = os.path.join(prefix, 'var', 'lib', 'rvpkg', 'packages.log')

def load_config():
    global verbose, default_yes, no_confirm, runtime, show_deps

    with open(config_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        
        verbose = data['config']['verbose']
        default_yes = data['config']['default_yes']
        no_confirm = data['config']['no_confirm']
        runtime = data['config']['runtime']
        show_deps = data['config']['show_deps']

def parse_args():
    # argparse setup
    global verbose, no_confirm, runtime, show_deps

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
    parser.add_argument(
        '-r',
        '--runtime',
        action="store_true",
        dest='runtime',
        default=False,
        help='Display runtime dependencies'
    )
    parser.add_argument(
        '-d',
        '--show-deps',
        action='store_true',
        dest='show_deps',
        default=False,
        help='Display package dependencies'
    )

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
    parser_search = subparsers.add_parser(
        'search',
        help='Searches for a package'
    )
    parser_built_with = subparsers.add_parser(
        'built-with',
        help='Checks if one package is built with another'
    )
    parser_tail = subparsers.add_parser(
        'tail',
        help='Displays the last N numbers of the log file'
    )

    # TODO: add tail subcommand

    # TODO: add new subcommand, interactively adds a package to the database

    # TODO: add flags to subcommands to make flag placement more flexible

    parser_add.add_argument(
        'packages',
        type=str,
        action='append',
        nargs='+'
    )
    parser_check.add_argument(
        'packages',
        type=str,
        action='append',
        nargs='+'
    )
    parser_search.add_argument(
        'query',
        type=str
    )

    parser_built_with.add_argument(
        'package',
        type=str
    )
    parser_built_with.add_argument(
        'dependencies',
        type=str,
        action='append',
        nargs='+'
    )

    parser_tail.add_argument(
        'lines',
        type=int
    )

    args = parser.parse_args()
    
    verbose = verbose or args.verbose
    no_confirm = no_confirm or args.no_confirm
    runtime = runtime or args.runtime
    show_deps = show_deps or args.show_deps

    command = args.command

    if command in ['add', 'check']:
        data = args.packages[0]
    elif command == 'search':
        data = [args.query]
    elif command == 'built-with':
        data = [args.package] + args.dependencies[0]
    elif command == 'tail':
        data = [args.lines]
    else:
        data = None

    return command, data

# Convert package strings to package objects
def parse_pkgs(pkgs):
    output = []
    data = None
    package = None

    with open(db_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    package_names = data['packages'].keys()

    for pkg in pkgs:
        matches = [x for x in package_names if pkg in x]

        if len(matches) == 0:
            print(f'Package "{pkg}" not found in database. Exiting...', file=sys.stderr)
            sys.exit(1)
        elif len(matches) == 1:
            name, ver = name_ver_split(matches[0])
            package = Package(name, ver)
        else:
            print(f'\nPackage "{pkg}" has multiple matches')

            for i, pkg in enumerate(matches):
                print(f'{i + 1}) {pkg}')

            try:
                index = int(input('Package # to add: '))
            except:
                print('Error: Invalid selection', file=sys.stderr)
                sys.exit(1)

            if 1 <= index <= len(matches):
                name, ver = name_ver_split(matches[index - 1])
                package = Package(name, ver)
            else:
                print('Error: Invalid selection', file=sys.stderr)
                sys.exit(1)


        package.installed = is_installed(package.entry)

        package.req_deps = data['packages'][package.entry].get('req', [])
        package.rec_deps = data['packages'][package.entry].get('rec', [])
        package.opt_deps = data['packages'][package.entry].get('opt', [])

        output.append(package)
        package = None

    return output


# Add packages to the package list
def add_pkgs(pkgs):
    installed_pkgs = []
    for pkg in pkgs:
        if is_installed(pkg.entry):
            installed_pkgs.append(pkg.entry)

    if installed_pkgs:
        print('Package(s) "{}" already tracked, updating dependencies...'.format(
            ', '.join(installed_pkgs)
        ))
    print_pkgs(pkgs)

    confirm()

    with open(log_path, 'a+') as file:
        for pkg in pkgs:
            file.write(f'{pkg.entry}\n')

    print('Packages successfully added!')


# Show information about multiple packages
def check_pkgs(pkgs):
    print_pkgs(pkgs)

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

def tail(lines):
    for pkg in get_log()[-lines:]:
        print(pkg)

# Looks for packages with the query in the name
def search(query):
    with open(db_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    for item in list(data['packages']):
        if query in item:
            print(item)

# Checks if one package is built with another
def is_built_with(pkg, deps):
    # TODO: rewrite, consider if the package being built is not installed
    pass

def get_log():
    with open(log_path, 'r') as file:
        log = file.readlines()

    new_log = []
    for line in log:
        new_log.append(line.rstrip('\n'))

    log, new_log = new_log, None

    return log
    
def is_installed(pkg):
    return pkg in get_log()

# Display a package and details to the screen
def print_pkgs(pkgs):
    # TODO: scale with terminal width
    # TODO: print header and footer
    # TODO: get rid of "has deps" stuff
    width = min(128, os.get_terminal_size().columns)

    version_width = 0
    for pkg in pkgs:
        version_width = max(version_width, len(pkg.version))
    version_width = max(16, version_width)

    print('\n{}{}{}'.format(
        'Name',
        'Version',
        'Installed'
    ))
    print('{}'.format(''.join(['=' for x in range(width)])))

    for pkg in pkgs:
        print('{}{}{}'.format(
            pkg.name,
            pkg.version,
            'Yes' if pkg.installed else 'No'
        ))
        if show_deps and len(pkg.req_deps + pkg.rec_deps + pkg.opt_deps) > 0:
            print(f'{pkg.name} build dependencies:')
            for item in (pkg.req_deps + pkg.rec_deps + pkg.opt_deps):
                name, version = name_ver_split(item)
                print('{}{}{}'.format(
                    name,
                    version,
                    'Yes' if is_installed(item) else 'No'
                ))

    print('{}'.format(''.join(['=' for x in range(width)])))

# Prompt for confirmation
def confirm():
    if not no_confirm:
        print('Do you want to continue? {}: '.format('[Y/n]' if default_yes else '[y/N]'), end='')
        response = input()

        if not (response.lower() == "y" or (response == "" and default_yes)):
            print("Operation cancelled", file=sys.stderr)
            sys.exit(1)

def name_ver_split(entry):
    pattern = re.compile(r'(.*)-((\d+.)*\d+(.*)?)')
    match = pattern.search(entry)

    if match is None:
        print(f'Package "{entry}" not recognized! Must match format "<name>-<version>"', file=sys.stderr)
        sys.exit(1)

    return match.group(1), match.group(2)


def main():
    load_config()
    cmd, data = parse_args()
    pkgs = None

    if data and cmd != 'search' and cmd != 'tail':
        pkgs = parse_pkgs(data)

    if cmd == 'add':
        add_pkgs(pkgs)
    elif cmd == 'check':
        check_pkgs(pkgs)
    elif cmd == 'count':
        count_pkgs()
    elif cmd == 'list':
        list_pkgs()
    elif cmd == 'search':
        search(data[0])
    elif cmd == 'built-with':
        is_built_with(pkgs[0], pkgs[1:])
    elif cmd == 'tail':
        tail(data[0])
    elif cmd == 'new':
        pass
    

if __name__ == '__main__':
    main()
