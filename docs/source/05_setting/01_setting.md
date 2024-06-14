## The Configuration File

Ansible uses a configuration file named `ansible.cfg` to change its behavior. Ansible looks for this file in the following order:

1. `ANSIBLE_CONFIG` (if set as an environment variable)
2. `ansible.cfg` (in the current directory)
3. `~/.ansible.cfg` (in the home directory)
4. `/etc/ansible/ansible.cfg`

Ansible uses the first configuration file it finds and ignores the rest. This order allows different configurations based on the context.

### The `ansible-config` Utility

The `ansible-config` utility helps you view, list, or dump Ansible’s settings. This tool makes it easier to manage and understand your Ansible configurations.

#### Viewing the Current Configuration

To print the content of your current `ansible.cfg` file, use:

```bash
ansible-config view
```

For example:

```bash
zolo@u22s:~/ansible-networking-lab$ ansible-config view
[defaults]
inventory=./inventory.cfg
gathering=explicit
host_key_checking=false
```

#### Dumping the Current Configuration

To see all of Ansible's current configuration settings, use:

```bash
ansible-config dump --only-changed
```

This command shows all the current configuration settings, making it easier to troubleshoot and understand Ansible's behavior.

#### Listing All Parameters

To list all parameters, their default values, and possible values you can set, use:

```bash
ansible-config list
```

This command helps you discover configurable options and understand Ansible’s defaults.

### How Ansible Works - Precedence Rules

Ansible offers multiple ways to control its behavior. Here’s the order of precedence from lowest to highest:

1. **Configuration settings**: Settings in your `ansible.cfg` file.
2. **Command-line options**: Flags and parameters passed directly on the command line.
3. **Playbook keywords**: Directives within your playbooks.
4. **Variables**: Values defined in your inventory files, playbooks, or directly in tasks.

Each higher-precedence category overrides the lower ones. For example, a playbook keyword will override any configuration setting.

### Example Configuration

Here’s an example `ansible.cfg` file for a typical lab setup:

```ini
[defaults]
inventory=./inventory.cfg
gathering=explicit
host_key_checking=false
deprecation_warnings=false
interpreter_python=auto
retry_files_enabled=false
```

- **inventory**: Path to the inventory file.
- **gathering**: Controls gathering of facts; `explicit` means facts are only gathered when explicitly requested.
- **host_key_checking**: Disables SSH key checking to avoid issues with new hosts.
- **deprecation_warnings**: Disables deprecation warnings to reduce clutter in output.
- **interpreter_python**: Automatically determines the Python interpreter to use.
- **retry_files_enabled**: Disables creation of retry files for failed playbook runs.

This configuration helps streamline Ansible’s operation, ensuring tasks run smoothly without unnecessary interruptions or checks.

By understanding and using these configuration options, you can tailor Ansible to fit your needs, improving efficiency and control over your automation tasks. The `ansible-config` utility helps by providing clear insights into current settings and available options.
