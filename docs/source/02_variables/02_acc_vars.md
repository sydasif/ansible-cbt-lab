## Referencing Nested Variables

Many registered variables (and facts) in Ansible are nested YAML or JSON data structures. Accessing values from these nested structures requires more than the simple `{{ foo }}` syntax. You must use either bracket notation or dot notation. Let's explore how to reference these nested variables and analyze their output with a practical example.

### Using Bracket Notation

Bracket notation is useful when your variable names contain special characters or if they might conflict with Python keywords. Here’s how you can access an IP address from your facts using bracket notation:

```jinja
{{ ansible_facts["eth0"]["ipv4"]["address"] }}
```

### Using Dot Notation

Dot notation is more concise and readable. However, it only works when variable names are valid Python identifiers. Here’s how you can access the same IP address using dot notation:

```jinja
{{ ansible_facts.eth0.ipv4.address }}
```

### Example Playbook

To illustrate how to reference nested variables, let's consider an example where we want to print out the OSPF network information of a router. We will use a playbook to achieve this:

```yaml
---
- name: "Load Variable"
  hosts: router
  gather_facts: false

  tasks:
    - name: Print Variable
      ansible.builtin.debug:
        msg: "{{ hostvars[ansible_host]['ospf']['network'] }}"
```

### Analyzing the Playbook Output

When we run the playbook, we get the following output:

```bash
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook access_vars.yaml 

PLAY [Load Variable] *********************************************************************

TASK [Print Variable] ********************************************************************
ok: [172.16.10.14] => {
    "msg": [
        "10.10.10.0 0.0.0.255",
        "192.168.10.0 0.0.0.255",
        "172.16.10.0 0.0.0.255"
    ]
}

PLAY RECAP *******************************************************************************
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Breakdown of the Output

- **Task Name**: Print Variable
  - This task uses the `ansible.builtin.debug` module to print the value of the nested variable.
- **Host**: 172.16.10.14
  - The playbook targets the host with the IP address `172.16.10.14`.
- **Message (`msg`)**:
  - The variable `hostvars[ansible_host]['ospf']['network']` contains a list of OSPF networks configured on the router.
  - The output shows three OSPF networks:
    - `10.10.10.0 0.0.0.255`
    - `192.168.10.0 0.0.0.255`
    - `172.16.10.0 0.0.0.255`

Understanding how to reference nested variables in Ansible is crucial for effectively managing and utilizing complex data structures within your playbooks. Whether using bracket notation or dot notation, correctly referencing these variables allows you to dynamically access and manipulate detailed configurations and facts. By mastering these techniques, you can create more flexible and powerful Ansible playbooks.
