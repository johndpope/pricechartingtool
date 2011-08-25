
# For obtaining the line separator and directory separator.
import os

# For serializing and unserializing objects.
import pickle

# For logging.
import logging

from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For icon images, etc.
import resources

# For dialogs for user input.
from dialogs import *
from widgets import *

# For data objects manipulated in the ui.
from data_objects import BirthInfo
from data_objects import PriceChartDocumentData

# For widgets used in the ui.
from pricebarchart import *
from pricebarspreadsheet import *
from astrologychart import PlanetaryInfoTableWidget

class MainWindow(QMainWindow):
    """The QMainWindow class that is a multiple document interface (MDI)."""

    # Filter for opening files of all types of file extensions.
    allFilesFileFilter = "All files (*)"

    # Default timeout for showing a message in the QStatusBar.
    defaultStatusBarMsgTimeMsec = 4000

    
    def __init__(self, 
                 appName, 
                 appVersion, 
                 appDate, 
                 appAuthor,
                 appAuthorEmail, 
                 parent=None):
        super().__init__(parent)

        self.log = logging.getLogger("ui.MainWindow")

        # Save off the application name, version and date.
        self.appName = appName
        self.appVersion = appVersion
        self.appDate = appDate
        self.appAuthor = appAuthor
        self.appAuthorEmail = appAuthorEmail
        self.appIcon = QIcon(":/images/rluu/appIcon.png")
        
        # Set application details so the we can use QSettings default
        # constructor later.
        QCoreApplication.setOrganizationName(appAuthor)
        QCoreApplication.setApplicationName(appName)

        # Settings attributes that are set when _readSettings() is called.
        self.defaultPriceBarDataOpenDirectory = ""
        self.windowGeometry = QByteArray()
        self.windowState = QByteArray()

        # Create and set up the widgets.
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        # Maps actions in the window menu to changing active document windows.
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].\
            connect(self.mdiArea.setActiveSubWindow)

        # Any updates in window activation will update action objects and
        # the window menu.
        self.mdiArea.subWindowActivated.connect(self._updateActions)
        self.mdiArea.subWindowActivated.connect(self._updateWindowMenu)

        # Create actions, menus, toolbars, statusbar, widgets, etc.
        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

        self._updateActions()
        self._updateWindowMenu()

        self._readSettings()

        self.restoreGeometry(self.windowGeometry)
        self.restoreState(self.windowState)

        self.setWindowTitle(self.appName)
        self.setWindowIcon(self.appIcon)


    def _createActions(self):
        """Creates all the QAction objects that will be mapped to the 
        choices on the menu, toolbar and keyboard shortcuts."""

        ####################
        # Create actions for the File Menu.

        # Create the newChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-new.png")
        self.newChartAction = QAction(icon, "&New", self)
        self.newChartAction.setShortcut("Ctrl+n")
        self.newChartAction.setStatusTip("Create a new Chart file")
        self.newChartAction.triggered.connect(self._newChart)

        # Create the openChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-open.png")
        self.openChartAction = QAction(icon, "&Open", self)
        self.openChartAction.setShortcut("Ctrl+o")
        self.openChartAction.setStatusTip("Open an existing Chart file")
        self.openChartAction.triggered.connect(self._openChart)

        # The closeChartAction is used in the File menu, but created below
        # in the section for the Window menu.

        # Create the saveChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-save.png")
        self.saveChartAction = QAction(icon, "&Save", self)
        self.saveChartAction.setShortcut("Ctrl+s")
        self.saveChartAction.setStatusTip("Save the Chart to disk")
        self.saveChartAction.triggered.connect(self._saveChart)

        # Create the saveAsChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-save-as.png")
        self.saveAsChartAction = QAction(icon, "Save &As...", self)
        self.saveAsChartAction.setStatusTip("Save the Chart as a new file")
        self.saveAsChartAction.triggered.connect(self._saveAsChart)

        # Create the printAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print.png")
        self.printAction = QAction(icon, "&Print", self)
        self.printAction.setShortcut("Ctrl+p")
        self.printAction.setStatusTip("Print the Chart")
        self.printAction.triggered.connect(self._print)

        # Create the printPreviewAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print-preview.png")
        self.printPreviewAction = QAction(icon, "Print Pre&view", self)
        self.printPreviewAction.\
            setStatusTip("Preview the document before printing")
        self.printPreviewAction.triggered.connect(self._printPreview)

        # Create the exitAppAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/system-log-out.png")
        self.exitAppAction = QAction(icon, "E&xit", self)
        self.exitAppAction.setShortcut("Ctrl+q")
        self.exitAppAction.setStatusTip("Exit the application")
        self.exitAppAction.triggered.connect(self._exitApp)

        ####################
        # Create actions for the Edit Menu.

        # Create the editAppPreferencesAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/categories/preferences-system.png")
        self.editAppPreferencesAction = \
            QAction(icon, "Edit Application &Preferences", self)
        self.editAppPreferencesAction.\
            setStatusTip("Edit Application Preferences")
        self.editAppPreferencesAction.triggered.\
            connect(self._editAppPreferences)

        # Create the editBirthInfoAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/apps/internet-web-browser.png")
        self.editBirthInfoAction = QAction(icon, "Edit &Birth Data", self)
        self.editBirthInfoAction.setStatusTip(
                "Edit the birth time and birth location")
        self.editBirthInfoAction.triggered.connect(self._editBirthInfo)

        # Create the editPriceChartDocumentDataAction.
        icon = QIcon(":/images/rluu/gearGreen.png")
        self.editPriceChartDocumentDataAction = \
            QAction(icon, "Edit PriceChartDocument &Data", self)
        self.editPriceChartDocumentDataAction.\
            setStatusTip("Edit PriceChartDocument Data")
        self.editPriceChartDocumentDataAction.triggered.\
            connect(self._editPriceChartDocumentData)
        
        # Create the editPriceBarChartSettingsAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/categories/applications-system.png")
        self.editPriceBarChartSettingsAction = \
            QAction(icon, "Edit PriceBarChart &Settings", self)
        self.editPriceBarChartSettingsAction.\
            setStatusTip("Edit PriceBarChart Settings")
        self.editPriceBarChartSettingsAction.triggered.\
            connect(self._editPriceBarChartSettings)
        
        # Create the editPriceBarChartScalingAction.
        icon = QIcon(":/images/rluu/triangleRuler.png")
        self.editPriceBarChartScalingAction = \
            QAction(icon, "Edit PriceBarChart S&caling", self)
        self.editPriceBarChartScalingAction.\
            setStatusTip("Edit PriceBarChart Scaling")
        self.editPriceBarChartScalingAction.triggered.\
            connect(self._editPriceBarChartScaling)
        

        ####################
        # Create actions for the Tools Menu.

        # Create the ReadOnlyPointerToolAction.
        icon = QIcon(":/images/qt/pointer.png")
        self.readOnlyPointerToolAction = \
            QAction(icon, "Read-Only Pointer Tool", self)
        self.readOnlyPointerToolAction.setStatusTip("Read-Only Pointer Tool")
        self.readOnlyPointerToolAction.setCheckable(True)

        # Create the PointerToolAction.
        icon = QIcon(":/images/rluu/pointerPencil.png")
        self.pointerToolAction = QAction(icon, "Pointer Tool", self)
        self.pointerToolAction.setStatusTip("Pointer Tool")
        self.pointerToolAction.setCheckable(True)

        # Create the HandToolAction.
        icon = QIcon(":/images/rluu/handOpen.png")
        self.handToolAction = QAction(icon, "Hand Tool", self)
        self.handToolAction.setStatusTip("Hand Tool")
        self.handToolAction.setCheckable(True)

        # Create the ZoomInToolAction.
        icon = QIcon(":/images/rluu/zoomInBlue.png")
        self.zoomInToolAction = QAction(icon, "Zoom In Tool", self)
        self.zoomInToolAction.setStatusTip("Zoom In Tool")
        self.zoomInToolAction.setCheckable(True)

        # Create the ZoomOutToolAction.
        icon = QIcon(":/images/rluu/zoomOutBlue.png")
        self.zoomOutToolAction = QAction(icon, "Zoom Out Tool", self)
        self.zoomOutToolAction.setStatusTip("Zoom Out Tool")
        self.zoomOutToolAction.setCheckable(True)

        # Create the BarCountToolAction
        icon = QIcon(":/images/rluu/barCount.png")
        self.barCountToolAction = QAction(icon, "Bar Count Tool", self)
        self.barCountToolAction.setStatusTip("Bar Count Tool")
        self.barCountToolAction.setCheckable(True)

        # Create the TimeMeasurementToolAction
        icon = QIcon(":/images/rluu/timeMeasurement.png")
        self.timeMeasurementToolAction = \
            QAction(icon, "Time Measurement Tool", self)
        self.timeMeasurementToolAction.setStatusTip("Time Measurement Tool")
        self.timeMeasurementToolAction.setCheckable(True)

        # Create the PriceMeasurementToolAction
        icon = QIcon(":/images/rluu/priceMeasurement.png")
        self.priceMeasurementToolAction = \
            QAction(icon, "Price Measurement Tool", self)
        self.priceMeasurementToolAction.setStatusTip("Price Measurement Tool")
        self.priceMeasurementToolAction.setCheckable(True)

        # Create the TimeModalScaleToolAction
        icon = QIcon(":/images/rluu/timeModalScale.png")
        self.timeModalScaleToolAction = \
            QAction(icon, "Time Modal Scale Tool", self)
        self.timeModalScaleToolAction.setStatusTip("Time Modal Scale Tool")
        self.timeModalScaleToolAction.setCheckable(True)

        # Create the PriceModalScaleToolAction
        icon = QIcon(":/images/rluu/priceModalScale.png")
        self.priceModalScaleToolAction = \
            QAction(icon, "Price Modal Scale Tool", self)
        self.priceModalScaleToolAction.setStatusTip("Price Modal Scale Tool")
        self.priceModalScaleToolAction.setCheckable(True)

        # Create the TextToolAction
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/mimetypes/font-x-generic.png")
        self.textToolAction = \
            QAction(icon, "Text Tool", self)
        self.textToolAction.setStatusTip("Text Tool")
        self.textToolAction.setCheckable(True)

        # Create the PriceTimeInfoToolAction
        icon = QIcon(":/images/rluu/priceTimeInfo.png")
        self.priceTimeInfoToolAction = \
            QAction(icon, "Price Time Info Tool", self)
        self.priceTimeInfoToolAction.setStatusTip("Price Time Info Tool")
        self.priceTimeInfoToolAction.setCheckable(True)

        # Create the TimeRetracementToolAction
        icon = QIcon(":/images/rluu/timeRetracement.png")
        self.timeRetracementToolAction = \
            QAction(icon, "Time Retracement Tool", self)
        self.timeRetracementToolAction.setStatusTip("Time Retracement Tool")
        self.timeRetracementToolAction.setCheckable(True)

        # Create the PriceRetracementToolAction
        icon = QIcon(":/images/rluu/priceRetracement.png")
        self.priceRetracementToolAction = \
            QAction(icon, "Price Retracement Tool", self)
        self.priceRetracementToolAction.setStatusTip("Price Retracement Tool")
        self.priceRetracementToolAction.setCheckable(True)

        # Create the PriceTimeVectorToolAction
        icon = QIcon(":/images/rluu/ptv.png")
        self.priceTimeVectorToolAction = \
            QAction(icon, "Price Time Vector Tool", self)
        self.priceTimeVectorToolAction.setStatusTip("Price Time Vector Tool")
        self.priceTimeVectorToolAction.setCheckable(True)

        # Create the LineSegmentToolAction
        icon = QIcon()
        self.lineSegmentToolAction = \
            QAction(icon, "Line Segment Tool", self)
        self.lineSegmentToolAction.setStatusTip("Line Segment Tool")
        self.lineSegmentToolAction.setCheckable(True)

        # Create a QActionGroup because all these tool modes should be
        # exclusive.  
        self.toolActionGroup = QActionGroup(self)
        self.toolActionGroup.setExclusive(True)
        self.toolActionGroup.addAction(self.readOnlyPointerToolAction)
        self.toolActionGroup.addAction(self.pointerToolAction)
        self.toolActionGroup.addAction(self.handToolAction)
        self.toolActionGroup.addAction(self.zoomInToolAction)
        self.toolActionGroup.addAction(self.zoomOutToolAction)
        self.toolActionGroup.addAction(self.barCountToolAction)
        self.toolActionGroup.addAction(self.timeMeasurementToolAction)
        self.toolActionGroup.addAction(self.priceMeasurementToolAction)
        self.toolActionGroup.addAction(self.timeModalScaleToolAction)
        self.toolActionGroup.addAction(self.priceModalScaleToolAction)
        self.toolActionGroup.addAction(self.timeRetracementToolAction)
        self.toolActionGroup.addAction(self.priceRetracementToolAction)
        self.toolActionGroup.addAction(self.textToolAction)
        self.toolActionGroup.addAction(self.priceTimeInfoToolAction)
        self.toolActionGroup.addAction(self.priceTimeVectorToolAction)
        self.toolActionGroup.addAction(self.lineSegmentToolAction)
        self.toolActionGroup.triggered.connect(self._toolsActionTriggered)
            
        # Default to the ReadOnlyPointerTool being checked by default.
        self.readOnlyPointerToolAction.setChecked(True)

        ####################
        # Create actions for the Window menu.

        # Create the closeChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/status/image-missing.png")
        self.closeChartAction = QAction(icon, "&Close", self)
        self.closeChartAction.setShortcut("Ctrl+F4")
        self.closeChartAction.setStatusTip("Close the active window")
        self.closeChartAction.triggered.connect(self._closeChart)

        # Create the closeAllChartsAction.
        self.closeAllChartsAction = QAction("Close &All", self)
        self.closeAllChartsAction.setStatusTip("Close all the windows")
        self.closeAllChartsAction.triggered.connect(
                self.mdiArea.closeAllSubWindows)

        # Create the tileSubWindowsAction.
        self.tileSubWindowsAction = QAction("&Tile", self)
        self.tileSubWindowsAction.setStatusTip("Tile the windows")
        self.tileSubWindowsAction.triggered.connect(
                self.mdiArea.tileSubWindows)

        # Create the cascadeSubWindowsAction.
        self.cascadeSubWindowsAction = QAction("Ca&scade", self)
        self.cascadeSubWindowsAction.setStatusTip("Cascade the windows")
        self.cascadeSubWindowsAction.triggered.connect(
                self.mdiArea.cascadeSubWindows)

        # Create the nextSubWindowAction.
        self.nextSubWindowAction = QAction("Ne&xt", self)
        self.nextSubWindowAction.setStatusTip(
                "Move the focus to the next subwindow")
        self.nextSubWindowAction.triggered.connect(
                self.mdiArea.activateNextSubWindow)

        # Create the previousSubWindowAction.
        self.previousSubWindowAction = QAction("Pre&vious", self)
        self.previousSubWindowAction.setStatusTip(
                "Move the focus to the previous subwindow")
        self.previousSubWindowAction.triggered.connect(
                self.mdiArea.activatePreviousSubWindow)

        # Create a separator for the Window menu.
        self.windowMenuSeparator = QAction(self)
        self.windowMenuSeparator.setSeparator(True)

        # Create a QActionGroup for the list of windows.
        self.windowMenuActionGroup = QActionGroup(self)
        self.windowMenuActionGroup.setExclusive(True)

        ####################
        # Create actions for the Help menu.
        self.aboutAction = QAction(self.appIcon, "&About", self)
        self.aboutAction.\
            setStatusTip("Show information about this application.")
        self.aboutAction.triggered.connect(self._about)

        self.aboutQtAction = \
            QAction(QIcon(":/images/qt/qt-logo.png"), "About &Qt", self)
        self.aboutQtAction.setStatusTip("Show information about Qt.")
        self.aboutQtAction.triggered.connect(self._aboutQt)


    def _createMenus(self):
        """Creates the QMenus and adds them to the QMenuBar of the
        QMainWindow"""

        # Create the File menu.
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newChartAction)
        self.fileMenu.addAction(self.openChartAction)
        self.fileMenu.addAction(self.closeChartAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveChartAction)
        self.fileMenu.addAction(self.saveAsChartAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.printPreviewAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAppAction)

        # Create the Edit menu.
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editAppPreferencesAction)
        self.editMenu.addAction(self.editBirthInfoAction)
        self.editMenu.addAction(self.editPriceChartDocumentDataAction)
        self.editMenu.addAction(self.editPriceBarChartSettingsAction)
        self.editMenu.addAction(self.editPriceBarChartScalingAction)

        # Create the Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.toolsMenu.addAction(self.readOnlyPointerToolAction)
        self.toolsMenu.addAction(self.pointerToolAction)
        self.toolsMenu.addAction(self.handToolAction)
        self.toolsMenu.addAction(self.zoomInToolAction)
        self.toolsMenu.addAction(self.zoomOutToolAction)
        self.toolsMenu.addAction(self.barCountToolAction)
        self.toolsMenu.addAction(self.timeMeasurementToolAction)
        self.toolsMenu.addAction(self.priceMeasurementToolAction)
        self.toolsMenu.addAction(self.timeModalScaleToolAction)
        self.toolsMenu.addAction(self.priceModalScaleToolAction)
        self.toolsMenu.addAction(self.timeRetracementToolAction)
        self.toolsMenu.addAction(self.priceRetracementToolAction)
        self.toolsMenu.addAction(self.textToolAction)
        self.toolsMenu.addAction(self.priceTimeInfoToolAction)
        self.toolsMenu.addAction(self.priceTimeVectorToolAction)
        self.toolsMenu.addAction(self.lineSegmentToolAction)

        # Create the Window menu.
        self.windowMenu = self.menuBar().addMenu("&Window")
        self._updateWindowMenu()

        # Add a separator between the Window menu and the Help menu.
        self.menuBar().addSeparator()

        # Create the Help menu.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)


    def _createToolBars(self):
        """Creates the toolbars used in the application"""

        # Create the File toolbar.
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("fileToolBar")
        self.fileToolBar.addAction(self.newChartAction)
        self.fileToolBar.addAction(self.openChartAction)
        self.fileToolBar.addAction(self.saveChartAction)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.printAction)
        self.fileToolBar.addAction(self.printPreviewAction)

        # Create the Edit toolbar.
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setObjectName("editToolBar")
        self.editToolBar.addAction(self.editAppPreferencesAction)
        self.editToolBar.addAction(self.editBirthInfoAction)
        self.editToolBar.addAction(self.editPriceChartDocumentDataAction)
        self.editToolBar.addAction(self.editPriceBarChartSettingsAction)
        self.editToolBar.addAction(self.editPriceBarChartScalingAction)

        # Create the Tools toolbar.
        self.toolsToolBar = self.addToolBar("Tools")
        self.toolsToolBar.setObjectName("toolsToolBar")
        self.toolsToolBar.addAction(self.readOnlyPointerToolAction)
        self.toolsToolBar.addAction(self.pointerToolAction)
        self.toolsToolBar.addAction(self.handToolAction)
        self.toolsToolBar.addAction(self.zoomInToolAction)
        self.toolsToolBar.addAction(self.zoomOutToolAction)
        self.toolsToolBar.addAction(self.barCountToolAction)
        self.toolsToolBar.addAction(self.timeMeasurementToolAction)
        self.toolsToolBar.addAction(self.priceMeasurementToolAction)
        self.toolsToolBar.addAction(self.timeModalScaleToolAction)
        self.toolsToolBar.addAction(self.priceModalScaleToolAction)
        self.toolsToolBar.addAction(self.timeRetracementToolAction)
        self.toolsToolBar.addAction(self.priceRetracementToolAction)
        self.toolsToolBar.addAction(self.textToolAction)
        self.toolsToolBar.addAction(self.priceTimeInfoToolAction)
        self.toolsToolBar.addAction(self.priceTimeVectorToolAction)
        self.toolsToolBar.addAction(self.lineSegmentToolAction)

    def _createStatusBar(self):
        """Creates the QStatusBar by showing the message "Ready"."""

        self.statusBar().showMessage("Ready")

    def _updateActions(self):
        """Updates the QActions (enable or disable) depending on the
        current state of the application."""

        self.log.debug("Entered _updateActions()")

        priceChartDocument = self.getActivePriceChartDocument()

        # Flag for whether or not a PriceChartDocument is active or not.
        # Initialize to False.
        isActive = False

        if priceChartDocument == None:
            isActive = False
            self.log.debug("Currently active subwindow is: None")
        else:
            isActive = True
            self.log.debug("Currently active subwindow title is: " + 
                           priceChartDocument.title)

        # Set the QActions according to whether it is always True, always
        # False, or dependent on whether a PriceChartDocument is selected.
        self.newChartAction.setEnabled(True)
        self.openChartAction.setEnabled(True)

        self.saveChartAction.setEnabled(isActive)
        self.saveAsChartAction.setEnabled(isActive)
        self.printAction.setEnabled(isActive)
        self.printPreviewAction.setEnabled(isActive)
        self.exitAppAction.setEnabled(True)

        self.editAppPreferencesAction.setEnabled(True)
        self.editBirthInfoAction.setEnabled(isActive)
        self.editPriceChartDocumentDataAction.setEnabled(isActive)
        self.editPriceBarChartSettingsAction.setEnabled(isActive)
        self.editPriceBarChartScalingAction.setEnabled(isActive)

        self.readOnlyPointerToolAction.setEnabled(isActive)
        self.pointerToolAction.setEnabled(isActive)
        self.handToolAction.setEnabled(isActive)
        self.zoomInToolAction.setEnabled(isActive)
        self.zoomOutToolAction.setEnabled(isActive)
        self.barCountToolAction.setEnabled(isActive)
        self.timeMeasurementToolAction.setEnabled(isActive)
        self.timeModalScaleToolAction.setEnabled(isActive)
        self.priceModalScaleToolAction.setEnabled(isActive)
        self.textToolAction.setEnabled(isActive)
        self.priceTimeInfoToolAction.setEnabled(isActive)
        self.priceMeasurementToolAction.setEnabled(isActive)
        self.timeRetracementToolAction.setEnabled(isActive)
        self.priceRetracementToolAction.setEnabled(isActive)
        self.priceTimeVectorToolAction.setEnabled(isActive)
        self.lineSegmentToolAction.setEnabled(isActive)

        self.closeChartAction.setEnabled(isActive)
        self.closeAllChartsAction.setEnabled(isActive)
        self.tileSubWindowsAction.setEnabled(isActive)
        self.cascadeSubWindowsAction.setEnabled(isActive)
        self.nextSubWindowAction.setEnabled(isActive)
        self.previousSubWindowAction.setEnabled(isActive)

        self.aboutAction.setEnabled(True)
        self.aboutQtAction.setEnabled(True)

        # Depending on what ToolMode QAction is checked,
        # set the priceChartDocument to be in that mode.
        if isActive:
            if self.readOnlyPointerToolAction.isChecked():
                priceChartDocument.toReadOnlyPointerToolMode()
            elif self.pointerToolAction.isChecked():
                priceChartDocument.toPointerToolMode()
            elif self.handToolAction.isChecked():
                priceChartDocument.toHandToolMode()
            elif self.zoomInToolAction.isChecked():
                priceChartDocument.toZoomInToolMode()
            elif self.zoomOutToolAction.isChecked():
                priceChartDocument.toZoomOutToolMode()
            elif self.barCountToolAction.isChecked():
                priceChartDocument.toBarCountToolMode()
            elif self.timeMeasurementToolAction.isChecked():
                priceChartDocument.toTimeMeasurementToolMode()
            elif self.timeModalScaleToolAction.isChecked():
                priceChartDocument.toTimeModalScaleToolMode()
            elif self.priceModalScaleToolAction.isChecked():
                priceChartDocument.toPriceModalScaleToolMode()
            elif self.textToolAction.isChecked():
                priceChartDocument.toTextToolMode()
            elif self.priceTimeInfoToolAction.isChecked():
                priceChartDocument.toPriceTimeInfoToolMode()
            elif self.priceMeasurementToolAction.isChecked():
                priceChartDocument.toPriceMeasurementToolMode()
            elif self.timeRetracementToolAction.isChecked():
                priceChartDocument.toTimeRetracementToolMode()
            elif self.priceRetracementToolAction.isChecked():
                priceChartDocument.toPriceRetracementToolMode()
            elif self.priceTimeVectorToolAction.isChecked():
                priceChartDocument.toPriceTimeVectorToolMode()
            elif self.lineSegmentToolAction.isChecked():
                priceChartDocument.toLineSegmentToolMode()
            else:
                self.log.warn("No ToolMode QAction is currently selected!")


        self.log.debug("Exiting _updateActions()")

    def _updateWindowMenu(self):
        """Updates the Window menu according to which documents are open
        currently.
        """

        self.log.debug("Entered _updateWindowMenu()")

        for action in self.windowMenuActionGroup.actions():
            self.windowMenuActionGroup.removeAction(action)

        # Clear the Window menu and re-add all the standard actions that
        # always show up.
        self.windowMenu.clear()

        self.windowMenu.addAction(self.nextSubWindowAction)
        self.windowMenu.addAction(self.previousSubWindowAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.closeChartAction)
        self.windowMenu.addAction(self.closeAllChartsAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileSubWindowsAction)
        self.windowMenu.addAction(self.cascadeSubWindowsAction)
        self.windowMenu.addAction(self.windowMenuSeparator)

        # Get the list of subwindows.
        subwindows = self.mdiArea.subWindowList()

        if len(subwindows) > 0:
            self.windowMenuSeparator.setVisible(True)
        else:
            self.windowMenuSeparator.setVisible(False)

        # j is the counter for the document list in the Menu.
        j = 1

        # i is the index into the subwindows available.
        # Some of these subwindows may not be PriceChartDocuments, or
        # things we know how to get a name/title/filename for.
        for i in range(len(subwindows)):
            subwindow = subwindows[i]

            # Number windows only if it is a PriceChartDocument.
            if isinstance(subwindow, PriceChartDocument) == True:
                priceChartDocument = subwindow

                # Build the text that will go in the menu's QAction.
                # Here we will have a short-cut (underscore) only if
                # the window count is single digits.
                text = ""
                if j < 10:
                    text += "&"
                text += "{} {}".format(j, priceChartDocument.title)

                # Create the action.
                action = QAction(text, self)
                action.setCheckable(True)

                # Add the action to the QActionGroup.
                self.windowMenuActionGroup.addAction(action)

                # Add the action to the menu.
                self.windowMenu.addAction(action)

                # Set the action as checked if it is the active
                # PriceChartDocument.
                if priceChartDocument == self.getActivePriceChartDocument():
                    action.setChecked(True)
                else:
                    action.setChecked(False)

                # Add the action to the signal mapper that will connect
                # this action being triggered to the related 
                # priceChartDocument.
                self.windowMapper.setMapping(action, priceChartDocument)
                action.triggered.connect(self.windowMapper.map)
                
                # Increment counter for the window number in the Window
                # menu.
                j += 1
            else:
                self.log.debug("Currently only supporting windows that " + 
                               "are PriceChartDocument types only.")

        self.log.debug("Exiting _updateWindowMenu()")

    def _addSubWindow(self, widget):
        """Adds a subwindow to the QMdiArea.  This subwindow is a
        QMdiSubwindow created with the given QWidget 'widget'.
        'widget' may be a QWidget or a QMdiSubWindow.
        After adding the subwindow, the menus are updated appropriately.
        """

        self.log.debug("Entered _addSubWindow()")

        mdiSubWindow = self.mdiArea.addSubWindow(widget)
        mdiSubWindow.show()

        # Set the active subwindow so that subsequent update functions can
        # be called via signals-and-slots.
        self.mdiArea.setActiveSubWindow(mdiSubWindow)

        self.log.debug("Exiting _addSubWindow()")

    def getActivePriceChartDocument(self):
        """Returns a reference to the currently selected
        PriceChartDocument.  If no PriceChartDocument is selected 
        (nothing selected, or some other kind of document selected), 
        then None is returned.
        """

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            return subwindow
        else:
            return None


    def _readSettings(self):
        """
        Reads in QSettings values for preferences and default values.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _readSettings()")

        # Preference settings.
        settings = QSettings() 

        # Window geometry.
        self.windowGeometry = \
            settings.value("ui/MainWindow/windowGeometry")
        if self.windowGeometry == None:
            self.windowGeometry = QByteArray()
            
        # Window state.
        self.windowState = \
            settings.value("ui/MainWindow/windowState")
        if self.windowState == None:
            self.windowState = QByteArray()


        self.log.debug("Exiting _readSettings()")

    def _writeSettings(self):
        """
        Writes current settings values to the QSettings object.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _writeSettings()")

        # Preference settings.
        settings = QSettings() 

        # Only write the settings if the value has changed.

        # Window geometry.
        if settings.value("ui/MainWindow/windowGeometry") != \
                self.saveGeometry():

            settings.setValue("ui/MainWindow/windowGeometry", 
                              self.saveGeometry())

        # Window state.
        if settings.value("ui/MainWindow/windowState") != self.saveState():
            settings.setValue("ui/MainWindow/windowState", self.saveState())


        self.log.debug("Exiting _writeSettings()")

    def _newChart(self):
        """Opens a PriceChartDocumentWizard to load information for a new
        price chart.
        """

        self.log.debug("Entered _newChart()")

        wizard = PriceChartDocumentWizard()
        returnVal = wizard.exec_() 

        if returnVal == QDialog.Accepted:
            self.log.debug("PriceChartDocumentWizard accepted")

            # Debug output:
            self.log.debug("Data filename is: " + \
                           wizard.field("dataFilename"))
            self.log.debug("Data num lines to skip is: {}".\
                format(wizard.field("dataNumLinesToSkip")))
            self.log.debug("Timezone is: " + wizard.field("timezone"))
            self.log.debug("Description is: " + wizard.field("description"))


            # Create the document data.
            priceChartDocumentData = PriceChartDocumentData()

            # Load data into it.
            priceChartDocumentData.\
                loadWizardData(wizard.getPriceBars(),
                               wizard.field("dataFilename"),
                               wizard.field("dataNumLinesToSkip"),
                               wizard.field("timezone"),
                               wizard.field("description"))

            # Create a PriceChartDocument with the data.
            priceChartDocument = PriceChartDocument()
            priceChartDocument.\
                setPriceChartDocumentData(priceChartDocumentData)

            # Connect the signal for updating the status bar message.
            priceChartDocument.statusMessageUpdate[str].\
                connect(self.showInStatusBar)

            # Add this priceChartDocument to the list of subwindows
            self._addSubWindow(priceChartDocument)

        else:
            self.log.debug("PriceChartDocumentWizard rejected")


        self.log.debug("Exiting _newChart()")

    def _openChart(self):
        """Interactive dialogs to open an existing PriceChartDocument.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _openChart()")

        # Set filters for what files are displayed.
        filters = \
            PriceChartDocument.fileFilter + ";;" + \
            MainWindow.allFilesFileFilter

        # Directory location default for the file open dialogs for
        # PriceChartDocument.
        settings = QSettings()
        defaultPriceChartDocumentOpenDirectory = \
            settings.value("ui/defaultPriceChartDocumentOpenDirectory", "")

        filename = \
            QFileDialog.\
                getOpenFileName(self, 
                                "Open PriceChartDocument File",
                                defaultPriceChartDocumentOpenDirectory,
                                filters)

        if filename != "":
            # Okay, so the person chose a file that is non-empty.  
            # See if this filename has already been opened in another
            # PriceChartDocument.  If this is so, prompt to make sure the
            # user wants to open two PriceChartDocuments that point to the
            # same file.  
            filenameAlreadyOpened = False

            # Get the list of subwindows.
            subwindows = self.mdiArea.subWindowList()

            # i is the index into the subwindows available.
            # Some of these subwindows may not be PriceChartDocuments, or
            # things we know how to get a name/title/filename for.
            for i in range(len(subwindows)):
                subwindow = subwindows[i]

                if isinstance(subwindow, PriceChartDocument) == True:
                    priceChartDocument = subwindow

                    if priceChartDocument.filename == filename:
                        filenameAlreadyOpened = True

            if filenameAlreadyOpened == True:
                # Prompt to make sure the user wants to open
                # another PriceChartDocument with the same
                # filename.
                title = "File Already Open"
                text = "The filename you have selected is already open " + \
                       "in another subwindow." + os.linesep + os.linesep + \
                       "Do you still want to open this file?"
                buttons = (QMessageBox.Yes | QMessageBox.No)
                defaultButton = QMessageBox.No

                buttonClicked = \
                    QMessageBox.warning(self, title, text, buttons, 
                                        defaultButton)

                if buttonClicked == QMessageBox.No:
                    # The user doesn't want to load this file.
                    # Exit this function.
                    return
            
            # Load the file.

            # Create the subwindow.
            priceChartDocument = PriceChartDocument()

            # Try to load the file data into the subwindow.
            loadSuccess = \
                priceChartDocument.\
                    unpicklePriceChartDocumentDataFromFile(filename)

            if loadSuccess == True:
                # Load into the object was successful.  

                # Connect the signal for updating the status bar message.
                priceChartDocument.statusMessageUpdate[str].\
                    connect(self.showInStatusBar)

                # Now Add this priceChartDocument to the list of subwindows
                self._addSubWindow(priceChartDocument)

                # Update the statusbar to tell what file was opened.
                statusBarMessage = \
                    "Opened PriceChartDocument {}.".format(filename)

                self.showInStatusBar(statusBarMessage)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # Compare the directory of the file chosen with the
                # QSettings value for the default open location.  
                # If they are different, then set a new default.
                if directory != defaultPriceChartDocumentOpenDirectory:
                    settings.\
                        setValue("ui/defaultPriceChartDocumentOpenDirectory",
                                 directory)
            else:
                # Load failed.  Tell the user via the statusbar.
                statusBarMessage = \
                    "Open operation failed.  " + \
                    "Please see the log file for why."

                self.showInStatusBar(statusBarMessage)
        else:
            self.log.debug("_openChart(): " +
                           "No filename was selected for opening.")

        self.log.debug("Exiting _openChart()")

    def _closeChart(self):
        """Attempts to closes the current QMdiSubwindow.  If things should
        be saved, dialogs will be brought up to get that to happen.
        """

        self.log.debug("Entered _closeChart()")

        subwindow = self.mdiArea.currentSubWindow()

        subwindow.close()

        self.log.debug("Exiting _closeChart()")

    def _saveChart(self):
        """Saves the current QMdiSubwindow.
        
        Returns True if the save action suceeded, False otherwise.
        """

        self.log.debug("Entered _saveChart()")

        # Return value.
        rv = False

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            priceChartDocument = subwindow

            rv = priceChartDocument.saveChart()
        else:
            self.log.warn("Saving this QMdiSubwindow type is not supported.")
            rv = False
            
        self.log.debug("Exiting _saveChart() with rv == {}".format(rv))
        return rv

    def _saveAsChart(self):
        """Saves the current QMdiSubwindow to a new file.
        
        Returns True if the save action suceeded, False otherwise.
        """

        self.log.debug("Entered _saveAsChart()")

        # Return value.
        rv = False

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            priceChartDocument = subwindow

            rv = priceChartDocument.saveAsChart()
        else:
            self.log.warn("'Save As' for this QMdiSubwindow type " + 
                          "is not supported.")
            rv = False
            
        self.log.debug("Exiting _saveAsChart() with rv == {}".format(rv))
        return rv

    def showInStatusBar(self, text):
        """Shows the given text in the MainWindow status bar for
        timeoutMSec milliseconds.
        """

        self.statusBar().showMessage(text, 
                                     MainWindow.defaultStatusBarMsgTimeMsec)

    def _print(self):
        """Opens up a dialog for printing the current selected document."""

        self.log.debug("Entered _print()")
        # TODO: implement this _print() function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        self.log.debug("Exiting _print()")


    def _printPreview(self):
        """Opens up a dialog for previewing the current selected document
        for printing.
        """

        self.log.debug("Entered _printPreview()")
        # TODO: implement this _printPreview() function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        self.log.debug("Exiting _printPreview()")

    def closeEvent(self, closeEvent):
        """Attempts to close the QMainWindow.  Does any cleanup necessary."""

        self.log.debug("Entered closeEvent()")

        # Flag that indicates that we should exit. 
        shouldExit = True
        
        # Get the list of subwindows.
        subwindows = self.mdiArea.subWindowList()

        # Go through each subwindow and try to close each.
        for subwindow in subwindows:
            subwindowClosed = subwindow.close()

            # If a subwindow is not closed (i.e., the user clicked
            # cancel), then we will not exit the application.
            if subwindowClosed == False:
                shouldExit = False
                break


        # Accept the close event if the flag is set.
        if shouldExit == True:
            self.log.debug("Accepting close event.")

            # Save application settings/preferences.
            self._writeSettings()

            closeEvent.accept()
        else:
            self.log.debug("Ignoring close event.")

            closeEvent.ignore()

        self.log.debug("Exiting closeEvent()")

    def _exitApp(self):
        """Exits the app by trying to close all windows."""

        self.log.debug("Entered _exitApp()")

        qApp.closeAllWindows()

        self.log.debug("Exiting _exitApp()")

    def _editAppPreferences(self):
        """Opens up a dialog for editing the application-wide preferences.
        These values are saved via QSettings."""

        self.log.debug("Entered _editAppPreferences()")

        dialog = AppPreferencesEditDialog()

        retVal = dialog.exec_()

        if retVal == QDialog.Accepted:
            self.log.debug("AppPreferencesDialog accepted")
        else:
            self.log.debug("AppPreferencesDialog rejected")

        self.log.debug("Exiting _editAppPreferences()")

    def _editBirthInfo(self):
        """Opens up a BirthInfoEditDialog for editing the BirthInfo of the
        current active PriceChartDocument.
        """

        self.log.debug("Entered _editBirthInfo()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the BirthInfo.
            birthInfo = priceChartDocument.getBirthInfo()

            # Create a dialog to edit the birth info.
            dialog = BirthInfoEditDialog(birthInfo)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("BirthInfoEditDialog accepted.  Data is: " + \
                               dialog.getBirthInfo().toString())
                birthInfo = dialog.getBirthInfo()
                priceChartDocument.setBirthInfo(birthInfo)
            else:
                self.log.debug("BirthInfoEditDialog rejected.  " + \
                               "Doing nothing more.")
        else:
            self.log.error("Tried to edit the birth info when either no " +
                           "PriceChartDocument is selected, or some " +
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editBirthInfo()")

    def _editPriceChartDocumentData(self):
        """Opens up a PriceChartDocumentDataEditDialog to edit the
        currently open PriceChartDocument's backing data object.

        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceChartDocumentData()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceChartDocumentData object.
            priceChartDocumentData = \
                priceChartDocument.getPriceChartDocumentData()

            # Create a dialog to edit the PriceBarChartSettings.
            dialog = PriceChartDocumentDataEditDialog(priceChartDocumentData)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceChartDocumentDataEditDialog accepted.")

                # Reload the entire PriceChartDocument.
                priceChartDocument.\
                    setPriceChartDocumentData(priceChartDocumentData)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceChartDocumentDataEditDialog rejected.")
        else:
            self.log.error("Tried to edit the PriceChartDocumentData " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceChartDocumentData()")

        # TODO:  write this function.

    def _editPriceBarChartSettings(self):
        """Opens up a PriceBarChartSettingsEditDialog to edit
        the PriceBarChartSettings associated with the current active
        PriceChartDocument in the in the UI.  
        
        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceBarChartSettings()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceBarChartSettings object.
            priceBarChartSettings = \
                priceChartDocument.getPriceChartDocumentData().\
                    priceBarChartSettings

            # Create a dialog to edit the PriceBarChartSettings.
            dialog = PriceBarChartSettingsEditDialog(priceBarChartSettings)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceBarChartSettingsEditDialog accepted.")

                # Apply the settings changes to the PriceChartDocument.
                # This should trigger a redraw of everything in the chart.
                priceChartDocument.\
                    applyPriceBarChartSettings(priceBarChartSettings)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceBarChartSettingsEditDialog rejected." + \
                               "  Doing nothing more.")
        else:
            self.log.error("Tried to edit the PriceBarChartSettings " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceBarChartSettings()")


    def _editPriceBarChartScaling(self):
        """Opens up a PriceBarChartScalingsListEditDialog to edit
        the PriceBarChartScaling associated with the current active
        PriceChartDocument in the in the UI.  
        
        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceBarChartScaling()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceBarChartSettings object.
            priceBarChartSettings = \
                priceChartDocument.getPriceChartDocumentData().\
                    priceBarChartSettings

            # Get the list of scalings and the index of the one that is
            # currently applied.
            scalings = \
                priceBarChartSettings.priceBarChartGraphicsViewScalings
            index = \
                priceBarChartSettings.priceBarChartGraphicsViewScalingsIndex

            # Create a dialog to edit the PriceBarChart's list of scalings
            # and which one is currently applied.
            dialog = PriceBarChartScalingsListEditDialog(scalings, index)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceBarChartScalingsListEditDialog " + \
                               "accepted.")

                # Get the new values from the dialog.
                scalings = dialog.getPriceBarChartScalings()
                index = dialog.getPriceBarChartScalingsIndex()

                # Set the scaling and index into the PriceBarChartSettings.
                priceBarChartSettings.\
                    priceBarChartGraphicsViewScalings = scalings
                priceBarChartSettings.\
                    priceBarChartGraphicsViewScalingsIndex = index

                # Apply the settings changes to the PriceChartDocument.
                # This should trigger a redraw of everything in the chart.
                priceChartDocument.\
                    applyPriceBarChartSettings(priceBarChartSettings)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceBarChartScalingsListEditDialog " + \
                               "rejected.  Doing nothing more.")
        else:
            self.log.error("Tried to edit the PriceBarChart scaling " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceBarChartScaling()")

    def _toolsActionTriggered(self, qaction):
        """Slot function that is called when a Tools menu QAction is
        selected/activated.  This changes the Tools mode to whatever the
        new selection is.
        
        Arguments:
        qaction - Reference to the QAction that was triggered.
        """

        self.log.debug("Entered _toolsActionTriggered()")

        # Tool actions only make sense to be triggered if there is a
        # PriceChartDocument open and active.  
        # Check to make sure that is true.
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        if qaction == self.readOnlyPointerToolAction:
            self.log.debug("readOnlyPointerToolAction triggered.")
            pcd.toReadOnlyPointerToolMode()
        elif qaction == self.pointerToolAction:
            self.log.debug("pointerToolAction triggered.")
            pcd.toPointerToolMode()
        elif qaction == self.handToolAction:
            self.log.debug("handToolAction triggered.")
            pcd.toHandToolMode()
        elif qaction == self.zoomInToolAction:
            self.log.debug("zoomInToolAction triggered.")
            pcd.toZoomInToolMode()
        elif qaction == self.zoomOutToolAction:
            self.log.debug("zoomOutToolAction triggered.")
            pcd.toZoomOutToolMode()
        elif qaction == self.barCountToolAction:
            self.log.debug("barCountToolAction triggered.")
            pcd.toBarCountToolMode()
        elif qaction == self.timeMeasurementToolAction:
            self.log.debug("timeMeasurementToolAction triggered.")
            pcd.toTimeMeasurementToolMode()
        elif qaction == self.timeModalScaleToolAction:
            self.log.debug("timeModalScaleToolAction triggered.")
            pcd.toTimeModalScaleToolMode()
        elif qaction == self.priceModalScaleToolAction:
            self.log.debug("priceModalScaleToolAction triggered.")
            pcd.toPriceModalScaleToolMode()
        elif qaction == self.textToolAction:
            self.log.debug("textToolAction triggered.")
            pcd.toTextToolMode()
        elif qaction == self.priceTimeInfoToolAction:
            self.log.debug("priceTimeInfoToolAction triggered.")
            pcd.toPriceTimeInfoToolMode()
        elif qaction == self.priceMeasurementToolAction:
            self.log.debug("priceMeasurementToolAction triggered.")
            pcd.toPriceMeasurementToolMode()
        elif qaction == self.timeRetracementToolAction:
            self.log.debug("timeRetracementToolAction triggered.")
            pcd.toTimeRetracementToolMode()
        elif qaction == self.priceRetracementToolAction:
            self.log.debug("priceRetracementToolAction triggered.")
            pcd.toPriceRetracementToolMode()
        elif qaction == self.priceTimeVectorToolAction:
            self.log.debug("priceTimeVectorToolAction triggered.")
            pcd.toPriceTimeVectorToolMode()
        elif qaction == self.lineSegmentToolAction:
            self.log.debug("lineSegmentToolAction triggered.")
            pcd.toLineSegmentToolMode()
        else:
            self.log.warn("Unknown Tools QAction selected!  " + \
                "There might be something wrong with the code, or " + \
                "I maybe forgot to add a qaction type.")
            
        self.log.debug("Exiting _toolsActionTriggered()")

    def _about(self):
        """Opens a popup window displaying information about this
        application.
        """

        endl = os.linesep

        title = "About"

        message = self.appName + endl + \
                  endl + \
                  self.appName + " is a PyQt application that " + \
                  "is a research tool for the study of the financial " + \
                  "markets." + \
                  endl + \
                  endl + \
                  "Version: " + self.appVersion + endl + \
                  "Released: " + self.appDate + endl + \
                  endl + \
                  "Author: " + self.appAuthor + endl + \
                  "Email: " + self.appAuthorEmail

        QMessageBox.about(self, title, message)

    def _aboutQt(self):
        """Opens a popup window displaying information about the Qt
        toolkit used in this application.
        """

        title = "About Qt"
        QMessageBox.aboutQt(self, title)


class PriceChartDocument(QMdiSubWindow):
    """QMdiSubWindow in the QMdiArea.  This window allows a user to 
    view and edit the data contained in a PriceChartDocumentData object.
    """

    # Initialize the sequence number for untitled documents.
    untitledDocSequenceNum = 1

    # File extension.
    fileExtension = ".pcd"

    # File filter.
    fileFilter = "PriceChartDocument files (*" + fileExtension + ")"

    # Modified-file string that is displayed in the window title after the
    # filename.
    modifiedFileStr = " (*)"

    # Signal emitted when the object wants to display something to the
    # status bar.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Creates the QMdiSubWindow with the internal widgets,
        and loads the given PriceChartDocumentData object.
        """
        super().__init__(parent)

        self.log = logging.getLogger("ui.PriceChartDocument")
        self.log.debug("Entered PriceChartDocument()")

        
        # Create internal data attributes.
        self.priceChartDocumentData = PriceChartDocumentData()

        self.dirtyFlag = True
        self.isUntitled = True
        self.filename = ""

        self.title = \
            "Untitled{}".\
                format(PriceChartDocument.untitledDocSequenceNum) + \
            PriceChartDocument.fileExtension +  \
            PriceChartDocument.modifiedFileStr 
        PriceChartDocument.untitledDocSequenceNum += 1

        # Create the internal widget(s).
        self.widgets = PriceChartDocumentWidget()
        self.setWidget(self.widgets)

        # According to the Qt QMdiArea documentation:
        # 
        #   When you create your own subwindow, you must set the
        #   Qt.WA_DeleteOnClose  widget attribute if you want the window to
        #   be deleted when closed in the MDI area. If not, the window will
        #   be hidden and the MDI area will not activate the next subwindow.
        #
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setWindowTitle(self.title)

        # Connect signals and slots.
        self.widgets.priceChartDocumentWidgetChanged.\
            connect(self._handlePriceChartDocumentWidgetChanged)
        self.widgets.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
        self.log.debug("Exiting PriceChartDocument()")

    def picklePriceChartDocumentDataToFile(self, filename):
        """Pickles the internal PriceChartDocumentData object to the given
        filename.  If the file currently exists, it will be overwritten.

        Returns True if the write operation succeeded without problems.
        """

        self.log.debug("Entered picklePriceChartDocumentDataToFile()")

        # Return value.
        rv = True

        # Get the internal PriceChartDocumentData.
        priceChartDocumentData = self.getPriceChartDocumentData()

        # Pickle to file.
        with open(filename, "wb") as fh:
            try:
                pickle.dump(priceChartDocumentData, fh) 
                rv = True
            except pickle.PickleError as pe:
                self.log.error("Error while pickling a " +
                               "PriceChartDocumentData to file " + 
                               filename + 
                               ".  Error is: {}".format(pe) +
                               ".  PriceChartDocumentData object " + 
                               "has the following info: " + 
                               priceChartDocumentData.toString())
                rv = False

        self.log.debug("Exiting picklePriceChartDocumentDataToFile(), " + \
                       "rv = {}".format(rv))
        return rv

    def unpicklePriceChartDocumentDataFromFile(self, filename):
        """Un-Pickles a PriceChartDocumentData object from file.
        The PriceChartDocumentData obtained is then set to the internal
        PriceChartDocumentData.

        Returns True if the operation succeeded without problems.
        """

        self.log.debug("Entered unpicklePriceChartDocumentDataFromFile()")

        # Return value.
        rv = False

        # Get the PriceChartDocumentData from filename.
        try:
            with open(filename, "rb") as fh:
                try:
                    priceChartDocumentData = pickle.load(fh)

                    # Verify it is a PriceChartDocumentData object.
                    if isinstance(priceChartDocumentData, 
                                  PriceChartDocumentData) == True:
                        self.setPriceChartDocumentData(priceChartDocumentData)
                        self.setFilename(filename)
                        self.setDirtyFlag(False)
                        rv = True
                    else:
                        # Print error message.
                        self.log.error("Cannot load this object.  " + 
                                       "The object unpickled from file " + 
                                       filename + " is not a " + 
                                       "PriceChartDocumentData.")
                        rv = False
                except pickle.UnpicklingError as upe:
                    self.log.error("Error while unpickling a " +
                                   "PriceChartDocumentData from file " + 
                                   filename + 
                                   ".  Error is: {}".format(upe))
                    rv = False
        except IOError as e:
            self.log.error("IOError while trying to open a file: {}".\
                format(e))

            rv = False

            QMessageBox.warning(None, 
                                "Error", 
                                "IOError exception: " + 
                                os.linesep + os.linesep + "{}".format(e))

        self.log.debug("Exiting unpicklePriceChartDocumentDataFromFile(), " +
                       "rv = {}".format(rv))
        return rv

    def setFilename(self, filename):
        """Sets the filename of the document.  This also sets the window
        title as well.
        """

        self.log.debug("Entered setFilename()")

        if self.filename != filename:
            self.log.debug("Updating filename to: " + filename)

            self.filename = filename

            self.isUntitled = False

            # The title is set to the filename without the path.
            loc = self.filename.rfind(os.sep)
            loc += len(os.sep)

            self.title = self.filename[loc:]
            self.setWindowTitle(self.title)
        else:
            self.log.debug("Filename didn't change.  No need to update.")

        self.log.debug("Exiting setFilename()")

    def getFilename(self):
        """Returns the currently set filename.  This is an empty str if
        the filename has not been set yet.
        """

        return self.filename


    def getPriceChartDocumentData(self):
        """Obtains all the data in the widgets and puts it into the
        internal PriceChartDocumentData object, then returns that object.

        Returns: PriceChartDocumentData object that holds all the
        information about this document as stored in the widgets.
        """

        self.log.debug("Entered getPriceChartDocumentData()")

        
        # The PriceBars reference in self.priceChartDocumentData
        # should hold the internal bars, since this is the reference that
        # passed into the child widgets to load stuff.  If there are bars
        # added (via dialogs or some other means), the list that 
        # the reference is pointing to should have those new bars.  
        # The same should be true with the BirthInfo.
        # Therefore, all we need to retrieve is the pricebarchart
        # artifacts and the settings objects.

        self.priceChartDocumentData.priceBarChartArtifacts = \
            self.widgets.getPriceBarChartArtifacts()

        self.priceChartDocumentData.priceBarChartSettings = \
            self.widgets.getPriceBarChartSettings()

        self.priceChartDocumentData.priceBarSpreadsheetSettings = \
            self.widgets.getPriceBarSpreadsheetSettings()

        self.log.debug("Exiting getPriceChartDocumentData()")

        return self.priceChartDocumentData

    def setPriceChartDocumentData(self, priceChartDocumentData):
        """Stores the PriceChartDocumentData and sets the widgets with the
        information it requires.
        """

        self.log.\
            debug("Entered setPriceChartDocumentData()")

        # Store the object reference.
        self.priceChartDocumentData = priceChartDocumentData
            
        self.log.debug("Number of priceBars is: {}".\
                format(len(self.priceChartDocumentData.priceBars)))

        # Clear all the old data.
        self.widgets.clearAllPriceBars()
        self.widgets.clearAllPriceBarChartArtifacts()

        # Set the description text.
        self.widgets.\
            setDescriptionText(self.priceChartDocumentData.description)
        
        # Set the timezone.
        self.widgets.setTimezone(self.priceChartDocumentData.locationTimezone)

        # Set the birth info.
        self.widgets.setBirthInfo(self.priceChartDocumentData.birthInfo)

        # Load pricebars.
        priceBars = self.priceChartDocumentData.priceBars
        self.widgets.loadPriceBars(priceBars)

        # Apply the settings objects.
        priceBarChartSettings = \
            self.priceChartDocumentData.priceBarChartSettings
        priceBarSpreadsheetSettings = \
            self.priceChartDocumentData.priceBarSpreadsheetSettings
        self.widgets.applyPriceBarChartSettings(priceBarChartSettings)
        self.widgets.\
            applyPriceBarSpreadsheetSettings(priceBarSpreadsheetSettings)

        # Load the chart artifacts.
        priceBarChartArtifacts = \
            self.priceChartDocumentData.priceBarChartArtifacts
        self.widgets.loadPriceBarChartArtifacts(priceBarChartArtifacts)
        
        # By default, set the flag as dirty.  
        # If this was an open/load from file, the caller of this 
        # function should themselves call the function to set the flag to
        # be not dirty.
        self.setDirtyFlag(True)

        self.log.\
            debug("Exiting setPriceChartDocumentData()")
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the given PriceBarChartSettings to the underlying
        PriceBarChart.  
        
        The caller is responsible for setting the dirty
        flag if this priceBarChartSettings is different from the 
        currently used internal priceBarChartSettings.
        If it is expected to be the same, then the parent will need to
        explicitly set the dirty flag to False because a redraw of the
        internal widgets will cause signals to be emitted to notify
        higher-up qobjects that there are outstanding changes.
        """

        self.priceChartDocumentData.priceBarChartSettings = \
            priceBarChartSettings

        self.widgets.applyPriceBarChartSettings\
                (self.priceChartDocumentData.priceBarChartSettings)

    def applyPriceBarSpreadsheetSettings(self, priceBarSpreadsheetSettings):
        """Applies the given PriceBarSpreadsheetSettings to the underlying
        PriceBarSpreadsheet.  The caller is responsible for setting the dirty
        flag if this priceBarSpreadsheetSettings is different from the 
        currently used internal priceBarSpreadsheetSettings 
        (which most likely it is).
        """

        self.priceChartDocumentData.priceBarSpreadsheetSettings = \
            priceBarSpreadsheetSettings

        self.widgets.applyPriceBarSpreadsheetSettings\
                (self.priceChartDocumentData.priceBarSpreadsheetSettings)

    def getBirthInfo(self):
        """Returns the internal BirthInfo object from the internal
        PriceChartDocumentData object.
        """

        self.log.debug("Entered getBirthInfo()")
        self.log.debug("Exiting getBirthInfo()")
        return self.priceChartDocumentData.getBirthInfo()

    def setBirthInfo(self, birthInfo):
        """Sets the the internal BirthInfo in the internal
        PriceChartDocumentData object.  This also causes the dirty flag to
        be set on the document.
        """

        self.log.debug("Entered setBirthInfo()")

        self.priceChartDocumentData.setBirthInfo(birthInfo)

        self.widgets.setBirthInfo(birthInfo)

        self.setDirtyFlag(True)

        self.log.debug("Exiting setBirthInfo()")

    def getDirtyFlag(self):
        """Returns the dirty flag value."""

        return self.dirtyFlag

    def setDirtyFlag(self, dirtyFlag):
        """Sets the flag that says that the PriceChartDocument is dirty.
        The document being dirty means that the document has modifications
        that have not been saved to file (or other persistent backend).

        Parameters:
        dirtyFlag - bool value for what the dirty flag is.  True means
        there are modifications not saved yet.
        """

        self.log.debug("Entered setDirtyFlag({})".format(dirtyFlag))

        # Set the flag first.
        self.dirtyFlag = dirtyFlag

        modFileStr = PriceChartDocument.modifiedFileStr
        modFileStrLen = len(PriceChartDocument.modifiedFileStr)

        if self.dirtyFlag == True:
            # Modify the title, but only if it isn't already there.
            if self.title[(-1 * modFileStrLen):] != modFileStr:
                self.title += modFileStr
        else:
            # Remove the modified-file string from the title if it is
            # already there.
            if (len(self.title) >= modFileStrLen and \
                self.title[(-1 * modFileStrLen):] == modFileStr):

                # Chop off the string.
                self.title = self.title[:(-1 * modFileStrLen)]

        # Actually update the window title if it is now different.
        if self.title != str(self.windowTitle()):
            self.setWindowTitle(self.title)

        self.log.debug("Exiting setDirtyFlag({})".format(dirtyFlag))

    def closeEvent(self, closeEvent):
        """Closes this QMdiSubWindow.
        If there are unsaved modifications, then the user will be prompted
        for saving.
        """
        
        self.log.debug("Entered closeEvent()")

        priceChartDocument = self

        # Prompt for saving if there are unsaved modifications.
        if priceChartDocument.getDirtyFlag() == True:
            title = "Save before closing?"
            text = "This PriceChartDocument has not been saved yet." + \
                   os.linesep + os.linesep + \
                   "Save before closing?"
            buttons = (QMessageBox.Save | 
                       QMessageBox.Discard | 
                       QMessageBox.Cancel)

            defaultButton = QMessageBox.Save 

            buttonClicked = \
                QMessageBox.question(self, title, text, 
                                     buttons, defaultButton)

            # Check what button was clicked in the prompt.
            if buttonClicked == QMessageBox.Save:
                # Save the document before closing.
                debugMsg = "closeEvent(): " + \
                    "User chose to save mods to PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                # Only close if the save action succeeded.
                # We can always prompt again and they can click discard if
                # they really don't want to save.
                if self.saveChart() == True:
                    self.log.debug("Save was successful.  " + \
                                   "Now closing PriceChartDocument.")
                    closeEvent.accept()
                else:
                    self.log.debug("Save was not successful.  " + \
                                   "Ignoring close event.")
                    closeEvent.ignore()

            elif buttonClicked == QMessageBox.Discard:
                # Discard modifications.  Here we just send a close event.
                debugMsg = "closeEvent(): " + \
                    "Discarding modifications to PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                closeEvent.accept()

            elif buttonClicked == QMessageBox.Cancel:
                # Use clicked cancel, meaning he doesn't want to close the
                # chart after all.
                debugMsg = "closeEvent(): " + \
                    "Canceled closeChart for PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                closeEvent.ignore()
        else:
            # Document is not dirty (it has been saved).  Just close.
            self.log.debug("Document has no unsaved mods.  " + \
                           "Just closing the PriceChartDocument: " + \
                           priceChartDocument.toString())

            closeEvent.accept()

        self.log.debug("Exiting closeEvent()")

    def saveChart(self):
        """Saves this PriceChartDocument.
        If the document has not been saved before, then a prompt 
        will be brought up for the user to specify a filename 
        to save as.

        Returns: True if the save action succeeded.
        """

        self.log.debug("Entered saveChart()")

        # Return value.
        rv = True

        priceChartDocument = self

        # See if it has been saved before and has a filename,
        # of it is untitled and never been saved before.
        filename = priceChartDocument.getFilename()

        if filename == "":
            # The document has never been saved before.
            # Bring up the Save As prompt for file.
            rv = self.saveAsChart()
        else:
            # The document has been saved before and has a filename
            # associated with it.
            self.log.debug("saveChart(): " + 
                           "Filename associated with " +
                           "the PriceChartDocument is: " + filename)

            if os.path.exists(filename):
                self.log.debug("saveChart(): " + 
                               "Updating existing file: " + 
                               filename)
            else:
                self.log.warn("saveChart(): " +
                              "Filename was non-empty " +
                              "and set to a file that does not exist!  " +
                              "This is an invalid state.  Filenames " + 
                              "should only be set if it was previously " +
                              "saved to the given filename.")

            # Pickle to file.
            rv = priceChartDocument.\
                    picklePriceChartDocumentDataToFile(filename)

            # Clear the dirty flag if the operation was successful.
            if rv == True:
                self.log.info("PriceChartDocumentData saved to file: " + 
                              filename)

                if self.log.isEnabledFor(logging.DEBUG):
                    # Get the data object for debugging messages.
                    priceChartDocumentData = \
                        priceChartDocument.getPriceChartDocumentData()

                    debugMsg = \
                        "File '{}' ".format(filename) + \
                        "now holds the following " + \
                        "PriceChartDocumentData: " + \
                        priceChartDocumentData.toString()

                    self.log.debug(debugMsg)

                # Filename shouldn't have changed, so there's no need to
                # set it again.
                priceChartDocument.setDirtyFlag(False)

                self.statusMessageUpdate.emit("PriceChartDocument saved.")
            else:
                # Save failure.
                self.statusMessageUpdate.emit("Save failed.  " + 
                                "Please check the log file for why.")

        self.log.debug("Exiting saveChart().  Returning {}".format(rv))
        return rv


    def saveAsChart(self):
        """Brings up a prompt for the user to save this 
        PriceChartDocument to a new file.  After the 
        user selects the file, it will be saved
        to that file.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).

        Returns: True if the saveAs action succeeded.
        """

        self.log.debug("Entered saveAsChart()")

        # Return value.
        rv = True

        priceChartDocument = self

        # Set filters for what files are displayed.
        filters = \
            PriceChartDocument.fileFilter + ";;" + \
            MainWindow.allFilesFileFilter

        # Directory location default for the file save dialogs for
        # PriceChartDocument.
        settings = QSettings()
        defaultPriceChartDocumentSaveDirectory = \
            settings.value("ui/defaultPriceChartDocumentSaveDirectory", "")

        # Prompt for what filename to save the data to.
        filename = QFileDialog.\
            getSaveFileName(self, 
                            "Save As", 
                            defaultPriceChartDocumentSaveDirectory, 
                            filters)

        # Convert filename from QString to str.
        filename = str(filename)

        self.log.debug("saveAsChart(): The user selected filename: " +
                       filename + " as what they wanted to save to.")

        # Verify input.
        if filename == "":
            # The user must of clicked cancel at the file dialog prompt.
            rv = False
        else:
            # Pickle to file.
            rv = priceChartDocument.\
                    picklePriceChartDocumentDataToFile(filename)

            # If the save operation was successful, then update the
            # filename and clear the dirty flag.
            if rv == True:
                self.log.info("PriceChartDocumentData saved to " + 
                              "new file: " + filename)

                if self.log.isEnabledFor(logging.DEBUG):
                    # Get the data object for debugging messages.
                    priceChartDocumentData = \
                        priceChartDocument.getPriceChartDocumentData()

                    debugMsg = \
                        "File '{}' ".format(filename) + \
                        "now holds the following " + \
                        "PriceChartDocumentData: " + \
                        priceChartDocumentData.toString()

                    self.log.debug(debugMsg)

                priceChartDocument.setFilename(filename)
                priceChartDocument.setDirtyFlag(False)
 
                statusBarMessage = \
                    "PriceChartDocument saved to file {}.".format(filename)

                self.statusMessageUpdate.emit(statusBarMessage)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # Update the self.defaultPriceChartDocumentSaveDirectory
                # with the directory where filename is, if the directory
                # is different.
                if directory != defaultPriceChartDocumentSaveDirectory:
                    settings.\
                        setValue("ui/defaultPriceChartDocumentSaveDirectory",
                                 directory)
            else:
                # Save failure.
                self.statusMessageUpdate.emit("Save failed.  " + 
                                "Please check the log file for why.")

        self.log.debug("Exiting saveAsChart().  Returning {}".format(rv))
        return rv

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.widgets.toReadOnlyPointerToolMode()

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.widgets.toPointerToolMode()

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.widgets.toHandToolMode()

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.widgets.toZoomInToolMode()

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.widgets.toZoomOutToolMode()

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.widgets.toBarCountToolMode()

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.widgets.toTimeMeasurementToolMode()

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.widgets.toTimeModalScaleToolMode()

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.widgets.toPriceModalScaleToolMode()

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.widgets.toTextToolMode()

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.widgets.toPriceTimeInfoToolMode()

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.widgets.toPriceMeasurementToolMode()

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.widgets.toTimeRetracementToolMode()

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.widgets.toPriceRetracementToolMode()

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.widgets.toPriceTimeVectorToolMode()

    def toLineSegmentToolMode(self):
        """Changes the tool mode to be the LineSegmentTool."""

        self.widgets.toLineSegmentToolMode()

    def _handlePriceChartDocumentWidgetChanged(self):
        """Slot for when the PriceBarDocumentWidget emits a signal to say
        that the widget(s) changed.  This means the document should be
        marked as dirty.
        """
        
        if self.getDirtyFlag() != True:
            self.setDirtyFlag(True)

    def toString(self):
        """Returns the str representation of this class object.
        """

        # Return value.
        rv = \
            "[title={}, ".format(self.title) + \
            "filename={}, ".format(self.filename) + \
            "isUntitled={}, ".format(self.isUntitled) + \
            "dirtyFlag={}, ".format(self.dirtyFlag) + \
            "priceChartDocumentData={}]".\
                format(self.priceChartDocumentData.toString())

        return rv

    def __str__(self):
        """Returns the str representation of this class object.
        """

        return self.toString() 

class PriceChartDocumentWidget(QWidget):
    """Internal widget within a PriceChartDocument (QMdiSubWindow) that
    holds all the other widgets.  This basically serves as a QLayout
    for the PriceChartDocument.
    """

    # Signal emitted when the widgets in the PriceChartDocument changes.
    # This is caused by a meaningful change to either the contents, or the
    # settings object for that widget.
    priceChartDocumentWidgetChanged = QtCore.pyqtSignal()

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger("ui.PriceChartDocumentWidget")

        self.birthInfo = BirthInfo()

        # Create the internal widgets displayed.
        self.priceBarChartWidget = PriceBarChartWidget()
        self.priceBarSpreadsheetWidget = PriceBarSpreadsheetWidget()
        # TODO:  uncomment to at the table planetary info table widget.
        #self.planetaryInfoTableWidget = PlanetaryInfoTableWidget()

        # TODO:  Add QSplitters to divide the above internal widgets.

        self.setBirthInfo(self.birthInfo)

        # Setup the layout.
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.priceBarChartWidget)
        vlayout.addWidget(self.priceBarSpreadsheetWidget)

        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout)
        # TODO:  Uncomment to re-add the PlanetaryInfoTableWidget.
        #hlayout.addWidget(self.planetaryInfoTableWidget)

        self.setLayout(hlayout)

        # Connect signals and slots.
        self.priceBarChartWidget.priceBarChartChanged.\
            connect(self._handleWidgetChanged)
        self.priceBarChartWidget.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
                                   
        # TODO:  Uncomment to re-add the PlanetaryInfoTableWidget.
        #self.priceBarChartWidget.currentTimestampChanged.\
        #    connect(self._handleCurrentTimestampChanged)
        
        # TODO:  Add methods to handle for the following astro signals:
        # TODO:  Make sure to handle the timezone stuff (and test thoroughly).
        # self.priceBarChartWidget.astroChart1Update
        # self.priceBarChartWidget.astroChart2Update
        # self.priceBarChartWidget.astroChart3Update
        # self.priceBarChartWidget.jhoraLaunch
        
    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        self.birthInfo = birthInfo

        # Give the self.priceBarChartWidget the birth time as well.
        self.priceBarChartWidget.setBirthInfo(self.birthInfo)

    def setDescriptionText(self, text):
        """Sets the description text of this PriceChartDocument.
        
        Arguments:
            
        text - str variable holding the new text to set the description
               with.
        """

        self.priceBarChartWidget.setDescriptionText(text)
        
    def setTimezone(self, timezone):
        """Sets the timezone of this PriceChartDocument.
        
        Arguments:

        timezone - datetime.tzinfo object to set for the location of this
                   exchange/market.
        """

        self.priceBarChartWidget.setTimezone(timezone)

    def clearAllPriceBars(self):
        """Clears all PriceBars from all the internal widgets.
        This is called if a full reload is desired.
        After this call, one can then call loadPriceBars(priceBars) 
        with all the pricebars to be loaded.
        """

        self.log.debug("Entered clearAllPriceBars()")

        # PriceBars in the PriceBarChart.
        self.priceBarChartWidget.clearAllPriceBars()

        # PriceBars in the PriceBarSpreadsheet.
        self.priceBarSpreadsheetWidget.clearAllPriceBars()

        self.log.debug("Leaving clearAllPriceBars()")
        
    def clearAllPriceBarChartArtifacts(self):
        """Clears all the PriceBarChartArtifact objects from the 
        PriceBarChartWidget."""

        self.priceBarChartWidget.clearAllPriceBarChartArtifacts()


    def loadPriceBars(self, priceBars):
        """Loads the price bars into the widgets.
        
        Arguments:
            
        priceBars - list of PriceBar objects with the price data.
        """

        self.log.debug("Entered loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

        # Load PriceBars into the PriceBarChart.
        self.priceBarChartWidget.loadPriceBars(priceBars)

        # Load PriceBars into the PriceBarSpreadsheet.
        self.priceBarSpreadsheetWidget.loadPriceBars(priceBars)

        self.log.debug("Leaving loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

    def loadPriceBarChartArtifacts(self, priceBarChartArtifacts):
        """Loads the PriceBarChart artifacts.

        Arguments:

        priceBarChartArtifacts - list of PriceBarArtifact objects.
        """

        self.log.debug("Entered loadPriceBarChartArtifacts({} artifacts)".\
                       format(len(priceBarChartArtifacts)))

        self.priceBarChartWidget.\
            loadPriceBarChartArtifacts(priceBarChartArtifacts)

        self.log.debug("Leaving loadPriceBarChartArtifacts({} artifacts)".\
                       format(len(priceBarChartArtifacts)))

    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the given PriceBarChartSettings object to the
        internal PriceBarChartWidget.  
        
        Note:  This will most likely cause a redraw and thus signals will
        be emitted to say that the view has changed.
        """

        self.log.debug("Entered applyPriceBarChartSettings()")

        self.log.debug("Applying the following settings: {}".\
                       format(priceBarChartSettings.toString()))
        
        self.priceBarChartWidget.\
            applyPriceBarChartSettings(priceBarChartSettings)

        self.log.debug("Exiting applyPriceBarChartSettings()")
        
    def applyPriceBarSpreadsheetSettings(self, priceBarSpreadsheetSettings):
        """Applies the given PriceBarSpreadsheetSettings object to the
        internal PriceBarSpreadsheetWidget.
        """

        self.priceBarSpreadsheetWidget.\
            applyPriceBarSpreadsheetSettings(priceBarSpreadsheetSettings)

    def getPriceBarChartArtifacts(self):
        """Returns the list of PriceBarChartArtifacts that are used in the
        PriceBarChartWidget.
        """

        return self.priceBarChartWidget.getPriceBarChartArtifacts()

    def getPriceBarChartSettings(self):
        """Obtains the current PriceBarChartSettings object from the
        PriceBarChartWidget.
        """

        return self.priceBarChartWidget.getPriceBarChartSettings()

    def getPriceBarSpreadsheetSettings(self):
        """Obtains the current PriceBarSpreadsheetsettings object from the
        PriceBarSpreadsheetWidget.
        """

        return self.priceBarSpreadsheetWidget.\
                getPriceBarSpreadsheetSettings()

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.priceBarChartWidget.toReadOnlyPointerToolMode()

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.priceBarChartWidget.toPointerToolMode()

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.priceBarChartWidget.toHandToolMode()

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.priceBarChartWidget.toZoomInToolMode()

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.priceBarChartWidget.toZoomOutToolMode()

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.priceBarChartWidget.toBarCountToolMode()

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.priceBarChartWidget.toTimeMeasurementToolMode()

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.priceBarChartWidget.toTimeModalScaleToolMode()

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.priceBarChartWidget.toPriceModalScaleToolMode()

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.priceBarChartWidget.toTextToolMode()

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.priceBarChartWidget.toPriceTimeInfoToolMode()

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.priceBarChartWidget.toPriceMeasurementToolMode()

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.priceBarChartWidget.toTimeRetracementToolMode()

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.priceBarChartWidget.toPriceRetracementToolMode()

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.priceBarChartWidget.toPriceTimeVectorToolMode()

    def toLineSegmentToolMode(self):
        """Changes the tool mode to be the LineSegmentTool."""

        self.priceBarChartWidget.toLineSegmentToolMode()

    def _handleWidgetChanged(self):
        """Handles when the internal widget has some kind of change
        that would cause the document to be dirty.  This is either a
        change in the contents, or perhaps some change in the settings
        object.
        """

        self.priceChartDocumentWidgetChanged.emit()

    def jhoraLaunch(self, dt=None):
        """Opens JHora with the given datetime.datetime timestamp.
        Uses the currently set self.birthInfo object for timezone
        information.
        
        Arguments:
        
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in JHora.  If dt is None, then JHora is
             opened with the current time (the default behavior of JHora
             with no file argument).
        """

        # TODO:  write this function.
        
        # My thoughts: Should I just bubble this up again two more
        # times (via emitting signals) all the way up to MainWindow?
        # And then from here we will launch JHora.  Passing it up from
        # here we should include the relevant birthInfo/timezone.
        pass
        
    def _handleCurrentTimestampChanged(self, dt):
        """Handles when the current mouse cursor datetime changes.
        This just calls certain widgets to update their
        display of what the current time is.  For example,
        the PlanetaryInfoTableWidget would need to have it's info reloaded
        with the planetary locations for that timestamp.
        """

        # TODO:  this stuff probably will be deprecated as I handle this type of stuff in AstrologyChartWidget.  The below will need to change to call teh appropriate function of AstrologyChartWidget.
        
        
        # Set the location (required).
        Ephemeris.setGeographicPosition(self.birthInfo.longitudeDegrees,
                                        self.birthInfo.latitudeDegrees,
                                        self.birthInfo.elevation)

        # Get planetary info for all the planets.
        planets = []

        # TODO:  Add more 'planets' (planetary calculations) here as more
        # are available.
        
        p = Ephemeris.getSunPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMoonPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMercuryPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getVenusPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMarsPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getJupiterPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getSaturnPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getUranusPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getNeptunePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getPlutoPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMeanNorthNodePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getTrueNorthNodePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMeanLunarApogeePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getEarthPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getChironPlanetaryInfo(dt)
        planets.append(p)

        self.planetaryInfoTableWidget.load(planets)

