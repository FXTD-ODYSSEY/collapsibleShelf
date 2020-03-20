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

# # NOTE replaceWidget ----------------------------------------------------------------------------

# def replaceWidget(src,dst):
#     u"""replaceWidget 替换组件
    
#     Parameters
#     ----------
#     src : QWidget
#         源组件
#     dst : QWidget
#         目标组件
    
#     Returns
#     -------
#     QWidget
#         [description]
#     """
#     updateWidgetState(src,dst)
#     layout = src.parent().layout()
#     layout,index = getTargetLayoutIndex(layout,src)
#     if not layout:
#         print (u"没有找到 %s 的 Layout，替换失败" % src)
#         return src

#     layout.insertWidget(index,dst)
#     src.setParent(None)
    
#     return dst

# def updateWidgetState(src,dst):
#     u"""updateWidgetState 同步组件状态
    
#     Parameters
#     ----------
#     src : QWidget
#         源组件
#     dst : QWidget
#         目标组件
#     """
#     if src.acceptDrops()           : dst.setAcceptDrops(src.acceptDrops())
#     if src.accessibleDescription() : dst.setAccessibleDescription(src.accessibleDescription())
#     if src.backgroundRole()        : dst.setBackgroundRole(src.backgroundRole())
#     if src.baseSize()              : dst.setBaseSize(src.baseSize())
#     if src.contentsMargins()       : dst.setContentsMargins(src.contentsMargins())
#     if src.contextMenuPolicy()     : dst.setContextMenuPolicy(src.contextMenuPolicy())
#     if src.cursor()                : dst.setCursor(src.cursor())
#     if src.focusPolicy()           : dst.setFocusPolicy(src.focusPolicy())
#     if src.focusProxy()            : dst.setFocusProxy(src.focusProxy())
#     if src.font()                  : dst.setFont(src.font())
#     if src.foregroundRole()        : dst.setForegroundRole(src.foregroundRole())
#     if src.geometry()              : dst.setGeometry(src.geometry())
#     if src.inputMethodHints()      : dst.setInputMethodHints(src.inputMethodHints())
#     if src.layout()                : dst.setLayout(src.layout())
#     if src.layoutDirection()       : dst.setLayoutDirection(src.layoutDirection())
#     if src.locale()                : dst.setLocale(src.locale())
#     if src.mask()                  : dst.setMask(src.mask())
#     if src.maximumSize()           : dst.setMaximumSize(src.maximumSize())
#     if src.minimumSize()           : dst.setMinimumSize(src.minimumSize())
#     if src.hasMouseTracking ()     : dst.setMouseTracking(src.hasMouseTracking ())
#     if src.palette()               : dst.setPalette(src.palette())
#     # if src.parent()                : dst.setParent(src.parent())
#     if src.sizeIncrement()         : dst.setSizeIncrement(src.sizeIncrement())
#     if src.sizePolicy()            : dst.setSizePolicy(src.sizePolicy())
#     if src.statusTip()             : dst.setStatusTip(src.statusTip())
#     if src.style()                 : dst.setStyle(src.style())
#     if src.toolTip()               : dst.setToolTip(src.toolTip())
#     if src.updatesEnabled()        : dst.setUpdatesEnabled(src.updatesEnabled())
#     if src.whatsThis()             : dst.setWhatsThis(src.whatsThis())
#     if src.windowFilePath()        : dst.setWindowFilePath(src.windowFilePath())
#     if src.windowFlags()           : dst.setWindowFlags(src.windowFlags())
#     if src.windowIcon()            : dst.setWindowIcon(src.windowIcon())
#     if src.windowIconText()        : dst.setWindowIconText(src.windowIconText())
#     if src.windowModality()        : dst.setWindowModality(src.windowModality())
#     if src.windowOpacity()         : dst.setWindowOpacity(src.windowOpacity())
#     if src.windowRole()            : dst.setWindowRole(src.windowRole())
#     if src.windowState()           : dst.setWindowState(src.windowState())


# def getTargetLayoutIndex(layout,target):
#     u"""getTargetLayoutIndex 获取目标 Layout 和 序号
    
#     Parameters
#     ----------
#     layout : QLayout 
#         通过 QLayout 递归遍历下属的组件
#     target : QWidget
#         要查询的组件
    
#     Returns
#     -------
#     layout : QLayout
#         查询组件所在的 Layout
#     i : int
#         查询组件所在的 Layout 的序号
#     """
#     count = layout.count()
#     for i in range(count):
#         item = layout.itemAt(i).widget()
#         if item == target:
#             return layout,i
#     else:
#         for child in layout.children():
#             layout,i = getTargetLayoutIndex(child,target)
#             if layout:
#                 return layout,i
#         return [None,None]
