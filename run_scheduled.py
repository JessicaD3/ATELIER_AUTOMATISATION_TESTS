import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import storage
from tester.runner import executer_tous_les_tests


def main():
    run = executer_tous_les_tests()
    storage.enregistrer_run(run)
    print(f"[run_scheduled] {run['timestamp']} — {run['summary']['passed']} réussis / {run['summary']['failed']} échoués")


if __name__ == "__main__":
    main()