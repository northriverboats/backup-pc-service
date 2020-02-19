# backup-pc-service
## To Edit Source Code and Work with GIT
1. Use Git Bash
2. `cd ../../Development`
3. `git clone git@github.com:northriverboats/backup-pc-service.git`
4. `cd backup-pc-service`

5. __Use windows shell__
6. `cd \Development\backup-pc-serice`
7. `\Python37\python -m venv venv`
8. `venv\Scripts\activate`
9. `python -m pip install pip --upgrade`
10. `pip install -r requirements.txt`
11. Remember to Create New Branch Before Doing Any Work

# Build Executable
`venv\Scripts\pyinstaller.exe --onefile --windowed --icon options.ico  --name "BackupPCService" "backup-pc-service.spec" backuppcservice.py`

# Installing
1. Copy `files` folder to PC as `C:\BackupPC`
2. Copy `dist\BackuppcService.exe` to `C:\BackupPC`
3. Run `firewall.cmd`
4. Edit `rsyncd.secrets` and set username:password
4. Run `BackuppcService install`
5. Run `BackuppcService start`

# Notes
1. There are `preusercmd.sh` and `postusercmd.sh` files for the backpc server.

# Security Issues
1. All access is served over HTTP not HTTPS
2. There is no login
3. The two major exploits would be a denial of service attack or stopping a backup from running everytime one is started.
