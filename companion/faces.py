from dataclasses import dataclass


@dataclass(frozen=True)
class Face:
    name: str
    rows: tuple[str, ...]


FACES = {
    "happy": Face("happy", (" .------. ", " | ^  ^ | ", " |  __  | ", " | \\__/ | ", " '------' ")),
    "calm": Face("calm", (" .------. ", " | -  - | ", " |      | ", " |  --  | ", " '------' ")),
    "curious": Face("curious", (" .------. ", " | o  ^ | ", " |   ?  | ", " |  __  | ", " '------' ")),
    "sleepy": Face("sleepy", (" .------. ", " | -  - | ", " |  zZ  | ", " |  --  | ", " '------' ")),
    "encourage": Face("encourage", (" .------. ", " | ^  ^ | ", " |  __  | ", " | /  \\ | ", " '------' ")),
}


def get_face(name: str) -> Face:
    return FACES.get(name, FACES["calm"])
