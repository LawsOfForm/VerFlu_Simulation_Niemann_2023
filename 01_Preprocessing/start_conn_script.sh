#!/bin/bash

matlab -nodisplay -nojvm -nosplash -nodesktop -r \
	"try, data=pwd, run('SET_THE_PATH_WHERE_THE_SCRIPT_IS_SAVED/connpp_setup_ses.m'), catch, exit(1), end, exit(0);"
echo "matlab exit code: $?"

