import argparse

from package import Package

# global configuration
verbose = False
no_confirm = False

def main() :
    # argparse setup
    global verbose, no_confirm
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

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        '-a',
        '--add',
        action="store_true",
        dest='add',
        default=False,
        help='Adds package(s) to the system package list'
    )

    args = parser.parse_args()
    print(args.add)

if __name__ == '__main__':
    main()

'''

        .subcommand(
            SubCommand::with_name("check")
                .about("Displays information about a package")
                .arg(Arg::with_name("packages")
                    .help("package(s) to check")
                    .takes_value(true)
                    .multiple(true)
                    .required(true)
                )
        )
        .subcommand(
            SubCommand::with_name("count")
                .about("Displays the number of installed packages")
        )
        .subcommand(
            SubCommand::with_name("list")
                .about("Displays a list of installed packages")
        )
        .subcommand(
            SubCommand::with_name("remove")
                .about("Removes a package from the system package list")
                .arg(Arg::with_name("packages")
                    .help("package(s) to remove")
                    .takes_value(true)
                    .multiple(true)
                    .required(true)
                )
        )
        .subcommand(
            SubCommand::with_name("update")
                .about("Updates a package to reflect currently installed dependencies")
                .arg(Arg::with_name("packages")
                    .help("package to update")
                    .takes_value(true)
                    .multiple(false)
                    .required(true)
                )
        )
        .setting(AppSettings::SubcommandRequiredElseHelp)
        .get_matches()
    ;

    let verbose: bool = if matches.is_present("verbose") { true } else { false };

    match matches.subcommand() {
        ("add", Some(add_matches)) => {
            let packages: Vec<String> = add_matches
                .values_of("packages")
                .unwrap()
                .map(|s| s.to_string())
                .collect();

            println!("Adding {}", packages.join(", "));

            add_packages(packages);
        }
        ("check", Some(check_matches)) => {
            let packages: Vec<String> = check_matches
                .values_of("packages")
                .unwrap()
                .map(|s| s.to_string())
                .collect();

            println!("Checking {}", packages.join(", "));

            check_packages(packages);
        }
        ("count", None) => {
            count();
        }
        ("list", None) => {
            list();
        }
        ("remove", Some(remove_matches)) => {
            let packages: Vec<String> = remove_matches
                .values_of("packages")
                .unwrap()
                .map(|s| s.to_string())
                .collect();

            println!("Remove {}", packages.join(", "));

            remove_packages(packages);
        }
        ("update", Some(check_matches)) => {
            let package: String = check_matches
                .value_of("packages")
                .unwrap()
                .to_string();

            println!("Checking {}", package);

            update_package(package);
        }
        _ => unreachable!(),
    }

    name_ver_split(&String::from("test-"));
}

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