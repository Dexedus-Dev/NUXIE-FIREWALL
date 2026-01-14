# safe_monitor.py
# ==========================================
# Safe Monitor Mode (READ-ONLY)
# - ไม่ขอสิทธิ์ Admin
# - ไม่แก้ Firewall / iptables
# - ไม่ติดตั้ง Npcap / libpcap อัตโนมัติ
# - ไม่รัน exe ภายนอก
# ใช้สำหรับ: ตรวจจับ, วิเคราะห์, เก็บ log, แสดงสถิติ
# ==========================================

import os
import sys
import time
import threading
from datetime import datetime

# =====================
# ADMIN (DISABLED)
# =====================
def request_admin():
    """
    ❌ ปิดการขอสิทธิ์ Administrator อัตโนมัติ
    เหตุผล: ความปลอดภัย และความโปร่งใส
    """
    return True


# =====================
# DASHBOARD AUTORUN (DISABLED)
# =====================
def check_run_deshbord():
    """
    ❌ ปิดการรันไฟล์ .exe ภายนอกอัตโนมัติ
    """
    return


# =====================
# PCAP CHECK (NO AUTO INSTALL)
# =====================
class PacketCaptureInstaller:
    def check_pcap_library(self):
        """
        ตรวจสอบ libpcap / Npcap เท่านั้น
        ❌ ไม่ติดตั้งให้อัตโนมัติ
        """
        try:
            import scapy.all  # noqa
            return True
        except Exception:
            return False


# =====================
# LOG SYSTEM
# =====================
LOG_FILE = "monitor.log"

def write_log(level, tag, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{tag}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


# =====================
# BLOCK SYSTEM (DISABLED)
# =====================
def block_ip(ip):
    """
    ❌ ปิดการ block IP จริง
    ใช้เพียงแจ้งเตือนเท่านั้น
    """
    msg = f"[MONITOR] ตรวจพบ IP น่าสงสัย: {ip} (ยังไม่ block)"
    print(msg)
    write_log(1, "DETECT", msg)


def force_unblock_ip(ip):
    """
    ❌ ปิดการ unblock จริง
    """
    pass


def unblock_ip_timer(ip, delay):
    """
    ❌ ไม่ใช้ในโหมด Monitor
    """
    pass


# =====================
# PACKET MONITOR
# =====================
def monitor_packet(packet):
    """
    โหมด READ-ONLY
    - วิเคราะห์ packet
    - ไม่แตะ firewall
    - ไม่ kill connection
    """
    try:
        src_ip = packet[0][1].src
        # ตัวอย่าง logic ตรวจจับ (ปรับได้)
        if src_ip.startswith("192.168.") is False:
            block_ip(src_ip)
    except Exception:
        pass


# =====================
# STATS LOOP
# =====================
def stats_loop(interval, label):
    while True:
        write_log(0, "STATS", f"update stats interval={label}")
        time.sleep(interval)


# =====================
# LOAD DATA
# =====================
def load_data_list():
    """
    โหลด blacklist / whitelist (ถ้ามี)
    """
    write_log(0, "INIT", "load data list completed")


# =====================
# MAIN
# =====================
def main():
    print("=== Safe Monitor Mode ===")
    print("Running in READ-ONLY mode")

    # ตัวอย่าง loop จำลอง
    while True:
        time.sleep(5)


# =====================
# ENTRY POINT
# =====================
if __name__ == "__main__":
    # ❌ ไม่ elevate สิทธิ์
    request_admin()

    # ❌ ไม่รัน exe
    check_run_deshbord()

    installer = PacketCaptureInstaller()

    # ✅ ตรวจสอบเท่านั้น
    if not installer.check_pcap_library():
        print("❌ ไม่พบ libpcap / Npcap")
        print("ℹ กรุณาติดตั้งด้วยตนเองก่อนใช้งาน")
        sys.exit(0)

    load_data_list()

    threading.Thread(target=stats_loop, args=(60, "1m"), daemon=True).start()
    threading.Thread(target=stats_loop, args=(300, "5m"), daemon=True).start()

    main()
