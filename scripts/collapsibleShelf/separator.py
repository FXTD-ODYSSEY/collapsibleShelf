# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-20 12:26:48'

"""
Qt separator collapsible widget
"""

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets


BAR_CLOSE_ICON = ":/closeBar.png"
BAR_OPEN_ICON = ":/openBar.png"

class CollapsibleSperator(QtWidgets.QWidget):
    toggle = False
    child_width = 0
    color = None
    def __init__(self,parent=None,duration=200,tooltip=""):
        super(CollapsibleSperator,self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setToolTip(tooltip)

        # create bar
        self.bar = QtWidgets.QPushButton()
        self.bar.setFlat(True)
        self.bar.setFixedWidth(8)
        self.bar.setFixedHeight(35)   
        self.bar.setIcon(QtGui.QPixmap(BAR_OPEN_ICON))
        self.bar.setIconSize(QtCore.QSize(8,35))
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

        self._setColor()
        self.setFixedWidth(8)
        self.toggle = not self.toggle
    
    def setButtonColor(self,color=QtGui.QColor("red")):
        """setButtonColor set SVG Icon Color
        # NOTE https://stackoverflow.com/questions/53107173/change-color-png-image-qpushbutton
        Parameters
        ----------
        button : QPushButton
            Icon Button
        color : QColor, optional
            set the Icon color, by default QtGui.QColor("red")
        """
        self.color = color
        self._setColor()

    def _setColor(self):
        if not self.color:
            return
        icon = self.bar.icon()
        pixmap = icon.pixmap(35)
        image = pixmap.toImage()
        pcolor = image.pixelColor(8,35)
        for x in range(image.width()):
            for y in range(image.height()):
                pcolor = image.pixelColor(x, y)
                if pcolor.alpha() > 0:
                    self.color.setAlpha(pcolor.alpha())
                    image.setPixelColor(x, y, self.color)
        self.bar.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image)))


if __name__ == "__main__":
    widget = CollapsibleSperator()
    widget.show()
    widget.setButtonColor(QtGui.QColor("rgb(0,255,0)"))
   