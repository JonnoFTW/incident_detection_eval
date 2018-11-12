#!/bin/bash
source ~/.bashrc
source ~/.bash_profile
export PATH="$HOME/.pyenv/bin:$PATH:/home/mack0242/tools/bin"
pyenv local 2.7.12
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
#echo $ts $ds $method $si;'
echo $1 $2 $3 $4
python main.py $3 $1 $2 $4
