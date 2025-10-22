# debug.py
import os
import time
import traceback
from kivy.logger import Logger

# path on Android external storage - easy to open with file managers
LOG_FILE = "/sdcard/kivy_debug.log"

def _write_file(line):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    except Exception:
        pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            try:
                os.fsync(f.fileno())
            except Exception:
                # fsync might not be available, ignore
                pass
    except Exception as e:
        Logger.error(f"Debug: failed to write log file: {e}")

def log(msg, level="info", tag="APP"):
    """
    level: 'debug', 'info', 'warning', 'error'
    tag: short module name like 'Row', 'Logger', 'DB'
    """
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [{tag}] {msg}"
    # send to Kivy logger (shows up in logcat)
    try:
        if level == "debug":
            Logger.debug(line)
        elif level == "warning":
            Logger.warning(line)
        elif level == "error":
            Logger.error(line)
        else:
            Logger.info(line)
    except Exception:
        pass
    # also write to file
    _write_file(line)

def exc(tag="APP"):
    """Call from an except: block to log stack trace"""
    tb = traceback.format_exc()
    log(tb, level="error", tag=tag)