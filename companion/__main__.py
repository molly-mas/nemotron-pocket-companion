from pathlib import Path

from .config import load_config
from .faces import get_face
from .hardware import Hardware
from .nemotron import NemotronClient


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "config.json")
    ai = NemotronClient(config)
    hardware = Hardware()

    print("Nemotron Pocket Companion — demo input loop")
    print("Try: task_done, idle, button, shake. Type quit to exit.")
    while True:
        try:
            event = input("event> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if event in {"quit", "exit"}:
            break
        if not event:
            continue
        reaction = ai.choose_reaction(event)
        print(f"reaction: {reaction}")
        hardware.apply(reaction, get_face(reaction.face))


if __name__ == "__main__":
    main()
