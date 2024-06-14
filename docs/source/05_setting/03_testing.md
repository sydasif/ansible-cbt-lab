## Test Your Ansible Setup - Playbook

A playbook is Ansible's way of defining configurations, deployments, and orchestrations. It consists of one or more *plays*, and each play contains a series of *tasks*. A task is a single action you want Ansible to perform. Here, we'll create a simple playbook to gather facts from an IOS device and display them using Ansible's debug module.

### Example Playbook

Here's a basic playbook:

```yaml
---
- name: "Playbook-1: Get ios facts"
  hosts: all
  gather_facts: false
  connection: network_cli
  
  tasks:
    - name: "P1T1: Get config from ios_facts"
      ios_facts:
        gather_subset: all

    - name: "P1T2: Display debug message"
      debug:
        msg: "The {{ ansible_net_hostname }} has {{ ansible_net_iostype }} platform"
```

### Understanding the Playbook

1. **Playbook Definition**: Starts with `---` to indicate the beginning of a YAML document. A playbook can have one or more plays.

2. **Play Name**: "Playbook-1: Get ios facts" helps identify what this play does.

3. **Hosts**: `hosts: all` means this play will run on all hosts listed in your inventory.

4. **Gather Facts**: `gather_facts: false` disables Ansible's default fact-gathering. Instead, we'll gather facts using the `ios_facts` module.

5. **Connection Type**: `connection: network_cli` specifies that we are connecting to network devices using the CLI.

6. **Tasks**: Each play has a list of tasks. This play has two tasks:

- **P1T1: Get config from ios_facts**: Uses the `ios_facts` module to gather all facts from the IOS device (`gather_subset: all`).
- **P1T2: Display debug message**: Uses the `debug` module to show a message with the device's hostname (`ansible_net_hostname`) and platform type (`ansible_net_iostype`).

### Running the Playbook

To run this playbook, ensure your inventory file is correctly set up. Then, run the playbook with this command:

```bash
ansible-playbook playbook.yml
```

### Example Output

When you run the playbook, you might see output like this:

```
zolo@u22s:~/ansible-networking-lab$ ansible-playbook playbook.yml

PLAY [Playbook-1: Get ios facts] ***************

TASK [P1T1: Get config from ios_facts] *********
ok: [access1]
ok: [access2]
ok: [r1]
ok: [core-sw]

TASK [P1T2: Display debug message] *************
ok: [r1] => {
    "msg": "The r1 has IOS platform"
}
ok: [access1] => {
    "msg": "The access1 has IOS platform"
}
ok: [core-sw] => {
    "msg": "The core-sw has IOS platform"
}
ok: [access2] => {
    "msg": "The access2 has IOS platform"
}

PLAY RECAP ****************************************************************
access1                    : ok=2    changed=0    unreachable=0    failed=0
access2                    : ok=2    changed=0    unreachable=0    failed=0
core-sw                    : ok=2    changed=0    unreachable=0    failed=0
r1                         : ok=2    changed=0    unreachable=0    failed=0
```

This command tells Ansible to execute the playbook (`playbook.yml`) using your inventory file.

Creating and running a simple Ansible playbook is a powerful way to automate tasks on network devices. This basic playbook gathers facts from an IOS device and displays them, providing a foundation you can build on for more complex automation workflows. Whether you're managing a small lab or a large production network, Ansible playbooks can help streamline your operations and reduce manual configuration efforts.
