"""A TAP state-transition model. It never opens a USB probe or target."""
import argparse

# Each pair is (next state for TMS=0, next state for TMS=1).
NEXT = {
    "Test-Logic-Reset": ("Run-Test/Idle", "Test-Logic-Reset"),
    "Run-Test/Idle": ("Run-Test/Idle", "Select-DR-Scan"),
    "Select-DR-Scan": ("Capture-DR", "Select-IR-Scan"),
    "Capture-DR": ("Shift-DR", "Exit1-DR"),
    "Shift-DR": ("Shift-DR", "Exit1-DR"),
    "Exit1-DR": ("Pause-DR", "Update-DR"),
    "Pause-DR": ("Pause-DR", "Exit2-DR"),
    "Exit2-DR": ("Shift-DR", "Update-DR"),
    "Update-DR": ("Run-Test/Idle", "Select-DR-Scan"),
    "Select-IR-Scan": ("Capture-IR", "Test-Logic-Reset"),
    "Capture-IR": ("Shift-IR", "Exit1-IR"),
    "Shift-IR": ("Shift-IR", "Exit1-IR"),
    "Exit1-IR": ("Pause-IR", "Update-IR"),
    "Pause-IR": ("Pause-IR", "Exit2-IR"),
    "Exit2-IR": ("Shift-IR", "Update-IR"),
    "Update-IR": ("Run-Test/Idle", "Select-DR-Scan"),
}


def walk(bits, state):
    for cycle, bit in enumerate(bits, 1):
        if bit not in "01":
            raise ValueError("TMS must contain only 0 and 1")
        old = state
        state = NEXT[state][int(bit)]
        print(f"{cycle:02d} TMS={bit}: {old} -> {state}")
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tms", default="1111101100")
    parser.add_argument("--start", choices=NEXT, default="Shift-DR")
    args = parser.parse_args()
    final = walk(args.tms, args.start)
    print(f"FINAL={final}; model only, no electrical/IDCODE test")


if __name__ == "__main__":
    main()
