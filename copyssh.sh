#!/bin/sh
cp "${USERPROFILE}/.ssh/.*" /root/.ssh/
# echo list of .ssh folder
ls -la /root/.ssh/
# wait for prompt
read -p "Press enter to continue"
chmod 600 /root/.ssh/id_rsa
ssh-keyscan bitbucket.collectivemedicaltech.com >> /root/.ssh/known_hosts