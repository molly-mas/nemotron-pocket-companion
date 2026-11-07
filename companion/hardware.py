"""Replace these safe console adapters with the drivers for your components."""

from .faces import Face
from .reactions import Reaction


class ConsoleDisplay:
    def show(self, face: Face, caption: str = "") -> None:
        print("\n" + "\n".join(face.rows))
        if caption:
            print(caption)


class ConsoleLED:
    def play(self, pattern: str) -> None:
        print(f"[LED pattern: {pattern}]")


class ConsoleHaptics:
    def play(self, pattern: str) -> None:
        print(f"[Haptic pattern: {pattern}]")


class GpioZeroLED:
    """Optional example. Add gpiozero and set LED_GPIO only after wiring a driver."""

    def __init__(self, pin: int):
        from gpiozero import LED
        self.led = LED(pin)

    def play(self, pattern: str) -> None:
        # TODO: map the allow-listed pattern to a safe color/blink sequence.
        self.led.on() if pattern != "off" else self.led.off()


class GpioZeroHaptics:
    """Skeleton only: drive a transistor/MOSFET input, never the motor directly."""

    def __init__(self, pin: int):
        from gpiozero import OutputDevice
        self.output = OutputDevice(pin, initial_value=False)

    def play(self, pattern: str) -> None:
        # TODO: implement fixed, short, named pulses with a strict maximum duration.
        # Keep the output off until a safe driver circuit and pulse policy are ready.
        if pattern == "off":
            self.output.off()


class Hardware:
    def __init__(self):
        self.display = ConsoleDisplay()
        self.led = ConsoleLED()
        self.haptics = ConsoleHaptics()

    def apply(self, reaction: Reaction, face: Face) -> None:
        self.display.show(face, reaction.message)
        self.led.play(reaction.led)
        self.haptics.play(reaction.haptic)
