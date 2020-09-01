use std::io;

use regex::Regex;

use clap::{Arg, App, AppSettings, SubCommand};

mod package;
use package::Package;

fn main() {
    // clap setup
    let matches = App::new("rvpkg")
        .version("0.1.0")
        .author("Michael R. <mrivnak86@gmail.com>")
        .arg(Arg::with_name("verbose")
            .short("v")
            .long("verbose")
            .help("Displays additional information")
        )
        .subcommand(
            SubCommand::with_name("add")
                .about("Adds a package to the system package list")
                .arg(Arg::with_name("packages")
                    .help("package(s) to add")
                    .takes_value(true)
                    .multiple(true)
                    .required(true)
                )
        )
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
}

// Add multiple packages to the package list
fn add_packages(packages: Vec<String>) {

}

// Add package to the package list
fn add_package(package: String) {

}

// Show information about multiple packages
fn check_packages(packages: Vec<String>) {

}

// Show information about a package
fn check_package(package: String) {

}

// Displays number of installed packages
fn count() {

}

// Displays list of installed packages
fn list() {

}

// Remove multiple packages from the package list
fn remove_packages(packages: Vec<String>) {
    
}

// Remove a package from the package list
fn remove_package(package: String) {
    
}

// Update a package to reflect currently installed dependencies
fn update_package(packages: String) {

}

// Read package dependecies from packages db
fn get_deps(package: &mut Package) {

}

// 
fn get_installed_deps(package: &Package) {

}