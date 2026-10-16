# GAAS Cluster Instructions for Agents

This file tells you (the coding agent) how to work with the GAAS cluster.

You run on the researcher's **local computer**. You are never installed or run on
the GAAS login node itself. When you need to do something on the cluster, you
reach it over SSH only, and you run work only through the PBS scheduler on
compute nodes.

Below is how to connect, how to synchronize approved project code, the
commands you will commonly use on the cluster, and the rules you must follow.

---

## Project-local configuration — confirmed during `SET-UP`

This is the **personalized project-local copy** for the `hello-world` project.
It was configured during onboarding and reviewed by the researcher. Never
store secrets in this file.

| Setting | Confirmed, project-specific value |
| --- | --- |
| Local agent runtime and local code working directory | opencode (terminal agent) in WSL2 Ubuntu 24.04 on Windows; local project: `/home/stvnpham/HPCC/hello-world` |
| Working SSH alias/command from the **agent's** local runtime | `ssh gaas` (key-based, verified non-interactive) |
| GAAS username | `pham0094` |
| GAAS code deployment destination, **actual PBS execution directory**, and job-script path | GAAS Git clone `/home/pham0094/hello-world` — this is also the **actual PBS execution directory**; job scripts live at the repository root (e.g. `hello_world.pbs`) |
| Other authorized GAAS paths and access level (read-only / read-write) | GAAS home `/home/pham0094`: default navigation only; `/home/pham0094/hello-world`: **read-write** (git pull, qsub, job outputs). No other GAAS paths authorized. |
| Code synchronization mode | Shared Git remote (Option A below) |
| Git remote and branch, **if shared Git** | GitHub `QuangPham2404/hello-world`, branch `main`. The **local** clone pushes via SSH (`git@github.com:QuangPham2404/hello-world.git`, key `~/.ssh/id_ed25519_github`). The **GAAS** clone pulls via the public HTTPS URL only — **no GitHub credentials on GAAS**. |
| Exact alternative synchronization procedure, **if applicable** | Not applicable |

Distinguish approved **code write/execute locations** from directories where
the researcher is permitted only to **read existing datasets/results**.
SSH access and filesystem visibility do not authorize access to unrelated
locations. Use only the paths and access levels explicitly confirmed with the
researcher and allowed by cluster policy.

---

## 1. SSH access

The connection below is the **confirmed working SSH configuration** for this
project (already present in the agent's local `~/.ssh/config` — do not modify
it; reuse it):

```sshconfig
Host gaas
    HostName 172.21.33.7
    User pham0094
    IdentityFile ~/.ssh/id_ed25519_gaas
    IdentitiesOnly yes
```

Authentication uses an SSH key; a local key passphrase, MFA challenge, or other
user-managed authentication step may still apply, depending on the environment.
Never ask the agent to collect or automate those credentials.

- **Human-operated terminal only:** `ssh gaas` opens an interactive login
  session. Coding agents must use the non-interactive form below instead.
- Run a single command using the approved **non-interactive** SSH connection:

```bash
ssh gaas "<command>"
```

Examples:

```bash
ssh gaas "hostname"
ssh gaas "qstat"
```

Always use one-shot, non-interactive SSH commands with the confirmed `gaas`
alias. Do not open an interactive
shell and type commands into it. Do not ask for, read, store,
echo, or log the SSH password. Never use `sshpass`, password files, or any tool
that enters a password automatically.

---

## 2. Code synchronization — use the approved project method

**This project uses Option A below (shared Git remote).** Option B is not
applicable.

### Option A — Shared Git remote (ACTIVE for this project)

In this mode, the project has two Git working copies that can access the
approved remote (GitHub `QuangPham2404/hello-world`, branch `main`).

- **Local clone** — `/home/stvnpham/HPCC/hello-world` (WSL2). Your primary
  workspace. This is where you read and edit files, prepare and review
  scripts, and make commits. You live and work here.
- **GAAS clone** — `/home/pham0094/hello-world`. The cluster-side copy. It is
  used only for what requires the cluster: compiling, submitting jobs, running
  cluster-specific software, and accessing GAAS resources. Its remote is the
  public HTTPS URL, so it is **pull-only** — never push from GAAS and never
  install GitHub credentials there.

When Option A is configured, keep them consistent through Git instead of
editing code independently in both places:

```text
Git remote (e.g. GitHub)
      ▲                ▲
  push/pull        push/pull
      │                │
  local clone      GAAS clone
      │                │
  you edit here    PBS / cluster execution
```

### Git rules (only for Option A)

- Before working in either clone, run `git status` to inspect its state.
- Prepare, review, and commit changes in the **local** clone, then `git push`
  when authorized.
- Bring the **GAAS** clone up to date with `git pull --ff-only` before using it
  to build or submit jobs. Verify the intended commit and scripts are present
  remotely before running anything.
- Do not store GitHub or cluster credentials on the cluster.
- If `git pull --ff-only` fails because the clones have diverged, stop and
  inspect the difference. Do not create a merge commit automatically and do not
  overwrite or delete the researcher's changes.

### Option B — Another explicitly approved synchronization method (Not applicable)

**This project does not use Option B.** It is retained only for reference: if
the project ever switches to a local-controlled transfer or another approved
non-shared-Git workflow, use **only its documented, approved procedure** and
source/destination paths. **Do not run `git push`, `git pull`, or `git status`
as mandatory steps on directories that are not Git repositories.** Do not
assume private GitHub credentials or keys are available on GAAS, and never
copy personal Git-host credentials to the cluster.

