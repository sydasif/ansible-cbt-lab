## IP Address Filter

Filters in Ansible are powerful tools that let you manipulate data in various ways. A useful filter for network configuration is `ipaddr`. It allows you to work with IP addresses using the `netaddr` Python package. You can check if data are valid IP addresses and extract specific information. First, install the `netaddr` package:

```bash
$ python3 -m pip install netaddr
```

### Handling Network and IP Addresses

Here's a simple playbook demonstrating some capabilities of the `ipaddr` filter:

```yaml
---

- name: Handling network and IP addresses
  hosts: localhost
  gather_facts: false
  vars:
    ip_list:
      - "10.0.0.72/24"
      - "10.0.300.12"
      - "192.168.15.15"
      - "192.168.32.0/24"
  tasks:
    - name: Show information for network and IP
      ansible.builtin.debug:
        msg:
          - "Check this Addr...........: {{ item }}"
          - "A valid IP?...............: {{ item | ipaddr }}"
          - "Just the IP...............: {{ item | ipaddr('address') }}"
          - "Is this a network?........: {{ item | ipaddr('network') }}"
      loop: "{{ ip_list }}"
```

### Output

When you run this playbook, you get detailed information about each IP address in the list:

```bash
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ip_filter.yml

PLAY [Handling IP addresses] ***********************************************************

TASK [Show information for network and IP] *********************************************
ok: [localhost] => (item=10.0.0.72/24) => {
    "msg": [
        "Check this Addr...........: 10.0.0.72/24",
        "A valid IP?...............: 10.0.0.72/24",
        "Just the IP...............: 10.0.0.72",
        "Is this a network?........: 10.0.0.0"
    ]
}
ok: [localhost] => (item=10.0.300.12) => {
    "msg": [
        "Check this Addr...........: 10.0.300.12",
        "A valid IP?...............: False",
        "Just the IP...............: False",
        "Is this a network?........: False"
    ]
}
ok: [localhost] => (item=192.168.15.15) => {
    "msg": [
        "Check this Addr...........: 192.168.15.15",
        "A valid IP?...............: 192.168.15.15",
        "Just the IP...............: 192.168.15.15",
        "Is this a network?........: 192.168.15.15"
    ]
}
ok: [localhost] => (item=192.168.32.0/24) => {
    "msg": [
        "Check this Addr...........: 192.168.32.0/24",
        "A valid IP?...............: 192.168.32.0/24",
        "Just the IP...............: ",
        "Is this a network?........: 192.168.32.0"
    ]
}

PLAY RECAP *****************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0
```

In simple terms, this playbook checks each IP address in the list to see if it’s valid, extracts just the IP part, and checks if it’s a network address. This helps you manage and debug network configurations more effectively.
