#!/bin/bash
WOLDIR=/usr/tools/wol
BOX=$1
xferOK=$2
RESPONSE=`curl -m 5 http://$BOX:9305/stop 2>/dev/null`
echo "Rsync and shadow copy unloaded"
if [ $xferOK -eq 1 ]; then
   if [ -f $WOLDIR/$BOX.state ]; then
      read wasoff < $WOLDIR/$BOX.state
      echo -n "State before backup: "
      echo $wasoff
      if [ "$wasoff" = "OFF" ]; then
         $WINEXE --authentication-file=$AUTHFILE //$BOX 'shutdown -f -s -c "Backup Completed"' <&-
         echo "System shut down"
      fi
   rm $WOLDIR/$BOX.state
   fi
fi
