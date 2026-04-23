import customtkinter as ctk
import subprocess
import threading
import re
from datetime import datetime
from tkinter import filedialog, ttk
import csv
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AndroidQAConsole(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Android QA IAP Monitoring Console")
        self.geometry("1700x950")

        self.monitoring = False
        self.device_id = None
        self.selected_package = None
        self.package_list = []
        self.transactions = []

        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.abspath(".")

        self.adb_path = os.path.join(self.base_path, "platform-tools", "adb.exe")

        self.build_ui()

    # ================= UI =================

    def build_ui(self):

        header = ctk.CTkLabel(self, text="ANDROID QA IAP MONITORING CONSOLE",
                              font=("Arial", 24, "bold"))
        header.pack(pady=15)

        control = ctk.CTkFrame(self)
        control.pack(fill="x", padx=20, pady=10)

        self.device_menu = ctk.CTkOptionMenu(control, values=["No Device"])
        self.device_menu.grid(row=0, column=0, padx=10)

        ctk.CTkButton(control, text="Detect Devices",
                      command=self.detect_devices).grid(row=0, column=1, padx=10)

        ctk.CTkButton(control, text="List Packages",
                      command=self.list_packages).grid(row=0, column=2, padx=10)

        self.search_entry = ctk.CTkEntry(control, placeholder_text="Search Package")
        self.search_entry.grid(row=0, column=3, padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_packages)

        self.package_menu = ctk.CTkOptionMenu(control, values=["Select Package"])
        self.package_menu.grid(row=0, column=4, padx=10)

        ctk.CTkButton(control, text="Start Monitor",
                      command=self.start_monitor).grid(row=0, column=5, padx=10)

        ctk.CTkButton(control, text="Stop",
                      fg_color="red",
                      command=self.stop_monitor).grid(row=0, column=6, padx=10)

        # Tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.raw_tab = self.create_text_tab("Raw Logs")
        self.monitor_tab = self.create_text_tab("IAP Monitor")
        self.error_tab = self.create_text_tab("Errors")
        self.crash_tab = self.create_text_tab("Crashes")
        self.exception_tab = self.create_text_tab("Exceptions")

        self.create_transaction_tab()

    # ================= TEXT TAB BUILDER =================

    def create_text_tab(self, name):

        tab = self.tabs.add(name)

        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=5, pady=5)

        text_area = ctk.CTkTextbox(tab)
        text_area.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Save",
                      command=lambda: self.save_text(text_area)).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="Copy",
                      command=lambda: self.copy_text(text_area)).pack(side="left", padx=5)

        return text_area

    # ================= TRANSACTION TAB =================

    def create_transaction_tab(self):

        tab = self.tabs.add("Transactions")

        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(button_frame, text="Export CSV",
                      command=self.export_transactions_csv).pack(side="left", padx=5)

        columns = ("timestamp", "package", "product_id", "order_id",
                   "purchase_token", "purchase_state", "status")

        self.tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=220)

        # Row color tags
        self.tree.tag_configure("SUCCESS", background="#1e3d2b", foreground="white")
        self.tree.tag_configure("FAILED", background="#5c1f1f", foreground="white")
        self.tree.tag_configure("PENDING", background="#5c4a1f", foreground="white")
        self.tree.tag_configure("UNKNOWN", background="#3a3a3a", foreground="white")

        self.tree.pack(fill="both", expand=True)

    # ================= DEVICE =================

    def detect_devices(self):
        result = subprocess.run([self.adb_path, "devices"],
                                capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]
        devices = [line.split("\t")[0] for line in lines if "device" in line]

        if devices:
            self.device_menu.configure(values=devices)
            self.device_menu.set(devices[0])
            self.device_id = devices[0]

    def list_packages(self):
        self.device_id = self.device_menu.get()
        result = subprocess.run(
            [self.adb_path, "-s", self.device_id, "shell", "pm", "list", "packages"],
            capture_output=True, text=True
        )
        self.package_list = [line.replace("package:", "").strip()
                             for line in result.stdout.split("\n") if line]
        if self.package_list:
            self.package_menu.configure(values=self.package_list)
            self.package_menu.set(self.package_list[0])

    def filter_packages(self, event):
        search = self.search_entry.get().lower()
        filtered = [p for p in self.package_list if search in p.lower()]
        if filtered:
            self.package_menu.configure(values=filtered)
            self.package_menu.set(filtered[0])

    # ================= MONITOR =================

    def start_monitor(self):
        self.device_id = self.device_menu.get()
        self.selected_package = self.package_menu.get()

        subprocess.run([self.adb_path, "-s", self.device_id, "logcat", "-c"])

        self.monitoring = True
        thread = threading.Thread(target=self.stream_logs)
        thread.daemon = True
        thread.start()

    def stop_monitor(self):
        self.monitoring = False

    def stream_logs(self):

        process = subprocess.Popen(
            [self.adb_path, "-s", self.device_id, "logcat"],
            stdout=subprocess.PIPE,
            text=True,
            errors="ignore"
        )

        while self.monitoring:
            line = process.stdout.readline()
            if not line:
                continue

            self.raw_tab.insert("end", line)
            self.raw_tab.see("end")

            if "GOOGLEIAP" in line or (self.selected_package and self.selected_package in line):

                self.monitor_tab.insert("end", line)
                self.monitor_tab.see("end")

                product = self.extract_field(line, "productId")
                order = self.extract_field(line, "orderId")
                token = self.extract_field(line, "purchaseToken")
                state = self.extract_field(line, "purchaseState")

                if not state:
                    state_match = re.search(r'purchaseState=(\d)', line)
                    if state_match:
                        state = state_match.group(1)

                if token:

                    status = self.get_status(state)

                    txn = (
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.selected_package,
                        product,
                        order,
                        token,
                        state,
                        status
                    )

                    self.transactions.append(txn)

                    self.tree.insert("", "end",
                                     values=txn,
                                     tags=(status,))

            if " E " in line:
                self.error_tab.insert("end", line)

            if "FATAL EXCEPTION" in line or "AndroidRuntime" in line:
                self.crash_tab.insert("end", line)

            if "Exception" in line:
                self.exception_tab.insert("end", line)

        process.kill()

    # ================= EXPORT =================

    def export_transactions_csv(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")],
            title="Export Transactions"
        )

        if file_path:
            if not file_path.endswith(".csv"):
                file_path += ".csv"

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Package", "Product ID",
                                 "Order ID", "Purchase Token",
                                 "Purchase State", "Payment Status"])
                writer.writerows(self.transactions)

    # ================= UTIL =================

    def extract_field(self, line, field):
        match = re.search(rf'"{field}":"(.*?)"', line)
        if match:
            return match.group(1)

        match2 = re.search(rf'{field}=(.*?)[,\s]', line)
        if match2:
            return match2.group(1)

        return ""

    def get_status(self, state):
        if state == "0":
            return "SUCCESS"
        elif state == "1":
            return "FAILED"
        elif state == "2":
            return "PENDING"
        return "UNKNOWN"

    def save_text(self, textbox):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")],
            title="Save Logs"
        )
        if file_path:
            if not file_path.endswith(".txt"):
                file_path += ".txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(textbox.get("1.0", "end"))

    def copy_text(self, textbox):
        self.clipboard_clear()
        self.clipboard_append(textbox.get("1.0", "end"))


if __name__ == "__main__":
    app = AndroidQAConsole()
    app.mainloop()