# 📱 Android QA IAP Monitoring Console

A powerful desktop tool for monitoring Android in-app purchase (IAP) logs in real-time using ADB.

Designed for QA engineers and developers to track transactions, debug issues, and export logs efficiently.

---

## 🖼️ Application Preview

![App Screenshot](./assets/screenshot.png)

---

## 🚀 Features

* 🔌 Detect connected Android devices
* 📦 List installed packages
* 🔍 Search and filter packages
* 📊 Real-time logcat monitoring
* 💰 IAP transaction tracking
* 📁 Export transactions to CSV
* 🧾 Dedicated tabs:

  * Raw Logs
  * IAP Monitor
  * Errors
  * Crashes
  * Exceptions
  * Transactions
* ⚡ EXE support (no Python needed)
* 🛠️ Dev mode with virtual environment

---

## 📂 Project Structure

```
project-root/
│
├── app/                         # Main application source code
├── dist/                        # Built executable (EXE)
├── platform-tools/              # ADB tools
├── IAP_QA_MASTER_PACKAGE/       # Packaged release (final bundle)
├── venv/                        # Virtual environment (ignored in Git)
│
├── build_windows_master.bat     # Build EXE script
├── run_dev.bat                  # Run app in dev mode
├── setup.bat                    # Setup environment
├── environment.yml              # Environment config
├── IAP_Android_QA_Console.spec  # PyInstaller config
├── .gitattributes
├── README.md
├── LICENSE
```

---

## ⚙️ Quick Start (Easiest Way)

### 👉 Option 1: Run EXE (For QA / Testers)

1. Open:

```
dist/
```

2. Run:

```
AndroidQAConsole.exe
```

3. Connect Android device (USB debugging ON)

4. Click:

* Detect Devices
* List Packages
* Start Monitor

---

## ⚙️ Developer Setup (Using venv)

### Step 1: Setup environment

```
setup.bat
```

---

### Step 2: Run application

```
run_dev.bat
```

---

## 🛠️ Manual Dev Setup (Alternative)

### Activate venv

```
venv\Scripts\activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Run

```
python app/main.py
```

---

## 🏗️ Build EXE

Use provided script:

```
build_windows_master.bat
```

OR manually:

```
pyinstaller IAP_Android_QA_Console.spec
```

Output → `dist/`

---

## 📊 Transaction States

| State | Meaning |
| ----- | ------- |
| 0     | SUCCESS |
| 1     | FAILED  |
| 2     | PENDING |

---

## 📁 Export Features

* Export transactions → CSV
* Save logs → TXT
* Copy logs → Clipboard

---

## ⚠️ Important Notes

* Enable USB Debugging on Android device
* Authorize device when prompted
* Keep `platform-tools` folder available
* Logs depend on app implementation

---

## 🚫 Git Ignore (Important)

Do NOT push:

```
venv/
__pycache__/
build/
```

👉 You MAY push `dist/` if you want to share EXE

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and create PR

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Akash G
