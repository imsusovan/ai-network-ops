import subprocess


def run_docker_command(container, cmd):
    full_cmd = ["docker", "exec", container] + cmd

    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
    )

    return result.returncode, result.stdout, result.stderr
