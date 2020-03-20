# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-20 11:41:52'

"""
Auto Convert the Maya shelf seperator to a collapsible container
"""
import json

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

from maya import cmds
from maya import mel

from .util import mayaToQT
from .seperator import CollapsibleSperator

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


def install():
    """getShelfButton 
    
    Get Command data from Maya Shelf
    """

    # NOTE 加载所有的工具架
    loadShelves()

    # NOTE 获取工具架名称
    gShelfTopLevel = mel.eval("$temp = $gShelfTopLevel")
    shelves = cmds.shelfTabLayout(gShelfTopLevel,query=1,ca=1)
    labels = cmds.shelfTabLayout(gShelfTopLevel,query=1,tl=1)

    # NOTE 获取所有的工具架分隔符的信息
    shelf_data = {}
    for i,[shelf,label] in enumerate(zip(shelves,labels),1):
        # NOTE 获取完整组件名称
        shelf = cmds.shelfLayout(shelf,query=1,fpn=1)
        if not cmds.shelfLayout(shelf,query=1,ca=1):
            print "%s empty child" % shelf
            continue
        seperator = ""
        
        for item in cmds.shelfLayout(shelf,query=1,ca=1):
            if cmds.separator(item,query=1,ex=1):
                seperator = item
                if shelf not in shelf_data:
                    shelf_data[shelf] = {}
                shelf_data[shelf][seperator] = []
            elif cmds.shelfButton(item,query=1,ex=1):
                if not seperator :
                    continue
                shelf_data[shelf][seperator].append(item)

    # print "shelf_data",json.dumps(shelf_data)
    for shelf,data in shelf_data.items():
        shelf = mayaToQT(shelf)
        for seperator,button_list in data.items():
            container = CollapsibleSperator()
            layout = shelf.layout()
            layout.addWidget(container)
            cmds.deleteUI(seperator)
            for i,button in enumerate(button_list,1):
                button = mayaToQT(button)
                container.container_layout.addWidget(button)
            container.setFixedWidth(i * 40)

