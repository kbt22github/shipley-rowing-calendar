import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# This script is stored in the publish repo folder
PUBLISH_DIR = BASE_DIR

# Working project folder with generate_ics.py and .venv
PROJECT_DIR = BASE_DIR.parent / "shipley-rowing-calendar"

ICS_SOURCE = PROJECT_DIR / "output" / "shipley-upper-school-rowing.ics"
ICS_DEST = PUBLISH_DIR / "shipley-upper-school-rowing.ics"
PYTHON_BIN = PROJECT_DIR / ".venv" / "bin" / "python"


def run(cmd, cwd=None):
    print(f"\n> {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}")


def main():
    if not PYTHON_BIN.exists():
        raise FileNotFoundError(f"Virtualenv python not found: {PYTHON_BIN}")

    print("=== Generating ICS ===")
    run([str(PYTHON_BIN), "generate_ics.py"], cwd=PROJECT_DIR)

    print("=== Copying ICS to publish repo ===")
    if not ICS_SOURCE.exists():
        raise FileNotFoundError(f"ICS file not found: {ICS_SOURCE}")

    shutil.copy2(ICS_SOURCE, ICS_DEST)

    print("=== Checking for changes ===")
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PUBLISH_DIR,
        capture_output=True,
        text=True,
    )

    if not result.stdout.strip():
        print("No changes detected. Skipping commit.")
        return

    print("=== Committing and pushing ===")
    run(["git", "add", "."], cwd=PUBLISH_DIR)
    run(["git", "commit", "-m", "Auto-update rowing calendar"], cwd=PUBLISH_DIR)
    run(["git", "push", "origin", "main"], cwd=PUBLISH_DIR)

    print("\nSync complete.")


if __name__ == "__main__":
    main()
