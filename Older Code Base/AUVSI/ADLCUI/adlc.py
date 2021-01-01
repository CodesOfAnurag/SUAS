import subprocess as sp
import time


while True:
    extProc = sp.Popen(['python','adlcui3.py'])
    time.sleep(10)
    sp.Popen.terminate(extProc)
