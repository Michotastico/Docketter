from unittest import TestCase
from unittest.mock import patch

from docketter import Docketter


class TestDocketter(TestCase):
    def setUp(self):
        self.patch_os_get_env = patch('docketter.os.getenv')
        mock_get_env = self.patch_os_get_env.start()
        mock_get_env.return_value = 'home_path'

        self.patch_os_path_exists = patch('docketter.os.path.exists')
        mock_path_exists = self.patch_os_path_exists.start()
        mock_path_exists.return_value = False

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
        pass

    def test__set_configurations(self):
        pass

    def test__save_configurations(self):
        pass

    def test__check_healthy(self):
        pass

    def test_add_docker(self):
        pass

    def test_add_alias(self):
        pass

    def test_get_docker_name(self):
        pass

    def test_remove_alias(self):
        pass

    def test_remove_docker(self):
        pass

    def test__get_reference(self):
        pass

    def test_run_docker(self):
        pass

    def test_stop_docker(self):
        pass
