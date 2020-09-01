pub struct Package {
    pub name: String,
    pub version: String,
    pub installed: bool,
    pub required_deps: Vec<Package>,
    pub recommended_deps: Vec<Package>,
    pub optional_deps: Vec<Package>,
    pub required_run_deps: Vec<Package>,
    pub recommended_run_deps: Vec<Package>,
    pub optional_run_deps: Vec<Package>
}

impl Default for Package {
    fn default() -> Package {
        Package {
            name: String::from(""),
            version: String::from("0.0.0"),
            installed: false,
            required_deps: Vec::from([]),
            recommended_deps: Vec::from([]),
            optional_deps: Vec::from([]),
            required_run_deps: Vec::from([]),
            recommended_run_deps: Vec::from([]),
            optional_run_deps: Vec::from([])
        }
    }
}

impl Package {
    fn to_string(&self) -> String {
        return format!("{}-{}", self.name, self.version);
    }

    fn get_entry(&self) -> String {
        return self.to_string();
    }
}