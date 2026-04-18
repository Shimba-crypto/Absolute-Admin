
import psutil

def get_process_modules(pid):
    try:
        proc = psutil.Process(pid)
        modules = proc.memory_maps()
        return [m.path for m in modules if m.path.lower().endswith(('.dll', '.exe'))]
    except Exception as e:
        return [f"Error: {e}"]
