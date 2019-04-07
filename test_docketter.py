import json
import os
from unittest import TestCase, main
from unittest.mock import patch

from docketter import Docketter


class MockFileOpen(object):
    def __init__(self, value, write=lambda *args, **kwargs: None):
        self.value = value
        self.write_callback = write

    def read(self):
        return json.dumps(self.value)

    def write(self, *args, **kwargs):
        self.write_callback(args, kwargs)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return True


class TestDocketter(TestCase):
    def setUp(self):
        self.home_path = 'home_path'
        self.patch_os_get_env = patch('docketter.os.getenv')
        mock_get_env = self.patch_os_get_env.start()
        mock_get_env.return_value = self.home_path

        self.patch_os_path_exists = patch('docketter.os.path.exists')
        self.mock_path_exists = self.patch_os_path_exists.start()
        self.mock_path_exists.return_value = False

        self.patch_os_make_dirs = patch('docketter.os.makedirs')
        mock_make_dirs = self.patch_os_make_dirs.start()
        mock_make_dirs.return_value = True

        self.patch_datetime = patch('docketter.datetime')
        self.patch_datetime.start()

        self.docketter = Docketter()

    def tearDown(self):
        self.patch_os_get_env.stop()
        self.patch_os_path_exists.stop()
        self.patch_os_make_dirs.stop()
        self.patch_datetime.stop()

    def test__log(self):
        template = '[{}] {}'
        message = 'MESSAGE'
        execution_value = list()

        patch_print = patch('docketter.print')
        mock_print = patch_print.start()
        mock_print.side_effect = lambda value: execution_value.append(value)

        now_value = "NOW"
        patch_datetime_now = patch('docketter.datetime.now')
        mock_dt_now = patch_datetime_now.start()
        mock_dt_now.return_value = now_value

        self.docketter._log(message)

        self.assertEqual(len(execution_value), 1)
        executed_value = execution_value[0]

        expected_value = template.format(now_value, message)

        self.assertEqual(expected_value, executed_value)

    def test__exec_command(self):
        instruction_to_be_executed = list()

        patch_subprocess_run = patch('docketter.subprocess.run')
        mock_run = patch_subprocess_run.start()
        mock_run.side_effect = (
            lambda value: instruction_to_be_executed.extend(value)
        )

        instructions = ['test', 'instruction']
        self.docketter._exec_command(instructions)

        self.assertEqual(len(instruction_to_be_executed), len(instructions))

    def test__get_configurations_path(self):
        expected_path = os.path.join(
            self.home_path, self.docketter.BASE_PATH, self.docketter.CONFIG_FILE
        )
        obtained_path = self.docketter._get_configurations_path()
        self.assertEqual(expected_path, obtained_path)

    def test__set_configurations(self):
        config = {
            'test': 'config'
        }

        patch_open_file = patch('docketter.open')
        mock = patch_open_file.start()
        mock.side_effect = lambda *args, **kwargs: MockFileOpen(config)

        self.mock_path_exists.return_value = True

        self.docketter._set_configurations()

        self.assertDictEqual(config, self.docketter.configurations)

        patch_open_file.stop()

    def test__save_configurations(self):
        config = {}
        write_counter = list()

        patch_open_file = patch('docketter.open')
        mock = patch_open_file.start()
        mock.side_effect = lambda *args, **kwargs: MockFileOpen(
            config,
            lambda *args, **kwargs: write_counter.append(args)
        )

        self.mock_path_exists.return_value = True

        self.assertEqual(len(write_counter), 0)
        self.docketter._save_configurations()
        self.assertTrue(len(write_counter) > 0)

        patch_open_file.stop()

    def test__check_healthy(self):
        self.docketter.configurations = dict()
        self.docketter._check_healthy()
        self.assertIn('dockers', self.docketter.configurations)
        self.assertIn('alias', self.docketter.configurations)

    def test_add_docker(self):
        self.docketter._save_configurations = lambda: None
        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        self.assertIn(name, self.docketter.configurations['dockers'])
        self.assertEqual(self.docketter.configurations['dockers'][name], path)
        self.assertIn(alias, self.docketter.configurations['alias'])
        self.assertEqual(self.docketter.configurations['alias'][alias], name)

    def test_add_alias(self):
        self.docketter._save_configurations = lambda: None
        name = 'name'
        alias = 'alias'

        self.docketter.add_alias(name, alias)

        self.assertIn(alias, self.docketter.configurations['alias'])
        self.assertEqual(self.docketter.configurations['alias'][alias], name)

    def test_get_docker_name(self):
        name = 'DOCKER_NAME'
        reference = self.docketter.get_docker_name(name)

        self.assertEqual(name, reference)

    def test_remove_alias(self):
        self.docketter._save_configurations = lambda: None
        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        # Remove name, not alias
        success = self.docketter.remove_alias(name)

        self.assertFalse(success)
        self.assertIn(alias, self.docketter.configurations['alias'])
        self.assertEqual(self.docketter.configurations['alias'][alias], name)

        # Remove the alias
        success = self.docketter.remove_alias(alias)

        self.assertTrue(success)
        self.assertNotIn(alias, self.docketter.configurations['alias'])

    def test_remove_docker(self):
        self.docketter._save_configurations = lambda: None
        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        # The docker can be removed by alias
        self.docketter.remove_docker(alias)

        self.assertNotIn(alias, self.docketter.configurations['alias'])
        self.assertNotIn(name, self.docketter.configurations['dockers'])

        self.docketter.add_docker(name, path, alias)

        # And can be removed using his name. But this not remove the alias
        self.docketter.remove_docker(name)

        self.assertNotIn(name, self.docketter.configurations['dockers'])

    def test__get_reference(self):
        self.docketter._save_configurations = lambda: None
        self.docketter._log = lambda value: None
        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        # The reference can be used with the name or the alias

        reference_name = self.docketter._get_reference(name)
        reference_alias = self.docketter._get_reference(alias)

        self.assertEqual(path, reference_name)
        self.assertEqual(path, reference_alias)
        self.assertEqual(reference_name, reference_alias)

        # If the docker is removed by name and try to get the reference using
        # his alias, the alias is removed

        self.docketter.remove_docker(name)
        self.assertIn(alias, self.docketter.configurations['alias'])

        reference = self.docketter._get_reference(alias)
        self.assertIsNone(reference)
        self.assertNotIn(alias, self.docketter.configurations['alias'])

    def test_run_docker(self):
        log_counter = list()
        exec_command_counter = list()

        self.docketter._save_configurations = lambda: None
        self.docketter._log = lambda value: log_counter.append(value)
        self.docketter._exec_command = (
            lambda value: exec_command_counter.append(value)
        )

        name = 'name'
        alias = 'alias'
        path = 'path'

        # Missing docker, log the case
        self.docketter.run_docker(alias)

        expected_log = 'Missing label {}'.format(alias)
        self.assertEqual(len(log_counter), 1)
        self.assertEqual(log_counter[0], expected_log)

        self.docketter.add_docker(name, path, alias)

        # Existent docker
        self.docketter.run_docker(alias)
        self.assertEqual(len(exec_command_counter), 1)

        expected_instruction = [
            'docker-compose',
            '-f',
            path,
            'up',
            '-d'
        ]

        self.assertListEqual(expected_instruction, exec_command_counter[0])

    def test_stop_docker(self):
        log_counter = list()
        exec_command_counter = list()

        self.docketter._save_configurations = lambda: None
        self.docketter._log = lambda value: log_counter.append(value)
        self.docketter._exec_command = (
            lambda value: exec_command_counter.append(value)
        )

        name = 'name'
        alias = 'alias'
        path = 'path'

        # Missing docker, log the case
        self.docketter.stop_docker(alias)

        expected_log = 'Missing label {}'.format(alias)
        self.assertEqual(len(log_counter), 1)
        self.assertEqual(log_counter[0], expected_log)

        self.docketter.add_docker(name, path, alias)

        # Existent docker
        self.docketter.stop_docker(alias)
        self.assertEqual(len(exec_command_counter), 1)

        expected_instruction = [
            'docker-compose',
            '-f',
            path,
            'stop'
        ]

        self.assertListEqual(expected_instruction, exec_command_counter[0])

    def test_get_dockers(self):
        self.docketter._save_configurations = lambda: None
        dockers = self.docketter.get_dockers()
        self.assertEqual(len(dockers), 0)

        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        dockers = self.docketter.get_dockers()
        self.assertEqual(len(dockers), 1)

        expected_docker = {
            'name': name,
            'docker': path
        }

        self.assertDictEqual(dockers[0], expected_docker)

    def test_get_aliases(self):
        self.docketter._save_configurations = lambda: None
        aliases = self.docketter.get_aliases()
        self.assertEqual(len(aliases), 0)

        name = 'name'
        alias = 'alias'
        path = 'path'

        self.docketter.add_docker(name, path, alias)

        aliases = self.docketter.get_aliases()
        self.assertEqual(len(aliases), 1)

        expected_alias = {
            'alias': alias,
            'docker': path
        }

        self.assertDictEqual(aliases[0], expected_alias)

if __name__ == '__main__':
    main()