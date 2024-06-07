## Test Your Ansible Setup - Playbook

A playbook is Ansible's configuration, deployment, and orchestration language. Each playbook is composed of one or more *plays* in a list. One *play* is a collection of one or more *tasks*, and a *task* is a single action that you want to execute through Ansible. In this section, we'll create a basic playbook to gather facts from an IOS device and display them using Ansible's debug module.

Here's an example playbook:

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

Let's break down the playbook:

1. **Playbook Definition**: The playbook starts with `---` to denote the beginning of a YAML document. Each playbook consists of one or more plays.

2. **Play Name**: The play is named "Playbook-1: Get ios facts". This is for your reference and helps identify the purpose of the play.

3. **Hosts**: The `hosts` directive specifies the target devices for this play. In this case, `all` means it will run on all hosts defined in your inventory.

4. **Gather Facts**: `gather_facts: false` means that Ansible's default fact-gathering mechanism is disabled. Instead, we'll use the `ios_facts` module to gather facts.
5. **Connection Type**: `connection: network_cli` indicates that the play will use CLI to connect to network devices.
6. **Tasks**: Each play consists of a list of tasks. In this play, we have two tasks:
    * **P1T1: Get config from ios_facts**: This task uses the `ios_facts` module to gather all possible facts from the IOS device. `gather_subset: all` means we are gathering all available facts.
    * **P1T2: Display debug message**: This task uses the `debug` module to display a custom message that includes the gathered facts. The message is dynamically generated using Jinja2 templating, inserting the device's hostname (`ansible_net_hostname`) and platform type (`ansible_net_iostype`).

### Running the Playbook

To run this playbook, ensure you have your inventory file set up correctly. Execute the playbook with the following command:

```bash
ansible-playbook playbook.yml
```

```json
zolo@u22s:~/ansible-networking-lab$ ansible-playbook 01_play.yaml 

PLAY [Playbook-1: Get ios facts] ********************************************************************************************************************

TASK [P1T1: Get config from ios_facts] **************************************************************************************************************
ok: [access1]
ok: [access2]
ok: [r1]
ok: [core-sw]

TASK [P1T2: Display debug message] ******************************************************************************************************************
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

PLAY RECAP ******************************************************************************************************************************************
access1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
access2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
core-sw                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
r1                         : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

This command tells Ansible to run the playbook (`playbook.yml`) using the specified inventory file.

Creating and running a simple Ansible playbook is a powerful way to automate tasks on network devices. This basic playbook gathers facts from an IOS device and displays them, providing a foundation you can build on for more complex automation workflows. Whether you're managing a small lab or a large production network, Ansible playbooks can help streamline your operations and reduce manual configuration efforts.
