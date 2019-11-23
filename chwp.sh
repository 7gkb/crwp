#!/bin/bash

export DISPLAY=:0
/opt/crwp/crwp

PATHTOPIC="/opt/crwp/default_background.jpg"
dconf write /org/mate/desktop/background/picture-filename "'$PATHTOPIC'"
