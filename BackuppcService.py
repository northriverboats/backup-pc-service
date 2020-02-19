import servicemanager
import socket
import os
import sys
import win32event
import win32service
import win32serviceutil
import pythoncom
import time
import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from win32com.client import Dispatch
from pythoncom import CoInitialize  # pylint: disable=E0611
hostName = "0.0.0.0"
hostPort = 9305

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects

class MyServer(BaseHTTPRequestHandler):
    def kill_rsyncd(self):
        procs = findProcessIdByName('rsync.exe')
        if procs:
            process = psutil.Process(procs[0]['pid'])
            process.terminate()
            time.sleep(2)
        try:
            os.remove(r"\BackupPC\rsyncd.pid")
        except OSError:
            pass

    def _status(self):
        rsync = findProcessIdByName('rsync.exe')
        vscsc = findProcessIdByName('vscsc.exe')
        if rsync:
            status = "running"
        elif vscsc:
            status = "snapshotting"
        else:
            status = "idle"
        return status
    
    def status(self):
        message = self._status()
        self.output(message)

    def start(self):
        # must delete PID if it exists and stop rsyncd.exe
        self.kill_rsyncd()
        try:
            CoInitialize()
            shell = Dispatch("WScript.Shell")
            shell.Run(r"\BackupPC\backuppc.cmd > C:\BackupPC\file.out")
        except Exception as e:
            self.output(e)
        self.output("starting")

    def stop(self):
        self.kill_rsyncd()
        self.output("stopping")
    
    def not_found(self):
        message = "You accessed path: {}".format(self.path)
        self.output(message)

    def output(self, message):
        self.wfile.write(bytes("{}".format(message), "utf-8"))

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()

    # GET is for clients geting the predicate
    def do_GET(self):
        self._set_headers()
        parts = self.path.split(r"/")
        command = parts[1]
        if command == 'status': self.status()
        elif command == 'start': self.start()
        elif command == 'stop': self.stop()
        else: self.not_found()


class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BackupPCService"
    _svc_display_name_ = "Backup PC Service"
    _svc_description_ = "Comand and control service for BackupPC"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.server = None
        self.running = True

    def SvcStop(self):
        self.running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.server = HTTPServer((hostName, hostPort), MyServer)
        self.server.timeout = 2
        while self.running:
            try:
                self.server.handle_request()
            except KeyboardInterrupt:
                pass
        self.server.server_close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)