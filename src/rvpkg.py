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
db_path = os.path.join(prefix, 'usr', 'share', 'packages.yaml')
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

    parser_add.add_argument(
        'packages',
        type=str,
        action='append',
        nargs='+'
    )
    parser_check.add_argument(
        '-d',
        '--show-deps',
        action='store_true',
        dest='show_deps',
        default=False,
        help='Display package dependencies'
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

    parser_built_with.add_argument('package', type=str)
    parser_built_with.add_argument('dependency', type=str)

    args = parser.parse_args()
    
    verbose = verbose or args.verbose
    no_confirm = no_confirm or args.no_confirm
    runtime = runtime or args.runtime
    show_deps = show_deps or args.show_deps

    command = args.command

    if command in ['add', 'check']:
        packages = args.packages[0]
    elif command == 'search':
        packages = [args.query]
    elif command == 'built-with':
        packages = [args.package, args.dependency]
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

        package.req_deps = data['packages'][package.entry].get('req', [])
        package.rec_deps = data['packages'][package.entry].get('rec', [])
        package.opt_deps = data['packages'][package.entry].get('opt', [])
        package.req_run_deps = data['packages'][package.entry].get('req_run', [])
        package.rec_run_deps = data['packages'][package.entry].get('rec_run', [])
        package.opt_run_deps = data['packages'][package.entry].get('opt_run', [])
        
        package.has_req_deps = has_deps(package.entry, package.req_deps)
        package.has_rec_deps = has_deps(package.entry, package.rec_deps)
        package.has_opt_deps = has_deps(package.entry, package.opt_deps)
        package.has_req_run_deps = has_deps(package.entry, package.req_run_deps)
        package.has_rec_run_deps = has_deps(package.entry, package.rec_run_deps)
        package.has_opt_run_deps = has_deps(package.entry, package.opt_run_deps)

        output.append(package)

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
    print_header()
    print_pkgs(pkgs)
    print_footer()

    confirm()

    with open(log_path, 'a+') as file:
        for pkg in pkgs:
            file.write(f'{pkg.entry}\n')

    print('Packages successfully added!')


# Show information about multiple packages
def check_pkgs(pkgs):
    print_header()
    print_pkgs(pkgs)
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

# Looks for packages with the query in the name
def search(query):
    with open(db_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    for item in list(data['packages']):
        if query in item:
            print(item)

# Checks if one package is built with another
def is_built_with(pkg, dep):
    if has_deps(pkg.entry, [dep.entry]) == 'All':
        print(f'Package "{pkg}" is built with "{dep}"')
    else:
        print(f'Package "{pkg}" is NOT built with "{dep}"')

def get_log():
    with open(log_path, 'r') as file:
        log = file.readlines()

    new_log = []
    for line in log:
        new_log.append(line.rstrip('\n'))

    log, new_log = new_log, None

    return log

def has_deps(pkg, dep_pkgs):
    reverse_log = get_log()
    reverse_log.reverse()

    new_log = []
    for i, item in enumerate(reverse_log):
        if item == pkg:
            new_log = list(reverse_log)[i:]
            new_log.reverse()

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
def print_pkgs(pkgs):
    if runtime:
        for pkg in pkgs:
            print('{0:<24}{1:<12}{2:<12}{3:<8}{4:<8}{5:<8}{6:<9}{7:<9}{8:<9}'.format(
                pkg.name,
                pkg.version,
                'Yes' if pkg.installed else 'No',
                pkg.has_req_deps,
                pkg.has_rec_deps, 
                pkg.has_opt_deps,
                pkg.has_req_run_deps,
                pkg.has_rec_run_deps,
                pkg.has_opt_run_deps
            ))
            if show_deps and len(pkg.req_deps + pkg.rec_deps + pkg.opt_deps) > 0:
                print(f'{pkg.name} build dependencies:')
                for item in (pkg.req_deps + pkg.rec_deps + pkg.opt_deps):
                    name, version = name_ver_split(item)
                    print('  {0:<22}{1:<12}{2:<12}'.format(
                        name,
                        version,
                        'Yes' if is_installed(item) else 'No'
                    ))
    else:
        for pkg in pkgs:
            print('{0:<24}{1:<12}{2:<12}{3:<8}{4:<8}{5:<8}'.format(
                pkg.name,
                pkg.version,
                'Yes' if pkg.installed else 'No',
                pkg.has_req_deps,
                pkg.has_rec_deps, 
                pkg.has_opt_deps
            ))
            if show_deps and len(pkg.req_deps + pkg.rec_deps + pkg.opt_deps) > 0:
                print(f'{pkg.name} build dependencies:')
                for item in (pkg.req_deps + pkg.rec_deps + pkg.opt_deps):
                    name, version = name_ver_split(item)
                    print('  {0:<22}{1:<12}{2:<12}'.format(
                        name,
                        version,
                        'Yes' if is_installed(item) else 'No'
                    ))

def print_header():
    if runtime:
        print('{0:<24}{1:<12}{2:<12}{3:<8}{4:<8}{5:<8}{6:<9}{7:<9}{8:<9}'.format(
                'Package Name',
                'Version',
                'Installed',
                'Req',
                'Rec', 
                'Opt',
                'Req R',
                'Rec R',
                'Opt R'
            ))
        print('-------------------------------------------------------------------------------------------')
    else:
        print('{0:<24}{1:<12}{2:<12}{3:<8}{4:<8}{5:<8}'.format(
                'Package Name',
                'Version',
                'Installed',
                'Req',
                'Rec', 
                'Opt'
            ))
        print('---------------------------------------------------------------')

def print_footer():
    if runtime:
        print('-------------------------------------------------------------------------------------------')
    else:
        print('---------------------------------------------------------------')

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
    cmd, pkgs = parse_args()

    if pkgs and cmd != 'search':
        pkgs = parse_pkgs(pkgs)

    if cmd == 'add':
        add_pkgs(pkgs)
    elif cmd == 'check':
        check_pkgs(pkgs)
    elif cmd == 'count':
        count_pkgs()
    elif cmd == 'list':
        list_pkgs()
    elif cmd == 'search':
        search(pkgs[0])
    elif cmd == 'built-with':
        is_built_with(pkgs[0], pkgs[1])
    

if __name__ == '__main__':
    main()
