## Referencing Nested Variables

In Ansible, many variables and facts are organized in nested YAML or JSON data structures. Accessing values from these nested structures requires specific syntax, either using bracket notation or dot notation. Let's see how to reference these nested variables with a simple example.

### Using Bracket Notation

Bracket notation is helpful when variable names have special characters or might conflict with Python keywords. Here's how you can access an IP address from your facts using bracket notation:

```jinja
{{ ansible_facts["eth0"]["ipv4"]["address"] }}
```

### Using Dot Notation

Dot notation is more concise and readable but only works when variable names are valid Python identifiers. Here’s how you can access the same IP address using dot notation:

```jinja
{{ ansible_facts.eth0.ipv4.address }}
```

### Example Playbook

Let’s use a playbook to print out the OSPF network information of a router as an example:

```yaml
---
- name: "Print OSPF Network"
  hosts: router
  gather_facts: false

  tasks:
    - name: Print OSPF Network Information
      ansible.builtin.debug:
        msg: "{{ hostvars[ansible_host]['ospf']['network'] }}"
```

### Analyzing the Playbook Output

When we run this playbook, we get the following output:

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ospf_network.yaml 

PLAY [Print OSPF Network] *********************************************************************

TASK [Print OSPF Network Information] *********************************************************
ok: [172.16.10.14] => {
    "msg": [
        "10.10.10.0 0.0.0.255",
        "192.168.10.0 0.0.0.255",
        "172.16.10.0 0.0.0.255"
    ]
}

PLAY RECAP *******************************************************************************
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0    skipped=0  
```

#### Breakdown of the Output

- **Task Name**: Print OSPF Network Information
  - This task prints the value of the nested variable using the `ansible.builtin.debug` module.
- **Host**: 172.16.10.14
  - The playbook targets the host with the IP address `172.16.10.14`.
- **Message (`msg`)**:
  - The variable `hostvars[ansible_host]['ospf']['network']` contains a list of OSPF networks configured on the router.
  - The output shows three OSPF networks:
    - `10.10.10.0 0.0.0.255`
    - `192.168.10.0 0.0.0.255`
    - `172.16.10.0 0.0.0.255`

Understanding how to reference nested variables in Ansible allows you to dynamically access and manipulate detailed configurations and facts within your playbooks. By mastering these techniques, you can create more flexible and powerful Ansible automation scripts.
