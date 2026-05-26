# TaskTracerCLI
## Project Overview

This program is a lightweight, local **Task Tracker Command Line Interface (CLI)** that runs directly inside your terminal. It operates as a self-contained personal database assistant, allowing you to manage and organize a dynamic to-do list using simple, single-word terminal inputs.
**Project URL: https://roadmap.sh/projects/task-tracker**

### What the Program Can Do:

* **Create (`add`)**: Instantly creates a new task. It generates a unique tracking ID, sets its initial status to `"to do"`, and stamps it with the exact date and time it was entered.
* **Read (`list`)**: Scans your records to print out your tasks cleanly on the screen. It can show all items at once, or dynamically filter them based on their completion status:
    * `task-cli list "to do"`
    * `task-cli list "in progress"`
    * `task-cli list "done"`
* **Update (`update` / status change)**: 
    * Modifies the written description of any existing task by targeting its ID.
    * Transitions a task's lifecycle stage (e.g., shifting from `"to do"` to `"in progress"` or `"done"`).
    * Automatically rewrites the `updatedAt` timestamp so you can track precisely when the changes occurred.
* **Delete (`delete`)**: Permanently wipes out an existing task using its unique ID number and cleanly updates the tracking list.


### Installation & Setup

To use this application globally in your terminal as `task-cli`, follow these quick steps:

1. Clone this repository to your local machine.
2. Open your shell configuration profile (usually `~/.zshrc` or `~/.bashrc`).
3. Add the following alias to the bottom of the file, pointing to your downloaded path:
   ```bash
   alias task-cli="python3 /path/to/your/cloned/repo/task-cli.py"
4. Restart your terminal or run source ~/.zshrc.


