from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class Debugger():
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False

    def load(self, path_to_exe):
        creation_flags = DEBUG_PROCESS
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessW(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print("[*] We have successfully launched the process!")
            print("[*] PID: {}".format(process_information.dwProcessId))
            return process_information.dwProcessId

        else:
            print("[*] Error: {}".format(kernel32.GetLastError()))

    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not h_process:
            print("[*] Error opening process: {}".format(kernel32.GetLastError()))
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)

        if kernel32.DebugActiveProcess(pid):
            print("[*] Attached to: {}".format(pid))
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print("[*] Unable to attach to the process: {}".format(kernel32.GetLastError()))

    def run(self):
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            input("Press a key to continue...")
            self.debugger_active = False
            if not kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status):
                print("[*] Unable to continue: {}".format(kernel32.GetLastError()))
            else:
                print("continued")

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("[*] Unable to stop debugging: {}".format(kernel32.GetLastError()))
            return False

