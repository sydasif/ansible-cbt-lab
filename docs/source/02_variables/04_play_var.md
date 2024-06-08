## Defining Variables within a Play

In Ansible, you can define variables directly within a play using the `vars` keyword. This approach allows for convenient configuration and access to variables specific to tasks executed within that play.

```yaml
- hosts: webservers
  vars:
    http_port: 80
```

In the example above, the `http_port` variable is set to `80` and is accessible to any tasks within the play targeting the `webservers` group.

### Registering variables

You can create variables from the output of an Ansible task with the task keyword register. You can use registered variables in any later tasks in your play. For example:

```yaml
# Playbook for configuring banners on Cisco devices
- name: "Configure Banners"
  hosts: all
  gather_facts: false

  tasks:
    - name: "Configure MOTD Banner"
      cisco.ios.ios_banner:
        banner: motd
        text: |
          This is my banner configured
          by ansible test lab with gns3
        state: present  # Ensure MOTD banner is configured

      register: banner_result  # Register the result for debugging

    - name: "Display Banner Configuration Result"
      ansible.builtin.debug:
        var: banner_result  # Display the result of banner configuration
```

Registered variables are stored in memory. You cannot cache registered variables for use in future playbook runs. Registered variables are only valid on the host for the rest of the current playbook run, including subsequent plays within the same playbook run.
