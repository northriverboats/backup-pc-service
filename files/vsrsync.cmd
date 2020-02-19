REM @ECHO OFF
REM *****************************************************************
REM
REM VSRSYNC.CMD - Batch file template to start your rsync command (s).
REM
REM By Michael Stowe
REM *****************************************************************

cd \BackupPC

SET CWRSYNCHOME=\BACKUPPC
SET CYGWIN=nontsec
SET CWOLDPATH=%PATH%
SET PATH=\BACKUPPC;%PATH%

DOSDEV B: %1

REM Priming the pump
dir B:\
dir B:\Users

REM Go into daemon mode, we'll kill it once we're done
rsync -v -v --daemon --config=rsyncd.conf --no-detach --log-file=diagnostic.txt

DOSDEV /D B:
