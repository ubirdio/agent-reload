# Demo using firecracker to hotreload code

If you could pause a program, snapshot, and restart, at any point, you could have an execution environment for AI agents to rapidly iterate on code.
Instead of having them repeatedly run a test and check for failure, or attempt to use a debugger, have them run a program until it gets to the code they're writing and then repeatedly restart from that point.

# Setup

Start an AWS c5.metal instance.

```bash
# Install sky pilot for this.
$ uv venv --seed --python 3.10
$ uv pip install 'skypilot[aws]'
$ sky launch demo-sky.yaml
```

SSH into the machine (see the output of the `sky` command).

Install `uv` on the server.

Run steps 0 & 1.

Run `uv run update-server.py`

Open a new terminal
