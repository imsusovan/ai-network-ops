import subprocess


containers = [
    "clab-ringlab-r1",
    "clab-ringlab-r2",
    "clab-ringlab-r3",
    "clab-ringlab-r4",
    "clab-ringlab-r5",
]


def is_container_running(container):
    try:
        result = subprocess.run(
            ["docker", "inspect", container, "--format", "{{.State.Running}}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False


def test_all_lab_containers_running():
    print("Executing TC01 - Verify all lab containers are running")
    for container in containers:
        running = is_container_running(container)
        print(f"Container {container} running state: {running}")
        assert running, f"Container {container} is not running"
