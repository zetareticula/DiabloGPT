#!/bin/sh

# Remove the program
rm -rf /usr/local/bin/diablogpt-da-vinci-1

# Remove the data
rm -rf /usr/local/share/diablogpt-da-vinci-1

# Remove the configuration
rm -rf /usr/local/etc/diablogpt-da-vinci-1

# Remove the log
rm -rf /usr/local/var/log/diablogpt-da-vinci-1

# Remove the user
userdel diablogpt-da-vinci-1

# Remove the group
groupdel diablogpt-da-vinci-1

# Remove the service
rm -rf /etc/systemd/system/diablogpt-da-vinci-1.service

# Remove the logrotate
rm -rf /etc/logrotate.d/diablogpt-da-vinci-1




if [ $# -ne 1 ];then
    echo "Usage: `basename $0` <program>"
    exit 1
fi
program=$(echo $1 | tr '[:upper:]' '[:lower:]')

echo "remove $program"

rm -f $program package/$program -R

echo "Done."