Before transferring code, confirm the source of truth, approved **individual
regular-file manifest**, destination, **actual PBS execution directory**,
and conflict/overwrite policy. If the project uses the local-controlled
SSH workflow, follow the **approved project-local procedure established
from Section 3B of `user_guide.md`**: dry-run preview, researcher review,
then explicit authorization for any destination replacements. Do not assume
the reusable setup package is present during ordinary project work.

Do not silently transfer datasets,
delete destination files, overwrite divergent work, or run destructive sync
options. Verify the intended code revision at the authorized GAAS working
path before job submission. **If no exact alternative procedure has been
approved, stop; do not invent one.**

**All methods:** Honor the approved project-directory allowlist, keep original
research data in place, and do not edit source on both sides without an
agreed reconciliation procedure.

---

## 3. Common cluster commands

The commands below use the confirmed `gaas` alias. The modules and job
commands are read-write but
non-destructive in normal use; use them as needed rather than treating this as
an exhaustive,
"nothing else is ever allowed" list. However, always honour the working rules at
the end of this section.

### Modules

```bash
ssh gaas "module avail"                      # list available modules
ssh gaas "module avail <name>"               # search for a matching module
ssh gaas "module list"                       # show currently loaded modules
ssh gaas "module show <module-name>"         # show what a module sets
ssh gaas "module load <module-name>"         # load a module
ssh gaas "module load <name>/<version>"      # load a specific version
ssh gaas "module swap <old> <new>"           # swap one loaded module for another
ssh gaas "module unload <module-name>"       # unload a module
ssh gaas "module purge"                      # unload all modules
```

### Submitting and managing PBS jobs

Use the configured **PBS execution directory** and correct job-script path.
Non-interactive SSH does not automatically start in the research project:
always `cd` into the approved remote working directory explicitly. For this
project the execution directory is `/home/pham0094/hello-world`:

```bash
ssh gaas 'cd /home/pham0094/hello-world && qsub <job-script>.pbs'
```

Submitting jobs requires the researcher's authorization; separately confirm
the **exact job ID** and obtain approval before `qdel` cancels any job. Do
not execute experimental code directly on the GAAS login node.

```bash
ssh gaas "qsub <job>.pbs"                              # submit a job (prints job-id)
ssh gaas "qsub -q <queue> <job>.pbs"                   # submit to a specific queue
ssh gaas "qstat"                                       # show your queued/running jobs
ssh gaas "qstat -u pham0094"                          # show jobs for one user
ssh gaas "qstat -f <job-id>"                           # show full details for one job
ssh gaas "watch -n 5 qstat -u pham0094"                # monitor jobs, refresh every 5s
ssh gaas "qdel <job-id>"                               # cancel a job
```

`watch` repeats its command and blocks until stopped (Ctrl+C); for non-blocking
monitoring, poll with repeated `qstat` calls instead.

### Inspecting job output

PBS writes each job's standard output and error to files named after the job,
for example `<job-name>.o<job-id>` and `<job-name>.e<job-id>`.

```bash
ssh gaas "cat <job-name>.o<job-id>"      # view standard output
ssh gaas "tail -n 50 <job-name>.o<job-id>"   # view the end of the output
ssh gaas "cat <job-name>.e<job-id>"      # view error output
```

### Basic navigation (inside the project's approved GAAS paths only)

```bash
ssh gaas "pwd"
ssh gaas "ls"
ssh gaas "cd <subdirectory> && pwd"
```

### Rules for working on the cluster

1. **Stay inside explicitly approved GAAS paths.** The researcher's home
   directory is the default; approved project/shared-group/scratch/data paths
   outside it are allowed **only** when the researcher has permission and
   GAAS policy permits their use. Use the project-local allowlist and observe
   each path's read-only or read-write scope. Do not infer permission simply
   from filesystem visibility or enter unrelated user/project directories.
2. **Do not run compute on the login node.** Never run computational work
   (builds, runs, experiments) directly on the login node. All compute must go
   through the scheduler — either a batch job (`qsub ...`) or an interactive job
   terminal.
3. **Prefer the local project for reading.** Read approved local code first
   when it contains enough information. Use SSH for information that genuinely
   requires GAAS, honoring the approved path allowlist and rules 1–2 above.

---

## 4. Example: submit a small job and check it

Use the **approved PBS code/execution directory** and an actual test script,
such as the minimal `gaas_setup_smoke.pbs` described in `user_guide.md`
Section 7. With authorization, create it in the local project, commit and push
from the local clone, then `git pull --ff-only` in the GAAS clone so the
script reaches the execution directory. **Do not assume it already exists on
the cluster.**

```bash
ssh gaas 'cd /home/pham0094/hello-world && git pull --ff-only && qsub gaas_setup_smoke.pbs'
ssh gaas "qstat -f <returned-job-id>"
```

Capture the returned PBS job ID,
and check the scheduler-designated output for `GAAS_SETUP_SMOKE_OK` and the
compute-node hostname. A finished job may no longer be displayed by `qstat`.
Do not run the test directly on the login node.

---

## 5. Cluster usage rules

Beyond the working rules in Section 3, you must also follow these:

- **Do not run computational work on the login node.** Use PBS jobs on compute
  nodes for anything that actually computes (builds, runs, experiments).
- **Do not install or launch another coding agent on the login node.** You are
  the agent, and you live on the local computer only.
- **Use SSH for remote operations.** The login node is not your development
  environment. Edit files locally and use SSH for the cluster-specific steps.
- **Work only in approved GAAS paths.** Honor the project's home, code,
  scratch, and dataset allowlist and each path's read/write permissions.
  Never inspect unrelated users' personal directories, run `find /`, or
  use `sudo`. Do not install software unless the researcher approves it.
- **Do not bypass cluster restrictions or exploit unintended system access.**