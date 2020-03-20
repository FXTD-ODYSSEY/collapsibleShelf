# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-20 12:26:48'

"""
Qt seperator collapsible widget
"""

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets


BAR_CLOSE_ICON = ":/closeBar.png"
BAR_OPEN_ICON = ":/openBar.png"

class CollapsibleSperator(QtWidgets.QWidget):
    toggle = False
    child_width = 0
    def __init__(self,parent=None,duration=200):
        super(CollapsibleSperator,self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        
        # create bar
        self.bar = QtWidgets.QPushButton()
        self.bar.setFlat(True)
        self.bar.setFixedWidth(8)
        self.bar.setFixedHeight(40)   
        self.bar.setIcon(QtGui.QPixmap(BAR_OPEN_ICON))
        self.bar.setIconSize(QtCore.QSize(8,40))
        self.bar.released.connect(self.switch)

        self.container = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QHBoxLayout()
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container_layout.setSpacing(0)
        self.container.setLayout(self.container_layout)

        # create layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(1)

        layout.addWidget(self.bar)
        layout.addWidget(self.container)

        # NOTE 配置动画
        self.anim = QtCore.QPropertyAnimation(self.container, "maximumWidth")
        self.anim2 = QtCore.QPropertyAnimation(self, "maximumWidth")

        self.anim.setDuration(duration)
        self.anim.setStartValue(0)

        self.anim2.setDuration(duration)
        self.anim2.setStartValue(0)

        # self.container.installEventFilter(self)


    def switch(self):
        """
        Switch visibility of the widget, it is build in the same style as all
        if the maya status line ui elements.
        """
        
        if self.toggle:
            self.bar.setIcon(QtGui.QPixmap(BAR_OPEN_ICON))

            self.anim.setDirection(QtCore.QAbstractAnimation.Forward)
            self.anim.setEndValue(self.child_width)
            self.anim.start()

            self.anim2.setDirection(QtCore.QAbstractAnimation.Forward)
            self.anim2.setEndValue(self.child_width)
            self.anim2.start()
        else:
            self.bar.setIcon(QtGui.QPixmap(BAR_CLOSE_ICON))
            self.child_width = self.width()

            self.anim.setDirection(QtCore.QAbstractAnimation.Backward)
            self.anim.setEndValue(self.child_width)
            self.anim.start()

            self.anim2.setDirection(QtCore.QAbstractAnimation.Backward)
            self.anim2.setEndValue(self.child_width)
            self.anim2.start()

        self.setFixedWidth(8)
        self.toggle = not self.toggle

    # def eventFilter(self, receiver,event):
    #     # NOTE 68 = QtCore.QEvent.Type.ChildAdded
    #     if event.type() == 68:
    #         self.child_width += 40
    #     return False

if __name__ == "__main__":
    widget = CollapsibleSperator()
    widget.show()
            
# class ICollapsibleWidget( object ):
#     # config_schema = Schema({
#     #     Required('duration', default=300): int,
#     #     Required('toggle_mark', default=True): bool,
#     #     'expand_callback' :FunctionType,
#     #     'collapse_callback': FunctionType,
#     # })

#     @staticmethod
#     def install(btn,container,config={}):
        
#         config = ICollapsibleWidget.config_schema(config)
#         duration = config.get("duration") if config.get("duration") else 300
#         toggle_mark = config.get("toggle_mark")
#         expand_callback = config.get("expand_callback")
#         collapse_callback = config.get("collapse_callback")

#         anim = QtCore.QPropertyAnimation(container, "maximumHeight")
        
#         anim.setDuration(duration)
#         anim.setStartValue(0)
#         anim.setEndValue(container.sizeHint().height())
#         anim.finished.connect(lambda:container.setMaximumHeight(16777215) if not btn.toggle else None)

#         btn.toggle = False
#         if toggle_mark:
#             btn.setText(u"▼ %s"%btn.text())
#         def toggleFn(btn,anim):
#             if btn.toggle:
#                 btn.toggle = False
#                 anim.setDirection(QtCore.QAbstractAnimation.Forward)

#                 anim.setEndValue(ICollapsibleWidget.getHeightEndValue(container))
#                 anim.start()
#                 if toggle_mark:
#                     btn.setText(u"▼%s"%btn.text()[1:])
#                 btn.setStyleSheet('font:normal')
#                 if expand_callback:
#                     expand_callback()
#             else:
#                 btn.toggle = True
#                 anim.setDirection(QtCore.QAbstractAnimation.Backward)
#                 anim.setEndValue(container.sizeHint().height())
#                 anim.start()
#                 if toggle_mark:
#                     btn.setText(u"■%s"%btn.text()[1:])
#                     btn.setStyleSheet('font:bold')
#                 if collapse_callback:
#                     collapse_callback()

#         func = lambda x:toggleFn(btn,anim)
#         btn.clicked.connect(func)
#         return func

#     @staticmethod
#     def getHeightEndValue(widget):

#         parent = widget.parent()
#         total_height = parent.height()

#         height = 0
#         for child in parent.children():
#             if child == widget or not hasattr(child,"height"):
#                 continue
            
#             height += child.height()

#         widget.updateGeometry()
#         prefer = widget.sizeHint().height()
#         height = total_height - height
#         return height if height > prefer else prefer