# kwaf
Simple WAF security tester and bypasser. Works only on
mobile devices running the `termux` terminal emulator.

`DEVICE MUST BE ROOTED`

## installation
To obtain the latest source release of kwaf, download the git repository.
```
$ git clone https://github.com/PyDever/kwaf
```
To install kwaf, run `android-install.sh` in `termux`. 
```
$ bash android-install.sh
```

## building source
To build your own source-tree distribution, run the following command
in the `master` branch.
```
$ python2 setup.py build dist
```
The distribution can be found inside `build/kwaf.tar.gz`.
Unzip the tarball to obtain the distribution structure.
