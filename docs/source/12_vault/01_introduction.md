## Protecting Sensitive Data with Ansible Vault

Ansible Vault provides a method to encrypt and manage sensitive data such as passwords. This section introduces you to the basics of Ansible Vault and how you can use encrypted variables and files in ad hoc commands and playbooks by supplying the passwords you used to encrypt them.

### Using Ansible Vault

Let's practice using Ansible Vault with a practical example. Assume you have a file in the `group_vars` directory named `all.yaml` with the following content:

```yaml
# Group_vars/cisco.yaml - Variables for all hosts
ansible_user: admin
ansible_password: cisco12
ansible_network_os: cisco.ios.ios
ansible_connection: ansible.netcommon.network_cli
```

This file contains a username and password in plain text. If you push this file to GitHub, anyone can see these credentials. This is a security risk. Instead, you should encrypt the credentials using Ansible Vault.

To get started with Ansible Vault, you can check the available options using the `--help` command:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-vault --help
usage: ansible-vault [-h] [--version] [-v] {create,decrypt,edit,view,encrypt,encrypt_string,rekey}

encryption/decryption utility for Ansible data files

positional arguments:
  {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
    create              Create new vault encrypted file
    decrypt             Decrypt vault encrypted file
    edit                Edit vault encrypted file
    view                View vault encrypted file
    encrypt             Encrypt YAML file
    encrypt_string      Encrypt a string
    rekey               Re-key a vault encrypted file

optional arguments:
  --version             show program's version number, config file location, configured module search path,
                        module location, executable location and exit
  -h, --help            show this help message and exit
  -v, --verbose         Causes Ansible to print more debug messages. Adding multiple -v will increase the
                        verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to
                        start is -vvv, connection debugging might require -vvvv.

See 'ansible-vault <command> --help' for more information on a specific command.
```

To encrypt an existing file, use the following command:

```sh
(.venv) ➜  group_vars git:(main) ✗ ansible-vault encrypt all.yaml
New Vault password: 
Confirm New Vault password: 
Encryption successful
```

You will be prompted to enter and confirm a password. After successful encryption, the file content will look like this:

```sh
(.venv) ➜  group_vars git:(main) ✗ cat all.yaml
$ANSIBLE_VAULT;1.1;AES256
31393465666434393833353661383431343930396634373634626461303831366135623830636264
3262346437376665363363326630343033373534336131660a383236303464353432343963616237
62383535313038306564653364333432376130623137623033393734663438636662373665623064
31653433666537333664623735323335656561633063643737383230396239323335
```

To verify the encryption, create a playbook:

```yaml
---
- name: Playbook - Ansible Vault
  hosts: router
  gather_facts: false

  tasks:
    - name: Print Credential
      debug:
        msg: "The username: {{ ansible_user }}, and password: {{ ansible_password }}"
```

If you run the playbook without providing the vault password, you will get an error:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook playbook/ansible_vault.yaml 

PLAY [Playbook - Ansible Vault] ******************************************************
ERROR! Attempting to decrypt but no vault secrets found
```

To run the playbook with the vault password, use the `--ask-vault-pass` option:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook playbook/ansible_vault.yaml --ask-vault-pass
Vault password: 

PLAY [Playbook - Ansible Vault] **********************************************************************

TASK [Print Credential] ******************************************************************************
ok: [172.16.10.14] => {
    "msg": "The username: admin, and password: cisco12"
}

PLAY RECAP ******************************************************************************************
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0    skipped=0
```

The playbook runs successfully, indicating that the encrypted credentials were decrypted and used correctly.
