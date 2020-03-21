# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-20 11:41:52'

"""
Auto Convert the Maya shelf separator to a collapsible container
"""
import json

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

from maya import cmds
from maya import mel
import maya.api.OpenMaya as om

from .util import mayaToQT
from .util import mayaWindow
from .separator import CollapsibleSperator

global shelf_data
global container_list
shelf_data = {}
container_list = []

   
def loadShelf(index):
    """loadShelf 
    
    convert shelf.mel loadShelf global proc to python code
    
    Parameters
    ----------
    index : int
        the loading shelf index
    """
    
    varName="shelfName" + str(index)
    shelfName=str(cmds.optionVar(q=varName))
    if cmds.shelfLayout(shelfName, exists=1) and cmds.shelfLayout(shelfName, query=1, numberOfChildren=1) == 0:
        shelfFileNum="shelfFile" + str(index)
        shelfFile=cmds.optionVar(q=shelfFileNum)
        if shelfFile and mel.eval("exists %s"%shelfFile):
            cmds.setParent(shelfName)
            shelfVersion=""
            try:
                shelfVersion = mel.eval("eval %s"%shelfFile)
            except:
                print "eval %s fail" % shelfFile
                import traceback
                traceback.print_exc()
                return False
                
            cmds.optionVar(intValue=(("shelfLoad" + str(index)), True))
            if shelfVersion:
                cmds.optionVar(stringValue=(("shelfVersion" + str(index)), shelfVersion))
                if cmds.shelfLayout(shelfName, exists=1):
                    cmds.shelfLayout(shelfName, edit=1, version=shelfVersion)

    return True    

def loadShelves():
    gShelfTopLevel = mel.eval("$temp = $gShelfTopLevel")
    shelves = cmds.shelfTabLayout(gShelfTopLevel,query=1,ca=1)
    for i,_ in enumerate(shelves,1):
        loadShelf(i)


def collectShelfData():
    # NOTE 加载所有的工具架 - 默认不加载全部 参考 commandLuancher 插件
    loadShelves()

    # NOTE 获取工具架名称
    gShelfTopLevel = mel.eval("$temp = $gShelfTopLevel")
    shelves = cmds.shelfTabLayout(gShelfTopLevel,query=1,ca=1)
    labels = cmds.shelfTabLayout(gShelfTopLevel,query=1,tl=1)

    # NOTE 获取所有的工具架分隔符的信息
    for i,[shelf,label] in enumerate(zip(shelves,labels),1):
        # NOTE 获取完整组件名称
        shelf = cmds.shelfLayout(shelf,query=1,fpn=1)
        if not cmds.shelfLayout(shelf,query=1,ca=1):
            print "%s empty child" % shelf
            continue
        separator = ""
        
        for item in cmds.shelfLayout(shelf,query=1,ca=1):
            if cmds.separator(item,query=1,ex=1):
                separator = item
                if shelf not in shelf_data:
                    shelf_data[shelf] = {}
                shelf_data[shelf][separator] = []
            elif cmds.shelfButton(item,query=1,ex=1):
                if not separator :
                    continue
                shelf_data[shelf][separator].append(item)

def uninstall():
    
    global shelf_data
    global container_list
    for shelf,data in shelf_data.items():
        shelf = mayaToQT(shelf)
        for separator,button_list in data.items():
            cmds.separator(separator,e=1,vis=1)
            layout = shelf.layout()
            layout.addWidget(mayaToQT(separator))
            for i,button in enumerate(button_list,1):
                button = mayaToQT(button)
                layout.addWidget(button)
    
    for container in container_list:
        container.deleteLater()
    container_list = []

def install():
    """getShelfButton 
    
    Get Command data from Maya Shelf
    """
    global shelf_data
    global container_list

    # NOTE 已经安装避免重复安装
    if container_list:
        return

    if not shelf_data:
        collectShelfData()

        # NOTE 监听 Maya 关闭的事件，关闭 Maya 的时候确保切换插件为默认状态
        QuitBinding(mayaWindow(),lambda x:uninstall())
        
        # NOTE 添加 menu item 到图标按钮
        # gShelfOptionsButton = mel.eval("$temp = $gShelfOptionsButton")
        gShelfForm = mel.eval("$temp = $gShelfForm")
        option = cmds.formLayout(gShelfForm,q=1,ca=1)[0]
        frame = cmds.formLayout(option,q=1,ca=1)[0]
        form = cmds.frameLayout(frame,q=1,ca=1)[0]
        gShelfOptionsButton = cmds.formLayout(form,q=1,ca=1)[1]

        menu_list = cmds.iconTextButton(gShelfOptionsButton,q=1,pma=1)
        if menu_list:
            menu = menu_list[0]
            cmds.menuItem(dividerLabel='CollapsibleShelf',divider=True,parent=menu )
            cmds.menuItem(ecr=0,label='enable', checkBox=True,c=lambda x: uninstall() if container_list else install(),parent=menu)
            cmds.menuItem(ecr=0,label='update', c=lambda x:collectShelfData(),parent=menu)
    
    # print "shelf_data",json.dumps(shelf_data)
    for shelf,data in shelf_data.items():
        shelf = mayaToQT(shelf)
        for separator,button_list in data.items():
            container = CollapsibleSperator()
            container_list.append(container)
            layout = shelf.layout()
            layout.addWidget(container)

            cmds.separator(separator,e=1,vis=0)

            # NOTE 读取数据
            try:
                tooltip,colors = cmds.separator(separator,q=1,docTag=1).split(";")
                if "," in colors:
                    container.setButtonColor(QtGui.QColor(*[float(digit) for digit in colors.split(",")[:3]]))
                elif colors:
                    container.setButtonColor(QtGui.QColor(colors))
            except:
                tooltip = cmds.separator(separator,q=1,docTag=1)

            status = cmds.separator(separator,q=1,annotation=1)

            container.setToolTip(tooltip)
            container.setStatusTip(status)

            container.container_layout.addWidget(mayaToQT(separator))
            for i,button in enumerate(button_list,1):
                button = mayaToQT(button)
                container.container_layout.addWidget(button)
            container.setFixedWidth(8 + i * 35)


class QuitBinding(QtCore.QObject):
    def __init__(self,widget,quitEvent = None):
        super(QuitBinding,self).__init__()
        self.setParent(widget)
        widget.installEventFilter(self)
        self.quitEvent = quitEvent
    
    def eventFilter(self,receiver,event):
        # NOTE QtCore.QEvent.Type.ChildRemoved = 71
        # NOTE 确保 Maya 正确退出的时候 uninstall 避免保存错误的工具架
        if event.type() == 71:
            if callable(self.quitEvent):
                self.quitEvent(event)
        
        return False
