sudo chmod 774 pish_posh
sudo chgrp www-data pish-posh
sudo chmod 774 pishposh/pish.db
sudo chgrp www-data pish-posh/pish.db
DBPATH=$(pwd)/pish.db
sudo sed -i -e 's/pish.db/$DBPATH/g'
sudo service apache2 reload