class Package:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.installed = False
        self.req_deps = []
        self.rec_deps = []
        self.opt_deps = []
        self.req_run_deps = []
        self.rec_run_deps = []
        self.opt_run_deps = []

    def __to_string__(self):
        return f'{self.name}-{self.version}'

    @property
    def entry(self):
        return self.__to_string__()