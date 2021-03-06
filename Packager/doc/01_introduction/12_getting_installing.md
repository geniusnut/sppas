## Getting and installing


### Websites

Since January 2016, the main website of SPPAS is located at the following 
URL:

<http://www.sppas.org>

The source code with recent stable releases is hosted on github.
From this website, anyone can download the development version,
contribute, send comments and/or declare an issue:

<https://github.com/brigittebigi/>



### External programs

On the main website, you will find information about the software 
requirements. In fact, other programs are required for SPPAS to operate.
Of course, they must be installed before using SPPAS, and *only once*.
This operation takes 5 up to 10 minutes depending on the operating 
system. 

The following software are required:

1. Python 2.7.x
2. wxPython >= 3.0
3. julius >= 4.1

It is very (very very) important to take care about the version of 
Python. An installation guide is available on the website, depending 
on the operating system. **Please, closely follow the instructions.**
Notice that administrator rights are required to perform the installations.


### Download and install SPPAS

The main website contains the `Download Page` to download a new version.

SPPAS is ready to run, so it does not need elaborate installation, except for
the other software required for SPPAS to work properly.
All you need to do is to copy the SPPAS package from the website to somewhere
on your computer. Choose *a location with only US-ASCII characters in the 
name of the path*.

The SPPAS package is compressed and zipped, so you will need to
*decompress and unpack* it once you've got it.

There is a unique version of SPPAS which does not depend on the operating
system. The only obvious difference depending on the system is how it looks
on the computer screen.

![Operating systems](./etc/logos/systemes.jpg)


### The SPPAS package

Unlike many other software tool, SPPAS is not what is called a "black box".
Instead, everything is done so that users can check / change operation.
It is particularly suitable for automatic annotations: it allows any user
to adapt automatic annotations to its own needs.

The package of SPPAS is then a directory with content as files and folders.

![SPPAS Package content](./etc/screenshots/explorer-sppas-folder.png)

The SPPAS package contains:

- the `README.txt` file, which aims to be read by users
- the files `sppas.bat` and `sppas.command` to execute the Graphical User Interface of SPPAS
- the `resources` directory contains data that are used by automatic annotations (lexicons, dictionaries, ...)
- the `samples` directory contains folders of data of various languages, they are sets of annotations freely distributed to test features of SPPAS
- the `sppas` directory contains the program itself
- the `documentation` directory contains:

    - the copyright
    - the printable documentation
    - the printable version of the main reference published in "the Phonetician" journal
    - the folder `scripting_solutions` is a set of python scripts corresponding 
      to the exercises proposed in the chapter "Scripting with Python and SPPAS"


### Update

SPPAS is constantly being improved and new packages are published 
frequently (about 10 versions a year). It is important to update 
regularly in order to get the latest functions and corrections.

Updating SPPAS is very easy and fast:

1. Download the last updated package from the SPPAS main web site;
2. Unpack the downloaded package;
3. Optionally, put the old one into the Trash.
