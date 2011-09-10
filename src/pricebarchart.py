
# For line separator.
import os

# For logging.
import logging

# For copy.deepcopy().
import copy

# For dynamically adding methods to instances.
import types

# For calculating square roots and other calculations.
import math

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

# For QSettings keys.
from settings import SettingsKeys

# For PriceBars and artifacts in the chart.
from data_objects import BirthInfo
from data_objects import PriceBar
from data_objects import MusicalRatio
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartTimeMeasurementArtifact
from data_objects import PriceBarChartTimeModalScaleArtifact
from data_objects import PriceBarChartPriceModalScaleArtifact
from data_objects import PriceBarChartTextArtifact
from data_objects import PriceBarChartPriceTimeInfoArtifact
from data_objects import PriceBarChartPriceMeasurementArtifact
from data_objects import PriceBarChartTimeRetracementArtifact
from data_objects import PriceBarChartPriceRetracementArtifact
from data_objects import PriceBarChartPriceTimeVectorArtifact
from data_objects import PriceBarChartLineSegmentArtifact
from data_objects import PriceBarChartOctaveFanArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings
from data_objects import Util

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris

# For edit dialogs for modifying the PriceBarChartArtifact objects of
# various PriceBarChartArtifactGraphicsItems.
from pricebarchart_dialogs import PriceBarChartBarCountArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeMeasurementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeModalScaleArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceModalScaleArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTextArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceTimeInfoArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceMeasurementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeRetracementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceRetracementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceTimeVectorArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartLineSegmentArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartOctaveFanArtifactEditDialog

# For edit dialogs.
from dialogs import PriceBarEditDialog

class PriceBarGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar object.

    There exists two kinds of standard PriceBar drawings:
        - Candle
        - Bar with open and close

    This draws the second one.  It is displayed as a bar with open
    and close ticks on the left and right side.  The bar is drawn with a
    green pen if the high is higher than or equal the low, and drawn as
    red otherwise.
    """
    
    def __init__(self, parent=None, scene=None):

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarGraphicsItem")
        self.log.debug("Entered __init__().")

        super().__init__(parent, scene)

        # Pen width for PriceBars.
        self.penWidth = \
            PriceBarChartSettings.defaultPriceBarGraphicsItemPenWidth

        # Width of the left extension drawn that represents the open price.
        self.leftExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemLeftExtensionWidth 

        # Width of the right extension drawn that represents the close price.
        self.rightExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemRightExtensionWidth 


        # Internally stored PriceBar.
        self.priceBar = None

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(self.penWidth)

        # Color setting for a PriceBar that has a higher close than open.
        self.higherPriceBarColor = \
            SettingsKeys.higherPriceBarColorSettingsDefValue

        # Color setting for a PriceBar that has a lower close than open.
        self.lowerPriceBarColor = \
            SettingsKeys.lowerPriceBarColorSettingsDefValue

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()


    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        # priceBarGraphicsItemPenWidth (float).
        self.penWidth = priceBarChartSettings.priceBarGraphicsItemPenWidth

        # priceBarGraphicsItemLeftExtensionWidth (float).
        self.leftExtensionWidth = \
            priceBarChartSettings.priceBarGraphicsItemLeftExtensionWidth

        # priceBarGraphicsItemRightExtensionWidth (float).
        self.rightExtensionWidth = \
            priceBarChartSettings.priceBarGraphicsItemRightExtensionWidth


        # Update the pen.
        self.pen.setWidthF(self.penWidth)

        # Schedule an update.
        self.update()


    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # higherPriceBarColor
        key = SettingsKeys.higherPriceBarColorSettingsKey
        defaultValue = \
            SettingsKeys.higherPriceBarColorSettingsDefValue
        self.higherPriceBarColor = \
            QColor(settings.value(key, defaultValue))

        # lowerPriceBarColor
        key = SettingsKeys.lowerPriceBarColorSettingsKey
        defaultValue = \
            SettingsKeys.lowerPriceBarColorSettingsDefValue
        self.lowerPriceBarColor = \
            QColor(settings.value(key, defaultValue))


    def setPriceBar(self, priceBar):
        """Sets the internally used priceBar.  
        This has an effect on the color of the pricebar.
        """

        self.log.debug("Entered setPriceBar().  priceBar={}".\
                       format(priceBar.toString()))

        self.priceBar = priceBar

        # Set if it is a green or red pricebar.
        if self.priceBar != None:
            if self.priceBar.open <= self.priceBar.close:
                self.setPriceBarColor(self.higherPriceBarColor)
            else:
                self.setPriceBarColor(self.lowerPriceBarColor)
        else:
            # PriceBar is None.  Just use a black bar.
            self.setPriceBarColor(Qt.black)

        # Schedule an update to redraw the QGraphicsItem.
        self.update()

        self.log.debug("Leaving setPriceBar().")

    def getPriceBar(self):
        """Returns the internally stored PriceBar.
        If no PriceBar was previously stored in
        this PriceBarGraphicsItem, then None is returned.
        """

        return self.priceBar
    
    def setPriceBarColor(self, color):
        """Sets the color of the price bar."""

        self.log.debug("Entered setPriceBarColor().")

        if self.pen.color() != color:
            self.log.debug("Updating pen color.")
            self.pen.setColor(color)
            self.update()

        self.log.debug("Leaving setPriceBarColor().")

    def getPriceBarOpenScenePoint(self):
        """Returns the scene coordinates of the open point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the open of this
        pricebar is.
        """

        openPrice = 0.0
        high = 0.0
        low = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) * 0.5

        x = 0.0
        yOpen = -1.0 * (openPrice - priceMidpoint)
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yOpen))

        return rv


    def getPriceBarHighScenePoint(self):
        """Returns the scene coordinates of the high point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) * 0.5

        x = 0.0
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yHigh))

        return rv


    def getPriceBarLowScenePoint(self):
        """Returns the scene coordinates of the low point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) * 0.5

        x = 0.0
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yLow))

        return rv

    def getPriceBarCloseScenePoint(self):
        """Returns the scene coordinates of the close point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the close of this
        pricebar is.
        """

        close = 0.0
        high = 0.0
        low = 0.0

        if self.priceBar != None:
            close = self.priceBar.close
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) * 0.5

        x = 0.0
        yClose = -1.0 * (close - priceMidpoint)
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yClose))

        return rv


    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinates (0, 0) is the center of the widget.  
        # The QRectF returned should be related to this point as the
        # center.

        halfPenWidth = self.penWidth * 0.5

        openPrice = 0.0
        highPrice = 0.0
        lowPrice = 0.0
        closePrice = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            highPrice = self.priceBar.high
            lowPrice = self.priceBar.low
            closePrice = self.priceBar.close

        # For X we have:
        #     leftExtensionWidth units for the left extension (open price)
        #     rightExtensionWidth units for the right extension (close price)
        #     halfPenWidth on the left side
        #     halfPenWidth on the right side

        # For Y we have:
        #     halfPenWidth for the bottom side.
        #     priceRange units
        #     halfPenWidth for the top side

        priceRange = abs(highPrice - lowPrice)

        x = -1.0 * (self.leftExtensionWidth + halfPenWidth)
        y = -1.0 * ((priceRange * 0.5) + halfPenWidth)

        height = halfPenWidth + priceRange + halfPenWidth

        width = \
                halfPenWidth + \
                self.leftExtensionWidth + \
                self.rightExtensionWidth + \
                halfPenWidth

        return QRectF(x, y, width, height)

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        openPrice = 0.0
        highPrice = 0.0
        lowPrice = 0.0
        closePrice = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            highPrice = self.priceBar.high
            lowPrice = self.priceBar.low
            closePrice = self.priceBar.close

        priceRange = abs(highPrice - lowPrice)
        priceMidpoint = (highPrice + lowPrice) * 0.5

        # Draw the stem.
        x1 = 0.0
        y1 = 1.0 * (priceRange * 0.5)
        x2 = 0.0
        y2 = -1.0 * (priceRange * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the left extension (open price).
        x1 = 0.0
        y1 = -1.0 * (openPrice - priceMidpoint)
        x2 = -1.0 * self.leftExtensionWidth
        y2 = y1

        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right extension (close price).
        x1 = 0.0
        y1 = -1.0 * (closePrice - priceMidpoint)
        x2 = 1.0 * self.rightExtensionWidth
        y2 = y1
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.pen.widthF() * 0.5;
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceBarGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceBarGraphicsItem to handle the desired functionality.

        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        # Set the menu title.
        if self.priceBar != None:
            datetimeObj = self.priceBar.timestamp
            timestampStr = Ephemeris.datetimeToDayStr(datetimeObj)
            menu.setTitle("PriceBar_" + timestampStr)
        else:
            menu.setTitle("PriceBar_" + "Unknown")
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setAstro1Action = QAction("Set timestamp on Astro Chart &1", parent)
        setAstro2Action = QAction("Set timestamp on Astro Chart &2", parent)
        setAstro3Action = QAction("Set timestamp on Astro Chart &3", parent)
        openJHoraAction = QAction("Open JHor&a with timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setAstro1Action.triggered.\
            connect(self._handleSetAstro1Action)
        setAstro2Action.triggered.\
            connect(self._handleSetAstro2Action)
        setAstro3Action.triggered.\
            connect(self._handleSetAstro3Action)
        openJHoraAction.triggered.\
            connect(self._handleOpenJHoraAction)
                    
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(False)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setAstro1Action.setEnabled(True)
        setAstro2Action.setEnabled(True)
        setAstro3Action.setEnabled(True)
        openJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setAstro1Action)
        menu.addAction(setAstro2Action)
        menu.addAction(setAstro3Action)
        menu.addAction(openJHoraAction)
        
        return menu

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""

        scene = self.scene()
        scene.removeItem(self)
        scene.priceBarChartChanged.emit()

    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem pricebar.
        """

        pb = self.getPriceBar()
        
        dialog = PriceBarEditDialog(priceBar=pb, readOnly=True)

        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem pricebar.
        """

        pb = self.getPriceBar()
        
        dialog = PriceBarEditDialog(priceBar=pb, readOnly=False)

        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # Set the item with the new values.

            self.setPriceBar(dialog.getPriceBar())

            # X location based on the timestamp.
            x = self.scene().datetimeToSceneXPos(self.priceBar.timestamp)

            # Y location based on the mid price (average of high and low).
            y = self.scene().priceToSceneYPos(self.priceBar.midPrice())

            # Set the position, in parent coordinates.
            self.setPos(QPointF(x, y))

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()
            
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart1(self.scenePos().x())
        
    def _handleSetAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart2(self.scenePos().x())
        
    def _handleSetAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart3(self.scenePos().x())

    def _handleOpenJHoraAction(self):
        """Causes the timestamp of this PriceBarGraphicsItem to be
        opened in JHora.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().openJHora(self.scenePos().x())
        
class PriceBarChartArtifactGraphicsItem(QGraphicsItem):
    """QGraphicsItem that has members to indicate and set the
    readOnly mode.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartArtifactGraphicsItem")
        
        self.readOnlyFlag = True
        self.artifact = None
        
    def setReadOnlyFlag(self, flag):
        self.readOnlyFlag = flag

    def getReadOnlyFlag(self):
        return self.readOnlyFlag

    def setArtifact(self, artifact):
        """Virtual function that is meant to be overwritten by a child class to
        implement the custom functionality of loading the internals of the
        PriceBarChart GraphicsItem, so that it may be displayed in the chart.

        Arguments:
        artifact - PriceBarChartArtifact object to store.
        """

        self.log.debug("Entered " + \
                       "PriceBarChartArtifactGraphicsItem.setArtifact()")

        self.artifact = artifact
        
        self.log.debug("Exiting " + \
                       "PriceBarChartArtifactGraphicsItem.setArtifact()")

    def getArtifact(self):
        """Returns the PriceBarChartArtifact associated with this
        PriceBarChartArtifactGraphicsItem.
        """

        self.log.debug("Entered " + \
                       "PriceBarChartArtifactGraphicsItem.getArtifact()")
        
        if artifact == None:
            raise TypeError("Expected artifact to be not None.")

        self.log.debug("Exiting " + \
                       "PriceBarChartArtifactGraphicsItem.getArtifact()")
        
        return artifact


class TextGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBarChartTextArtifact."""
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTextArtifact()

        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(0.0, 0.0)

        # Set the font of the text.
        self.textItemFont = self.artifact.getFont()
        self.textItem.setFont(self.textItemFont)

        # Set the color of the text.
        self.color = self.artifact.getColor()
        
        # Set the pen color of the text.
        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.artifact.getColor())
        self.textItem.setPen(self.textItemPen)

        # Set the brush color of the text.
        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.artifact.getColor())
        self.textItem.setBrush(self.textItemBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.artifact.getTextXScaling(), \
                            self.artifact.getTextYScaling())
        self.textItem.setTransform(textTransform)

    def setText(self, text):
        """Sets the text in this graphics item.

        Arguments:
        text - str value for the new text.
        """

        self.textItem.setText(text)
        
    def getText(self):
        """Returns the text in this graphics item as a str."""

        return self.textItem.text()
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTextArtifact object's data
        into this QGraphicsTextItem.

        Arguments:
        artifact - PriceBarChartTextArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entered setArtifact()")

        if isinstance(artifact, PriceBarChartTextArtifact):
            self.artifact = artifact

            self.log.debug("Setting TextGraphicsItem with the " +
                           "following artifact: " + self.artifact.toString())
            self.log.debug("Font in artifact is: " +
                           self.artifact.getFont().toString())
                           
            # Extract and set the internals according to the info 
            # in self.artifact.
            self.setPos(self.artifact.getPos())
            
            # Internal QGraphicsItem that holds the text of the bar count.
            # Initialize to blank and set at the end point.
            self.textItem.setText(self.artifact.getText())

            # Set the font of the text.
            self.textItemFont = self.artifact.getFont()
            self.textItem.setFont(self.textItemFont)

            # Set the color of the text.
            self.color = self.artifact.getColor()
            
            # Set the pen color of the text.
            self.textItemPen = self.textItem.pen()
            self.textItemPen.setColor(self.color)
            self.textItem.setPen(self.textItemPen)

            # Set the brush color of the text.
            self.textItemBrush = self.textItem.brush()
            self.textItemBrush.setColor(self.color)
            self.textItem.setBrush(self.textItemBrush)

            # Apply some size scaling to the text.
            self.textTransform = QTransform()
            self.textTransform.scale(self.artifact.getTextXScaling(), \
                                     self.artifact.getTextYScaling())
            self.textItem.setTransform(self.textTransform)

        else:
            raise TypeError("Expected artifact type: PriceBarChartTextArtifact")
    
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTextArtifact to be 
        # current, then return it.
        self.artifact.setPos(self.pos())
        self.artifact.setText(self.textItem.text())
        self.artifact.setFont(self.textItemFont)
        self.artifact.setColor(self.color)
        self.artifact.setTextXScaling(self.textTransform.m11())
        self.artifact.setTextYScaling(self.textTransform.m22())
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        # Set values from the priceBarChartSettings into the internal
        # member variables.
        
        self.textItemFont = QFont()
        self.textItemFont.fromString(priceBarChartSettings.\
                                     textGraphicsItemDefaultFontDescription) 
        self.color = \
            priceBarChartSettings.textGraphicsItemDefaultColor
        
        self.textTransform = QTransform()
        self.textTransform.scale(priceBarChartSettings.\
                                 textGraphicsItemDefaultXScaling,
                                 priceBarChartSettings.\
                                 textGraphicsItemDefaultYScaling)

        # Update the internal text item.
        self.textItem.setFont(self.textItemFont)

        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.color)
        self.textItem.setPen(self.textItemPen)

        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.color)
        self.textItem.setBrush(self.textItemBrush)

        self.textItem.setTransform(self.textTransform)

        # Schedule an update.
        self.prepareGeometryChange()
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        pass
    
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Arguments:
        pos - QPointF holding the new position.
        """
        
        super().setPos(pos)
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the location of the internal text item
        # in local coordinates.  The QRectF returned is relative to
        # this (0, 0) point.

        textItemBoundingRect = self.textItem.boundingRect()

        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        width = textItemBoundingRect.width()
        height = textItemBoundingRect.height()

        newWidth = width * self.textTransform.m11()
        newHeight = height * self.textTransform.m22()

        textItemBoundingRect.setWidth(newWidth)
        textItemBoundingRect.setHeight(newHeight)
        
        return textItemBoundingRect

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.textItemPen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.textItemPen:
            painter.setPen(QPen(self.textItemPen))

        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.textItemPen.widthF() * 0.5;
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceBarChartArtifactGraphicsItem.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()

        self.log.debug("Inside _handleInfoAction(): artifact is: " +
                       artifact.toString())
        
        dialog = PriceBarChartTextArtifactEditDialog(artifact,
                                                     self.scene(),
                                                     readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTextArtifactEditDialog(artifact,
                                                     self.scene(),
                                                     readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
        
class BarCountGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new BarCountGraphicsItem the position
    and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger("pricebarchart.BarCountGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Color of the bar count graphicsitems.
        self.barCountGraphicsItemColor = \
            SettingsKeys.barCountGraphicsItemColorSettingsDefValue

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.barCountGraphicsItemTextColor = \
            SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue

        # Height of the vertical bar drawn.
        self.barCountGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.barCountFontSize = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemFontSize 

        # X scaling of the text.
        self.barCountTextXScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.barCountTextYScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartBarCountArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.barCountPenWidth = 0.0
        self.barCountPen = QPen()
        self.barCountPen.setColor(self.barCountGraphicsItemColor)
        self.barCountPen.setWidthF(self.barCountPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Number of PriceBars between self.startPointF and self.endPointF.
        self.barCount = 0

        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.barCountText = QGraphicsSimpleTextItem("", self)
        self.barCountText.setPos(self.endPointF)

        # Set the font of the text.
        self.barCountTextFont = QFont()
        self.barCountTextFont.setPointSizeF(self.barCountFontSize)
        self.barCountText.setFont(self.barCountTextFont)

        # Set the pen color of the text.
        self.barCountTextPen = self.barCountText.pen()
        self.barCountTextPen.setColor(self.barCountGraphicsItemTextColor)
        self.barCountText.setPen(self.barCountTextPen)

        # Set the brush color of the text.
        self.barCountTextBrush = self.barCountText.brush()
        self.barCountTextBrush.setColor(self.barCountGraphicsItemTextColor)
        self.barCountText.setBrush(self.barCountTextBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.barCountTextXScaling, \
                            self.barCountTextYScaling)
        self.barCountText.setTransform(textTransform)

        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.barCountGraphicsItemBarHeight = \
            priceBarChartSettings.\
                barCountGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.barCountFontSize = \
            priceBarChartSettings.\
                barCountGraphicsItemFontSize 

        # X scaling of the text.
        self.barCountTextXScaling = \
            priceBarChartSettings.\
                barCountGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.barCountTextYScaling = \
            priceBarChartSettings.\
                barCountGraphicsItemTextYScaling 

        # Set the font size of the text.
        self.log.debug("Setting font size to: {}".format(self.barCountFontSize))
        self.barCountTextFont = QFont()
        self.barCountTextFont.setPointSizeF(self.barCountFontSize)
        self.barCountText.setFont(self.barCountTextFont)

        # Apply some size scaling to the text.
        self.log.debug("Setting transform: (dx={}, dy={})".\
                       format(self.barCountTextXScaling,
                              self.barCountTextYScaling))
        textTransform = QTransform()
        textTransform.scale(self.barCountTextXScaling, \
                            self.barCountTextYScaling)
        self.barCountText.setTransform(textTransform)

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # barCountGraphicsItemColor
        key = SettingsKeys.barCountGraphicsItemColorSettingsKey
        defaultValue = \
            SettingsKeys.barCountGraphicsItemColorSettingsDefValue
        self.barCountGraphicsItemColor = \
            QColor(settings.value(key, defaultValue))

        # barCountGraphicsItemTextColor
        key = SettingsKeys.barCountGraphicsItemTextColorSettingsKey
        defaultValue = \
            SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue
        self.barCountGraphicsItemTextColor = \
            QColor(settings.value(key, defaultValue))
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.startPointF.setX(round(self.startPointF.x()))
        self.endPointF = self.endPointF + posDelta
        self.endPointF.setX(round(self.endPointF.x()))

        if self.scene() != None:
            self.recalculateBarCount()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            self.log.debug("DEBUG: " + \
                           "getReadOnlyFlag() == True, so passing to super()")
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointX <= scenePosX <= startThreshold or \
                   startingPointX >= scenePosX >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))

            elif endingPointX <= scenePosX <= endThreshold or \
                   endingPointX >= scenePosX >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.  Do the move, but also set emit that the
                    # PriceBarChart has changed.
                    super().mouseMoveEvent(event)
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()
            
            self.prepareGeometryChange()

            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()

            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        The actual start location drawn utilizes the mouse 
        location, and snaps to the closest whole X position.
        """

        #x = self._mousePosToNearestPriceBarX(pointF)
        x = round(pointF.x())

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)
            
            # Update the barCount label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            y = 0
            self.barCountText.setPos(QPointF(deltaX, y))

            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateBarCount()
                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        The actual start location drawn utilizes the mouse 
        location, and snaps to the closest whole X position.
        """

        #x = self._mousePosToNearestPriceBarX(pointF)
        x = round(pointF.x())

        newValue = QPointF(x, self.startPointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the barCount label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            y = 0
            self.barCountText.setPos(QPointF(deltaX, y))

            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateBarCount()
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            self.log.debug("Normalization of BarCountGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

        # Update the barCount label position.  For some reason, this
        # is required irregardless of the above if statement.  If we
        # don't do this, then some of the BarCountGraphicsItems
        # created can't be clicked on.  I'm not sure why that is...
        deltaX = self.endPointF.x() - self.startPointF.x()
        y = 0
        self.barCountText.setPos(QPointF(deltaX, y))
        
        self.recalculateBarCount()
        
        super().setPos(self.startPointF)

    def recalculateBarCount(self):
        """Sets the internal variable holding the number of bars in the
        X space between:

        (self.startPointF, self.endPointF]

        In the event self.startPointF or self.endPointF conjoin the X
        value of a PriceBar, the count excludes the bar conjoining
        self.startPointF and includes the bar conjoining self.endPointF.
        If the X values for both points are the same, then the bar count
        is zero.

        Returns:
        int value for the number of bars between the two points.
        """

        scene = self.scene()

        if scene == None:
            self.barCount = 0
        else:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

            # Reset the bar count.
            self.barCount = 0

            # Test for special case.
            if self.startPointF.x() == self.endPointF.x():
                self.barCount = 0
            else:
                # Go through the PriceBarGraphicsItems and count the ones in
                # between self.startPointF and self.endPointF.
                for item in graphicsItems:
                    if isinstance(item, PriceBarGraphicsItem):

                        x = item.getPriceBarHighScenePoint().x()

                        # Here we check for the bar being in between
                        # the self.startPointF and the self.endPointF.
                        # This handles the case when the start and end
                        # points are reversed also.
                        if (self.startPointF.x() < x <= self.endPointF.x()) or \
                           (self.endPointF.x() < x <= self.startPointF.x()):
                            
                            self.barCount += 1
                            

        # Update the text of the self.barCountText.
        self.barCountText.setText("{}".format(self.barCount))
        
        return self.barCount

    def setArtifact(self, artifact):
        """Loads a given PriceBarChartBarCountArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartBarCountArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartBarCountArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        # Need to recalculate the bar count, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the bar count will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateBarCount()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartBarCountArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartBarCountArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.

        # The QRectF returned is relative to this (0, 0) point.

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 * (self.barCountGraphicsItemBarHeight * 0.5))
        
        bottomRight = \
            QPointF(xDelta, 1.0 * (self.barCountGraphicsItemBarHeight * 0.5))
        
        rectWithoutText = QRectF(topLeft, bottomRight)

        return rectWithoutText

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.barCountPen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.barCountPen:
            painter.setPen(self.barCountPen)
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.barCountGraphicsItemBarHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (self.barCountGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.barCountGraphicsItemBarHeight * 0.5)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.barCountGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.barCountPen.widthF() * 0.5;
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this BarCountGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        BarCountGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        BarCountGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        BarCountGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        
        
class TimeMeasurementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a time measurement in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new TimeMeasurementGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.TimeMeasurementGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling 

        # Font.
        self.timeMeasurementTextFont = QFont()
        self.timeMeasurementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeMeasurementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeMeasurementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultColor

        # TimeMeasurementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtBarsTextFlag (bool).
        self.showSqrtBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdBarsTextFlag (bool).
        self.showSqrdBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdBarsTextFlag
    
        # TimeMeasurementGraphicsItem showHoursTextFlag (bool).
        self.showHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtHoursTextFlag (bool).
        self.showSqrtHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdHoursTextFlag (bool).
        self.showSqrdHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdHoursTextFlag
    
        # TimeMeasurementGraphicsItem showDaysTextFlag (bool).
        self.showDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtDaysTextFlag (bool).
        self.showSqrtDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdDaysTextFlag (bool).
        self.showSqrdDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdDaysTextFlag
    
        # TimeMeasurementGraphicsItem showWeeksTextFlag (bool).
        self.showWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.showSqrtWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdWeeksTextFlag (bool).
        self.showSqrdWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showMonthsTextFlag (bool).
        self.showMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMonthsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.showSqrtMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag

        # TimeMeasurementGraphicsItem showSqrdMonthsTextFlag (bool).
        self.showSqrdMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMonthsTextFlag

        # TimeMeasurementGraphicsItem showTimeRangeTextFlag (bool).
        self.showTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtTimeRangeTextFlag (bool).
        self.showSqrtTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdTimeRangeTextFlag (bool).
        self.showSqrdTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.showScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.showSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdScaledValueRangeTextFlag (bool).
        self.showSqrdScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag

        # TimeMeasurementGraphicsItem showAyanaTextFlag (bool).
        self.showAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrtAyanaTextFlag (bool).
        self.showSqrtAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrdAyanaTextFlag (bool).
        self.showSqrdAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdAyanaTextFlag

        # TimeMeasurementGraphicsItem showMuhurtaTextFlag (bool).
        self.showMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showSqrtMuhurtaTextFlag (bool).
        self.showSqrtMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showSqrdMuhurtaTextFlag (bool).
        self.showSqrdMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showVaraTextFlag (bool).
        self.showVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowVaraTextFlag

        # TimeMeasurementGraphicsItem showSqrtVaraTextFlag (bool).
        self.showSqrtVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtVaraTextFlag

        # TimeMeasurementGraphicsItem showSqrdVaraTextFlag (bool).
        self.showSqrdVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdVaraTextFlag

        # TimeMeasurementGraphicsItem showRtuTextFlag (bool).
        self.showRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowRtuTextFlag

        # TimeMeasurementGraphicsItem showSqrtRtuTextFlag (bool).
        self.showSqrtRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtRtuTextFlag

        # TimeMeasurementGraphicsItem showSqrdRtuTextFlag (bool).
        self.showSqrdRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdRtuTextFlag

        # TimeMeasurementGraphicsItem showMasaTextFlag (bool).
        self.showMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMasaTextFlag

        # TimeMeasurementGraphicsItem showSqrtMasaTextFlag (bool).
        self.showSqrtMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMasaTextFlag

        # TimeMeasurementGraphicsItem showSqrdMasaTextFlag (bool).
        self.showSqrdMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMasaTextFlag

        # TimeMeasurementGraphicsItem showPaksaTextFlag (bool).
        self.showPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowPaksaTextFlag

        # TimeMeasurementGraphicsItem showSqrtPaksaTextFlag (bool).
        self.showSqrtPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtPaksaTextFlag

        # TimeMeasurementGraphicsItem showSqrdPaksaTextFlag (bool).
        self.showSqrdPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdPaksaTextFlag

        # TimeMeasurementGraphicsItem showSamaTextFlag (bool).
        self.showSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSamaTextFlag

        # TimeMeasurementGraphicsItem showSqrtSamaTextFlag (bool).
        self.showSqrtSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtSamaTextFlag

        # TimeMeasurementGraphicsItem showSqrdSamaTextFlag (bool).
        self.showSqrdSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdSamaTextFlag
        
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTimeMeasurementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.timeMeasurementPenWidth = 0.0
        self.timeMeasurementPen = QPen()
        self.timeMeasurementPen.setColor(self.timeMeasurementGraphicsItemColor)
        self.timeMeasurementPen.setWidthF(self.timeMeasurementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Variables holding the time measurement values.
        self.numPriceBars = 0.0
        self.numSqrtPriceBars = 0.0
        self.numSqrdPriceBars = 0.0
        self.numHours = 0.0
        self.numSqrtHours = 0.0
        self.numSqrdHours = 0.0
        self.numDays = 0.0
        self.numSqrtDays = 0.0
        self.numSqrdDays = 0.0
        self.numWeeks = 0.0
        self.numSqrtWeeks = 0.0
        self.numSqrdWeeks = 0.0
        self.numMonths = 0.0
        self.numSqrtMonths = 0.0
        self.numSqrdMonths = 0.0
        self.numTimeRange = 0.0
        self.numSqrtTimeRange = 0.0
        self.numSqrdTimeRange = 0.0
        self.numScaledValueRange = 0.0
        self.numSqrtScaledValueRange = 0.0
        self.numSqrdScaledValueRange = 0.0
        self.numAyana = 0.0
        self.numSqrtAyana = 0.0
        self.numSqrdAyana = 0.0
        self.numMuhurta = 0.0
        self.numSqrtMuhurta = 0.0
        self.numSqrdMuhurta = 0.0
        self.numVara = 0.0
        self.numSqrtVara = 0.0
        self.numSqrdVara = 0.0
        self.numRtu = 0.0
        self.numSqrtRtu = 0.0
        self.numSqrdRtu = 0.0
        self.numMasa = 0.0
        self.numSqrtMasa = 0.0
        self.numSqrdMasa = 0.0
        self.numPaksa = 0.0
        self.numSqrtPaksa = 0.0
        self.numSqrdPaksa = 0.0
        self.numSama = 0.0
        self.numSqrtSama = 0.0
        self.numSqrdSama = 0.0
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(self.endPointF)

        # Transform object applied to the text item.
        self.textTransform = QTransform()
        
        # Set the text item with the properties we want it to have.
        self.reApplyTextItemAttributes(self.textItem)
        
        # Flag that indicates that vertical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def reApplyTextItemAttributes(self, textItem):
        """Takes the given text item and reapplies the pen, brush,
        transform, etc. that should be set for the text item.
        """

        # Set properties of the text item.
        
        # Set the font of the text.
        textItem.setFont(self.timeMeasurementTextFont)
        
        # Set the pen color of the text.
        self.timeMeasurementTextPen = textItem.pen()
        self.timeMeasurementTextPen.\
            setColor(self.timeMeasurementGraphicsItemTextColor)
            
        textItem.setPen(self.timeMeasurementTextPen)

        # Set the brush color of the text.
        self.timeMeasurementTextBrush = textItem.brush()
        self.timeMeasurementTextBrush.\
            setColor(self.timeMeasurementGraphicsItemTextColor)
            
        textItem.setBrush(self.timeMeasurementTextBrush)

        # Apply some size scaling to the text.
        self.textTransform = QTransform()
        self.textTransform.scale(self.timeMeasurementTextXScaling, \
                            self.timeMeasurementTextYScaling)
        textItem.setTransform(self.textTransform)

        
    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextYScaling 

        # Font.
        self.timeMeasurementTextFont = QFont()
        self.timeMeasurementTextFont.fromString(\
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeMeasurementGraphicsItemTextColor = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeMeasurementGraphicsItemColor = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultColor

        # TimeMeasurementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtBarsTextFlag (bool).
        self.showSqrtBarsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdBarsTextFlag (bool).
        self.showSqrdBarsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdBarsTextFlag
    
        # TimeMeasurementGraphicsItem showHoursTextFlag (bool).
        self.showHoursTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtHoursTextFlag (bool).
        self.showSqrtHoursTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdHoursTextFlag (bool).
        self.showSqrdHoursTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdHoursTextFlag
    
        # TimeMeasurementGraphicsItem showDaysTextFlag (bool).
        self.showDaysTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtDaysTextFlag (bool).
        self.showSqrtDaysTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdDaysTextFlag (bool).
        self.showSqrdDaysTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdDaysTextFlag
    
        # TimeMeasurementGraphicsItem showWeeksTextFlag (bool).
        self.showWeeksTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.showSqrtWeeksTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdWeeksTextFlag (bool).
        self.showSqrdWeeksTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showMonthsTextFlag (bool).
        self.showMonthsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowMonthsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.showSqrtMonthsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtMonthsTextFlag

        # TimeMeasurementGraphicsItem showSqrdMonthsTextFlag (bool).
        self.showSqrdMonthsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdMonthsTextFlag

        # TimeMeasurementGraphicsItem showTimeRangeTextFlag (bool).
        self.showTimeRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtTimeRangeTextFlag (bool).
        self.showSqrtTimeRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdTimeRangeTextFlag (bool).
        self.showSqrdTimeRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.showScaledValueRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.showSqrtScaledValueRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdScaledValueRangeTextFlag (bool).
        self.showSqrdScaledValueRangeTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showAyanaTextFlag (bool).
        self.showAyanaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrtAyanaTextFlag (bool).
        self.showSqrtAyanaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrdAyanaTextFlag (bool).
        self.showSqrdAyanaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdAyanaTextFlag

        # TimeMeasurementGraphicsItem showMuhurtaTextFlag (bool).
        self.showMuhurtaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showSqrtMuhurtaTextFlag (bool).
        self.showSqrtMuhurtaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showSqrdMuhurtaTextFlag (bool).
        self.showSqrdMuhurtaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag

        # TimeMeasurementGraphicsItem showVaraTextFlag (bool).
        self.showVaraTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowVaraTextFlag

        # TimeMeasurementGraphicsItem showSqrtVaraTextFlag (bool).
        self.showSqrtVaraTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtVaraTextFlag

        # TimeMeasurementGraphicsItem showSqrdVaraTextFlag (bool).
        self.showSqrdVaraTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdVaraTextFlag

        # TimeMeasurementGraphicsItem showRtuTextFlag (bool).
        self.showRtuTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowRtuTextFlag

        # TimeMeasurementGraphicsItem showSqrtRtuTextFlag (bool).
        self.showSqrtRtuTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtRtuTextFlag

        # TimeMeasurementGraphicsItem showSqrdRtuTextFlag (bool).
        self.showSqrdRtuTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdRtuTextFlag

        # TimeMeasurementGraphicsItem showMasaTextFlag (bool).
        self.showMasaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowMasaTextFlag

        # TimeMeasurementGraphicsItem showSqrtMasaTextFlag (bool).
        self.showSqrtMasaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtMasaTextFlag

        # TimeMeasurementGraphicsItem showSqrdMasaTextFlag (bool).
        self.showSqrdMasaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdMasaTextFlag

        # TimeMeasurementGraphicsItem showPaksaTextFlag (bool).
        self.showPaksaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowPaksaTextFlag

        # TimeMeasurementGraphicsItem showSqrtPaksaTextFlag (bool).
        self.showSqrtPaksaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtPaksaTextFlag

        # TimeMeasurementGraphicsItem showSqrdPaksaTextFlag (bool).
        self.showSqrdPaksaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdPaksaTextFlag

        # TimeMeasurementGraphicsItem showSamaTextFlag (bool).
        self.showSamaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSamaTextFlag

        # TimeMeasurementGraphicsItem showSqrtSamaTextFlag (bool).
        self.showSqrtSamaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtSamaTextFlag

        # TimeMeasurementGraphicsItem showSqrdSamaTextFlag (bool).
        self.showSqrdSamaTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrdSamaTextFlag

        ####################################################################

        # Update the text item with the new settings.
        self.reApplyTextItemAttributes(self.textItem)

        # Update the time measurement calculations since scaling could
        # have changed.
        self.recalculateTimeMeasurement()
        
        # Update the timeMeasurement text item position.
        self._updateTextItemPositions()
        
        # Set the new color of the pen for drawing the bar.
        self.timeMeasurementPen.\
            setColor(self.timeMeasurementGraphicsItemColor)
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculateTimeMeasurement()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointX <= scenePosX <= startThreshold or \
                   startingPointX >= scenePosX >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointX <= scenePosX <= endThreshold or \
                   endingPointX >= scenePosX >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)
            
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the timeMeasurement label position.
        
        # Changes in x and y.
        deltaX = self.endPointF.x() - self.startPointF.x()
        deltaY = self.endPointF.y() - self.startPointF.y()
        
        # Get bounding rectangle of text item.
        boundingRect = self.textItem.boundingRect()

        # Find largest text height and width.
        largestTextHeight = boundingRect.height()
        largestTextWidth = boundingRect.width()

        # Now replace the above with the scaled version of it. 
        largestTextHeight = largestTextHeight * self.textTransform.m22()
        largestTextWidth = largestTextWidth * self.textTransform.m11()

        self.log.debug("largestTextHeight = {}".format(largestTextHeight))
        self.log.debug("largestTextWidth = {}".format(largestTextWidth))
        
        # Get the x and y of the point to place the text, referenced
        # on the line from start point to end point, but offset by a
        # certain amount such that the largest text would be centered
        # on the line.
        midX = self.mapFromScene(\
            QPointF(self.startPointF.x() + (deltaX * 0.5), 0.0)).x()
        midY = self.mapFromScene(\
            QPointF(0.0, self.startPointF.y() + (deltaY * 0.5))).y()

        self.log.debug("midX={}, midY={}".format(midX, midY))
                       
        startX = midX
        startY = midY

        # Amount to mutiply to get a largest offset from startY.
        offsetY = largestTextHeight
        offsetX = (largestTextWidth / 2.0)
        
        x = startX - offsetX
        y = startY - offsetY
        
        self.textItem.setPos(QPointF(x, y))
                    
    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timemeasurement.
                self.recalculateTimeMeasurement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.startPointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timemeasurement.
                self.recalculateTimeMeasurement()
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            self.log.debug("Normalization of TimeMeasurementGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            self.recalculateTimeMeasurement()
            
            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
            super().setPos(self.startPointF)
            

    def recalculateTimeMeasurement(self):
        """Sets the internal variables:
        
        self.numPriceBars
        self.numSqrtPriceBars
        self.numSqrdPriceBars
        self.numHours
        self.numSqrtHours
        self.numSqrdHours
        self.numDays
        self.numSqrtDays
        self.numSqrdDays
        self.numWeeks
        self.numSqrtWeeks
        self.numSqrdWeeks
        self.numMonths
        self.numSqrtMonths
        self.numSqrdMonths
        self.numTimeRange
        self.numSqrtTimeRange
        self.numSqrdTimeRange
        self.numScaledValueRange
        self.numSqrtScaledValueRange
        self.numSqrdScaledValueRange
        self.numAyana
        self.numSqrtAyana
        self.numSqrdAyana
        self.numMuhurta
        self.numSqrtMuhurta
        self.numSqrdMuhurta
        self.numVara
        self.numSqrtVara
        self.numSqrdVara
        self.numRtu
        self.numSqrtRtu
        self.numSqrdRtu
        self.numMasa
        self.numSqrtMasa
        self.numSqrdMasa
        self.numPaksa
        self.numSqrtPaksa
        self.numSqrdPaksa
        self.numSama
        self.numSqrtSama
        self.numSqrdSama
            
        to hold the amount of time between the start and end points.
        """

        scene = self.scene()

        # Reset the values.
        self.numPriceBars = 0.0
        self.numSqrtPriceBars = 0.0
        self.numSqrdPriceBars = 0.0
        self.numHours = 0.0
        self.numSqrtHours = 0.0
        self.numSqrdHours = 0.0
        self.numDays = 0.0
        self.numSqrtDays = 0.0
        self.numSqrdDays = 0.0
        self.numWeeks = 0.0
        self.numSqrtWeeks = 0.0
        self.numSqrdWeeks = 0.0
        self.numMonths = 0.0
        self.numSqrtMonths = 0.0
        self.numSqrdMonths = 0.0
        self.numTimeRange = 0.0
        self.numSqrtTimeRange = 0.0
        self.numSqrdTimeRange = 0.0
        self.numScaledValueRange = 0.0
        self.numSqrtScaledValueRange = 0.0
        self.numSqrdScaledValueRange = 0.0
        self.numAyana = 0.0
        self.numSqrtAyana = 0.0
        self.numSqrdAyana = 0.0
        self.numMuhurta = 0.0
        self.numSqrtMuhurta = 0.0
        self.numSqrdMuhurta = 0.0
        self.numVara = 0.0
        self.numSqrtVara = 0.0
        self.numSqrdVara = 0.0
        self.numRtu = 0.0
        self.numSqrtRtu = 0.0
        self.numSqrdRtu = 0.0
        self.numMasa = 0.0
        self.numSqrtMasa = 0.0
        self.numSqrdMasa = 0.0
        self.numPaksa = 0.0
        self.numSqrtPaksa = 0.0
        self.numSqrdPaksa = 0.0
        self.numSama = 0.0
        self.numSqrtSama = 0.0
        self.numSqrdSama = 0.0
        
        if scene != None:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

            # Go through the PriceBarGraphicsItems and count the bars in
            # between self.startPointF and self.endPointF.
            for item in graphicsItems:
                if isinstance(item, PriceBarGraphicsItem):

                    x = item.getPriceBarHighScenePoint().x()

                    # Here we check for the bar being in between
                    # the self.startPointF and the self.endPointF.
                    # This handles the case when the start and end
                    # points are reversed also.
                    if (self.startPointF.x() < x <= self.endPointF.x()) or \
                       (self.endPointF.x() < x <= self.startPointF.x()):

                        self.numPriceBars += 1
        
            # Calculate the number of (calendar) days.
            startTimestamp = \
                scene.sceneXPosToDatetime(self.startPointF.x())
            
            timestampStr = Ephemeris.datetimeToDayStr(startTimestamp)
            self.log.debug("startTimestamp: " + timestampStr)
            
            endTimestamp = \
                scene.sceneXPosToDatetime(self.endPointF.x())
            
            timestampStr = Ephemeris.datetimeToDayStr(endTimestamp)
            self.log.debug("endTimestamp: " + timestampStr)
            
            timeDelta = endTimestamp - startTimestamp
            
            self.log.debug("timeDelta is: " + timeDelta.__str__())

            # Calculate number of days.
            self.numDays = timeDelta.days
            self.numDays += (timeDelta.seconds / 86400.0)

            # Calculate number of hours.
            self.numHours = self.numDays * 24.0
            
            # Calculate number of weeks.
            self.numWeeks = self.numDays / 7.0

            # Calculate number of months.
            daysInTropicalYear = 365.242199
            daysInMonth = daysInTropicalYear / 12.0
            self.numMonths = self.numDays / daysInMonth

            # Calculate the time range.  (In what units should we do
            # this?... for now we will just use the default.)
            self.numTimeRange = abs(self.endPointF.x() - self.startPointF.x())
            
            # Calculate the scaled value range.
            self.numScaledValueRange = \
                abs(scene.convertDatetimeToScaledValue(endTimestamp) -
                    scene.convertDatetimeToScaledValue(startTimestamp))

            # Calculate number of ayanas (6 months).
            # Ayana is half of a tropical year (solstice to solstice).
            daysInAyana = daysInTropicalYear / 2.0
            self.numAyana = self.numDays / daysInAyana

            # Calculate number of muhurtas (48 minutes).
            minutesInDay = 1440
            self.numMuhurta = (self.numDays * minutesInDay) / 48.0

            # Calculate number of varas (24-hour day).
            self.numVara = float(self.numDays)

            # Calculate number of rtu (season of 2 months).  Although
            # some authors say this is relative to sidereal zodiac, I
            # believe it's supposed to be relative to divisions of a
            # tropical year, so I will use that below.
            daysInRtu = daysInTropicalYear / 6.0
            self.numRtu = self.numDays / daysInRtu

            # Calculate number of masa (lunar synodic months).
            daysInLunarSynodicMonth = 29.530588853
            self.numMasa = self.numDays / daysInLunarSynodicMonth
            
            # Calculate number of paksa (fortnights).
            daysInPaksa = daysInLunarSynodicMonth / 2.0
            self.numPaksa = self.numDays / daysInPaksa

            # Calculate number of sama (solar year).
            self.numSama = self.numDays / daysInTropicalYear
            
            self.log.debug("self.numPriceBars={}".format(self.numPriceBars))
            self.log.debug("self.numHours={}".format(self.numHours))
            self.log.debug("self.numDays={}".format(self.numDays))
            self.log.debug("self.numWeeks={}".format(self.numWeeks))
            self.log.debug("self.numMonths={}".format(self.numMonths))
            self.log.debug("self.numTimeRange={}".format(self.numTimeRange))
            self.log.debug("self.numScaledValueRange={}".
                           format(self.numScaledValueRange))
            self.log.debug("self.numAyana={}".format(self.numAyana))
            self.log.debug("self.numMuhurta={}".format(self.numMuhurta))
            self.log.debug("self.numVara={}".format(self.numVara))
            self.log.debug("self.numRtu={}".format(self.numRtu))
            self.log.debug("self.numMasa={}".format(self.numMasa))
            self.log.debug("self.numPaksa={}".format(self.numPaksa))
            self.log.debug("self.numSama={}".format(self.numSama))

            self.numSqrtPriceBars = math.sqrt(abs(self.numPriceBars))
            self.numSqrtHours = math.sqrt(abs(self.numHours))
            self.numSqrtDays = math.sqrt(abs(self.numDays))
            self.numSqrtWeeks = math.sqrt(abs(self.numWeeks))
            self.numSqrtMonths = math.sqrt(abs(self.numMonths))
            self.numSqrtTimeRange = math.sqrt(abs(self.numTimeRange))
            self.numSqrtScaledValueRange = \
                math.sqrt(abs(self.numScaledValueRange))
            self.numSqrtAyana = math.sqrt(abs(self.numAyana))
            self.numSqrtMuhurta = math.sqrt(abs(self.numMuhurta))
            self.numSqrtVara = math.sqrt(abs(self.numVara))
            self.numSqrtRtu = math.sqrt(abs(self.numRtu))
            self.numSqrtMasa = math.sqrt(abs(self.numMasa))
            self.numSqrtPaksa = math.sqrt(abs(self.numPaksa))
            self.numSqrtSama = math.sqrt(abs(self.numSama))

            self.log.debug("self.numSqrtPriceBars={}".\
                           format(self.numSqrtPriceBars))
            self.log.debug("self.numSqrtHours={}".format(self.numSqrtHours))
            self.log.debug("self.numSqrtDays={}".format(self.numSqrtDays))
            self.log.debug("self.numSqrtWeeks={}".format(self.numSqrtWeeks))
            self.log.debug("self.numSqrtMonths={}".format(self.numSqrtMonths))
            self.log.debug("self.numSqrtTimeRange={}".\
                format(self.numSqrtTimeRange))
            self.log.debug("self.numSqrtScaledValueRange={}".\
                format(self.numSqrtScaledValueRange))
            self.log.debug("self.numSqrtAyana={}".format(self.numSqrtAyana))
            self.log.debug("self.numSqrtMuhurta={}".format(self.numSqrtMuhurta))
            self.log.debug("self.numSqrtVara={}".format(self.numSqrtVara))
            self.log.debug("self.numSqrtRtu={}".format(self.numSqrtRtu))
            self.log.debug("self.numSqrtMasa={}".format(self.numSqrtMasa))
            self.log.debug("self.numSqrtPaksa={}".format(self.numSqrtPaksa))
            self.log.debug("self.numSqrtSama={}".format(self.numSqrtSama))

            self.numSqrdPriceBars = math.pow(self.numPriceBars, 2.0)
            self.numSqrdHours = math.pow(self.numHours, 2.0)
            self.numSqrdDays = math.pow(self.numDays, 2.0)
            self.numSqrdWeeks = math.pow(self.numWeeks, 2.0)
            self.numSqrdMonths = math.pow(self.numMonths, 2.0)
            self.numSqrdTimeRange = math.pow(self.numTimeRange, 2.0)
            self.numSqrdScaledValueRange = \
                math.pow(self.numScaledValueRange, 2.0)
            self.numSqrdAyana = math.pow(self.numAyana, 2.0)
            self.numSqrdMuhurta = math.pow(self.numMuhurta, 2.0)
            self.numSqrdVara = math.pow(self.numVara, 2.0)
            self.numSqrdRtu = math.pow(self.numRtu, 2.0)
            self.numSqrdMasa = math.pow(self.numMasa, 2.0)
            self.numSqrdPaksa = math.pow(self.numPaksa, 2.0)
            self.numSqrdSama = math.pow(self.numSama, 2.0)
            
            self.log.debug("self.numSqrdPriceBars={}".\
                           format(self.numSqrdPriceBars))
            self.log.debug("self.numSqrdHours={}".format(self.numSqrdHours))
            self.log.debug("self.numSqrdDays={}".format(self.numSqrdDays))
            self.log.debug("self.numSqrdWeeks={}".format(self.numSqrdWeeks))
            self.log.debug("self.numSqrdMonths={}".format(self.numSqrdMonths))
            self.log.debug("self.numSqrdTimeRange={}".\
                format(self.numSqrdTimeRange))
            self.log.debug("self.numSqrdScaledValueRange={}".\
                format(self.numSqrdScaledValueRange))
            self.log.debug("self.numSqrdAyana={}".format(self.numSqrdAyana))
            self.log.debug("self.numSqrdMuhurta={}".format(self.numSqrdMuhurta))
            self.log.debug("self.numSqrdVara={}".format(self.numSqrdVara))
            self.log.debug("self.numSqrdRtu={}".format(self.numSqrdRtu))
            self.log.debug("self.numSqrdMasa={}".format(self.numSqrdMasa))
            self.log.debug("self.numSqrdPaksa={}".format(self.numSqrdPaksa))
            self.log.debug("self.numSqrdSama={}".format(self.numSqrdSama))

        # Update the text of the internal items.
        barsText = "{} B".format(self.numPriceBars)
        sqrtBarsText = "{:.2f} sqrt B".format(self.numSqrtPriceBars)
        sqrdBarsText = "{:.2f} sqrd B".format(self.numSqrdPriceBars)
        hoursText = "{:.2f} H".format(self.numHours)
        sqrtHoursText = "{:.2f} sqrt H".format(self.numSqrtHours)
        sqrdHoursText = "{:.2f} sqrd H".format(self.numSqrdHours)
        daysText = "{:.2f} CD".format(self.numDays)
        sqrtDaysText = "{:.2f} sqrt CD".format(self.numSqrtDays)
        sqrdDaysText = "{:.2f} sqrd CD".format(self.numSqrdDays)
        weeksText = "{:.2f} W".format(self.numWeeks)
        sqrtWeeksText = "{:.2f} sqrt W".format(self.numSqrtWeeks)
        sqrdWeeksText = "{:.2f} sqrd W".format(self.numSqrdWeeks)
        monthsText = "{:.2f} M".format(self.numMonths)
        sqrtMonthsText = "{:.2f} sqrt M".format(self.numSqrtMonths)
        sqrdMonthsText = "{:.2f} sqrd M".format(self.numSqrdMonths)
        timeRangeText = \
            "{:.4f} t_range".format(self.numTimeRange)
        sqrtTimeRangeText = \
            "{:.4f} sqrt(t_range)".format(self.numSqrtTimeRange)
        sqrdTimeRangeText = \
            "{:.4f} sqrd(t_range)".format(self.numSqrdTimeRange)
        scaledValueRangeText = \
            "{:.4f} u_range".format(self.numScaledValueRange)
        sqrtScaledValueRangeText = \
            "{:.4f} sqrt(u_range)".format(self.numSqrtScaledValueRange)
        sqrdScaledValueRangeText = \
            "{:.4f} sqrd(u_range)".format(self.numSqrdScaledValueRange)
        ayanaText = "{} ayana".format(self.numAyana)
        sqrtAyanaText = "{} sqrt ayana".format(self.numSqrtAyana)
        sqrdAyanaText = "{} sqrd ayana".format(self.numSqrdAyana)
        muhurtaText = "{} muhurta".format(self.numMuhurta)
        sqrtMuhurtaText = "{} sqrt muhurta".format(self.numSqrtMuhurta)
        sqrdMuhurtaText = "{} sqrd muhurta".format(self.numSqrdMuhurta)
        varaText = "{} vara".format(self.numVara)
        sqrtVaraText = "{} sqrt vara".format(self.numSqrtVara)
        sqrdVaraText = "{} sqrd vara".format(self.numSqrdVara)
        rtuText = "{} rtu".format(self.numRtu)
        sqrtRtuText = "{} sqrt rtu".format(self.numSqrtRtu)
        sqrdRtuText = "{} sqrd rtu".format(self.numSqrdRtu)
        masaText = "{} masa".format(self.numMasa)
        sqrtMasaText = "{} sqrt masa".format(self.numSqrtMasa)
        sqrdMasaText = "{} sqrd masa".format(self.numSqrdMasa)
        paksaText = "{} paksa".format(self.numPaksa)
        sqrtPaksaText = "{} sqrt paksa".format(self.numSqrtPaksa)
        sqrdPaksaText = "{} sqrd paksa".format(self.numSqrdPaksa)
        samaText = "{} sama".format(self.numSama)
        sqrtSamaText = "{} sqrt sama".format(self.numSqrtSama)
        sqrdSamaText = "{} sqrd sama".format(self.numSqrdSama)

        # Text to set in the text item.
        text = ""

        if self.showBarsTextFlag == True:
            text += barsText + os.linesep
        if self.showSqrtBarsTextFlag == True:
            text += sqrtBarsText + os.linesep
        if self.showSqrdBarsTextFlag == True:
            text += sqrdBarsText + os.linesep
        if self.showHoursTextFlag == True:
            text += hoursText + os.linesep
        if self.showSqrtHoursTextFlag == True:
            text += sqrtHoursText + os.linesep
        if self.showSqrdHoursTextFlag == True:
            text += sqrdHoursText + os.linesep
        if self.showDaysTextFlag == True:
            text += daysText + os.linesep
        if self.showSqrtDaysTextFlag == True:
            text += sqrtDaysText + os.linesep
        if self.showSqrdDaysTextFlag == True:
            text += sqrdDaysText + os.linesep
        if self.showWeeksTextFlag == True:
            text += weeksText + os.linesep
        if self.showSqrtWeeksTextFlag == True:
            text += sqrtWeeksText + os.linesep
        if self.showSqrdWeeksTextFlag == True:
            text += sqrdWeeksText + os.linesep
        if self.showMonthsTextFlag == True:
            text += monthsText + os.linesep
        if self.showSqrtMonthsTextFlag == True:
            text += sqrtMonthsText + os.linesep
        if self.showSqrdMonthsTextFlag == True:
            text += sqrdMonthsText + os.linesep
        if self.showTimeRangeTextFlag == True:
            text += timeRangeText + os.linesep
        if self.showSqrtTimeRangeTextFlag == True:
            text += sqrtTimeRangeText + os.linesep
        if self.showSqrdTimeRangeTextFlag == True:
            text += sqrdTimeRangeText + os.linesep
        if self.showScaledValueRangeTextFlag == True:
            text += scaledValueRangeText + os.linesep
        if self.showSqrtScaledValueRangeTextFlag == True:
            text += sqrtScaledValueRangeText + os.linesep
        if self.showSqrdScaledValueRangeTextFlag == True:
            text += sqrdScaledValueRangeText + os.linesep
        if self.showAyanaTextFlag == True:
            text += ayanaText + os.linesep
        if self.showSqrtAyanaTextFlag == True:
            text += sqrtAyanaText + os.linesep
        if self.showSqrdAyanaTextFlag == True:
            text += sqrdAyanaText + os.linesep
        if self.showMuhurtaTextFlag == True:
            text += muhurtaText + os.linesep
        if self.showSqrtMuhurtaTextFlag == True:
            text += sqrtMuhurtaText + os.linesep
        if self.showSqrdMuhurtaTextFlag == True:
            text += sqrdMuhurtaText + os.linesep
        if self.showVaraTextFlag == True:
            text += varaText + os.linesep
        if self.showSqrtVaraTextFlag == True:
            text += sqrtVaraText + os.linesep
        if self.showSqrdVaraTextFlag == True:
            text += sqrdVaraText + os.linesep
        if self.showRtuTextFlag == True:
            text += rtuText + os.linesep
        if self.showSqrtRtuTextFlag == True:
            text += sqrtRtuText + os.linesep
        if self.showSqrdRtuTextFlag == True:
            text += sqrdRtuText + os.linesep
        if self.showMasaTextFlag == True:
            text += masaText + os.linesep
        if self.showSqrtMasaTextFlag == True:
            text += sqrtMasaText + os.linesep
        if self.showSqrdMasaTextFlag == True:
            text += sqrdMasaText + os.linesep
        if self.showPaksaTextFlag == True:
            text += paksaText + os.linesep
        if self.showSqrtPaksaTextFlag == True:
            text += sqrtPaksaText + os.linesep
        if self.showSqrdPaksaTextFlag == True:
            text += sqrdPaksaText + os.linesep
        if self.showSamaTextFlag == True:
            text += samaText + os.linesep
        if self.showSqrtSamaTextFlag == True:
            text += sqrtSamaText + os.linesep
        if self.showSqrdSamaTextFlag == True:
            text += sqrdSamaText + os.linesep

        text = text.rstrip()
        self.textItem.setText(text)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTimeMeasurementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartTimeMeasurementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartTimeMeasurementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartTimeMeasurementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.timeMeasurementTextXScaling = self.artifact.getTextXScaling()
        self.timeMeasurementTextYScaling = self.artifact.getTextYScaling()
        self.timeMeasurementTextFont = self.artifact.getFont()
        self.timeMeasurementGraphicsItemTextColor = self.artifact.getTextColor()
        self.timeMeasurementPen.setColor(self.artifact.getColor())
        
        self.showBarsTextFlag = self.artifact.getShowBarsTextFlag()
        self.showSqrtBarsTextFlag = self.artifact.getShowSqrtBarsTextFlag()
        self.showSqrdBarsTextFlag = self.artifact.getShowSqrdBarsTextFlag()
        self.showHoursTextFlag = self.artifact.getShowHoursTextFlag()
        self.showSqrtHoursTextFlag = self.artifact.getShowSqrtHoursTextFlag()
        self.showSqrdHoursTextFlag = self.artifact.getShowSqrdHoursTextFlag()
        self.showDaysTextFlag = self.artifact.getShowDaysTextFlag()
        self.showSqrtDaysTextFlag = self.artifact.getShowSqrtDaysTextFlag()
        self.showSqrdDaysTextFlag = self.artifact.getShowSqrdDaysTextFlag()
        self.showWeeksTextFlag = self.artifact.getShowWeeksTextFlag()
        self.showSqrtWeeksTextFlag = self.artifact.getShowSqrtWeeksTextFlag()
        self.showSqrdWeeksTextFlag = self.artifact.getShowSqrdWeeksTextFlag()
        self.showMonthsTextFlag = self.artifact.getShowMonthsTextFlag()
        self.showSqrtMonthsTextFlag = self.artifact.getShowSqrtMonthsTextFlag()
        self.showSqrdMonthsTextFlag = self.artifact.getShowSqrdMonthsTextFlag()
        self.showTimeRangeTextFlag = \
            self.artifact.getShowTimeRangeTextFlag()
        self.showSqrtTimeRangeTextFlag = \
            self.artifact.getShowSqrtTimeRangeTextFlag()
        self.showSqrdTimeRangeTextFlag = \
            self.artifact.getShowSqrdTimeRangeTextFlag()
        self.showScaledValueRangeTextFlag = \
            self.artifact.getShowScaledValueRangeTextFlag()
        self.showSqrtScaledValueRangeTextFlag = \
            self.artifact.getShowSqrtScaledValueRangeTextFlag()
        self.showSqrdScaledValueRangeTextFlag = \
            self.artifact.getShowSqrdScaledValueRangeTextFlag()
        self.showAyanaTextFlag = \
            self.artifact.getShowAyanaTextFlag()
        self.showSqrtAyanaTextFlag = \
            self.artifact.getShowSqrtAyanaTextFlag()
        self.showSqrdAyanaTextFlag = \
            self.artifact.getShowSqrdAyanaTextFlag()
        self.showMuhurtaTextFlag = \
            self.artifact.getShowMuhurtaTextFlag()
        self.showSqrtMuhurtaTextFlag = \
            self.artifact.getShowSqrtMuhurtaTextFlag()
        self.showSqrdMuhurtaTextFlag = \
            self.artifact.getShowSqrdMuhurtaTextFlag()
        self.showVaraTextFlag = \
            self.artifact.getShowVaraTextFlag()
        self.showSqrtVaraTextFlag = \
            self.artifact.getShowSqrtVaraTextFlag()
        self.showSqrdVaraTextFlag = \
            self.artifact.getShowSqrdVaraTextFlag()
        self.showRtuTextFlag = \
            self.artifact.getShowRtuTextFlag()
        self.showSqrtRtuTextFlag = \
            self.artifact.getShowSqrtRtuTextFlag()
        self.showSqrdRtuTextFlag = \
            self.artifact.getShowSqrdRtuTextFlag()
        self.showMasaTextFlag = \
            self.artifact.getShowMasaTextFlag()
        self.showSqrtMasaTextFlag = \
            self.artifact.getShowSqrtMasaTextFlag()
        self.showSqrdMasaTextFlag = \
            self.artifact.getShowSqrdMasaTextFlag()
        self.showPaksaTextFlag = \
            self.artifact.getShowPaksaTextFlag()
        self.showSqrtPaksaTextFlag = \
            self.artifact.getShowSqrtPaksaTextFlag()
        self.showSqrdPaksaTextFlag = \
            self.artifact.getShowSqrdPaksaTextFlag()
        self.showSamaTextFlag = \
            self.artifact.getShowSamaTextFlag()
        self.showSqrtSamaTextFlag = \
            self.artifact.getShowSqrtSamaTextFlag()
        self.showSqrdSamaTextFlag = \
            self.artifact.getShowSqrdSamaTextFlag()

        #############

        # Update all the text item with the new settings.
        self.reApplyTextItemAttributes(self.textItem)

        # Need to recalculate the time measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the time measurements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateTimeMeasurement()
        
        # Update the timeMeasurement text item position.
        self._updateTextItemPositions()
        
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTimeMeasurementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTimeMeasurementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.timeMeasurementTextXScaling)
        self.artifact.setTextYScaling(self.timeMeasurementTextYScaling)
        self.artifact.setFont(self.timeMeasurementTextFont)
        self.artifact.setTextColor(self.timeMeasurementGraphicsItemTextColor)
        self.artifact.setColor(self.timeMeasurementPen.color())
        
        self.artifact.setShowBarsTextFlag(self.showBarsTextFlag)
        self.artifact.setShowSqrtBarsTextFlag(self.showSqrtBarsTextFlag)
        self.artifact.setShowSqrdBarsTextFlag(self.showSqrdBarsTextFlag)
        self.artifact.setShowHoursTextFlag(self.showHoursTextFlag)
        self.artifact.setShowSqrtHoursTextFlag(self.showSqrtHoursTextFlag)
        self.artifact.setShowSqrdHoursTextFlag(self.showSqrdHoursTextFlag)
        self.artifact.setShowDaysTextFlag(self.showDaysTextFlag)
        self.artifact.setShowSqrtDaysTextFlag(self.showSqrtDaysTextFlag)
        self.artifact.setShowSqrdDaysTextFlag(self.showSqrdDaysTextFlag)
        self.artifact.setShowWeeksTextFlag(self.showWeeksTextFlag)
        self.artifact.setShowSqrtWeeksTextFlag(self.showSqrtWeeksTextFlag)
        self.artifact.setShowSqrdWeeksTextFlag(self.showSqrdWeeksTextFlag)
        self.artifact.setShowMonthsTextFlag(self.showMonthsTextFlag)
        self.artifact.setShowSqrtMonthsTextFlag(self.showSqrtMonthsTextFlag)
        self.artifact.setShowSqrdMonthsTextFlag(self.showSqrdMonthsTextFlag)
        self.artifact.setShowTimeRangeTextFlag(\
            self.showTimeRangeTextFlag)
        self.artifact.setShowSqrtTimeRangeTextFlag(\
            self.showSqrtTimeRangeTextFlag)
        self.artifact.setShowSqrdTimeRangeTextFlag(\
            self.showSqrdTimeRangeTextFlag)
        self.artifact.setShowScaledValueRangeTextFlag(\
            self.showScaledValueRangeTextFlag)
        self.artifact.setShowSqrtScaledValueRangeTextFlag(\
            self.showSqrtScaledValueRangeTextFlag)
        self.artifact.setShowSqrdScaledValueRangeTextFlag(\
            self.showSqrdScaledValueRangeTextFlag)
        self.artifact.setShowAyanaTextFlag(self.showAyanaTextFlag)
        self.artifact.setShowSqrtAyanaTextFlag(self.showSqrtAyanaTextFlag)
        self.artifact.setShowSqrdAyanaTextFlag(self.showSqrdAyanaTextFlag)
        self.artifact.setShowMuhurtaTextFlag(self.showMuhurtaTextFlag)
        self.artifact.setShowSqrtMuhurtaTextFlag(self.showSqrtMuhurtaTextFlag)
        self.artifact.setShowSqrdMuhurtaTextFlag(self.showSqrdMuhurtaTextFlag)
        self.artifact.setShowVaraTextFlag(self.showVaraTextFlag)
        self.artifact.setShowSqrtVaraTextFlag(self.showSqrtVaraTextFlag)
        self.artifact.setShowSqrdVaraTextFlag(self.showSqrdVaraTextFlag)
        self.artifact.setShowRtuTextFlag(self.showRtuTextFlag)
        self.artifact.setShowSqrtRtuTextFlag(self.showSqrtRtuTextFlag)
        self.artifact.setShowSqrdRtuTextFlag(self.showSqrdRtuTextFlag)
        self.artifact.setShowMasaTextFlag(self.showMasaTextFlag)
        self.artifact.setShowSqrtMasaTextFlag(self.showSqrtMasaTextFlag)
        self.artifact.setShowSqrdMasaTextFlag(self.showSqrdMasaTextFlag)
        self.artifact.setShowPaksaTextFlag(self.showPaksaTextFlag)
        self.artifact.setShowSqrtPaksaTextFlag(self.showSqrtPaksaTextFlag)
        self.artifact.setShowSqrdPaksaTextFlag(self.showSqrdPaksaTextFlag)
        self.artifact.setShowSamaTextFlag(self.showSamaTextFlag)
        self.artifact.setShowSqrtSamaTextFlag(self.showSqrtSamaTextFlag)
        self.artifact.setShowSqrdSamaTextFlag(self.showSqrdSamaTextFlag)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.

        # The QRectF returned is relative to this (0, 0) point.

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()

        topLeft = \
            QPointF(0.0, -1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight * 0.5))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight * 0.5))

        # Initalize to the above boundaries.  We will set them below.
        localHighY = topLeft.y()
        localLowY = bottomRight.y()
        if self.drawVerticalDottedLinesFlag or self.isSelected():
            # Get the highest high, and lowest low PriceBar in local
            # coordinates.
            highestPrice = self.scene().getHighestPriceBar().high
            highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
            localHighestPriceBarY = \
                       self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

            # Overwrite the high if it is larger.
            if localHighestPriceBarY > localHighY:
                localHighY = localHighestPriceBarY
                
            lowestPrice = self.scene().getLowestPriceBar().low
            lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
            localLowestPriceBarY = \
                      self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
            
            # Overwrite the low if it is smaller.
            if localLowestPriceBarY < localLowY:
                localLowY = localLowestPriceBarY
                
        xValues = []
        xValues.append(topLeft.x())
        xValues.append(bottomRight.x())

        yValues = []
        yValues.append(topLeft.y())
        yValues.append(bottomRight.y())
        yValues.append(localHighY)
        yValues.append(localLowY)

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight * 0.5))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight * 0.5))

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.timeMeasurementPen is set to what we want for the drawing
        style.
        """

        if painter.pen() != self.timeMeasurementPen:
            painter.setPen(self.timeMeasurementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight * 0.5)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each enabled tick area if the
        # flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.timeMeasurementPen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]
        
                # Vertical line at the beginning.
                localPosX = 0.0
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
            
                # Vertical line at the end.
                localPosX = 0.0 + xDelta
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.timeMeasurementPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this TimeMeasurementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        TimeMeasurementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        TimeMeasurementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        TimeMeasurementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        
class VerticalTickGraphicsItem(QGraphicsItem):
    """QGraphicsItem that draws a vertical tick line. """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = logging.getLogger("pricebarchart.VerticalTickGraphicsItem")

        self.barHeight = 0.2
        
        # Pen which is used to do the painting of the bar tick.
        self.pen = QPen()
        self.penWidth = 0.0
        self.pen.setWidthF(self.penWidth)

    def setPen(self, pen):
        """Sets the pen used to draw this QGraphicsItem."""
        
        self.pen = pen
        
    def setPenWidth(self, penWidth):
        """Sets the pen width used to draw this QGraphicsItem.
        Arguments:

        penWidth - float value for the pen width.
        """
        
        self.penWidth = penWidth
        self.pen.setWidthF(self.penWidth)
    
    def setBarHeight(self, barHeight):
        """Sets the bar height of the tick.

        Arguments:
        barHeight - float value for the bar height.
        """

        self.barHeight = barHeight

    def getBarHeight(self):
        """Returns the bar height of the tick."""
        
        return self.barHeight

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        topLeft = QPointF(self.penWidth * -0.5,
                          1.0 * self.barHeight * 0.5)
        
        bottomRight = QPointF(self.penWidth * 0.5,
                              -1.0 * self.barHeight * 0.5)

        return QRectF(topLeft, bottomRight).normalized()

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.pen:
            painter.setPen(QPen(self.pen))
            
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.barHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (self.barHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

               
class HorizontalTickGraphicsItem(QGraphicsItem):
    """QGraphicsItem that draws a horizontal tick line. """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = logging.getLogger("pricebarchart.HorizontalTickGraphicsItem")

        self.barWidth = 1.0
        
        # Pen which is used to do the painting of the bar tick.
        self.pen = QPen()
        self.penWidth = 0.0
        self.pen.setWidthF(self.penWidth)

    def setPen(self, pen):
        """Sets the pen used to draw this QGraphicsItem."""
        
        self.pen = pen
        
    def setPenWidth(self, penWidth):
        """Sets the pen width used to draw this QGraphicsItem.
        Arguments:

        penWidth - float value for the pen width.
        """
        
        self.penWidth = penWidth
        self.pen.setWidthF(self.penWidth)
    
    def setBarWidth(self, barWidth):
        """Sets the bar width of the tick.

        Arguments:
        barWidth - float value for the bar width.
        """

        self.barWidth = barWidth

    def getBarWidth(self):
        """Returns the bar width of the tick."""
        
        return self.barWidth

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        topLeft = QPointF(1.0 * self.barWidth * 0.5,
                          self.penWidth * -0.5)
        
        bottomRight = QPointF(-1.0 * self.barWidth * 0.5,
                              self.penWidth * 0.5)

        return QRectF(topLeft, bottomRight).normalized()

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.pen:
            painter.setPen(QPen(self.pen))
            
        # Draw the left horizontal bar part.
        x1 = 1.0 * (self.barWidth * 0.5)
        y1 = 0.0
        x2 = -1.0 * (self.barWidth * 0.5)
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

               
class TimeModalScaleGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a musical scale in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new TimeModalScaleGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger(\
            "pricebarchart.TimeModalScaleGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.

        # Color of the graphicsitem bar.
        self.timeModalScaleGraphicsItemColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarColor

        # Color of the text that is associated with the graphicsitem.
        self.timeModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextColor

        # X scaling of the text.
        self.timeModalScaleTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeModalScaleTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTimeModalScaleArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.timeModalScalePenWidth = 0.0
        self.timeModalScalePen = QPen()
        self.timeModalScalePen.setColor(self.timeModalScaleGraphicsItemColor)
        self.timeModalScalePen.setWidthF(self.timeModalScalePenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Dummy item.
        self.dummyItem = QGraphicsSimpleTextItem("", self)
        
        # Set the font of the text.
        self.timeModalScaleTextFont = QFont("Sans Serif")
        self.timeModalScaleTextFont.\
            setPointSizeF(self.artifact.getFontSize())

        # Set the pen color of the text.
        self.timeModalScaleTextPen = self.dummyItem.pen()
        self.timeModalScaleTextPen.\
            setColor(self.timeModalScaleGraphicsItemTextColor)

        # Set the brush color of the text.
        self.timeModalScaleTextBrush = self.dummyItem.brush()
        self.timeModalScaleTextBrush.\
            setColor(self.timeModalScaleGraphicsItemTextColor)

        # Degrees of text rotation.
        self.rotationDegrees = 90.0
        
        # Size scaling for the text.
        textTransform = QTransform()
        textTransform.scale(self.timeModalScaleTextXScaling, \
                            self.timeModalScaleTextYScaling)
        textTransform.rotate(self.rotationDegrees)
        
        # Below is a 2-dimensional list of (2
        # QGraphicsSimpleTextItems), for each of the MusicalRatios in
        # the PriceBarChartTimeModalScaleArtifact.  The 2 texts displayed
        # for each MusicalRatio is:
        #
        # 1) Fraction (or float if no numerator and no denominator is set).
        # 2) Timestamp value.
        #
        self.musicalRatioTextItems = []

        # Below is a list of VerticalTickGraphicsItems that correspond
        # to each of the musicalRatios.
        self.verticalTickItems = []
        
        # Initialize to blank and set at the end point.
        for musicalRatio in range(len(self.artifact.getMusicalRatios())):
            verticalTickItem = VerticalTickGraphicsItem(self)
            verticalTickItem.setPos(self.endPointF)
            verticalTickItem.setPen(self.timeModalScalePen)
            
            fractionTextItem = QGraphicsSimpleTextItem("", self)
            fractionTextItem.setPos(self.endPointF)
            fractionTextItem.setFont(self.timeModalScaleTextFont)
            fractionTextItem.setPen(self.timeModalScaleTextPen)
            fractionTextItem.setBrush(self.timeModalScaleTextBrush)
            fractionTextItem.setTransform(textTransform)
            
            timestampTextItem = QGraphicsSimpleTextItem("", self)
            timestampTextItem.setPos(self.endPointF)
            timestampTextItem.setFont(self.timeModalScaleTextFont)
            timestampTextItem.setPen(self.timeModalScaleTextPen)
            timestampTextItem.setBrush(self.timeModalScaleTextBrush)
            timestampTextItem.setTransform(textTransform)
            
            self.musicalRatioTextItems.\
                append([fractionTextItem, timestampTextItem])

            self.verticalTickItems.append(verticalTickItem)

        # Flag that indicates that vertical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag
        
        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        ########
        
        # List of used musical ratios.
        musicalRatios = \
            copy.deepcopy(priceBarChartSettings.\
                          timeModalScaleGraphicsItemMusicalRatios)
        
        # TimeModalScaleGraphicsItem bar color (QColor).
        self.timeModalScaleGraphicsItemColor = \
            priceBarChartSettings.timeModalScaleGraphicsItemBarColor

        # TimeModalScaleGraphicsItem text color (QColor).
        self.timeModalScaleGraphicsItemTextColor = \
            priceBarChartSettings.timeModalScaleGraphicsItemTextColor
        
        # X scaling of the text.
        self.timeModalScaleTextXScaling = \
            priceBarChartSettings.\
                timeModalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeModalScaleTextYScaling = \
            priceBarChartSettings.\
                timeModalScaleGraphicsItemTextYScaling 

        # textEnabledFlag (bool).
        textEnabledFlag = \
            priceBarChartSettings.\
            timeModalScaleGraphicsItemTextEnabledFlag

        ########

        # Set values in the artifact.

        self.artifact.setMusicalRatios(musicalRatios)
        self.artifact.setColor(self.timeModalScaleGraphicsItemColor)
        self.artifact.setTextColor(self.timeModalScaleGraphicsItemTextColor)
        self.artifact.setTextEnabled(textEnabledFlag)

        self.setArtifact(self.artifact)
        
        self.refreshTextItems()
        
        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings read from app preferences.
        pass
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.refreshTextItems()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointX <= scenePosX <= startThreshold or \
                   startingPointX >= scenePosX >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointX <= scenePosX <= endThreshold or \
                   endingPointX >= scenePosX >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()
            
            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def refreshTextItems(self):
        """Sets the positions of the text items for the MusicalRatios,
        and updates the text so that they are current.
        """

        # Update the timeModalScale label text item texts.
        if self.scene() != None:
            self.recalculateTimeModalScale()

            # Traverse the 2-dimensional list and set the position of
            # each of the text items.
            artifact = self.getArtifact()
            for i in range(len(artifact.getMusicalRatios())):
                # Get the MusicalRatio that corresponds to this index.
                musicalRatio = artifact.getMusicalRatios()[i]

                # Here we always set the positions of everything.  If
                # the musicalRatio not enabled, then the corresponding
                # graphics items would have gotten disabled in the
                # self.recalculateTimeModalScale() call above.
                
                # Get the x and y position that will be the new
                # position of the text item.
                (x, y) = artifact.getXYForMusicalRatio(i)

                # Map those x and y to local coordinates.
                pointF = self.mapFromScene(QPointF(x, y))

                # Create the text transform to use.
                textTransform = QTransform()
                textTransform.scale(self.timeModalScaleTextXScaling, \
                                    self.timeModalScaleTextYScaling)
                textTransform.rotate(self.rotationDegrees)
                
                # Get the text items for this point on the scale.
                listOfTextItems = self.musicalRatioTextItems[i]

                # For each text item for that point on the scale,
                # set the position.
                for j in range(len(listOfTextItems)):
                    textItem = listOfTextItems[j]
                    # The position set is not exactly at (x, y),
                    # but instead at an offset slightly below that
                    # point so that multiple texts dont' overlap
                    # each other.
                    offsetX = (textItem.boundingRect().height() * 0.54) * j
                    textItem.setPos(QPointF(pointF.x() - offsetX,
                                            pointF.y()))
                    textItem.setFont(self.timeModalScaleTextFont)
                    textItem.setPen(self.timeModalScaleTextPen)
                    textItem.setBrush(self.timeModalScaleTextBrush)
                    textItem.setTransform(textTransform)
                    
                # Also set the position of the vertical tick line.
                barHeight = artifact.getBarHeight()
                self.verticalTickItems[i].setBarHeight(barHeight)
                self.verticalTickItems[i].setPos(pointF)
                    
            # Call update on this item since positions and child items
            # were updated.
            self.prepareGeometryChange()
            self.update()

    def setStartPointF(self, pointF):
        """Sets the starting point of the timeModalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.startPointF != pointF: 
            self.startPointF = pointF

            self.setPos(self.startPointF)
            
            # Update the timeModalScale label text item positions.
            self.refreshTextItems()            

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the timeModalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.endPointF != pointF:
            self.endPointF = pointF

            self.log.debug("TimeModalScaleGraphicsItem." +
                           "setEndPointF(QPointF({}, {}))".\
                           format(pointF.x(), pointF.y()))
            
            # Update the timeModalScale label text item positions.
            self.refreshTextItems()

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        #if self.startPointF.x() > self.endPointF.x():
        #    self.log.debug("Normalization of TimeModalScaleGraphicsItem " +
        #                   "required.")
        #    
        #    # Swap the points.
        #    temp = self.startPointF
        #    self.startPointF = self.endPointF
        #    self.endPointF = temp
        #
        #    super().setPos(self.startPointF)
        #    
        #    # Update the timeModalScale label text item positions.
        #    self.refreshTextItems()
        pass

    def recalculateTimeModalScale(self):
        """Updates the text items that represent the ticks on the
        modal scale.  These texts will have accurate values for where
        the notes are in terms of price and time.

        In this process, it also sets the internal variables such that
        a call to self.getArtifact().getXYForMusicalRatio(index) can
        be made and a value returned that is accurate.
        """

        scene = self.scene()

        if scene != None:
            artifact = self.getArtifact()
            musicalRatios = artifact.getMusicalRatios()
            for i in range(len(musicalRatios)):
                musicalRatio = musicalRatios[i]

                if musicalRatio.isEnabled():
                    # Enable and make visible.

                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For the text items for that point on the scale,
                    # set the text.  
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]

                        # Make the text visible if it is enabled.
                        textEnabled = artifact.isTextEnabled()
                        textItem.setEnabled(textEnabled)
                        textItem.setVisible(textEnabled)

                        # If text isn't enabled, there's no need to
                        # set the text for it.  Go to the next text item.
                        if textEnabled == False:
                            continue
                    
                        if j == 0:
                            # Fraction text.  This is either the
                            # fraction (if the numerator and
                            # denominator are available), or the float
                            # value for the ratio.
                            
                            numerator = musicalRatio.getNumerator()
                            denominator = musicalRatio.getDenominator()
                            
                            if numerator != None and denominator != None:
                                fractionText = \
                                    "{}/{}".format(numerator, denominator)
                                textItem.setText(fractionText)
                            else:
                                ratio = musicalRatio.getRatio()
                                ratioText = "{}".format(ratio)
                                textItem.setText(ratioText)
                        elif j == 1:
                            # Timestamp text.
                            
                            # Get the x location and then convert to a datetime.
                            (x, y) = artifact.getXYForMusicalRatio(i)
                            timestamp = \
                                self.scene().sceneXPosToDatetime(x)
                            timestampText = \
                                Ephemeris.datetimeToDayStr(timestamp)
                            textItem.setText(timestampText)

                    # Also enable and set the vertical tick line.
                    self.verticalTickItems[i].setVisible(True)
                    self.verticalTickItems[i].setEnabled(True)
                            
                else:
                    # Disable and make not visable.
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For each text item for that point on the scale,
                    # set as disabled and not visible.
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]
                        textItem.setVisible(False)
                        textItem.setEnabled(False)

                    # Also disable the vertical tick line.
                    self.verticalTickItems[i].setVisible(False)
                    self.verticalTickItems[i].setEnabled(False)
                    

                        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTimeModalScaleArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartTimeModalScaleArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartTimeModalScaleArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartTimeModalScaleArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.timeModalScaleTextFont.\
            setPointSizeF(self.artifact.getFontSize())
        self.timeModalScalePen.\
            setColor(self.artifact.getColor())
        self.timeModalScaleTextPen.\
            setColor(self.artifact.getTextColor())
        self.timeModalScaleTextBrush.\
            setColor(self.artifact.getTextColor())

        
        # Need to recalculate the time measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the measurements will be zero.
        self.refreshTextItems()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTimeModalScaleArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        # Update the internal self.priceBarChartTimeModalScaleArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        # Everything else gets modified only by the edit dialog.
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.
        
        # The QRectF returned is relative to this (0, 0) point.
        barHeight = \
            self.getArtifact().getBarHeight()
        
        xTopLeft = 0.0
        yTopLeft = 1.0 * (barHeight * 0.5)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (barHeight * 0.5)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (barHeight * 0.5)) + yDelta
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (barHeight * 0.5)) + yDelta

        # Get the highest high, and lowest low PriceBar in local
        # coordinates.
        highestPrice = self.scene().getHighestPriceBar().high
        highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
        localHighY = \
            self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

        lowestPrice = self.scene().getLowestPriceBar().low
        lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
        localLowY = \
            self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          

        xValues = []
        xValues.append(xTopLeft)
        xValues.append(xBottomLeft)
        xValues.append(xTopRight)
        xValues.append(xBottomRight)

        yValues = []
        yValues.append(yTopLeft)
        yValues.append(yBottomLeft)
        yValues.append(yTopRight)
        yValues.append(yBottomRight)
        yValues.append(localHighY)
        yValues.append(localLowY)
        
        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        barHeight = \
            self.getArtifact().getBarHeight()
        
        # The QRectF returned is relative to this (0, 0) point.

        xTopLeft = 0.0
        yTopLeft = 1.0 * (barHeight * 0.5)
        topLeft = QPointF(xTopLeft, yTopLeft)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (barHeight * 0.5)
        bottomLeft = QPointF(xBottomLeft, yBottomLeft)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (barHeight * 0.5)) + yDelta
        topRight = QPointF(xTopRight, yTopRight)
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (barHeight * 0.5)) + yDelta
        bottomRight = QPointF(xBottomRight, yBottomRight)

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)
        
        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.timeModalScalePen is set to what we want for the drawing
        style.
        """

        self.log.debug("Entered TimeModalScaleGraphicsItem.paint().  " +
                       "pos is: ({}, {})".format(self.pos().x(),
                                                 self.pos().y()))
                       
        if painter.pen() != self.timeModalScalePen:
            painter.setPen(self.timeModalScalePen)

        artifact = self.getArtifact()
        barHeight = artifact.getBarHeight()

        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (barHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (barHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = 0.0 + xDelta
        y1 = (1.0 * (barHeight * 0.5)) + yDelta
        x2 = 0.0 + xDelta
        y2 = (-1.0 * (barHeight * 0.5)) + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each enabled musicalRatio if
        # the flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.timeModalScalePen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]
        
                for verticalTickItem in self.verticalTickItems:
                    if verticalTickItem.isEnabled() and \
                       verticalTickItem.isVisible():
                    
                        localPosX = verticalTickItem.pos().x()

                        startPoint = QPointF(localPosX, largestY)
                        endPoint = QPointF(localPosX, smallestY)
                        
                        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
                
                        painter.setPen(QPen(option.palette.windowText(), 0,
                                            Qt.DashLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)

                # Draw the vertical line for the start point.
                startPoint = QPointF(0.0, largestY)
                endPoint = QPointF(0.0, smallestY)
                
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)

                # Draw the vertical line for the end point.
                startPoint = QPointF(0.0 + xDelta, largestY)
                endPoint = QPointF(0.0 + xDelta, smallestY)
                
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)

        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.timeModalScalePen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this TimeModalScaleGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        TimeModalScaleGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        rotateDownAction = QAction("Rotate Down", parent)
        rotateUpAction = QAction("Rotate Up", parent)
        reverseAction = QAction("Reverse", parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        rotateDownAction.triggered.\
            connect(self._handleRotateDownAction)
        rotateUpAction.triggered.\
            connect(self._handleRotateUpAction)
        reverseAction.triggered.\
            connect(self._handleReverseAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        rotateDownAction.setEnabled(not readOnlyMode)
        rotateUpAction.setEnabled(not readOnlyMode)
        reverseAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addAction(rotateDownAction)
        menu.addAction(rotateUpAction)
        menu.addAction(reverseAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def rotateDown(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        self._handleRotateDownAction()
        
    def rotateUp(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        self._handleRotateUpAction()

    def reverse(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """

        self._handleReverseAction()
        
    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeModalScaleArtifactEditDialog(artifact,
                                                           self.scene(),
                                                           readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeModalScaleArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleRotateDownAction(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()

        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
            else:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
                
            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        
    def _handleRotateUpAction(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()
        
        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
            else:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
                

            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()

    def _handleReverseAction(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """
        
        # Flip the flag that indicates that the musical ratios are reversed.
        self.artifact.setReversed(not self.artifact.isReversed())
        
        # Refresh everything.
        self.refreshTextItems()
        
        # Emit that the PriceBarChart has changed so that the
        # dirty flag can be set.
        self.scene().priceBarChartChanged.emit()
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        TimeModalScaleGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the TimeModalScaleGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        TimeModalScaleGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        
class PriceModalScaleGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a musical scale in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point width bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new PriceModalScaleGraphicsItem
    the position and points can be consistently set.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger(\
            "pricebarchart.PriceModalScaleGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Color of the graphicsitem bar.
        self.priceModalScaleGraphicsItemColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarColor

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.priceModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextColor

        # X scaling of the text.
        self.priceModalScaleTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceModalScaleTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceModalScaleArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.priceModalScalePenWidth = 0.0
        self.priceModalScalePen = QPen()
        self.priceModalScalePen.setColor(self.priceModalScaleGraphicsItemColor)
        self.priceModalScalePen.setWidthF(self.priceModalScalePenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Dummy item.
        self.dummyItem = QGraphicsSimpleTextItem("", self)
        
        # Set the font of the text.
        self.priceModalScaleTextFont = QFont("Sans Serif")
        self.priceModalScaleTextFont.\
            setPointSizeF(\
            self.artifact.getFontSize())

        # Set the pen color of the text.
        self.priceModalScaleTextPen = self.dummyItem.pen()
        self.priceModalScaleTextPen.\
            setColor(self.priceModalScaleGraphicsItemTextColor)

        # Set the brush color of the text.
        self.priceModalScaleTextBrush = self.dummyItem.brush()
        self.priceModalScaleTextBrush.\
            setColor(self.priceModalScaleGraphicsItemTextColor)

        # Degrees of text rotation.
        self.rotationDegrees = 0.0
        
        # Size scaling for the text.
        textTransform = QTransform()
        textTransform.scale(self.priceModalScaleTextXScaling, \
                            self.priceModalScaleTextYScaling)
        textTransform.rotate(self.rotationDegrees)
        
        # Below is a 2-dimensional list of (2
        # QGraphicsSimpleTextItems), for each of the MusicalRatios in
        # the PriceBarChartPriceModalScaleArtifact.  The 2 texts displayed
        # for each MusicalRatio is:
        #
        # 1) Fraction (or float if no numerator and no denominator is set).
        # 2) Price value
        #
        self.musicalRatioTextItems = []

        # Below is a list of HorizontalTickGraphicsItems that correspond
        # to each of the musicalRatios.
        self.horizontalTickItems = []
        
        # Initialize to blank and set at the end point.
        for musicalRatio in range(len(self.artifact.getMusicalRatios())):
            horizontalTickItem = HorizontalTickGraphicsItem(self)
            horizontalTickItem.setPos(self.endPointF)
            horizontalTickItem.setPen(self.priceModalScalePen)
            
            fractionTextItem = QGraphicsSimpleTextItem("", self)
            fractionTextItem.setPos(self.endPointF)
            fractionTextItem.setFont(self.priceModalScaleTextFont)
            fractionTextItem.setPen(self.priceModalScaleTextPen)
            fractionTextItem.setBrush(self.priceModalScaleTextBrush)
            fractionTextItem.setTransform(textTransform)
            
            priceTextItem = QGraphicsSimpleTextItem("", self)
            priceTextItem.setPos(self.endPointF)
            priceTextItem.setFont(self.priceModalScaleTextFont)
            priceTextItem.setPen(self.priceModalScaleTextPen)
            priceTextItem.setBrush(self.priceModalScaleTextBrush)
            priceTextItem.setTransform(textTransform)
            
            self.musicalRatioTextItems.\
                append([fractionTextItem, priceTextItem])

            self.horizontalTickItems.append(horizontalTickItem)

        # Flag that indicates that horizontal dotted lines should be drawn.
        self.drawHorizontalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def setDrawHorizontalDottedLinesFlag(self, flag):
        """If flag is set to true, then the horizontal dotted lines are drawn.
        """

        self.drawHorizontalDottedLinesFlag = flag
        
        # Need to call this because the bounding box is updated with
        # all the extra horizontal lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        ########
        
        # List of used musical ratios.
        musicalRatios = \
            copy.deepcopy(priceBarChartSettings.\
                          priceModalScaleGraphicsItemMusicalRatios)
        
        # PriceModalScaleGraphicsItem bar color (QColor).
        self.priceModalScaleGraphicsItemColor = \
            priceBarChartSettings.priceModalScaleGraphicsItemBarColor

        # PriceModalScaleGraphicsItem text color (QColor).
        self.priceModalScaleGraphicsItemTextColor = \
            priceBarChartSettings.priceModalScaleGraphicsItemTextColor
        
        # X scaling of the text.
        self.priceModalScaleTextXScaling = \
            priceBarChartSettings.\
                priceModalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceModalScaleTextYScaling = \
            priceBarChartSettings.\
                priceModalScaleGraphicsItemTextYScaling 

        # textEnabledFlag (bool).
        textEnabledFlag = \
            priceBarChartSettings.\
            priceModalScaleGraphicsItemTextEnabledFlag

        ########

        # Set values in the artifact.
        
        self.artifact.setMusicalRatios(musicalRatios)
        self.artifact.setColor(self.priceModalScaleGraphicsItemColor)
        self.artifact.setTextColor(self.priceModalScaleGraphicsItemTextColor)
        self.artifact.setTextEnabled(textEnabledFlag)

        self.setArtifact(self.artifact)
        
        self.refreshTextItems()
        
        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings read from app preferences.
        pass
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.refreshTextItems()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointY + (diff * (1.0 / 5))
            endThreshold = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointY <= scenePosY <= startThreshold or \
                   startingPointY >= scenePosY >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointY <= scenePosY <= endThreshold or \
                   endingPointY >= scenePosY >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(self.startPointF.x(),
                                                event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(self.endPointF.x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()
            
            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def refreshTextItems(self):
        """Sets the positions of the text items for the MusicalRatios,
        and updates the text so that they are current.
        """

        # Update the priceModalScale label text item texts.
        if self.scene() != None:
            self.recalculatePriceModalScale()

            # Traverse the 2-dimensional list and set the position of
            # each of the text items.
            artifact = self.getArtifact()
            for i in range(len(artifact.getMusicalRatios())):
                # Get the MusicalRatio that corresponds to this index.
                musicalRatio = artifact.getMusicalRatios()[i]

                # Here we always set the positions of everything.  If
                # the musicalRatio not enabled, then the corresponding
                # graphics items would have gotten disabled in the
                # self.recalculatePriceModalScale() call above.
                
                # Get the x and y position that will be the new
                # position of the text item.
                (x, y) = artifact.getXYForMusicalRatio(i)

                # Map those x and y to local coordinates.
                pointF = self.mapFromScene(QPointF(x, y))

                # Create the text transform to use.
                textTransform = QTransform()
                textTransform.scale(self.priceModalScaleTextXScaling, \
                                    self.priceModalScaleTextYScaling)
                textTransform.rotate(self.rotationDegrees)
                
                # Get the text items for this point on the scale.
                listOfTextItems = self.musicalRatioTextItems[i]

                # For each text item for that point on the scale,
                # set the position.
                for j in range(len(listOfTextItems)):
                    textItem = listOfTextItems[j]
                    # The position set is not exactly at (x, y),
                    # but instead at an offset slightly below that
                    # point so that multiple texts dont' overlap
                    # each other.
                    offsetY = (textItem.boundingRect().height() * 0.11) * j
                    textItem.setPos(QPointF(pointF.x(),
                                            pointF.y() + offsetY))
                    textItem.setFont(self.priceModalScaleTextFont)
                    textItem.setPen(self.priceModalScaleTextPen)
                    textItem.setBrush(self.priceModalScaleTextBrush)
                    textItem.setTransform(textTransform)
                    
                # Also set the position of the horizontal tick line.
                barWidth = artifact.getBarWidth()
                self.horizontalTickItems[i].setBarWidth(barWidth)
                self.horizontalTickItems[i].setPos(pointF)
                    
            # Call update on this item since positions and child items
            # were updated.
            self.prepareGeometryChange()
            self.update()

    def setStartPointF(self, pointF):
        """Sets the starting point of the priceModalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.startPointF != pointF: 
            self.startPointF = pointF

            self.setPos(self.startPointF)
            
            # Update the priceModalScale label text item positions.
            self.refreshTextItems()            

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the priceModalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.endPointF != pointF:
            self.endPointF = pointF

            self.log.debug("PriceModalScaleGraphicsItem." +
                           "setEndPointF(QPointF({}, {}))".\
                           format(pointF.x(), pointF.y()))
            
            # Update the priceModalScale label text item positions.
            self.refreshTextItems()

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        #if self.startPointF.x() > self.endPointF.x():
        #    self.log.debug("Normalization of PriceModalScaleGraphicsItem " +
        #                   "required.")
        #    
        #    # Swap the points.
        #    temp = self.startPointF
        #    self.startPointF = self.endPointF
        #    self.endPointF = temp
        #
        #    super().setPos(self.startPointF)
        #    
        #    # Update the priceModalScale label text item positions.
        #    self.refreshTextItems()
        pass
            

    def recalculatePriceModalScale(self):
        """Updates the text items that represent the ticks on the
        modal scale.  These texts will have accurate values for where
        the notes are in terms of price and price.

        In this process, it also sets the internal variables such that
        a call to self.getArtifact().getXYForMusicalRatio(index) can
        be made and a value returned that is accurate.
        """

        scene = self.scene()

        if scene != None:
            artifact = self.getArtifact()
            musicalRatios = artifact.getMusicalRatios()
            for i in range(len(musicalRatios)):
                musicalRatio = musicalRatios[i]

                if musicalRatio.isEnabled():
                    # Enable and make visible.

                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For the text items for that point on the scale,
                    # set the text.  
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]

                        # Make the text visible if it is enabled.
                        textEnabled = artifact.isTextEnabled()
                        textItem.setEnabled(textEnabled)
                        textItem.setVisible(textEnabled)

                        # If text isn't enabled, there's no need to
                        # set the text for it.  Go to the next text item.
                        if textEnabled == False:
                            continue
                    
                        if j == 0:
                            # Fraction text.  This is either the
                            # fraction (if the numerator and
                            # denominator are available), or the float
                            # value for the ratio.
                            
                            numerator = musicalRatio.getNumerator()
                            denominator = musicalRatio.getDenominator()
                            
                            if numerator != None and denominator != None:
                                fractionText = \
                                    "{}/{}".format(numerator, denominator)
                                textItem.setText(fractionText)
                            else:
                                ratio = musicalRatio.getRatio()
                                ratioText = "{}".format(ratio)
                                textItem.setText(ratioText)
                        elif j == 1:
                            # Price text.
                            
                            # Get the y location and then convert to a price.
                            (x, y) = artifact.getXYForMusicalRatio(i)
                            price = self.scene().sceneYPosToPrice(y)
                            priceText = "{}".format(price)
                            textItem.setText(priceText)

                    # Also enable and set the horizontal tick line.
                    self.horizontalTickItems[i].setVisible(True)
                    self.horizontalTickItems[i].setEnabled(True)
                            
                else:
                    # Disable and make not visable.
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For each text item for that point on the scale,
                    # set as disabled and not visible.
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]
                        textItem.setVisible(False)
                        textItem.setEnabled(False)

                    # Also disable the horizontal tick line.
                    self.horizontalTickItems[i].setVisible(False)
                    self.horizontalTickItems[i].setEnabled(False)
                    

                        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceModalScaleArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartPriceModalScaleArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartPriceModalScaleArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartPriceModalScaleArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.priceModalScaleTextFont.\
            setPointSizeF(self.artifact.getFontSize())
        self.priceModalScalePen.\
            setColor(self.artifact.getColor())
        self.priceModalScaleTextPen.\
            setColor(self.artifact.getTextColor())
        self.priceModalScaleTextBrush.\
            setColor(self.artifact.getTextColor())
        

        # Need to recalculate the price measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the measurements will be zero.
        self.refreshTextItems()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartPriceModalScaleArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        # Update the internal self.priceBarChartPriceModalScaleArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)

        # Everything else gets modified only by the edit dialog.
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the horizontal bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.
        
        barWidth = \
            self.getArtifact().getBarWidth()
        
        # The QRectF returned is relative to this (0, 0) point.
        xBottomRight = 1.0 * (barWidth * 0.5)
        yBottomRight = 0.0
        
        xBottomLeft = -1.0 * (barWidth * 0.5)
        yBottomLeft = 0.0
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopLeft = (-1.0 * (barWidth * 0.5)) + xDelta
        yTopLeft = 0.0 + yDelta

        xTopRight = (1.0 * (barWidth * 0.5)) + xDelta
        yTopRight = 0.0 + yDelta
        
        # Get the last and first PriceBar's timestamp in local
        # coordinates.
        earliestPriceBar = self.scene().getEarliestPriceBar()
        smallestPriceBarX = \
            self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
        localSmallestPriceBarX = \
            self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

        latestPriceBar = self.scene().getLatestPriceBar()
        largestPriceBarX = \
            self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
        localLargestPriceBarX = \
            self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
                
        xValues = []
        xValues.append(xTopLeft)
        xValues.append(xBottomLeft)
        xValues.append(xTopRight)
        xValues.append(xBottomRight)
        xValues.append(localSmallestPriceBarX)
        xValues.append(localLargestPriceBarX)
        
        yValues = []
        yValues.append(yTopLeft)
        yValues.append(yBottomLeft)
        yValues.append(yTopRight)
        yValues.append(yBottomRight)
        
        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        barWidth = \
            self.getArtifact().getBarWidth()
        
        # The QRectF returned is relative to this (0, 0) point.
        xBottomRight = 1.0 * (barWidth * 0.5)
        yBottomRight = 0.0
        
        xBottomLeft = -1.0 * (barWidth * 0.5)
        yBottomLeft = 0.0
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopLeft = (-1.0 * (barWidth * 0.5)) + xDelta
        yTopLeft = 0.0 + yDelta

        xTopRight = (1.0 * (barWidth * 0.5)) + xDelta
        yTopRight = 0.0 + yDelta
        
        topLeft = QPointF(xTopLeft, yTopLeft)
        topRight = QPointF(xTopRight, yTopRight)
        bottomRight = QPointF(xBottomRight, yBottomRight)
        bottomLeft = QPointF(xBottomLeft, yBottomLeft)
        
        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.priceModalScalePen is set to what we want for the drawing
        style.
        """

        self.log.debug("Entered PriceModalScaleGraphicsItem.paint().  " +
                       "pos is: ({}, {})".format(self.pos().x(),
                                                 self.pos().y()))
                       
        if painter.pen() != self.priceModalScalePen:
            painter.setPen(self.priceModalScalePen)

        artifact = self.getArtifact()
        barWidth = artifact.getBarWidth()

        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left horizontal bar part.
        x1 = 1.0 * (barWidth * 0.5)
        y1 = 0.0
        x2 = -1.0 * (barWidth * 0.5)
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right horizontal bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = (1.0 * (barWidth * 0.5)) + xDelta
        y1 = 0.0 + yDelta
        x2 = (-1.0 * (barWidth * 0.5)) + xDelta
        y2 = 0.0 + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw horizontal dotted lines at each enabled musicalRatio if
        # the flag is set to do so, or if it is selected.
        if self.drawHorizontalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.priceModalScalePen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the last and first PriceBar's timestamp in local
                # coordinates.
                earliestPriceBar = self.scene().getEarliestPriceBar()
                smallestPriceBarX = \
                    self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
                localSmallestPriceBarX = \
                    self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

                latestPriceBar = self.scene().getLatestPriceBar()
                largestPriceBarX = \
                    self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
                localLargestPriceBarX = \
                    self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
                
                xValues.append(localSmallestPriceBarX)
                xValues.append(localLargestPriceBarX)

                # We have all x values now, so sort them to get the
                # low and high.
                xValues.sort()
                smallestX = xValues[0]
                largestX = xValues[-1]
        
                for horizontalTickItem in self.horizontalTickItems:
                    if horizontalTickItem.isEnabled() and \
                       horizontalTickItem.isVisible():
                    
                        localPosY = horizontalTickItem.pos().y()

                        startPoint = QPointF(largestX, localPosY)
                        endPoint = QPointF(smallestX, localPosY)
                        
                        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
                
                        painter.setPen(QPen(option.palette.windowText(), 0,
                                            Qt.DashLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
            
                # Draw the horizontal line for the start point.
                startPoint = QPointF(largestX, 0.0)
                endPoint = QPointF(smallestX, 0.0)
                
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)

                # Draw the horizontal line for the end point.
                startPoint = QPointF(largestX, 0.0 + yDelta)
                endPoint = QPointF(smallestX, 0.0 + yDelta)
                
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)

                
        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.priceModalScalePen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceModalScaleGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceModalScaleGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        rotateDownAction = QAction("Rotate Down", parent)
        rotateUpAction = QAction("Rotate Up", parent)
        reverseAction = QAction("Reverse", parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)

        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        rotateDownAction.triggered.\
            connect(self._handleRotateDownAction)
        rotateUpAction.triggered.\
            connect(self._handleRotateUpAction)
        reverseAction.triggered.\
            connect(self._handleReverseAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        rotateDownAction.setEnabled(not readOnlyMode)
        rotateUpAction.setEnabled(not readOnlyMode)
        reverseAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addAction(rotateDownAction)
        menu.addAction(rotateUpAction)
        menu.addAction(reverseAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)

    def rotateDown(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        self._handleRotateDownAction()
        
    def rotateUp(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        self._handleRotateUpAction()

    def reverse(self):
        """Causes the TimeModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """

        self._handleReverseAction()
        
    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceModalScaleArtifactEditDialog(artifact,
                                                           self.scene(),
                                                           readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceModalScaleArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleRotateDownAction(self):
        """Causes the PriceModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()

        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
            else:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
                
            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        
    def _handleRotateUpAction(self):
        """Causes the PriceModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()
        
        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
            else:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
                

            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()

    def _handleReverseAction(self):
        """Causes the PriceModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """
        
        # Flip the flag that indicates that the musical ratios are reversed.
        self.artifact.setReversed(not self.artifact.isReversed())
        
        # Refresh everything.
        self.refreshTextItems()
        
        # Emit that the PriceBarChart has changed so that the
        # dirty flag can be set.
        self.scene().priceBarChartChanged.emit()
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the PriceModalScaleGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the PriceModalScaleGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the PriceModalScaleGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        PriceModalScaleGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
        
class PriceTimeInfoGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBarChartPriceTimeInfoArtifact."""
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceTimeInfoArtifact()

        # Convert object.
        self.convertObj = None
        
        # BirthInfo object that holds information about the birth of
        # this trading entity.  This is used so we can determine
        # amount of time elapsed since birth.
        self.birthInfo = None
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(0.0, 0.0)

        # Set the font of the text.
        self.textItemFont = self.artifact.getFont()
        self.textItem.setFont(self.textItemFont)

        # Set the color of the text.
        self.color = self.artifact.getColor()
        
        # Set the pen color of the text.
        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.artifact.getColor())
        self.textItem.setPen(self.textItemPen)

        # Set the brush color of the text.
        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.artifact.getColor())
        self.textItem.setBrush(self.textItemBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.artifact.getTextXScaling(), \
                            self.artifact.getTextYScaling())
        self.textItem.setTransform(textTransform)

        # Flag that indicates that we should draw a dotted line to the
        # infoPointF.
        self.drawLineToInfoPointFFlag = False

    def setDrawLineToInfoPointFFlag(self, flag):
        """If set to true, then a line is drawn from the box to the
        infoPointF point during paint calls.  If false, then that line
        is not drawn.
        """

        self.drawLineToInfoPointFFlag = flag
        
        # Need to call this because the bounding box is updated with
        # all the extra line being drawn.
        self.prepareGeometryChange()
        
    def setConvertObj(self, convertObj):
        """Object for doing conversions from x and datetime and y to
        price.  This should be the graphics scene.  This is used
        because sometimes we want to be able to do conversions and
        stuff before we even add the item to the scene.
        """

        self.log.debug("Entered setConvertObj()")
        
        self.convertObj = convertObj
        
        self.log.debug("Exiting setConvertObj()")
        
    def setBirthInfo(self, birthInfo):
        """Sets the internal BirthInfo object so that time elapsed
        from birth can be calculated.
        """

        self.birthInfo = birthInfo

        # Update the text according to what's in infoPointF and birthInfo.
        self._updateText()
        self.update()
        
    def getBirthInfo(self):
        """Returns the internal BirthInfo object.
        """

        return self.birthInfo

    def setInfoPointF(self, infoPointF):
        """Sets the infoPointF used in this QGraphicsItem.  Also
        updates the artifact accordingly.
        """

        self.artifact.setInfoPointF(infoPointF)
    
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceTimeInfoArtifact object's data
        into this QGraphicsPriceTimeInfoItem.

        Arguments:
        artifact - PriceBarChartPriceTimeInfoArtifact object with information
                   about this PriceTimeInfoGraphisItem
        """

        self.log.debug("Entered setArtifact()")

        if isinstance(artifact, PriceBarChartPriceTimeInfoArtifact):
            self.artifact = artifact

            self.log.debug("Setting PriceTimeInfoGraphicsItem with the " +
                           "following artifact: " + self.artifact.toString())
            self.log.debug("Font in artifact is: " +
                           self.artifact.getFont().toString())
                           
            # Extract and set the internals according to the info 
            # in self.artifact.
            self.setPos(self.artifact.getPos())

            # Update the text according to what's in infoPointF and birthInfo.
            self._updateText()
            
            # Set the font of the text.
            self.textItemFont = self.artifact.getFont()
            self.textItem.setFont(self.textItemFont)

            # Set the color of the text.
            self.color = self.artifact.getColor()
            
            # Set the pen color of the text.
            self.textItemPen = self.textItem.pen()
            self.textItemPen.setColor(self.color)
            self.textItem.setPen(self.textItemPen)

            # Set the brush color of the text.
            self.textItemBrush = self.textItem.brush()
            self.textItemBrush.setColor(self.color)
            self.textItem.setBrush(self.textItemBrush)

            # Apply some size scaling to the text.
            self.textTransform = QTransform()
            self.textTransform.scale(self.artifact.getTextXScaling(), \
                                     self.artifact.getTextYScaling())
            self.textItem.setTransform(self.textTransform)

            self.update()
        else:
            raise TypeError("Expected artifact type: " +
                            "PriceBarChartPriceTimeInfoArtifact")
    
        self.log.debug("Exiting setArtifact()")

    def recalculatePriceTimeInfo(self):
        """Just updates the text."""

        self._updateText()
        
    def _updateText(self):
        """Updates the text based on what is in the artifact.
        """

        # This object needs either the self.convertObj set, or the
        # parent graphicsscene set or else it won't have the capacity
        # to do price and datetime conversions to coordinates.
        if self.convertObj == None:
            if self.scene() == None:
                self.log.debug("_updateText(): Not able to update the text " +
                               "because QGraphicsScene for unit conversions " +
                               "was not set (or the item wasn't added to a " +
                               "qgraphicsscene yet")
                self.textItem.setText("INVALID")
                return
            else:
                self.convertObj = self.scene()
        
        # Set the text according to various flags in the artifact.
        # Internal QGraphicsItem that holds the text.
        # Initialize to blank and set at the end point.
        infoPointF = self.artifact.getInfoPointF()
        dt = self.convertObj.sceneXPosToDatetime(infoPointF.x())
        price = self.convertObj.sceneYPosToPrice(infoPointF.y())

        text = ""

        if self.artifact.getShowTimestampFlag():
            text += "t={}".format(Ephemeris.datetimeToDayStr(dt)) + \
                    os.linesep
            
        if self.artifact.getShowPriceFlag():
            text += "p={:.4f}".format(price) + os.linesep
            
        if self.artifact.getShowSqrtPriceFlag():
            text += "sqrt(p)={:.4f}".format(math.sqrt(price)) + os.linesep
            
        if self.artifact.getShowTimeElapsedSinceBirthFlag():
            if self.birthInfo != None:
                # Get the birth timestamp and convert to X coordinate.
                birthDtUtc = self.birthInfo.getBirthUtcDatetime()
                birthX = self.convertObj.datetimeToSceneXPos(birthDtUtc)

                # Find the difference between the info points and birthX
                xDiff = infoPointF.x() - birthX

                text += "t_elapsed={:.4f}".format(xDiff) + os.linesep
                
        if self.artifact.getShowSqrtTimeElapsedSinceBirthFlag():
            if self.birthInfo != None:
                # Get the birth timestamp and convert to X coordinate.
                birthDtUtc = self.birthInfo.getBirthUtcDatetime()
                birthX = self.convertObj.datetimeToSceneXPos(birthDtUtc)

                # Find the difference between the info points and birthX
                xDiff = infoPointF.x() - birthX

                text += "sqrt(t_elapsed)={:.4f}".format(math.sqrt(xDiff)) + \
                        os.linesep
        
        if self.artifact.getShowPriceScaledValueFlag():
            scaledValue = self.convertObj.convertPriceToScaledValue(price)
            text += "p_u={:.4f}".format(scaledValue) + os.linesep
            
        if self.artifact.getShowSqrtPriceScaledValueFlag():
            scaledValue = self.convertObj.convertPriceToScaledValue(price)
            sqrtScaledValue = math.sqrt(abs(scaledValue))
            text += "sqrt(p_u)={:.4f}".format(sqrtScaledValue) + os.linesep
            
        if self.artifact.getShowTimeScaledValueFlag():
            scaledValue = self.convertObj.convertDatetimeToScaledValue(dt)
            text += "t_u={:.4f}".format(scaledValue) + os.linesep
            
        if self.artifact.getShowSqrtTimeScaledValueFlag():
            scaledValue = self.convertObj.convertDatetimeToScaledValue(dt)
            sqrtScaledValue = math.sqrt(abs(scaledValue))
            text += "sqrt(t_u)={:.4f}".format(sqrtScaledValue) + os.linesep

        text = text.rstrip()
        self.textItem.setText(text)
        self.prepareGeometryChange()
        
    def getArtifact(self):
        """Returns a PriceBarChartPriceTimeInfoArtifact for this QGraphicsItem 
        so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceTimeInfoArtifact to be 
        # current, then return it.
        self.artifact.setPos(self.pos())
        self.artifact.setFont(self.textItemFont)
        self.artifact.setColor(self.color)
        self.artifact.setTextXScaling(self.textTransform.m11())
        self.artifact.setTextYScaling(self.textTransform.m22())
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        # Set values from the priceBarChartSettings into the internal
        # member variables.
        
        self.textItemFont = QFont()
        self.textItemFont.\
            fromString(priceBarChartSettings.\
                       priceTimeInfoGraphicsItemDefaultFontDescription) 
        self.color = \
            priceBarChartSettings.priceTimeInfoGraphicsItemDefaultColor
        
        self.textTransform = QTransform()
        self.textTransform.scale(priceBarChartSettings.\
                                 priceTimeInfoGraphicsItemDefaultXScaling,
                                 priceBarChartSettings.\
                                 priceTimeInfoGraphicsItemDefaultYScaling)

        # Set values in the artifact since that's what we reference to
        # draw things.

        # showTimestampFlag (bool).
        self.artifact.setShowTimestampFlag(\
            priceBarChartSettings.priceTimeInfoGraphicsItemShowTimestampFlag)

        # showPriceFlag (bool).
        self.artifact.setShowPriceFlag(\
            priceBarChartSettings.priceTimeInfoGraphicsItemShowPriceFlag)
        
        # showSqrtPriceFlag (bool).
        self.artifact.setShowSqrtPriceFlag(\
            priceBarChartSettings.priceTimeInfoGraphicsItemShowSqrtPriceFlag)
        
        # showTimeElapsedSinceBirthFlag (bool).
        self.artifact.setShowTimeElapsedSinceBirthFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag)
        
        # showSqrtTimeElapsedSinceBirthFlag (bool).
        self.artifact.setShowSqrtTimeElapsedSinceBirthFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag)

        # showPriceScaledValueFlag (bool).
        self.artifact.setShowPriceScaledValueFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowPriceScaledValueFlag)
        
        # showSqrtPriceScaledValueFlag (bool).
        self.artifact.setShowSqrtPriceScaledValueFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag)
        
        # showTimeScaledValueFlag (bool).
        self.artifact.setShowTimeScaledValueFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowTimeScaledValueFlag)
        
        # showSqrtTimeScaledValueFlag (bool).
        self.artifact.setShowSqrtTimeScaledValueFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag)
        
        # showLineToInfoPointFlag (bool).
        self.artifact.setShowLineToInfoPointFlag(\
            priceBarChartSettings.\
            priceTimeInfoGraphicsItemShowLineToInfoPointFlag)

        # Update the internal text item.
        self.textItem.setFont(self.textItemFont)

        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.color)
        self.textItem.setPen(self.textItemPen)

        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.color)
        self.textItem.setBrush(self.textItemBrush)

        self.textItem.setTransform(self.textTransform)

        # Update text since the flags for what to display could have
        # been updated.
        self._updateText()
        
        # Schedule an update.
        self.prepareGeometryChange()
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        pass

    def setTextLabelEdgeYLocation(self, y):
        """Sets the y location of the edge of the box that is the text
        graphics item.

        Arguments:
        y - float value for the y position of the edge of the box.
        """

        artifact = self.getArtifact()
        infoPointF = artifact.getInfoPointF()
        
        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        textBoundingRect = self.textItem.boundingRect().normalized()
        width = textBoundingRect.width()
        height = textBoundingRect.height()
        scaledWidth = width * self.textTransform.m11()
        scaledHeight = height * self.textTransform.m22()
        
        if y > infoPointF.y():
            # Below.
            posX = infoPointF.x() - (scaledWidth * 0.5)
            posY = y
            pos = QPointF(posX, posY)
            self.setPos(pos)
        else:
            # Above
            posX = infoPointF.x() - (scaledWidth * 0.5)
            posY = y - scaledHeight
            pos = QPointF(posX, posY)
            self.setPos(pos)

        self.update()
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Arguments:
        pos - QPointF holding the new position.
        """
        
        super().setPos(pos)

    def _getScaledRectOfTextItem(self):
        """Returns the scaled QRectF of the self.textItem."""
        
        # Coordinate (0, 0) is the location of the internal text item
        # in local coordinates.  The QRectF returned is relative to
        # this (0, 0) point.

        textItemBoundingRect = self.textItem.boundingRect()

        self.log.debug("Bounding rect of textItem is: x={}, y={}, w={}, h={}".\
                       format(textItemBoundingRect.x(),
                              textItemBoundingRect.y(),
                              textItemBoundingRect.width(),
                              textItemBoundingRect.height()))
                       
        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        width = textItemBoundingRect.width()
        height = textItemBoundingRect.height()
        scaledWidth = width * self.textTransform.m11()
        scaledHeight = height * self.textTransform.m22()

        topLeft = QPointF(0, 0)
        bottomRight = QPointF(scaledWidth, scaledHeight)
        scaledTextRect = QRectF(topLeft, bottomRight)

        return scaledTextRect
    
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        self.log.debug("Entered boundingRect()")

        scaledTextRect = self._getScaledRectOfTextItem()
        
        self.log.debug("scaledTextRect is: x={}, y={}, w={}, h={}".\
                       format(scaledTextRect.x(),
                              scaledTextRect.y(),
                              scaledTextRect.width(),
                              scaledTextRect.height()))
                       
        localInfoPointF = self.mapFromScene(self.artifact.getInfoPointF())
        
        self.log.debug("localInfoPointF is: x={}, y={}".\
                       format(localInfoPointF.x(),
                              localInfoPointF.y()))
                       
        xValues = []
        xValues.append(scaledTextRect.topLeft().x())
        xValues.append(scaledTextRect.bottomLeft().x())
        xValues.append(scaledTextRect.topRight().x())
        xValues.append(scaledTextRect.bottomRight().x())
        xValues.append(localInfoPointF.x())

        yValues = []
        yValues.append(scaledTextRect.topLeft().y())
        yValues.append(scaledTextRect.bottomLeft().y())
        yValues.append(scaledTextRect.topRight().y())
        yValues.append(scaledTextRect.bottomRight().y())
        yValues.append(localInfoPointF.y())

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        self.log.debug("rv coordinates are: ({}, {}), width={}, height={}".\
                       format(rv.x(), rv.y(), rv.width(), rv.height()))
        
        self.log.debug("Exiting boundingRect()")
        
        return rv
    
    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        self.log.debug("Entering shape()")
        
        scaledTextRect = self._getScaledRectOfTextItem()

        painterPath = QPainterPath()
        painterPath.addRect(scaledTextRect)

        self.log.debug("scaledTextRect coordinates are: " +
                       "({}, {}), width={}, height={}".\
                       format(scaledTextRect.x(),
                              scaledTextRect.y(),
                              scaledTextRect.width(),
                              scaledTextRect.height()))
        
        self.log.debug("Exiting shape()")
        
        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.textItemPen is set
        to what we want for the drawing style.
        """

        self.log.debug("Entering paint()")
        self.log.debug("self.drawLineToInfoPointFFlag={}".\
                       format(self.drawLineToInfoPointFFlag))
        
        if painter.pen() != self.textItemPen:
            painter.setPen(QPen(self.textItemPen))

        if self.drawLineToInfoPointFFlag == True or \
               option.state & QStyle.State_Selected:

            self.log.debug("Drawing the line to the infoPointF...")
            
            # Draw a line to the infoPointF.  Below is setting the colors
            # and drawing parameters.
            pad = self.textItemPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            bgcolor = QColor(r, g, b)
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
    
            scaledTextRect = self._getScaledRectOfTextItem()
            
            topLeft = scaledTextRect.topLeft()
            bottomRight = scaledTextRect.bottomRight()
            localInfoPointF = self.mapFromScene(self.artifact.getInfoPointF())
    
            x = scaledTextRect.width() * 0.5
            y = None
            if localInfoPointF.y() > 0:
                y = scaledTextRect.height()
            else:
                y = 0.0
                
            # Set the start and end points to the line.
            startLinePoint = QPointF(x, y)
            endLinePoint = localInfoPointF
    
            self.log.debug("Start and end points of the line are: " +
                           "({}, {}), ({}, {})".\
                           format(startLinePoint.x(),
                                  startLinePoint.y(),
                                  endLinePoint.x(),
                                  endLinePoint.y()))
            
            # Draw the line.
            painter.drawLine(startLinePoint, endLinePoint)
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawLine(startLinePoint, endLinePoint)
        
        elif self.artifact.getShowLineToInfoPointFlag() == True:
            
            self.log.debug("Drawing regular line to InfoPoint.")
            
            scaledTextRect = self._getScaledRectOfTextItem()
            
            topLeft = scaledTextRect.topLeft()
            bottomRight = scaledTextRect.bottomRight()
            localInfoPointF = self.mapFromScene(self.artifact.getInfoPointF())
    
            x = scaledTextRect.width() * 0.5
            y = None
            if localInfoPointF.y() > 0:
                y = scaledTextRect.height()
            else:
                y = 0.0
                
            # Set the start and end points to the line.
            startLinePoint = QPointF(x, y)
            endLinePoint = localInfoPointF

            self.log.debug("Start and end points of the line are: " +
                           "({}, {}), ({}, {})".\
                           format(startLinePoint.x(),
                                  startLinePoint.y(),
                                  endLinePoint.x(),
                                  endLinePoint.y()))
                           
            # Draw the line.
            pen = QPen()
            pen.setColor(self.artifact.getColor())
            painter.setPen(pen)
            
            brush = QBrush()
            brush.setColor(self.artifact.getColor())
            painter.setBrush(brush)
            
            painter.drawLine(startLinePoint, endLinePoint)
            
        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.textItemPen.widthF() * 0.5;

            self.log.debug("Drawing selected dotted line.")
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

        self.log.debug("Exiting paint()")
        
    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceBarChartArtifactGraphicsItem.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setAstro1Action = \
            QAction("Set info point timestamp on Astro Chart &1", parent)
        setAstro2Action = \
            QAction("Set info point timestamp on Astro Chart &2", parent)
        setAstro3Action = \
            QAction("Set info point timestamp on Astro Chart &3", parent)
        openJHoraAction = \
            QAction("Open JHor&a with info point timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setAstro1Action.triggered.\
            connect(self._handleSetAstro1Action)
        setAstro2Action.triggered.\
            connect(self._handleSetAstro2Action)
        setAstro3Action.triggered.\
            connect(self._handleSetAstro3Action)
        openJHoraAction.triggered.\
            connect(self._handleOpenJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setAstro1Action.setEnabled(True)
        setAstro2Action.setEnabled(True)
        setAstro3Action.setEnabled(True)
        openJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setAstro1Action)
        menu.addAction(setAstro2Action)
        menu.addAction(setAstro3Action)
        menu.addAction(openJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()

        self.log.debug("Inside _handleInfoAction(): artifact is: " +
                       artifact.toString())
        
        dialog = PriceBarChartPriceTimeInfoArtifactEditDialog(artifact,
                                                              self.scene(),
                                                              readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceTimeInfoArtifactEditDialog(artifact,
                                                     self.scene(),
                                                     readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart1(self.artifact.getInfoPointF().x())
        
    def _handleSetAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart2(self.artifact.getInfoPointF().x())
        
    def _handleSetAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart3(self.artifact.getInfoPointF().x())

    def _handleOpenJHoraAction(self):
        """Causes the timestamp of this PriceBarGraphicsItem to be
        opened in JHora.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().openJHora(self.artifact.getInfoPointF().x())

        
class PriceMeasurementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a measurement ruler for price in
    the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point of the start point of the ruler.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceMeasurementGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Width of the horizontal bar drawn.
        self.priceMeasurementGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemBarWidth
 
        # X scaling of the text.
        self.priceMeasurementTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceMeasurementTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextYScaling 

        # Font.
        self.priceMeasurementTextFont = QFont()
        self.priceMeasurementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceMeasurementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceMeasurementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultColor

        # PriceMeasurementGraphicsItem showPriceRangeTextFlag (bool).
        self.showPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtPriceRangeTextFlag (bool).
        self.showSqrtPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.showScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.showSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceMeasurementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.priceMeasurementPenWidth = 0.0
        self.priceMeasurementPen = QPen()
        self.priceMeasurementPen.\
            setColor(self.priceMeasurementGraphicsItemColor)
        self.priceMeasurementPen.setWidthF(self.priceMeasurementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Variables holding the price measurement values.
        self.priceRange = 0.0
        self.sqrtPriceRange = 0.0
        self.scaledValueRange = 0.0
        self.sqrtScaledValueRange = 0.0
        
        # Internal QGraphicsItem that holds the text of the price measurements.
        # Initialize to blank and set at the end point.
        self.priceMeasurementPriceRangeText = \
            QGraphicsSimpleTextItem("", self)
        self.priceMeasurementSqrtPriceRangeText = \
            QGraphicsSimpleTextItem("", self)
        self.priceMeasurementScaledValueRangeText = \
            QGraphicsSimpleTextItem("", self)
        self.priceMeasurementSqrtScaledValueRangeText = \
            QGraphicsSimpleTextItem("", self)

        # List of text items as created above.  This is so we can more
        # quickly and easily apply new settings.  It also helps for
        # painting things nicely.
        self.textItems = []
        self.textItems.append(self.priceMeasurementPriceRangeText)
        self.textItems.append(self.priceMeasurementSqrtPriceRangeText)
        self.textItems.append(self.priceMeasurementScaledValueRangeText)
        self.textItems.append(self.priceMeasurementSqrtScaledValueRangeText)

        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Flag that indicates that horizontaldotted lines should be drawn.
        self.drawHorizontalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def setDrawHorizontalDottedLinesFlag(self, flag):
        """If flag is set to true, then the horizontal dotted lines are drawn.
        """

        self.drawHorizontalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra horizontal lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Width of the horizontal bar drawn.
        self.priceMeasurementGraphicsItemBarWidth = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultBarWidth
 
        # X scaling of the text.
        self.priceMeasurementTextXScaling = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultTextXScaling 

        # Y scaling of the text.
        self.priceMeasurementTextYScaling = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultTextYScaling 

        # Font.
        self.priceMeasurementTextFont = QFont()
        self.priceMeasurementTextFont.fromString(\
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceMeasurementGraphicsItemTextColor = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceMeasurementGraphicsItemColor = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultColor

        # PriceMeasurementGraphicsItem showPriceRangeTextFlag (bool).
        self.showPriceRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtPriceRangeTextFlag (bool).
        self.showSqrtPriceRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.showScaledValueRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.showSqrtScaledValueRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
    
        ####################################################################

        # Set specific items enabled or disabled, visible or not,
        # based on the above flags being set.
        
        # Set the text items as enabled or disabled.
        self.priceMeasurementPriceRangeText.\
            setEnabled(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setEnabled(self.showSqrtPriceRangeTextFlag)
        self.priceMeasurementScaledValueRangeText.\
            setEnabled(self.showScaledValueRangeTextFlag)
        self.priceMeasurementSqrtScaledValueRangeText.\
            setEnabled(self.showSqrtScaledValueRangeTextFlag)

        # Set the text items as visible or invisible.
        self.priceMeasurementPriceRangeText.\
            setVisible(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setVisible(self.showSqrtPriceRangeTextFlag)
        self.priceMeasurementScaledValueRangeText.\
            setVisible(self.showScaledValueRangeTextFlag)
        self.priceMeasurementSqrtScaledValueRangeText.\
            setVisible(self.showSqrtScaledValueRangeTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Recalculate the price measurement because scaling could have changed.
        self.recalculatePriceMeasurement()
        
        # Update the priceMeasurement text item position.
        self._updateTextItemPositions()

        # Set the new color of the pen for drawing the bar.
        self.priceMeasurementPen.\
            setColor(self.priceMeasurementGraphicsItemColor)
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculatePriceMeasurement()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointY={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointY + (diff * (1.0 / 5))
            endThreshold = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if scenePosY <= startThreshold:
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
            elif scenePosY >= endThreshold:
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(self.startPointF.x(),
                                                event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(self.endPointF.x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)
            
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the priceMeasurement label position.
            
        # Y location where to place the item.
        deltaY = self.endPointF.y() - self.startPointF.y()
        y = deltaY * 0.5

        # Starting Y location to place the text item.
        startY = y

        # Amount to mutiply to the bar width to get the offset.
        offsetY = 0.3

        # j is the running index of the enabled text item.
        j = 0

        for i in reversed(range(len(self.textItems))):
            # Get the current text item.
            textItem = self.textItems[i]

            # Set the position no matter what, but only increment
            # j if the item is enabled and displayed.  This is so
            # we keep the text items on the graphicsScene close to
            # its parent item.
            x = self.priceMeasurementGraphicsItemBarWidth * 0.5
            y = startY - \
                ((offsetY * j) * self.priceMeasurementGraphicsItemBarWidth)
            textItem.setPos(QPointF(x, y))
            if textItem.isEnabled() and textItem.isVisible():
                j += 1
                    
    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        y = pointF.y()

        newValue = QPointF(self.endPointF.x(), y)

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the pricemeasurement.
                self.recalculatePriceMeasurement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        y = pointF.y()

        newValue = QPointF(self.startPointF.x(), y)

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the pricemeasurement.
                self.recalculatePriceMeasurement()
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.y() > self.endPointF.y():
            self.log.debug("Normalization of PriceMeasurementGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            self.recalculatePriceMeasurement()
            
            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            super().setPos(self.startPointF)
            

    def recalculatePriceMeasurement(self):
        """Sets the internal variables:
        
            self.priceRange
            self.sqrtPriceRange
            self.scaledValueRange
            self.sqrtScaledValueRange
            
        to hold the amount of price between the start and end points.
        """

        scene = self.scene()

        # Reset the values.
        self.priceRange = 0.0
        self.sqrtPriceRange = 0.0
        self.scaledValueRange = 0.0
        self.sqrtScaledValueRange = 0.0

        if scene != None:
            startPointPrice = \
                scene.sceneYPosToPrice(self.startPointF.y())
            self.log.debug("startPointPrice: {}".format(startPointPrice))
            
            endPointPrice = \
                scene.sceneYPosToPrice(self.endPointF.y())
            self.log.debug("endPointPrice: {}".format(endPointPrice))

            self.priceRange = abs(endPointPrice - startPointPrice)
            self.sqrtPriceRange = math.sqrt(abs(self.priceRange))
            self.scaledValueRange = \
                abs(scene.convertPriceToScaledValue(endPointPrice) - \
                    scene.convertPriceToScaledValue(startPointPrice))
            self.sqrtScaledValueRange = \
                math.sqrt(abs(self.scaledValueRange))
            
            self.log.debug("self.priceRange={}".format(self.priceRange))
            self.log.debug("self.sqrtPriceRange={}".format(self.sqrtPriceRange))
            self.log.debug("self.scaledValueRange={}".\
                           format(self.scaledValueRange))
            self.log.debug("self.sqrtScaledValueRange={}".\
                           format(self.sqrtScaledValueRange))
            
        # Update the text of the internal items.
        priceRangeText = "{:.4f} p_range".format(self.priceRange)
        sqrtPriceRangeText = "{:.4f} sqrt(p_range)".format(self.sqrtPriceRange)
        scaledValueRangeText = "{:.4f} u_range".\
                               format(self.scaledValueRange)
        sqrtScaledValueRangeText = "{:.4f} sqrt(u_range)".\
                               format(self.sqrtScaledValueRange)
        
        self.priceMeasurementPriceRangeText.setText(priceRangeText)
        self.priceMeasurementSqrtPriceRangeText.setText(sqrtPriceRangeText)
        self.priceMeasurementScaledValueRangeText.setText(scaledValueRangeText)
        self.priceMeasurementSqrtScaledValueRangeText.\
            setText(sqrtScaledValueRangeText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceMeasurementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartPriceMeasurementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartPriceMeasurementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartPriceMeasurementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.priceMeasurementTextXScaling = self.artifact.getTextXScaling()
        self.priceMeasurementTextYScaling = self.artifact.getTextYScaling()
        self.priceMeasurementTextFont = self.artifact.getFont()
        self.priceMeasurementGraphicsItemTextColor = \
            self.artifact.getTextColor()
        self.priceMeasurementPen.setColor(self.artifact.getColor())
        
        self.showPriceRangeTextFlag = \
            self.artifact.getShowPriceRangeTextFlag()
        self.showSqrtPriceRangeTextFlag = \
            self.artifact.getShowSqrtPriceRangeTextFlag()
        self.showScaledValueRangeTextFlag = \
            self.artifact.getShowScaledValueRangeTextFlag()
        self.showSqrtScaledValueRangeTextFlag = \
            self.artifact.getShowSqrtScaledValueRangeTextFlag()

        #############

        # Set the text items as enabled or disabled.
        self.priceMeasurementPriceRangeText.\
            setEnabled(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setEnabled(self.showSqrtPriceRangeTextFlag)
        self.priceMeasurementScaledValueRangeText.\
            setEnabled(self.showScaledValueRangeTextFlag)
        self.priceMeasurementSqrtScaledValueRangeText.\
            setEnabled(self.showSqrtScaledValueRangeTextFlag)

        # Set the text items as visible or invisible.
        self.priceMeasurementPriceRangeText.\
            setVisible(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setVisible(self.showSqrtPriceRangeTextFlag)
        self.priceMeasurementScaledValueRangeText.\
            setVisible(self.showScaledValueRangeTextFlag)
        self.priceMeasurementSqrtScaledValueRangeText.\
            setVisible(self.showSqrtScaledValueRangeTextFlag)

        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the priceMeasurement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the price measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the price measurements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculatePriceMeasurement()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartPriceMeasurementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceMeasurementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.priceMeasurementTextXScaling)
        self.artifact.setTextYScaling(self.priceMeasurementTextYScaling)
        self.artifact.setFont(self.priceMeasurementTextFont)
        self.artifact.setTextColor(self.priceMeasurementGraphicsItemTextColor)
        self.artifact.setColor(self.priceMeasurementPen.color())
        
        self.artifact.setShowPriceRangeTextFlag(\
            self.showPriceRangeTextFlag)
        self.artifact.setShowSqrtPriceRangeTextFlag(\
            self.showSqrtPriceRangeTextFlag)
        self.artifact.setShowScaledValueRangeTextFlag(\
            self.showScaledValueRangeTextFlag)
        self.artifact.setShowSqrtScaledValueRangeTextFlag(\
            self.showSqrtScaledValueRangeTextFlag)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.

        # The QRectF returned is relative to this (0, 0) point.

        # Get the QRectF with just the lines.
        yDelta = self.endPointF.y() - self.startPointF.y()

        topLeft = \
            QPointF(-1.0 * \
                    (self.priceMeasurementGraphicsItemBarWidth * 0.5),
                    0.0)
        
        bottomRight = \
            QPointF(1.0 * \
                    (self.priceMeasurementGraphicsItemBarWidth * 0.5),
                    yDelta)

        # Initalize to the above boundaries.  We will set them below.
        localHighX = bottomRight.x()
        localLowX = topLeft.x()
        if self.drawHorizontalDottedLinesFlag or self.isSelected():
            # Get the last and first PriceBar's timestamp in local
            # coordinates.
            earliestPriceBar = self.scene().getEarliestPriceBar()
            smallestPriceBarX = \
                self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
            localSmallestPriceBarX = \
                self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

            # Overwrite the low if it is smaller.
            if localSmallestPriceBarX < localLowX:
                localLowX = localSmallestPriceBarX
            
            latestPriceBar = self.scene().getLatestPriceBar()
            largestPriceBarX = \
                self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
            localLargestPriceBarX = \
                self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
        
            # Overwrite the high if it is larger.
            if localLargestPriceBarX > localHighX:
                localHighX = localLargestPriceBarX
            
        xValues = []
        xValues.append(topLeft.x())
        xValues.append(bottomRight.x())
        xValues.append(localHighX)
        xValues.append(localLowX)

        yValues = []
        yValues.append(topLeft.y())
        yValues.append(bottomRight.y())

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Get the QRectF with just the lines.
        yDelta = self.endPointF.y() - self.startPointF.y()

        topLeft = \
            QPointF(-1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5),
                    0.0)
        
        bottomRight = \
            QPointF(1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5),
                    yDelta)

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.priceMeasurementPen is set to what we want for the
        drawing style.
        """

        if painter.pen() != self.priceMeasurementPen:
            painter.setPen(self.priceMeasurementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the start point horizontal bar part.
        x1 = -1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5)
        y1 = 0.0
        x2 = 1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5)
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the end point horizontal bar part.
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = -1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5)
        y1 = 0.0 + yDelta
        x2 = 1.0 * (self.priceMeasurementGraphicsItemBarWidth * 0.5)
        y2 = 0.0 + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle vertical line.
        x1 = 0.0
        y1 = 0.0
        x2 = 0.0
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each tick area if the flag is
        # set to do so, or if it is selected.
        if self.drawHorizontalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.priceMeasurementPen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the last and first PriceBar's timestamp in local
                # coordinates.
                earliestPriceBar = self.scene().getEarliestPriceBar()
                smallestPriceBarX = \
                    self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
                localSmallestPriceBarX = \
                    self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

                latestPriceBar = self.scene().getLatestPriceBar()
                largestPriceBarX = \
                    self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
                localLargestPriceBarX = \
                    self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
            
                xValues.append(localSmallestPriceBarX)
                xValues.append(localLargestPriceBarX)

                # We have all x values now, so sort them to get the
                # low and high.
                xValues.sort()
                smallestX = xValues[0]
                largestX = xValues[-1]
        
                # Horizontal line at the startPoint.
                localPosY = 0.0
                startPoint = QPointF(largestX, localPosY)
                endPoint = QPointF(smallestX, localPosY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
            
                # Horizontal line at the endPoint.
                localPosY = 0.0 + yDelta
                startPoint = QPointF(largestX, localPosY)
                endPoint = QPointF(smallestX, localPosY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.priceMeasurementPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceMeasurementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceMeasurementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        TimeMeasurementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        

class TimeRetracementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a time retracement in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new TimeRetracementGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger(\
            "pricebarchart.TimeRetracementGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Height of the vertical bar drawn.
        self.timeRetracementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeRetracementTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeRetracementTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextYScaling 

        # Font.
        self.timeRetracementTextFont = QFont()
        self.timeRetracementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeRetracementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeRetracementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultColor

        # TimeRetracementGraphicsItem showFullLinesFlag (bool).
        self.showFullLinesFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowFullLinesFlag
    
        # TimeRetracementGraphicsItem showTimeTextFlag (bool).
        self.showTimeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowTimeTextFlag
    
        # TimeRetracementGraphicsItem showPercentTextFlag (bool).
        self.showPercentTextFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowPercentTextFlag
    
        # TimeRetracementGraphicsItem ratios (bool).
        self.ratios = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemRatios
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTimeRetracementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.timeRetracementPenWidth = 0.0
        self.timeRetracementPen = QPen()
        self.timeRetracementPen.setColor(self.timeRetracementGraphicsItemColor)
        self.timeRetracementPen.setWidthF(self.timeRetracementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Degrees of text rotation.
        self.rotationDegrees = 90.0
        
        # Holds the QGraphicsSimpleTextItems for the texts associated
        # with the ratios.
        self.timeRetracementRatioTimeTexts = []
        self.timeRetracementRatioPercentTexts = []

        # Holds all the above text items, so that settings may be
        # applied more easily.
        self.textItems = []

        # Create the text items and put them in the above lists.
        self._recreateRatioTextItems()
        
        # Flag that indicates that vertical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def _recreateRatioTextItems(self):
        """Re-creates the text items related to the Ratios in
        self.ratios.  This includes making sure there are the correct
        number of them, and making sure their settings are correct, as
        expected.
        """

        # Disable and remove the old text items.
        for textItem in self.textItems:
            textItem.setEnabled(False)
            textItem.setVisible(False)

            if self.scene() != None:
                self.scene().removeItem(textItem)
                
        # Clear out the arrays holding the text items.
        self.textItems = []
        self.timeRetracementRatioTimeTexts = []
        self.timeRetracementRatioPercentTexts = []

        # Recreate the text items for all the ratios.  We recreate
        # them to make sure we have enough items.
        for ratio in self.ratios:
            timeTextItem = QGraphicsSimpleTextItem("", self)
            self.timeRetracementRatioTimeTexts.append(timeTextItem)
            self.textItems.append(timeTextItem)
            
            percentTextItem = QGraphicsSimpleTextItem("", self)
            self.timeRetracementRatioPercentTexts.append(percentTextItem)
            self.textItems.append(percentTextItem)

        # Apply location, and various other settings to the text items.
        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.timeRetracementTextFont)
        
            # Set the pen color of the text.
            self.timeRetracementTextPen = textItem.pen()
            self.timeRetracementTextPen.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setPen(self.timeRetracementTextPen)

            # Set the brush color of the text.
            self.timeRetracementTextBrush = textItem.brush()
            self.timeRetracementTextBrush.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeRetracementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeRetracementTextXScaling, \
                                self.timeRetracementTextYScaling)
            textTransform.rotate(self.rotationDegrees)
            textItem.setTransform(textTransform)

    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.timeRetracementGraphicsItemBarHeight = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeRetracementTextXScaling = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeRetracementTextYScaling = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemTextYScaling 

        # Font.
        self.timeRetracementTextFont = QFont()
        self.timeRetracementTextFont.fromString(\
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeRetracementGraphicsItemTextColor = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeRetracementGraphicsItemColor = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultColor

        # TimeRetracementGraphicsItem showFullLinesFlag (bool).
        self.showFullLinesFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowFullLinesFlag
    
        # TimeRetracementGraphicsItem showTimeTextFlag (bool).
        self.showTimeTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowTimeTextFlag
    
        # TimeRetracementGraphicsItem showPercentTextFlag (bool).
        self.showPercentTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowPercentTextFlag
    
        # TimeRetracementGraphicsItem ratios (bool).
        self.ratios = \
            copy.deepcopy(priceBarChartSettings.\
                          timeRetracementGraphicsItemRatios)
        
        ####################################################################

        # Set the new color of the pen for drawing the bar.
        self.timeRetracementPen.\
            setColor(self.timeRetracementGraphicsItemColor)
        
        # Recreate the text items for the ratios.  This will also
        # apply the new scaling and font, etc. as needed.
        self._recreateRatioTextItems()
        
        # Set the text items as enabled or disabled, visible or
        # invisible, depending on whether the show flag is set.
        for textItem in self.timeRetracementRatioTimeTexts:
            textItem.setEnabled(self.showTimeTextFlag)
            textItem.setVisible(self.showTimeTextFlag)
            
        for textItem in self.timeRetracementRatioPercentTexts:
            textItem.setEnabled(self.showPercentTextFlag)
            textItem.setVisible(self.showPercentTextFlag)

        # Go through all the Ratio objects and disable texts if the
        # Ratios are not enabled.  This will be a second pass-through
        # of settings the text items, but this time, we do not enable
        # them, we only disable them if the corresponding Ratio is disabled.
        for i in range(len(self.ratios)):
            ratio = self.ratios[i]
            
            if not ratio.isEnabled():
                self.timeRetracementRatioTimeTexts[i].setEnabled(False)
                self.timeRetracementRatioTimeTexts[i].setVisible(False)

                self.timeRetracementRatioPercentTexts[i].setEnabled(False)
                self.timeRetracementRatioPercentTexts[i].setVisible(False)

        # Update the timeRetracement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the timeRetracement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the time retracements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateTimeRetracement()

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculateTimeRetracement()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointX <= scenePosX <= startThreshold or \
                   startingPointX >= scenePosX >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointX <= scenePosX <= endThreshold or \
                   endingPointX >= scenePosX >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.setEndPointF(QPointF(self.endPointF.x(),
                                              event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)

                    # Update calculation/text for the retracement.
                    self.recalculateTimeRetracement()
        
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)
            
                    # Update calculation/text for the retracement.
                    self.recalculateTimeRetracement()
        
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the timeRetracement label position.
        
        # X range.  Used in calculations for the X coordinate of the text items.
        deltaX = self.endPointF.x() - self.startPointF.x()

        # Remember, these text items are rotated, so what we are
        # trying to do here is to put the time text to the left of the
        # tick, and the percent text to the right of the tick.
        
        for i in range(len(self.ratios)):
            ratio = self.ratios[i]

            timeTextItem = self.timeRetracementRatioTimeTexts[i]
            percentTextItem = self.timeRetracementRatioPercentTexts[i]

            x = deltaX * ratio.getRatio()
            y = 0
            
            timeTextItem.setPos(QPointF(x, y))

            offset = self.timeRetracementGraphicsItemBarHeight * 10
            x = x + offset

            percentTextItem.setPos(QPointF(x, y))


    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the timeRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timeretracement.
                self.recalculateTimeRetracement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the timeRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timeretracement.
                self.recalculateTimeRetracement()
                self.update()

    def normalizeStartAndEnd(self):
        """Does not do anything since normalization is not applicable
        to this graphics item.
        """

        # Do don't anything.
        pass

    def recalculateTimeRetracement(self):
        """Recalculates the timeRetracement and sets the text items'
        text accordingly.
        """

        scene = self.scene()

        # X range.  Used in calculations for the X coordinate of
        # the text items.
        deltaX = self.endPointF.x() - self.startPointF.x()
        
        if scene != None:
            # Update the text of the internal items.

            for i in range(len(self.ratios)):
                ratio = self.ratios[i]

                timeTextItem = self.timeRetracementRatioTimeTexts[i]
                percentTextItem = self.timeRetracementRatioPercentTexts[i]

                sceneXPos = self.startPointF.x() + (deltaX * ratio.getRatio())
                timestamp = self.scene().sceneXPosToDatetime(sceneXPos)

                # Set texts.
                timeText = "{}".format(Ephemeris.datetimeToDayStr(timestamp))
                percentText = "{:.2f} %".format(ratio.getRatio() * 100)
                
                timeTextItem.setText(timeText)
                percentTextItem.setText(percentText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTimeRetracementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartTimeRetracementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartTimeRetracementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartTimeRetracementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.timeRetracementTextXScaling = self.artifact.getTextXScaling()
        self.timeRetracementTextYScaling = self.artifact.getTextYScaling()
        self.timeRetracementTextFont = self.artifact.getFont()
        self.timeRetracementGraphicsItemTextColor = self.artifact.getTextColor()
        self.timeRetracementPen.setColor(self.artifact.getColor())
        
        self.showFullLinesFlag = self.artifact.getShowFullLinesFlag()
        self.showTimeTextFlag = self.artifact.getShowTimeTextFlag()
        self.showPercentTextFlag = self.artifact.getShowPercentTextFlag()

        self.ratios = self.artifact.getRatios()

        #############

        # Recreate the text items for the ratios.  This will also
        # apply the new scaling and font, etc. as needed.
        self._recreateRatioTextItems()
        
        # Set the text items as enabled or disabled, visible or
        # invisible, depending on whether the show flag is set.
        for textItem in self.timeRetracementRatioTimeTexts:
            textItem.setEnabled(self.showTimeTextFlag)
            textItem.setVisible(self.showTimeTextFlag)
            
        for textItem in self.timeRetracementRatioPercentTexts:
            textItem.setEnabled(self.showPercentTextFlag)
            textItem.setVisible(self.showPercentTextFlag)

        # Go through all the Ratio objects and disable texts if the
        # Ratios are not enabled.  This will be a second pass-through
        # of settings the text items, but this time, we do not enable
        # them, we only disable them if the corresponding Ratio is disabled.
        for i in range(len(self.ratios)):
            ratio = self.ratios[i]
            
            if not ratio.isEnabled():
                self.timeRetracementRatioTimeTexts[i].setEnabled(False)
                self.timeRetracementRatioTimeTexts[i].setVisible(False)

                self.timeRetracementRatioPercentTexts[i].setEnabled(False)
                self.timeRetracementRatioPercentTexts[i].setVisible(False)

        # Update the timeRetracement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the timeRetracement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the time retracements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateTimeRetracement()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTimeRetracementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTimeRetracementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.timeRetracementTextXScaling)
        self.artifact.setTextYScaling(self.timeRetracementTextYScaling)
        self.artifact.setFont(self.timeRetracementTextFont)
        self.artifact.setTextColor(self.timeRetracementGraphicsItemTextColor)
        self.artifact.setColor(self.timeRetracementPen.color())
        
        self.artifact.setShowFullLinesFlag(self.showFullLinesFlag)
        self.artifact.setShowTimeTextFlag(self.showTimeTextFlag)
        self.artifact.setShowPercentTextFlag(self.showPercentTextFlag)

        self.artifact.setRatios(self.ratios)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of the
        # vertical bar that is at startPointF.  If the user created
        # the widget with the startPointF to the right of the
        # endPointF, then the startPointF will have a higher X value
        # than endPointF.

        # The QRectF returned is relative to this (0, 0) point.

        # Bounding box here is the whole area that is painted.  That
        # means we need to take into account whether or not the full
        # lines are painted for the enabled ratios (for the Y height
        # value).  We always include the endPointF, which is the 100%
        # 'retracement'.

        # Get the QRectF with just the lines.

        # Keep track of x and y values so we can get the largest and
        # smallest x and y values.
        xValues = []
        yValues = []
        
        # The left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # The right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # The vertical lines for all the enabled ratios.
        if self.drawVerticalDottedLinesFlag or \
               self.isSelected() or \
               self.showFullLinesFlag == True:

            # Get the highest high, and lowest low PriceBar in local
            # coordinates.
            highestPrice = self.scene().getHighestPriceBar().high
            highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
            localHighY = \
                self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

            lowestPrice = self.scene().getLowestPriceBar().low
            lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
            localLowY = \
                self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()

            yValues.append(localHighY)
            yValues.append(localLowY)

        # Go through the ratios and track the x values for the enabled ratios.
        for ratio in self.ratios:
            if ratio.isEnabled():
                # Calculate the x in local coordinates.
                localX = xDelta * ratio.getRatio()
                xValues.append(localX)
        
        # We have all x and y values now, so sort them to get the
        # low and high.
        xValues.sort()
        yValues.sort()

        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 *
                    (self.timeRetracementGraphicsItemBarHeight * 0.5))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeRetracementGraphicsItemBarHeight * 0.5))

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.timeRetracementPen is set to what we want for the drawing
        style.
        """

        if painter.pen() != self.timeRetracementPen:
            painter.setPen(self.timeRetracementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        x2 = 0.0
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the vertical lines for all the enabled ratios.
        for ratio in self.ratios:
            if ratio.isEnabled():
                localX = xDelta * ratio.getRatio()

                x1 = localX
                y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
                x2 = localX
                y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight * 0.5)
        
                painter.drawLine(QLineF(x1, y1, x2, y2))

                xValues.append(x1)
                xValues.append(x2)
                yValues.append(y1)
                yValues.append(y2)

                # If the full lines flag is enabled, then draw the
                # full length fo the line, from the 0 Y coordinate
                # location to the self.endPointF.y() location, in
                # local coordinates.
                if self.showFullLinesFlag == True:
                    x1 = localX
                    y1 = 0
                    x2 = localX
                    y2 = self.mapFromScene(QPointF(0.0, self.endPointF.y())).y()
        
                    painter.drawLine(QLineF(x1, y1, x2, y2))

                    xValues.append(x1)
                    xValues.append(x2)
                    yValues.append(y1)
                    yValues.append(y2)

        # Draw the middle horizontal line.
        xValues.sort()
        smallestX = xValues[0]
        largestX = xValues[-1]
        
        x1 = smallestX
        y1 = 0.0
        x2 = largestX
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)

        # Draw vertical dotted lines at each enabled tick area if the
        # flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.timeRetracementPen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]

                # Draw the vertical lines for all the enabled ratios.
                xDelta = self.endPointF.x() - self.startPointF.x()
                for ratio in self.ratios:
                    if ratio.isEnabled():
                        x = xDelta * ratio.getRatio()

                        x1 = x
                        y1 = largestY
                        x2 = x
                        y2 = smallestY

                        xValues.append(x1)
                        xValues.append(x2)
                        yValues.append(y1)
                        yValues.append(y2)
                    
                        startPoint = QPointF(x1, y1)
                        endPoint = QPointF(x2, y2)

                        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
                
                        painter.setPen(QPen(option.palette.windowText(), 0,
                                            Qt.DashLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
        
        # Draw the shape if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.timeRetracementPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this TimeRetracementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        TimeRetracementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeRetracementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeRetracementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        TimeRetracementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        TimeRetracementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())


class PriceRetracementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a price retracement in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point width bar, on the start point (bottom part) of the bar ruler.

    That means when a user creates a new PriceRetracementGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger(\
            "pricebarchart.PriceRetracementGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Width of the vertical bar drawn.
        self.priceRetracementGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.priceRetracementTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceRetracementTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextYScaling 

        # Font.
        self.priceRetracementTextFont = QFont()
        self.priceRetracementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceRetracementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceRetracementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultColor

        # PriceRetracementGraphicsItem showFullLinesFlag (bool).
        self.showFullLinesFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowFullLinesFlag
    
        # PriceRetracementGraphicsItem showPriceTextFlag (bool).
        self.showPriceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPriceTextFlag
    
        # PriceRetracementGraphicsItem showPercentTextFlag (bool).
        self.showPercentTextFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPercentTextFlag
    
        # PriceRetracementGraphicsItem ratios (bool).
        self.ratios = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemRatios
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceRetracementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.priceRetracementPenWidth = 0.0
        self.priceRetracementPen = QPen()
        self.priceRetracementPen.\
            setColor(self.priceRetracementGraphicsItemColor)
        self.priceRetracementPen.\
            setWidthF(self.priceRetracementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Degrees of text rotation.
        self.rotationDegrees = 0.0
        
        # Holds the QGraphicsSimpleTextItems for the texts associated
        # with the ratios.
        self.priceRetracementRatioPriceTexts = []
        self.priceRetracementRatioPercentTexts = []

        # Holds all the above text items, so that settings may be
        # applied more easily.
        self.textItems = []

        # Create the text items and put them in the above lists.
        self._recreateRatioTextItems()
        
        # Flag that indicates that horizontal dotted lines should be drawn.
        self.drawHorizontalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def _recreateRatioTextItems(self):
        """Re-creates the text items related to the Ratios in
        self.ratios.  This includes making sure there are the correct
        number of them, and making sure their settings are correct, as
        expected.
        """

        # Disable and remove the old text items.
        for textItem in self.textItems:
            textItem.setEnabled(False)
            textItem.setVisible(False)

            if self.scene() != None:
                self.scene().removeItem(textItem)
                
        # Clear out the arrays holding the text items.
        self.textItems = []
        self.priceRetracementRatioPriceTexts = []
        self.priceRetracementRatioPercentTexts = []

        # Recreate the text items for all the ratios.  We recreate
        # them to make sure we have enough items.
        for ratio in self.ratios:
            priceTextItem = QGraphicsSimpleTextItem("", self)
            self.priceRetracementRatioPriceTexts.append(priceTextItem)
            self.textItems.append(priceTextItem)
            
            percentTextItem = QGraphicsSimpleTextItem("", self)
            self.priceRetracementRatioPercentTexts.append(percentTextItem)
            self.textItems.append(percentTextItem)

        # Apply location, and various other settings to the text items.
        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.priceRetracementTextFont)
        
            # Set the pen color of the text.
            self.priceRetracementTextPen = textItem.pen()
            self.priceRetracementTextPen.\
                setColor(self.priceRetracementGraphicsItemTextColor)
            
            textItem.setPen(self.priceRetracementTextPen)

            # Set the brush color of the text.
            self.priceRetracementTextBrush = textItem.brush()
            self.priceRetracementTextBrush.\
                setColor(self.priceRetracementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceRetracementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceRetracementTextXScaling, \
                                self.priceRetracementTextYScaling)
            textTransform.rotate(self.rotationDegrees)
            textItem.setTransform(textTransform)

    def setDrawHorizontalDottedLinesFlag(self, flag):
        """If flag is set to true, then the horizontal dotted lines are drawn.
        """

        self.drawHorizontalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra horizontal lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Width of the horizontal bar drawn.
        self.priceRetracementGraphicsItemBarWidth = \
            priceBarChartSettings.\
                priceRetracementGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.priceRetracementTextXScaling = \
            priceBarChartSettings.\
                priceRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceRetracementTextYScaling = \
            priceBarChartSettings.\
                priceRetracementGraphicsItemTextYScaling 

        # Font.
        self.priceRetracementTextFont = QFont()
        self.priceRetracementTextFont.fromString(\
            priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceRetracementGraphicsItemTextColor = \
            priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceRetracementGraphicsItemColor = \
            priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultColor

        # PriceRetracementGraphicsItem showFullLinesFlag (bool).
        self.showFullLinesFlag = \
            priceBarChartSettings.\
            priceRetracementGraphicsItemShowFullLinesFlag
    
        # PriceRetracementGraphicsItem showPriceTextFlag (bool).
        self.showPriceTextFlag = \
            priceBarChartSettings.\
            priceRetracementGraphicsItemShowPriceTextFlag
    
        # PriceRetracementGraphicsItem showPercentTextFlag (bool).
        self.showPercentTextFlag = \
            priceBarChartSettings.\
            priceRetracementGraphicsItemShowPercentTextFlag
    
        # PriceRetracementGraphicsItem ratios (bool).
        self.ratios = \
            copy.deepcopy(priceBarChartSettings.\
                          priceRetracementGraphicsItemRatios)
        
        ####################################################################

        # Set the new color of the pen for drawing the bar.
        self.priceRetracementPen.\
            setColor(self.priceRetracementGraphicsItemColor)
        
        # Recreate the text items for the ratios.  This will also
        # apply the new scaling and font, etc. as needed.
        self._recreateRatioTextItems()
        
        # Set the text items as enabled or disabled, visible or
        # invisible, depending on whether the show flag is set.
        for textItem in self.priceRetracementRatioPriceTexts:
            textItem.setEnabled(self.showPriceTextFlag)
            textItem.setVisible(self.showPriceTextFlag)
            
        for textItem in self.priceRetracementRatioPercentTexts:
            textItem.setEnabled(self.showPercentTextFlag)
            textItem.setVisible(self.showPercentTextFlag)

        # Go through all the Ratio objects and disable texts if the
        # Ratios are not enabled.  This will be a second pass-through
        # of settings the text items, but this time, we do not enable
        # them, we only disable them if the corresponding Ratio is disabled.
        for i in range(len(self.ratios)):
            ratio = self.ratios[i]
            
            if not ratio.isEnabled():
                self.priceRetracementRatioPriceTexts[i].setEnabled(False)
                self.priceRetracementRatioPriceTexts[i].setVisible(False)

                self.priceRetracementRatioPercentTexts[i].setEnabled(False)
                self.priceRetracementRatioPercentTexts[i].setVisible(False)

        # Update the priceRetracement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the priceRetracement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the price retracements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculatePriceRetracement()

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculatePriceRetracement()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointY={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointY + (diff * (1.0 / 5))
            endThreshold = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if startingPointY <= scenePosY <= startThreshold or \
                   startingPointY >= scenePosY >= startThreshold:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointY <= scenePosY <= endThreshold or \
                   endingPointY >= scenePosY >= endThreshold:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(self.startPointF.x(),
                                                event.scenePos().y()))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)

                    # Update calculation/text for the retracement.
                    self.recalculatePriceRetracement()
        
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)
            
                    # Update calculation/text for the retracement.
                    self.recalculatePriceRetracement()
        
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the priceRetracement label position.
        
        # Y range.  Used in calculations for the Y coordinate of the text items.
        deltaY = self.endPointF.y() - self.startPointF.y()

        for i in range(len(self.ratios)):
            ratio = self.ratios[i]

            priceTextItem = self.priceRetracementRatioPriceTexts[i]
            percentTextItem = self.priceRetracementRatioPercentTexts[i]

            x = 0
            y = deltaY * ratio.getRatio()
            
            priceTextItem.setPos(QPointF(x, y))

            offset = self.priceRetracementGraphicsItemBarWidth * 0.4
            y = y - offset

            percentTextItem.setPos(QPointF(x, y))


    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the priceRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculatePriceRetracement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the priceRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculatePriceRetracement()
                self.update()

    def normalizeStartAndEnd(self):
        """Does not do anything since normalization is not applicable
        to this graphics item.
        """

        # Do don't anything.
        pass

    def recalculatePriceRetracement(self):
        """Recalculates the priceRetracement and sets the text items'
        text accordingly.
        """

        scene = self.scene()

        # Y range.  Used in calculations for the Y coordinate of
        # the text items.
        deltaY = self.endPointF.y() - self.startPointF.y()
        
        if scene != None:
            # Update the text of the internal items.

            for i in range(len(self.ratios)):
                ratio = self.ratios[i]

                priceTextItem = self.priceRetracementRatioPriceTexts[i]
                percentTextItem = self.priceRetracementRatioPercentTexts[i]

                sceneYPos = self.startPointF.y() + (deltaY * ratio.getRatio())
                price = self.scene().sceneYPosToPrice(sceneYPos)

                # Set texts.
                priceText = "{}".format(price)
                percentText = "{:.2f} %".format(ratio.getRatio() * 100)
                
                priceTextItem.setText(priceText)
                percentTextItem.setText(percentText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceRetracementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartPriceRetracementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartPriceRetracementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartPriceRetracementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.priceRetracementTextXScaling = self.artifact.getTextXScaling()
        self.priceRetracementTextYScaling = self.artifact.getTextYScaling()
        self.priceRetracementTextFont = self.artifact.getFont()
        self.priceRetracementGraphicsItemTextColor = \
            self.artifact.getTextColor()
        self.priceRetracementPen.setColor(self.artifact.getColor())
        
        self.showFullLinesFlag = self.artifact.getShowFullLinesFlag()
        self.showPriceTextFlag = self.artifact.getShowPriceTextFlag()
        self.showPercentTextFlag = self.artifact.getShowPercentTextFlag()

        self.ratios = self.artifact.getRatios()

        #############

        # Recreate the text items for the ratios.  This will also
        # apply the new scaling and font, etc. as needed.
        self._recreateRatioTextItems()
        
        # Set the text items as enabled or disabled, visible or
        # invisible, depending on whether the show flag is set.
        for textItem in self.priceRetracementRatioPriceTexts:
            textItem.setEnabled(self.showPriceTextFlag)
            textItem.setVisible(self.showPriceTextFlag)
            
        for textItem in self.priceRetracementRatioPercentTexts:
            textItem.setEnabled(self.showPercentTextFlag)
            textItem.setVisible(self.showPercentTextFlag)

        # Go through all the Ratio objects and disable texts if the
        # Ratios are not enabled.  This will be a second pass-through
        # of settings the text items, but this time, we do not enable
        # them, we only disable them if the corresponding Ratio is disabled.
        for i in range(len(self.ratios)):
            ratio = self.ratios[i]
            
            if not ratio.isEnabled():
                self.priceRetracementRatioPriceTexts[i].setEnabled(False)
                self.priceRetracementRatioPriceTexts[i].setVisible(False)

                self.priceRetracementRatioPercentTexts[i].setEnabled(False)
                self.priceRetracementRatioPercentTexts[i].setVisible(False)

        # Need to recalculate the priceRetracement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the price retracements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculatePriceRetracement()

        # Update the priceRetracement text item position.
        self._updateTextItemPositions()
            
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartPriceRetracementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceRetracementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.priceRetracementTextXScaling)
        self.artifact.setTextYScaling(self.priceRetracementTextYScaling)
        self.artifact.setFont(self.priceRetracementTextFont)
        self.artifact.setTextColor(self.priceRetracementGraphicsItemTextColor)
        self.artifact.setColor(self.priceRetracementPen.color())
        
        self.artifact.setShowFullLinesFlag(self.showFullLinesFlag)
        self.artifact.setShowPriceTextFlag(self.showPriceTextFlag)
        self.artifact.setShowPercentTextFlag(self.showPercentTextFlag)

        self.artifact.setRatios(self.ratios)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of the
        # horizontal bar that is at startPointF.  If the user created
        # the widget with the startPointF to the right of the
        # endPointF, then the startPointF will have a higher X value
        # than endPointF.

        # The QRectF returned is relative to this (0, 0) point.

        # Bounding box here is the whole area that is painted.  That
        # means we need to take into account whether or not the full
        # lines are painted for the enabled ratios (for the X width
        # value).  We always include the endPointF, which is the 100%
        # 'retracement'.

        # Get the QRectF with just the lines.

        # Keep track of x and y values so we can get the largest and
        # smallest x and y values.
        xValues = []
        yValues = []
        
        # The bottom horizontal bar part.
        x1 = 1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y1 = 0.0
        x2 = -1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y2 = 0.0

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # The top horizontal bar part.
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = 1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y1 = 0.0 + yDelta
        x2 = -1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y2 = 0.0 + yDelta

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # The horizontal lines for all the enabled ratios.
        if self.drawHorizontalDottedLinesFlag or \
               self.isSelected() or \
               self.showFullLinesFlag == True:

            # Get the earliest and latest PriceBar timestamp in local
            # coordinates.
            earliestPriceBar = self.scene().getEarliestPriceBar()
            smallestPriceBarX = \
                self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
            localSmallestPriceBarX = \
                self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()
            
            latestPriceBar = self.scene().getLatestPriceBar()
            largestPriceBarX = \
                self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
            localLargestPriceBarX = \
                self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()


            xValues.append(localSmallestPriceBarX)
            xValues.append(localLargestPriceBarX)

        # Go through the ratios and track the y values for the enabled ratios.
        for ratio in self.ratios:
            if ratio.isEnabled():
                # Calculate the y in local coordinates.
                localY = yDelta * ratio.getRatio()
                yValues.append(localY)
        
        # We have all x and y values now, so sort them to get the
        # low and high.
        xValues.sort()
        yValues.sort()

        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Get the QRectF with just the lines.
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        topLeft = \
            QPointF(-1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5),
                    0.0)
        
        
        bottomRight = \
            QPointF(1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5),
                    yDelta)

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.priceRetracementPen is set to what we want for the
        drawing style.
        """

        if painter.pen() != self.priceRetracementPen:
            painter.setPen(self.priceRetracementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the bottom horizontal bar part.
        x1 = 1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y1 = 0.0
        x2 = -1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the top horizontal bar part.
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = 1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y1 = 0.0 + yDelta
        x2 = -1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
        y2 = 0.0 + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the horizontal lines for all the enabled ratios.
        for ratio in self.ratios:
            if ratio.isEnabled():
                localY = yDelta * ratio.getRatio()

                x1 = 1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
                y1 = localY
                x2 = -1.0 * (self.priceRetracementGraphicsItemBarWidth * 0.5)
                y2 = localY
        
                painter.drawLine(QLineF(x1, y1, x2, y2))

                xValues.append(x1)
                xValues.append(x2)
                yValues.append(y1)
                yValues.append(y2)

                # If the full lines flag is enabled, then draw the
                # full length fo the line, from the 0 Y coordinate
                # location to the self.endPointF.y() location, in
                # local coordinates.
                if self.showFullLinesFlag == True:
                    x1 = 0
                    y1 = localY
                    x2 = self.mapFromScene(QPointF(self.endPointF.x(), 0.0)).x()
                    y2 = localY
        
                    painter.drawLine(QLineF(x1, y1, x2, y2))

                    xValues.append(x1)
                    xValues.append(x2)
                    yValues.append(y1)
                    yValues.append(y2)

        # Draw the middle horizontal line.
        yValues.sort()
        smallestY = yValues[0]
        largestY = yValues[-1]
        
        x1 = 0.0
        y1 = smallestY
        x2 = 0.0
        y2 = largestY
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)

        # Draw horizontal dotted lines at each enabled tick area if the
        # flag is set to do so, or if it is selected.
        if self.drawHorizontalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.priceRetracementPen.widthF() * 0.5;
                penWidth = 0.0
                fgcolor = option.palette.windowText().color()
                # Ensure good contrast against fgcolor.
                r = 255
                g = 255
                b = 255
                if fgcolor.red() > 127:
                    r = 0
                if fgcolor.green() > 127:
                    g = 0
                if fgcolor.blue() > 127:
                    b = 0
                bgcolor = QColor(r, g, b)
    
                # Get the earliest and latest PriceBar timestamp in local
                # coordinates.
                earliestPriceBar = self.scene().getEarliestPriceBar()
                smallestPriceBarX = \
                    self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
                localSmallestPriceBarX = \
                    self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()
            
                latestPriceBar = self.scene().getLatestPriceBar()
                largestPriceBarX = \
                    self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
                localLargestPriceBarX = \
                    self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()

                xValues.append(localLargestPriceBarX)
                xValues.append(localSmallestPriceBarX)

                # We have all x values now, so sort them to get the
                # low and high.
                xValues.sort()
                smallestX = xValues[0]
                largestX = xValues[-1]

                # Draw the horizontal lines for all the enabled ratios.
                yDelta = self.endPointF.y() - self.startPointF.y()
                for ratio in self.ratios:
                    if ratio.isEnabled():
                        y = yDelta * ratio.getRatio()

                        x1 = largestX
                        y1 = y
                        x2 = smallestX
                        y2 = y

                        xValues.append(x1)
                        xValues.append(x2)
                        yValues.append(y1)
                        yValues.append(y2)
                    
                        startPoint = QPointF(x1, y1)
                        endPoint = QPointF(x2, y2)

                        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
                
                        painter.setPen(QPen(option.palette.windowText(), 0,
                                            Qt.DashLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
        
        # Draw the shape if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.priceRetracementPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceRetracementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceRetracementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceRetracementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceRetracementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        PriceRetracementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the PriceRetracementGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        PriceRetracementGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        

class PriceTimeVectorGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a price retracement in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point width bar, on the start point (bottom part) of the bar ruler.

    That means when a user creates a new PriceTimeVectorGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger(\
            "pricebarchart.PriceTimeVectorGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Width of the vertical bar drawn.
        self.priceTimeVectorGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.priceTimeVectorTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceTimeVectorTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemTextYScaling 

        # Font.
        self.priceTimeVectorTextFont = QFont()
        self.priceTimeVectorTextFont.fromString(\
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceTimeVectorGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextColor

        # Color of the item.
        self.priceTimeVectorGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemColor

        # PriceTimeVectorGraphicsItem showDistanceTextFlag (bool).
        self.showDistanceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag
    
        # PriceTimeVectorGraphicsItem showSqrtDistanceTextFlag (bool).
        self.showSqrtDistanceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowSqrtDistanceTextFlag
    
        # PriceTimeVectorGraphicsItem showDistanceScaledValueTextFlag (bool).
        self.showDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag
    
        # PriceTimeVectorGraphicsItem
        # showSqrtDistanceScaledValueTextFlag (bool).
        self.showSqrtDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag
    
        # PriceTimeVectorGraphicsItem tiltedTextFlag (bool).
        self.tiltedTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTiltedTextFlag
    
        # PriceTimeVectorGraphicsItem angleTextFlag (bool).
        self.angleTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemAngleTextFlag
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceTimeVectorArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.priceTimeVectorPenWidth = 0.0
        self.priceTimeVectorPen = QPen()
        self.priceTimeVectorPen.\
            setColor(self.priceTimeVectorGraphicsItemColor)
        self.priceTimeVectorPen.\
            setWidthF(self.priceTimeVectorPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Degrees of text rotation.
        self.rotationDegrees = 0.0

        # Variable holding the distance measurement.
        self.distance = 0.0
        self.sqrtDistance = 0.0
        self.distanceScaledValue = 0.0
        self.sqrtDistanceScaledValue = 0.0
        
        # Internal text item.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(self.endPointF)

        # Transform object applied to the text item.
        self.textTransform = QTransform()

        # Set the text item with the properties we want it to have.
        self.reApplyTextItemAttributes(self.textItem)
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False

        # Working variables for clicking and draging.
        self.clickScenePointF = None
        self.origStartPointF = None

    def reApplyTextItemAttributes(self, textItem):
        """Takes the given text item and reapplies the pen, brush,
        transform, etc. that should be set for the text item.
        """
        
        # Set properties of the text item.
        
        # Set the font of the text.
        textItem.setFont(self.priceTimeVectorTextFont)
        
        # Set the pen color of the text.
        self.priceTimeVectorTextPen = textItem.pen()
        self.priceTimeVectorTextPen.\
            setColor(self.priceTimeVectorGraphicsItemTextColor)
        textItem.setPen(self.priceTimeVectorTextPen)

        # Set the brush color of the text.
        self.priceTimeVectorTextBrush = textItem.brush()
        self.priceTimeVectorTextBrush.\
            setColor(self.priceTimeVectorGraphicsItemTextColor)
        textItem.setBrush(self.priceTimeVectorTextBrush)

        # Apply some size scaling to the text.
        self.textTransform = QTransform()
        self.textTransform.scale(self.priceTimeVectorTextXScaling, \
                                 self.priceTimeVectorTextYScaling)
        textItem.setTransform(self.textTransform)

        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Width of the horizontal bar drawn.
        self.priceTimeVectorGraphicsItemBarWidth = \
            priceBarChartSettings.\
                priceTimeVectorGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.priceTimeVectorTextXScaling = \
            priceBarChartSettings.\
                priceTimeVectorGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceTimeVectorTextYScaling = \
            priceBarChartSettings.\
                priceTimeVectorGraphicsItemTextYScaling 

        # Font.
        self.priceTimeVectorTextFont = QFont()
        self.priceTimeVectorTextFont.fromString(\
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceTimeVectorGraphicsItemTextColor = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemTextColor

        # Color of the item.
        self.priceTimeVectorGraphicsItemColor = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemColor

        # PriceTimeVectorGraphicsItem showDistanceTextFlag (bool).
        self.showDistanceTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemShowDistanceTextFlag
    
        # PriceTimeVectorGraphicsItem showSqrtDistanceTextFlag (bool).
        self.showSqrtDistanceTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag
    
        # PriceTimeVectorGraphicsItem showDistanceScaledValueTextFlag (bool).
        self.showDistanceScaledValueTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag
    
        # PriceTimeVectorGraphicsItem
        # showSqrtDistanceScaledValueTextFlag (bool).
        self.showSqrtDistanceScaledValueTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag
    
        # PriceTimeVectorGraphicsItem tiltedTextFlag (bool).
        self.tiltedTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemTiltedTextFlag

        # PriceTimeVectorGraphicsItem angleTextFlag (bool).
        self.angleTextFlag = \
            priceBarChartSettings.\
            priceTimeVectorGraphicsItemAngleTextFlag

        ####################################################################

        # Set the new color of the pen for drawing the bar.
        self.priceTimeVectorPen.\
            setColor(self.priceTimeVectorGraphicsItemColor)

        # Set the text item with the properties we want it to have.
        self.reApplyTextItemAttributes(self.textItem)
        
        # Need to recalculate the priceTimeVector, since the scaling
        # or start/end points could have changed.  Note, if no scene
        # has been set for the QGraphicsView, then the price
        # retracements will be zero, since it can't look up
        # PriceBarGraphicsItems in the scene.
        self.recalculatePriceTimeVector()

        # Update the priceTimeVector text item position.
        self._updateTextItemPositions()
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculatePriceTimeVector()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointY={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThresholdY = startingPointY + (diff * (1.0 / 5))
            endThresholdY = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThresholdY={}".format(startThresholdY))
            self.log.debug("DEBUG: endThresholdY={}".format(endThresholdY))


            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThresholdX = startingPointX + (diff * (1.0 / 5))
            endThresholdX = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThresholdX={}".format(startThresholdX))
            self.log.debug("DEBUG: endThresholdX={}".format(endThresholdX))


            if startingPointY <= scenePosY <= startThresholdY or \
                   startingPointY >= scenePosY >= startThresholdY or \
                   startingPointX <= scenePosX <= startThresholdX or \
                   startingPointX >= scenePosX >= startThresholdX:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointY <= scenePosY <= endThresholdY or \
                     endingPointY >= scenePosY >= endThresholdY or \
                     endingPointX <= scenePosX <= endThresholdX or \
                     endingPointX >= scenePosX >= endThresholdX:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                self.origStartPointF = QPointF(self.startPointF)
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)

                    # For some reason, setPos() is not getting called
                    # until after the user releases the mouse button
                    # after dragging.  So here we will calculate the
                    # change ourselves and call setPos ourselves so
                    # that the item is drawn correctly.
                    delta = event.scenePos() - self.clickScenePointF
                    if delta.x() != 0.0 and delta.y() != 0.0:
                        newPos = self.origStartPointF + delta
                        self.setPos(newPos)
                    
                    # Calculate Update calculation/text for the
                    # retracement.
                    self.recalculatePriceTimeVector()

                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.origStartPointF + delta
                    self.setPos(newPos)
            
                    # Update calculation/text for the retracement.
                    self.recalculatePriceTimeVector()
        
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def refreshItem(self):
        """Refreshes the item by recalculating and updating the text
        position/rotation.
        """

        self.recalculatePriceTimeVector()
        
        self._updateTextItemPositions()
        
    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the priceTimeVector label position.
        
        # X and Y range.  Used in calculations for the Y coordinate of
        # the text items.
        deltaY = self.endPointF.y() - self.startPointF.y()
        deltaX = self.endPointF.x() - self.startPointF.x()

        self.log.debug("deltaY = {}".format(deltaY))
        self.log.debug("deltaX = {}".format(deltaX))
        
        # Get bounding rectangles of text items.
        boundingRect = self.textItem.boundingRect()

        # Find largest text height and width.
        largestTextHeight = boundingRect.height()
        largestTextWidth = boundingRect.width()

        # Now replace the above with the scaled version of it. 
        largestTextHeight = largestTextHeight * self.textTransform.m22()
        largestTextWidth = largestTextWidth * self.textTransform.m11()

        self.log.debug("largestTextHeight = {}".format(largestTextHeight))
        self.log.debug("largestTextWidth = {}".format(largestTextWidth))
        
        # Get the x and y of the point to place the text, referenced
        # on the line from start point to end point, but offset by a
        # certain amount such that the largest text would be centered
        # on the line.
        midX = self.mapFromScene(\
            QPointF(self.startPointF.x() + (deltaX * 0.5), 0.0)).x()
        midY = self.mapFromScene(\
            QPointF(0.0, self.startPointF.y() + (deltaY * 0.5))).y()

        self.log.debug("midX={}, midY={}".format(midX, midY))
                       
        if self.tiltedTextFlag == True:
            # Utilize scaling of the graphics view for angle
            # calculations (if available).
            scaling = PriceBarChartScaling()
            if self.scene() != None:
                scaling = self.scene().getScaling()

            viewScaledStartPoint = \
                QPointF(self.startPointF.x() * scaling.getViewScalingX(),
                        self.startPointF.y() * scaling.getViewScalingY())
            viewScaledEndPoint = \
                QPointF(self.endPointF.x() * scaling.getViewScalingX(),
                        self.endPointF.y() * scaling.getViewScalingY())
            
            angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
            self.log.debug("angleDeg={}".format(angleDeg))

            # Normalize the angle so that the text is always upright.
            self.rotationDegrees = angleDeg
            if 90 <= self.rotationDegrees <= 270:
                self.rotationDegrees += 180
            self.rotationDegrees = \
                Util.toNormalizedAngle(self.rotationDegrees)

            # Fudge factor since for some reason the text item doesn't
            # exactly line up with the PTV line.
            fudge = 0.0
            if 0 < self.rotationDegrees <= 90:
                self.log.debug("0 to 90")
                removed = 45 - abs(45 - self.rotationDegrees)
                fudge = removed * 0.19
                self.rotationDegrees -= fudge
            elif 90 < self.rotationDegrees <= 180:
                self.log.debug("90 to 180")
                removed = 45 - abs(135 - self.rotationDegrees)
                fudge = removed * 0.12
                self.rotationDegrees += fudge
            elif 180 < self.rotationDegrees <= 270:
                self.log.debug("180 to 270")
                removed = 45 - abs(225 - self.rotationDegrees)
                fudge = removed * 0.19
                self.rotationDegrees -= fudge
            elif 270 < self.rotationDegrees <= 360:
                self.log.debug("270 to 360")
                removed = 45 - abs(315 - self.rotationDegrees)
                fudge = removed * 0.12
                self.rotationDegrees += fudge
            
            self.rotationDegrees = -1.0 * self.rotationDegrees
            self.log.debug("rotationDegrees={}".format(self.rotationDegrees))

            startX = midX
            startY = midY

            self.log.debug("startX={}, startY={}".format(startX, startY))
            
            self.textItem.setPos(QPointF(startX, startY))
            self.textItem.setRotation(self.rotationDegrees)
        else:
            startX = midX
            startY = midY

            # Amount to mutiply to get a largest offset from startY.
            offsetY = largestTextHeight

            x = startX
            y = startY - offsetY
            
            self.textItem.setPos(QPointF(x, y))


    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculatePriceTimeVector()
                self.update()
                
            # Update the priceTimeVector text item position.
            self._updateTextItemPositions()
            
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculatePriceTimeVector()
                self.update()

            # Update the priceTimeVector text item position.
            self._updateTextItemPositions()
            
    def normalizeStartAndEnd(self):
        """Does not do anything since normalization is not applicable
        to this graphics item.
        """

        # Do don't anything.
        pass

    def recalculatePriceTimeVector(self):
        """Recalculates the priceTimeVector and sets the text items'
        text accordingly.
        """

        scene = self.scene()

        # X and Y range.
        deltaY = self.endPointF.y() - self.startPointF.y()
        deltaX = self.endPointF.x() - self.startPointF.x()

        # Text to set in the text item.
        text = ""
        
        if scene != None:
            # Calculate the values for the PriceTimeVector.
            line = QLineF(self.startPointF, self.endPointF)
            self.distance = abs(line.length())
            self.sqrtDistance = math.pow(self.distance, 0.5)

            scaledValueLine = \
                QLineF(scene.convertScenePointToScaledPoint(self.startPointF),
                       scene.convertScenePointToScaledPoint(self.endPointF))
            self.distanceScaledValue = abs(scaledValueLine.length())
            self.sqrtDistanceScaledValue = \
                math.pow(self.distanceScaledValue, 0.5)
            
            # Append text.
            if self.showDistanceTextFlag == True:
                text += "d={:.4f}".\
                    format(self.distance) + os.linesep
            if self.showSqrtDistanceTextFlag == True:
                text += "sqrt(d)={:.4f}".\
                    format(self.sqrtDistance) + os.linesep
            if self.showDistanceScaledValueTextFlag == True:
                text += "d_u={:.4f}".\
                    format(self.distanceScaledValue) + os.linesep
            if self.showSqrtDistanceScaledValueTextFlag == True:
                text += "sqrt(d_u)={:.4f}".\
                    format(self.sqrtDistanceScaledValue) + os.linesep
            if self.angleTextFlag == True:
                # Subtract from 30 since the angle given is in the
                # opposite rotational direction from what we want to
                # display it as.
                angle = 360.0 - scaledValueLine.angle()

                # Show downward angles as negative instead of from 270 to 360.
                if 270.0 <= angle < 360.0:
                    angle -= 360.0

                # Text as the scaled angle.
                text += "{:.4f} deg".format(angle) + os.linesep
        else:
            # No scene, so keep text empty.
            text = ""

        text = text.rstrip()
        self.textItem.setText(text)
        self.prepareGeometryChange()
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceTimeVectorArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartPriceTimeVectorArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartPriceTimeVectorArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartPriceTimeVectorArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.priceTimeVectorTextXScaling = self.artifact.getTextXScaling()
        self.priceTimeVectorTextYScaling = self.artifact.getTextYScaling()
        self.priceTimeVectorTextFont = self.artifact.getFont()
        self.priceTimeVectorGraphicsItemTextColor = \
            self.artifact.getTextColor()
        self.priceTimeVectorPen.setColor(self.artifact.getColor())
        
        self.showDistanceTextFlag = \
            self.artifact.getShowDistanceTextFlag()
        self.showSqrtDistanceTextFlag = \
            self.artifact.getShowSqrtDistanceTextFlag()
        self.showDistanceScaledValueTextFlag = \
            self.artifact.getShowDistanceScaledValueTextFlag()
        self.showSqrtDistanceScaledValueTextFlag = \
            self.artifact.getShowSqrtDistanceScaledValueTextFlag()
        self.tiltedTextFlag = self.artifact.getTiltedTextFlag()
        self.angleTextFlag = self.artifact.getAngleTextFlag()

        #############

        # Set the position.
        self.textItem.setPos(self.endPointF)

        # Apply current attributes like color, brush, etc.
        self.reApplyTextItemAttributes(self.textItem)

        # Need to recalculate the priceTimeVector, since the scaling
        # or start/end points may have changed.  Note, if no scene has
        # been set for the QGraphicsView, then the price retracements
        # will be zero, since it can't look up PriceBarGraphicsItems
        # in the scene.
        self.recalculatePriceTimeVector()

        # Update the priceTimeVector text item position.
        self._updateTextItemPositions()
        
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartPriceTimeVectorArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceTimeVectorArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)

        self.artifact.setTextXScaling(self.priceTimeVectorTextXScaling)
        self.artifact.setTextYScaling(self.priceTimeVectorTextYScaling)
        self.artifact.setFont(self.priceTimeVectorTextFont)
        self.artifact.setTextColor(self.priceTimeVectorGraphicsItemTextColor)
        self.artifact.setColor(self.priceTimeVectorPen.color())
        
        self.artifact.setShowDistanceTextFlag(self.showDistanceTextFlag)
        self.artifact.setShowSqrtDistanceTextFlag(self.showSqrtDistanceTextFlag)
        self.artifact.setShowDistanceScaledValueTextFlag(\
            self.showDistanceScaledValueTextFlag)
        self.artifact.setShowSqrtDistanceScaledValueTextFlag(\
            self.showSqrtDistanceScaledValueTextFlag)
        self.artifact.setTiltedTextFlag(self.tiltedTextFlag)
        self.artifact.setAngleTextFlag(self.angleTextFlag)

        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the startPointF.
        # If the user created the widget with the startPointF to the
        # right of the endPointF, then the startPointF will have a
        # higher X value than endPointF.

        # The QRectF returned is relative to this (0, 0) point.

        textItemRectTopLeft = \
            self.textItem.mapToParent(\
            self.textItem.boundingRect().topLeft())
        textItemRectBottomRight = \
            self.textItem.mapToParent(\
            self.textItem.boundingRect().bottomRight())
        
        rv = self.shape().boundingRect() | \
             QRectF(textItemRectTopLeft, textItemRectBottomRight)
        
        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Calculate the points that would be the selection box area
        # around the line.

        # Start and end points in local coordinates.
        localStartPointF = self.mapFromScene(self.startPointF)
        localEndPointF = self.mapFromScene(self.endPointF)

        # Utilize scaling from the scene if it is available.
        scaling = PriceBarChartScaling()
        if self.scene() != None:
            scaling = self.scene().getScaling()
            
        viewScaledStartPoint = \
            QPointF(self.startPointF.x() * scaling.getViewScalingX(),
                    self.startPointF.y() * scaling.getViewScalingY())
        viewScaledEndPoint = \
            QPointF(self.endPointF.x() * scaling.getViewScalingX(),
                    self.endPointF.y() * scaling.getViewScalingY())

        # Here we are calculating the angle of the text and the line
        # as the user would see it.  Actual angle is different if we
        # are calculating it from a scene perspective.
        angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
        angleRad = math.radians(angleDeg)

        shiftX = math.cos(angleRad) * \
                     (0.5 * self.priceTimeVectorGraphicsItemBarWidth)
        shiftY = math.sin(angleRad) * \
                     (0.5 * self.priceTimeVectorGraphicsItemBarWidth)

        # Create new points.
        p1 = \
            QPointF(localStartPointF.x() - shiftX,
                    localStartPointF.y() - shiftY)
        p2 = \
            QPointF(localStartPointF.x() + shiftX,
                    localStartPointF.y() + shiftY)
        p3 = \
            QPointF(localEndPointF.x() - shiftX,
                    localEndPointF.y() - shiftY)
        p4 = \
            QPointF(localEndPointF.x() + shiftX,
                    localEndPointF.y() + shiftY)

        points = [p2, p1, p3, p4, p2]
        polygon = QPolygonF(points)

        painterPath = QPainterPath()
        painterPath.addPolygon(polygon)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that
        self.priceTimeVectorPen is set to what we want for the drawing
        style.
        """

        self.log.debug("PriceTimeVectorGraphicsItem.paint()")
        
        if painter.pen() != self.priceTimeVectorPen:
            painter.setPen(self.priceTimeVectorPen)
        
        # Draw the line.
        localStartPointF = self.mapFromScene(self.startPointF)
        localEndPointF = self.mapFromScene(self.endPointF)
        painter.drawLine(QLineF(localStartPointF, localEndPointF))
        
        # Draw the shape if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.priceTimeVectorPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceTimeVectorGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceTimeVectorGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceTimeVectorArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceTimeVectorArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        PriceTimeVectorGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the PriceTimeVectorGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        PriceTimeVectorGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        

class LineSegmentGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a price retracement in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point width bar, on the start point (bottom part) of the bar ruler.

    That means when a user creates a new LineSegmentGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger(\
            "pricebarchart.LineSegmentGraphicsItem")
        
        self.log.debug("Entered __init__().")

        # Constant value for the multiple amount to extend the start
        # or end points.  This shows up in the right-click context
        # menu option for extending the start or end points.
        self.extendMultiple = 1.6
        
        ############################################################
        # Set default values for preferences/settings.
        
        # Width of the vertical bar drawn.
        self.lineSegmentGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.lineSegmentTextXScaling = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.lineSegmentTextYScaling = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemTextYScaling 

        # Font.
        self.lineSegmentTextFont = QFont()
        self.lineSegmentTextFont.fromString(\
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.lineSegmentGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextColor

        # Color of the item.
        self.lineSegmentGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemColor

        # LineSegmentGraphicsItem tiltedTextFlag (bool).
        self.tiltedTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTiltedTextFlag
    
        # LineSegmentGraphicsItem angleTextFlag (bool).
        self.angleTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemAngleTextFlag
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartLineSegmentArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.lineSegmentPenWidth = 0.0
        self.lineSegmentPen = QPen()
        self.lineSegmentPen.\
            setColor(self.lineSegmentGraphicsItemColor)
        self.lineSegmentPen.\
            setWidthF(self.lineSegmentPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Degrees of text rotation.
        self.rotationDegrees = 0.0

        # Internal text item.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(self.endPointF)

        # Transform object applied to the text item.
        self.textTransform = QTransform()

        # Set the text item with the properties we want it to have.
        self.reApplyTextItemAttributes(self.textItem)
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False

        # Working variables for clicking and draging.
        self.clickScenePointF = None
        self.origStartPointF = None

    def reApplyTextItemAttributes(self, textItem):
        """Takes the given text item and reapplies the pen, brush,
        transform, etc. that should be set for the text item.
        """
        
        # Set properties of the text item.
        
        # Set the font of the text.
        textItem.setFont(self.lineSegmentTextFont)
        
        # Set the pen color of the text.
        self.lineSegmentTextPen = textItem.pen()
        self.lineSegmentTextPen.\
            setColor(self.lineSegmentGraphicsItemTextColor)
        textItem.setPen(self.lineSegmentTextPen)

        # Set the brush color of the text.
        self.lineSegmentTextBrush = textItem.brush()
        self.lineSegmentTextBrush.\
            setColor(self.lineSegmentGraphicsItemTextColor)
        textItem.setBrush(self.lineSegmentTextBrush)

        # Apply some size scaling to the text.
        self.textTransform = QTransform()
        self.textTransform.scale(self.lineSegmentTextXScaling, \
                                 self.lineSegmentTextYScaling)
        textItem.setTransform(self.textTransform)

        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Width of the horizontal bar drawn.
        self.lineSegmentGraphicsItemBarWidth = \
            priceBarChartSettings.\
                lineSegmentGraphicsItemBarWidth 
 
        # X scaling of the text.
        self.lineSegmentTextXScaling = \
            priceBarChartSettings.\
                lineSegmentGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.lineSegmentTextYScaling = \
            priceBarChartSettings.\
                lineSegmentGraphicsItemTextYScaling 

        # Font.
        self.lineSegmentTextFont = QFont()
        self.lineSegmentTextFont.fromString(\
            priceBarChartSettings.\
            lineSegmentGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.lineSegmentGraphicsItemTextColor = \
            priceBarChartSettings.\
            lineSegmentGraphicsItemTextColor

        # Color of the item.
        self.lineSegmentGraphicsItemColor = \
            priceBarChartSettings.\
            lineSegmentGraphicsItemColor

        # LineSegmentGraphicsItem tiltedTextFlag (bool).
        self.tiltedTextFlag = \
            priceBarChartSettings.\
            lineSegmentGraphicsItemTiltedTextFlag

        # LineSegmentGraphicsItem angleTextFlag (bool).
        self.angleTextFlag = \
            priceBarChartSettings.\
            lineSegmentGraphicsItemAngleTextFlag

        ####################################################################

        # Set the new color of the pen for drawing the bar.
        self.lineSegmentPen.\
            setColor(self.lineSegmentGraphicsItemColor)

        # Set the text item with the properties we want it to have.
        self.reApplyTextItemAttributes(self.textItem)
        
        # Need to recalculate the lineSegment, since the scaling
        # or start/end points could have changed.  Note, if no scene
        # has been set for the QGraphicsView, then the price
        # retracements will be zero, since it can't look up
        # PriceBarGraphicsItems in the scene.
        self.recalculateLineSegment()

        # Update the lineSegment text item position.
        self._updateTextItemPositions()
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings.
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculateLineSegment()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointY={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThresholdY = startingPointY + (diff * (1.0 / 5))
            endThresholdY = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThresholdY={}".format(startThresholdY))
            self.log.debug("DEBUG: endThresholdY={}".format(endThresholdY))


            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThresholdX = startingPointX + (diff * (1.0 / 5))
            endThresholdX = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThresholdX={}".format(startThresholdX))
            self.log.debug("DEBUG: endThresholdX={}".format(endThresholdX))


            if startingPointY <= scenePosY <= startThresholdY or \
                   startingPointY >= scenePosY >= startThresholdY or \
                   startingPointX <= scenePosX <= startThresholdX or \
                   startingPointX >= scenePosX >= startThresholdX:
                
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
                
            elif endingPointY <= scenePosY <= endThresholdY or \
                     endingPointY >= scenePosY >= endThresholdY or \
                     endingPointX <= scenePosX <= endThresholdX or \
                     endingPointX >= scenePosX >= endThresholdX:
                
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                self.origStartPointF = QPointF(self.startPointF)
                
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True:
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)

                    # For some reason, setPos() is not getting called
                    # until after the user releases the mouse button
                    # after dragging.  So here we will calculate the
                    # change ourselves and call setPos ourselves so
                    # that the item is drawn correctly.
                    delta = event.scenePos() - self.clickScenePointF
                    if delta.x() != 0.0 and delta.y() != 0.0:
                        newPos = self.origStartPointF + delta
                        self.setPos(newPos)
                    
                    # Calculate Update calculation/text for the
                    # retracement.
                    self.recalculateLineSegment()

                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.origStartPointF + delta
                    self.setPos(newPos)
            
                    # Update calculation/text for the retracement.
                    self.recalculateLineSegment()
        
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def refreshItem(self):
        """Refreshes the item by recalculating and updating the text
        position/rotation.
        """

        self.recalculateLineSegment()
        
        self._updateTextItemPositions()
        
    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the lineSegment label position.
        
        # X and Y range.  Used in calculations for the Y coordinate of
        # the text items.
        deltaY = self.endPointF.y() - self.startPointF.y()
        deltaX = self.endPointF.x() - self.startPointF.x()

        self.log.debug("deltaY = {}".format(deltaY))
        self.log.debug("deltaX = {}".format(deltaX))
        
        # Get bounding rectangles of text items.
        boundingRect = self.textItem.boundingRect()

        # Find largest text height and width.
        largestTextHeight = boundingRect.height()
        largestTextWidth = boundingRect.width()

        # Now replace the above with the scaled version of it. 
        largestTextHeight = largestTextHeight * self.textTransform.m22()
        largestTextWidth = largestTextWidth * self.textTransform.m11()

        self.log.debug("largestTextHeight = {}".format(largestTextHeight))
        self.log.debug("largestTextWidth = {}".format(largestTextWidth))
        
        # Get the x and y of the point to place the text, referenced
        # on the line from start point to end point, but offset by a
        # certain amount such that the largest text would be centered
        # on the line.
        midX = self.mapFromScene(\
            QPointF(self.startPointF.x() + (deltaX * 0.5), 0.0)).x()
        midY = self.mapFromScene(\
            QPointF(0.0, self.startPointF.y() + (deltaY * 0.5))).y()

        self.log.debug("midX={}, midY={}".format(midX, midY))
                       
        if self.tiltedTextFlag == True:
            # Utilize scaling of the graphics view for angle
            # calculations (if available).
            scaling = PriceBarChartScaling()
            if self.scene() != None:
                scaling = self.scene().getScaling()

            viewScaledStartPoint = \
                QPointF(self.startPointF.x() * scaling.getViewScalingX(),
                        self.startPointF.y() * scaling.getViewScalingY())
            viewScaledEndPoint = \
                QPointF(self.endPointF.x() * scaling.getViewScalingX(),
                        self.endPointF.y() * scaling.getViewScalingY())
            
            angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
            self.log.debug("angleDeg={}".format(angleDeg))

            # Normalize the angle so that the text is always upright.
            self.rotationDegrees = angleDeg
            if 90 <= self.rotationDegrees <= 270:
                self.rotationDegrees += 180
            self.rotationDegrees = \
                Util.toNormalizedAngle(self.rotationDegrees)

            # Fudge factor since for some reason the text item doesn't
            # exactly line up with the PTV line.
            fudge = 0.0
            if 0 < self.rotationDegrees <= 90:
                self.log.debug("0 to 90")
                removed = 45 - abs(45 - self.rotationDegrees)
                fudge = removed * 0.19
                self.rotationDegrees -= fudge
            elif 90 < self.rotationDegrees <= 180:
                self.log.debug("90 to 180")
                removed = 45 - abs(135 - self.rotationDegrees)
                fudge = removed * 0.12
                self.rotationDegrees += fudge
            elif 180 < self.rotationDegrees <= 270:
                self.log.debug("180 to 270")
                removed = 45 - abs(225 - self.rotationDegrees)
                fudge = removed * 0.19
                self.rotationDegrees -= fudge
            elif 270 < self.rotationDegrees <= 360:
                self.log.debug("270 to 360")
                removed = 45 - abs(315 - self.rotationDegrees)
                fudge = removed * 0.12
                self.rotationDegrees += fudge
            
            self.rotationDegrees = -1.0 * self.rotationDegrees
            self.log.debug("rotationDegrees={}".format(self.rotationDegrees))

            startX = midX
            startY = midY

            self.log.debug("startX={}, startY={}".format(startX, startY))
            
            self.textItem.setPos(QPointF(startX, startY))
            self.textItem.setRotation(self.rotationDegrees)
        else:
            startX = midX
            startY = midY

            # Amount to mutiply to get a largest offset from startY.
            offsetY = largestTextHeight

            x = startX
            y = startY - offsetY
            
            self.textItem.setPos(QPointF(x, y))


    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculateLineSegment()
                self.update()
                
            # Update the lineSegment text item position.
            self._updateTextItemPositions()
            
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        newValue = QPointF(pointF.x(), pointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            if self.scene() != None:
                # Re-calculate the priceretracement.
                self.recalculateLineSegment()
                self.update()

            # Update the lineSegment text item position.
            self._updateTextItemPositions()
            
    def normalizeStartAndEnd(self):
        """Does not do anything since normalization is not applicable
        to this graphics item.
        """

        # Do don't anything.
        pass

    def recalculateLineSegment(self):
        """Recalculates the lineSegment and sets the text items'
        text accordingly.
        """

        scene = self.scene()

        # X and Y range.
        deltaY = self.endPointF.y() - self.startPointF.y()
        deltaX = self.endPointF.x() - self.startPointF.x()

        # Text to set in the text item.
        text = ""
        
        if scene != None:
            # Calculate the angle for the scaled LineSegment.
            scaledValueLine = \
                QLineF(scene.convertScenePointToScaledPoint(self.startPointF),
                       scene.convertScenePointToScaledPoint(self.endPointF))
            
            # Set the text.
            if self.angleTextFlag == True:
                # Subtract from 30 since the angle given is in the
                # opposite rotational direction from what we want to
                # display it as.
                angle = 360.0 - scaledValueLine.angle()

                # Show downward angles as negative instead of from 270 to 360.
                if 270.0 <= angle < 360.0:
                    angle -= 360.0

                # Text as the scaled angle.
                text += "{:.4f} deg".format(angle) + os.linesep
        else:
            # No scene, so keep text empty.
            text = ""

        text = text.rstrip()
        self.textItem.setText(text)
        self.prepareGeometryChange()
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartLineSegmentArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartLineSegmentArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartLineSegmentArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartLineSegmentArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.lineSegmentTextXScaling = self.artifact.getTextXScaling()
        self.lineSegmentTextYScaling = self.artifact.getTextYScaling()
        self.lineSegmentTextFont = self.artifact.getFont()
        self.lineSegmentGraphicsItemTextColor = \
            self.artifact.getTextColor()
        self.lineSegmentPen.setColor(self.artifact.getColor())
        
        self.tiltedTextFlag = self.artifact.getTiltedTextFlag()
        self.angleTextFlag = self.artifact.getAngleTextFlag()

        #############

        # Set the position.
        self.textItem.setPos(self.endPointF)

        # Apply current attributes like color, brush, etc.
        self.reApplyTextItemAttributes(self.textItem)

        # Need to recalculate the lineSegment, since the scaling
        # or start/end points may have changed.  Note, if no scene has
        # been set for the QGraphicsView, then the price retracements
        # will be zero, since it can't look up PriceBarGraphicsItems
        # in the scene.
        self.recalculateLineSegment()

        # Update the lineSegment text item position.
        self._updateTextItemPositions()
        
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartLineSegmentArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartLineSegmentArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)

        self.artifact.setTextXScaling(self.lineSegmentTextXScaling)
        self.artifact.setTextYScaling(self.lineSegmentTextYScaling)
        self.artifact.setFont(self.lineSegmentTextFont)
        self.artifact.setTextColor(self.lineSegmentGraphicsItemTextColor)
        self.artifact.setColor(self.lineSegmentPen.color())
        
        self.artifact.setTiltedTextFlag(self.tiltedTextFlag)
        self.artifact.setAngleTextFlag(self.angleTextFlag)

        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the startPointF.
        # If the user created the widget with the startPointF to the
        # right of the endPointF, then the startPointF will have a
        # higher X value than endPointF.

        # The QRectF returned is relative to this (0, 0) point.

        textItemRectTopLeft = \
            self.textItem.mapToParent(\
            self.textItem.boundingRect().topLeft())
        textItemRectBottomRight = \
            self.textItem.mapToParent(\
            self.textItem.boundingRect().bottomRight())
                                
        rv = self.shape().boundingRect() | \
             QRectF(textItemRectTopLeft, textItemRectBottomRight)

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem.
        """

        # Calculate the points that would be the selection box area
        # around the line.

        # Start and end points in local coordinates.
        localStartPointF = self.mapFromScene(self.startPointF)
        localEndPointF = self.mapFromScene(self.endPointF)

        # Utilize scaling from the scene if it is available.
        scaling = PriceBarChartScaling()
        if self.scene() != None:
            scaling = self.scene().getScaling()
            
        viewScaledStartPoint = \
            QPointF(self.startPointF.x() * scaling.getViewScalingX(),
                    self.startPointF.y() * scaling.getViewScalingY())
        viewScaledEndPoint = \
            QPointF(self.endPointF.x() * scaling.getViewScalingX(),
                    self.endPointF.y() * scaling.getViewScalingY())

        # Here we are calculating the angle of the text and the line
        # as the user would see it.  Actual angle is different if we
        # are calculating it from a scene perspective.
        angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
        angleRad = math.radians(angleDeg)
        
        shiftX = math.cos(angleRad) * \
                     (0.5 * self.lineSegmentGraphicsItemBarWidth)
        shiftY = math.sin(angleRad) * \
                     (0.5 * self.lineSegmentGraphicsItemBarWidth)

        # Create new points.
        p1 = \
            QPointF(localStartPointF.x() - shiftX,
                    localStartPointF.y() - shiftY)
        p2 = \
            QPointF(localStartPointF.x() + shiftX,
                    localStartPointF.y() + shiftY)
        p3 = \
            QPointF(localEndPointF.x() - shiftX,
                    localEndPointF.y() - shiftY)
        p4 = \
            QPointF(localEndPointF.x() + shiftX,
                    localEndPointF.y() + shiftY)

        points = [p2, p1, p3, p4, p2]
        polygon = QPolygonF(points)

        painterPath = QPainterPath()
        painterPath.addPolygon(polygon)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.lineSegmentPen is set
        to what we want for the drawing style.
        """

        self.log.debug("LineSegmentGraphicsItem.paint()")
        
        if painter.pen() != self.lineSegmentPen:
            painter.setPen(self.lineSegmentPen)
        
        # Draw the line.
        localStartPointF = self.mapFromScene(self.startPointF)
        localEndPointF = self.mapFromScene(self.endPointF)
        painter.drawLine(QLineF(localStartPointF, localEndPointF))
        
        # Draw the shape if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.lineSegmentPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this LineSegmentGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        LineSegmentGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        extendStartPointAction = \
            QAction("Ex&tend start point {}-fold".\
                    format(self.extendMultiple), parent)
        extendEndPointAction = \
            QAction("E&xtend end point by {}-fold".\
                    format(self.extendMultiple), parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        openStartInJHoraAction = \
            QAction("Open JHor&a with start timestamp", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        openEndInJHoraAction = \
            QAction("Open JHora with end timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        extendStartPointAction.triggered.\
            connect(self._handleExtendStartPointAction)
        extendEndPointAction.triggered.\
            connect(self._handleExtendEndPointAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        openEndInJHoraAction.triggered.\
            connect(self._handleOpenEndInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        extendStartPointAction.setEnabled(not readOnlyMode)
        extendEndPointAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)
        openEndInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(extendStartPointAction)
        menu.addAction(extendEndPointAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)
        menu.addAction(openEndInJHoraAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartLineSegmentArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartLineSegmentArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleExtendStartPointAction(self):
        """Updates the QGraphicsItem so that the start point is a
        self.extendMultiple of the current distance away from end
        point.  The artifact is edited too to correspond with this change.
        """

        # Get the X and Y deltas between the start and end points.
        deltaX = self.endPointF.x() - self.startPointF.x()
        deltaY = self.endPointF.y() - self.startPointF.y()

        # Calculate the new offsets from the end point.
        offsetX = deltaX * self.extendMultiple
        offsetY = deltaY * self.extendMultiple

        # Calculate new start point X and Y values.
        newStartPointX = self.endPointF.x() - offsetX
        newStartPointY = self.endPointF.y() - offsetY

        # Update the QGraphicsItem manually.
        newStartPointF = QPointF(newStartPointX, newStartPointY)
        
        # Call the parent version for setPos(), not the self version
        # because the self version moves both the start and end
        # points.  We want to keep the end point the same.
        super().setPos(newStartPointF)
        self.startPointF = newStartPointF
        
        # Update the artifact.
        self.artifact.setPos(self.startPointF)
        self.artifact.setStartPointF(self.startPointF)

        # Refresh the item so that the textItem and drawing can be updated.
        self.refreshItem()

        # Emit that the chart has changed.
        self.scene().priceBarChartChanged.emit()
        
    def _handleExtendEndPointAction(self):
        """Updates the QGraphicsItem so that the end point is a
        self.extendMultiple of the current distance away from start
        point.  The artifact is edited too to correspond with this change.
        """

        # Get the X and Y deltas between the start and end points.
        deltaX = self.endPointF.x() - self.startPointF.x()
        deltaY = self.endPointF.y() - self.startPointF.y()

        # Calculate the new offsets from the end point.
        offsetX = deltaX * self.extendMultiple
        offsetY = deltaY * self.extendMultiple

        # Calculate new end point X and Y values.
        newEndPointX = self.startPointF.x() + offsetX
        newEndPointY = self.startPointF.y() + offsetY

        # Update the QGraphicsItem manually.
        newEndPointF = QPointF(newEndPointX, newEndPointY)
        self.setEndPointF(newEndPointF)
        
        # Update the artifact.
        self.artifact.setEndPointF(newEndPointF)
        
        # Refresh the item so that the textItem and drawing can be updated.
        self.refreshItem()
        
        # Emit that the chart has changed.
        self.scene().priceBarChartChanged.emit()
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        LineSegmentGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the LineSegmentGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

    def _handleOpenEndInJHoraAction(self):
        """Causes the the timestamp of the end the
        LineSegmentGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.endPointF.x())
        

class OctaveFanGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a musical scale in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    origin point.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger(\
            "pricebarchart.OctaveFanGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.

        # Color of the graphicsitem bar.
        self.octaveFanGraphicsItemColor = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemBarColor

        # Color of the text that is associated with the graphicsitem.
        self.octaveFanGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextColor

        # X scaling of the text.
        self.octaveFanTextXScaling = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.octaveFanTextYScaling = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartOctaveFanArtifact()

        # Convert object.
        self.convertObj = None
        
        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.octaveFanPenWidth = 0.0
        self.octaveFanPen = QPen()
        self.octaveFanPen.setColor(self.octaveFanGraphicsItemColor)
        self.octaveFanPen.setWidthF(self.octaveFanPenWidth)
        
        # Origin point, in scene coordinates.
        self.originPointF = QPointF(0, 0)

        # Leg1 point, in scene coordinates.
        self.leg1PointF = QPointF(0, 0)

        # Leg2 point, in scene coordinates.
        self.leg2PointF = QPointF(0, 0)

        # Dummy item.
        self.dummyItem = QGraphicsSimpleTextItem("", self)
        
        # Set the font of the text.
        self.octaveFanTextFont = QFont("Sans Serif")
        self.octaveFanTextFont.\
            setPointSizeF(self.artifact.getFontSize())

        # Set the pen color of the text.
        self.octaveFanTextPen = self.dummyItem.pen()
        self.octaveFanTextPen.\
            setColor(self.octaveFanGraphicsItemTextColor)

        # Set the brush color of the text.
        self.octaveFanTextBrush = self.dummyItem.brush()
        self.octaveFanTextBrush.\
            setColor(self.octaveFanGraphicsItemTextColor)

        # Size scaling for the text.
        textTransform = QTransform()
        textTransform.scale(self.octaveFanTextXScaling, \
                            self.octaveFanTextYScaling)
        textTransform.rotate(0.0)
        
        # Below is a list of QGraphicsSimpleTextItems, for each of the
        # MusicalRatios in the PriceBarChartOctaveFanArtifact.  The
        # text contains the musical interval fraction, and the angle
        # of the line.
        #
        self.musicalRatioTextItems = []

        # Initialize to blank and set at the leg1 point.
        for musicalRatio in range(len(self.artifact.getMusicalRatios())):
            
            fractionTextItem = QGraphicsSimpleTextItem("", self)
            fractionTextItem.setPos(self.leg1PointF)
            fractionTextItem.setFont(self.octaveFanTextFont)
            fractionTextItem.setPen(self.octaveFanTextPen)
            fractionTextItem.setBrush(self.octaveFanTextBrush)
            fractionTextItem.setTransform(textTransform)
            
            self.musicalRatioTextItems.\
                append(fractionTextItem)

        # Flags that indicate that the user is dragging either the
        # origin, leg1 or leg2 points of the QGraphicsItem.
        self.draggingOriginPointFlag = False
        self.draggingLeg1PointFlag = False
        self.draggingLeg2PointFlag = False
        self.clickScenePointF = None

    def setConvertObj(self, convertObj):
        """Object for doing conversions from x and datetime and y to
        price.  This should be the graphics scene.  This is used for
        doing conversions from a scene point to price or datetime.  It
        is also used so we can convert price or datetime to a scaled
        value.
        """

        self.log.debug("Entered setConvertObj()")
        
        self.convertObj = convertObj
        
        self.log.debug("Exiting setConvertObj()")
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        ########
        
        # List of used musical ratios.
        musicalRatios = \
            copy.deepcopy(priceBarChartSettings.\
                          octaveFanGraphicsItemMusicalRatios)
        
        # OctaveFanGraphicsItem bar color (QColor).
        self.octaveFanGraphicsItemColor = \
            priceBarChartSettings.octaveFanGraphicsItemBarColor

        # OctaveFanGraphicsItem text color (QColor).
        self.octaveFanGraphicsItemTextColor = \
            priceBarChartSettings.octaveFanGraphicsItemTextColor
        
        # X scaling of the text.
        self.octaveFanTextXScaling = \
            priceBarChartSettings.\
                octaveFanGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.octaveFanTextYScaling = \
            priceBarChartSettings.\
                octaveFanGraphicsItemTextYScaling 

        # textEnabledFlag (bool).
        textEnabledFlag = \
            priceBarChartSettings.\
            octaveFanGraphicsItemTextEnabledFlag

        ########

        # Set values in the artifact.

        self.artifact.setMusicalRatios(musicalRatios)
        self.artifact.setColor(self.octaveFanGraphicsItemColor)
        self.artifact.setTextColor(self.octaveFanGraphicsItemTextColor)
        self.artifact.setTextEnabled(textEnabledFlag)

        self.setArtifact(self.artifact)
        
        self.refreshTextItems()
        
        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        GraphicsItem from the QSettings object. 
        """

        # No settings read from app preferences.
        pass
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.originPointF,
        self.leg1PointF, and self.leg2PointF

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.originPointF

        # Update the start, leg1 and leg2 points accordingly. 
        self.originPointF = self.originPointF + posDelta
        self.leg1PointF = self.leg1PointF + posDelta
        self.leg2PointF = self.leg2PointF + posDelta

        if self.scene() != None:
            self.refreshTextItems()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # origin or leg points, then the user is trying to adjust
            # the origin or leg points.

            # Get the click point in scene coordinates.
            clickScenePos = event.scenePos()
            clickScenePosX = clickScenePos.x()
            clickScenePosY = clickScenePos.y()
            
            self.log.debug("DEBUG: clickScenePosX={}".format(clickScenePosX))
            self.log.debug("DEBUG: clickScenePosY={}".format(clickScenePosY))


            # Get the shape of the line segments of the legs.  The
            # returned QPainterPath is in scene coordinates.
            shapeOfOriginToLeg1Point = \
                self.getShapeOfLineSegment(self.originPointF, self.leg1PointF)
            shapeOfOriginToLeg2Point = \
                self.getShapeOfLineSegment(self.originPointF, self.leg2PointF)

            # Flags that hold whether the click was inside the leg1
            # line segment or leg2 line segment.
            insideLeg1LineSegment = False
            insideLeg2LineSegment = False

            # Holds the QRectF of either leg1LineSegment orl leg2LineSegment.
            rectF = None

            if shapeOfOriginToLeg1Point.contains(clickScenePos) == True:

                insideLeg1LineSegment = True

                # Turn the shape into a bounding rect and determine the
                # 1/5th point from the ends using x and y values of that
                # bounding rect.  This rect below is in scene coordinates.
                rectF = shapeOfOriginToLeg1Point.boundingRect()

            elif shapeOfOriginToLeg2Point.contains(clickScenePos) == True:
                self.log.debug("Click point is within the line segment from " +
                               "origin point to leg2 point.")

                insideLeg2LineSegment = True

                # Turn the shape into a bounding rect and determine the
                # 1/5th point from the ends using x and y values of that
                # bounding rect.  This rect below is in scene coordinates.
                rectF = shapeOfOriginToLeg2Point.boundingRect()


            self.log.debug("insideLeg1LineSegment={}".\
                           format(insideLeg1LineSegment))
            self.log.debug("insideLeg2LineSegment={}".\
                           format(insideLeg2LineSegment))

            # Handle the case that the click was inside a line segment
            # that makes up the outter edge of this fan.
            if insideLeg1LineSegment == True or insideLeg2LineSegment == True:

                self.log.debug("boundingRect  is: " +
                               "(x={}, y={}, w={}, h={})".\
                               format(rectF.x(),
                                      rectF.y(),
                                      rectF.width(),
                                      rectF.height()))

                # Here we will get various points that make up the
                # bounding rect of this line segment.  We will create
                # two sub-rectangles that are 1/5th the portion of x
                # and y of the original rectangle.  The click point
                # being inside one of these sub-rectangles will tell
                # us if the click was near the origin point or if it
                # was near the end leg point.  

                startingPointX = rectF.x()
                startingPointY = rectF.y()

                endingPointX = rectF.x() + rectF.width()
                endingPointY = rectF.y() + rectF.height()

                self.log.debug("DEBUG: startingPointX={}, startingPointY={}".\
                               format(startingPointX, startingPointY))
                self.log.debug("DEBUG: endingPointX={}, endingPointY={}".\
                               format(endingPointX, endingPointY))

                startThresholdX = startingPointX + (rectF.width() * (1.0 / 5))
                endThresholdX = endingPointX - (rectF.width() * (1.0 / 5))

                startThresholdY = startingPointY + (rectF.height() * (1.0 / 5))
                endThresholdY = endingPointY - (rectF.height() * (1.0 / 5))

                self.log.debug("DEBUG: startThresholdX={}".\
                               format(startThresholdX))
                self.log.debug("DEBUG: endThresholdX={}".\
                               format(endThresholdX))

                self.log.debug("DEBUG: startThresholdY={}".\
                               format(startThresholdY))
                self.log.debug("DEBUG: endThresholdY={}".\
                               format(endThresholdY))

                startingPointRect = \
                    QRectF(QPointF(startingPointX, startingPointY),
                           QPointF(startThresholdX, startThresholdY))

                endingPointRect = \
                    QRectF(QPointF(endingPointX, endingPointY),
                           QPointF(endThresholdX, endThresholdY))

                if startingPointRect.contains(clickScenePos):

                    self.draggingOriginPointFlag = True
                    self.log.debug("DEBUG: self.draggingOriginPointFlag={}".
                                   format(self.draggingOriginPointFlag))

                elif endingPointRect.contains(clickScenePos):

                    if insideLeg1LineSegment == True:
                        self.draggingLeg1PointFlag = True
                        self.log.debug("DEBUG: self.draggingLeg1PointFlag={}".
                                       format(self.draggingLeg1PointFlag))

                    elif insideLeg2LineSegment == True:
                        self.draggingLeg2PointFlag = True
                        self.log.debug("DEBUG: self.draggingLeg2PointFlag={}".
                                       format(self.draggingLeg2PointFlag))

                else:

                    self.log.debug("Middle area of the line segment clicked.")


            # If none of the drag point flags are set, then the user
            # has clicked somewhere in teh middle part of the
            # QGraphicsItem (somewhere not close to an endpoint).
            if self.draggingOriginPointFlag == False and \
                self.draggingLeg1PointFlag == False and \
                self.draggingLeg2PointFlag == False:

                # Pass the event to the parent, because the user wants
                # to either select or drag-move the position of the
                # QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()

                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                
                if self.draggingOriginPointFlag == True:
                    self.log.debug("DEBUG: self.draggingOriginPointFlag={}".
                                   format(self.draggingOriginPointFlag))
                    self.setOriginPointF(QPointF(event.scenePos()))
                    self.prepareGeometryChange()
                    
                elif self.draggingLeg1PointFlag == True:
                    self.log.debug("DEBUG: self.draggingLeg1PointFlag={}".
                                   format(self.draggingLeg1PointFlag))
                    self.setLeg1PointF(QPointF(event.scenePos()))
                    self.prepareGeometryChange()

                elif self.draggingLeg2PointFlag == True:
                    self.log.debug("DEBUG: self.draggingLeg2PointFlag={}".
                                   format(self.draggingLeg2PointFlag))
                    self.setLeg2PointF(QPointF(event.scenePos()))
                    self.prepareGeometryChange()
                    
                else:
                    # This means that the user is dragging the whole
                    # item.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingOriginPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "originPoint.")
            
            self.draggingOriginPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingLeg1PointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "leg1Point.")
            
            self.draggingLeg1PointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingLeg2PointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "leg2Point.")
            
            self.draggingLeg2PointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            #self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.originPointF + delta
                    self.setPos(newPos)

            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingOriginPointFlag = False
            self.draggingLeg1PointFlag = False
            self.draggingLeg2PointFlag = False

    def refreshItem(self):
        """Refreshes the item by recalculating and updating the text
        position/rotation.
        """

        self.recalculateOctaveFan()
        
        self.refreshTextItems()
        
    def refreshTextItems(self):
        """Sets the positions of the text items for the MusicalRatios,
        and updates the text so that they are current.
        """

        # If the self.convertObj is None, then try to use the scene if the
        # scene isn't None.
        scene = self.scene()
        if self.convertObj == None:
            if scene != None:
                self.log.debug("self.convertObj wasn't set, but self.scene() " +
                               "is not None, so we're going to set " +
                               "self.convertObj to the scene")
                self.convertObj = self.scene()
            else:
                self.log.debug("Both self.convertObj and " + \
                               "self.scene() are None.")

        # Update the octaveFan label text item texts.
        if self.scene() != None and self.convertObj != None:
            self.recalculateOctaveFan()

            # Traverse the 2-dimensional list and set the position of
            # each of the text items.
            artifact = self.getArtifact()
            for i in range(len(artifact.getMusicalRatios())):
                # Get the MusicalRatio that corresponds to this index.
                musicalRatio = artifact.getMusicalRatios()[i]

                # Here we always set the positions of everything.  If
                # the musicalRatio not enabled, then the corresponding
                # graphics items would have gotten disabled in the
                # self.recalculateOctaveFan() call above.

                # Get the unscaled originPointF, leg1PointF, and leg2PointF.
                unscaledOriginPointF = artifact.getOriginPointF()
                unscaledLeg1PointF = artifact.getLeg1PointF()
                unscaledLeg2PointF = artifact.getLeg2PointF()

                self.log.debug("unscaledOriginPointF is: ({}, {})".
                               format(unscaledOriginPointF.x(),
                                      unscaledOriginPointF.y()))
                self.log.debug("unscaledLeg1PointF is: ({}, {})".
                               format(unscaledLeg1PointF.x(),
                                      unscaledLeg1PointF.y()))
                self.log.debug("unscaledLeg2PointF is: ({}, {})".
                               format(unscaledLeg2PointF.x(),
                                      unscaledLeg2PointF.y()))

                # Calculate scaled originPointF, leg1PointF and
                # leg2PointF points.
                scaledOriginPointF = \
                    self.convertObj.convertScenePointToScaledPoint(\
                    artifact.getOriginPointF())
                scaledLeg1PointF = \
                    self.convertObj.convertScenePointToScaledPoint(\
                    artifact.getLeg1PointF())
                scaledLeg2PointF = \
                    self.convertObj.convertScenePointToScaledPoint(\
                    artifact.getLeg2PointF())
        
                self.log.debug("scaledOriginPointF is: ({}, {})".
                               format(scaledOriginPointF.x(),
                                      scaledOriginPointF.y()))
                self.log.debug("scaledLeg1PointF is: ({}, {})".
                               format(scaledLeg1PointF.x(),
                              scaledLeg1PointF.y()))
                self.log.debug("scaledLeg2PointF is: ({}, {})".
                               format(scaledLeg2PointF.x(),
                                      scaledLeg2PointF.y()))

                # Get the x and y position that will be the new
                # position of the text item.  This function returns
                # the x and y in scaled coordinates so we must
                # remember to convert those values afterwards.
                (x, y) = \
                    artifact.getXYForMusicalRatio(i,
                                                  scaledOriginPointF,
                                                  scaledLeg1PointF,
                                                  scaledLeg2PointF)
                
                # Map those x and y to local coordinates.
                scenePointF = \
                    self.convertObj.convertScaledPointToScenePoint(\
                    QPointF(x, y))
                localPointF = self.mapFromScene(scenePointF)
                
                # Get the number of degrees to rotate the text by,
                # utilizing scaling.
                rotationDegrees = \
                    self.calculateTextRotationDegrees(self.originPointF,
                                                      scenePointF)
                
                # Create the text transform to use.
                textTransform = QTransform()
                textTransform.scale(self.octaveFanTextXScaling, \
                                    self.octaveFanTextYScaling)
                textTransform.rotate(rotationDegrees)

                # Get the text item for this point on the scale.
                textItem = self.musicalRatioTextItems[i]

                # Set the position and other attributes.
                textItem.setPos(localPointF)
                textItem.setFont(self.octaveFanTextFont)
                textItem.setPen(self.octaveFanTextPen)
                textItem.setBrush(self.octaveFanTextBrush)
                textItem.setTransform(textTransform)


            
    def setOriginPointF(self, pointF):
        """Sets the origin point of the octaveFan.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.originPointF != pointF: 
            self.originPointF = pointF

            self.setPos(self.originPointF)
            
            # Update the octaveFan label text item positions.
            self.refreshTextItems()            

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.prepareGeometryChange()

    def setLeg1PointF(self, pointF):
        """Sets the leg1ing point of the octaveFan.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.leg1PointF != pointF:
            self.leg1PointF = pointF

            self.log.debug("OctaveFanGraphicsItem." +
                           "setLeg1PointF(QPointF({}, {}))".\
                           format(pointF.x(), pointF.y()))
            
            # Update the octaveFan label text item positions.
            self.refreshTextItems()

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.prepareGeometryChange()

    def setLeg2PointF(self, pointF):
        """Sets the leg2ing point of the octaveFan.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.leg2PointF != pointF:
            self.leg2PointF = pointF

            self.log.debug("OctaveFanGraphicsItem." +
                           "setLeg2PointF(QPointF({}, {}))".\
                           format(pointF.x(), pointF.y()))
            
            # Update the octaveFan label text item positions.
            self.refreshTextItems()

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.prepareGeometryChange()

    def normalizeStartAndEnd(self):
        """Does nothing since we do not normalize points for this class."""

        pass

    def recalculateOctaveFan(self):
        """Updates the text items that tell about the fann lines on the
        modal scale.  These texts will have accurate values for where
        the notes are in terms of angle.
        """

        # If the self.convertObj is None, then try to use the scene if the
        # scene isn't None.
        scene = self.scene()
        if self.convertObj == None:
            if scene != None:
                self.log.debug("self.convertObj wasn't set, but self.scene() " +
                               "is not None, so we're going to set " +
                               "self.convertObj to the scene")
                self.convertObj = self.scene()
            else:
                self.log.debug("Both self.convertObj and " + \
                               "self.scene() are None.")

        # Now recalculate if we have a convertObj to use for scaling
        # conversion calculation.
        if self.convertObj != None:
        
            # Get the origin point in scene, scaled, and local coordinates.
            sceneOriginPointF = self.originPointF
            scaledOriginPointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.originPointF)
            localOriginPointF = QPointF(0.0, 0.0)
    
            # Get the leg1 point in scene, scaled, and local coordinates.
            sceneLeg1PointF = self.leg1PointF
            scaledLeg1PointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.leg1PointF)
            localLeg1PointF = QPointF(0.0, 0.0) + \
                              (self.leg1PointF - self.originPointF)
            
            # Get the leg2 point in scene, scaled, and local coordinates.
            sceneLeg2PointF = self.leg2PointF
            scaledLeg2PointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.leg2PointF)
            localLeg2PointF = QPointF(0.0, 0.0) + \
                              (self.leg2PointF - self.originPointF)


            # Go through each musical ratio.
            artifact = self.getArtifact()
            musicalRatios = artifact.getMusicalRatios()
            for i in range(len(musicalRatios)):
                musicalRatio = musicalRatios[i]

                if musicalRatio.isEnabled():
                    # Get the x and y position that will be the end point.
                    # This function returns the x and y in scaled
                    # coordinates so we must remember to convert those
                    # values afterwards.
                    (x, y) = \
                        artifact.getXYForMusicalRatio(i,
                                                      scaledOriginPointF,
                                                      scaledLeg1PointF,
                                                      scaledLeg2PointF)
            
                    # Map those x and y to local coordinates.
                    sceneEndPointF = \
                        self.convertObj.convertScaledPointToScenePoint(\
                        QPointF(x, y))
                    
                    # Do conversion to local coordinates.
                    localEndPointF = sceneEndPointF - sceneOriginPointF

                    # Enable and make visible.

                    # Get the text item for this point on the scale.
                    textItem = self.musicalRatioTextItems[i]
                    
                    # Make the text visible if it is enabled.
                    textEnabled = artifact.isTextEnabled()
                    textItem.setEnabled(textEnabled)
                    textItem.setVisible(textEnabled)

                    # If text isn't enabled, there's no need to
                    # set the text for it.  Go to the next text item.
                    if textEnabled == False:
                        continue

                    # Text to set in the text item.
                    text = ""

                    # Append the text for the fraction of the musical note.
                    numerator = musicalRatio.getNumerator()
                    denominator = musicalRatio.getDenominator()

                    if numerator != None and denominator != None:
                        text += \
                            "{}/{}".format(numerator, denominator) + os.linesep

                    # Append the text for the angle of the line.
                    scaledAngleDegrees = \
                        self.calculateScaledAngleDegrees(self.originPointF,
                                                         sceneEndPointF)
                    text += "{:.4f} deg".format(scaledAngleDegrees) + os.linesep

                    # Set the text to the text item.
                    text = text.rstrip()
                    textItem.setText(text)
                    
                else:
                    # Disable and make not visable.
                    
                    # Get the text item for this point on the scale.
                    textItem = self.musicalRatioTextItems[i]
                    
                    textItem.setVisible(False)
                    textItem.setEnabled(False)
                
                        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartOctaveFanArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartOctaveFanArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartOctaveFanArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartOctaveFanArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setOriginPointF(self.artifact.getOriginPointF())
        self.setLeg1PointF(self.artifact.getLeg1PointF())
        self.setLeg2PointF(self.artifact.getLeg2PointF())

        self.octaveFanTextFont.\
            setPointSizeF(self.artifact.getFontSize())
        self.octaveFanPen.\
            setColor(self.artifact.getColor())
        self.octaveFanTextPen.\
            setColor(self.artifact.getTextColor())
        self.octaveFanTextBrush.\
            setColor(self.artifact.getTextColor())

        
        # Need to recalculate the angles, since the origin, leg1 and leg2
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the measurements may not be valid.
        self.refreshTextItems()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartOctaveFanArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        # Update the internal self.priceBarChartOctaveFanArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setOriginPointF(self.originPointF)
        self.artifact.setLeg1PointF(self.leg1PointF)
        self.artifact.setLeg2PointF(self.leg2PointF)
        
        # Everything else gets modified only by the edit dialog.
        
        return self.artifact

    def getShapeOfLineSegment(self, startPointF, endPointF):
        """Returns the shape as a QPainterPath of the line segment
        constructed via the two input QPointFs.  The shape is
        constructed by a rectangle around the start and end points.
        The rectangle is tilted based on the angle of the start and
        end points in view-scaled coordinates.  The bar height used is
        whatever is returned by self.artifact.getBarHeight().

        Arguments:
        
        startPointF - QPointF representing the start point of the line
                      segment in either scene or local coordinates.
        endPointF   - QPointF representing the end point of the line segment
                      in either scene or local scene coordinates.

        Returns:
        QPainterPath object holding the shape of the rectangle around
        the line segment.  If the start and end points are given in
        local coordinates, then the QPainterPath returned will also be
        in local coordinates, otherwise the QPainterPath returned will
        be in scene coordinates.
        """
        
        # Utilize scaling from the scene if it is available.
        scaling = PriceBarChartScaling()
        if self.scene() != None:
            scaling = self.scene().getScaling()
            
        viewScaledStartPoint = \
            QPointF(startPointF.x() * scaling.getViewScalingX(),
                    startPointF.y() * scaling.getViewScalingY())
        viewScaledEndPoint = \
            QPointF(endPointF.x() * scaling.getViewScalingX(),
                    endPointF.y() * scaling.getViewScalingY())

        # Here we are calculating the angle of the text and the line
        # as the user would see it.  Actual angle is different if we
        # are calculating it from a scene perspective.
        angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
        angleRad = math.radians(angleDeg)

        shiftX = math.sin(angleRad) * \
                     (0.5 * self.artifact.getBarHeight())
        shiftY = math.cos(angleRad) * \
                     (0.5 * self.artifact.getBarHeight())
        
        # Create new points.
        p1 = \
            QPointF(startPointF.x() - shiftX,
                    startPointF.y() - shiftY)
        p2 = \
            QPointF(startPointF.x() + shiftX,
                    startPointF.y() + shiftY)
        p3 = \
            QPointF(endPointF.x() - shiftX,
                    endPointF.y() - shiftY)
        p4 = \
            QPointF(endPointF.x() + shiftX,
                    endPointF.y() + shiftY)

        points = [p2, p1, p3, p4, p2]
        polygon = QPolygonF(points)

        painterPath = QPainterPath()
        painterPath.addPolygon(polygon)
        
        return painterPath

    def calculateTextRotationDegrees(self, startPointF, endPointF):
        """Calculates the number of degrees that a
        QGraphicsSimpleTextItem should be rotated so that it is
        parallel to the line constructed by the 'startPointF' and
        'endPointF' parameters.  ViewScaling is utilized to determine the angle.

        Arguments:
        startPointF - start point of the line segment to align the
                      text's angle with.
        endPointF   - start point of the line segment to align the
                      text's angle with.

        Returns:
        float value holding angle that the text needs to be rotated, in degrees.
        """

        # Return value.
        angleDeg = 0.0
        
        # Determine the number of degrees to rotate the text by,
        # utilizing scaling.
        if self.scene() != None:
            scaling = self.scene().getScaling()

            viewScaledStartPoint = \
                QPointF(startPointF.x() * scaling.getViewScalingX(),
                        startPointF.y() * scaling.getViewScalingY())
            viewScaledEndPoint = \
                QPointF(endPointF.x() * scaling.getViewScalingX(),
                        endPointF.y() * scaling.getViewScalingY())
            
            angleDeg = QLineF(viewScaledStartPoint, viewScaledEndPoint).angle()
            self.log.debug("Scaled angleDeg before normalizing and fudge, " +
                           "angleDeg={}".format(angleDeg))
        else:
            # No scaling is available, so just do the unscaled angle.
            angleDeg = QLineF(startPointF, endPointF).angle()
            self.log.debug("Unscaled angleDeg before normalizing and fudge, " +
                           "angleDeg={}".format(angleDeg))
            
        # Normalize the angle so that the text is always upright.
        if 90 <= angleDeg <= 270:
            angleDeg += 180
        angleDeg = Util.toNormalizedAngle(angleDeg)

        self.log.debug("Before fudge, angleDeg={}".format(angleDeg))
        
        # Fudge factor since for some reason the text item doesn't
        # exactly line up with the line.
        fudge = 0.0
        if 0 < angleDeg <= 90:
            self.log.debug("0 to 90")
            removed = 45 - abs(45 - angleDeg)
            fudge = removed * 0.19
            angleDeg -= fudge
        elif 90 < angleDeg <= 180:
            self.log.debug("90 to 180")
            removed = 45 - abs(135 - angleDeg)
            fudge = removed * 0.12
            angleDeg += fudge
        elif 180 < angleDeg <= 270:
            self.log.debug("180 to 270")
            removed = 45 - abs(225 - angleDeg)
            fudge = removed * 0.19
            angleDeg -= fudge
        elif 270 < angleDeg <= 360:
            self.log.debug("270 to 360")
            removed = 45 - abs(315 - angleDeg)
            fudge = removed * 0.12
            angleDeg += fudge
            
        angleDeg = -1.0 * angleDeg
        self.log.debug("angleDeg={}".format(angleDeg))

        return angleDeg
    
    def calculateScaledAngleDegrees(self, startPointF, endPointF):
        """Calculates the number of degrees of angle between
        'startPointF' and 'endPointF'.  This angle is calculated
        utilizing scaling conversion from self.convertObj.

        Arguments:
        startPointF - start point of the line segment, in scene coordinates.
        endPointF   - start point of the line segment, in scene coordinates.

        Returns:
        float value holding the scaled angle, in degrees.
        """

        angleDeg = 0.0

        # If the self.convertObj is None, then try to use the scene if the
        # scene isn't None.
        scene = self.scene()
        if self.convertObj == None:
            if scene != None:
                self.log.debug("self.convertObj wasn't set, but self.scene() " +
                               "is not None, so we're going to set " +
                               "self.convertObj to the scene")
                self.convertObj = self.scene()
            else:
                self.log.debug("Both self.convertObj and " + \
                               "self.scene() are None.")

        if self.convertObj != None:
            startScaledPoint = \
                self.convertObj.convertScenePointToScaledPoint(startPointF)
            endScaledPoint = \
                self.convertObj.convertScenePointToScaledPoint(endPointF)
        
            angleDeg = QLineF(startScaledPoint, endScaledPoint).angle()
        else:
            # Convert object is not set, so don't apply scaling, and
            # just return the angle with unscaled points.
            angleDeg = QLineF(startPointF, endPointF).angle()
            
        return angleDeg
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is origin point.
        
        rv = self.shape().boundingRect()

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.

        Returns:
        QPainterPath object holding the shape of this QGraphicsItem,
        in local item coordinates.
        """

        # Return value.
        # Holds the QPainterPath of the whole item (in local coordinates).
        painterPath = QPainterPath()

        # If the self.convertObj is None, then try to use the scene if the
        # scene isn't None.
        scene = self.scene()
        if self.convertObj == None:
            if scene != None:
                self.log.debug("self.convertObj wasn't set, but self.scene() " +
                               "is not None, so we're going to set " +
                               "self.convertObj to the scene")
                self.convertObj = self.scene()
            else:
                self.log.debug("Both self.convertObj and " + \
                               "self.scene() are None.")

        if scene != None and self.convertObj != None:
            # Scene exists and we can do scaling conversions.
            # Continue to calculate the painterPath.
            
            # Get the origin point in scene, scaled, and local coordinates.
            sceneOriginPointF = self.originPointF
            scaledOriginPointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.originPointF)
            localOriginPointF = QPointF(0.0, 0.0)
    
            # Get the leg1 point in scene, scaled, and local coordinates.
            sceneLeg1PointF = self.leg1PointF
            scaledLeg1PointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.leg1PointF)
            localLeg1PointF = QPointF(0.0, 0.0) + \
                              (self.leg1PointF - self.originPointF)
            
            # Get the leg2 point in scene, scaled, and local coordinates.
            sceneLeg2PointF = self.leg2PointF
            scaledLeg2PointF = \
                self.convertObj.convertScenePointToScaledPoint(\
                self.leg2PointF)
            localLeg2PointF = QPointF(0.0, 0.0) + \
                              (self.leg2PointF - self.originPointF)
    
            # Add the path for the shape of the line segment created by
            # points self.originPointF to self.leg1PointF.  
            localLeg1PointF = self.leg1PointF - self.originPointF
            leg1PainterPath = \
                self.getShapeOfLineSegment(localOriginPointF, localLeg1PointF)
            painterPath.addPath(leg1PainterPath)
            
            # Add the path for the shape of the line segment created by
            # points self.originPointF to self.leg2PointF.
            localLeg2PointF = self.leg2PointF - self.originPointF
            leg2PainterPath = \
                self.getShapeOfLineSegment(localOriginPointF, localLeg2PointF)
            painterPath.addPath(leg2PainterPath)
            
            # Go through each line of each enabled musical ratio, getting
            # the shape of the line segment and add that path to
            # 'painterPath'.
            artifact = self.getArtifact()
            musicalRatios = artifact.getMusicalRatios()
            for i in range(len(musicalRatios)):
                musicalRatio = musicalRatios[i]
    
                # Only add the path if the musical ratio is enabled.
                if musicalRatio.isEnabled():
                    # Get the x and y position that will be the end point.
                    # This function returns the x and y in scaled
                    # coordinates so we must remember to convert those
                    # values afterwards.
                    (x, y) = \
                        artifact.getXYForMusicalRatio(i,
                                                      scaledOriginPointF,
                                                      scaledLeg1PointF,
                                                      scaledLeg2PointF)
            
                    # Map those x and y to local coordinates.
                    sceneEndPointF = \
                        self.convertObj.convertScaledPointToScenePoint(\
                        QPointF(x, y))
                
                    # Do conversion to local coordinates.
                    localEndPointF = sceneEndPointF - sceneOriginPointF
    
                    # Get the painter path.
                    endPointPainterPath = \
                        self.getShapeOfLineSegment(localOriginPointF,
                                                   localEndPointF)
    
                    # Add the path to 'painterPath'.
                    painterPath.addPath(endPointPainterPath)

        else:
            # Scene doesn't exist or we can't scaling conversions.
            # No calculations to do since it won't get plotted anyways.
            self.log.debug("Tried to get shape scene isn't set.")
            pass
            
        # The 'painterPath' should now have all the paths for the tilted
        # rectangles that make up the whole item.
        return painterPath

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.octaveFanPen is set
        to what we want for the drawing style.
        """

        self.log.debug("Entered OctaveFanGraphicsItem.paint().  " +
                       "pos is: ({}, {})".format(self.pos().x(),
                                                 self.pos().y()))
        
        if painter.pen() != self.octaveFanPen:
            painter.setPen(self.octaveFanPen)

        # If the self.convertObj is None, then try to use the scene if the
        # scene isn't None.
        scene = self.scene()
        if self.convertObj == None:
            if scene != None:
                self.log.debug("self.convertObj wasn't set, but self.scene() " +
                               "is not None, so we're going to set " +
                               "self.convertObj to the scene")
                self.convertObj = self.scene()
            else:
                self.log.debug("Both self.convertObj and " + \
                               "self.scene() are None.")
                # No scene, so don't paint anything.
                self.log.debug("There's no scene so we won't paint anything.")
                return

        # Get the origin point in scene, scaled, and local coordinates.
        sceneOriginPointF = self.originPointF
        scaledOriginPointF = \
            self.convertObj.convertScenePointToScaledPoint(\
            self.originPointF)
        localOriginPointF = QPointF(0.0, 0.0)

        # Get the leg1 point in scene, scaled, and local coordinates.
        sceneLeg1PointF = self.leg1PointF
        scaledLeg1PointF = \
            self.convertObj.convertScenePointToScaledPoint(\
            self.leg1PointF)
        localLeg1PointF = QPointF(0.0, 0.0) + \
                          (self.leg1PointF - self.originPointF)
        
        # Get the leg2 point in scene, scaled, and local coordinates.
        sceneLeg2PointF = self.leg2PointF
        scaledLeg2PointF = \
            self.convertObj.convertScenePointToScaledPoint(\
            self.leg2PointF)
        localLeg2PointF = QPointF(0.0, 0.0) + \
                          (self.leg2PointF - self.originPointF)

        
        # Always draw the line from origin point to leg1 point.
        painter.drawLine(QLineF(localOriginPointF, localLeg1PointF))
        
        # Always draw the line from origin point to leg2 point.
        painter.drawLine(QLineF(localOriginPointF, localLeg2PointF))
        
        # For each musical ratio that is enabled, draw it as a line
        # segment from the origin point to the end point of that
        # musical ratio.
        artifact = self.getArtifact()
        musicalRatios = artifact.getMusicalRatios()
        for i in range(len(musicalRatios)):
            musicalRatio = musicalRatios[i]

            # Only add the path if the musical ratio is enabled.
            if musicalRatio.isEnabled():
                # Get the x and y position that will be the end point.
                # This function returns the x and y in scaled
                # coordinates so we must remember to convert those
                # values afterwards.
                (x, y) = \
                    artifact.getXYForMusicalRatio(i,
                                                  scaledOriginPointF,
                                                  scaledLeg1PointF,
                                                  scaledLeg2PointF)
        
                # Map those x and y to local coordinates.
                sceneEndPointF = \
                    self.convertObj.convertScaledPointToScenePoint(\
                    QPointF(x, y))
            
                # Do conversion to local coordinates.
                localEndPointF = sceneEndPointF - sceneOriginPointF

                # Draw the line segment for this musical ratio.
                painter.drawLine(QLineF(localOriginPointF,
                                        localEndPointF))

        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.octaveFanPen.widthF() * 0.5;
            penWidth = 0.0
            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this OctaveFanGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        OctaveFanGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        rotateDownAction = QAction("Rotate Down", parent)
        rotateUpAction = QAction("Rotate Up", parent)
        reverseAction = QAction("Reverse", parent)
        
        setOriginOnAstro1Action = \
            QAction("Set origin timestamp on Astro Chart &1", parent)
        setOriginOnAstro2Action = \
            QAction("Set origin timestamp on Astro Chart &2", parent)
        setOriginOnAstro3Action = \
            QAction("Set origin timestamp on Astro Chart &3", parent)
        openOriginInJHoraAction = \
            QAction("Open JHor&a with origin timestamp", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        rotateDownAction.triggered.\
            connect(self._handleRotateDownAction)
        rotateUpAction.triggered.\
            connect(self._handleRotateUpAction)
        reverseAction.triggered.\
            connect(self._handleReverseAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        openStartInJHoraAction.triggered.\
            connect(self._handleOpenStartInJHoraAction)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        rotateDownAction.setEnabled(not readOnlyMode)
        rotateUpAction.setEnabled(not readOnlyMode)
        reverseAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        openStartInJHoraAction.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addAction(rotateDownAction)
        menu.addAction(rotateUpAction)
        menu.addAction(reverseAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addAction(openStartInJHoraAction)

    def rotateDown(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        self._handleRotateDownAction()
        
    def rotateUp(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        self._handleRotateUpAction()

    def reverse(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        reversed.
        """

        self._handleReverseAction()
        
    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartOctaveFanArtifactEditDialog(artifact,
                                                           self.scene(),
                                                           readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartOctaveFanArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleRotateDownAction(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()

        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
            else:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
                
            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        
    def _handleRotateUpAction(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()
        
        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
            else:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
                

            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()

    def _handleReverseAction(self):
        """Causes the OctaveFanGraphicsItem to have its musicalRatios
        reversed.
        """
        
        # Flip the flag that indicates that the musical ratios are reversed.
        self.artifact.setReversed(not self.artifact.isReversed())
        
        # Refresh everything.
        self.refreshTextItems()
        
        # Emit that the PriceBarChart has changed so that the
        # dirty flag can be set.
        self.scene().priceBarChartChanged.emit()
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the OctaveFanGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the OctaveFanGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the OctaveFanGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleOpenStartInJHoraAction(self):
        """Causes the the timestamp of the start the
        OctaveFanGraphicsItem to be opened in JHora.
        """

        self.scene().openJHora(self.startPointF.x())
        
        
class PriceBarChartWidget(QWidget):
    """Widget holding the QGraphicsScene and QGraphicsView that displays
    the PriceBar information along with other indicators and analysis
    tools.
    """

    # Signal emitted when the PriceBarChartWidget changes.
    # 
    # Possible changes to the widget that will trigger this include: 
    #   - Any scene change (pricebars, artifacts)
    #   - Any settings change (scaling)
    #   
    # It does NOT include:
    #   - User selecting a pricebar
    #   - User opening a wheel astrology chart from a pricebar
    #
    priceBarChartChanged = QtCore.pyqtSignal()

    # Signal emitted when current timestamp of where the mouse is changes.
    currentTimestampChanged = QtCore.pyqtSignal(datetime.datetime)

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    # Signal emitted when the user desires to change astro chart 1.
    astroChart1Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 2.
    astroChart2Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 3.
    astroChart3Update = QtCore.pyqtSignal(datetime.datetime)

    # Signal emitted when the user desires to view a datetime.datetime
    # in JHora.
    jhoraLaunch = QtCore.pyqtSignal(datetime.datetime)
    
    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool"  : 0,
                "PointerTool"          : 1,
                "HandTool"             : 2,
                "ZoomInTool"           : 3,
                "ZoomOutTool"          : 4,
                "BarCountTool"         : 5,
                "TimeMeasurementTool"  : 6,
                "TimeModalScaleTool"   : 7,
                "PriceModalScaleTool"  : 8,
                "TextTool"             : 9,
                "PriceTimeInfoTool"    : 10,
                "PriceMeasurementTool" : 11,
                "TimeRetracementTool"  : 12,
                "PriceRetracementTool" : 13,
                "PriceTimeVectorTool"  : 14,
                "LineSegmentTool"      : 15,
                "OctaveFanTool"        : 16 }



    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarChartWidget")
        self.log.debug("Entered __init__()")

        # Create the contents.
        self.priceBarChartSettings = PriceBarChartSettings()
        
        # Holds the tool mode that this widget is currently in.
        self.toolMode = PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']

        # Holds the timezone of PriceBars in this widget.  
        # This is a datetime.tzinfo object.  We need this to convert X
        # scene coordinate values to a datetime.datetime object with the
        # correct timezone.
        self.timezone = pytz.utc

        # These are the label widgets at the top of the PriceBarChartWidget.
        self.descriptionLabel = QLabel("")
        self.firstPriceBarTimestampLabel = QLabel("")
        self.lastPriceBarTimestampLabel = QLabel("")
        self.numPriceBarsLabel = QLabel("")
        
        localizedTimestampStr = "Mouse time: "
        utcTimestampStr = "Mouse time: "
        priceStr = "Mouse price: " 
        self.cursorLocalizedTimestampLabel = \
            QLabel(localizedTimestampStr)
        self.cursorUtcTimestampLabel = \
            QLabel(utcTimestampStr)
        self.cursorPriceLabel = \
            QLabel(priceStr)

        
        self.selectedPriceBarTimestampLabel = QLabel("")
        self.selectedPriceBarOpenPriceLabel = QLabel("")
        self.selectedPriceBarHighPriceLabel = QLabel("")
        self.selectedPriceBarLowPriceLabel = QLabel("")
        self.selectedPriceBarClosePriceLabel = QLabel("")
        
        # These labels will have smaller font.
        smallFont = QFont()
        smallFont.setPointSize(7)
        self.descriptionLabel.setFont(smallFont)
        self.firstPriceBarTimestampLabel.setFont(smallFont)
        self.lastPriceBarTimestampLabel.setFont(smallFont)
        self.numPriceBarsLabel.setFont(smallFont)
        self.selectedPriceBarTimestampLabel.setFont(smallFont)
        self.selectedPriceBarOpenPriceLabel.setFont(smallFont)
        self.selectedPriceBarHighPriceLabel.setFont(smallFont)
        self.selectedPriceBarLowPriceLabel.setFont(smallFont)
        self.selectedPriceBarClosePriceLabel.setFont(smallFont)

        # Set the cursor timestamp labels as being in a monospaced font.
        smallMonospacedFont = QFont()
        smallMonospacedFont.setFamily("DejaVu Sans Mono")
        smallMonospacedFont.setPointSize(7)
        self.cursorLocalizedTimestampLabel.setFont(smallMonospacedFont)
        self.cursorUtcTimestampLabel.setFont(smallMonospacedFont)
        self.cursorPriceLabel.setFont(smallMonospacedFont)
        
        # Create the QGraphicsView and QGraphicsScene for the display portion.
        self.graphicsScene = PriceBarChartGraphicsScene()
        self.graphicsView = PriceBarChartGraphicsView()
        self.graphicsView.setScene(self.graphicsScene)

        # Setup the layouts.
        dataTimeRangeLayout = QVBoxLayout()
        dataTimeRangeLayout.addWidget(self.descriptionLabel)
        dataTimeRangeLayout.addWidget(self.firstPriceBarTimestampLabel)
        dataTimeRangeLayout.addWidget(self.lastPriceBarTimestampLabel)
        dataTimeRangeLayout.addWidget(self.numPriceBarsLabel)

        cursorInfoLayout = QVBoxLayout()
        cursorInfoLayout.addWidget(self.cursorLocalizedTimestampLabel)
        cursorInfoLayout.addWidget(self.cursorUtcTimestampLabel)
        cursorInfoLayout.addWidget(self.cursorPriceLabel)
       
        priceBarPricesLayout = QVBoxLayout()
        priceBarPricesLayout.addWidget(self.selectedPriceBarTimestampLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarOpenPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarHighPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarLowPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarClosePriceLabel)
        
        topLabelsLayout = QHBoxLayout()
        topLabelsLayout.addLayout(dataTimeRangeLayout)
        topLabelsLayout.addLayout(cursorInfoLayout)
        topLabelsLayout.addLayout(priceBarPricesLayout)
        
        layout = QVBoxLayout()
        layout.addLayout(topLabelsLayout)
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

        self.graphicsView.show()

        # Connect signals and slots.
        self.graphicsView.mouseLocationUpdate.\
            connect(self._handleMouseLocationUpdate)
        self.graphicsView.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
        self.graphicsScene.priceBarChartChanged.\
            connect(self.priceBarChartChanged)
        self.graphicsScene.selectionChanged.\
            connect(self._handleSelectionChanged)

        # Bubble up the signal emission to update the time of the astro charts.
        self.graphicsScene.astroChart1Update.\
            connect(self.astroChart1Update)
        self.graphicsScene.astroChart2Update.\
            connect(self.astroChart2Update)
        self.graphicsScene.astroChart3Update.\
            connect(self.astroChart3Update)
        self.graphicsScene.jhoraLaunch.\
            connect(self.jhoraLaunch)
        
        self.log.debug("Leaving __init__()")

    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        # Pass the information to the graphics scene.  If graphics
        # items need it, it will get it from there.
        self.graphicsScene.setBirthInfo(birthInfo)
        
    def setTimezone(self, timezone):
        """Sets the timezone used.  This is used for converting mouse
        X location to a datetime.datetime object.
        
        Arguments:
            
        timezone - A datetime.tzinfo object holding the timezone for the
                   pricebars in this widget.
        """

        self.timezone = timezone

        # The PriceBarChartGraphicsScene is actually the object that
        # does the conversions.  Pass the timezone info to that object.
        self.graphicsScene.setTimezone(self.timezone)

    def setDescriptionText(self, text):
        """Sets the text of the QLabel self.descriptionLabel."""

        self.descriptionLabel.setText("Description: " + text)

    def updateFirstPriceBarTimestampLabel(self, priceBar=None):
        """Updates the QLabel holding the timestamp of the first PriceBar
        in the pricebarchart.

        Arguments:

        priceBar - PriceBar object to use for updating the timestamp.  
                   If this argument is None, then the label text will be
                   blank.
        """

        # Datetime format to datetime.strftime().
        timestampStr = "First PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)

        self.firstPriceBarTimestampLabel.setText(timestampStr)

    def updateLastPriceBarTimestampLabel(self, priceBar=None):
        """Updates the QLabel holding the timestamp of the last PriceBar
        in the pricebarchart.

        Arguments:

        priceBar - PriceBar object to use for updating the timestamp.  
                   If this argument is None, then the label text will be
                   blank.
        """

        timestampStr = "Last PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)
        
        self.lastPriceBarTimestampLabel.setText(timestampStr)

    def updateNumPriceBarsLabel(self, numPriceBars):
        """Updates the QLabel holding the number of PriceBars
        currently drawn in the pricebarchart.

        Arguments:

        numPriceBars - int value for the number of PriceBars displayed in
                       the PriceBarChart.
        """

        text = "Number of PriceBars: {}".format(numPriceBars)

        self.numPriceBarsLabel.setText(text)

    def updateMouseLocationLabels(self, sceneXPos=None, sceneYPos=None):
        """Updates the QLabels holding the information about the time and
        price of where the mouse position is.  If either of the input
        arguments are None, then the cursor labels are cleared out.
        
        Arguments:
            
        sceneXPos - float value holding the X location of the mouse, in
                    scene coordinates. 
        sceneYPos - float value holding the X location of the mouse, in
                    scene coordinates.
        """

        localizedTimestampStr = "Mouse time: "
        utcTimestampStr = "Mouse time: "
        priceStr = "Mouse price: " 

        # Set the values if the X and Y positions are valid.
        if sceneXPos != None and sceneYPos != None:

            # Convert coordinate to the actual values they represent.
            timestamp = self.graphicsScene.sceneXPosToDatetime(sceneXPos)
            price = self.graphicsScene.sceneYPosToPrice(sceneYPos)

            # Append to the strings.
            localizedTimestampStr += Ephemeris.datetimeToDayStr(timestamp)
            utcTimestampStr += \
                Ephemeris.datetimeToDayStr(timestamp.astimezone(pytz.utc))
            priceStr += "{}".format(price)

        # Actually set the text to the widgets.
        self.cursorLocalizedTimestampLabel.setText(localizedTimestampStr)
        self.cursorUtcTimestampLabel.setText(utcTimestampStr)
        self.cursorPriceLabel.setText(priceStr)

    def updateSelectedPriceBarLabels(self, priceBar=None):
        """Updates the QLabels describing the currently selected PriceBar.
        
        Arguments:

        priceBar - PriceBar object that holds info about the currently
                   selected PriceBar.
        """

        timestampStr = "Timestamp: "
        openStr = "Open: "
        highStr = "High: "
        lowStr = "Low: "
        closeStr = "Close: "

        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)
            openStr += "{}".format(priceBar.open)
            highStr += "{}".format(priceBar.high)
            lowStr += "{}".format(priceBar.low)
            closeStr += "{}".format(priceBar.close)

        # Only change the labels if they are now different.
        if self.selectedPriceBarTimestampLabel.text() != timestampStr:
            self.selectedPriceBarTimestampLabel.setText(timestampStr)

        if self.selectedPriceBarOpenPriceLabel.text() != openStr:
            self.selectedPriceBarOpenPriceLabel.setText(openStr)

        if self.selectedPriceBarHighPriceLabel.text() != highStr:
            self.selectedPriceBarHighPriceLabel.setText(highStr)

        if self.selectedPriceBarLowPriceLabel.text() != lowStr:
            self.selectedPriceBarLowPriceLabel.setText(lowStr)

        if self.selectedPriceBarClosePriceLabel.text() != closeStr:
            self.selectedPriceBarClosePriceLabel.setText(closeStr)


    def loadPriceBars(self, priceBars):
        """Loads the given PriceBars list into this widget as
        PriceBarGraphicsItems.
        """
        
        self.log.debug("Entered loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

        for priceBar in priceBars:

            # Create the QGraphicsItem
            item = PriceBarGraphicsItem()
            item.loadSettingsFromPriceBarChartSettings(\
                self.priceBarChartSettings)
            item.setPriceBar(priceBar)

            # Add the item.
            self.graphicsScene.addItem(item)

            # Make sure the proper flags are set for the mode we're in.
            self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(item)

            # X location based on the timestamp.
            x = self.graphicsScene.datetimeToSceneXPos(priceBar.timestamp)

            # Y location based on the mid price (average of high and low).
            y = self.graphicsScene.priceToSceneYPos(priceBar.midPrice())

            # Set the position, in parent coordinates.
            item.setPos(QPointF(x, y))

        # Set the labels for the timestamps of the first and 
        # last pricebars.
        if len(priceBars) > 0:
            firstPriceBar = priceBars[0]
            lastPriceBar = priceBars[-1]

            self.updateFirstPriceBarTimestampLabel(firstPriceBar)
            self.updateLastPriceBarTimestampLabel(lastPriceBar)
            self.updateNumPriceBarsLabel(len(priceBars))
        else:
            # There are no PriceBars.  Update the labels to reflect that.
            self.updateFirstPriceBarTimestampLabel(None)
            self.updateLastPriceBarTimestampLabel(None)
            self.updateNumPriceBarsLabel(len(priceBars))
            
        self.log.debug("Leaving loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

    def clearAllPriceBars(self):
        """Clears all the PriceBar QGraphicsItems from the 
        QGraphicsScene."""

        # Get all the QGraphicsItems.
        graphicsItems = self.graphicsScene.items()

        # Only remove the PriceBarGraphicsItem items.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                self.graphicsScene.removeItem(item)

        # Update the labels describing the pricebarchart.
        self.updateFirstPriceBarTimestampLabel(None)
        self.updateLastPriceBarTimestampLabel(None)
        self.updateNumPriceBarsLabel(0)
        self.updateSelectedPriceBarLabels(None)


    def getPriceBarChartArtifacts(self):
        """Returns the list of PriceBarChartArtifacts that have been used
        to draw the the artifacts in the QGraphicsScene.
        """

        self.log.debug("Entered getPriceBarChartArtifacts()")
        
        # List of PriceBarChartArtifact objects returned.
        artifacts = []
        
        # Go through all the QGraphicsItems and for each artifact type,
        # extract the PriceBarChartArtifact.
        graphicsItems = self.graphicsScene.items()
        
        for item in graphicsItems:
            if isinstance(item, PriceBarChartArtifactGraphicsItem):
                artifacts.append(item.getArtifact())

        self.log.debug("Number of artifacts being returned is: {}".\
                       format(len(artifacts)))
        
        self.log.debug("Exiting getPriceBarChartArtifacts()")
        
        return artifacts

    def loadPriceBarChartArtifacts(self, priceBarChartArtifacts):
        """Loads the given list of PriceBarChartArtifact objects
        into this widget as QGraphicsItems.

        Arguments:
        
        priceBarChartArtifacts - list of PriceBarChartArtifact objects,
                                 which is used to create various types of
                                 PriceBarChartArtifactGraphicsItem to be
                                 added to the QGraphicsScene.
        """
        
        self.log.debug("Entered loadPriceBarChartArtifacts()")

        self.log.debug("Attempting to load {} artifacts.".\
                       format(len(priceBarChartArtifacts)))

        # Flag to determine if an item was created and added.
        addedItemFlag = False
        
        for artifact in priceBarChartArtifacts:

            # Create the specific PriceBarChartArtifactGraphicsItem,
            # depending on what kind of artifact this is.
            if isinstance(artifact, PriceBarChartBarCountArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = BarCountGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate bar count, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateBarCount()
        
                addedItemFlag = True
                
            elif isinstance(artifact, PriceBarChartTimeMeasurementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TimeMeasurementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate time measurement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateTimeMeasurement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartTimeModalScaleArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TimeModalScaleGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate musicalRatios in the scale,
                # since it wasn't in the QGraphicsScene until now.
                newItem.refreshTextItems()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartPriceModalScaleArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceModalScaleGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate musicalRatios in the scale,
                # since it wasn't in the QGraphicsScene until now.
                newItem.refreshTextItems()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartTextArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TextGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)

                self.log.debug("Before setting artifact, " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                newItem.setArtifact(artifact)

                self.log.debug("After  setting artifact, " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                self.log.debug("After  adding item,      " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                addedItemFlag = True
                
            elif isinstance(artifact, PriceBarChartPriceTimeInfoArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceTimeInfoGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)

                # Set the conversion object as the scene so that it
                # can do initial calculations for the text to display.
                newItem.setConvertObj(self.graphicsScene)

                # Set the artifact offically so that it can update the text.
                newItem.setArtifact(artifact)

                # Set the birthInfo in the new item.  This will again
                # trigger a text update.
                birthInfo = self.graphicsScene.getBirthInfo()
                newItem.setBirthInfo(birthInfo)
                
                # Add the item to the graphics scene.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartPriceMeasurementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceMeasurementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate price measurement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculatePriceMeasurement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartTimeRetracementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TimeRetracementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate time retracement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateTimeRetracement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartPriceRetracementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceRetracementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate price retracement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculatePriceRetracement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartPriceTimeVectorArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceTimeVectorGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to refresh the item (recalculate) since it
                # wasn't in the QGraphicsScene until now.
                newItem.refreshItem()

                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartLineSegmentArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = LineSegmentGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to refresh the item (recalculate) since it
                # wasn't in the QGraphicsScene until now.
                newItem.refreshItem()

                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartOctaveFanArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = OctaveFanGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
        
                # Set the conversion object as the scene so that it
                # can do initial calculations for the text to display.
                newItem.setConvertObj(self.graphicsScene)

                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to refresh the item (recalculate) since it
                # wasn't in the QGraphicsScene until now.
                newItem.refreshItem()
                
                addedItemFlag = True

        if addedItemFlag == True:
            # Emit that the PriceBarChart has changed.
            self.graphicsScene.priceBarChartChanged.emit()
            
        self.log.debug("Exiting loadPriceBarChartArtifacts()")



    def addPriceBarChartArtifact(self, priceBarChartArtifact):
        """Adds the given PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""

        # List of one element.
        artifacts = [priceBarChartArtifact]

        # Load it via a list.  If it is added, then it will emit
        # the self.priceBarChartChanged signal for us.
        self.loadPriceBarChartArtifacts(artifacts)
        
    def clearAllPriceBarChartArtifacts(self):
        """Clears all the PriceBarChartArtifact objects from the 
        QGraphicsScene."""

        self.log.debug("Entered clearAllPriceBarChartArtifacts()")

        # Flag to determine if an item was removed.
        removedItemFlag = False
        
        # Go through all the QGraphicsItems and remove the artifact items.
        graphicsItems = self.graphicsScene.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarChartArtifactGraphicsItem):
                self.log.debug("Removing QGraphicsItem for artifact " + \
                               item.toString())
                self.graphicsScene.removeItem(item)
                
                removedItemFlag = True

        if removedItemFlag == True:
            # Emit that the PriceBarChart has changed.
            self.graphicsScene.priceBarChartChanged.emit()
            
        self.log.debug("Exiting clearAllPriceBarChartArtifacts()")
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.log.debug("Entering applyPriceBarChartSettings()")

        self.priceBarChartSettings = priceBarChartSettings

        # Save a reference to the current PriceBarChartSettings in the
        # QGraphicsView.  This is used when the user creates new chart
        # artificats at run time.
        self.graphicsView.setPriceBarChartSettings(self.priceBarChartSettings)

        # Flag to indicate if the settings has changed because we
        # corrected an invalid settings field and the settings needs
        # to be re-saved.
        settingsChangedFlag = False

        self.log.debug("Applying QGraphicsView scaling...")

        numScalings = \
            len(self.priceBarChartSettings.priceBarChartGraphicsViewScalings)

        # Get the index for which scaling we should apply.
        currScalingIndex = \
            self.priceBarChartSettings.priceBarChartGraphicsViewScalingsIndex

        # Temporary variable holding the PriceBarChartScaling scaling
        # object to use.
        scaling = PriceBarChartScaling()

        if numScalings >= 1:
            
            if currScalingIndex < 0 or currScalingIndex >= numScalings:
                # Use the first scaling in the list.
                currScalingIndex = 0
                self.priceBarChartSettings.\
                    priceBarChartGraphicsViewScalingsIndex = 0

                settingsChangedFlag = True

            # Use the scaling at index currScalingIndex.
            scaling = \
                self.priceBarChartSettings.\
                    priceBarChartGraphicsViewScalings[currScalingIndex]

        elif numScalings == 0:
            # There are no scalings in the list.  

            # Create a scaling containing the identity matrix, and then
            # add it to the array and then use that scaling.
            scaling = PriceBarChartScaling()
            scaling.name = "Default"

            self.priceBarChartSettings.\
                priceBarChartGraphicsViewScalings.append(scaling)

            self.priceBarChartSettings.\
                priceBarChartGraphicsViewScalingsIndex = 0

            settingsChangedFlag = True

        # Give the scaling to the QGraphicsScene so that it is
        # available for scaling-related calculations that some of the
        # graphics items/indicators.
        self.graphicsScene.setScaling(scaling)
        
        # Create a new QTransform that holds the scaling we want
        # but preserve the translation and other parts of the
        # transform from what is currently displayed in the
        # QGraphicsView.

        # Get the current QTransform.
        transform = self.graphicsView.transform()

        # Get the QTransform that has the desired scaling from the
        # PriceBarChartSettings.
        scalingTransform = scaling.getTransform()

        # Create a new QTransform that has elements of both.
        newTransform = QTransform(scalingTransform.m11(),
                                  transform.m12(),
                                  transform.m13(),
                                  transform.m21(),
                                  scalingTransform.m22(),
                                  transform.m23(),
                                  transform.m31(),
                                  transform.m32(),
                                  transform.m33())

        # Apply the transform.
        self.graphicsView.setTransform(newTransform)

        # Apply the settings on all the existing relevant QGraphicsItems.
        graphicsItems = self.graphicsScene.items()
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                self.log.debug("Applying settings to PriceBarGraphicsItem.")
                item.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
            elif isinstance(item, BarCountGraphicsItem):
                self.log.debug("Applying settings to BarCountGraphicsItem.")
                item.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
            elif isinstance(item, TimeMeasurementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TimeMeasurementGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculateTimeMeasurement()
            elif isinstance(item, TimeModalScaleGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TimeModalScaleGraphicsItem.")
            elif isinstance(item, PriceModalScaleGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceModalScaleGraphicsItem.")
            elif isinstance(item, TextGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TextGraphicsItem.")
            elif isinstance(item, PriceTimeInfoGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceTimeInfoGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculatePriceTimeInfo()
            elif isinstance(item, PriceMeasurementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceMeasurementGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculatePriceMeasurement()
            elif isinstance(item, TimeRetracementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TimeRetracementGraphicsItem.")
            elif isinstance(item, PriceRetracementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceRetracementGraphicsItem.")
            elif isinstance(item, PriceTimeVectorGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceTimeVectorGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculatePriceTimeVector()
            elif isinstance(item, LineSegmentGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "LineSegmentGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculateLineSegment()
            elif isinstance(item, OctaveFanGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "OctaveFanGraphicsItem.")
                # Redo calculations in case the scaling changed.
                item.recalculateOctaveFan()
                
        if settingsChangedFlag == True:
            # Emit that the PriceBarChart has changed, because we have
            # updated the PriceBarChartSettings.
            self.priceBarChartChanged.emit()

        self.log.debug("Exiting applyPriceBarChartSettings()")

    def getPriceBarChartSettings(self):
        """Returns the current settings used in this PriceBarChartWidget."""
        
        return self.priceBarChartSettings

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.log.debug("Entered toReadOnlyPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']:

            self.toolMode = \
                PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']
            self.graphicsView.toReadOnlyPointerToolMode()

        self.log.debug("Exiting toReadOnlyPointerToolMode()")

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.log.debug("Entered toPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['PointerTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['PointerTool']
            self.graphicsView.toPointerToolMode()

        self.log.debug("Exiting toPointerToolMode()")

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.log.debug("Entered toHandToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['HandTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['HandTool']
            self.graphicsView.toHandToolMode()

        self.log.debug("Exiting toHandToolMode()")

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.log.debug("Entered toZoomInToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['ZoomInTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['ZoomInTool']
            self.graphicsView.toZoomInToolMode()

        self.log.debug("Exiting toZoomInToolMode()")

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.log.debug("Entered toZoomOutToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['ZoomOutTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['ZoomOutTool']
            self.graphicsView.toZoomOutToolMode()

        self.log.debug("Exiting toZoomOutToolMode()")

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.log.debug("Entered toBarCountToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['BarCountTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['BarCountTool']
            self.graphicsView.toBarCountToolMode()

        self.log.debug("Exiting toBarCountToolMode()")


    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.log.debug("Entered toTimeMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TimeMeasurementTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TimeMeasurementTool']
            self.graphicsView.toTimeMeasurementToolMode()

        self.log.debug("Exiting toTimeMeasurementToolMode()")

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.log.debug("Entered toTimeModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TimeModalScaleTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TimeModalScaleTool']
            self.graphicsView.toTimeModalScaleToolMode()

        self.log.debug("Exiting toTimeModalScaleToolMode()")

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.log.debug("Entered toPriceModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['PriceModalScaleTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['PriceModalScaleTool']
            self.graphicsView.toPriceModalScaleToolMode()

        self.log.debug("Exiting toPriceModalScaleToolMode()")

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.log.debug("Entered toTextToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TextTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TextTool']
            self.graphicsView.toTextToolMode()

        self.log.debug("Exiting toTextToolMode()")

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.log.debug("Entered toPriceTimeInfoToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['PriceTimeInfoTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['PriceTimeInfoTool']
            self.graphicsView.toPriceTimeInfoToolMode()

        self.log.debug("Exiting toPriceTimeInfoToolMode()")

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.log.debug("Entered toPriceMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['PriceMeasurementTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['PriceMeasurementTool']
            self.graphicsView.toPriceMeasurementToolMode()

        self.log.debug("Exiting toPriceMeasurementToolMode()")

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.log.debug("Entered toTimeRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TimeRetracementTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TimeRetracementTool']
            self.graphicsView.toTimeRetracementToolMode()

        self.log.debug("Exiting toTimeRetracementToolMode()")

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.log.debug("Entered toPriceRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['PriceRetracementTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['PriceRetracementTool']
            self.graphicsView.toPriceRetracementToolMode()

        self.log.debug("Exiting toPriceRetracementToolMode()")

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.log.debug("Entered toPriceTimeVectorToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['PriceTimeVectorTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['PriceTimeVectorTool']
            self.graphicsView.toPriceTimeVectorToolMode()

        self.log.debug("Exiting toPriceTimeVectorToolMode()")

    def toLineSegmentToolMode(self):
        """Changes the tool mode to be the LineSegmentTool."""

        self.log.debug("Entered toLineSegmentToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['LineSegmentTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['LineSegmentTool']
            self.graphicsView.toLineSegmentToolMode()

        self.log.debug("Exiting toLineSegmentToolMode()")

    def toOctaveFanToolMode(self):
        """Changes the tool mode to be the OctaveFanTool."""

        self.log.debug("Entered toOctaveFanToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['OctaveFanTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['OctaveFanTool']
            self.graphicsView.toOctaveFanToolMode()

        self.log.debug("Exiting toOctaveFanToolMode()")

    def _handleMouseLocationUpdate(self, x, y):
        """Handles mouse location changes in the QGraphicsView.  
        Arguments:

        x - float value of the mouse's X coordinate position, in scene
        coordinates.
        y - float value of the mouse's Y coordinate position, in scene
        coordinates.
        """

        # Update labels that tell where the mouse pointer is.
        self.updateMouseLocationLabels(x, y)

        # Emit a signal so that other widgets/entities can know
        # the timestamp where the mouse pointer is.
        dt = self.graphicsScene.sceneXPosToDatetime(x)
        self.currentTimestampChanged.emit(dt)

    def _handleSelectionChanged(self):
        """Handles when the QGraphicsScene has it's selection of
        QGraphicsItems changed.

        This function obtains the selected items, and if there is only
        one PriceBarGraphicsItem selected, then it displays the
        information about that pricebar in the labels at the top of
        the widget.
        """

        selectedItems = self.graphicsScene.selectedItems()

        numPriceBarGraphicsItemsSelected = 0
        lastPriceBarGraphicsItem = None
        
        for item in selectedItems:
            if isinstance(item, PriceBarGraphicsItem):
                numPriceBarGraphicsItemsSelected += 1
                lastPriceBarGraphicsItem = item

        self.log.debug("Number of PriceBarGraphicsItems selected is: {}".\
                       format(numPriceBarGraphicsItemsSelected))

        # Only update the labels with price/time information if there
        # was only one PriceBarGraphicsItem selected.  This is done to
        # avoid confusion in the event that a second
        # PriceBarGraphicsItem is selected and the user didn't notice
        # that it was (to prevent the wrong information from being
        # interpreted).
        if numPriceBarGraphicsItemsSelected == 1:
            priceBar = lastPriceBarGraphicsItem.getPriceBar()
            self.updateSelectedPriceBarLabels(priceBar)
        else:
            self.updateSelectedPriceBarLabels(None)
            
        
class PriceBarChartGraphicsScene(QGraphicsScene):
    """QGraphicsScene holding all the pricebars and artifacts.
    We inherit QGraphicsScene to allow for future feature additions.
    """

    # Signal emitted when there is an addition of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartArtifactGraphicsItemAdded = \
        QtCore.pyqtSignal(PriceBarChartArtifactGraphicsItem)
        
    # Signal emitted when there is a removal of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartArtifactGraphicsItemRemoved = \
        QtCore.pyqtSignal(PriceBarChartArtifactGraphicsItem)

    # Signal emitted when there is an addition or removal of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartChanged = QtCore.pyqtSignal()

    # Signal emitted when the user desires to change astro chart 1.
    astroChart1Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 2.
    astroChart2Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 3.
    astroChart3Update = QtCore.pyqtSignal(datetime.datetime)

    # Signal emitted when the user desires to view a datetime.datetime
    # in JHora.
    jhoraLaunch = QtCore.pyqtSignal(datetime.datetime)
    
    def __init__(self, parent=None):
        """Pass-through to the QGraphicsScene constructor."""

        super().__init__(parent)

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarChartGraphicsScene")

        # Holds the scaling object which is used for scaling-related
        # calculations.
        self.scaling = PriceBarChartScaling()
        
        # Holds the BirthInfo object.  This is used in calculating
        # information related to astrology.
        self.birthInfo = None
        
        # Holds the timezone as a datetime.tzinfo object.  This is
        # used in conversions of scene position X value to
        # datetime.datetime.
        self.timezone = pytz.utc
        
        # Adding or removing an artifact graphics item counts as
        # something changed.
        self.priceBarChartArtifactGraphicsItemAdded.\
            connect(self.priceBarChartChanged)
        self.priceBarChartArtifactGraphicsItemRemoved.\
            connect(self.priceBarChartChanged)

    def setScaling(self, scaling):
        """Sets the PriceBarChartScaling scaling object used for this
        trading entity.  This scaling object is used for various
        scaling-related calculations.  This function does not apply
        scaling to the QGraphicsView.
        """

        self.scaling = scaling

    def getScaling(self):
        """Returns PriceBarChartScaling object being used for scaling.
        """

        return self.scaling
    
    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        self.birthInfo = birthInfo

        # Go through all the current items, and for every time that
        # needs a current BirthInfo, then set the birthInfo in that
        # item.

        graphicsItems = self.items()
        for item in graphicsItems:
            if isinstance(item, PriceTimeInfoGraphicsItem):
                # Setting birthInfo on this object will cause the
                # whole widget to update it's internal text and info
                # accordingly.
                item.setBirthInfo(self.birthInfo)

    def getBirthInfo(self):
        """Returns the birthInfo for this trading entity as a BirthInfo object.
        """

        return self.birthInfo
    
    def setTimezone(self, timezone):
        """Sets the timezone used.  This is used for converting mouse
        X location to a datetime.datetime object.
        
        Arguments:
            
        timezone - A datetime.tzinfo object holding the timezone for the
                   pricebars in this widget.
        """

        self.timezone = timezone
    
    def sceneXPosToDatetime(self, sceneXPos):
        """Returns a datetime.datetime object for the given X position in
        scene coordinates.

        Arguments:

        sceneXPos - float value holding the X position in scene coordinates.

        Returns:

        datetime.datetime object holding the timestamp of the input X
        position.  This datetime.datetime object has its timezone set to
        whatever was set in setTimezone() previously.  If nothing was set
        before, then the default timezone is pytz.utc.
        """

        return Ephemeris.julianDayToDatetime(sceneXPos, self.timezone)
    
    def sceneYPosToPrice(self, sceneYPos):
        """Returns a price value for the given Y position in scene
        coordinates.

        Arguments:

        sceneYPos - float value holding the Y position in scene
        coordinates.

        Returns:

        float value for the price that this Y position represents.
        """

        # Make sure I don't return a negative 0.0.
        if (sceneYPos != 0.0):
            return float(-1.0 * sceneYPos)
        else:
            return float(sceneYPos)

    def datetimeToSceneXPos(self, dt):
        """Returns the conversion from datetime.datetime object to what we
        chosen the X coordinate values to be.

        Arguments:

        dt - datetime.datetime object that holds a timestamp.

        Returns:

        float value for the X position that would match up with this timestamp.
        """

        return Ephemeris.datetimeToJulianDay(dt)

    def priceToSceneYPos(self, price):
        """Returns the conversion from price to what we have chosen the Y
        coordinate values to be.

        Arguments:

        price - float value holding the price value.

        Returns:

        float value for the Y position that would match up with this price.
        """

        # Below ensures the value returned is not -0.0 (negative 0.0).
        if (price != 0.0):
            return float(-1.0 * price)
        else:
            return float(price)


    def convertPriceToScaledValue(self, price):
        """Converts the given price value to a scaled value,
        using the set scaling object.

        Arguments:
        price - float value for the price to convert to a scaled value.

        Returns:
        float value representing the scaled value of the given price.
        """

        scaledValue = price / self.scaling.getUnitsOfPrice()

        return scaledValue
        
    def convertScaledValueToPrice(self, scaledValue):
        """Converts the given scaled value to a price, using the set
        scaling object.

        Arguments:
        scaledValue - float value to convert to a price value.

        Returns:
        float value representing the price.
        """

        price = scaledValue * self.scaling.getUnitsOfPrice()

        return price
        
    def convertDatetimeToScaledValue(self, dt):
        """Converts the given datetime to the scaled value, using the
        set scaling object.  This returned value is the scaled value
        relative to the birth time in self.birthInfo

        Arguments:
        dt - datetime.datetime object for the timestamp to convert to
             a scaled value.

        Returns:
        float value representing the scaled value of the
        given timestamp, from the birth timestamp.
        """

        birthDatetime = self.getBirthDatetime()
        birthJd = Ephemeris.datetimeToJulianDay(birthDatetime)

        currDatetime = dt
        currJd = Ephemeris.datetimeToJulianDay(currDatetime)

        jdDiff = currJd - birthJd

        scaledValue = jdDiff / self.scaling.getUnitsOfTime()
        
        return scaledValue
        
    def convertScaledValueToDatetime(self, scaledValue, tzInfo=None):
        """Converts the given scaled value to it's equivalent datetime using the
        set scaling object.  

        Arguments:
        scaledValue - float value representing a scaled value that is to be
                      converted to a timestamp value.
        tzInfo - pytz.timezone object for the timezone to use for
                 the datetime object returned.  If tzInfo is None, then
                 the previously set timezone of this trading
                 entity (self.timezone) is used.

        Returns:
        datetime.datetime object representing the timestamp for the
        given scaled value.
        """

        jd = scaledValue * self.scaling.getUnitsOfTime()

        if tzInfo == None:
            tzInfo = self.timezone
            
        dt = Ephemeris.julianDayToDatetime(jd, tzInfo)
        
        return dt

    def getBirthPrice(self):
        """Returns the open price at birth.  We assume here that the
        first pricebar we have is the first pricebar of this trading
        entity.

        Returns:
        float value for the birth price.  0.0 is returned if
        there are no pricebars found.
        """

        openPrice = 0.0
        earliestPriceBar = self.getEarliestPriceBar()
        
        if earliestPriceBar != None:
            openPrice = earliestPriceBar.open

        return openPrice
        
    def getBirthDatetime(self, tzInfo=None):
        """Returns the datetime.datetime for the timestamp at birth.

        Arguments:
        tzInfo - pytz.timezone object that is the timezone to
                 return the datetime in.  If tzInfo is None,
                 then the previously set timezone of this
                 trading entity (self.timezone) is used.
        
        Returns:
        datetime.datetime for the birth timestamp.
        """

        birthInfo = self.birthInfo
        
        if tzInfo == None:
            tzInfo = self.timezone
        
        if self.birthInfo == None:
            self.log.warn("Birth info is not set.  " +
                          "Scaling calculations may not be accurate.")
                          
            birthInfo = BirthInfo()
            
        birthDatetime = birthInfo.getBirthUtcDatetime()
        birthJd = Ephemeris.datetimeToJulianDay(birthDatetime)
        dt = Ephemeris.julianDayToDatetime(birthJd, tzInfo)
        
        return dt
        
    def getBirthScaledPoint(self):
        """Returns a QPointF for the birth price and time, converted
        to independent unit values, and scaled appropriately using the
        self.scaling scaling object.

        There are two ways to set the Y for time:
          - Assume that the open price is the point.
          - Assume that zero price is this point.
        
        In this function, the first method is used.

        Returns:
        QPointF for the birth point in scaled unit-less values.
        """

        price = self.getBirthPrice()

        # Time at birth is assumed to be 0.
        jd = 0.0
        
        # Do scaling.
        scaledPriceValue = price / self.scaling.getUnitsOfPrice()
        scaledTimeValue = jd / self.scaling.getUnitsOfTime()

        return QPointF(scaledTimeValue, scaledPriceValue)

    def getBirthScaledPointOrigin(self):
        """Returns a QPointF for the birth price and time, converted
        to independent unit values, and scaled appropriately using the
        self.scaling scaling object.

        There are two ways to set the Y for time:
          - Assume that the open price is the point.
          - Assume that zero price is this point.
        
        In this function, the second method is used.
        
        Returns:
        QPointF for the birth point in scaled unit-less values.
        """

        # Regardless of scaling, the origin birth point will be (0, 0).
        return QPointF(0.0, 0.0)
        
    def convertScenePointToScaledPoint(self, pointF):
        """Converts the given QPointF from the QGraphicsScene to a
        scaled QPointF using the price and time scaling in
        self.scaling.

        Arguments:
        pointF - QPointF object holding the QGraphicsScene point that
                 the caller wants to convert to a scaled QPointF.

        Returns:
        QPointF holding a scaled QPointF equivalent to the given input point.
        """

        x = pointF.x()
        y = pointF.y()

        dt = self.sceneXPosToDatetime(x)
        price = self.sceneYPosToPrice(y)

        scaledX = self.convertDatetimeToScaledValue(dt)
        scaledY = self.convertPriceToScaledValue(price)

        return QPointF(scaledX, scaledY)

    def convertScaledPointToScenePoint(self, pointF):
        """Converts the given QPoint as a scaled QPointF, to a QPointF
        that is represented in the QGraphicsScene.

        Arguments:
        pointF - QPointF object holding a scaled point that the user
                 wants to convert to a QGraphicsScene point.

        Returns:
        QPointF holding a QPointF in a QGraphicsScene that is equivalent
        to the given input point.
        """

        x = pointF.x()
        y = pointF.y()

        dt = self.convertScaledValueToDatetime(x)
        price = self.convertScaledValueToPrice(y)

        sceneX = self.datetimeToSceneXPos(dt)
        sceneY = self.priceToSceneYPos(price)

        return QPointF(sceneX, sceneY)
    
    def getEarliestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the earliest timestamp.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object that has the earliest timestamp.
        """

        earliestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if earliestPriceBar == None:
                    earliestPriceBar = pb
                elif pb.timestamp < earliestPriceBar.timestamp:
                    earliestPriceBar = pb
                    
        return earliestPriceBar

    def getLatestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the latest timestamp.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object that has the latest timestamp.
        """

        latestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if latestPriceBar == None:
                    latestPriceBar = pb
                elif pb.timestamp > latestPriceBar.timestamp:
                    latestPriceBar = pb
                    
        return latestPriceBar

    def getHighestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the highest high price.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object for the highest pricebar in price.
        """

        highestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if highestPriceBar == None:
                    highestPriceBar = pb
                elif pb.hasHigherHighThan(highestPriceBar):
                    highestPriceBar = pb
                    
        
        return highestPriceBar

    def getLowestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the lowest low price.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object for the lowest pricebar in price.
        """

        lowestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if lowestPriceBar == None:
                    lowestPriceBar = pb
                elif pb.hasLowerLowThan(lowestPriceBar):
                    lowestPriceBar = pb
        
        return lowestPriceBar

    def getClosestPriceBarOHLCPoint(self, pointF):
        """Goes through all the PriceBars, looking at the QPointF of
        the open, high, low, and close of each bar (in price and
        time), and tests it to locate the point out of all the bars
        that is the closest to 'pointF'.

        WARNING: This may not do what you expect to do!  The reason is
        because our current scaling for time (x coordinate) is 1 unit
        of x per day.  Our price scaling (y coordinate) is 1 unit of
        price per y.  This means the 'qgraphicsview' scaling of x and
        y (in appearance) is misleading when compared to actual
        coordinates.  So the algorithm works correctly, but may not
        produce expected results due to a huge skew in scaling.  If
        this is not what you want, then consider using
        getClosestPriceBarOHLCViewPoint().
        
        Returns:
        QPointF - Point that is a scene pos of a open, high, low,
                  or close of a PriceBar, where it is the closest
                  to the given 'pointF'.
        """

        self.log.debug("Entered getClosestPriceBarOHLCPoint()")
        
        # QPointF for the closest point.
        closestPoint = None

        # Smallest length of line from pointF to desired point.
        smallestLength = None
        
        # PriceBarGraphicsItem that is the closest.
        closestPriceBarGraphicsItem = None
        
        graphicsItems = self.items()

        self.log.debug("PointF is: ({}, {})".format(pointF.x(), pointF.y()))
                       
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                # Get the points of the open, high, low, and close of
                # this PriceBarGraphicsItem.
                openPointF = item.getPriceBarOpenScenePoint()
                highPointF = item.getPriceBarHighScenePoint()
                lowPointF = item.getPriceBarLowScenePoint()
                closePointF = item.getPriceBarCloseScenePoint()

                self.log.debug("openPointF is: ({}, {})".
                               format(openPointF.x(), openPointF.y()))
                self.log.debug("highPointF is: ({}, {})".
                               format(highPointF.x(), highPointF.y()))
                self.log.debug("lowPointF is: ({}, {})".
                               format(lowPointF.x(), lowPointF.y()))
                self.log.debug("closePointF is: ({}, {})".
                               format(closePointF.x(), closePointF.y()))

                # Create lines so we can get the lengths between the points.
                lineToOpen = QLineF(pointF, openPointF)
                lineToHigh = QLineF(pointF, highPointF)
                lineToLow = QLineF(pointF, lowPointF)
                lineToClose = QLineF(pointF, closePointF)

                lineToOpenLength = lineToOpen.length()
                lineToHighLength = lineToHigh.length()
                lineToLowLength = lineToLow.length()
                lineToCloseLength = lineToClose.length()
                
                self.log.debug("lineToOpenLength is: {}".\
                               format(lineToOpenLength))
                self.log.debug("lineToHighLength is: {}".\
                               format(lineToHighLength))
                self.log.debug("lineToLowLength is: {}".\
                               format(lineToLowLength))
                self.log.debug("lineToCloseLength is: {}".\
                               format(lineToCloseLength))

                # Set the initial smallestLength as the first point if
                # it is not set already.
                if smallestLength == None:
                    closestPoint = openPointF
                    smallestLength = lineToOpen.length()
                    closestPriceBarGraphicsItem = item

                # Test the open, high, low, and close points to see if
                # they are now the closest to pointF.
                if lineToOpenLength < smallestLength:
                    closestPoint = openPointF
                    smallestLength = lineToOpenLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToHighLength < smallestLength:
                    closestPoint = highPointF
                    smallestLength = lineToHighLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToLowLength < smallestLength:
                    closestPoint = lowPointF
                    smallestLength = lineToLowLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToCloseLength < smallestLength:
                    closestPoint = closePointF
                    smallestLength = lineToCloseLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))
                    
        self.log.debug("Closest point is: ({}, {})".format(closestPoint.x(),
                                                           closestPoint.y()))

        self.log.debug("Exiting getClosestPriceBarOHLCPoint()")
        
        return closestPoint

    def getClosestPriceBarOHLCViewPoint(self, pointF):
        """Goes through all the PriceBars, looking at the QPointF of
        the open, high, low, and close of each pricebar (in price and
        time), and tests it to locate the point out of all the bars
        that is the closest to 'pointF' in the GraphicsView.  This
        utilizes the graphics view scaling to see what is closest.  

        Arguments:
        pointF - QPointF object that is a point in scene
        coordinates.  This point is used as a reference point to
        calculate distances to the open, high, low, and close points
        of the price bars.
        
        Returns:
        QPointF - Point in scene coordinates of the closest pricebar's
        open, high, low, or close (in price and time), when computed
        using scaled view coordinates.
        """
        
        self.log.debug("Entered getClosestPriceBarOHLCViewPoint()")
        
        # QPointF for the closest point.
        closestPoint = None

        # Smallest length of line from pointF to desired point.
        smallestLength = None
        
        # PriceBarGraphicsItem that is the closest.
        closestPriceBarGraphicsItem = None

        # Scaling object to use.
        scaling = self.scaling
        
        self.log.debug("PointF is: ({}, {})".format(pointF.x(), pointF.y()))

        viewScaledPointF = QPointF(pointF.x() * scaling.getViewScalingX(),
                                   pointF.y() * scaling.getViewScalingY())
        
        self.log.debug("View-scaled PointF is: ({}, {})".\
                       format(viewScaledPointF.x(), viewScaledPointF.y()))

        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                # Get the points of the open, high, low, and close of
                # this PriceBarGraphicsItem.
                openPointF = item.getPriceBarOpenScenePoint()
                highPointF = item.getPriceBarHighScenePoint()
                lowPointF = item.getPriceBarLowScenePoint()
                closePointF = item.getPriceBarCloseScenePoint()

                self.log.debug("openPointF is: ({}, {})".
                               format(openPointF.x(), openPointF.y()))
                self.log.debug("highPointF is: ({}, {})".
                               format(highPointF.x(), highPointF.y()))
                self.log.debug("lowPointF is: ({}, {})".
                               format(lowPointF.x(), lowPointF.y()))
                self.log.debug("closePointF is: ({}, {})".
                               format(closePointF.x(), closePointF.y()))

                viewScaledOpenPointF = \
                    QPointF(openPointF.x() * scaling.getViewScalingX(),
                            openPointF.y() * scaling.getViewScalingY())
                viewScaledHighPointF = \
                    QPointF(highPointF.x() * scaling.getViewScalingX(),
                            highPointF.y() * scaling.getViewScalingY())
                viewScaledLowPointF = \
                    QPointF(lowPointF.x() * scaling.getViewScalingX(),
                            lowPointF.y() * scaling.getViewScalingY())
                viewScaledClosePointF = \
                    QPointF(closePointF.x() * scaling.getViewScalingX(),
                            closePointF.y() * scaling.getViewScalingY())

                self.log.debug("viewScaledOpenPointF is: ({}, {})".
                               format(viewScaledOpenPointF.x(),
                                      viewScaledOpenPointF.y()))
                self.log.debug("viewScaledHighPointF is: ({}, {})".
                               format(viewScaledHighPointF.x(),
                                      viewScaledHighPointF.y()))
                self.log.debug("viewScaledLowPointF is: ({}, {})".
                               format(viewScaledLowPointF.x(),
                                      viewScaledLowPointF.y()))
                self.log.debug("viewScaledClosePointF is: ({}, {})".
                               format(viewScaledClosePointF.x(),
                                      viewScaledClosePointF.y()))

                # Create lines so we can get the lengths between the points.
                lineToOpen = QLineF(viewScaledPointF, viewScaledOpenPointF)
                lineToHigh = QLineF(viewScaledPointF, viewScaledHighPointF)
                lineToLow = QLineF(viewScaledPointF, viewScaledLowPointF)
                lineToClose = QLineF(viewScaledPointF, viewScaledClosePointF)

                lineToOpenLength = lineToOpen.length()
                lineToHighLength = lineToHigh.length()
                lineToLowLength = lineToLow.length()
                lineToCloseLength = lineToClose.length()
                
                self.log.debug("lineToOpenLength is: {}".\
                               format(lineToOpenLength))
                self.log.debug("lineToHighLength is: {}".\
                               format(lineToHighLength))
                self.log.debug("lineToLowLength is: {}".\
                               format(lineToLowLength))
                self.log.debug("lineToCloseLength is: {}".\
                               format(lineToCloseLength))

                # Set the initial smallestLength as the first point if
                # it is not set already.
                if smallestLength == None:
                    # Here we are keeping the scene coordinate, not the
                    # view-scaled one.
                    closestPoint = openPointF
                    smallestLength = lineToOpen.length()
                    closestPriceBarGraphicsItem = item

                # Test the open, high, low, and close points to see if
                # they are now the closest to pointF.
                if lineToOpenLength < smallestLength:
                    # Here we are keeping the scene coordinate, not the
                    # view-scaled one.
                    closestPoint = openPointF
                    smallestLength = lineToOpenLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: ({}, {})".\
                                   format(closestPoint.x(),
                                          closestPoint.y()))

                if lineToHighLength < smallestLength:
                    # Here we are keeping the scene coordinate, not the
                    # view-scaled one.
                    closestPoint = highPointF
                    smallestLength = lineToHighLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: ({}, {})".\
                                   format(closestPoint.x(),
                                          closestPoint.y()))

                if lineToLowLength < smallestLength:
                    # Here we are keeping the scene coordinate, not the
                    # view-scaled one.
                    closestPoint = lowPointF
                    smallestLength = lineToLowLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: ({}, {})".\
                                   format(closestPoint.x(),
                                          closestPoint.y()))

                if lineToCloseLength < smallestLength:
                    # Here we are keeping the scene coordinate, not the
                    # view-scaled one.
                    closestPoint = closePointF
                    smallestLength = lineToCloseLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: ({}, {})".\
                                   format(closestPoint.x(),
                                          closestPoint.y()))
                    
        self.log.debug("Closest point is: ({}, {})".\
                       format(closestPoint.x(), closestPoint.y()))

        self.log.debug("Exiting getClosestPriceBarOHLCViewPoint()")
        
        return closestPoint
        
        
    def getClosestPriceBarX(self, pointF):
        """Gets the X position value of the closest PriceBar (on the X
        axis) to the given QPointF position.

        Arguments:
        pointF - QPointF to do the lookup on.

        Returns:
        float value for the X value.  If there are no PriceBars, then it
        returns the X given in the input pointF.
        """

        # Get all the QGraphicsItems.
        graphicsItems = self.items()

        closestPriceBarX = None
        currClosestDistance = None

        # Go through the PriceBarGraphicsItems and find the closest one in
        # X coordinates.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):

                x = item.getPriceBarHighScenePoint().x()
                distance = abs(pointF.x() - x)

                if closestPriceBarX == None:
                    closestPriceBarX = x
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarX = x
                    currClosestDistance = distance
                    
        if closestPriceBarX == None:
            closestPriceBarX = pointF.x()

        return closestPriceBarX

    def getClosestPriceBarOHLCY(self, pointF):
        """Gets the Y position value of the closest open, high, low,
        or close price on all the PriceBars (on the Y axis) to the
        given QPointF position.

        Arguments:
        pointF - QPointF to do the lookup on.

        Returns:
        float value for the Y value.  If there are no PriceBars, then it
        returns the Y given in the input pointF.
        """

        # Get all the QGraphicsItems.
        graphicsItems = self.items()

        closestPriceBarY = None
        currClosestDistance = None

        # Go through the PriceBarGraphicsItems and find the closest one in
        # Y coordinates.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):

                # High price's Y.
                y = item.getPriceBarHighScenePoint().y()
                distance = abs(pointF.y() - y)
                
                if closestPriceBarY == None:
                    closestPriceBarY = y
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarY = y
                    currClosestDistance = distance

                # Low price's Y.
                y = item.getPriceBarLowScenePoint().y()
                distance = abs(pointF.y() - y)

                if closestPriceBarY == None:
                    closestPriceBarY = y
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarY = y
                    currClosestDistance = distance
                    
        if closestPriceBarY == None:
            closestPriceBarY = pointF.y()

        return closestPriceBarY

    def setAstroChart1(self, x):
        """Emits the astroChart1Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart1Update.emit(dt)
        
    def setAstroChart2(self, x):
        """Emits the astroChart2Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart2Update.emit(dt)
        
    def setAstroChart3(self, x):
        """Emits the astroChart3Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart3Update.emit(dt)
        
    def openJHora(self, x):
        """Opens the JHora application with the timestamp represented
        by the X coordinate value.  This function uses the birth
        location/timezone set in self.birthInfo.
        
        Arguments:
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the JHora can be launched
        # for this datetime.datetime.
        self.jhoraLaunch.emit(dt)

class PriceBarChartGraphicsView(QGraphicsView):
    """QGraphicsView that visualizes the main QGraphicsScene.
    We inherit QGraphicsView because we may want to add 
    custom syncrhonized functionality in other widgets later."""


    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool"  : 0,
                "PointerTool"          : 1,
                "HandTool"             : 2,
                "ZoomInTool"           : 3,
                "ZoomOutTool"          : 4,
                "BarCountTool"         : 5,
                "TimeMeasurementTool"  : 6,
                "TimeModalScaleTool"   : 7,
                "PriceModalScaleTool"  : 8,
                "TextTool"             : 9,
                "PriceTimeInfoTool"    : 10,
                "PriceMeasurementTool" : 11,
                "TimeRetracementTool"  : 12,
                "PriceRetracementTool" : 13,
                "PriceTimeVectorTool"  : 14,
                "LineSegmentTool"      : 15,
                "OctaveFanTool"        : 16 }

    # Signal emitted when the mouse moves within the QGraphicsView.
    # The position emitted is in QGraphicsScene x, y, float coordinates.
    mouseLocationUpdate = QtCore.pyqtSignal(float, float)

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartGraphicsView")
        self.log.debug("Entered __init__()")

        # Save the current transformation matrix of the view.
        self.transformationMatrix = None

        # Save the current viewable portion of the scene.
        self.viewableSceneRectF = self.mapToScene(self.rect()).boundingRect()

        # Holds the tool mode that this widget is currently in.
        self.toolMode = \
            PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

        # Anchor variable we will use for click-drag, etc.
        self.dragAnchorPointF = QPointF()

        # Variable used for storing mouse clicks (used in the various
        # modes for various purposes).
        self.clickOnePointF = None
        self.clickTwoPointF = None
        self.clickThreePointF = None

        # Variable used for storing the new BarCountGraphicsItem,
        # as it is modified in BarCountToolMode.
        self.barCountGraphicsItem = None

        # Variable used for storing the new TimeMeasurementGraphicsItem,
        # as it is modified in TimeMeasurementToolMode.
        self.timeMeasurementGraphicsItem = None

        # Variable used for storing the new TimeModalScaleGraphicsItem,
        # as it is modified in TimeModalScaleToolMode.
        self.timeModalScaleGraphicsItem = None

        # Variable used for storing the new PriceModalScaleGraphicsItem,
        # as it is modified in PriceModalScaleToolMode.
        self.priceModalScaleGraphicsItem = None

        # Variable used for storing the new TextGraphicsItem,
        # as it is modified in TextToolMode.
        self.textGraphicsItem = None
        
        # Variable used for storing the new PriceTimeInfoGraphicsItem,
        # as it is modified in PriceTimeInfoToolMode.
        self.priceTimeInfoGraphicsItem = None

        # Variable used for storing the new PriceMeasurementGraphicsItem,
        # as it is modified in PriceMeasurementToolMode.
        self.priceMeasurementGraphicsItem = None

        # Variable used for storing the new TimeRetracementGraphicsItem,
        # as it is modified in TimeRetracementToolMode.
        self.timeRetracementGraphicsItem = None

        # Variable used for storing the new PriceRetracementGraphicsItem,
        # as it is modified in PriceRetracementToolMode.
        self.priceRetracementGraphicsItem = None

        # Variable used for storing the new PriceTimeVectorGraphicsItem,
        # as it is modified in PriceTimeVectorToolMode.
        self.priceTimeVectorGraphicsItem = None

        # Variable used for storing the new LineSegmentGraphicsItem,
        # as it is modified in LineSegmentToolMode.
        self.lineSegmentGraphicsItem = None

        # Variable used for storing the new OctaveFanGraphicsItem,
        # as it is modified in OctaveFanToolMode.
        self.octaveFanGraphicsItem = None

        # Variable used for storing that snapping to the closest bar
        # high or low is enabled.
        #
        # Used in:
        #   - PriceTimeInfoTool
        #   - TimeModalScaleTool
        #   - PriceModalScaleTool
        #   - TimeMeasurementTool
        #   - PriceMeasurementTool
        #   - TimeRetracementTool
        #   - PriceRetracementTool
        #   - PriceTimeVectorTool
        #   - LineSegmentTool
        #   - OctaveFanTool
        #
        self.snapEnabledFlag = True

        # Variable used for holding the PriceBarChartSettings.
        self.priceBarChartSettings = PriceBarChartSettings()
        
        # Get the QSetting key for the zoom scaling amounts.
        self.zoomScaleFactorSettingsKey = \
            SettingsKeys.zoomScaleFactorSettingsKey 

        #self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)

        # Set some rendering settings so things draw nicely.
        self.setRenderHints(QPainter.Antialiasing | 
                            QPainter.TextAntialiasing | 
                            QPainter.SmoothPixmapTransform)

        # Set to FullViewportUpdate update mode.
        #
        # The default is normally QGraphicsView.MinimalViewportUpdate, but
        # this caused us to have missing parts of artifacts and missing
        # parts of pricebars.  And while performance isn't as great in
        # the FullViewportUpdate mode, we dont' have many things dynamically
        # updating and changing, so it isn't too big of an issue.
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def setPriceBarChartSettings(self, priceBarChartSettings):
        """Stores the reference to PriceBarChartSettings to be used in
        creating new QGraphicsItems.
        """
        
        self.priceBarChartSettings = priceBarChartSettings
        
    def setGraphicsItemFlagsPerCurrToolMode(self, item):
        """Sets the QGraphicsItem flags of the given QGraphicsItem,
        according to what the flags should be set to for the current
        tool mode.

        Arguments:

        item - QGraphicsItem that needs its flags set.
        """

        #self.log.debug("setGraphicsItemFlagsPerCurrToolMode(): " +
        #               "toolMode == {}.  ".format(self.toolMode) +
        #               "type(item) == {}.  ".format(type(item)) +
        #               "item is of type PriceBarGraphicsItem: {}.  ".\
        #               format(isinstance(item, PriceBarGraphicsItem)) +
        #               "item is of type PriceBarChartArtifactGraphicsItem: " +
        #               "{}.".
        #               format(isinstance(item,
        #                                 PriceBarChartArtifactGraphicsItem)))
                       
        if self.toolMode == \
               PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            if isinstance(item, PriceBarGraphicsItem):
                flags = QGraphicsItem.GraphicsItemFlags(QGraphicsItem.
                                                        ItemIsSelectable)
                item.setFlags(flags)
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                flags = QGraphicsItem.\
                    GraphicsItemFlags(QGraphicsItem.ItemIsSelectable)
                item.setFlags(flags)
                
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:
             
            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(False)

                flags = QGraphicsItem.\
                    GraphicsItemFlags(QGraphicsItem.ItemIsMovable +
                                      QGraphicsItem.ItemIsSelectable)
                item.setFlags(flags)
                
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:
             
            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
             
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

                
    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool.
        
        This has the following effects on QGraphicsItem flags:
          - All PriceBarGraphicsItems are selectable.
          - All PriceBarGraphicsItems are not movable.
          - All PriceBarChartArtifactGraphicsItem are selectable.
          - All PriceBarChartArtifactGraphicsItem are not movable.
        """

        self.log.debug("Entered toReadOnlyPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.RubberBandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)

        self.log.debug("Exiting toReadOnlyPointerToolMode()")

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool.
        
        This has the following effects on QGraphicsItem flags:
          - All PriceBarGraphicsItems are not selectable.
          - All PriceBarGraphicsItems are not movable.
          - All PriceBarChartArtifactGraphicsItem are selectable.
          - All PriceBarChartArtifactGraphicsItem are movable.
        """

        self.log.debug("Entered toPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['PointerTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['PointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.RubberBandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
            
        self.log.debug("Exiting toPointerToolMode()")

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.log.debug("Entered toHandToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['HandTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['HandTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.ScrollHandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)

        self.log.debug("Exiting toHandToolMode()")

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.log.debug("Entered toZoomInToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomInTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomInTool']

            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomIn.png")
                self.setCursor(QCursor(pixmap))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toZoomInToolMode()")

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.log.debug("Entered toZoomOutToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomOutTool']

            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomOut.png")
                self.setCursor(QCursor(pixmap))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toZoomOutToolMode()")

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.log.debug("Entered toBarCountToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.barCountGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toBarCountToolMode()")

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.log.debug("Entered toTimeMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.timeMeasurementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTimeMeasurementToolMode()")

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.log.debug("Entered toTimeModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.timeModalScaleGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTimeModalScaleToolMode()")

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.log.debug("Entered toPriceModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceModalScaleGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceModalScaleToolMode()")

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.log.debug("Entered toTextToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TextTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.textGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTextToolMode()")

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.log.debug("Entered toPriceTimeInfoToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceTimeInfoGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceTimeInfoToolMode()")

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.log.debug("Entered toPriceMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceMeasurementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceMeasurementToolMode()")

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.log.debug("Entered toTimeRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.timeRetracementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTimeRetracementToolMode()")

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.log.debug("Entered toPriceRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceRetracementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceRetracementToolMode()")

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.log.debug("Entered toPriceTimeVectorToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceTimeVectorGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceTimeVectorToolMode()")

    def toLineSegmentToolMode(self):
        """Changes the tool mode to be the LineSegmentTool."""

        self.log.debug("Entered toLineSegmentToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.lineSegmentGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toLineSegmentToolMode()")

    def toOctaveFanToolMode(self):
        """Changes the tool mode to be the OctaveFanTool."""

        self.log.debug("Entered toOctaveFanToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.clickThreePointF = None
            self.octaveFanGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toOctaveFanToolMode()")

    def createContextMenu(self, clickPosF, readOnlyFlag):
        """Creates a context menu for a right-click somewhere in
        the QGraphicsView, and returns it.

        Arguments:
        clickPosF - QPointF object of the right-click location,
            in scene coordinates.
        readOnlyFlag - bool value that indicates whether or not to
            bring up the menu options for the readonly
            mode or not.
        """

        scene = self.scene()

        # See if the user has right clicked on a QGraphicsItem.
        items = scene.items(clickPosF,
                            Qt.ContainsItemBoundingRect,
                            Qt.AscendingOrder)

        # Here count the number of items at this position that
        # we care about for creating a context menu for.
        debugLogStr = ""
        numContextSubMenuItems = 0

        menu = QMenu(self)
        menu.setTitle("PriceBarChartGraphicsView context menu")
        parent = None

        
        for item in items:
            if isinstance(item, PriceBarGraphicsItem):
                debugLogStr += \
                    "PriceBarGraphicsItem with PriceBar: " + \
                    item.priceBar.toString() + ". "
                
                numContextSubMenuItems += 1

                # Add the menu for this item.  We create the menu this
                # way so that 'submenu' is owned by 'menu'.
                submenu = menu.addMenu("")
                
                # Append actions and update the submenu title.
                item.appendActionsToContextMenu(submenu,
                                                readOnlyMode=readOnlyFlag)

            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                debugLogStr += \
                    "PriceBarChartArtifactGraphicsItem with " + \
                    "artifact info: " + item.artifact.toString() + ". "

                numContextSubMenuItems += 1

                # Add the menu for this item.  We create the menu this
                # way so that 'submenu' is owned by 'menu'.
                submenu = menu.addMenu("")
                
                # Append actions and update the submenu title.
                item.appendActionsToContextMenu(submenu,
                                                readOnlyMode=readOnlyFlag)
            else:
                self.log.debug("Non-PriceBar and Non-artifact item.")


        self.log.debug("{} items under scene clickPosF({}, {}): {}".\
                       format(numContextSubMenuItems,
                              clickPosF.x(),
                              clickPosF.y(),
                              debugLogStr))

        # Add context menu options that are available for all locations.
        menu.addSeparator()

        # Here I am creating QActions that will handle the QMenu
        # option selection, but for setting astro times, I have to
        # jump through a few hoops to be able to pass the
        # information about the recent right-click that caused the
        # context menu to come up.  Maybe there's a better way to
        # do this.
        setAstro1Action = QAction("Set timestamp on Astro Chart 1", parent)
        setAstro2Action = QAction("Set timestamp on Astro Chart 2", parent)
        setAstro3Action = QAction("Set timestamp on Astro Chart 3", parent)
        openJHoraAction = QAction("Open JHora with timestamp", parent)

        # Define a method to add to each instance.
        def handleActionTriggered(self):
            self.emit(QtCore.SIGNAL("actionTriggered(QPointF)"), self.data())

        # Add the method to the instances of the actions.
        setAstro1Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro1Action)
        setAstro2Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro2Action)
        setAstro3Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro3Action)
        openJHoraAction.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             openJHoraAction)
        
        # Store in the actions, the scene position as a QPointF.
        setAstro1Action.setData(clickPosF)
        setAstro2Action.setData(clickPosF)
        setAstro3Action.setData(clickPosF)
        openJHoraAction.setData(clickPosF)

        # Connect the triggered signal to the signal we appended
        # to the instances.
        setAstro1Action.triggered.\
            connect(setAstro1Action.handleActionTriggered)
        setAstro2Action.triggered.\
            connect(setAstro2Action.handleActionTriggered)
        setAstro3Action.triggered.\
            connect(setAstro3Action.handleActionTriggered)
        openJHoraAction.triggered.\
            connect(openJHoraAction.handleActionTriggered)
        
        QtCore.QObject.connect(setAstro1Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro1Action)
        QtCore.QObject.connect(setAstro2Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro2Action)
        QtCore.QObject.connect(setAstro2Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro2Action)
        QtCore.QObject.connect(openJHoraAction,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleOpenJHoraAction)

        # TODO: add more options here for showing the sq-of-9,
        # etc. for this price/time.

        menu.addAction(setAstro1Action)
        menu.addAction(setAstro2Action)
        menu.addAction(setAstro3Action)
        menu.addAction(openJHoraAction)
        return menu
    
    def _handleSetAstro1Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart1(clickPosF.x())
        
    def _handleSetAstro2Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart2(clickPosF.x())
        
    def _handleSetAstro3Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart3(clickPosF.x())
        
    def _handleOpenJHoraAction(self, clickPosF):
        """Causes the timestamp of this GraphicsItem to be opened in
        JHora.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().openJHora(clickPosF.x())
        
    def wheelEvent(self, qwheelevent):
        """Triggered when the mouse wheel is scrolled."""

        self.log.debug("Entered wheelEvent()")

        # Save the old transformation anchor and change the current on
        # to anchor under the mouse.  We will put it back at the end
        # of this method.
        oldViewportAnchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Get the QSetting key for the zoom scaling amounts.
        settings = QSettings()
        scaleFactor = \
            float(settings.value(self.zoomScaleFactorSettingsKey, \
                  SettingsKeys.zoomScaleFactorSettingsDefValue))
        
        # Actually do the scaling of the view.
        if qwheelevent.delta() > 0:
            # Zoom in.
            self.scale(scaleFactor, scaleFactor)
        else:
            # Zoom out.
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

        # Put the old transformation anchor back.
        self.setTransformationAnchor(oldViewportAnchor)
        
        self.log.debug("Exiting wheelEvent()")

    def keyPressEvent(self, qkeyevent):
        """Overwrites the QGraphicsView.keyPressEvent() function.
        Called when a key is pressed.
        """

        self.log.debug("Entered keyPressEvent()")

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Unselect any selected items.
                self.log.debug("Escape key pressed while in " +
                               "'ReadOnlyPointerTool' mode")
                self.scene().clearSelection()
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Unselect any selected items.
                self.log.debug("Escape key pressed while in 'PointerTool' mode")
                self.scene().clearSelection()
            elif qkeyevent.matches(QKeySequence.Delete):
                # Get the items that are selected, and out of those,
                # remove the PriceBarChartArtifactGraphicsItems.
                self.log.debug("Delete key pressed while in 'PointerTool' mode")
                
                scene = self.scene()
                selectedItems = scene.selectedItems()

                for item in selectedItems:
                    if isinstance(item, PriceBarChartArtifactGraphicsItem):

                        self.log.debug("Removing item with artifact: " +
                                       item.getArtifact().getInternalName())
                        scene.removeItem(item)
        
                        # Emit signal to show that an item is removed.
                        # This sets the dirty flag.
                        scene.priceBarChartArtifactGraphicsItemRemoved.\
                            emit(item)
            else:
                # See what item type(s) are selected and take action
                # based on that.

                scene = self.scene()
                selectedItems = scene.selectedItems()

                for item in selectedItems:
                    if isinstance(item, TimeModalScaleGraphicsItem):
                        if qkeyevent.key() == Qt.Key_S:
                            item.rotateUp()
                            self.statusMessageUpdate.emit(\
                                "TimeModalScaleGraphicsItem rotated UP")
                        elif qkeyevent.key() == Qt.Key_G:
                            item.rotateDown()
                            self.statusMessageUpdate.emit(\
                                "TimeModalScaleGraphicsItem rotated DOWN")
                        elif qkeyevent.key() == Qt.Key_R:
                            item.reverse()
                            self.statusMessageUpdate.emit(\
                                "TimeModalScaleGraphicsItem reversed")
                    elif isinstance(item, PriceModalScaleGraphicsItem):
                        if qkeyevent.key() == Qt.Key_S:
                            item.rotateUp()
                            self.statusMessageUpdate.emit(\
                                "PriceModalScaleGraphicsItem rotated UP")
                        elif qkeyevent.key() == Qt.Key_G:
                            item.rotateDown()
                            self.statusMessageUpdate.emit(\
                                "PriceModalScaleGraphicsItem rotated DOWN")
                        elif qkeyevent.key() == Qt.Key_R:
                            item.reverse()
                            self.statusMessageUpdate.emit(\
                                "PriceModalScaleGraphicsItem reversed")
                    elif isinstance(item, OctaveFanGraphicsItem):
                        if qkeyevent.key() == Qt.Key_S:
                            item.rotateUp()
                            self.statusMessageUpdate.emit(\
                                "OctaveFanGraphicsItem rotated UP")
                        elif qkeyevent.key() == Qt.Key_G:
                            item.rotateDown()
                            self.statusMessageUpdate.emit(\
                                "OctaveFanGraphicsItem rotated DOWN")
                        elif qkeyevent.key() == Qt.Key_R:
                            item.reverse()
                            self.statusMessageUpdate.emit(\
                                "OctaveFanGraphicsItem reversed")

                # Pass the key event upwards in case it applies to
                # something else (like a parent widget).
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited bar count item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.barCountGraphicsItem != None:
                    self.scene().removeItem(self.barCountGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.barCountGraphicsItem = None

            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.timeMeasurementGraphicsItem != None:
                    self.scene().removeItem(self.timeMeasurementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.timeMeasurementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.timeModalScaleGraphicsItem != None:
                    self.scene().removeItem(self.timeModalScaleGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.timeModalScaleGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceModalScaleGraphicsItem != None:
                    self.scene().removeItem(self.priceModalScaleGraphicsItem)
                    
                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceModalScaleGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.textGraphicsItem != None:
                    self.scene().removeItem(self.textGraphicsItem)

                self.textGraphicsItem = None
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceTimeInfoGraphicsItem != None:
                    self.scene().removeItem(self.priceTimeInfoGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceTimeInfoGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceMeasurementGraphicsItem != None:
                    self.scene().removeItem(self.priceMeasurementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceMeasurementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.timeRetracementGraphicsItem != None:
                    self.scene().removeItem(self.timeRetracementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.timeRetracementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceRetracementGraphicsItem != None:
                    self.scene().removeItem(self.priceRetracementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceRetracementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceTimeVectorGraphicsItem != None:
                    self.scene().removeItem(self.priceTimeVectorGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceTimeVectorGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.lineSegmentGraphicsItem != None:
                    self.scene().removeItem(self.lineSegmentGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.lineSegmentGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.octaveFanGraphicsItem != None:
                    self.scene().removeItem(self.octaveFanGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.clickThreePointF = None
                self.octaveFanGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().keyPressEvent(qkeyevent)

        
        self.log.debug("Exiting keyPressEvent()")

        
    def mousePressEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mousePressEvent()")

        # Get the click position in scene coordinates for debugging purposes.
        clickPosF = self.mapToScene(qmouseevent.pos())
        self.log.debug("Click pos in scene coordinates is: ({}, {})".\
                       format(clickPosF.x(), clickPosF.y()))
        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:
            
            self.log.debug("Current toolMode is: ReadOnlyPointerTool")

            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            self.log.debug("Current toolMode is: PointerTool")
            
            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in non-readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=False)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            self.log.debug("Current toolMode is: HandTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                self.log.debug("Passing mouse press event to super().")
                # Panning the QGraphicsView.
                super().mousePressEvent(qmouseevent)
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            self.log.debug("Current toolMode is: ZoomInTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                # New center
                newCenterPointF = self.mapToScene(qmouseevent.pos())

                # Get the QSetting key for the zoom scaling amounts.
                settings = QSettings()
                scaleFactor = \
                    float(settings.value(self.zoomScaleFactorSettingsKey, \
                            SettingsKeys.zoomScaleFactorSettingsDefValue))

                # Actually do the scaling of the view.
                self.scale(scaleFactor, scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            
            self.log.debug("Current toolMode is: ZoomOutTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                # New center
                newCenterPointF = self.mapToScene(qmouseevent.pos())

                # Get the QSetting key for the zoom scaling amounts.
                settings = QSettings()
                scaleFactor = \
                    float(settings.value(self.zoomScaleFactorSettingsKey, \
                            SettingsKeys.zoomScaleFactorSettingsDefValue))

                # Actually do the scaling of the view.
                self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:
            
            self.log.debug("Current toolMode is: BarCountTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # Create the BarCountGraphicsItem and initialize it to
                    # the mouse location.
                    self.barCountGraphicsItem = BarCountGraphicsItem()
                    self.barCountGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
                    self.barCountGraphicsItem.setPos(self.clickOnePointF)
                    self.barCountGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.barCountGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.barCountGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.barCountGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.barCountGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem != None.")
                    
                    # Set the end point of the BarCountGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    self.barCountGraphicsItem.setEndPointF(self.clickTwoPointF)
                    self.barCountGraphicsItem.normalizeStartAndEnd()
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.barCountGraphicsItem.getArtifact()
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.barCountGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.barCountGraphicsItem.sceneBoundingRect()
                    self.log.debug("barCountGraphicsItem " +
                                   "officially added.  " +
                                   "pos is: {}.  ".\
                                   format(self.barCountGraphicsItem.pos()) +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None

                else:
                    self.log.warn("Unexpected state reached.")

            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.barCountGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem != None.")
                    
                    # Right-click during setting the BarCountGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.barCountGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.barCountGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:
            
            self.log.debug("Current toolMode is: TimeMeasurementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickOnePointF.setX(x)
                    
                    # Create the TimeMeasurementGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeMeasurementGraphicsItem = \
                        TimeMeasurementGraphicsItem()
                    self.timeMeasurementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.timeMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
        
                    self.timeMeasurementGraphicsItem.setPos(self.clickOnePointF)
                    self.timeMeasurementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.timeMeasurementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.timeMeasurementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.timeMeasurementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.timeMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem != None.")
                    
                    # Set the end point of the TimeMeasurementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickTwoPointF.setX(x)
                    
                    self.timeMeasurementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.timeMeasurementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeMeasurementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.timeMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.timeMeasurementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.timeMeasurementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("timeMeasurementGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                                   
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeMeasurementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.timeMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem != None.")
                    
                    # Right-click during setting the TimeMeasurementGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.timeMeasurementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeMeasurementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.timeMeasurementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:
            
            self.log.debug("Current toolMode is: TimeModalScaleTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickOnePointF.setX(x)
                    
                    # Create the TimeModalScaleGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeModalScaleGraphicsItem = \
                        TimeModalScaleGraphicsItem()
                    self.timeModalScaleGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)

                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.timeModalScaleGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
                    
                    self.timeModalScaleGraphicsItem.setPos(self.clickOnePointF)
                    self.timeModalScaleGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.timeModalScaleGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.timeModalScaleGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.timeModalScaleGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.timeModalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeModalScaleGraphicsItem != None.")
                    
                    # Set the end point of the TimeModalScaleGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickTwoPointF.setX(x)
                    
                    newEndPointF = QPointF(self.clickTwoPointF.x(),
                                           self.clickOnePointF.y())
                    self.timeModalScaleGraphicsItem.\
                        setEndPointF(newEndPointF)
                    self.timeModalScaleGraphicsItem.normalizeStartAndEnd()

                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.timeModalScaleGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeModalScaleGraphicsItem.getArtifact()
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.timeModalScaleGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.timeModalScaleGraphicsItem.sceneBoundingRect()
                    self.log.debug("timeModalScaleGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))

                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeModalScaleGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.timeModalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeModalScaleGraphicsItem != None.")
                    
                    # Right-click during setting the TimeModalScaleGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.timeModalScaleGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeModalScaleGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.timeModalScaleGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeModalScaleGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:
            
            self.log.debug("Current toolMode is: PriceModalScaleTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar price Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)

                        # Use this Y value.
                        self.clickOnePointF.setY(y)
                    
                    # Create the PriceModalScaleGraphicsItem and
                    # initialize it to the mouse location.
                    self.priceModalScaleGraphicsItem = \
                        PriceModalScaleGraphicsItem()
                    self.priceModalScaleGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)

                    # Set the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.priceModalScaleGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(True)
                    
                    self.priceModalScaleGraphicsItem.setPos(self.clickOnePointF)
                    self.priceModalScaleGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.priceModalScaleGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.priceModalScaleGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.priceModalScaleGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.priceModalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceModalScaleGraphicsItem != None.")
                    
                    # Set the end point of the PriceModalScaleGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar price Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)

                        # Use this Y value.
                        self.clickTwoPointF.setY(y)
                    
                    newEndPointF = \
                        QPointF(self.clickOnePointF.x(),
                                self.clickTwoPointF.y())
                    self.priceModalScaleGraphicsItem.\
                        setEndPointF(newEndPointF)
                    self.priceModalScaleGraphicsItem.normalizeStartAndEnd()

                    # Unset the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.
                    self.priceModalScaleGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(False)
                    
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.priceModalScaleGraphicsItem.getArtifact()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.priceModalScaleGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.priceModalScaleGraphicsItem.sceneBoundingRect()
                    self.log.debug("priceModalScaleGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))

                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceModalScaleGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceModalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceModalScaleGraphicsItem != None.")
                    
                    # Right-click during setting the PriceModalScaleGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.priceModalScaleGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceModalScaleGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceModalScaleGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceModalScaleGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:
            
            self.log.debug("Current toolMode is: TextTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")

                # Create the TextGraphicsItem and initialize it to the
                # mouse location.
                self.textGraphicsItem = TextGraphicsItem()
                self.textGraphicsItem.\
                    loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                self.textGraphicsItem.setPos(self.mapToScene(qmouseevent.pos()))

                # Now create and run a edit dialog for typing in the text.
                dialog = \
                    PriceBarChartTextArtifactEditDialog(\
                        self.textGraphicsItem.getArtifact(),
                        self.scene(),
                        readOnlyFlag=False)
                rv = dialog.exec_()
                
                # If the user accepts the dialog, then add the item,
                # otherwise, delete and remove.
                if rv == QDialog.Accepted:
                    self.log.debug("PriceBarChartTextArtifactEditDialog " +
                                   "accepted.")
                    self.textGraphicsItem.setArtifact(dialog.getArtifact())
                    self.scene().addItem(self.textGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.textGraphicsItem)
                else:
                    self.log.debug("PriceBarChartTextArtifactEditDialog " +
                                   "rejected.")

                self.textGraphicsItem = None
                
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:
            
            self.log.debug("Current toolMode is: PriceTimeInfoTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")

                if self.clickOnePointF == None:
                    
                    self.log.debug("clickOnePointF is None.")

                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # First click sets the position and everything.
                    # Assumes that the text is above the point.
        
                    # Create the PriceTimeInfoGraphicsItem
                    self.priceTimeInfoGraphicsItem = PriceTimeInfoGraphicsItem()
                    self.priceTimeInfoGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                        self.priceBarChartSettings)

                    # Set the flag that indicates that we should draw
                    # a line from the text to the infoPointF.  This is
                    # set to false once we've fully set the item.
                    self.priceTimeInfoGraphicsItem.\
                        setDrawLineToInfoPointFFlag(True)
                    
                    # Set the conversion object as the scene so that it
                    # can do initial calculations for the text to display.
                    self.priceTimeInfoGraphicsItem.\
                        setConvertObj(self.scene())
                    
                    # Location of the graphics item.  This is calculated
                    # below, based on where the used clicked.
                    pos = QPointF()
                
                    # If snap is enabled, then find the closest high, low,
                    # open or close QPointF to the place clicked.
                    infoPointF = self.mapToScene(qmouseevent.pos())
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        # Find if there is a point closer to this
                        # infoPointF related to a PriceBarGraphicsItem.
                        barPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(infoPointF)

                        # If a point was found, then use it as the info point.
                        if barPoint != None:
                            infoPointF = barPoint
                            
                            # Set this also as the first click point,
                            # as if the user clicked perfectly.
                            self.clickOnePointF = infoPointF

                    # Get and modify the artifact.
                    artifact = self.priceTimeInfoGraphicsItem.getArtifact()
                    artifact.setInfoPointF(infoPointF)

                    # Now set the artifact again so we can get an updated
                    # boundingRect size.
                    self.priceTimeInfoGraphicsItem.setArtifact(artifact)
                    boundingRect = self.priceTimeInfoGraphicsItem.boundingRect()

                    # Determine what y pos would be for this new item,
                    # assuming the text will be above the infoPointF.
                    self.priceTimeInfoGraphicsItem.\
                        setTextLabelEdgeYLocation(infoPointF.y())

                    # Set the BirthInfo.
                    birthInfo = self.scene().getBirthInfo()
                    self.priceTimeInfoGraphicsItem.setBirthInfo(birthInfo)
                    
                    # Add the item to the scene.
                    self.scene().addItem(self.priceTimeInfoGraphicsItem)
                    
                elif self.clickOnePointF != None and \
                       self.clickTwoPointF == None and \
                       self.priceTimeInfoGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem != None.")
                    
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    
                    # Turn off the flag that indicates that we should
                    # draw a line from the text to the infoPointF.  It
                    # will now only draw that line when we have the
                    # item selected.
                    self.priceTimeInfoGraphicsItem.\
                        setDrawLineToInfoPointFFlag(False)
                    
                    # Set the position of the item by calling the set
                    # function for the Y location of the edge of the
                    # text.
                    posY = self.clickTwoPointF.y()
                    self.priceTimeInfoGraphicsItem.\
                        setTextLabelEdgeYLocation(posY)

                    # Done settings values, so clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeInfoGraphicsItem = None
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceTimeInfoGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem != None.")
                    
                    # Right-click during setting the priceTimeInfoGraphicsItem
                    # causes the currently edited item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.priceTimeInfoGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeInfoGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceTimeInfoGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:
            
            self.log.debug("Current toolMode is: PriceMeasurementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)
                        
                        # Use this Y value.
                        self.clickOnePointF.setY(y)
                    
                    # Create the PriceMeasurementGraphicsItem and
                    # initialize it to the mouse location.
                    self.priceMeasurementGraphicsItem = \
                        PriceMeasurementGraphicsItem()
                    self.priceMeasurementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.priceMeasurementGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(True)
        
                    self.priceMeasurementGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.priceMeasurementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.priceMeasurementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.priceMeasurementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.priceMeasurementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.priceMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem != None.")
                    
                    # Set the end point of the PriceMeasurementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)
                        
                        # Use this Y value.
                        self.clickTwoPointF.setY(y)
                    
                    self.priceMeasurementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.priceMeasurementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.priceMeasurementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.
                    self.priceMeasurementGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.priceMeasurementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.priceMeasurementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("priceMeasurementGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                                   
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceMeasurementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem != None.")
                    
                    # Right-click during setting the
                    # PriceMeasurementGraphicsItem causes the
                    # currently edited bar count item to be removed
                    # and cleared out.  Temporary variables used are
                    # cleared out too.
                    self.scene().removeItem(self.priceMeasurementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceMeasurementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceMeasurementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:
            
            self.log.debug("Current toolMode is: TimeRetracementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickOnePointF.setX(x)
                    
                    # Create the TimeRetracementGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeRetracementGraphicsItem = \
                        TimeRetracementGraphicsItem()
                    self.timeRetracementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.timeRetracementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
        
                    self.timeRetracementGraphicsItem.setPos(self.clickOnePointF)
                    self.timeRetracementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.timeRetracementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.timeRetracementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.timeRetracementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.timeRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem != None.")
                    
                    # Set the end point of the TimeRetracementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickTwoPointF.setX(x)
                    
                    self.timeRetracementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.timeRetracementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeRetracementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.timeRetracementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.timeRetracementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.timeRetracementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("timeRetracementGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                                   
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeRetracementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.timeRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem != None.")
                    
                    # Right-click during setting the TimeRetracementGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.timeRetracementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeRetracementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.timeRetracementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:
            
            self.log.debug("Current toolMode is: PriceRetracementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar price Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)

                        # Use this Y value.
                        self.clickOnePointF.setY(y)
                    
                    # Create the PriceRetracementGraphicsItem and
                    # initialize it to the mouse location.
                    self.priceRetracementGraphicsItem = \
                        PriceRetracementGraphicsItem()
                    self.priceRetracementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.priceRetracementGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(True)
        
                    self.priceRetracementGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.priceRetracementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.priceRetracementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.priceRetracementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.priceRetracementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.priceRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceRetracementGraphicsItem != None.")
                    
                    # Set the end point of the PriceRetracementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar price Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)

                        # Use this Y value.
                        self.clickTwoPointF.setY(y)
                    
                    self.priceRetracementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.priceRetracementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.priceRetracementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted horizontal lines at the tick areas.
                    self.priceRetracementGraphicsItem.\
                        setDrawHorizontalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.priceRetracementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.priceRetracementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("priceRetracementGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                                   
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceRetracementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceRetracementGraphicsItem != None.")
                    
                    # Right-click during setting the
                    # PriceRetracementGraphicsItem causes the
                    # currently edited bar count item to be removed
                    # and cleared out.  Temporary variables used are
                    # cleared out too.
                    self.scene().removeItem(self.priceRetracementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceRetracementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceRetracementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceRetracementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:
            
            self.log.debug("Current toolMode is: PriceTimeVectorTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X and Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        closestPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(infoPointF)

                        # Use these X and Y values.
                        self.clickOnePointF.setX(closestPoint.x())
                        self.clickOnePointF.setY(closestPoint.y())
                    
                    # Create the PriceTimeVectorGraphicsItem and
                    # initialize it to the mouse location.
                    self.priceTimeVectorGraphicsItem = \
                        PriceTimeVectorGraphicsItem()
                    self.priceTimeVectorGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    self.priceTimeVectorGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.priceTimeVectorGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.priceTimeVectorGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.priceTimeVectorGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.priceTimeVectorGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.priceTimeVectorGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeVectorGraphicsItem != None.")
                    
                    # Set the end point of the PriceTimeVectorGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X and Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        closestPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(infoPointF)

                        # Use these X and Y values.
                        self.clickTwoPointF.setX(closestPoint.x())
                        self.clickTwoPointF.setY(closestPoint.y())
                    
                    self.priceTimeVectorGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.priceTimeVectorGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.priceTimeVectorGraphicsItem.getArtifact()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.priceTimeVectorGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.priceTimeVectorGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("priceTimeVectorGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeVectorGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceTimeVectorGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeVectorGraphicsItem != None.")
                    
                    # Right-click during setting the
                    # PriceTimeVectorGraphicsItem causes the
                    # currently edited bar count item to be removed
                    # and cleared out.  Temporary variables used are
                    # cleared out too.
                    self.scene().removeItem(self.priceTimeVectorGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeVectorGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceTimeVectorGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeVectorGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:
            
            self.log.debug("Current toolMode is: LineSegmentTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X and Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        closestPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(infoPointF)

                        # Use these X and Y values.
                        self.clickOnePointF.setX(closestPoint.x())
                        self.clickOnePointF.setY(closestPoint.y())
                    
                    # Create the LineSegmentGraphicsItem and
                    # initialize it to the mouse location.
                    self.lineSegmentGraphicsItem = \
                        LineSegmentGraphicsItem()
                    self.lineSegmentGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    self.lineSegmentGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.lineSegmentGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.lineSegmentGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.lineSegmentGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.lineSegmentGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.lineSegmentGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "lineSegmentGraphicsItem != None.")
                    
                    # Set the end point of the LineSegmentGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X and Y.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        closestPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(infoPointF)

                        # Use these X and Y values.
                        self.clickTwoPointF.setX(closestPoint.x())
                        self.clickTwoPointF.setY(closestPoint.y())
                    
                    self.lineSegmentGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.lineSegmentGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.lineSegmentGraphicsItem.getArtifact()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.lineSegmentGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.lineSegmentGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("lineSegmentGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.lineSegmentGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.lineSegmentGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "lineSegmentGraphicsItem != None.")
                    
                    # Right-click during setting the
                    # LineSegmentGraphicsItem causes the
                    # currently edited bar count item to be removed
                    # and cleared out.  Temporary variables used are
                    # cleared out too.
                    self.scene().removeItem(self.lineSegmentGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.lineSegmentGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.lineSegmentGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "lineSegmentGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:
            
            self.log.debug("Current toolMode is: OctaveFanTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        originPointF = self.mapToScene(qmouseevent.pos())
                        
                        # Find if there is a point closer to this
                        # originPointF related to a PriceBarGraphicsItem.
                        barPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(originPointF)

                        # If a point was found, then use it as the origin point.
                        if barPoint != None:
                            originPointF = barPoint
                            
                            # Set this also as the first click point,
                            # as if the user clicked perfectly.
                            self.clickOnePointF = originPointF

                    # Create the OctaveFanGraphicsItem and
                    # initialize it to the mouse location.
                    self.octaveFanGraphicsItem = \
                        OctaveFanGraphicsItem()
                    self.octaveFanGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)

                    # Set the conversion object as the scene so that it
                    # can do scaling calculations.
                    self.octaveFanGraphicsItem.\
                        setConvertObj(self.scene())

                    self.octaveFanGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.octaveFanGraphicsItem.\
                        setOriginPointF(self.clickOnePointF)
                    self.octaveFanGraphicsItem.\
                        setLeg1PointF(self.clickOnePointF)
                    self.octaveFanGraphicsItem.\
                        setLeg2PointF(self.clickOnePointF)
                    
                    self.scene().addItem(self.octaveFanGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.octaveFanGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.clickThreePointF == None and \
                    self.octaveFanGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "clickThreePointF == None and " +
                                   "octaveFanGraphicsItem != None.")
                    
                    # Set the click two point of the OctaveFanGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        leg1PointF = self.mapToScene(qmouseevent.pos())
                        
                        # Find if there is a point closer to this
                        # leg1PointF related to a PriceBarGraphicsItem.
                        barPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(leg1PointF)

                        # If a point was found, then use it as the leg1 point.
                        if barPoint != None:
                            leg1PointF = barPoint
                            
                            # Set this also as the second click point,
                            # as if the user clicked perfectly.
                            self.clickTwoPointF = leg1PointF
                    
                    self.octaveFanGraphicsItem.\
                        setLeg1PointF(leg1PointF)
                    self.octaveFanGraphicsItem.\
                        setLeg2PointF(leg1PointF)
                    
                elif self.clickOnePointF != None and \
                    self.clickTwoPointF != None and \
                    self.clickThreePointF == None and \
                    self.octaveFanGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF != None and " +
                                   "clickThreePointF == None and " +
                                   "octaveFanGraphicsItem != None.")
                    
                    # Set the click three point of the OctaveFanGraphicsItem.
                    self.clickThreePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        leg2PointF = self.mapToScene(qmouseevent.pos())
                        
                        # Find if there is a point closer to this
                        # leg2PointF related to a PriceBarGraphicsItem.
                        barPoint = \
                            self.scene().\
                            getClosestPriceBarOHLCViewPoint(leg2PointF)

                        # If a point was found, then use it as the leg2 point.
                        if barPoint != None:
                            leg2PointF = barPoint
                            
                            # Set this also as the third click point,
                            # as if the user clicked perfectly.
                            self.clickThreePointF = leg2PointF
                    
                    self.octaveFanGraphicsItem.\
                        setLeg2PointF(leg2PointF)
                    
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.octaveFanGraphicsItem.\
                        setDrawDottedLinesFlag(False)
                    
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.octaveFanGraphicsItem.getArtifact()
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.octaveFanGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.octaveFanGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("octaveFanGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))

                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.clickThreePointF = None
                    self.octaveFanGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.clickThreePointF == None and \
                   self.octaveFanGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "clickThreePointF == None and " +
                                   "octaveFanGraphicsItem != None.")
                    
                    # Right-click during setting the OctaveFanGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.octaveFanGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.clickThreePointF = None
                    self.octaveFanGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.clickThreePointF == None and \
                     self.octaveFanGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "clickThreePointF == None and " +
                                   "octaveFanGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")

        else:
            self.log.warn("Current toolMode is: UNKNOWN.")

            # For any other mode we don't have specific functionality
            # for, do a context menu if it is a right-click, otherwise
            # just pass the event to the parent to handle.
            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        self.log.debug("Exiting mousePressEvent()")

    def mouseReleaseEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mouseReleaseEvent()")

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            self.log.debug("Current toolMode is: ReadOnlyPointerTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            self.log.debug("Current toolMode is: PointerTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            self.log.debug("Current toolMode is: HandTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            self.log.debug("Current toolMode is: ZoomInTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            self.log.debug("Current toolMode is: ZoomOutTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            self.log.debug("Current toolMode is: BarCountTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            self.log.debug("Current toolMode is: TimeMeasurementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:

            self.log.debug("Current toolMode is: TimeModalScaleTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:

            self.log.debug("Current toolMode is: PriceModalScaleTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            self.log.debug("Current toolMode is: TextTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            self.log.debug("Current toolMode is: PriceTimeInfoTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            self.log.debug("Current toolMode is: PriceMeasurementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            self.log.debug("Current toolMode is: TimeRetracementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:

            self.log.debug("Current toolMode is: PriceRetracementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:

            self.log.debug("Current toolMode is: PriceTimeVectorTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:

            self.log.debug("Current toolMode is: LineSegmentTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:

            self.log.debug("Current toolMode is: OctaveFanTool")
            super().mouseReleaseEvent(qmouseevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            self.log.warn("Current toolMode is: UNKNOWN.")
            super().mouseReleaseEvent(qmouseevent)

        self.log.debug("Exiting mouseReleaseEvent()")

    def mouseMoveEvent(self, qmouseevent):
        """Triggered when the mouse is moving in this widget."""

        # Emit the current mouse location in scene coordinates.
        posScene = self.mapToScene(qmouseevent.pos())
        self.mouseLocationUpdate.emit(posScene.x(), posScene.y())

        
        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if self.clickOnePointF != None and \
                self.barCountGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # BarCountGraphicsItem.
                self.barCountGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if self.clickOnePointF != None and \
                self.timeMeasurementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # TimeMeasurementGraphicsItem.
                self.timeMeasurementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:

            if self.clickOnePointF != None and \
                self.timeModalScaleGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # TimeModalScaleGraphicsItem.
                newEndPointF = \
                    QPointF(pos.x(),
                            self.timeModalScaleGraphicsItem.endPointF.y())
                self.timeModalScaleGraphicsItem.setEndPointF(newEndPointF)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:

            if self.clickOnePointF != None and \
                self.priceModalScaleGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # PriceModalScaleGraphicsItem.
                newEndPointF = \
                    QPointF(self.priceModalScaleGraphicsItem.endPointF.x(),
                            pos.y())
                self.priceModalScaleGraphicsItem.setEndPointF(newEndPointF)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if self.clickOnePointF != None and \
                self.priceTimeInfoGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Set the position of the item by calling the set
                # function for the Y location of the edge of the
                # text.
                posY = pos.y()
                self.priceTimeInfoGraphicsItem.setTextLabelEdgeYLocation(posY)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if self.clickOnePointF != None and \
                self.priceMeasurementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # PriceMeasurementGraphicsItem.
                self.priceMeasurementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            if self.clickOnePointF != None and \
                self.timeRetracementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # TimeRetracementGraphicsItem.
                self.timeRetracementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:

            if self.clickOnePointF != None and \
                self.priceRetracementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # PriceRetracementGraphicsItem.
                self.priceRetracementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:

            if self.clickOnePointF != None and \
                self.priceTimeVectorGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # PriceTimeVectorGraphicsItem.
                self.priceTimeVectorGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:

            if self.clickOnePointF != None and \
                self.lineSegmentGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # LineSegmentGraphicsItem.
                self.lineSegmentGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:

            if self.clickOnePointF != None and \
                self.clickTwoPointF == None and \
                self.clickThreePointF == None and \
                self.octaveFanGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the leg1 and leg2 points of the current
                # OctaveFanGraphicsItem.
                self.octaveFanGraphicsItem.setLeg1PointF(pos)
                self.octaveFanGraphicsItem.setLeg2PointF(pos)
                
            elif self.clickOnePointF != None and \
                 self.clickTwoPointF == None and \
                 self.clickThreePointF == None and \
                 self.octaveFanGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the leg2 point of the current
                # OctaveFanGraphicsItem.
                self.octaveFanGraphicsItem.setLeg2PointF(pos)
                
            else:
                super().mouseMoveEvent(qmouseevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().mouseMoveEvent(qmouseevent)



    def enterEvent(self, qevent):
        """Overwrites the QWidget.enterEvent() function.  

        Whenever the mouse enters the area of this widget, this function
        is called.  I've overwritten this function to change the mouse
        cursor according to what tool mode is currently active.

        Arguments:

        qevent - QEvent object that triggered this function call.
        """

        self.log.debug("Entered enterEvent()")

        # Set the cursor shape/image according to what tool mode the
        # pricebarchart is in.

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:
            pixmap = QPixmap(":/images/rluu/zoomIn.png")
            self.setCursor(QCursor(pixmap))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            pixmap = QPixmap(":/images/rluu/zoomOut.png")
            self.setCursor(QCursor(pixmap))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeModalScaleTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceModalScaleTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceRetracementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeVectorTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['LineSegmentTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['OctaveFanTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.log.warn("Unknown toolMode while in enterEvent().")

        # Allow any other super classes to process the event as well.
        super().enterEvent(qevent)

        self.log.debug("Exiting enterEvent()")

    def leaveEvent(self, qevent):
        """Overwrites the QWidget.leaveEvent() function.  

        Whenever the mouse leaves the area of this widget, this function
        is called.  I've overwritten this function to change the mouse
        cursor from whatever it is currently set to, back to the original
        pointer cursor.

        Arguments:

        qevent - QEvent object that triggered this function call.
        """

        self.log.debug("Entered leaveEvent()")

        # Set the cursor shape/image to the ArrowCursor.
        self.setCursor(QCursor(Qt.ArrowCursor))

        # Allow any other super classes to process the event as well.
        super().leaveEvent(qevent)

        self.log.debug("Exiting leaveEvent()")

