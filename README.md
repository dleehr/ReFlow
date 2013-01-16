ReFlow
======

Repository for Flow Cytometry Data

Requirements
----

* django 1.4.2
* django-tastypie 0.9.11
* fcm 0.9 (https://code.google.com/p/py-fcm/)
* numpy 1.6.2
* scipy
* matplotlib

Installation
----

Note for Mac users: You'll need to get gfortran in addition to the command line tools (via Xcode). I recommend install gfortran using Homebrew (http://mxcl.github.com/homebrew/)

To install fcm, you'll need to first install numpy and then scipy. To install these via pip you will need a compiler

You'll probably want to install mercurial to get the latest fcm package via:

`pip install -e hg+https://code.google.com/p/py-fcm/#egg=fcm`
