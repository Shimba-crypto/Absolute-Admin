# Absolute Admin

Absolute Admin is a research-oriented Windows management toolkit. It offers a modern GUI for monitoring processes, inspecting modules, and safe task termination. Built for learning, it features a "crash-stopper" to prevent accidental interference with critical OS processes. Ideal for studying Win32 API and system administration.

## Features
* **Process Dashboard**: Real-time view of running processes with safety status.
* **Module Inspector**: View DLLs and EXEs loaded by any process.
* **Safety Guardrails**: Built-in `sys_crash_stoper.py` prevents termination of system-critical processes.
* **Controlled Injection**: Educational interface for DLL injection testing.
* **Modern UI**: Dark-themed dashboard built with `ttkbootstrap`.

## Safety Disclaimer
Educational Use Only. This software interacts with system processes and memory. It is designed for administrative research and educational purposes. While this tool includes safeguards to prevent interaction with critical OS components, users are strongly advised to test injection and termination features within a Virtual Machine (VM) to ensure system stability. The author is not responsible for any misuse or system instability caused by this software.

## Contributing
Contributions are welcome! If you find a bug or want to add a feature, please feel free to open an issue or submit a pull request.

## Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Shimba-crypto/Absolute-Admin.git](https://github.com/Shimba-crypto/Absolute-Admin.git)
   cd Absolute-Admin
