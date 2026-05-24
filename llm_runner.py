import os
import re
import shutil
import subprocess
from pathlib import Path

from openai import OpenAI


MODEL_NAME = "gpt-4.1-mini"

TESTCASE_DOCUMENT = Path("generated_testcases.md")
PYTEST_SCRIPT_DIR = Path("generated_scripts")
EXECUTION_REPORT = Path("ospf_test_report.txt")

LAB_CONTAINERS = [
    "clab-ringlab-r1",
    "clab-ringlab-r2",
    "clab-ringlab-r3",
    "clab-ringlab-r4",
    "clab-ringlab-r5",
]

TEST_GENERATION_REQUEST = """
Create an OSPF testcase document and one pytest file per testcase.

Lab containers:
- clab-ringlab-r1
- clab-ringlab-r2
- clab-ringlab-r3
- clab-ringlab-r4
- clab-ringlab-r5

Validation commands:
docker inspect <container> --format "{{.State.Running}}"
docker exec <container> vtysh -c "show ip ospf neighbor"
docker exec <container> vtysh -c "show ip route ospf"
docker exec <container> vtysh -c "show ip ospf"

Generate 5 OSPF functional testcases.

Testcase list:
TC01 - Verify all lab containers are running
TC02 - Verify every router has at least one OSPF neighbor
TC03 - Verify every discovered OSPF neighbor is in Full state
TC04 - Verify no OSPF neighbor is in bad states: Down, Init, ExStart, Exchange, Loading
TC05 - Verify OSPF routes are present on every router

For each testcase, include:
- Testcase ID
- Testcase name
- Objective
- Preconditions
- Steps
- Expected result

Pytest generation requirements:
- Generate one separate pytest file per testcase.
- Each pytest filename must start with test_.
- Each pytest file must be standalone and include its own imports and helper functions.
- Use subprocess for command execution.
- Do not configure or modify routers.
- Do not hardcode OSPF neighbor IDs.
- Discover OSPF neighbors dynamically from "show ip ospf neighbor".
- Parse FRR OSPF neighbor output using this column order:
  Neighbor ID | Pri | State | Up Time | Dead Time | Address | Interface
- The OSPF state value is the third column after splitting the neighbor line.
- A valid OSPF adjacency includes Full-state representations such as:
  Full
  Full/DR
  Full/Backup
- The generated pytest logic shall consider any neighbor state beginning with "Full" as a valid adjacency.
- Non-operational CLI warning messages shall not affect validation results.
- Each pytest file must print:
  Executing TCxx - <testcase name>
- Each pytest file must print useful command output or discovered data.
- Each assertion must have a useful failure message.
- Return Python code as plain text without markdown code blocks.

Output exactly in this format:

===TESTCASES_MD===
<markdown testcases with Testcase ID, Name, Objective, Preconditions, Steps, Expected Result>

===FILE: generated_scripts/test_TC01_verify_all_lab_containers_running.py===
<valid python pytest code>

===FILE: generated_scripts/test_TC02_verify_every_router_has_ospf_neighbor.py===
<valid python pytest code>

===FILE: generated_scripts/test_TC03_verify_ospf_neighbors_full_state.py===
<valid python pytest code>

===FILE: generated_scripts/test_TC04_verify_no_bad_ospf_neighbor_states.py===
<valid python pytest code>

===FILE: generated_scripts/test_TC05_verify_ospf_routes_present.py===
<valid python pytest code>

Do not output explanation outside the required format.
"""


def normalize_generated_artifact(content: str) -> str:
    return content.replace("```python", "").replace("```", "").strip()


def validate_lab_environment() -> None:
    print("Validating lab environment...")

    result = subprocess.run(
        ["docker", "exec", "clab-ringlab-r1", "vtysh", "-c", "show ip ospf neighbor"],
        text=True,
        capture_output=True,
    )

    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise RuntimeError(f"Unable to run OSPF validation command:\n{output}")

    if "full" not in output.lower():
        raise RuntimeError(f"OSPF Full neighbor state not found on r1:\n{output}")

    print("Lab validation completed.")
    print(output)


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    validate_lab_environment()

    print("Cleaning old generated files...")
    if PYTEST_SCRIPT_DIR.exists():
        shutil.rmtree(PYTEST_SCRIPT_DIR)

    TESTCASE_DOCUMENT.unlink(missing_ok=True)
    EXECUTION_REPORT.unlink(missing_ok=True)

    PYTEST_SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating testcase document and pytest files...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model=MODEL_NAME,
        input=TEST_GENERATION_REQUEST,
        temperature=0.1,
    )

    content = response.output_text

    print("Extracting testcase document...")
    testcase_match = re.search(
        r"===TESTCASES_MD===\s*(.*?)(?=\n===FILE:)",
        content,
        re.DOTALL,
    )

    if not testcase_match:
        raise RuntimeError("Could not find TESTCASES_MD section in LLM output")

    TESTCASE_DOCUMENT.write_text(testcase_match.group(1).strip() + "\n")
    print(f"Saved: {TESTCASE_DOCUMENT}")

    print("Extracting generated pytest files...")
    file_blocks = re.findall(
        r"===FILE:\s*(generated_scripts/test_[A-Za-z0-9_]+\.py)===\s*(.*?)(?=\n===FILE:|\Z)",
        content,
        re.DOTALL,
    )

    if len(file_blocks) != 5:
        raise RuntimeError(
            f"Expected 5 pytest files in model response, received {len(file_blocks)}"
        )

    generated_files = []

    for file_path, code in file_blocks:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        artifact_content = normalize_generated_artifact(code)
        path.write_text(artifact_content + "\n")

        generated_files.append(path)
        print(f"Saved pytest file: {path}")

    print("Running pytest on generated testcase-wise files...")
    pytest_result = subprocess.run(
        ["pytest", "-v", "-s", str(PYTEST_SCRIPT_DIR)],
        text=True,
        capture_output=True,
    )

    report = f"""
OSPF TEST EXECUTION REPORT

Generated files:
- {TESTCASE_DOCUMENT}
- {PYTEST_SCRIPT_DIR}/
- {EXECUTION_REPORT}

Generated testcase-wise pytest files:
{chr(10).join(str(path) for path in generated_files)}

Pytest return code:
{pytest_result.returncode}

STDOUT:
{pytest_result.stdout}

STDERR:
{pytest_result.stderr}
"""

    EXECUTION_REPORT.write_text(report)

    print(f"Saved report: {EXECUTION_REPORT}")
    print(report)


if __name__ == "__main__":
    main()
