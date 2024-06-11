#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # Define module arguments
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default=''),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )

    # Create an AnsibleModule instance
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    state = module.params['state']

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    if state == 'present':
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.write(content)
            result['changed'] = True
            result['message'] = f'File {path} created.'
        else:
            with open(path, 'r') as file:
                current_content = file.read()
            if current_content != content:
                with open(path, 'w') as file:
                    file.write(content)
                result['changed'] = True
                result['message'] = f'File {path} updated.'
            else:
                result['message'] = f'File {path} already exists with the same content.'
    elif state == 'absent':
        if os.path.exists(path):
            os.remove(path)
            result['changed'] = True
            result['message'] = f'File {path} deleted.'
        else:
            result['message'] = f'File {path} does not exist.'

    # Exit the module with the result
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

