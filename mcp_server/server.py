from pathlib import Path
from mcp.server.fastmcp import FastMCP

import chromadb
from sentence_transformers import SentenceTransformer
import subprocess


mcp = FastMCP("ospf-test-automation")

DB_DIR = "rag/chroma_db"
COLLECTION_NAME = "ospf_test_knowledge"


@mcp.tool()
def get_topology() -> str:
    """Return lab topology YAML."""
    return Path("topology.yaml").read_text()


@mcp.tool()
def get_pytest_template() -> str:
    """Return pytest testcase guidance."""
    return Path("knowledge/pytest_template.md").read_text()


@mcp.tool()
def get_ospf_requirements() -> str:
    """Return OSPF testcase requirements."""
    return Path("knowledge/ospf_testcase_requirements.md").read_text()


@mcp.tool()
def search_knowledge(query: str) -> str:
    """Search knowledge base using semantic similarity."""

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2,
    )

    output = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0], strict=False):
        output.append(f"Source: {meta['source']}\n{doc}")

    return "\n\n" + "=" * 50 + "\n\n".join(output)


@mcp.tool()
def run_pytest() -> str:
    """Run pytest and return raw results."""

    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True,
    )

    return f"""
RETURN CODE: {result.returncode}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""


@mcp.tool()
def run_pytest_and_explain() -> str:
    """Run pytest and provide a summarized explanation of results."""

    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True,
    )

    output = result.stdout
    stderr = result.stderr

    summary = []

    if result.returncode == 0:
        summary.append("All tests passed successfully.")
    else:
        summary.append("Some tests failed.")

    failure_lines = []
    for line in output.splitlines():
        if "FAILED" in line or "ERROR" in line:
            failure_lines.append(line)

    if failure_lines:
        summary.append("\nFailures detected:")
        summary.extend(failure_lines)

    summary.append("\nPossible reasons if failures occur:")
    summary.append("- OSPF neighbors are not in FULL state")
    summary.append("- OSPF routes are missing")
    summary.append("- Docker containerlab links are not up")
    summary.append("- Wrong WSL distro or Docker context is being used")
    summary.append("- FRR ospfd daemon is not running")

    return f"""
SUMMARY:
{chr(10).join(summary)}

RETURN CODE:
{result.returncode}

RAW STDOUT:
{output}

RAW STDERR:
{stderr}
"""


if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
