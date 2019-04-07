import json
import os
import subprocess
from datetime import datetime


class Docketter(object):
    BASE_PATH = '.config/docketter/'
    CONFIG_FILE = 'configurations.json'

    def __init__(self):
        self.configurations = {
            'dockers': {},
            'alias': {}
        }
        self._set_configurations()

    def _log(self, message):
        now = datetime.now()
        print("[{}] {}".format(now, message))

    def _exec_command(self, instructions):
        subprocess.run(instructions)

    def _get_configurations_path(self):
        home = os.getenv('HOME')
        config_path = os.path.join(home, self.BASE_PATH)
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        configuration_file = os.path.join(config_path, self.CONFIG_FILE)
        return configuration_file

    def _set_configurations(self):
        configuration_file = self._get_configurations_path()

        if os.path.exists(configuration_file):
            with open(configuration_file) as configs:
                self.configurations = json.load(configs)

    def _save_configurations(self):
        configuration_file = self._get_configurations_path()

        with open(configuration_file, 'w') as configs:
            json.dump(self.configurations, configs)

    def _check_healthy(self):
        if 'dockers' not in self.configurations:
            self.configurations['dockers'] = dict()
        if 'alias' not in self.configurations:
            self.configurations['alias'] = dict()

    def add_docker(self, name, path, alias=None):
        self._check_healthy()
        self.configurations['dockers'][name] = path

        if alias is not None:
            self.configurations['alias'][alias] = name

        self._save_configurations()

    def add_alias(self, name, alias):
        self._check_healthy()
        self.configurations['alias'][alias] = name

        self._save_configurations()

    def get_docker_name(self, label):
        self._check_healthy()
        reference = self.configurations['alias'].get(label, label)
        return reference

    def remove_alias(self, alias):
        self._check_healthy()
        reference = self.configurations['alias'].get(alias, None)
        if reference is not None:
            del self.configurations['alias'][alias]
            return True
        return False

    def remove_docker(self, label):
        name = self.get_docker_name(label)
        self.remove_alias(label)
        reference = self.configurations['dockers'].get(name, None)
        if reference is not None:
            del self.configurations['dockers'][name]

    def _get_reference(self, label):
        name = self.get_docker_name(label)
        reference = self.configurations['dockers'].get(name, None)
        if reference is None:
            self._log("Missing label {}".format(label))
            self.remove_alias(label)
        return reference

    def run_docker(self, label):
        reference = self._get_reference(label)
        if reference is None:
            return

        instructions = [
            'docker-compose',
            '-f',
            reference,
            'up',
            '-d'
        ]

        self._exec_command(instructions)

    def stop_docker(self, label):
        reference = self._get_reference(label)
        if reference is None:
            return

        instructions = [
            'docker-compose',
            '-f',
            reference,
            'stop'
        ]

        self._exec_command(instructions)

    def get_dockers(self):
        self._check_healthy()
        dockers = list()

        for name, path in self.configurations['dockers'].items():
            dockers.append(
                {
                    'name': name,
                    'docker': path
                }
            )

        return dockers

    def get_aliases(self):
        self._check_healthy()
        aliases = list()

        for alias in self.configurations['alias'].keys():
            reference = self._get_reference(alias)
            if reference is not None:
                aliases.append(
                    {
                        'alias': alias,
                        'docker': reference
                    }
                )
        return aliases
