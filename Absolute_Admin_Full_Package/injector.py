
import ctypes
import os
from sys_crash_stoper import validate_action

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

def inject_dll(pid, dll_path):
    safe, error_msg = validate_action(pid, "DLL Injection")
    if not safe:
        return False, error_msg

    if not os.path.exists(dll_path):
        return False, "DLL file not found."
    
    dll_path_bytes = dll_path.encode('utf-8')
    dll_len = len(dll_path_bytes)
    
    h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        return False, "Failed to open process."

    arg_address = ctypes.windll.kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, 0x04)
    ctypes.windll.kernel32.WriteProcessMemory(h_process, arg_address, dll_path_bytes, dll_len, None)
    
    h_kernel32 = ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll")
    load_lib_addr = ctypes.windll.kernel32.GetProcAddress(h_kernel32, b"LoadLibraryA")
    
    thread_id = ctypes.c_ulong(0)
    ctypes.windll.kernel32.CreateRemoteThread(h_process, None, 0, load_lib_addr, arg_address, 0, ctypes.byref(thread_id))
    
    ctypes.windll.kernel32.CloseHandle(h_process)
    return True, "Injection successful."
