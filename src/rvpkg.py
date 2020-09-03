import argparse

from package import Package

# global configuration
verbose = False
no_confirm = False

def main() :
    # argparse setup
    global verbose, no_confirm
    command = None
    packages = []

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
    command, packages = args.command, ((args.packages[0] if hasattr(args, 'packages') else None) if args.command != 'update' else args.package)

    print(f'verbose: {verbose}, no_confirm: {no_confirm}')
    print(f'command: {command}, packages: {packages}')

if __name__ == '__main__':
    main()

def add_packages(packages):
    pass

def add_package(package):
    pass

def check_packages(packages):
    pass

def check_package(package):
    pass
'''

// Add multiple packages to the package list
fn add_packages(packages: Vec<String>) {
    for package in packages {
        
    }
    // TODO: add packages
}

// Add package to the package list
fn add_package(package: String) {
    // TODO: add package
}

// Show information about multiple packages
fn check_packages(packages: Vec<String>) {
    // TODO: check packages
}

// Show information about a package
fn check_package(package: String) {
    // TODO: check package
}

// Displays number of installed packages
fn count() {
    // TODO: count
}

// Displays list of installed packages
fn list() {
    // TODO: list
}

// Remove multiple packages from the package list
fn remove_packages(packages: Vec<String>) {
    // TODO: remove packages
}

// Remove a package from the package list
fn remove_package(package: String) {
    // TODO: remove package
}

// Update a package to reflect currently installed dependencies
fn update_package(packages: String) {
    // TODO: update package
}

// Read package dependecies from packages db
fn get_deps(package: &mut Package) -> Vec<String> {
    // TODO: get deps
    let db = fs::read_to_string("~/Documents/rvpkg/fs/usr/share/packages.toml").expect("Error database file not found");

    let data = db.parse::<Value>().unwrap();

    let deps: Vec<String> = data["meta"]["version"].as_str();
    
    return output;
}

// Read installed dependencies from package log
fn get_installed_deps(package: &Package) {
    // TODO: get installed deps
}

// Display a package and details to the screen
fn print_package(package: &Package, is_dep: bool) {
    // TODO: print package
}

fn print_header() {
    print!(
        "Package Name\t\tVersion\tReq. Deps\tRec. Deps\tOpt. Deps\n\
        -----------------------------------------------------------------------------\n"
    )
}

fn print_footer() {
    // TODO: print footer
}

fn confirm() {
    // TODO: confirm process

    let input: String = read!("{}\n");

    if input.to_lowercase() == "y" || input == "" {
        
    }
    else {
        println!("Operation cancelled");
        std::process::exit(1);
    }
}

fn name_ver_split(input: &String) -> (String, String) {
    let re = Regex::new(r"(.*)-((\d+.)*\d+\w+)").unwrap();

    if !re.is_match(input) {
        println!("Package \"{}\" not recognized! Must match format \"<name>-<version>\"", input);
        std::process::exit(1);
    }

    let matches = re.captures(input).unwrap();

    return (String::from(matches.get(1).unwrap().as_str()), String::from(matches.get(2).unwrap().as_str()));
}
'''