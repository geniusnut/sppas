#!/usr/bin python
"""

@author:       Brigitte Bigi
@date:         2016-May-07
@contact:      brigitte.bigi@gmail.com
@license:      GPL, v3
@copyright:    Copyright (C) 2016  Brigitte Bigi

@summary:      Open an annotated file and print information about tiers.

"""

# ----------------------------------------------------------------------------
# Get SPPAS API
# ----------------------------------------------------------------------------

import sys
import os
from os.path import *
sys.path.append( join("..","..", "sppas", "src") )

import annotationdata.aio
from annotationdata import Transcription
from annotationdata import Tier

# ----------------------------------------------------------------------------
# Python imports
# ----------------------------------------------------------------------------

import wx


# ----------------------------------------------------------------------------
# WX Functions
# ----------------------------------------------------------------------------

def wxAskItem( message, choices ):
    """ Return the index of the selected item in choices, or -1 if the user cancelled. """

    selection = -1
    dialog = wx.SingleChoiceDialog(None, message, "Script: Tier information", choices)
    if dialog.ShowModal() == wx.ID_OK:
        selection = dialog.GetSelection()
    dialog.Destroy()
    return selection


def wxGetDir():
    """ Open a DirDialog and return a directory name with its path. """

    dirname = ''
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        dirname = dialog.GetPath()
    dialog.Destroy()
    return dirname


def wxGetFile():
    """ Open a FileDialog and return a filename with its path. """

    dirname = ''
    filename = ''

    dlg = wx.FileDialog(None, "Choose a file", dirname, "", "*.*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        filename = dlg.GetFilename()
        dirname = dlg.GetDirectory()
    dlg.Destroy()
    return os.path.join(dirname, filename)

def wxGetPattern():
    """ Open a TextEntryDialog and return a string. """

    pattern = ''
    dialog = wx.TextEntryDialog(None, "Pattern to count:")
    if dialog.ShowModal() == wx.ID_OK:
        pattern = dialog.GetValue()
    dialog.Destroy()
    return pattern


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------

def checkExtension(filename):
    """ Check if filename is supported by SPPAS. """

    # List of accepted extensions
    extensions = annotationdata.aio.extensions

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(filename)[-1].lower()

    # Check
    return ext in extensions


def printFreqAnn(filename, pattern):
    """ Print the number of occurrences of a pattern in each tier of a file. """

    print filename
    trs = annotationdata.aio.read( filename )
    pattern = pattern.strip()

    for tier in trs:
        c = 0
        for ann in tier:
            if ann.GetLabel().GetValue() == pattern:
                c = c + 1
        print " - ",tier.GetName(),c


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    """ This is the main function. """

    # Get the pattern to find
    pattern = wxGetPattern()
    if not len(pattern):
        sys.exit(0)

    # Ask whether the script will be applied on one file or
    # on all files of a directory.
    message = "Apply the script on:"
    choices = ['a single file', 'all files in a directory']
    item = wxAskItem(message,choices)

    if item == -1:
        sys.exit(0)

    elif item == 0:
        # Get a filename
        filename = wxGetFile()
        # the user said OK or Cancel?
        if not len(filename):
            sys.exit(0)
        # Verify if the extension is correct
        if not checkExtension(filename):
            wxShowErrorMessage( "Un-recognized file extension." )
            sys.exit(1)
        # Now, do the job!
        printFreqAnn(filename, pattern)

    elif item == 1:
        # Get a directory name
        dirname = wxGetDir()
        # Get the list of expected files in this directory
        files = [ f for f in os.listdir(dirname) if checkExtension(f) ]
        # Now, do the job, for each file!
        for f in files:
            printFreqAnn(os.path.join(dirname,f), pattern)
            # Let the result until a key is pressed.
            raw_input("Press a key to continue")

    # Let the result until a key is pressed.
    raw_input("Press a key to exit")


# ----------------------------------------------------------------------------
# This is the python entry point:
# Here, we start the wxpython application and ask to execute the main function.
if __name__ == '__main__':
    app = wx.App()
    main()
    app.MainLoop()

# ----------------------------------------------------------------------------
