#!/usr/bin/env python3

#- Colors -
GREEN = '\033[32m'
YELLOW = '\003[33m'
RED = '\033[31m'
WHITE = '\033[0m'

#- Alerts -
PRIMARY = '[' + GREEN + '>' + WHITE + '] '
SUCCESS = '[' + GREEN + '+' + WHITE + '] '
ALERT = '[' + YELLOW + 'i' + WHITE + '] '
WARNING = '[' + YELLOW + '!' + WHITE + '] '
ERROR = '[' + RED + '!' + WHITE + '] '

title = input(PRIMARY + 'Title: ')

with open('template/example/index_temp.html', 'r') as template:
    template_read = template.read()
    new_template = template_read.replace('$TITLE$', title)

with open('template/example/index.html', 'w') as new_index:
    new_index.write(new_template)