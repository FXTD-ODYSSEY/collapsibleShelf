# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-3-20 12:21:24'

"""
"""

from maya import cmds 
from maya import mel 
from maya import OpenMayaUI

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import wrapInstance


def mayaToQT(name):
    """
    Maya -> QWidget

    :param str name: Maya name of an ui object
    :return: QWidget of parsed Maya name
    :rtype: QWidget
    """
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findLayout( name )    
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None:     
        return wrapInstance( long( ptr ), QtWidgets.QWidget )
        
def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = wrapInstance(long(window), QtWidgets.QMainWindow)
    return window