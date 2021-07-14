from .colors import Colors
from .helper import Helper
from .template import Template
from os.path import exists
from os import listdir
from threading import Thread
from time import sleep

class Scanner:

    def __init__(self, args) -> None:
        self.args = args
        self.all_templates = [f"templates/{_}" for _ in listdir("templates/")]
        self.threads:list[Thread] = []

        if args.template == 'all':
            self.check_all_templates(args.hostname)
        else:
            self.check_template_if_exists(args.template, args.hostname)


    def check_all_templates(self, hostname:str) -> None:
        self.check_multiple_threaded(self.all_templates, hostname)


    def check_multiple_threaded(self, templates:list[str], hostname:str) -> None:
        '''Makes chunks of templates and passes it to __check_multiple'''
        chunks = tuple(Helper.chunkify(templates, self.args.threads))
        
        for chunk in chunks:
            thread = Thread(target=self.__check_multiple, args=(chunk, hostname))
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


    def __check_multiple(self, templates:list[str], hostname:str) -> None:
        for _ in templates:
            self.__check_template(_, hostname)


    def __check_template(self, template_path:str, hostname:str) -> None:
        template = Template(template_path)

        Helper.clear_line()
        print(f"{Colors.GREEN}[+] Checking: {template.name} {Colors.RESET}", end='\r')

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
