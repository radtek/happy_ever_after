```sh
chmod 600 /etc/ssh/ssh_host_*_key
sed -i -e 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sed -i -e 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i -e 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g'       /etc/ssh/sshd_config
sed -i -e 's/#UsePAM no/UsePAM yes/g'                                  /etc/ssh/sshd_config
# sed -i -e 's/#X11Forwarding no/X11Forwarding yes/g'                    /etc/ssh/sshd_config
sed -i -e '/KexAlgorithms/d'                                           /etc/ssh/sshd_config
sed -i -e '$a \KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha1,diffie-hellman-group-exchange-sha256,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,sntrup761x25519-sha512@openssh.com'                 /etc/ssh/sshd_config
```