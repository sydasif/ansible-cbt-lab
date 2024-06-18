## Role Directory Structure

In the previous section, we explored what an Ansible role is and its benefits. Now, let's examine the specific structure of a role directory. The top-level directory is named after the role itself. Within this directory, there are several subdirectories, each serving a specific purpose. You can create this subdirectory structure manually or automatically using the command `ansible-galaxy init <folder_name>`.

### Creating a Role Directory

Let's create a top-level directory called `test_role`:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ansible-galaxy init test_role
- Role test_role was created successfully
```

This top-level directory, `test_role`, is the name of the role itself. The default structure is as follows:

```sh
(.venv) ➜  test_role git:(main) ✗ tree
.
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml

8 directories, 8 files
```

### Directory Descriptions

- **defaults**: Contains `main.yml` for default values.
  - Stores default variables for the role with low precedence.
- **files**: Used for static files that tasks may need to transfer to remote nodes.
  - No need to specify the path; the copy module automatically looks in this directory.
- **handlers**: Contains `main.yml` for handlers.
  - Handlers can be grouped together in this directory.
- **meta**: Stores metadata such as author, license, platform, and dependencies in `main.yml`.
- **README.md**: Provides information about the role.
  - Useful for documentation and sharing details about the role's purpose and usage.
- **tasks**: Contains `main.yml` for tasks.
  - Stores the tasks you want to run, similar to a playbook.
- **templates**: Stores Jinja2 configuration templates.
  - The role automatically finds templates in this directory.
- **tests**: Contains `inventory` and `test.yml` for testing the role.
  - Useful for testing your role in a lab environment.
- **vars**: Contains `main.yml` for variables.
  - Stores variables used within the role.

Understanding the structure of an Ansible role directory helps in organizing and managing your automation tasks effectively. Each directory serves a specific purpose, ensuring that your role is modular, reusable, and easy to maintain.
