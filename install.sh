#!/bin/bash

py_path=$(which python)
echo '- Locate ptyhon path: '$py_path
sed -i '1s+^+#!'$py_path'\n+' chmgr.py
sudo mkdir -p /usr/local/bin
echo '- ln -s '$(pwd)'/chmgr.py /usr/local/bin/chmgr'
sudo ln -s $(pwd)/chmgr.py /usr/local/bin/chmgr
echo '- cp chmgr.conf '$HOME'/.config/chmgr.conf'
mkdir -p $HOME/.config
cp chmgr.conf $HOME/.config/chmgr.conf

echo 
echo 'Successfully installed.'
echo 'Please config in '$HOME'/.config/chmgr.conf first.'