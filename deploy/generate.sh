HOST=$(cat host.txt)
USERNAME=$(cat username.txt)

ssh-keygen -t rsa -b 4096 -C "$USERNAME@$HOST" -q -N "" -f id_rsa
ssh-copy-id -i id_rsa.pub $USERNAME@$HOST
