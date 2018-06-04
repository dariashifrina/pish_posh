sudo chmod 774 pish_posh
sudo chgrp www-data pish_posh
sudo chmod 774 pish_posh/pish.db
sudo chgrp www-data pish_posh/pish.db
DBPATH=$(pwd)/pish_posh/pish.db
sudo sed -i -e "s|pish.db|$DBPATH|g" "pish_posh/db_stuff.py"
sudo service apache2 reload
