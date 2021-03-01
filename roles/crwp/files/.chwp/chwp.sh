#!/bin/bash

sleep 5
dev=$(ip r | awk -F 'dev' '{ print $2}' | awk -F ' ' '{print $1}' | grep -v "tun" | head -n1)
getip=$(ip -f inet a show dev $dev | grep "inet" | awk -F' ' '{ print $2 }' | head -n1)
getmac=$(ip -f link a show dev $dev | grep "link/ether" | awk -F' ' '{ print $2 }')
pcname=$(hostname)
room="$(curl -G "http://192.168.5.186/pcs/?host=$pcname&ip=$getip&mac=$getmac" 2>/dev/null | awk -F 'Room: ' '{ print $2 }')"
if [ "$room" != ' ' ]; then
    echo $room > /opt/crwp/.room
fi
export DISPLAY=:0
/opt/crwp/crwp

PATHTOPIC="/opt/crwp/default_background.jpg"
dconf write /org/mate/desktop/background/picture-filename "'$PATHTOPIC'"
