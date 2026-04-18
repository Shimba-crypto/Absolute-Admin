
import psutil
from sys_crash_stoper import validate_action, is_protected

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def get_process_rank(pid):
    if is_protected(pid):
        return "Critical/Protect"
    return "Safe to Interact"

def terminate_process(pid):
    safe, error = validate_action(pid, "Termination")
    if not safe:
        return False, error
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True, "Success"
    except Exception as e:
        return False, str(e)
