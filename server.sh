#!/usr/bin/bash
service=uwsgi@social.service

usage() {
cat <<EOM
Usage: $(basename "$0") OPTIONS

Options:
    -r, --reboot     reboot the application
    -u, --upgrade    reboot the application, install requirements,
                     and upgrade the database
    -h, --help       show this help
EOM
}

# Display help if no options are specified.
[[ $# -eq 0 ]] && usage && exit 1

# Loop through options and set variables accordingly.
# The '-:' specifies long options.
while getopts ":ruh-:" arg;
do
    case $arg in
        -) # Use long options too.
            case "${OPTARG}" in
                reboot) reboot=true;;
                upgrade) upgrade=true;;
                help) usage && exit 0;;
                *) usage && exit 1;;
            esac;;
        r) reboot=true;;
        u) upgrade=true;;
        h) usage && exit 0;;
        \?) usage && exit 1;;
    esac
done

upgrade() {
    sudo systemctl stop $service
    source venv/bin/activate
    pip install -r requirements.txt
    flask db upgrade
    sudo systemctl start $service
    exit 0
}

[[ -n "$upgrade" ]] && upgrade

reboot() {
    sudo systemctl restart $service
}

[[ -n "$reboot" ]] && reboot

exit 0
