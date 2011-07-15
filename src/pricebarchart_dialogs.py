
# For line separator.
import os

# For copy.deepcopy().
import copy

# For logging.
import logging
import logging.config

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For PriceBars and artifacts in the chart.
from data_objects import BirthInfo
from data_objects import PriceBar
from data_objects import MusicalRatio
from data_objects import PriceBarChartTextArtifact
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartTimeMeasurementArtifact
from data_objects import PriceBarChartModalScaleArtifact
from data_objects import PriceBarChartGannFanUpperRightArtifact
from data_objects import PriceBarChartGannFanLowerRightArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings
from data_objects import PriceBarChartTextArtifact

from dialogs import TimestampEditWidget

from widgets import ColorEditPushButton

# For formatting datetime.datetime to string.
from ephemeris import Ephemeris

# This file contains the edit widgets and dialogs for editing the
# fields in various PriceBarChartArtifact objects within the context
# of a PriceBarChart.


class PriceBarChartTextArtifactEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceBarChartTextArtifact within the context of a
    PriceBarChart.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartTextArtifact object.

        Arguments:
        artifact - PriceBarChartTextArtifact object to edit.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartTextArtifactEditWidget")

        # Save off the artifact object.
        self.artifact = artifact

        self.log.debug("Artifact passed into " +
                       "PriceBarChartTextArtifactEditWidget constructor is: " +
                       artifact.toString())
        
        # Save off the scene object used for unit conversions.
        self.convertObj = convertObj
        
        # Save off the readOnlyFlag
        self.readOnlyFlag = readOnlyFlag
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("PriceBarChartTextArtifact Data:")


        lineEditWidth = 420
        
        self.internalNameLabel = QLabel("Internal name:")
        self.internalNameLineEdit = QLineEdit()
        self.internalNameLineEdit.setMinimumWidth(lineEditWidth)

        self.uuidLabel = QLabel("Uuid:")
        self.uuidLineEdit = QLineEdit()
        self.uuidLineEdit.setMinimumWidth(lineEditWidth)

        self.priceLocationValueLabel = QLabel("Artifact location (in price):")
        self.priceLocationValueSpinBox = QDoubleSpinBox()
        self.priceLocationValueSpinBox.setMinimum(0.0)
        self.priceLocationValueSpinBox.setMaximum(999999999.0)

        self.datetimeLocationLabel = QLabel("Artifact location (in time)")
        self.datetimeLocationWidget = TimestampEditWidget()
        self.datetimeLocationWidget.groupBox.setTitle("")
        self.datetimeLocationWidget.okayButton.setVisible(False)
        self.datetimeLocationWidget.cancelButton.setVisible(False)
        
        self.textLabel = QLabel("Text:")
        self.textEdit = QTextEdit()
        self.textEdit.setMinimumWidth(lineEditWidth)
        self.textEdit.setTabChangesFocus(True)
        
        self.font = QFont()
        self.fontLabel = QLabel("Font:")
        self.fontValueLabel = QLabel(self.font.toString())
        self.fontEditButton = QPushButton("Modify")

        self.colorLabel = QLabel("Color of text:")
        self.colorEditPushButton = ColorEditPushButton()

        self.xScalingLabel = QLabel("X Scaling:")
        self.xScalingDoubleSpinBox = QDoubleSpinBox()
        self.xScalingDoubleSpinBox.setMinimum(0.0)
        self.xScalingDoubleSpinBox.setMaximum(999999999.0)
        
        self.yScalingLabel = QLabel("Y Scaling:")
        self.yScalingDoubleSpinBox = QDoubleSpinBox()
        self.yScalingDoubleSpinBox.setMinimum(0.0)
        self.yScalingDoubleSpinBox.setMaximum(999999999.0)
        
        # Layout for just the font info.
        self.fontLayout = QHBoxLayout()
        self.fontLayout.addWidget(self.fontValueLabel)
        self.fontLayout.addStretch()
        self.fontLayout.addWidget(self.fontEditButton)
        
        # Layout.
        self.gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        self.gridLayout.addWidget(self.internalNameLabel, r, 0, al)
        self.gridLayout.addWidget(self.internalNameLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.uuidLabel, r, 0, al)
        self.gridLayout.addWidget(self.uuidLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.priceLocationValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.priceLocationValueSpinBox, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.datetimeLocationLabel, r, 0, al)
        self.gridLayout.addWidget(self.datetimeLocationWidget, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.textLabel, r, 0, al)
        self.gridLayout.addWidget(self.textEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.fontLabel, r, 0, al)
        self.gridLayout.addLayout(self.fontLayout, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.colorLabel, r, 0, al)
        self.gridLayout.addWidget(self.colorEditPushButton, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.xScalingLabel, r, 0, al)
        self.gridLayout.addWidget(self.xScalingDoubleSpinBox, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.yScalingLabel, r, 0, al)
        self.gridLayout.addWidget(self.yScalingDoubleSpinBox, r, 1, al)
        r += 1
                
        self.groupBox.setLayout(self.gridLayout)
        
        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)
        
        self.setReadOnly(self.readOnlyFlag)
        
        # Now that all the widgets are created, load the values from the
        # artifact object.
        self.loadValues(self.artifact)

        # Connect signals and slots.

        self.fontEditButton.clicked.connect(self._handleFontEditButtonClicked)
        
        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        # Need to reload the artifact, so that the proper conversion
        # is done with the new conversion object.
        self.loadValues(self.artifact)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
        
    def getArtifact(self):
        """Returns the internally stored artifact object.

        Note: If saveValues() was called previously, then this object
        was updated with the values from the edit widgets.
        """

        return self.artifact
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
        ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.internalNameLineEdit.setReadOnly(True)
        self.uuidLineEdit.setReadOnly(True)
        self.priceLocationValueSpinBox.setEnabled(not self.readOnlyFlag)
        self.datetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        self.textEdit.setEnabled(not self.readOnlyFlag)
        self.fontEditButton.setEnabled(not self.readOnlyFlag)
        self.colorEditPushButton.setEnabled(not self.readOnlyFlag)
        self.xScalingDoubleSpinBox.setEnabled(not self.readOnlyFlag)
        self.yScalingDoubleSpinBox.setEnabled(not self.readOnlyFlag)
        
        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadValues(self, artifact):
        """Loads the widgets with values from the given
        PriceBarChartTextArtifact.

        Note: Upon calling saveValues(), the edit widget overwrites
        the values in the object pointed to by 'artifact' with the
        values in the edit widgets.

        Arguments:
        
        artifact - PriceBarChartTextArtifact object to load the
        values into the edit widgets.  
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if artifact == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  artifact can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        else:
            self.artifact = artifact

        # Set the widgets.
        self.internalNameLineEdit.\
            setText(self.artifact.getInternalName())
        self.uuidLineEdit.\
            setText(str(self.artifact.getUuid()))

        locationPointY = self.artifact.getPos().y()
        locationPointPrice = self.convertObj.sceneYPosToPrice(locationPointY)
        self.priceLocationValueSpinBox.setValue(locationPointPrice)
        
        locationPointX = self.artifact.getPos().x()
        locationPointDatetime = \
            self.convertObj.sceneXPosToDatetime(locationPointX)
        self.datetimeLocationWidget.\
            loadTimestamp(locationPointDatetime)

        self.textEdit.clear()
        self.textEdit.setText(self.artifact.getText())

        self.fontValueLabel.\
            setText(self._convertFontToNiceText(self.artifact.getFont()))
        
        self.colorEditPushButton.setColor(self.artifact.getColor())

        self.xScalingDoubleSpinBox.setValue(self.artifact.getTextXScaling())
        self.yScalingDoubleSpinBox.setValue(self.artifact.getTextYScaling())
        
        self.log.debug("Exiting loadValues()")
        
    def saveValues(self):
        """Saves the values in the widgets to the
        PriceBarChartTextArtifact object passed in this class's
        constructor or the loadValues() function.
        """
    
        self.log.debug("Entered saveValues()")

        # Call save on the timestamp widget.
        self.datetimeLocationWidget.saveTimestamp()
        
        # Position and start point should be the same values.

        price = self.priceLocationValueSpinBox.value()
        y = self.convertObj.priceToSceneYPos(price)

        locationPointDatetime = \
            self.datetimeLocationWidget.getTimestamp()
        locationPointX = \
            self.convertObj.datetimeToSceneXPos(locationPointDatetime)

        posF = QPointF(locationPointX, y)

        text = self.textEdit.toPlainText()

        font = self.font

        color = self.colorEditPushButton.getColor()

        xScaling = self.xScalingDoubleSpinBox.value()
        yScaling = self.yScalingDoubleSpinBox.value()

        
        # Set the values in the artifact.
        self.artifact.setPos(posF)
        self.artifact.setText(text)
        self.artifact.setFont(font)
        self.artifact.setColor(color)
        self.artifact.setTextXScaling(xScaling)
        self.artifact.setTextYScaling(yScaling)
        
        self.log.debug("Exiting saveValues()")


    def _convertFontToNiceText(self, font):
        """Converts the given QFont to some nice str for decribing in a label.
        """

        rv = "Family: {}".format(font.family()) + os.linesep + \
             "Size: {}".format(font.pointSizeF())

        return rv
        
    def _handleFontEditButtonClicked(self):
        """Called when the self.fontEditButton is clicked."""

        dialog = QFontDialog(self.font)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.font = dialog.selectedFont()
            self.fontValueLabel.setText(self._convertFontToNiceText(self.font))

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartTextArtifactEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceBarChartTextArtifact.
    """

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceBarChartTextArtifact.
        
        Arguments:
        artifact - PriceBarChartTextArtifact object to edit.
                   This object gets modified if the user clicks the
                   'Okay' button.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartTextArtifactEditDialog")

        self.setWindowTitle("Edit PriceBarChartTextArtifact Data")

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartTextArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      " constructor.")
            return

        # Save a reference to the artifact object.
        self.artifact = artifact

        # Save a reference to the conversion object.
        self.convertObj = convertObj
        
        # Save the readOnlyFlag value.
        self.readOnlyFlag = readOnlyFlag
        
        # Create the contents.
        self.editWidget = \
            PriceBarChartTextArtifactEditWidget(self.artifact,
                                                self.convertObj,
                                                self.readOnlyFlag)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def exec_(self):
        """Overwrites the QDialog.exec_() function.  Used so that we
        can set the focus to the text box right away before actually
        running exec_().
        """

        self.editWidget.textEdit.setFocus()
        return super().exec_()
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
                       ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        self.editWidget.setReadOnly(self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields.
        """
        
        return self.readOnlyFlag

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        self.editWidget.setConvertObj(self.convertObj)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
    def setArtifact(self, artifact):
        """Loads the edit widget with the given artifact object.
        
        Note:  Upon clicking 'Okay' this object will be modified.

        Arguments:
        artifact - PriceBarChartTextArtifact object to load the
                   widgets with.
        """

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartTextArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      ".setArtifact()")
            return

        self.artifact = artifact

        self.editWidget.loadValues(self.artifact)

    def getArtifact(self):
        """Returns a reference to the internally stored artifact object.
        """

        return self.editWidget.getArtifact()



class PriceBarChartBarCountArtifactEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceBarChartBarCountArtifact within the context of a
    PriceBarChart.  This means that fields that are editable in the
    widgets are not actually a one-to-one mapping with the members in
    a PriceBarChartBarCountArtifact.  They are derivatives of it such
    that the user can modify it without having to do the underlying
    conversions.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartBarCountArtifact object.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to edit.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartBarCountArtifactEditWidget")

        # Save off the artifact object.
        self.artifact = artifact

        # Save off the scene object used for unit conversions.
        self.convertObj = convertObj
        
        # Save off the readOnlyFlag
        self.readOnlyFlag = readOnlyFlag
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("PriceBarChartBarCountArtifact Data:")


        lineEditWidth = 420
        
        self.internalNameLabel = QLabel("Internal name:")
        self.internalNameLineEdit = QLineEdit()
        self.internalNameLineEdit.setMinimumWidth(lineEditWidth)

        self.uuidLabel = QLabel("Uuid:")
        self.uuidLineEdit = QLineEdit()
        self.uuidLineEdit.setMinimumWidth(lineEditWidth)

        self.priceLocationValueLabel = QLabel("Artifact location (in price):")
        self.priceLocationValueSpinBox = QDoubleSpinBox()
        self.priceLocationValueSpinBox.setMinimum(0.0)
        self.priceLocationValueSpinBox.setMaximum(999999999.0)

        self.startPointDatetimeLocationWidget = TimestampEditWidget()
        self.startPointDatetimeLocationWidget.groupBox.\
            setTitle("BarCount Start Point (in time)")
        self.startPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.startPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        self.endPointDatetimeLocationWidget = TimestampEditWidget()
        self.endPointDatetimeLocationWidget.groupBox.\
            setTitle("BarCount End Point (in time)")
        self.endPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.endPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        # Layout.
        self.gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        self.gridLayout.addWidget(self.internalNameLabel, r, 0, al)
        self.gridLayout.addWidget(self.internalNameLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.uuidLabel, r, 0, al)
        self.gridLayout.addWidget(self.uuidLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.priceLocationValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.priceLocationValueSpinBox, r, 1, al)
        r += 1

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.startPointDatetimeLocationWidget)
        self.layout.addWidget(self.endPointDatetimeLocationWidget)
        
        self.groupBox.setLayout(self.layout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)
        
        self.setReadOnly(self.readOnlyFlag)
        
        # Now that all the widgets are created, load the values from the
        # artifact object.
        self.loadValues(self.artifact)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        # Need to reload the artifact, so that the proper conversion
        # is done with the new conversion object.
        self.loadValues(self.artifact)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
        
    def getArtifact(self):
        """Returns the internally stored artifact object.

        Note: If saveValues() was called previously, then this object
        was updated with the values from the edit widgets.
        """

        return self.artifact
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
        ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.internalNameLineEdit.setReadOnly(True)
        self.uuidLineEdit.setReadOnly(True)
        self.priceLocationValueSpinBox.setReadOnly(self.readOnlyFlag)
        self.startPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        self.endPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        
        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadValues(self, artifact):
        """Loads the widgets with values from the given
        PriceBarChartBarCountArtifact.

        Note: Upon calling saveValues(), the edit widget overwrites
        the values in the object pointed to by 'artifact' with the
        values in the edit widgets.

        Arguments:
        
        artifact - PriceBarChartBarCountArtifact object to load the
        values into the edit widgets.  
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if artifact == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  artifact can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        else:
            self.artifact = artifact

        # Set the widgets.
        self.internalNameLineEdit.\
            setText(self.artifact.getInternalName())
        self.uuidLineEdit.\
            setText(str(self.artifact.getUuid()))

        locationPointY = self.artifact.startPointF.y()
        locationPointPrice = self.convertObj.sceneYPosToPrice(locationPointY)
        self.priceLocationValueSpinBox.setValue(locationPointPrice)
        
        startPointX = self.artifact.startPointF.x()
        startPointDatetime = self.convertObj.sceneXPosToDatetime(startPointX)
        self.startPointDatetimeLocationWidget.\
            loadTimestamp(startPointDatetime)
        
        endPointX = self.artifact.endPointF.x()
        endPointDatetime = self.convertObj.sceneXPosToDatetime(endPointX)
        self.endPointDatetimeLocationWidget.\
            loadTimestamp(endPointDatetime)
        
        self.log.debug("Exiting loadValues()")
        
    def saveValues(self):
        """Saves the values in the widgets to the
        PriceBarChartBarCountArtifact object passed in this class's
        constructor or the loadValues() function.
        """
    
        self.log.debug("Entered saveValues()")

        # Call save on the timestamp widgets.
        self.startPointDatetimeLocationWidget.saveTimestamp()
        self.endPointDatetimeLocationWidget.saveTimestamp()
        
        # Position and start point should be the same values.

        price = self.priceLocationValueSpinBox.value()
        y = self.convertObj.priceToSceneYPos(price)

        startPointDatetime = \
            self.startPointDatetimeLocationWidget.getTimestamp()
        endPointDatetime = \
            self.endPointDatetimeLocationWidget.getTimestamp()
                          
        startPointX = self.convertObj.datetimeToSceneXPos(startPointDatetime)
        endPointX = self.convertObj.datetimeToSceneXPos(endPointDatetime)

        posF = QPointF(startPointX, y)
        startPointF = QPointF(startPointX, y)
        endPointF = QPointF(endPointX, y)

        # Set the values in the artifact.
        self.artifact.setPos(posF)
        self.artifact.setStartPointF(startPointF)
        self.artifact.setEndPointF(endPointF)

        self.log.debug("Exiting saveValues()")


    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartBarCountArtifactEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceBarChartBarCountArtifact.
    """

    def __init__(self,
                 priceBarChartBarCountArtifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceBarChartBarCountArtifact.
        
        Note: The 'priceBarChartBarCountArtifact' object gets modified
        if the user clicks the 'Okay' button.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to edit.
                   This object gets modified if the user clicks the
                   'Okay' button.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartBarCountArtifactEditDialog")

        self.setWindowTitle("Edit PriceBarChartBarCountArtifact Data")

        # Check input.
        if not isinstance(priceBarChartBarCountArtifact,
                          PriceBarChartBarCountArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      " constructor.")
            return

        # Save a reference to the artifact object.
        self.artifact = priceBarChartBarCountArtifact

        # Save a reference to the conversion object.
        self.convertObj = convertObj
        
        # Save the readOnlyFlag value.
        self.readOnlyFlag = readOnlyFlag
        
        # Create the contents.
        self.editWidget = \
            PriceBarChartBarCountArtifactEditWidget(self.artifact,
                                                    self.convertObj,
                                                    self.readOnlyFlag)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
                       ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        self.editWidget.setReadOnly(self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields.
        """
        
        return self.readOnlyFlag

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        self.editWidget.setConvertObj(self.convertObj)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
    def setArtifact(self, artifact):
        """Loads the edit widget with the given artifact object.
        
        Note:  Upon clicking 'Okay' this object will be modified.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to load the
                   widgets with.
        """

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartBarCountArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      ".setArtifact()")
            return

        self.artifact = artifact

        self.editWidget.loadValues(self.artifact)

    def getArtifact(self):
        """Returns a reference to the internally stored artifact object.
        
        Note: If the 'Okay' button was previously clicked, then this
        object is modified with the widget's values, otherwise it is
        unchanged.
        """

        return self.artifact



class PriceBarChartTimeMeasurementArtifactEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceBarChartTimeMeasurementArtifact within the context of a
    PriceBarChart.  This means that fields that are editable in the
    widgets are not actually a one-to-one mapping with the members in
    a PriceBarChartTimeMeasurementArtifact.  They are derivatives of it such
    that the user can modify it without having to do the underlying
    conversions.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartTimeMeasurementArtifact object.

        Arguments:
        artifact - PriceBarChartTimeMeasurementArtifact object to edit.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartTimeMeasurementArtifactEditWidget")

        # Save off the artifact object.
        self.artifact = artifact

        # Save off the scene object used for unit conversions.
        self.convertObj = convertObj
        
        # Save off the readOnlyFlag
        self.readOnlyFlag = readOnlyFlag
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("PriceBarChartTimeMeasurementArtifact Data:")


        lineEditWidth = 420
        
        self.internalNameLabel = QLabel("Internal name:")
        self.internalNameLineEdit = QLineEdit()
        self.internalNameLineEdit.setMinimumWidth(lineEditWidth)

        self.uuidLabel = QLabel("Uuid:")
        self.uuidLineEdit = QLineEdit()
        self.uuidLineEdit.setMinimumWidth(lineEditWidth)

        self.priceLocationValueLabel = QLabel("Artifact location (in price):")
        self.priceLocationValueSpinBox = QDoubleSpinBox()
        self.priceLocationValueSpinBox.setMinimum(0.0)
        self.priceLocationValueSpinBox.setMaximum(999999999.0)

        self.startPointDatetimeLocationWidget = TimestampEditWidget()
        self.startPointDatetimeLocationWidget.groupBox.\
            setTitle("TimeMeasurement Start Point (in time)")
        self.startPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.startPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        self.endPointDatetimeLocationWidget = TimestampEditWidget()
        self.endPointDatetimeLocationWidget.groupBox.\
            setTitle("TimeMeasurement End Point (in time)")
        self.endPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.endPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        # Layout.
        self.gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        self.gridLayout.addWidget(self.internalNameLabel, r, 0, al)
        self.gridLayout.addWidget(self.internalNameLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.uuidLabel, r, 0, al)
        self.gridLayout.addWidget(self.uuidLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.priceLocationValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.priceLocationValueSpinBox, r, 1, al)
        r += 1

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.startPointDatetimeLocationWidget)
        self.layout.addWidget(self.endPointDatetimeLocationWidget)
        
        self.groupBox.setLayout(self.layout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)
        
        self.setReadOnly(self.readOnlyFlag)
        
        # Now that all the widgets are created, load the values from the
        # artifact object.
        self.loadValues(self.artifact)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        # Need to reload the artifact, so that the proper conversion
        # is done with the new conversion object.
        self.loadValues(self.artifact)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
        
    def getArtifact(self):
        """Returns the internally stored artifact object.

        Note: If saveValues() was called previously, then this object
        was updated with the values from the edit widgets.
        """

        return self.artifact
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
        ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.internalNameLineEdit.setReadOnly(True)
        self.uuidLineEdit.setReadOnly(True)
        self.priceLocationValueSpinBox.setReadOnly(self.readOnlyFlag)
        self.startPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        self.endPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        
        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadValues(self, artifact):
        """Loads the widgets with values from the given
        PriceBarChartTimeMeasurementArtifact.

        Note: Upon calling saveValues(), the edit widget overwrites
        the values in the object pointed to by 'artifact' with the
        values in the edit widgets.

        Arguments:
        
        artifact - PriceBarChartTimeMeasurementArtifact object to load the
        values into the edit widgets.  
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if artifact == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  artifact can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        else:
            self.artifact = artifact

        # Set the widgets.
        self.internalNameLineEdit.\
            setText(self.artifact.getInternalName())
        self.uuidLineEdit.\
            setText(str(self.artifact.getUuid()))

        locationPointY = self.artifact.startPointF.y()
        locationPointPrice = self.convertObj.sceneYPosToPrice(locationPointY)
        self.priceLocationValueSpinBox.setValue(locationPointPrice)
        
        startPointX = self.artifact.startPointF.x()
        startPointDatetime = self.convertObj.sceneXPosToDatetime(startPointX)
        self.startPointDatetimeLocationWidget.\
            loadTimestamp(startPointDatetime)
        
        endPointX = self.artifact.endPointF.x()
        endPointDatetime = self.convertObj.sceneXPosToDatetime(endPointX)
        self.endPointDatetimeLocationWidget.\
            loadTimestamp(endPointDatetime)
        
        self.log.debug("Exiting loadValues()")
        
    def saveValues(self):
        """Saves the values in the widgets to the
        PriceBarChartTimeMeasurementArtifact object passed in this class's
        constructor or the loadValues() function.
        """
    
        self.log.debug("Entered saveValues()")

        # Call save on the timestamp widgets.
        self.startPointDatetimeLocationWidget.saveTimestamp()
        self.endPointDatetimeLocationWidget.saveTimestamp()
        
        # Position and start point should be the same values.

        price = self.priceLocationValueSpinBox.value()
        y = self.convertObj.priceToSceneYPos(price)

        startPointDatetime = \
            self.startPointDatetimeLocationWidget.getTimestamp()
        endPointDatetime = \
            self.endPointDatetimeLocationWidget.getTimestamp()
                          
        startPointX = self.convertObj.datetimeToSceneXPos(startPointDatetime)
        endPointX = self.convertObj.datetimeToSceneXPos(endPointDatetime)

        posF = QPointF(startPointX, y)
        startPointF = QPointF(startPointX, y)
        endPointF = QPointF(endPointX, y)

        # Set the values in the artifact.
        self.artifact.setPos(posF)
        self.artifact.setStartPointF(startPointF)
        self.artifact.setEndPointF(endPointF)

        self.log.debug("Exiting saveValues()")


    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartTimeMeasurementArtifactEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceBarChartTimeMeasurementArtifact.
    """

    def __init__(self,
                 priceBarChartTimeMeasurementArtifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceBarChartTimeMeasurementArtifact.
        
        Note: The 'priceBarChartTimeMeasurementArtifact' object gets modified
        if the user clicks the 'Okay' button.

        Arguments:
        artifact - PriceBarChartTimeMeasurementArtifact object to edit.
                   This object gets modified if the user clicks the
                   'Okay' button.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartTimeMeasurementArtifactEditDialog")

        self.setWindowTitle("Edit PriceBarChartTimeMeasurementArtifact Data")

        # Check input.
        if not isinstance(priceBarChartTimeMeasurementArtifact,
                          PriceBarChartTimeMeasurementArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      " constructor.")
            return

        # Save a reference to the artifact object.
        self.artifact = priceBarChartTimeMeasurementArtifact

        # Save a reference to the conversion object.
        self.convertObj = convertObj
        
        # Save the readOnlyFlag value.
        self.readOnlyFlag = readOnlyFlag
        
        # Create the contents.
        self.editWidget = \
            PriceBarChartTimeMeasurementArtifactEditWidget(self.artifact,
                                                    self.convertObj,
                                                    self.readOnlyFlag)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
                       ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        self.editWidget.setReadOnly(self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields.
        """
        
        return self.readOnlyFlag

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        self.editWidget.setConvertObj(self.convertObj)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
    def setArtifact(self, artifact):
        """Loads the edit widget with the given artifact object.
        
        Note:  Upon clicking 'Okay' this object will be modified.

        Arguments:
        artifact - PriceBarChartTimeMeasurementArtifact object to load the
                   widgets with.
        """

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartTimeMeasurementArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      ".setArtifact()")
            return

        self.artifact = artifact

        self.editWidget.loadValues(self.artifact)

    def getArtifact(self):
        """Returns a reference to the internally stored artifact object.
        
        Note: If the 'Okay' button was previously clicked, then this
        object is modified with the widget's values, otherwise it is
        unchanged.
        """

        return self.artifact


class PriceBarChartModalScaleArtifactEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceBarChartModalScaleArtifact within the context of a
    PriceBarChart.  This means that fields that are editable in the
    widgets are not actually a one-to-one mapping with the members in
    a PriceBarChartModalScaleArtifact.  They are derivatives of it such
    that the user can modify it without having to do the underlying
    conversions.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartModalScaleArtifact object.

        Arguments:
        artifact - PriceBarChartModalScaleArtifact object to edit.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartModalScaleArtifactEditWidget")

        # This variable holds a copy of the artifact passed in.  We
        # set this value via self.loadValues(), which is called later
        # in this funtion on parameter 'artifact'.
        self.artifact = None

        # Save off the scene object used for unit conversions.
        self.convertObj = convertObj
        
        # Save off the readOnlyFlag
        self.readOnlyFlag = readOnlyFlag
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("PriceBarChartModalScaleArtifact Data:")

        lineEditWidth = 420
        
        self.internalNameLabel = QLabel("Internal name:")
        self.internalNameLineEdit = QLineEdit()
        self.internalNameLineEdit.setMinimumWidth(lineEditWidth)

        self.uuidLabel = QLabel("Uuid:")
        self.uuidLineEdit = QLineEdit()
        self.uuidLineEdit.setMinimumWidth(lineEditWidth)

        self.modalScaleGraphicsItemBarColorLabel = QLabel("Bar color: ")
        self.modalScaleGraphicsItemBarColorEditButton = ColorEditPushButton()

        self.modalScaleGraphicsItemTextColorLabel = QLabel("Text color: ")
        self.modalScaleGraphicsItemTextColorEditButton = ColorEditPushButton()
        
        self.barHeightValueLabel = \
            QLabel("ModalScale bar height:")
        self.barHeightValueSpinBox = QDoubleSpinBox()
        self.barHeightValueSpinBox.setMinimum(0.0)
        self.barHeightValueSpinBox.setMaximum(999999999.0)

        self.textFontSizeValueLabel = \
            QLabel("Text font size:")
        self.textFontSizeValueSpinBox = QDoubleSpinBox()
        self.textFontSizeValueSpinBox.setMinimum(0.0)
        self.textFontSizeValueSpinBox.setMaximum(999999999.0)

        self.textEnabledLabel = QLabel("Text is enabled:")
        self.textEnabledCheckBox = QCheckBox()
        self.textEnabledCheckBox.setCheckState(Qt.Unchecked)
        
        self.rotateDownButton = QPushButton("Rotate Down")
        self.rotateUpButton = QPushButton("Rotate Up")
        self.reverseButton = QPushButton("Reverse")
        self.checkMarkAllButton = QPushButton("Check All")
        self.checkMarkNoneButton = QPushButton("Check None")
        
        self.rotateButtonsLayout = QHBoxLayout()
        self.rotateButtonsLayout.addWidget(self.rotateDownButton)
        self.rotateButtonsLayout.addWidget(self.rotateUpButton)
        self.rotateButtonsLayout.addWidget(self.reverseButton)
        self.rotateButtonsLayout.addWidget(self.checkMarkAllButton)
        self.rotateButtonsLayout.addWidget(self.checkMarkNoneButton)
        self.rotateButtonsLayout.addStretch()
        
        self.startPointPriceValueLabel = \
            QLabel("ModalScale Start Point (in price):")
        self.startPointPriceValueSpinBox = QDoubleSpinBox()
        self.startPointPriceValueSpinBox.setMinimum(0.0)
        self.startPointPriceValueSpinBox.setMaximum(999999999.0)
        startPointPriceValueLayout = QHBoxLayout()
        startPointPriceValueLayout.addWidget(self.startPointPriceValueLabel)
        startPointPriceValueLayout.addStretch()
        startPointPriceValueLayout.addWidget(self.startPointPriceValueSpinBox)
        
        self.startPointDatetimeLocationWidget = TimestampEditWidget()
        self.startPointDatetimeLocationWidget.groupBox.\
            setTitle("ModalScale Start Point (in time)")
        self.startPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.startPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        self.endPointPriceValueLabel = \
            QLabel("ModalScale End Point (in price):")
        self.endPointPriceValueSpinBox = QDoubleSpinBox()
        self.endPointPriceValueSpinBox.setMinimum(0.0)
        self.endPointPriceValueSpinBox.setMaximum(999999999.0)
        endPointPriceValueLayout = QHBoxLayout()
        endPointPriceValueLayout.addWidget(self.endPointPriceValueLabel)
        endPointPriceValueLayout.addStretch()
        endPointPriceValueLayout.addWidget(self.endPointPriceValueSpinBox)
        
        self.endPointDatetimeLocationWidget = TimestampEditWidget()
        self.endPointDatetimeLocationWidget.groupBox.\
            setTitle("ModalScale End Point (in time)")
        self.endPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.endPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        # Layout.
        self.gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        self.gridLayout.addWidget(self.internalNameLabel, r, 0, al)
        self.gridLayout.addWidget(self.internalNameLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.uuidLabel, r, 0, al)
        self.gridLayout.addWidget(self.uuidLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.modalScaleGraphicsItemBarColorLabel,
                                  r, 0, al)
        self.gridLayout.addWidget(self.modalScaleGraphicsItemBarColorEditButton,
                                  r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.modalScaleGraphicsItemTextColorLabel,
                                  r, 0, al)
        self.gridLayout.\
            addWidget(self.modalScaleGraphicsItemTextColorEditButton,
                      r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.barHeightValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.barHeightValueSpinBox, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.textFontSizeValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.textFontSizeValueSpinBox, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.textEnabledLabel, r, 0, al)
        self.gridLayout.addWidget(self.textEnabledCheckBox, r, 1, al)
        r += 1
        self.gridLayout.addLayout(startPointPriceValueLayout, r, 0, al)
        self.gridLayout.addLayout(endPointPriceValueLayout, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.startPointDatetimeLocationWidget,
                                  r, 0, al)
        self.gridLayout.addWidget(self.endPointDatetimeLocationWidget,
                                  r, 1, al)
        r += 1

        # Layout for the musical ratio intervals.
        self.musicalRatiosGridLayout = QGridLayout()
        self.numMusicalRatios = 0

        # Holds the list of QCheckBox objects corresponding to the
        # MusicalRatios (ordered) in the artifact. 
        self.checkBoxes = []
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addLayout(self.rotateButtonsLayout)
        self.layout.addLayout(self.musicalRatiosGridLayout)
        
        self.groupBox.setLayout(self.layout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)
        
        # Now that all the widgets are created, load the values from the
        # artifact object.
        self.loadValues(artifact)

        self.setReadOnly(self.readOnlyFlag)
        
        # Connect signals and slots.

        self.barHeightValueSpinBox.valueChanged.\
            connect(self._handleBarHeightValueSpinBoxChanged)
        self.textFontSizeValueSpinBox.valueChanged.\
            connect(self._handleTextFontSizeValueSpinBoxChanged)
        self.textEnabledCheckBox.stateChanged.\
            connect(self._handleTextEnabledCheckBoxToggled)
        
        # Connect rotateUp and rotateDown buttons.
        self.rotateUpButton.clicked.\
            connect(self._handleRotateUpButtonClicked)
        self.rotateDownButton.clicked.\
            connect(self._handleRotateDownButtonClicked)
        self.reverseButton.clicked.\
            connect(self._handleReverseButtonClicked)
        self.checkMarkAllButton.clicked.\
            connect(self._handleCheckMarkAllButtonClicked)
        self.checkMarkNoneButton.clicked.\
            connect(self._handleCheckMarkNoneButtonClicked)

        # Connect the signals for the price and time values changing,
        # so that we can update the start and end points in the
        # artifact and update all the prices and datetimes in
        # between.
        self.startPointPriceValueSpinBox.valueChanged.\
            connect(self._saveAndReloadMusicalRatios)
        self.endPointPriceValueSpinBox.valueChanged.\
            connect(self. _saveAndReloadMusicalRatios)
        self.startPointDatetimeLocationWidget.valueChanged.\
            connect(self._saveAndReloadMusicalRatios)
        self.endPointDatetimeLocationWidget.valueChanged.\
            connect(self._saveAndReloadMusicalRatios)
        
        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        # Need to reload the artifact, so that the proper conversion
        # is done with the new conversion object.
        self.loadValues(self.artifact)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
        
    def getArtifact(self):
        """Returns the internally stored artifact object.

        Note: If saveValues() was called previously, then this object
        was updated with the values from the edit widgets.
        """

        return self.artifact
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
        ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.internalNameLineEdit.setReadOnly(True)
        self.uuidLineEdit.setReadOnly(True)
        self.barHeightValueSpinBox.setEnabled(not self.readOnlyFlag)
        self.textFontSizeValueSpinBox.setEnabled(not self.readOnlyFlag)
        self.textEnabledCheckBox.setEnabled(not self.readOnlyFlag)
        self.rotateDownButton.setEnabled(not self.readOnlyFlag)
        self.rotateUpButton.setEnabled(not self.readOnlyFlag)
        self.reverseButton.setEnabled(not self.readOnlyFlag)
        self.checkMarkAllButton.setEnabled(not self.readOnlyFlag)
        self.checkMarkNoneButton.setEnabled(not self.readOnlyFlag)
        self.startPointPriceValueSpinBox.setEnabled(not self.readOnlyFlag)
        self.startPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        self.endPointPriceValueSpinBox.setEnabled(not self.readOnlyFlag)
        self.endPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)

        for checkBox in self.checkBoxes:
            checkBox.setEnabled(not self.readOnlyFlag)
        
        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadValues(self, artifact):
        """Loads the widgets with values from the given
        PriceBarChartModalScaleArtifact.

        Arguments:
        
        artifact - PriceBarChartModalScaleArtifact object to load the
        values into the edit widgets.  
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if artifact == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  artifact can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        elif self.artifact is artifact:
            # They are the same, so no need to do a deep copy.
            # Just continue on, creating and loading the widgets.
            self.log.debug("Same artifact, no need for deep copy.")
        else:
            # Store a deep copy of the artifact because we manipulate
            # the musicalRatios list and its ordering.
            self.log.debug("Deep copying artifact...")
            self.artifact = copy.deepcopy(artifact)

        self.log.debug("Setting the widgets...")
        
        # Set the widgets.
        self.internalNameLineEdit.\
            setText(self.artifact.getInternalName())
        self.uuidLineEdit.\
            setText(str(self.artifact.getUuid()))
        self.modalScaleGraphicsItemBarColorEditButton.\
            setColor(self.artifact.getModalScaleGraphicsItemBarColor())
        self.modalScaleGraphicsItemTextColorEditButton.\
            setColor(self.artifact.getModalScaleGraphicsItemTextColor())
        self.barHeightValueSpinBox.\
            setValue(self.artifact.getModalScaleGraphicsItemBarHeight())
        self.textFontSizeValueSpinBox.\
            setValue(self.artifact.getModalScaleGraphicsItemFontSize())
                                        
        if self.artifact.isTextEnabled():
            self.textEnabledCheckBox.setCheckState(Qt.Checked)
        else:
            self.textEnabledCheckBox.setCheckState(Qt.Unchecked)

        startPointY = self.artifact.startPointF.y()
        startPointPrice = self.convertObj.sceneYPosToPrice(startPointY)
        self.startPointPriceValueSpinBox.setValue(startPointPrice)
        
        startPointX = self.artifact.startPointF.x()
        startPointDatetime = self.convertObj.sceneXPosToDatetime(startPointX)
        self.startPointDatetimeLocationWidget.\
            loadTimestamp(startPointDatetime)
        
        endPointY = self.artifact.endPointF.y()
        endPointPrice = self.convertObj.sceneYPosToPrice(endPointY)
        self.endPointPriceValueSpinBox.setValue(endPointPrice)
        
        endPointX = self.artifact.endPointF.x()
        endPointDatetime = self.convertObj.sceneXPosToDatetime(endPointX)
        self.endPointDatetimeLocationWidget.\
            loadTimestamp(endPointDatetime)

        self._reloadMusicalRatiosGrid()
        
        self.log.debug("Exiting loadValues()")

    def _reloadMusicalRatiosGrid(self):
        """Clears and recreates the self.musicalRatiosGridLayout
        according to teh values in self.artifact.
        """
        
        # Remove any old widgets that were in the grid layout from
        # the grid layout..
        for r in range(self.musicalRatiosGridLayout.rowCount()):
            for c in range(self.musicalRatiosGridLayout.columnCount()):
                # Get the QLayoutItem.
                item = self.musicalRatiosGridLayout.itemAtPosition(r, c)
                if item != None:
                    # Get the widget in the layout item.
                    widget = item.widget()
                    if widget != None:
                        widget.setEnabled(False)
                        widget.setVisible(False)
                        widget.setParent(None)

                        # Actually remove the widget from the
                        # QGridLayout.  
                        self.musicalRatiosGridLayout.removeWidget(widget)
                                
        # Row.
        r = 0
        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        # Create the musical ratio items in the
        # self.musicalRatiosGridLayout QGridLayout.
        musicalRatios = self.artifact.getMusicalRatios()
        self.numMusicalRatios = len(musicalRatios)

        # Clear the checkboxes list.
        self.checkBoxes = []

        rangeUsed = None
        if self.artifact.isReversed() == False:
            rangeUsed = range(self.numMusicalRatios)
        else:
            rangeUsed = reversed(range(self.numMusicalRatios))
            
        for i in rangeUsed:
            musicalRatio = musicalRatios[i]

            checkBox = QCheckBox("{}".format(musicalRatio.getRatio()))

            # Set the check state based on whether or not the musical
            # ratio is enabled.
            if musicalRatio.isEnabled():
                checkBox.setCheckState(Qt.Checked)
            else:
                checkBox.setCheckState(Qt.Unchecked)

            # Connect the signal to the slot function
            # _handleCheckMarkToggled().  That function will update
            # the self.artifact's musicalRatios with new check state.
            checkBox.stateChanged.connect(self._handleCheckMarkToggled)
            
            # Append to our list of checkboxes so that we can
            # reference them later and see what values are used in
            # them.  Remember, if we are reversed, then we will need
            # to reverse this list later.
            self.checkBoxes.append(checkBox)
            
            descriptionLabel = QLabel(musicalRatio.getDescription())

            # Use QLabels to
            # display the price and timestamp information.
            (x, y) = self.artifact.getXYForMusicalRatio(i)
                
            price = self.convertObj.sceneYPosToPrice(y)
            priceStr = "{}".format(price)
            priceWidget = QLabel(priceStr)

            timestamp = self.convertObj.sceneXPosToDatetime(x)
            timestampStr = Ephemeris.datetimeToDayStr(timestamp)
            timestampWidget = QLabel(timestampStr)

            # Actually add the widgets to the grid layout.
            self.musicalRatiosGridLayout.addWidget(checkBox, r, 0, al)
            self.musicalRatiosGridLayout.addWidget(descriptionLabel, r, 1, al)
            self.musicalRatiosGridLayout.addWidget(priceWidget, r, 2, al)
            self.musicalRatiosGridLayout.addWidget(timestampWidget, r, 3, al)

            r += 1

        # Reverse the self.checkBoxes list if we are reversed, since
        # if that is the case, then previously in this function we
        # added the checkBoxes in the reverse order.
        if self.artifact.isReversed():
            self.checkBoxes.reverse()
            
    def saveValues(self):
        """Saves the values in the widgets to the internally stored
        PriceBarChartModalScaleArtifact object.
        """

        self.log.debug("Entered saveValues()")

        # Get the colors.
        barColor = self.modalScaleGraphicsItemBarColorEditButton.getColor()
        textColor = self.modalScaleGraphicsItemTextColorEditButton.getColor()
        
        # Call save on the timestamp widgets.
        self.startPointDatetimeLocationWidget.saveTimestamp()
        self.endPointDatetimeLocationWidget.saveTimestamp()
        
        # Position and start point should be the same values.
        startPointPrice = \
            self.startPointPriceValueSpinBox.value()
        startPointY = self.convertObj.priceToSceneYPos(startPointPrice)
        endPointPrice = \
            self.endPointPriceValueSpinBox.value()
        endPointY = self.convertObj.priceToSceneYPos(endPointPrice)
        
        startPointDatetime = \
            self.startPointDatetimeLocationWidget.getTimestamp()
        endPointDatetime = \
            self.endPointDatetimeLocationWidget.getTimestamp()
                          
        startPointX = self.convertObj.datetimeToSceneXPos(startPointDatetime)
        endPointX = self.convertObj.datetimeToSceneXPos(endPointDatetime)

        posF = QPointF(startPointX, startPointY)
        startPointF = QPointF(startPointX, startPointY)
        endPointF = QPointF(endPointX, endPointY)

        # Set the values in the artifact.
        self.artifact.setPos(posF)
        self.artifact.setModalScaleGraphicsItemBarColor(barColor)
        self.artifact.setModalScaleGraphicsItemTextColor(textColor)
        self.artifact.setStartPointF(startPointF)
        self.artifact.setEndPointF(endPointF)

        # No need to save the musicalRatios inside self.artifact,
        # because each time there is a rotation or a check-marking
        # action, the internal artifact was updated.
        # The same is the case for the self.artifact.setReversed().

        self.log.debug("Exiting saveValues()")

    def _handleBarHeightValueSpinBoxChanged(self):
        """Called when the self.barHeightValueSpinBox is modified."""

        self.artifact.setModalScaleGraphicsItemBarHeight(\
            self.barHeightValueSpinBox.value())
        
    def _handleTextFontSizeValueSpinBoxChanged(self):
        """Called when the self.textFontSizeValueSpinBox is modified."""

        self.artifact.setModalScaleGraphicsItemFontSize(\
            self.textFontSizeValueSpinBox.value())
        
    def _handleTextEnabledCheckBoxToggled(self):
        """Called when the textEnabledCheckBox is checked or unchecked."""

        newValue = None
        
        if self.textEnabledCheckBox.checkState() == Qt.Checked:
            newValue = True
        else:
            newValue = False
        
        self.artifact.setTextEnabled(newValue)
        
    def _handleCheckMarkToggled(self):
        """Called when one of the check-mark boxes on the
        musicalRatios is checked or unchecked.
        """

        # Go through all the musicalRatios in the widget, and set them
        # as enabled or disabled in the artifact, based on the check
        # state of the QCheckBox objects in self.checkBoxes.
        for i in range(len(self.checkBoxes)):
            oldValue = self.artifact.getMusicalRatios()[i].isEnabled()
            newValue = None
            if self.checkBoxes[i].checkState() == Qt.Checked:
                newValue = True
            else:
                newValue = False

            if oldValue != newValue:
                self.log.debug("Updating enabled state of " +
                               "musicalRatio[{}] from {} to {}".\
                               format(i, oldValue, newValue))
                self.artifact.getMusicalRatios()[i].setEnabled(newValue)
            else:
                #self.log.debug("No update to musicalRatio[{}]".format(i))
                pass

    def _saveAndReloadMusicalRatios(self):
        """Saves and reloads the musical ratio widgets."""
        
        # Save values from what is in the widgets to the internal artifact.
        self.saveValues()
        
        # Reload the musicalRatiosGrid.
        self._reloadMusicalRatiosGrid()
    
    def _handleRotateDownButtonClicked(self):
        """Called when the 'Rotate Down' button is clicked."""

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.artifact.getMusicalRatios()

        if self.artifact.isReversed() == False:
            # Put the last musical ratio in the front.
            if len(musicalRatios) > 0:
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        else:
            # Put the first musical ratio in the back.
            if len(musicalRatios) > 0:
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
            
        # Overwrite the old list in the internally stored artifact.
        self.artifact.setMusicalRatios(musicalRatios)

        # Reload the musicalRatiosGrid.
        self._reloadMusicalRatiosGrid()
    
    def _handleRotateUpButtonClicked(self):
        """Called when the 'Rotate Up' button is clicked."""

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.artifact.getMusicalRatios()
        
        if self.artifact.isReversed() == False:
            # Put the first musical ratio in the back.
            if len(musicalRatios) > 0:
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        else:
            # Put the first musical ratio in the back.
            if len(musicalRatios) > 0:
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)

        # Overwrite the old list in the internally stored artifact.
        self.artifact.setMusicalRatios(musicalRatios)

        # Reload the musicalRatiosGrid.
        self._reloadMusicalRatiosGrid()
    
    def _handleReverseButtonClicked(self):
        """Called when the 'Reverse' button is clicked."""

        # Flip the flag that indicates that the musical ratios are reversed.
        self.artifact.setReversed(not self.artifact.isReversed())
        
        # Reload the musicalRatiosGrid.
        self._reloadMusicalRatiosGrid()
    
    def _handleCheckMarkAllButtonClicked(self):
        """Called when the 'Check All' button is clicked."""


        for checkBox in self.checkBoxes:
            checkBox.setCheckState(Qt.Checked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleCheckMarkToggled()
        
    def _handleCheckMarkNoneButtonClicked(self):
        """Called when the 'Check None' button is clicked."""


        for checkBox in self.checkBoxes:
            checkBox.setCheckState(Qt.Unchecked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleCheckMarkToggled()
        
    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartModalScaleArtifactEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceBarChartModalScaleArtifact.
    """

    def __init__(self,
                 priceBarChartModalScaleArtifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceBarChartModalScaleArtifact.
        
        Note: The 'priceBarChartModalScaleArtifact' object gets modified
        if the user clicks the 'Okay' button.

        Arguments:
        artifact - PriceBarChartModalScaleArtifact object to edit.
                   This object gets modified if the user clicks the
                   'Okay' button.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("pricebarchart_dialogs.PriceBarChartModalScaleArtifactEditDialog")

        self.setWindowTitle("Edit PriceBarChartModalScaleArtifact Data")

        # Check input.
        if not isinstance(priceBarChartModalScaleArtifact,
                          PriceBarChartModalScaleArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      " constructor.")
            return

        # Save a reference to the artifact object.
        self.artifact = priceBarChartModalScaleArtifact

        # Save a reference to the conversion object.
        self.convertObj = convertObj
        
        # Save the readOnlyFlag value.
        self.readOnlyFlag = readOnlyFlag
        
        # Create the contents.
        self.editWidget = \
            PriceBarChartModalScaleArtifactEditWidget(self.artifact,
                                                    self.convertObj,
                                                    self.readOnlyFlag)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
                       ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        self.editWidget.setReadOnly(self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields.
        """
        
        return self.readOnlyFlag

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        self.editWidget.setConvertObj(self.convertObj)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
    def setArtifact(self, artifact):
        """Loads the edit widget with the given artifact object.
        
        Note:  Upon clicking 'Okay' this object will be modified.

        Arguments:
        artifact - PriceBarChartModalScaleArtifact object to load the
                   widgets with.
        """

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartModalScaleArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      ".setArtifact()")
            return

        self.artifact = artifact

        self.editWidget.loadValues(self.artifact)

    def getArtifact(self):
        """Returns a reference to the artifact object.  If the 'Okay'
        button was previously clicked, then this object contains new
        values as set with the widget, otherwise it is unchanged.
        """

        # The edit widget keeps its own copy of the artifact, which it
        # modifies directly.
        if self.result() == QDialog.Accepted:
            return self.editWidget.getArtifact()
        else:
            return self.artifact


def testPriceBarChartTextArtifactEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Create an artifact.
    artifact = PriceBarChartTextArtifact()

    # Set the artifact's position.  It needs to be at a position where
    # the converted datetime.datetime is greater than the
    # datetime.datetime.MINYEAR.  A X value of 2450000 is in year 1995.
    pos = QPointF(2450000, -1000)
    artifact.setPos(pos)

    # TODO:  set more stuff in artifact to better fully test this.
    
    # Create an object for doing unit conversions.
    eastern = pytz.timezone('US/Eastern')
    from pricebarchart import PriceBarChartGraphicsScene
    convertObj = PriceBarChartGraphicsScene()
    convertObj.setTimezone(eastern)
    
    # Run the dialog in readonly mode.
    print("Before (readonly), PriceBarChartTextArtifactEditDialog: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartTextArtifactEditDialog(artifact,
                                                 convertObj,
                                                 readOnlyFlag=True)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (readonly), PriceBarChartTextArtifact: {}".\
          format(artifact.toString()))

    
    # Run the dialog in non-readonly mode.
    print("Before (not readonly), PriceBarChartTextArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartTextArtifactEditDialog(artifact,
                                                 convertObj,
                                                 readOnlyFlag=False)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (not readonly), PriceBarChartTextArtifact: {}".\
          format(artifact.toString()))

    
def testPriceBarChartBarCountArtifactEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Create an artifact.
    artifact = PriceBarChartBarCountArtifact()

    # Set the artifact's position and start/end points.  It needs to
    # be at a position where the converted datetime.datetime is
    # greater than the datetime.datetime.MINYEAR.
    # A X value of 2450000 is in year 1995.
    pos = QPointF(2450000, -1000)
    artifact.setPos(pos)
    artifact.setStartPointF(pos)
    artifact.setEndPointF(QPoint(pos.x() + 1000, pos.y()))

    # Create an object for doing unit conversions.
    eastern = pytz.timezone('US/Eastern')
    from pricebarchart import PriceBarChartGraphicsScene
    convertObj = PriceBarChartGraphicsScene()
    convertObj.setTimezone(eastern)
    
    # Run the dialog in readonly mode.
    print("Before (readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=True)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))

    
    # Run the dialog in non-readonly mode.
    print("Before (not readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=False)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (not readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))

    
def testPriceBarChartTimeMeasurementArtifactEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Create an artifact.
    artifact = PriceBarChartTimeMeasurementArtifact()

    # Set the artifact's position and start/end points.  It needs to
    # be at a position where the converted datetime.datetime is
    # greater than the datetime.datetime.MINYEAR.
    # A X value of 2450000 is in year 1995.
    pos = QPointF(2450000, -1000)
    artifact.setPos(pos)
    artifact.setStartPointF(pos)
    artifact.setEndPointF(QPoint(pos.x() + 1000, pos.y()))

    # Create an object for doing unit conversions.
    eastern = pytz.timezone('US/Eastern')
    from pricebarchart import PriceBarChartGraphicsScene
    convertObj = PriceBarChartGraphicsScene()
    convertObj.setTimezone(eastern)
    
    # Run the dialog in readonly mode.
    print("Before (readonly), PriceBarChartTimeMeasurementArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=True)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (readonly), PriceBarChartTimeMeasurementArtifact: {}".\
          format(artifact.toString()))

    
    # Run the dialog in non-readonly mode.
    print("Before (not readonly), PriceBarChartTimeMeasurementArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=False)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (not readonly), PriceBarChartTimeMeasurementArtifact: {}".\
          format(artifact.toString()))
    

def testPriceBarChartModalScaleArtifactEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Create an artifact.
    artifact = PriceBarChartModalScaleArtifact()

    # Set the artifact's position and start/end points.  It needs to
    # be at a position where the converted datetime.datetime is
    # greater than the datetime.datetime.MINYEAR.
    # A X value of 2450000 is in year 1995.
    pos = QPointF(2450000, -1000)
    artifact.setPos(pos)
    artifact.setStartPointF(pos)
    artifact.setEndPointF(QPoint(pos.x() + 1000, pos.y() - 1000))

    # Create an object for doing unit conversions.
    eastern = pytz.timezone('US/Eastern')
    from pricebarchart import PriceBarChartGraphicsScene
    convertObj = PriceBarChartGraphicsScene()
    convertObj.setTimezone(eastern)
    
    # Run the dialog in readonly mode.
    print("Before (readonly), PriceBarChartModalScaleArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartModalScaleArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=True)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (readonly), PriceBarChartModalScaleArtifact: {}".\
          format(artifact.toString()))

    
    # Run the dialog in non-readonly mode.
    print("Before (not readonly), PriceBarChartModalScaleArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartModalScaleArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=False)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (not readonly), PriceBarChartModalScaleArtifact: {}".\
          format(artifact.toString()))
    

# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    import os
    import sys
    
    from ephemeris import Ephemeris
    
    # Initialize the Ephemeris (required).
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)
    
    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)

    # Various tests to run:
    testPriceBarChartTextArtifactEditDialog()
    #testPriceBarChartBarCountArtifactEditDialog()
    #testPriceBarChartTimeMeasurementArtifactEditDialog()
    #testPriceBarChartModalScaleArtifactEditDialog()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

