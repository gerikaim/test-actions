# check_directory_changes.py

import sys
import subprocess
import re

import hydra
from omegaconf import DictConfig, OmegaConf

def get_changed_files(base_sha, current_sha):
    cmd = ['git', 'diff', '--name-only', base_sha, current_sha]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        print(f"Error: Failed to get the changed files between {base_sha} and {current_sha}.")
        sys.exit(1)

def check_changes_for_patterns(files, patterns):
    for file in files:
        for pattern in patterns:
            if re.match(pattern, file):
                print(f"Matched: {file} with pattern {pattern}")
                return True
    return False

@hydra.main(version_base=None)
def main(cfg : DictConfig) -> None:
    AI_PATTERNS = [r"^ai/.*", r"^shared/.*"]
    UI_PATTERNS = [r"^ui/.*", r"^shared/.*"]
    SIM_PATTERNS = [r"^sim/.*", r"^shared/.*"]

    files = get_changed_files(cfg.base_sha, cfg.current_sha)

    print("Changed files:")
    for file in files:
        print(file)
    print("-------------------------")

    AI_CHANGED = "true" if check_changes_for_patterns(files, AI_PATTERNS) else "false"
    UI_CHANGED = "true" if check_changes_for_patterns(files, UI_PATTERNS) else "false"
    SIM_CHANGED = "true" if check_changes_for_patterns(files, SIM_PATTERNS) else "false"

    print(f"AI_CHANGED={AI_CHANGED}")
    print(f"UI_CHANGED={UI_CHANGED}")
    print(f"SIM_CHANGED={SIM_CHANGED}")

if __name__ == "__main__":
    main()
