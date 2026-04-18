
import psutil

CRITICAL_PROCESSES = {
    "System", "smss.exe", "csrss.exe", "wininit.exe", 
    "services.exe", "lsass.exe", "winlogon.exe", 
    "fontdrvhost.exe", "dwm.exe", "svchost.exe"
}

def is_protected(pid):
    try:
        proc = psutil.Process(pid)
        name = proc.name().lower()
        if name in [p.lower() for p in CRITICAL_PROCESSES]:
            return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return True

def validate_action(pid, action_name="Action"):
    if is_protected(pid):
        return False, f"CRITICAL SYSTEM PROCESS PROTECTED: Cannot perform {action_name} on PID {pid}."
    return True, None
