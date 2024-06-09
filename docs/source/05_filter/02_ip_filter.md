## IP address filter

As I explained in previous section, filters are a very powerful feature in Ansible that allow you to manipulate data in many different ways. One useful filtering example is network configuration. `ipaddr` is designed to provide an interface to the `netaddr` Python package from within Ansible. 

It can operate on strings or lists of items, test various data to check if they are valid IP addresses, and manipulate the input data to extract requested information. To use it, you need to make sure you have the `netaddr` Python package, which you can install using:

```bash
$ python3 -m pip install netaddr
```

### Handle network and IP addresses

The following playbook showcases a mere fraction of the things you can do with this powerful plugin:

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
    - name: Show information for network and ip
      ansible.builtin.debug:
        msg:
          - "Check this Addr...........: {{ item }}"
          - "A valid IP?...............: {{ item | ipaddr }}"
          - "Just the IP...............: {{ item | ipaddr('address') }}"
          - "Is this a network?........: {{ item | ipaddr('network') }}"
      loop: "{{ ip_list }}"
```

### Output

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ip_filter.yml

PLAY [Handling IP addresses] ***********************************************************

TASK [Show information for network and ip] *********************************************
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