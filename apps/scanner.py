from .colors import Colors
from .helper import Helper
from .template import Template
from os.path import exists
from os import listdir
from threading import Thread

class Scanner:

    def __init__(self) -> None:
        self.all_templates = listdir("templates/")


    def check_all_templates(self, hostname:str, num_of_threads:int=10) -> None:
        for i in range(num_of_threads):
            t = Thread(target=self.__check, args=("templates"))
        for _ in listdir('templates/'):
            self.__check("templates/"+_, hostname)


    def check_template(self, template:str, hostname:str) -> None:
        if not exists(template):
            template = f"templates/{template.strip('templates/').strip('.yaml')}.yaml"
            if not exists(template):
                print("Template does not exist:", template)
                return
        self.__check(template, hostname)


    def __check(self, template_path:str, hostname:str) -> None:
        template = Template(template_path)

        Helper.clear_line()
        print(f"{Colors.GREEN}[+] Checking: {template.name} {Colors.RESET}", end='\r')

        for req in template.requests:
            req.paths = ['http://'+_.strip().replace('HOSTNAME', hostname) for _ in req.paths]
            req.paths.extend([_.replace('http', 'https') for _ in req.paths])

            for path in req.paths:
                if Helper.check_and_patterns(Helper.get(path, req.redirects), req.patterns):
                    Helper.clear_line()
                    Helper.color_display(f"[+][{template.severity.upper()}] {template.name}: {path}")
                    return
