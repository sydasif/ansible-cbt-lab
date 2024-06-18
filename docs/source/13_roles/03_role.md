## Creating Ansible Role

As we learned about the role directory structure, the next step is to create the structure of the role, populate it with the necessary data (such as variables and tasks), create a playbook to use the role, and ensure the role is portable and sharable without hardcoding your credentials.

### Creating the Role Structure

First, let's create the role directory structure using the `ansible-galaxy init` command. This command sets up the necessary directories and files for a new role.

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ansible-galaxy init ospf_role
- Role ospf_role was created successfully
```

### Populating the Role

We will convert the following playbook into an Ansible role:

#### Original Playbook

```yaml
---
- name: "PLAYBOOK - OSPF CONFIGURATION"
  hosts: 172.16.10.14
  gather_facts: false

  tasks:
    - name: "TASK 1 - CONFIG OSPF"
      cisco.ios.ios_config:
        src: "ospf.j2"

    - name: "TASK 2 - SHOW OSPF CONFIG"
      cisco.ios.ios_command:
        commands:
          - show run | sec ospf
      register: ospf_config

    - name: "TASK 3 - PRINT OSPF CONFIG"
      ansible.builtin.debug:
        msg: "{{ ospf_config.stdout_lines }}"
```

#### Variables for `172.16.10.14`

```yaml
ospf:
  process_id: 10
  router_id: 1.1.1.1
  networks:
    - network: 9.9.9.8
      mask: 0.0.0.3
    - network: 192.168.71.0
      mask: 0.0.0.255
```

#### Jinja2 Template `ospf.j2`

```python
router ospf {{ ospf.process_id }}
  router-id {{ ospf.router_id }}
  {% for network in ospf.networks %}
  network {{ network.network }} {{ network.mask }} area 0
  {% if ospf.router_id == '1.1.1.1' %}
  default-information originate
  {% endif %}
  {% endfor %}
```

### Creating the Role

With the role directory structure created, we will now populate it with the necessary tasks, templates, and variables.

#### Tasks

Copy the tasks from your playbook to `tasks/main.yml`:

```yml
---
# tasks file for ospf_role

- name: "TASK 1 - {{ TASK_ONE_NAME }}"
  cisco.ios.ios_config:
    src: "{{ ospf_template }}"

- name: "TASK 2 - {{ TASK_TWO_NAME }}"
  cisco.ios.ios_command:
    commands:
      - show run | sec ospf
  register: ospf_config

- name: "TASK 3 - {{ TASK_THREE_NAME }}"
  ansible.builtin.debug:
    msg: "{{ ospf_config.stdout_lines }}"
```

Note the use of generic task names and the removal of redundant `tasks` keywords.

#### Templates

Copy the Jinja2 `ospf.j2` template to the role's `templates` directory:

```python
router ospf {{ ospf.process_id }}
  router-id {{ ospf.router_id }}
  {% for network in ospf.networks %}
  network {{ network.network }} {{ network.mask }} area 0
  {% if ospf.router_id == '1.1.1.1' %}
  default-information originate
  {% endif %}
  {% endfor %}
```

#### Variables

Populate your variables into `defaults/main.yml`:

```yml
---
# defaults file for ospf_role
TASK_ONE_NAME: "OSPF CONFIGURATION"
TASK_TWO_NAME: "SHOW OSPF CONFIG"
TASK_THREE_NAME: "PRINT OSPF CONFIG"

ospf_template: "ospf.j2"
```

### Creating the Playbook to Run the Role

Now, create a playbook to utilize the role:

```yml
---
- name: "PLAYBOOK - OSPF CONFIGURATION"
  hosts: 172.16.10.14
  gather_facts: false

  roles:
    - ospf_role
```

### Running the Playbook

Execute the playbook to apply the OSPF configuration:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook ospf_role.yml

PLAY [PLAYBOOK - OSPF CONFIGURATION] ***************************************************

TASK [ospf_role : TASK 1 - OSPF CONFIGURATION] ****************************************************************************************
changed: [172.16.10.14]

TASK [ospf_role : TASK 2 - SHOW OSPF CONFIG] *******************************************
ok: [172.16.10.14]

TASK [ospf_role : TASK 3 - PRINT OSPF CONFIG] ******************************************
ok: [172.16.10.14] => {
    "msg": [
        [
            "router ospf 10",
            " router-id 1.1.1.1",
            " log-adjacency-changes",
            " network 9.9.9.8 0.0.0.3 area 0",
            " network 192.168.71.0 0.0.0.255 area 0",
            " default-information originate"
        ]
    ]
}

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=3    changed=1    unreachable=0    failed=0    skipped=0
```

### Conclusion

By following these steps, you can create an Ansible role, making your automation tasks modular, reusable, and easily shareable. Remember to avoid hardcoding credentials to ensure the role's portability and security.
