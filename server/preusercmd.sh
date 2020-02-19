#!/bin/bash
BOX=$1
RESPONSE=`curl -m 5 http://$BOX:9305/start 2>/dev/null`
if [ $? -ne 0 ]; then
   exit 100
fi
for i in {1..180};do
  RESPONSE=`curl -m 5 http://$BOX:9305/status 2>/dev/null`
  if [ $? -ne 0 ]; then
    exit 100
  fi
  if [ "$RESPONSE" == "running" ]; then
    echo "Rsync and shadow copy loaded"
    exit 0
  fi
  sleep 1
done
exit 100
