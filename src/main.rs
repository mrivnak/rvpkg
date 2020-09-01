use clap::{Arg, App, AppSettings, SubCommand};

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
        .subcommand(SubCommand::with_name("add")
            .about("Adds a package to the system package list")
            .arg(Arg::with_name("INPUT")
                .help("package(s) to add")
                .index(1)
                .multiple(true)
                .required(true)
            )
        )
        .subcommand(SubCommand::with_name("check")
            .about("Displays information about a package")
            .arg(Arg::with_name("INPUT")
                .help("package(s) to check")
                .index(1)
                .multiple(true)
                .required(true)
            )
        )
        .subcommand(SubCommand::with_name("count")
            .about("Displays the number of installed packages")
        )
        .subcommand(SubCommand::with_name("remove")
            .about("Removes a package from the system package list")
            .arg(Arg::with_name("INPUT")
                .help("package(s) to remove")
                .index(1)
                .multiple(true)
                .required(true)
            )
        )
        .subcommand(SubCommand::with_name("update")
            .about("Updates a package to reflect currently installed dependencies")
            .arg(Arg::with_name("INPUT")
                .help("package to update")
                .index(1)
                .multiple(false)
                .required(true)
            )
        )
        .setting(AppSettings::SubcommandRequiredElseHelp)
        .get_matches();
    
    println!("Hello, world!");
}
