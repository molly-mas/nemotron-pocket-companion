# Nemotron Pocket Companion

A Linux/Raspberry Pi starter for a small mental-wellness companion. It sends a short, non-identifying event summary to a local **Nemotron 3 Nano 4B** model served by `llama.cpp`, parses a constrained reaction, then renders an ASCII face and dispatches named LED/haptic patterns through replaceable hardware adapters.

## Hardware and model notes

- Intended host: Raspberry Pi OS 64-bit / other ARM64 Linux, Raspberry Pi 5 (4 GB).
- Model: NVIDIA `NVIDIA-Nemotron-3-Nano-4B-GGUF`, e.g. the Q4_K_M file. This is **Nemotron 3 Nano 4B**, not the older Nemotron-Mini-4B-Instruct model.
- A 4B model is a tight fit on a 4 GB Pi. Model file size is not the full RAM requirement: OS, llama.cpp, context/KV cache, and Python also use memory. Start with a short context (`-c 1024`) and a lower-memory quant if Q4 runs out of memory. Expect CPU inference latency; this is a hackathon prototype, not a guaranteed real-time deadline.
- The application uses only Python's standard library. `gpiozero` is optional for the example GPIO adapter. The starter defaults to safe console output and makes no GPIO changes until explicitly configured.
- This is a supportive interaction toy, not a mental-health assessment or crisis device. The model only selects from fixed, prebuilt reactions; it cannot set raw GPIO values or motor durations.

## 1. Install llama.cpp on the Pi

Use an ARM64 Linux build of `llama.cpp` with server support. Follow the upstream build instructions for Raspberry Pi OS, or install a compatible packaged build. Verify `llama-server --version` works.

Download the official GGUF repository and choose a quant that fits available memory. For example, using Hugging Face CLI (install separately if needed):

```bash
mkdir -p models
hf download nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF \
  NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf \
  --local-dir models
```

If that exact filename is not listed in the repository, check its current file list and use the available Q4_K_M filename. The official model repository is <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF>.

Run the local inference server (in one terminal):

```bash
llama-server \
  -m models/NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf \
  --host 127.0.0.1 --port 8080 \
  -c 1024 -t 4
```

Use the actual downloaded filename. The NVIDIA repository currently lists the Q4_K_M file at about 2.84 GB, so this is a tight memory fit on a 4 GB Pi and may fail once system/runtime memory is included. If it does not fit, choose a smaller quant and reduce context. Keep the server bound to localhost for this single-device prototype.

## 2. Run the companion

In a second terminal:

```bash
cd nemotron-tamagotchi
python3 -m companion
```

Enter demo events such as `task_done`, `idle`, `button`, or `shake`. Enter `quit` to exit. If the model server is unavailable, the app uses a deterministic local fallback so the UI remains responsive.

## 3. Connect a physical screen, LED, and haptic motor

Edit `config.json`, then replace the TODO bodies in `companion/hardware.py` with the driver code for your parts. Hardware classes accept *named patterns* rather than arbitrary model-produced values.

Example screen/actuator modules:

- Small I2C/SPI LCD or OLED: render the `Face` rows from `companion/faces.py` using the panel's Python driver.
- LED: map `calm`, `success`, `encourage`, `celebrate` to fixed colors/patterns.
- Vibration motor: use a transistor/MOSFET motor driver and flyback protection as appropriate; never power a motor directly from a Pi GPIO pin. Keep pulse duration and intensity fixed in hardware code.
- Sensor: have a sensor reader produce one of the event names. Add debounce, thresholds and cooldowns before sending repeated events to the model.

The included `ConsoleDisplay`, `ConsoleLED`, and `ConsoleHaptics` are intentionally safe defaults. The optional `gpiozero` example uses a GPIO output only as a stub; adapt pin numbers and circuitry to your actual board and driver.

## Reaction contract

The model is prompted to return one JSON object:

```json
{"emotion":"proud","face":"happy","led":"success","haptic":"success","message":"Nice work!"}
```

All fields are allow-listed in `companion/reactions.py`. Invalid output, extra values, timeout, or server errors fall back to a local reaction. The message is capped and printed as a caption; the model does not generate screen art or control pins directly.

For privacy, send only simple event labels and optional coarse counters. Do not send names, free-form journal entries, or raw biometric streams. Treat signals as interaction cues, not as evidence of a user's mood or diagnosis.

## Project layout

```text
companion/
  __main__.py       demo CLI and event loop
  config.py         configuration loading
  faces.py          fixed ASCII face library
  hardware.py       screen / LED / haptic extension points
  nemotron.py       local OpenAI-compatible llama.cpp client
  reactions.py      prompt, validation, fixed fallback mapping
config.json
```
