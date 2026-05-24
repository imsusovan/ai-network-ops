import subprocess
import sys
from pathlib import Path

import yaml


TOPOLOGY_FILE = Path("topology.yaml")


def run_command(command):
    return subprocess.run(command, capture_output=True, text=True)


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def load_expected_containers():
    if not TOPOLOGY_FILE.exists():
        fail(f"{TOPOLOGY_FILE} was not found")

    with TOPOLOGY_FILE.open(encoding="utf-8") as file:
        topology = yaml.safe_load(file)

    nodes = topology.get("nodes", {})
    containers = [data.get("container") for data in nodes.values()]
    containers = [container for container in containers if container]

    if not containers:
        fail("No containers found in topology.yaml")

    return containers


def check_docker_available():
    result = run_command(["docker", "ps"])
    if result.returncode != 0:
        fail(
            "Docker is not available. Start Docker Desktop, confirm WSL integration, "
            f"then retry.\n{result.stderr}"
        )


def check_container_running(container):
    result = run_command(["docker", "inspect", container, "--format", "{{.State.Running}}"])
    if result.returncode != 0:
        fail(f"Container {container} was not found.\n{result.stderr}")

    if result.stdout.strip() != "true":
        fail(f"Container {container} exists but is not running")


def check_vtysh(container):
    result = run_command(["docker", "exec", container, "vtysh", "-c", "show ip ospf neighbor"])
    if result.returncode != 0:
        fail(f"vtysh OSPF neighbor check failed on {container}.\n{result.stderr}")


def main():
    containers = load_expected_containers()

    print("Checking Docker availability")
    check_docker_available()

    for container in containers:
        print(f"Checking container: {container}")
        check_container_running(container)
        check_vtysh(container)

    print("Lab readiness check passed")


if __name__ == "__main__":
    main()
