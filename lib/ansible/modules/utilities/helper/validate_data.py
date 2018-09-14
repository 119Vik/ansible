#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: validate_data

short_description: This is my sample module

version_added: "2.4"

description:
    - "This module allows us validate data sample against schema"

options:
    spec_file:
        description:
            - Path to file with schema that data sample should be validated 
            againt of.
        required: true
    data_file:
        description:
            - Path to file with data sample that should be validated against 
            schema
        required: true
    model_name:
        description:
            - Name of the model in the schema file that data file should be 
            alligned with
        required: true
    
extends_documentation_fragment:
    - utilities

author:
    - Vitalii Kostenko (@119Vik)
'''

EXAMPLES = '''
# Pass in a message
- name: Validate data
  validate_data:
    spec_file: ~/file.schema
    data_file: ~/valid_file.sample
    model_name: SomeModel

# fail the module
- name: Validate data
  validate_data:
    spec_file: ~/file.schema
    data_file: ~/invalid_file.sample
    model_name: SomeModel
'''

RETURN = '''
status:
    description: Validation status
    type: str
error_message:
    description: Description of issue
    type: str
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        spec_file=dict(type='str', required=True),
        data_file=dict(type='str', required=True),
        model_name=dict(type='str', required=True)
    )
    result = dict(
        changed=False,
        status="valid",
        error_message=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    schema_file_name = module.params["spec_file"]
    data_sample_file_name = module.params["data_file"]
    model_name = module.params["model_name"]

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    # TODO: Find beeter way to find validate_sample executable
    cmd_template = "validate_sample {schema_file_name} {data_sample_file_name} {model_name}"

    cmd = cmd_template.format(
        schema_file_name=schema_file_name,
        data_sample_file_name=data_sample_file_name,
        model_name=model_name
    )

    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)

    if stderr:
        result['status'] = 'Invalid'
        result['error_message'] = stderr
        module.fail_json(msg='Validation Failed', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()