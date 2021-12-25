from .colors import Colors
from .helper import Helper
from .template import Template
from os.path import exists, join
from os import listdir
from threading import Thread
from time import sleep

PKG_ROOT = __file__.strip(__name__ + '.py')

class Scanner:

    def __init__(self, args) -> None:
        self.args = args
        self.templates:list[str] = []
        self.threads:list[Thread] = []
        self.hostsnames:list[str] = []

        if args.hostname:
            self.hostsnames = [args.hostname]
        elif args.hostnames:
            with args.hostnames as names:
                self.hostsnames = [_.rstrip('\n').strip() for _ in names if _.strip()]

        if args.template == 'all':
            self.templates = [join(PKG_ROOT, "templates/", _) for _ in listdir(join(PKG_ROOT, "templates/"))]
        else:
            if exists(args.template):
                self.templates = [args.template]
            else:
                self.templates = [join(PKG_ROOT, "templates/", args.template.lstrip('templates/').rstrip('.yaml') + ".yaml")]

        for host in self.hostsnames:
            self.thread_and_run(self.templates, host)        

    def thread_and_run(self, templates:list[str], hostname:str) -> None:
        '''Makes chunks of templates and passes it to __check_multiple'''
        chunks = tuple(Helper.chunkify(templates, self.args.threads))
        
        for chunk in chunks:
            thread = Thread(target=self.__check_multiple_templates, args=(chunk, hostname))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
        
        for thread in self.threads:
            thread.join()


    def check_template_if_exists(self, template:str, hostname:str) -> None:
        if not exists(template):
            template = f"templates/{template.strip('templates/').strip('.yaml')}.yaml"
            if not exists(template):
                print("Template does not exist:", template)
                return
        self.__check_template(template, hostname)


    def __check_multiple_templates(self, templates:list[str], hostname:str) -> None:
        for _ in templates:
            self.__check_template(_, hostname)


    def __check_template(self, template_path:str, hostname:str) -> None:
        template = Template(template_path)

        Helper.clear_line()
        print(f"{Colors.GREEN}[+] Checking: {template.name} {Colors.RESET} [{hostname}]\r", end='\r')

        for req in template.requests:
            req.paths = ['http://'+_.strip().replace('HOSTNAME', hostname) for _ in req.paths]
            req.paths.extend([_.replace('http', 'https') for _ in req.paths])

            for path in req.paths:
                if Helper.check_and_patterns(Helper.get(path, req.redirects), req.patterns):
                    _ = f"[+][{template.severity.upper()}] {template.name}: {path}"
                    Helper.clear_line()
                    Helper.color_display(_)
                    sleep(0.1)

                    if self.args.output is not None:
                        self.args.output.write(_ + '\n')
                    return
