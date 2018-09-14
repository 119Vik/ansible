from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.modules.utilities.helper import validate_data

from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args


class TestValidateData(ModuleTestCase):

    def setUp(self):
        super(TestValidateData, self).setUp()

    def test_without_required_parameters(self):
        """Failure must occurs when all parameters are missing"""
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            validate_data.main()

    def test_validation_success(self):
        """Positive result expected"""
        test_args = {
            "spec_file": "spec_file_path",
            "data_file": "data_file_path",
            "model_name": "some_model"
        }
        set_module_args(test_args)

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            run_command.return_value = 0, '', None
            with self.assertRaises(AnsibleExitJson) as result:
                validate_data.main()
                self.assertEqual(result.exception.args[0]['status'], "Valid")
                self.assertEqual(result.exception.args[0]['error_message'], "")

    def test_validation_failure(self):
        """Positive result expected"""
        test_args = {
            "spec_file": "spec_file_path",
            "data_file": "data_file_path",
            "model_name": "some_model"
        }
        set_module_args(test_args)

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            run_command.return_value = 1, '', 'Error'
            with self.assertRaises(AnsibleFailJson) as result:
                validate_data.main()
                self.assertEqual(result.exception.args[0]['status'], "Invalid")
                self.assertEqual(result.exception.args[0]['error_message'],
                                 "Error")

    def test_run_in_check_mode(self):
        test_args = {
            "spec_file": "spec_file_path",
            "data_file": "data_file_path",
            "model_name": "some_model",
            '_ansible_check_mode': True
        }
        set_module_args(test_args)

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            with self.assertRaises(AnsibleExitJson) as result:
                validate_data.main()
                self.assertEqual(result.exception.args[0]['status'], "Valid")
                self.assertEqual(result.exception.args[0]['error_message'], "")
            run_command.assert_not_called()

