Demo recording: https://screen.studio/share/FleAp8M9

# Demo using firecracker to hotreload code

If you could pause a program, snapshot, and restart, at any point, you could have an execution environment for AI agents to rapidly iterate on code.
Instead of having them repeatedly run a test and check for failure, or attempt to use a debugger, have them run a program until it gets to the code they're writing and then repeatedly restart from that point.

# Setup

Start an AWS c5.metal instance.

```bash
# Install sky pilot for this.
$ uv venv --seed --python 3.10
$ uv pip install 'skypilot[aws]'
$ sky launch -c demo-cluster demo-sky.yaml
```

Server time.
For simplicity we'll use 3 different terminals.
The first will run our update server (it handles passing updated code to a VM so a snapshot-based VM can get updated code).
The second will run the actual VM; it will be where we execute our programs.
The third runs the utility scripts for setting up the VM and snapshotting the VM when necessary.

## Terminal 1 -- update server

```bash
# SSH in
$ ssh demo-cluster
$ cd sky_workdir
# Start update server
$ uv run update-server.py
```

## Terminal 2 -- VM

```bash
# SSH in
$ ssh demo-cluster
$ cd sky_workdir
# Start VM
$ ./step-2-run-fc.sh
```

## Terminal 3 -- setup

```bash
# SSH in
$ ssh demo-cluster
$ cd sky_workdir
# Setup the VM fresh.
$ ./step-3-start-fresh-fc.sh
```

# Running a program and snapshotting

After the setup steps, go to term-2 and run the in-fc setup script (at this point term-2 should have an interactive bash shell in a firecracker VM):

```bash
# Run the setup script. This will automatically kickoff example.py. Just ctrl-C if you don't want that.
$ ./step-5-in-fc-setup.sh
```

Run the program until you hit your breakpoint (e.g. the request for input in example.py).
Then in term-3 run the fork script:

```bash
$ ./step-6-fork-fc.sh
```

Now you'll have a snapshot at that point.

## Shutting down a VM

At any point in the firecracker VM you can run `reboot` to shutdown the VM.
e.g. You may want to do this when you've completed your first run and you want to reset from the snapshot.

## Starting from a snapshot

Start the VM in term-2:

```bash
$ ./step-2-run-fc.sh
```

Set it up from a snapshot in term-3:

```bash
$ ./step-3a-start-fc-from-snapshot.sh
```

term-2 will now be _at the breakpoint_ where you took the snapshot.
e.g. In `example.py` you'll hit enter and it will run the next iteration.

### Editing code

You can edit `example.py`'s `inner` function and it be changed on the next iteration.
This is currently hacky.
There is probably some nice generic implementation, but this repo is an experiment for an idea.
