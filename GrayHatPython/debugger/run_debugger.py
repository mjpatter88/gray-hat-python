import my_debugger

debugger = my_debugger.Debugger()
# In order to attach to a 64-bit process, you must be running 64-bit version of python
pid = input("Enter the PID of the process to attach to: ")
debugger.attach(int(pid))
debugger.detach()
