
# For directory and file access.
import os
import sys
import io

# For copy.deepcopy().
import copy

# For access to urllib errors.
import urllib.error

# For logging.
import logging
import logging.config

# For PyQt UI classes.
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For timezone lookup.
import datetime
import pytz

# Import image resources.
import resources

# For PriceBars
from data_objects import PriceBar
from data_objects import BirthInfo
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings

# For geocoding.
from geonames import GeoNames
from geonames import GeoInfo

# For various miscellaneous widgets.
from widgets import *

# For QSettings keys.
from settings import SettingsKeys

# For converting attributes of datetime.datetime objects to str.
from ephemeris import Ephemeris

class PriceChartDocumentWizard(QWizard):
    """QWizard for creating a new PriceChartDocument."""

    def __init__(self, parent=None):
        """Creates and sets up a QWizard for creating a new 
        PriceChartDocument."""

        super().__init__(parent)
        #super(PriceChartDocumentWizard, self).__init__(parent)

        # Logger object.
        self.log = logging.getLogger("dialogs.PriceChartDocumentWizard")
        self.log.debug("Creating PriceChartDocumentWizard ...")

        # Add QWizardPages.
        self.log.debug("Creating PriceChartDocumentIntroWizardPage ...")
        self.priceChartDocumentIntroWizardPage = \
            PriceChartDocumentIntroWizardPage()
        self.addPage(self.priceChartDocumentIntroWizardPage)

        self.log.debug("Creating " + \
                       "PriceChartDocumentLoadDataFileWizardPage ...")
        self.priceChartDocumentLoadDataFileWizardPage = \
            PriceChartDocumentLoadDataFileWizardPage()
        self.addPage(self.priceChartDocumentLoadDataFileWizardPage)

        self.log.debug("Creating " + \
                       "PriceChartDocumentLocationTimezoneWizardPage ...")
        self.priceChartDocumentLocationTimezoneWizardPage = \
            PriceChartDocumentLocationTimezoneWizardPage()
        self.addPage(self.priceChartDocumentLocationTimezoneWizardPage)

        self.log.debug("Creating " + \
                       "PriceChartDocumentDescriptionWizardPage ...")
        self.priceChartDocumentDescriptionWizardPage = \
            PriceChartDocumentDescriptionWizardPage()
        self.addPage(self.priceChartDocumentDescriptionWizardPage)

        self.log.debug("Creating " + \
                       "PriceChartDocumentConclusionWizardPage ...")
        self.priceChartDocumentConclusionWizardPage = \
            PriceChartDocumentConclusionWizardPage()
        self.addPage(self.priceChartDocumentConclusionWizardPage)

        self.log.debug("Setting up Pixmaps ...")

        # Set the pictures used in the QWizard.
        watermarkPic = \
            QPixmap(":/images/gann/HowToMakeProfitsInCommodities.png")
        backgroundPic = \
            QPixmap(":/images/gann/HowToMakeProfitsInCommodities.png")
        logoPic = QPixmap(":/images/rluu/logo_ryan_d1.png").scaled(64, 64)
        bannerPic = QPixmap(":/images/aaa-banners/grad23.gif").scaled(640, 72)

        self.setPixmap(QWizard.WatermarkPixmap, watermarkPic)
        self.setPixmap(QWizard.BackgroundPixmap, backgroundPic)
        self.setPixmap(QWizard.LogoPixmap, logoPic)
        self.setPixmap(QWizard.BannerPixmap, bannerPic)

        self.log.debug("Setting window title ...")

        # Set the title of the window.
        self.setWindowTitle("New Price Chart")


    def getPriceBars(self):
        """Obtains the list of PriceBars from a finished wizard setup.
        These PriceBars have their timestamps set with the timezone given
        in the timezone wizard.

        The PriceBars from a file must have been successfully 
        validated previously.
        """

        priceBars = \
            self.priceChartDocumentLoadDataFileWizardPage.\
                loadDataFileWidget.getPriceBars()

        # Here we need to change all the timestamps in each of the
        # PriceBar objects so that each timestamp has the timezone that
        # was set in the PriceChartDocumentLocationTimezoneWizardPage.

        # First get the timezone as a pytz.timezone object.
        timezoneStr = self.field("timezone")
        timezone = pytz.timezone(timezoneStr)

        # Go through each PriceBar and re-set the timezone.
        for i in range(len(priceBars)):
            # This is the timestamp of the PriceBar, but with the timezone
            # changed to None.
            timestamp = priceBars[i].timestamp.replace(tzinfo=None)

            # This is the timestamp with the timezone set.
            # The localize function will make sure that daylight savings
            # is applied if it needs to be applied for that date and time.
            localizedTimestamp = timezone.localize(timestamp)

            # Replace the old timestamp.
            priceBars[i].timestamp = localizedTimestamp

        return priceBars

class PriceChartDocumentIntroWizardPage(QWizardPage):
    """A QWizardPage that displays an introduction message to the QWizard."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("New Price Chart")
        self.setSubTitle(" ")

        # Create the contents.
        label = QLabel("This wizard will guide you through creating " + \
                       "a Price Chart document.")
        label.setWordWrap(True)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class PriceChartDocumentLoadDataFileWizardPage(QWizardPage):
    """A QWizardPage for loading price data from a file."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentLoadDataFileWizardPage")

        # Set the title strings.
        self.setTitle("Loading Price Data")
        self.setSubTitle(" ")

        # Internal edit widget.
        self.loadDataFileWidget = LoadDataFileWidget()
        self.loadDataFileWidget.setBottomButtonsVisible(False)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.loadDataFileWidget)
        self.setLayout(layout)

        # Register the fields.
        self.registerField("dataFilename*", 
                           self.loadDataFileWidget.filenameLineEdit)
        self.registerField("dataNumLinesToSkip*", 
                           self.loadDataFileWidget.skipLinesSpinBox)

        # Connect signals and slots.
        self.loadDataFileWidget.validationStateChanged.\
            connect(self.completeChanged)

    def isComplete(self):
        """Returns True if validation succeeded, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        return self.loadDataFileWidget.isValidated()


class PriceChartDocumentLocationTimezoneWizardPage(QWizardPage):
    """A QWizardPage for setting the location of the trading exchange
    and the timezone that the exchange is in.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentLocationTimezoneWizardPage")

        # Set the title strings.
        self.setTitle("Exchange Timezone")
        self.setSubTitle(" ")

        # Create the contents.
        self.locationTimezoneEditWidget = LocationTimezoneEditWidget()
        self.locationTimezoneEditWidget.setBottomButtonsVisible(False)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.locationTimezoneEditWidget)
        self.setLayout(layout)

        # Register the fields.
        self.registerField("timezone*", \
                           self.locationTimezoneEditWidget.timezoneComboBox,
                           "currentText")

    def isComplete(self):
        """Returns True if inputs are all entered, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        # Combo box always has something valid.
        return True

class PriceChartDocumentDescriptionWizardPage(QWizardPage):
    """A QWizardPage for setting the description of the data or chart that
    is being created.  This is any info that might be informative to tell
    about what is loaded.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentDescriptionWizardPage")

        # Set the title strings.
        self.setTitle("Description")
        self.setSubTitle(" ")

        # Create the contents.
        self.descriptionLabel= QLabel("&Description of the trading entity (optional):")
        self.descriptionLineEdit = QLineEdit()
        self.descriptionLabel.setBuddy(self.descriptionLineEdit)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.descriptionLabel)
        layout.addWidget(self.descriptionLineEdit)
        self.setLayout(layout)

        # Register the field(s).
        self.registerField("description", self.descriptionLineEdit, "text")

class PriceChartDocumentConclusionWizardPage(QWizardPage):
    """A QWizardPage for presenting the conclusion to the QWizard."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Conclusion")
        self.setSubTitle(" ")

        # Create the contents.
        label = QLabel("Setup is now complete.  " + \
                       "Please click the Finish button.")
        label.setWordWrap(True)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class LoadDataFileWidget(QWidget):
    """A widget for loading and verifying CSV text files containing 
    price data.  This uses QSettings and assumes that the calls to
    QCoreApplication.setOrganizationName(), and
    QCoreApplication.setApplicationName() have been called previously
    (so that the QSettings constructor can be called without 
    any parameters specified).
    """

    # Signal emitted when the data file to be loaded has been 
    # validated or becomes unvalidated.  
    # Emitting True means the data file was found to be valid.  
    # Emitting False means the data file was found to be not valid.
    validationStateChanged = QtCore.pyqtSignal(bool)

    # Signal emitted when the Load button is clicked.
    loadButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.LoadDataFileWidget")

        # Validated flag that indicates the file and number of 
        # lines skipped is valid.
        self.validatedFlag = False

        # Internally stored list of pricebars.
        self.priceBars = []

        # QSettings key for the defaultPriceBarDataOpenDirectory.
        self.defaultPriceBarDataOpenDirectorySettingsKey = \
            SettingsKeys.defaultPriceBarDataOpenDirectorySettingsKey 

        # Value for the defaultPriceBarDataOpenDirectory.  It is a setting
        # read in via readSettings().
        self.defaultPriceBarDataOpenDirectory = ""

        # Read in settings value for this widget.
        self.readSettings()

        # Create the contents.

        # Informational labels.
        descriptionLabel = \
            QLabel("Please select a file for loading price data." + \
                   os.linesep + os.linesep + \
                   "The selected file must be in CSV format with each " + \
                   "line of text having fields in the following order: " + \
                   os.linesep)
        descriptionLabel.setWordWrap(True)

        fileInfoDataDescStr = \
                      "<MM/DD/YYYY>," + \
                      "<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>," + \
                      "<Volume>,<OpenInterest>" + os.linesep
        fileInfoLabel = QLabel(fileInfoDataDescStr)
        font = fileInfoLabel.font()
        font.setPointSize(7)
        fileInfoLabel.setFont(font)
        
        # Frame as a separator.
        self.sep1 = QFrame()
        self.sep1.setFrameShape(QFrame.HLine)
        self.sep1.setFrameShadow(QFrame.Sunken)
        self.sep2 = QFrame()
        self.sep2.setFrameShape(QFrame.HLine)
        self.sep2.setFrameShadow(QFrame.Sunken)
        self.sep3 = QFrame()
        self.sep3.setFrameShape(QFrame.HLine)
        self.sep3.setFrameShadow(QFrame.Sunken)

        # Filename selection widgets.
        filenameLabel = QLabel("Filename:")
        self.filenameLineEdit = QLineEdit()
        self.filenameLineEdit.setReadOnly(True)
        self.browseButton = QPushButton(QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-open.png"), "Br&owse")

        fileBrowseLayout = QHBoxLayout()
        fileBrowseLayout.addWidget(self.filenameLineEdit)
        fileBrowseLayout.addWidget(self.browseButton)

        self.filePreviewLabel = QLabel("File Preview:")
        self.textViewer = QPlainTextEdit()
        self.textViewer.setReadOnly(True)
        self.textViewer.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Lines skipped selection widgets.
        self.skipLinesLabel = \
            QLabel("N&umber of lines to skip before reading data:")
        self.skipLinesSpinBox = QSpinBox()
        self.skipLinesSpinBox.setMinimum(0)
        self.skipLinesSpinBox.setValue(1)
        self.skipLinesLabel.setBuddy(self.skipLinesSpinBox)

        skipLinesLayout = QHBoxLayout()
        skipLinesLayout.addWidget(self.skipLinesLabel)
        skipLinesLayout.addWidget(self.skipLinesSpinBox)
        skipLinesLayout.addStretch()

        # Validation widgets.
        validateLabel = QLabel("Click to validate: " )
        self.validateButton = QPushButton("&Validate")
        validateLayout = QHBoxLayout()
        validateLayout.addWidget(validateLabel)
        validateLayout.addWidget(self.validateButton)

        self.validationStatusLabel = QLabel("")
        self.validationStatusLabel.setWordWrap(True)
        font = self.validationStatusLabel.font()
        font.setPointSize(8)
        self.validationStatusLabel.setFont(font)

        # Load / Cancel buttons.
        self.loadButton = QPushButton("&Load")
        self.cancelButton = QPushButton("&Cancel")
        bottomButtonsLayout = QHBoxLayout()
        bottomButtonsLayout.addStretch()
        bottomButtonsLayout.addWidget(self.loadButton)
        bottomButtonsLayout.addWidget(self.cancelButton)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        layout.addWidget(fileInfoLabel)
        layout.addWidget(self.sep1)
        layout.addWidget(filenameLabel)
        layout.addLayout(fileBrowseLayout)
        layout.addWidget(self.filePreviewLabel)
        layout.addWidget(self.textViewer)
        layout.addLayout(skipLinesLayout)
        layout.addWidget(self.sep2)
        layout.addLayout(validateLayout)
        layout.addWidget(self.validationStatusLabel)
        layout.addWidget(self.sep3)
        layout.addLayout(bottomButtonsLayout)

        self.setLayout(layout)

        # Connect signals and slots.
        self.filenameLineEdit.textChanged.\
            connect(self.handleFilenameLineEditChanged)

        self.skipLinesSpinBox.valueChanged.\
            connect(self.handleSkipLinesSpinBoxChanged)

        self.browseButton.clicked.\
            connect(self.handleBrowseButtonClicked)

        self.validateButton.clicked.\
            connect(self.handleValidateButtonClicked)

        self.validationStateChanged.\
            connect(self.setLoadButtonEnabled)

        self.loadButton.clicked.\
            connect(self.loadButtonClicked)

        self.cancelButton.clicked.\
            connect(self.cancelButtonClicked)

    def readSettings(self):
        """Reads settings from QSettings.  
        This function assumes that the calls to 
        QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        (so that the QSettings constructor can be called without 
        any parameters specified).
        """

        self.log.debug("Entered readSettings()")

        settings = QSettings()

        # Default directory to start the file open dialog.
        key = self.defaultPriceBarDataOpenDirectorySettingsKey
        self.defaultPriceBarDataOpenDirectory = settings.value(key, "")

        self.log.debug("Exiting readSettings()")

    def writeSettings(self):
        """Writes any changed settings to QSettings.
        This function assumes that the calls to 
        QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        (so that the QSettings constructor can be called without 
        any parameters specified).
        """

        self.log.debug("Entered writeSettings()")

        settings = QSettings()

        # Only set values if they have changed from what is in QSettings.

        # Default directory to start the file open dialog.
        key = self.defaultPriceBarDataOpenDirectorySettingsKey
        settingsValue = settings.value(key, "")

        if self.defaultPriceBarDataOpenDirectory != settingsValue:
            newValue = self.defaultPriceBarDataOpenDirectory
            settings.setValue(key, newValue)

        self.log.debug("Exiting writeSettings()")

    def setLoadButtonEnabled(self, flag):
        """Sets the 'Load' button to be enabled or disabled.
        Argument:
        flag - Boolean for whether or not the button should be enabled.
        """

        self.log.debug("setLoadButtonEnabled(flag={})".format(flag))

        if type(flag) == bool:
            self.loadButton.setEnabled(flag)


    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.sep3.setVisible(flag)
            self.loadButton.setVisible(flag)
            self.cancelButton.setVisible(flag)


    def handleFilenameLineEditChanged(self, filename):
        """Sets that the information entered has not been validated.
        """

        self.log.debug("handleFilenameLineEditChanged(filename={})".\
            format(filename))

        if (self.validatedFlag != False):
            self.validatedFlag = False
            self.validationStateChanged.emit(self.validatedFlag)

        # Convert to Python string type.
        filename = str(filename)

        # Clear any text in the file preview viewer.
        self.textViewer.setPlainText("")

        # Clear any text set in the validationStatusLabel.
        self.validationStatusLabel.setText("")


        if filename != "":
            with io.open(filename, "r") as file:
                try:
                    fileText = file.read()
                    self.textViewer.setPlainText(fileText)
                except UnicodeDecodeError as e:
                    errStr = "Error while trying to read file '" + \
                        str(filename) + "'.  Only text files are supported!"
                    self.log.error(errStr)
                    QMessageBox.warning(None,
                                        "Error reading file",
                                        errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")
                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    QMessageBox.warning(None,
                                        "Error reading file",
                                        errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")


    def handleSkipLinesSpinBoxChanged(self):
        """Sets that the information entered has not been validated.
        The validatedFlag is set to False if it is not already False.
        """

        self.log.debug("handleSkipLinesSpinBoxChanged()")

        if (self.validatedFlag != False):
            self.validatedFlag = False

            self.log.debug("Emitting validationStateChanged({})".\
                format(self.validatedFlag))

            self.validationStateChanged.emit(self.validatedFlag)

    def handleBrowseButtonClicked(self):
        """Opens a QFileDialog for selecting a file.  If a file is selected,
        self.filenameLineEdit will be populated with the selected filename.
        """

        self.log.debug("Entering handleBrowseButtonClicked()")

        # Create a file dialog.
        dialog = QFileDialog()

        # Setup file filters.
        csvTextFilesFilter = "CSV Text files (*.txt)"
        allFilesFilter = "All files (*)"
        filters = []
        filters.append(csvTextFilesFilter)
        filters.append(allFilesFilter)

        if self.defaultPriceBarDataOpenDirectory != "":
            dialog.setDirectory(self.defaultPriceBarDataOpenDirectory)

        # Apply settings to the dialog.
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(csvTextFilesFilter)

        # Run the dialog.
        if dialog.exec_() == QDialog.Accepted:
            # Get the selected files. Note PyQt 4.7.5 returns QStringList
            # as a Python list of str objects now.  This is different from
            # the PyQt 4.6.
            selectedFiles = dialog.selectedFiles()
            if len(selectedFiles) != 0:
                filename = str(selectedFiles[0])

                # Set the QLineEdit with the filename.
                self.filenameLineEdit.setText(filename)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # If the directory of the file chosen is different
                # from the directory of the file chosen last time, 
                # then update the defaultPriceBarDataOpenDirectory.
                if directory != self.defaultPriceBarDataOpenDirectory:
                    self.defaultPriceBarDataOpenDirectory = directory
                    self.writeSettings()

        self.log.debug("Leaving handleBrowseButtonClicked()")

    def handleValidateButtonClicked(self):
        """Opens the filename in self.filenameLineEdit and tries to validate
        that the file is a text file and has the expected fields.  
        It also populates the QPlainTextEdit with the data found in the file.

        This is also where the list of PriceBar objects are read and stored.
        """

        self.log.debug("handleValidateButtonClicked()")

        # Assume a valid file unless it's not.
        validFlag = True
        self.validationStatusLabel.setText("")

        # Create a new empty list for PriceBars.  
        # (We do this instead of emptying the list in case someone 
        # grabbed a copy of self.priceBars at some point earlier).
        # We will add to this list as we read valid lines in the file.
        self.priceBars = []

        # Get the fields from which we'll get info to read the file with.
        # Here casting to Python str type is required because 
        # QLineEdits return QString, not str.
        filename = str(self.filenameLineEdit.text())
        numLinesToSkip = self.skipLinesSpinBox.value()

        if filename == "":
            validFlag = False
            validationStr = "Validation failed because" + \
                " the filename cannot be empty."
            self.log.warn(validationStr)
            validationStr = self.toRedString(validationStr)
            self.validationStatusLabel.setText(validationStr)
        else:
            with io.open(filename, "r") as file:
                try:
                    # Go through each line of the file.
                    i = 0
                    for line in file:
                        i += 1

                        # Skip over empty lines and lines before 
                        # line number 'numLinesToSkip'.
                        if i > numLinesToSkip and line.strip() != "":
                            (lineValid, reason) = self.validateLine(line)
                            if lineValid == False:
                                # Invalid line in the file.
                                validFlag = False
                                validationStr = \
                                    "Validation failed on line " + \
                                    "{} because: {}".format(i, reason)
                                self.log.warn(validationStr)
                                validationStr = self.toRedString(validationStr)
                                self.validationStatusLabel.\
                                    setText(validationStr)
                                break
                            else:
                                # Valid line in the file.

                                # Create a PriceBar and append it to 
                                # the PriceBar list.
                                pb = self.convertLineToPriceBar(line)
                                self.priceBars.append(pb)

                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error reading file", errStr)
                    validationStr = \
                        "Validation failed due to a I/O error.  " + \
                        "Please try again later."
                    self.log.error(validationStr)
                    validationStr = self.toRedString(validationStr)
                    self.validationStatusLabel.setText(validationStr)

        # If the validFlag is still True, then allow the user to 
        # click the 'Next' button.
        if validFlag == True:
            infoStr = "Validated data file {}".format(filename)
            self.log.info(infoStr)
            validationStr = self.toGreenString("Validated")
            self.validationStatusLabel.setText(validationStr)
            if self.validatedFlag == False:
                self.validatedFlag = True
                self.validationStateChanged.emit(self.validatedFlag)

        self.log.debug("Leaving handleValidateButtonClicked()")

    def toRedString(self, string):
        """Wraps the input str with HTML tags to turn it red."""

        return "<font color=\"red\">" + string + "</font>"

    def toGreenString(self, string):
        """Wraps the input str with HTML tags to turn it green."""

        return "<font color=\"green\">" + string + "</font>"


    def validateLine(self, line):
        """Returns a tuple of (boolean, str) that represents if the line
        of text was parsed to be a valid CSV data line.

        If the line of text is valid, the boolean part of the tuple 
        returned is True and the string is returned is empty.

        If the line of text is found to be not valid, the tuple returns
        False and a string explaining why the validation failed.

        The expected format of 'line' is:
        <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
        """

        self.log.debug("validateLine(line='{}')".format(line))

        # Check the number of fields.
        fields = line.split(",")
        numFieldsExpected = 7
        if len(fields) != numFieldsExpected:
            return (False, "Line does not have {} data fields".\
                    format(numFieldsExpected))

        dateStr = fields[0] 
        openStr = fields[1]
        highStr = fields[2]
        lowStr = fields[3]
        closeStr = fields[4]
        volumeStr = fields[5]
        openIntStr = fields[6]

        dateStrSplit = dateStr.split("/")
        if len(dateStrSplit) != 3:
            return (False, "Format of the date was not MM/DD/YYYY")

        monthStr = dateStrSplit[0]
        dayStr = dateStrSplit[1]
        yearStr = dateStrSplit[2]

        if len(monthStr) != 2:
            return (False, "Month in the date is not two characters long")
        if len(dayStr) != 2:
            return (False, "Day in the date is not two characters long")
        if len(yearStr) != 4:
            return (False, "Year in the date is not four characters long")

        try:
            monthInt = int(monthStr)
            if monthInt < 1 or monthInt > 12:
                return (False, "Month in the date is not between 1 and 12")
        except ValueError as e:
            return (False, "Month in the date is not a number")

        try:
            dayInt = int(dayStr)
            if dayInt < 1 or dayInt > 31:
                return (False, "Day in the date is not between 1 and 31")
        except ValueError as e:
            return (False, "Day in the date is not a number")

        try:
            yearInt = int(yearStr)
        except ValueError as e:
            return (False, "Year in the date is not a number")
                
        try:
            openFloat = float(openStr)
        except ValueError as e:
            return (False, "OpenPrice is not a number")

        try:
            highFloat = float(highStr)
        except ValueError as e:
            return (False, "HighPrice is not a number")

        try:
            lowFloat = float(lowStr)
        except ValueError as e:
            return (False, "LowPrice is not a number")

        try:
            closeFloat = float(closeStr)
        except ValueError as e:
            return (False, "ClosePrice is not a number")

        try:
            volumeFloat = float(volumeStr)
        except ValueError as e:
            return (False, "Volume is not a number")

        try:
            openIntFloat = float(openIntStr)
        except ValueError as e:
            return (False, "OpenInterest is not a number")


        # If it got this far without returning, then everything 
        # checked out fine.
        return (True, "")


    def convertLineToPriceBar(self, line):
        """Convert a line of text from a CSV file to a PriceBar.

        The expected format of 'line' is:
        <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>

        Returns:
        PriceBar object from the line of text.  If the text was incorrectly
        formatted, then None is returned.  
        """

        self.log.debug("convertLineToPriceBar(line='{}')".format(line))

        # Return value.
        retVal = None

        # Do validation on the line first.
        (validFlag, reasonStr) = self.validateLine(line)

        if validFlag == False:
            self.log.debug("Line conversion failed because: {}" + reasonStr)
            retVal = None
        else:
            # Although we already validated the line, we wrap the parsing 
            # here in a try block just in case something unexpected 
            # was thrown at us.
            try:
                fields = line.split(",")

                dateStr = fields[0] 
                openPrice = float(fields[1])
                highPrice = float(fields[2])
                lowPrice = float(fields[3])
                closePrice = float(fields[4])
                volume = float(fields[5])
                openInt = float(fields[6])

                dateStrSplit = dateStr.split("/")
                month = int(dateStrSplit[0])
                day = int(dateStrSplit[1])
                year = int(dateStrSplit[2])

                # Datetime object is set to be in timezone UTC, and the
                # timestamp will have a time of 9:30am.
                #
                # It may not necessarily be true that the timezone is UTC,
                # but this widget does not know what else it should be.
                # The caller can always modify the timezone of this
                # timestamp at a later point in time.
                hour = 9
                minute = 30
                second = 0
                timestamp = \
                    datetime.datetime(year,
                                      month, 
                                      day, 
                                      hour, 
                                      minute, 
                                      second,
                                      tzinfo=pytz.utc)

                # Create the PriceBar with the parsed data.
                retVal = PriceBar(timestamp, 
                                  open=openPrice,
                                  high=highPrice,
                                  low=lowPrice,
                                  close=closePrice,
                                  oi=openInt,
                                  vol=volume)

            except IndexError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an IndexError: " + e)
            except UnicodeDecodeError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an UnicodeDecodeError: " + e)
            except ValueError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an ValueError: " + e)
            except TypeError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an TypeError: " + e)

        # Return the PriceBar created (or None if an error occurred).
        return retVal


    def isValidated(self):
        """Returns True if validation succeeded, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        return self.validatedFlag

    def getPriceBars(self):
        """Returns a list of PriceBars if the opened file has been validated
        successfully (i.e., isValidated() returns True).  If the opened file
        failed validation, this function will return an empty list.
        """
        
        if self.isValidated():
            self.log.debug("getPriceBars(): returning list of PriceBars " + \
                           "with length {}".format(len(self.priceBars)))
            return self.priceBars
        else:
            self.log.debug("getPriceBars(): File was not validated. " + \
                           "Returning an empty list.")
            return []

class LocationTimezoneEditWidget(QWidget):
    """QWidget for searching for a location and timezone."""

    # Signal emitted when the Okay button is clicked.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.LocationTimezoneEditWidget")

        self.log.debug("Checking for internet connection to web service.")

        # Flag to determine if we have an internet connection and can reach
        # GeoNames web service.

        # TODO: Uncomment the line below after testing of the app is done.
        # I have it commented because I don't want to spam their
        # server while testing my own app.  Also, remove the line below
        # that one that sets the flag to True.
        #self.geoNamesEnabled = GeoNames.canConnectToWebService()
        self.geoNamesEnabled = True

        if self.geoNamesEnabled:
            self.log.debug("Internet connection to the web service is " + \
                           "available.")
        else:
            self.log.info("Internet connection to the web service is " + \
                          "not available.")

        # Create the contents.

        # Informational labels.
        descriptionLabel = \
            QLabel("Enter a search phrase for the location." + \
                   os.linesep + os.linesep + \
                   "Timezone information will be " + \
                   "determined from the selected search result." + \
                   os.linesep)
        descriptionLabel.setWordWrap(True)

        # Label that is displayed if we can't get to GeoNames.
        geoNamesStatus = \
            "<font color=\"red\">" + \
            "Search functionality is disabled due to failed " + \
            "network connection to GeoNames web service." + \
            "</font>"
        geoNamesStatusLabel = QLabel(geoNamesStatus)
        geoNamesStatusLabel.setWordWrap(True)

        # Frame as a separator.
        self.sep1 = QFrame()
        self.sep1.setFrameShape(QFrame.HLine)
        self.sep1.setFrameShadow(QFrame.Sunken)
        self.sep2 = QFrame()
        self.sep2.setFrameShape(QFrame.HLine)
        self.sep2.setFrameShadow(QFrame.Sunken)
        self.sep3 = QFrame()
        self.sep3.setFrameShape(QFrame.HLine)
        self.sep3.setFrameShadow(QFrame.Sunken)

        # Location search widgets.
        searchLocationLabel = QLabel("Search for &location:")
        self.searchLocationLineEdit = QLineEdit()
        searchLocationLabel.setBuddy(self.searchLocationLineEdit)
        self.searchButton = QPushButton("&Search")
        self.searchLocationLineEdit.returnPressed.\
            connect(self.searchButton.click)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLocationLineEdit)
        searchLayout.addWidget(self.searchButton)

        # Results selection widgets.
        resultsLabel = QLabel("Search &results:")
        self.resultsComboBox = QComboBox()
        self.resultsComboBox.setDuplicatesEnabled(True)
        resultsLabel.setBuddy(self.resultsComboBox)
        # Disable the QComboBox until the results come in.
        self.resultsComboBox.setEnabled(False)

        # Timezone widgets.
        timezoneLabel = QLabel("Timezone name:")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)

        # If GeoNames is not enabled, then disable some widgets.
        if self.geoNamesEnabled == False:
            self.searchLocationLineEdit.setEnabled(False)
            self.searchButton.setEnabled(False)
            self.resultsComboBox.setEnabled(False)

        # Okay / Cancel buttons.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        bottomButtonsLayout = QHBoxLayout()
        bottomButtonsLayout.addStretch()
        bottomButtonsLayout.addWidget(self.okayButton)
        bottomButtonsLayout.addWidget(self.cancelButton)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        if self.geoNamesEnabled == False:
            layout.addWidget(geoNamesStatusLabel)
        layout.addWidget(self.sep1)
        layout.addWidget(searchLocationLabel)
        layout.addLayout(searchLayout)
        layout.addWidget(resultsLabel)
        layout.addWidget(self.resultsComboBox)
        layout.addWidget(self.sep2)
        layout.addWidget(timezoneLabel)
        layout.addWidget(self.timezoneComboBox)
        layout.addWidget(self.sep3)
        layout.addLayout(bottomButtonsLayout)
        self.setLayout(layout)

        # Connect signals and slots.
        self.searchButton.clicked.connect(self.doLocationSearch)
        self.resultsComboBox.currentIndexChanged[int].\
            connect(self.handleSearchResultSelected)
        self.okayButton.clicked.connect(self.okayButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.sep3.setVisible(flag)
            self.okayButton.setVisible(flag)
            self.cancelButton.setVisible(flag)

    def doLocationSearch(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.searchLocationLineEdit.  Results that are returned are
        populated in the self.resultsComboBox.  If there is any error in doing
        the search, a pop-up dialog is displayed with the error description, 
        and the error is logged.
        """

        self.log.debug("Entered doLocationSearch()")

        searchString = str(self.searchLocationLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = GeoNames.search(searchStr=searchString, 
                                   countryBias="")

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))


        # Prepare the self.resultsComboBox if there are new results to 
        # populate it with.
        if len(geoInfos) > 0:
            self.log.debug("Clearing resultsComboBox...")
            # Clear the QComboBox of search results.
            self.resultsComboBox.clear()

            self.log.debug("Enabling resultsComboBox...")
            # If the self.resultsComboBox is disabled, then enable it.
            if self.resultsComboBox.isEnabled() == False:
                self.resultsComboBox.setEnabled(True)

        # Populate the self.resultsComboBox.
        for i in range(len(geoInfos)):
            geoInfo = geoInfos[i]

            displayStr = geoInfo.name
            if geoInfo.adminName1 != None and geoInfo.adminName1 != "":
                displayStr += ", " + geoInfo.adminName1
            if geoInfo.countryName != None and geoInfo.countryName != "":
                displayStr += ", " + geoInfo.countryName
            displayStr += " ({}, {})".format(geoInfo.latitudeStr(), 
                                             geoInfo.longitudeStr()) 
            if geoInfo.population != None and geoInfo.population != 0:
                displayStr += " (pop. {})".format(geoInfo.population)

            self.log.debug("Display name is: {}".format(displayStr))
            self.resultsComboBox.addItem(displayStr, geoInfo)

        self.log.debug("Leaving doLocationSearch()")


    def handleSearchResultSelected(self, index):
        """Determines which search result was selected, and populates
        the timezone QComboBox for that location.
        """

        self.log.debug("Entered handleSearchResultSelected(index={})".\
                       format(index))

        # Only makes sense if the index selected is valid.  
        # Theoretically index should only be -1 on the very first load.
        if index == -1:
            return

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        maybeQVariant = self.resultsComboBox.itemData(index)
        geoInfo = GeoInfo()
        if isinstance(maybeQVariant, QVariant):
            # This is really a QVariant, so use toPyObject().
            geoInfo = maybeQVariant.toPyObject()
        else:
            # PyQt converted it already for us.
            geoInfo = maybeQVariant

        # Make sure geoInfo is not None.  We need it in order to get the
        # timezone information.  It should never be None.
        if geoInfo == None:
            self.log.error("GeoInfo is None, when it should have " + \
                           "been an actual object!")
            return

        # Try to use the timezone in geoInfo first.  If that doesn't 
        # work, then the do a query for the timezone using the latitude and
        # longitude.
        if geoInfo.timezone != None and geoInfo.timezone != "":
            index = self.timezoneComboBox.findText(geoInfo.timezone)
            if index != -1:
                self.timezoneComboBox.setCurrentIndex(index)
            else:
                errStr = "Couldn't find timezone '" + geoInfo.timezone + \
                     "' returned by GeoNames in the pytz " + \
                     "list of timezones."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
        else:
            # Try to do the query ourselves from GeoNames.getTimezone().
            timezone = None
            try:
                timezone = GeoNames.getTimezone(geoInfo.latitude,
                                                geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't perform the search because " + \
                         "of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
                return

            if timezone != None and timezone != "":
                index = self.timezoneComboBox.findText(geoInfo.timezone)
                if index != -1:
                    self.timezoneComboBox.setCurrentIndex(index)
                else:
                    errStr = "Couldn't find timezone '" + timezone + \
                         "' returned by GeoNames in the pytz " + \
                         "list of timezones."
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error", errStr)
            else:
                errStr = "GeoNames returned a null or empty timezone."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        self.log.debug("Leaving handleSearchResultSelected()")


    def getTimezoneStr(self):
        """Returns the timezone selected in the QComboBox."""

        return str(self.timezoneComboBox.currentText())

class AppPreferencesEditWidget(QWidget):
    """QWidget for editing some of the app-wide preferences.
    These values are retrieved and stored from the QSettings.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Sets the internal widgets and loads the widgets with values
        from QSettings.  This uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        (so that the QSettings constructor can be called without 
        any parameters specified)
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.AppPreferencesEditWidget")


        # Build QWidgets that go into the QTabWidget.
        self.priceBarChartSettingsGroupBox =  \
            self._buildPriceBarChartSettingsWidget()
        self.planetSymbolSettingsGroupBox = \
            self._buildPlanetSymbolSettingsWidget()
        self.nonPlanetSymbolSettingsGroupBox = \
            self._buildNonPlanetSymbolSettingsWidget()
        self.signSymbolSettingsGroupBox = \
            self._buildSignSymbolSettingsWidget()


        # Create a QTabWidget to stack all the settings editing widgets.
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.priceBarChartSettingsGroupBox,
                              "PriceBarChart")
        self.tabWidget.addTab(self.planetSymbolSettingsGroupBox,
                              "Planet Symbols")
        self.tabWidget.addTab(self.nonPlanetSymbolSettingsGroupBox,
                              "Non-Planet Symbols")
        self.tabWidget.addTab(self.signSymbolSettingsGroupBox,
                              "Zodiac Symbols")

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.

        # Connect reset buttons.
        self.zoomScaleFactorResetButton.clicked.\
            connect(self._handleZoomScaleFactorResetButtonClicked)
        self.higherPriceBarColorResetButton.clicked.\
            connect(self._handleHigherPriceBarColorResetButtonClicked)
        self.lowerPriceBarColorResetButton.clicked.\
            connect(self._handleLowerPriceBarColorResetButtonClicked)
        self.barCountGraphicsItemColorResetButton.clicked.\
            connect(self._handleBarCountGraphicsItemColorResetButtonClicked)
        self.barCountGraphicsItemTextColorResetButton.clicked.\
            connect(self._handleBarCountGraphicsItemTextColorResetButtonClicked)

        # Button at bottom to reset to defaults.
        self.priceBarResetAllToDefaultButton.clicked.\
            connect(self._handlePriceBarResetAllToDefaultButtonClicked)
        self.planetSymbolResetAllToDefaultButton.clicked.\
            connect(self._handlePlanetSymbolResetAllToDefaultButtonClicked)
        self.nonPlanetSymbolResetAllToDefaultButton.clicked.\
            connect(self._handleNonPlanetSymbolResetAllToDefaultButtonClicked)
        self.signSymbolResetAllToDefaultButton.clicked.\
            connect(self._handleSignSymbolResetAllToDefaultButtonClicked)

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        # Load the widgets with values from QSettings.
        self.loadValuesFromSettings()

    def _buildPriceBarChartSettingsWidget(self):
        """Builds a QWidget for editing the settings in PriceBarChart.

        Returned widget is self.priceBarChartSettingsGroupBox.
        """

        self.priceBarChartSettingsGroupBox = \
            QGroupBox("PriceBarChart settings:")

        # PriceBarChart zoom-in/out scale factor (float).
        self.zoomScaleFactorLabel = QLabel("Zoom scale factor:")
        self.zoomScaleFactorSpinBox = QDoubleSpinBox()
        self.zoomScaleFactorSpinBox.setMinimum(1.0)
        self.zoomScaleFactorSpinBox.setMaximum(100.0)
        self.zoomScaleFactorResetButton = QPushButton("Reset to default")

        # PriceBarChart higherPriceBarColor (QColor).
        self.higherPriceBarColorLabel = QLabel("Higher PriceBar color:")
        self.higherPriceBarColorEditButton = ColorEditPushButton()
        self.higherPriceBarColorResetButton = QPushButton("Reset to default")

        # PriceBarChart lowerPriceBarColor (QColor).
        self.lowerPriceBarColorLabel = QLabel("Lower PriceBar color:")
        self.lowerPriceBarColorEditButton = ColorEditPushButton()
        self.lowerPriceBarColorResetButton = QPushButton("Reset to default")

        # PriceBarChart barCountGraphicsItemColor (QColor).
        self.barCountGraphicsItemColorLabel = \
            QLabel("BarCountGraphicsItem color: ")
        self.barCountGraphicsItemColorEditButton = ColorEditPushButton()
        self.barCountGraphicsItemColorResetButton = \
            QPushButton("Reset to default")
        
        # PriceBarChart barCountGraphicsItemTextColor (QColor).
        self.barCountGraphicsItemTextColorLabel = \
            QLabel("BarCountGraphicsItem text color: ")
        self.barCountGraphicsItemTextColorEditButton = ColorEditPushButton()
        self.barCountGraphicsItemTextColorResetButton = \
            QPushButton("Reset to default")
        
        # Button for resetting all the above edit widgets.
        self.priceBarResetAllToDefaultButton = \
            QPushButton("Reset all the above to original default values")

        # Grid layout.  We don't use QFormLayout because we need the 3rd
        # field area for a reset button.
        gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.zoomScaleFactorLabel, r, 0, al)
        gridLayout.\
            addWidget(self.zoomScaleFactorSpinBox, r, 1, ar)
        gridLayout.\
            addWidget(self.zoomScaleFactorResetButton, r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.higherPriceBarColorLabel, r, 0, al)
        gridLayout.\
            addWidget(self.higherPriceBarColorEditButton, r, 1, ar)
        gridLayout.\
            addWidget(self.higherPriceBarColorResetButton, r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.lowerPriceBarColorLabel, r, 0, al)
        gridLayout.\
            addWidget(self.lowerPriceBarColorEditButton, r, 1, ar)
        gridLayout.\
            addWidget(self.lowerPriceBarColorResetButton, r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.barCountGraphicsItemColorLabel, r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemColorEditButton, r, 1, ar)
        gridLayout.\
            addWidget(self.barCountGraphicsItemColorResetButton, r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextColorLabel, r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextColorEditButton, r, 1, ar)
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextColorResetButton, r, 2, ar)
        r += 1

        # Label to tell the user that not all settings will be applied
        # on existing windows when the 'Okay' button is pressed.
        endl = os.linesep
        noteLabel = \
            QLabel("Note: Upon clicking the 'Okay' button, the new " + \
                   "settings may not be immediately applied" + \
                   endl + \
                   "to the open PriceChartDocuments.  " + \
                   "You may need to close and re-open the " + \
                   endl + \
                   "PriceChartDocuments to get the changes.")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.priceBarResetAllToDefaultButton)
        hlayout.addStretch()

        vlayout = QVBoxLayout()
        vlayout.addLayout(gridLayout)
        vlayout.addStretch()
        vlayout.addWidget(noteLabel)
        vlayout.addSpacing(10)
        vlayout.addLayout(hlayout)

        self.priceBarChartSettingsGroupBox.setLayout(vlayout)

        return self.priceBarChartSettingsGroupBox


    def _buildPlanetSymbolSettingsWidget(self):
        """Builds a QWidget for editing the settings of Planets as
        displayed in the UI.

        Returned widget is self.planetSymbolSettingsGroupBox.
        """

        self.planetSymbolSettingsGroupBox = QGroupBox("Planet settings:")

        formLayout = QFormLayout()
        formLayout.setLabelAlignment(Qt.AlignLeft)

        # Sun
        self.planetSunGlyphUnicodeLabel = \
            QLabel("Sun unicode glyph:")
        self.planetSunGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSunGlyphUnicodeLabel,
                   self.planetSunGlyphUnicodeLineEdit)
        self.planetSunGlyphFontSizeLabel = \
            QLabel("Sun glyph font size:")
        self.planetSunGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetSunGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetSunGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetSunGlyphFontSizeLabel,
                   self.planetSunGlyphFontSizeSpinBox)
        self.planetSunAbbreviationLabel = \
            QLabel("Sun abbreviation:")
        self.planetSunAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSunAbbreviationLabel,
                   self.planetSunAbbreviationLineEdit)
        self.planetSunForegroundColorLabel = \
            QLabel("Sun foreground color:")
        self.planetSunForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSunForegroundColorLabel,
                   self.planetSunForegroundColorEditButton)
        self.planetSunBackgroundColorLabel = \
            QLabel("Sun background color:")
        self.planetSunBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSunBackgroundColorLabel,
                   self.planetSunBackgroundColorEditButton)

        # Moon
        self.planetMoonGlyphUnicodeLabel = \
            QLabel("Moon unicode glyph:")
        self.planetMoonGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMoonGlyphUnicodeLabel,
                   self.planetMoonGlyphUnicodeLineEdit)
        self.planetMoonGlyphFontSizeLabel = \
            QLabel("Moon glyph font size:")
        self.planetMoonGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMoonGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMoonGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMoonGlyphFontSizeLabel,
                   self.planetMoonGlyphFontSizeSpinBox)
        self.planetMoonAbbreviationLabel = \
            QLabel("Moon abbreviation:")
        self.planetMoonAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMoonAbbreviationLabel,
                   self.planetMoonAbbreviationLineEdit)
        self.planetMoonForegroundColorLabel = \
            QLabel("Moon foreground color:")
        self.planetMoonForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMoonForegroundColorLabel,
                   self.planetMoonForegroundColorEditButton)
        self.planetMoonBackgroundColorLabel = \
            QLabel("Moon background color:")
        self.planetMoonBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMoonBackgroundColorLabel,
                   self.planetMoonBackgroundColorEditButton)

        # Mercury
        self.planetMercuryGlyphUnicodeLabel = \
            QLabel("Mercury unicode glyph:")
        self.planetMercuryGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMercuryGlyphUnicodeLabel,
                   self.planetMercuryGlyphUnicodeLineEdit)
        self.planetMercuryGlyphFontSizeLabel = \
            QLabel("Mercury glyph font size:")
        self.planetMercuryGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMercuryGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMercuryGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMercuryGlyphFontSizeLabel,
                   self.planetMercuryGlyphFontSizeSpinBox)
        self.planetMercuryAbbreviationLabel = \
            QLabel("Mercury abbreviation:")
        self.planetMercuryAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMercuryAbbreviationLabel,
                   self.planetMercuryAbbreviationLineEdit)
        self.planetMercuryForegroundColorLabel = \
            QLabel("Mercury foreground color:")
        self.planetMercuryForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMercuryForegroundColorLabel,
                   self.planetMercuryForegroundColorEditButton)
        self.planetMercuryBackgroundColorLabel = \
            QLabel("Mercury background color:")
        self.planetMercuryBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMercuryBackgroundColorLabel,
                   self.planetMercuryBackgroundColorEditButton)

        # Venus
        self.planetVenusGlyphUnicodeLabel = \
            QLabel("Venus unicode glyph:")
        self.planetVenusGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVenusGlyphUnicodeLabel,
                   self.planetVenusGlyphUnicodeLineEdit)
        self.planetVenusGlyphFontSizeLabel = \
            QLabel("Venus glyph font size:")
        self.planetVenusGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetVenusGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetVenusGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetVenusGlyphFontSizeLabel,
                   self.planetVenusGlyphFontSizeSpinBox)
        self.planetVenusAbbreviationLabel = \
            QLabel("Venus abbreviation:")
        self.planetVenusAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVenusAbbreviationLabel,
                   self.planetVenusAbbreviationLineEdit)
        self.planetVenusForegroundColorLabel = \
            QLabel("Venus foreground color:")
        self.planetVenusForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVenusForegroundColorLabel,
                   self.planetVenusForegroundColorEditButton)
        self.planetVenusBackgroundColorLabel = \
            QLabel("Venus background color:")
        self.planetVenusBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVenusBackgroundColorLabel,
                   self.planetVenusBackgroundColorEditButton)

        # Earth
        self.planetEarthGlyphUnicodeLabel = \
            QLabel("Earth unicode glyph:")
        self.planetEarthGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetEarthGlyphUnicodeLabel,
                   self.planetEarthGlyphUnicodeLineEdit)
        self.planetEarthGlyphFontSizeLabel = \
            QLabel("Earth glyph font size:")
        self.planetEarthGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetEarthGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetEarthGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetEarthGlyphFontSizeLabel,
                   self.planetEarthGlyphFontSizeSpinBox)
        self.planetEarthAbbreviationLabel = \
            QLabel("Earth abbreviation:")
        self.planetEarthAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetEarthAbbreviationLabel,
                   self.planetEarthAbbreviationLineEdit)
        self.planetEarthForegroundColorLabel = \
            QLabel("Earth foreground color:")
        self.planetEarthForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetEarthForegroundColorLabel,
                   self.planetEarthForegroundColorEditButton)
        self.planetEarthBackgroundColorLabel = \
            QLabel("Earth background color:")
        self.planetEarthBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetEarthBackgroundColorLabel,
                   self.planetEarthBackgroundColorEditButton)

        # Mars
        self.planetMarsGlyphUnicodeLabel = \
            QLabel("Mars unicode glyph:")
        self.planetMarsGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMarsGlyphUnicodeLabel,
                   self.planetMarsGlyphUnicodeLineEdit)
        self.planetMarsGlyphFontSizeLabel = \
            QLabel("Mars glyph font size:")
        self.planetMarsGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMarsGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMarsGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMarsGlyphFontSizeLabel,
                   self.planetMarsGlyphFontSizeSpinBox)
        self.planetMarsAbbreviationLabel = \
            QLabel("Mars abbreviation:")
        self.planetMarsAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMarsAbbreviationLabel,
                   self.planetMarsAbbreviationLineEdit)
        self.planetMarsForegroundColorLabel = \
            QLabel("Mars foreground color:")
        self.planetMarsForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMarsForegroundColorLabel,
                   self.planetMarsForegroundColorEditButton)
        self.planetMarsBackgroundColorLabel = \
            QLabel("Mars background color:")
        self.planetMarsBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMarsBackgroundColorLabel,
                   self.planetMarsBackgroundColorEditButton)

        # Jupiter
        self.planetJupiterGlyphUnicodeLabel = \
            QLabel("Jupiter unicode glyph:")
        self.planetJupiterGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetJupiterGlyphUnicodeLabel,
                   self.planetJupiterGlyphUnicodeLineEdit)
        self.planetJupiterGlyphFontSizeLabel = \
            QLabel("Jupiter glyph font size:")
        self.planetJupiterGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetJupiterGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetJupiterGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetJupiterGlyphFontSizeLabel,
                   self.planetJupiterGlyphFontSizeSpinBox)
        self.planetJupiterAbbreviationLabel = \
            QLabel("Jupiter abbreviation:")
        self.planetJupiterAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetJupiterAbbreviationLabel,
                   self.planetJupiterAbbreviationLineEdit)
        self.planetJupiterForegroundColorLabel = \
            QLabel("Jupiter foreground color:")
        self.planetJupiterForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetJupiterForegroundColorLabel,
                   self.planetJupiterForegroundColorEditButton)
        self.planetJupiterBackgroundColorLabel = \
            QLabel("Jupiter background color:")
        self.planetJupiterBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetJupiterBackgroundColorLabel,
                   self.planetJupiterBackgroundColorEditButton)

        # Saturn
        self.planetSaturnGlyphUnicodeLabel = \
            QLabel("Saturn unicode glyph:")
        self.planetSaturnGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSaturnGlyphUnicodeLabel,
                   self.planetSaturnGlyphUnicodeLineEdit)
        self.planetSaturnGlyphFontSizeLabel = \
            QLabel("Saturn glyph font size:")
        self.planetSaturnGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetSaturnGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetSaturnGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetSaturnGlyphFontSizeLabel,
                   self.planetSaturnGlyphFontSizeSpinBox)
        self.planetSaturnAbbreviationLabel = \
            QLabel("Saturn abbreviation:")
        self.planetSaturnAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSaturnAbbreviationLabel,
                   self.planetSaturnAbbreviationLineEdit)
        self.planetSaturnForegroundColorLabel = \
            QLabel("Saturn foreground color:")
        self.planetSaturnForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSaturnForegroundColorLabel,
                   self.planetSaturnForegroundColorEditButton)
        self.planetSaturnBackgroundColorLabel = \
            QLabel("Saturn background color:")
        self.planetSaturnBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSaturnBackgroundColorLabel,
                   self.planetSaturnBackgroundColorEditButton)

        # Uranus
        self.planetUranusGlyphUnicodeLabel = \
            QLabel("Uranus unicode glyph:")
        self.planetUranusGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetUranusGlyphUnicodeLabel,
                   self.planetUranusGlyphUnicodeLineEdit)
        self.planetUranusGlyphFontSizeLabel = \
            QLabel("Uranus glyph font size:")
        self.planetUranusGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetUranusGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetUranusGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetUranusGlyphFontSizeLabel,
                   self.planetUranusGlyphFontSizeSpinBox)
        self.planetUranusAbbreviationLabel = \
            QLabel("Uranus abbreviation:")
        self.planetUranusAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetUranusAbbreviationLabel,
                   self.planetUranusAbbreviationLineEdit)
        self.planetUranusForegroundColorLabel = \
            QLabel("Uranus foreground color:")
        self.planetUranusForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetUranusForegroundColorLabel,
                   self.planetUranusForegroundColorEditButton)
        self.planetUranusBackgroundColorLabel = \
            QLabel("Uranus background color:")
        self.planetUranusBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetUranusBackgroundColorLabel,
                   self.planetUranusBackgroundColorEditButton)

        # Neptune
        self.planetNeptuneGlyphUnicodeLabel = \
            QLabel("Neptune unicode glyph:")
        self.planetNeptuneGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetNeptuneGlyphUnicodeLabel,
                   self.planetNeptuneGlyphUnicodeLineEdit)
        self.planetNeptuneGlyphFontSizeLabel = \
            QLabel("Neptune glyph font size:")
        self.planetNeptuneGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetNeptuneGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetNeptuneGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetNeptuneGlyphFontSizeLabel,
                   self.planetNeptuneGlyphFontSizeSpinBox)
        self.planetNeptuneAbbreviationLabel = \
            QLabel("Neptune abbreviation:")
        self.planetNeptuneAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetNeptuneAbbreviationLabel,
                   self.planetNeptuneAbbreviationLineEdit)
        self.planetNeptuneForegroundColorLabel = \
            QLabel("Neptune foreground color:")
        self.planetNeptuneForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetNeptuneForegroundColorLabel,
                   self.planetNeptuneForegroundColorEditButton)
        self.planetNeptuneBackgroundColorLabel = \
            QLabel("Neptune background color:")
        self.planetNeptuneBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetNeptuneBackgroundColorLabel,
                   self.planetNeptuneBackgroundColorEditButton)

        # Pluto
        self.planetPlutoGlyphUnicodeLabel = \
            QLabel("Pluto unicode glyph:")
        self.planetPlutoGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPlutoGlyphUnicodeLabel,
                   self.planetPlutoGlyphUnicodeLineEdit)
        self.planetPlutoGlyphFontSizeLabel = \
            QLabel("Pluto glyph font size:")
        self.planetPlutoGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetPlutoGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetPlutoGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetPlutoGlyphFontSizeLabel,
                   self.planetPlutoGlyphFontSizeSpinBox)
        self.planetPlutoAbbreviationLabel = \
            QLabel("Pluto abbreviation:")
        self.planetPlutoAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPlutoAbbreviationLabel,
                   self.planetPlutoAbbreviationLineEdit)
        self.planetPlutoForegroundColorLabel = \
            QLabel("Pluto foreground color:")
        self.planetPlutoForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPlutoForegroundColorLabel,
                   self.planetPlutoForegroundColorEditButton)
        self.planetPlutoBackgroundColorLabel = \
            QLabel("Pluto background color:")
        self.planetPlutoBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPlutoBackgroundColorLabel,
                   self.planetPlutoBackgroundColorEditButton)

        # MeanNorthNode
        self.planetMeanNorthNodeGlyphUnicodeLabel = \
            QLabel("MeanNorthNode unicode glyph:")
        self.planetMeanNorthNodeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanNorthNodeGlyphUnicodeLabel,
                   self.planetMeanNorthNodeGlyphUnicodeLineEdit)
        self.planetMeanNorthNodeGlyphFontSizeLabel = \
            QLabel("MeanNorthNode glyph font size:")
        self.planetMeanNorthNodeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMeanNorthNodeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMeanNorthNodeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMeanNorthNodeGlyphFontSizeLabel,
                   self.planetMeanNorthNodeGlyphFontSizeSpinBox)
        self.planetMeanNorthNodeAbbreviationLabel = \
            QLabel("MeanNorthNode abbreviation:")
        self.planetMeanNorthNodeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanNorthNodeAbbreviationLabel,
                   self.planetMeanNorthNodeAbbreviationLineEdit)
        self.planetMeanNorthNodeForegroundColorLabel = \
            QLabel("MeanNorthNode foreground color:")
        self.planetMeanNorthNodeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanNorthNodeForegroundColorLabel,
                   self.planetMeanNorthNodeForegroundColorEditButton)
        self.planetMeanNorthNodeBackgroundColorLabel = \
            QLabel("MeanNorthNode background color:")
        self.planetMeanNorthNodeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanNorthNodeBackgroundColorLabel,
                   self.planetMeanNorthNodeBackgroundColorEditButton)

        # MeanSouthNode
        self.planetMeanSouthNodeGlyphUnicodeLabel = \
            QLabel("MeanSouthNode unicode glyph:")
        self.planetMeanSouthNodeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanSouthNodeGlyphUnicodeLabel,
                   self.planetMeanSouthNodeGlyphUnicodeLineEdit)
        self.planetMeanSouthNodeGlyphFontSizeLabel = \
            QLabel("MeanSouthNode glyph font size:")
        self.planetMeanSouthNodeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMeanSouthNodeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMeanSouthNodeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMeanSouthNodeGlyphFontSizeLabel,
                   self.planetMeanSouthNodeGlyphFontSizeSpinBox)
        self.planetMeanSouthNodeAbbreviationLabel = \
            QLabel("MeanSouthNode abbreviation:")
        self.planetMeanSouthNodeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanSouthNodeAbbreviationLabel,
                   self.planetMeanSouthNodeAbbreviationLineEdit)
        self.planetMeanSouthNodeForegroundColorLabel = \
            QLabel("MeanSouthNode foreground color:")
        self.planetMeanSouthNodeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanSouthNodeForegroundColorLabel,
                   self.planetMeanSouthNodeForegroundColorEditButton)
        self.planetMeanSouthNodeBackgroundColorLabel = \
            QLabel("MeanSouthNode background color:")
        self.planetMeanSouthNodeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanSouthNodeBackgroundColorLabel,
                   self.planetMeanSouthNodeBackgroundColorEditButton)

        # TrueNorthNode
        self.planetTrueNorthNodeGlyphUnicodeLabel = \
            QLabel("TrueNorthNode unicode glyph:")
        self.planetTrueNorthNodeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTrueNorthNodeGlyphUnicodeLabel,
                   self.planetTrueNorthNodeGlyphUnicodeLineEdit)
        self.planetTrueNorthNodeGlyphFontSizeLabel = \
            QLabel("TrueNorthNode glyph font size:")
        self.planetTrueNorthNodeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetTrueNorthNodeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetTrueNorthNodeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetTrueNorthNodeGlyphFontSizeLabel,
                   self.planetTrueNorthNodeGlyphFontSizeSpinBox)
        self.planetTrueNorthNodeAbbreviationLabel = \
            QLabel("TrueNorthNode abbreviation:")
        self.planetTrueNorthNodeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTrueNorthNodeAbbreviationLabel,
                   self.planetTrueNorthNodeAbbreviationLineEdit)
        self.planetTrueNorthNodeForegroundColorLabel = \
            QLabel("TrueNorthNode foreground color:")
        self.planetTrueNorthNodeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTrueNorthNodeForegroundColorLabel,
                   self.planetTrueNorthNodeForegroundColorEditButton)
        self.planetTrueNorthNodeBackgroundColorLabel = \
            QLabel("TrueNorthNode background color:")
        self.planetTrueNorthNodeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTrueNorthNodeBackgroundColorLabel,
                   self.planetTrueNorthNodeBackgroundColorEditButton)

        # TrueSouthNode
        self.planetTrueSouthNodeGlyphUnicodeLabel = \
            QLabel("TrueSouthNode unicode glyph:")
        self.planetTrueSouthNodeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTrueSouthNodeGlyphUnicodeLabel,
                   self.planetTrueSouthNodeGlyphUnicodeLineEdit)
        self.planetTrueSouthNodeGlyphFontSizeLabel = \
            QLabel("TrueSouthNode glyph font size:")
        self.planetTrueSouthNodeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetTrueSouthNodeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetTrueSouthNodeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetTrueSouthNodeGlyphFontSizeLabel,
                   self.planetTrueSouthNodeGlyphFontSizeSpinBox)
        self.planetTrueSouthNodeAbbreviationLabel = \
            QLabel("TrueSouthNode abbreviation:")
        self.planetTrueSouthNodeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTrueSouthNodeAbbreviationLabel,
                   self.planetTrueSouthNodeAbbreviationLineEdit)
        self.planetTrueSouthNodeForegroundColorLabel = \
            QLabel("TrueSouthNode foreground color:")
        self.planetTrueSouthNodeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTrueSouthNodeForegroundColorLabel,
                   self.planetTrueSouthNodeForegroundColorEditButton)
        self.planetTrueSouthNodeBackgroundColorLabel = \
            QLabel("TrueSouthNode background color:")
        self.planetTrueSouthNodeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTrueSouthNodeBackgroundColorLabel,
                   self.planetTrueSouthNodeBackgroundColorEditButton)

        # Ceres
        self.planetCeresGlyphUnicodeLabel = \
            QLabel("Ceres unicode glyph:")
        self.planetCeresGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCeresGlyphUnicodeLabel,
                   self.planetCeresGlyphUnicodeLineEdit)
        self.planetCeresGlyphFontSizeLabel = \
            QLabel("Ceres glyph font size:")
        self.planetCeresGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetCeresGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetCeresGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetCeresGlyphFontSizeLabel,
                   self.planetCeresGlyphFontSizeSpinBox)
        self.planetCeresAbbreviationLabel = \
            QLabel("Ceres abbreviation:")
        self.planetCeresAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCeresAbbreviationLabel,
                   self.planetCeresAbbreviationLineEdit)
        self.planetCeresForegroundColorLabel = \
            QLabel("Ceres foreground color:")
        self.planetCeresForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCeresForegroundColorLabel,
                   self.planetCeresForegroundColorEditButton)
        self.planetCeresBackgroundColorLabel = \
            QLabel("Ceres background color:")
        self.planetCeresBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCeresBackgroundColorLabel,
                   self.planetCeresBackgroundColorEditButton)

        # Pallas
        self.planetPallasGlyphUnicodeLabel = \
            QLabel("Pallas unicode glyph:")
        self.planetPallasGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPallasGlyphUnicodeLabel,
                   self.planetPallasGlyphUnicodeLineEdit)
        self.planetPallasGlyphFontSizeLabel = \
            QLabel("Pallas glyph font size:")
        self.planetPallasGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetPallasGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetPallasGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetPallasGlyphFontSizeLabel,
                   self.planetPallasGlyphFontSizeSpinBox)
        self.planetPallasAbbreviationLabel = \
            QLabel("Pallas abbreviation:")
        self.planetPallasAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPallasAbbreviationLabel,
                   self.planetPallasAbbreviationLineEdit)
        self.planetPallasForegroundColorLabel = \
            QLabel("Pallas foreground color:")
        self.planetPallasForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPallasForegroundColorLabel,
                   self.planetPallasForegroundColorEditButton)
        self.planetPallasBackgroundColorLabel = \
            QLabel("Pallas background color:")
        self.planetPallasBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPallasBackgroundColorLabel,
                   self.planetPallasBackgroundColorEditButton)

        # Juno
        self.planetJunoGlyphUnicodeLabel = \
            QLabel("Juno unicode glyph:")
        self.planetJunoGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetJunoGlyphUnicodeLabel,
                   self.planetJunoGlyphUnicodeLineEdit)
        self.planetJunoGlyphFontSizeLabel = \
            QLabel("Juno glyph font size:")
        self.planetJunoGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetJunoGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetJunoGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetJunoGlyphFontSizeLabel,
                   self.planetJunoGlyphFontSizeSpinBox)
        self.planetJunoAbbreviationLabel = \
            QLabel("Juno abbreviation:")
        self.planetJunoAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetJunoAbbreviationLabel,
                   self.planetJunoAbbreviationLineEdit)
        self.planetJunoForegroundColorLabel = \
            QLabel("Juno foreground color:")
        self.planetJunoForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetJunoForegroundColorLabel,
                   self.planetJunoForegroundColorEditButton)
        self.planetJunoBackgroundColorLabel = \
            QLabel("Juno background color:")
        self.planetJunoBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetJunoBackgroundColorLabel,
                   self.planetJunoBackgroundColorEditButton)

        # Vesta
        self.planetVestaGlyphUnicodeLabel = \
            QLabel("Vesta unicode glyph:")
        self.planetVestaGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVestaGlyphUnicodeLabel,
                   self.planetVestaGlyphUnicodeLineEdit)
        self.planetVestaGlyphFontSizeLabel = \
            QLabel("Vesta glyph font size:")
        self.planetVestaGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetVestaGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetVestaGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetVestaGlyphFontSizeLabel,
                   self.planetVestaGlyphFontSizeSpinBox)
        self.planetVestaAbbreviationLabel = \
            QLabel("Vesta abbreviation:")
        self.planetVestaAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVestaAbbreviationLabel,
                   self.planetVestaAbbreviationLineEdit)
        self.planetVestaForegroundColorLabel = \
            QLabel("Vesta foreground color:")
        self.planetVestaForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVestaForegroundColorLabel,
                   self.planetVestaForegroundColorEditButton)
        self.planetVestaBackgroundColorLabel = \
            QLabel("Vesta background color:")
        self.planetVestaBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVestaBackgroundColorLabel,
                   self.planetVestaBackgroundColorEditButton)

        # Chiron
        self.planetChironGlyphUnicodeLabel = \
            QLabel("Chiron unicode glyph:")
        self.planetChironGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetChironGlyphUnicodeLabel,
                   self.planetChironGlyphUnicodeLineEdit)
        self.planetChironGlyphFontSizeLabel = \
            QLabel("Chiron glyph font size:")
        self.planetChironGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetChironGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetChironGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetChironGlyphFontSizeLabel,
                   self.planetChironGlyphFontSizeSpinBox)
        self.planetChironAbbreviationLabel = \
            QLabel("Chiron abbreviation:")
        self.planetChironAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetChironAbbreviationLabel,
                   self.planetChironAbbreviationLineEdit)
        self.planetChironForegroundColorLabel = \
            QLabel("Chiron foreground color:")
        self.planetChironForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetChironForegroundColorLabel,
                   self.planetChironForegroundColorEditButton)
        self.planetChironBackgroundColorLabel = \
            QLabel("Chiron background color:")
        self.planetChironBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetChironBackgroundColorLabel,
                   self.planetChironBackgroundColorEditButton)

        # Gulika
        self.planetGulikaGlyphUnicodeLabel = \
            QLabel("Gulika unicode glyph:")
        self.planetGulikaGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGulikaGlyphUnicodeLabel,
                   self.planetGulikaGlyphUnicodeLineEdit)
        self.planetGulikaGlyphFontSizeLabel = \
            QLabel("Gulika glyph font size:")
        self.planetGulikaGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetGulikaGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetGulikaGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetGulikaGlyphFontSizeLabel,
                   self.planetGulikaGlyphFontSizeSpinBox)
        self.planetGulikaAbbreviationLabel = \
            QLabel("Gulika abbreviation:")
        self.planetGulikaAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGulikaAbbreviationLabel,
                   self.planetGulikaAbbreviationLineEdit)
        self.planetGulikaForegroundColorLabel = \
            QLabel("Gulika foreground color:")
        self.planetGulikaForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGulikaForegroundColorLabel,
                   self.planetGulikaForegroundColorEditButton)
        self.planetGulikaBackgroundColorLabel = \
            QLabel("Gulika background color:")
        self.planetGulikaBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGulikaBackgroundColorLabel,
                   self.planetGulikaBackgroundColorEditButton)

        # Mandi
        self.planetMandiGlyphUnicodeLabel = \
            QLabel("Mandi unicode glyph:")
        self.planetMandiGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMandiGlyphUnicodeLabel,
                   self.planetMandiGlyphUnicodeLineEdit)
        self.planetMandiGlyphFontSizeLabel = \
            QLabel("Mandi glyph font size:")
        self.planetMandiGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMandiGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMandiGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMandiGlyphFontSizeLabel,
                   self.planetMandiGlyphFontSizeSpinBox)
        self.planetMandiAbbreviationLabel = \
            QLabel("Mandi abbreviation:")
        self.planetMandiAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMandiAbbreviationLabel,
                   self.planetMandiAbbreviationLineEdit)
        self.planetMandiForegroundColorLabel = \
            QLabel("Mandi foreground color:")
        self.planetMandiForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMandiForegroundColorLabel,
                   self.planetMandiForegroundColorEditButton)
        self.planetMandiBackgroundColorLabel = \
            QLabel("Mandi background color:")
        self.planetMandiBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMandiBackgroundColorLabel,
                   self.planetMandiBackgroundColorEditButton)

        # MeanOfFive
        self.planetMeanOfFiveGlyphUnicodeLabel = \
            QLabel("MeanOfFive unicode glyph:")
        self.planetMeanOfFiveGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanOfFiveGlyphUnicodeLabel,
                   self.planetMeanOfFiveGlyphUnicodeLineEdit)
        self.planetMeanOfFiveGlyphFontSizeLabel = \
            QLabel("MeanOfFive glyph font size:")
        self.planetMeanOfFiveGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMeanOfFiveGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMeanOfFiveGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMeanOfFiveGlyphFontSizeLabel,
                   self.planetMeanOfFiveGlyphFontSizeSpinBox)
        self.planetMeanOfFiveAbbreviationLabel = \
            QLabel("MeanOfFive abbreviation:")
        self.planetMeanOfFiveAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanOfFiveAbbreviationLabel,
                   self.planetMeanOfFiveAbbreviationLineEdit)
        self.planetMeanOfFiveForegroundColorLabel = \
            QLabel("MeanOfFive foreground color:")
        self.planetMeanOfFiveForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanOfFiveForegroundColorLabel,
                   self.planetMeanOfFiveForegroundColorEditButton)
        self.planetMeanOfFiveBackgroundColorLabel = \
            QLabel("MeanOfFive background color:")
        self.planetMeanOfFiveBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanOfFiveBackgroundColorLabel,
                   self.planetMeanOfFiveBackgroundColorEditButton)

        # CycleOfEight
        self.planetCycleOfEightGlyphUnicodeLabel = \
            QLabel("CycleOfEight unicode glyph:")
        self.planetCycleOfEightGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCycleOfEightGlyphUnicodeLabel,
                   self.planetCycleOfEightGlyphUnicodeLineEdit)
        self.planetCycleOfEightGlyphFontSizeLabel = \
            QLabel("CycleOfEight glyph font size:")
        self.planetCycleOfEightGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetCycleOfEightGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetCycleOfEightGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetCycleOfEightGlyphFontSizeLabel,
                   self.planetCycleOfEightGlyphFontSizeSpinBox)
        self.planetCycleOfEightAbbreviationLabel = \
            QLabel("CycleOfEight abbreviation:")
        self.planetCycleOfEightAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCycleOfEightAbbreviationLabel,
                   self.planetCycleOfEightAbbreviationLineEdit)
        self.planetCycleOfEightForegroundColorLabel = \
            QLabel("CycleOfEight foreground color:")
        self.planetCycleOfEightForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCycleOfEightForegroundColorLabel,
                   self.planetCycleOfEightForegroundColorEditButton)
        self.planetCycleOfEightBackgroundColorLabel = \
            QLabel("CycleOfEight background color:")
        self.planetCycleOfEightBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCycleOfEightBackgroundColorLabel,
                   self.planetCycleOfEightBackgroundColorEditButton)


        # Label to tell the user that not all settings will be applied
        # on existing windows when the 'Okay' button is pressed.
        endl = os.linesep
        noteLabel = \
            QLabel("Note: Upon clicking the 'Okay' button, the new " + \
                   "settings may not be immediately " + \
                   endl + \
                   "applied to the open PriceChartDocuments.  " + \
                   "You may need to close and re-open " + \
                   endl + \
                   "the PriceChartDocuments to get the changes.")

        # Button for resetting all the above edit widgets.
        self.planetSymbolResetAllToDefaultButton = \
            QPushButton("Reset all the above to original default values")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.planetSymbolResetAllToDefaultButton)
        hlayout.addStretch()

        vlayout = QVBoxLayout()
        vlayout.addLayout(formLayout)
        vlayout.addSpacing(20)
        vlayout.addWidget(noteLabel)
        vlayout.addSpacing(10)
        vlayout.addLayout(hlayout)

        self.planetSymbolSettingsGroupBox.setLayout(vlayout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.planetSymbolSettingsGroupBox)
        self.planetSymbolSettingsGroupBox = scrollArea

        return self.planetSymbolSettingsGroupBox


    def _buildNonPlanetSymbolSettingsWidget(self):
        """Builds a QWidget for editing the settings of Non-Planets as
        displayed in the UI.  This is things like ascendant, and various
        lagnas, etc.

        Returned widget is self.nonPlanetSymbolSettingsGroupBox.
        """

        self.nonPlanetSymbolSettingsGroupBox = QGroupBox("Non-Planet settings:")

        formLayout = QFormLayout()
        formLayout.setLabelAlignment(Qt.AlignLeft)

        # Retrograde
        self.planetRetrogradeGlyphUnicodeLabel = \
            QLabel("Retrograde unicode glyph:")
        self.planetRetrogradeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetRetrogradeGlyphUnicodeLabel,
                   self.planetRetrogradeGlyphUnicodeLineEdit)
        self.planetRetrogradeGlyphFontSizeLabel = \
            QLabel("Retrograde glyph font size:")
        self.planetRetrogradeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetRetrogradeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetRetrogradeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetRetrogradeGlyphFontSizeLabel,
                   self.planetRetrogradeGlyphFontSizeSpinBox)
        self.planetRetrogradeAbbreviationLabel = \
            QLabel("Retrograde abbreviation:")
        self.planetRetrogradeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetRetrogradeAbbreviationLabel,
                   self.planetRetrogradeAbbreviationLineEdit)
        self.planetRetrogradeForegroundColorLabel = \
            QLabel("Retrograde foreground color:")
        self.planetRetrogradeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetRetrogradeForegroundColorLabel,
                   self.planetRetrogradeForegroundColorEditButton)
        self.planetRetrogradeBackgroundColorLabel = \
            QLabel("Retrograde background color:")
        self.planetRetrogradeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetRetrogradeBackgroundColorLabel,
                   self.planetRetrogradeBackgroundColorEditButton)

        # Ascendant
        self.planetAscendantGlyphUnicodeLabel = \
            QLabel("Ascendant unicode glyph:")
        self.planetAscendantGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAscendantGlyphUnicodeLabel,
                   self.planetAscendantGlyphUnicodeLineEdit)
        self.planetAscendantGlyphFontSizeLabel = \
            QLabel("Ascendant glyph font size:")
        self.planetAscendantGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetAscendantGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetAscendantGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetAscendantGlyphFontSizeLabel,
                   self.planetAscendantGlyphFontSizeSpinBox)
        self.planetAscendantAbbreviationLabel = \
            QLabel("Ascendant abbreviation:")
        self.planetAscendantAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAscendantAbbreviationLabel,
                   self.planetAscendantAbbreviationLineEdit)
        self.planetAscendantForegroundColorLabel = \
            QLabel("Ascendant foreground color:")
        self.planetAscendantForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAscendantForegroundColorLabel,
                   self.planetAscendantForegroundColorEditButton)
        self.planetAscendantBackgroundColorLabel = \
            QLabel("Ascendant background color:")
        self.planetAscendantBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAscendantBackgroundColorLabel,
                   self.planetAscendantBackgroundColorEditButton)

        # Midheaven
        self.planetMidheavenGlyphUnicodeLabel = \
            QLabel("Midheaven unicode glyph:")
        self.planetMidheavenGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMidheavenGlyphUnicodeLabel,
                   self.planetMidheavenGlyphUnicodeLineEdit)
        self.planetMidheavenGlyphFontSizeLabel = \
            QLabel("Midheaven glyph font size:")
        self.planetMidheavenGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMidheavenGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMidheavenGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMidheavenGlyphFontSizeLabel,
                   self.planetMidheavenGlyphFontSizeSpinBox)
        self.planetMidheavenAbbreviationLabel = \
            QLabel("Midheaven abbreviation:")
        self.planetMidheavenAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMidheavenAbbreviationLabel,
                   self.planetMidheavenAbbreviationLineEdit)
        self.planetMidheavenForegroundColorLabel = \
            QLabel("Midheaven foreground color:")
        self.planetMidheavenForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMidheavenForegroundColorLabel,
                   self.planetMidheavenForegroundColorEditButton)
        self.planetMidheavenBackgroundColorLabel = \
            QLabel("Midheaven background color:")
        self.planetMidheavenBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMidheavenBackgroundColorLabel,
                   self.planetMidheavenBackgroundColorEditButton)

        # HoraLagna
        self.planetHoraLagnaGlyphUnicodeLabel = \
            QLabel("HoraLagna unicode glyph:")
        self.planetHoraLagnaGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetHoraLagnaGlyphUnicodeLabel,
                   self.planetHoraLagnaGlyphUnicodeLineEdit)
        self.planetHoraLagnaGlyphFontSizeLabel = \
            QLabel("HoraLagna glyph font size:")
        self.planetHoraLagnaGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetHoraLagnaGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetHoraLagnaGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetHoraLagnaGlyphFontSizeLabel,
                   self.planetHoraLagnaGlyphFontSizeSpinBox)
        self.planetHoraLagnaAbbreviationLabel = \
            QLabel("HoraLagna abbreviation:")
        self.planetHoraLagnaAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetHoraLagnaAbbreviationLabel,
                   self.planetHoraLagnaAbbreviationLineEdit)
        self.planetHoraLagnaForegroundColorLabel = \
            QLabel("HoraLagna foreground color:")
        self.planetHoraLagnaForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetHoraLagnaForegroundColorLabel,
                   self.planetHoraLagnaForegroundColorEditButton)
        self.planetHoraLagnaBackgroundColorLabel = \
            QLabel("HoraLagna background color:")
        self.planetHoraLagnaBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetHoraLagnaBackgroundColorLabel,
                   self.planetHoraLagnaBackgroundColorEditButton)

        # GhatiLagna
        self.planetGhatiLagnaGlyphUnicodeLabel = \
            QLabel("GhatiLagna unicode glyph:")
        self.planetGhatiLagnaGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGhatiLagnaGlyphUnicodeLabel,
                   self.planetGhatiLagnaGlyphUnicodeLineEdit)
        self.planetGhatiLagnaGlyphFontSizeLabel = \
            QLabel("GhatiLagna glyph font size:")
        self.planetGhatiLagnaGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetGhatiLagnaGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetGhatiLagnaGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetGhatiLagnaGlyphFontSizeLabel,
                   self.planetGhatiLagnaGlyphFontSizeSpinBox)
        self.planetGhatiLagnaAbbreviationLabel = \
            QLabel("GhatiLagna abbreviation:")
        self.planetGhatiLagnaAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGhatiLagnaAbbreviationLabel,
                   self.planetGhatiLagnaAbbreviationLineEdit)
        self.planetGhatiLagnaForegroundColorLabel = \
            QLabel("GhatiLagna foreground color:")
        self.planetGhatiLagnaForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGhatiLagnaForegroundColorLabel,
                   self.planetGhatiLagnaForegroundColorEditButton)
        self.planetGhatiLagnaBackgroundColorLabel = \
            QLabel("GhatiLagna background color:")
        self.planetGhatiLagnaBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGhatiLagnaBackgroundColorLabel,
                   self.planetGhatiLagnaBackgroundColorEditButton)

        # MeanLunarApogee
        self.planetMeanLunarApogeeGlyphUnicodeLabel = \
            QLabel("MeanLunarApogee unicode glyph:")
        self.planetMeanLunarApogeeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanLunarApogeeGlyphUnicodeLabel,
                   self.planetMeanLunarApogeeGlyphUnicodeLineEdit)
        self.planetMeanLunarApogeeGlyphFontSizeLabel = \
            QLabel("MeanLunarApogee glyph font size:")
        self.planetMeanLunarApogeeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetMeanLunarApogeeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetMeanLunarApogeeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetMeanLunarApogeeGlyphFontSizeLabel,
                   self.planetMeanLunarApogeeGlyphFontSizeSpinBox)
        self.planetMeanLunarApogeeAbbreviationLabel = \
            QLabel("MeanLunarApogee abbreviation:")
        self.planetMeanLunarApogeeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetMeanLunarApogeeAbbreviationLabel,
                   self.planetMeanLunarApogeeAbbreviationLineEdit)
        self.planetMeanLunarApogeeForegroundColorLabel = \
            QLabel("MeanLunarApogee foreground color:")
        self.planetMeanLunarApogeeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanLunarApogeeForegroundColorLabel,
                   self.planetMeanLunarApogeeForegroundColorEditButton)
        self.planetMeanLunarApogeeBackgroundColorLabel = \
            QLabel("MeanLunarApogee background color:")
        self.planetMeanLunarApogeeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetMeanLunarApogeeBackgroundColorLabel,
                   self.planetMeanLunarApogeeBackgroundColorEditButton)

        # OsculatingLunarApogee
        self.planetOsculatingLunarApogeeGlyphUnicodeLabel = \
            QLabel("OsculatingLunarApogee unicode glyph:")
        self.planetOsculatingLunarApogeeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetOsculatingLunarApogeeGlyphUnicodeLabel,
                   self.planetOsculatingLunarApogeeGlyphUnicodeLineEdit)
        self.planetOsculatingLunarApogeeGlyphFontSizeLabel = \
            QLabel("OsculatingLunarApogee glyph font size:")
        self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetOsculatingLunarApogeeGlyphFontSizeLabel,
                   self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox)
        self.planetOsculatingLunarApogeeAbbreviationLabel = \
            QLabel("OsculatingLunarApogee abbreviation:")
        self.planetOsculatingLunarApogeeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetOsculatingLunarApogeeAbbreviationLabel,
                   self.planetOsculatingLunarApogeeAbbreviationLineEdit)
        self.planetOsculatingLunarApogeeForegroundColorLabel = \
            QLabel("OsculatingLunarApogee foreground color:")
        self.planetOsculatingLunarApogeeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetOsculatingLunarApogeeForegroundColorLabel,
                   self.planetOsculatingLunarApogeeForegroundColorEditButton)
        self.planetOsculatingLunarApogeeBackgroundColorLabel = \
            QLabel("OsculatingLunarApogee background color:")
        self.planetOsculatingLunarApogeeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetOsculatingLunarApogeeBackgroundColorLabel,
                   self.planetOsculatingLunarApogeeBackgroundColorEditButton)

        # InterpolatedLunarApogee
        self.planetInterpolatedLunarApogeeGlyphUnicodeLabel = \
            QLabel("InterpolatedLunarApogee unicode glyph:")
        self.planetInterpolatedLunarApogeeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetInterpolatedLunarApogeeGlyphUnicodeLabel,
                   self.planetInterpolatedLunarApogeeGlyphUnicodeLineEdit)
        self.planetInterpolatedLunarApogeeGlyphFontSizeLabel = \
            QLabel("InterpolatedLunarApogee glyph font size:")
        self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetInterpolatedLunarApogeeGlyphFontSizeLabel,
                   self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox)
        self.planetInterpolatedLunarApogeeAbbreviationLabel = \
            QLabel("InterpolatedLunarApogee abbreviation:")
        self.planetInterpolatedLunarApogeeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetInterpolatedLunarApogeeAbbreviationLabel,
                   self.planetInterpolatedLunarApogeeAbbreviationLineEdit)
        self.planetInterpolatedLunarApogeeForegroundColorLabel = \
            QLabel("InterpolatedLunarApogee foreground color:")
        self.planetInterpolatedLunarApogeeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetInterpolatedLunarApogeeForegroundColorLabel,
                   self.planetInterpolatedLunarApogeeForegroundColorEditButton)
        self.planetInterpolatedLunarApogeeBackgroundColorLabel = \
            QLabel("InterpolatedLunarApogee background color:")
        self.planetInterpolatedLunarApogeeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetInterpolatedLunarApogeeBackgroundColorLabel,
                   self.planetInterpolatedLunarApogeeBackgroundColorEditButton)

        # InterpolatedLunarPerigee
        self.planetInterpolatedLunarPerigeeGlyphUnicodeLabel = \
            QLabel("InterpolatedLunarPerigee unicode glyph:")
        self.planetInterpolatedLunarPerigeeGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetInterpolatedLunarPerigeeGlyphUnicodeLabel,
                   self.planetInterpolatedLunarPerigeeGlyphUnicodeLineEdit)
        self.planetInterpolatedLunarPerigeeGlyphFontSizeLabel = \
            QLabel("InterpolatedLunarPerigee glyph font size:")
        self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetInterpolatedLunarPerigeeGlyphFontSizeLabel,
                   self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox)
        self.planetInterpolatedLunarPerigeeAbbreviationLabel = \
            QLabel("InterpolatedLunarPerigee abbreviation:")
        self.planetInterpolatedLunarPerigeeAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetInterpolatedLunarPerigeeAbbreviationLabel,
                   self.planetInterpolatedLunarPerigeeAbbreviationLineEdit)
        self.planetInterpolatedLunarPerigeeForegroundColorLabel = \
            QLabel("InterpolatedLunarPerigee foreground color:")
        self.planetInterpolatedLunarPerigeeForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetInterpolatedLunarPerigeeForegroundColorLabel,
                   self.planetInterpolatedLunarPerigeeForegroundColorEditButton)
        self.planetInterpolatedLunarPerigeeBackgroundColorLabel = \
            QLabel("InterpolatedLunarPerigee background color:")
        self.planetInterpolatedLunarPerigeeBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetInterpolatedLunarPerigeeBackgroundColorLabel,
                   self.planetInterpolatedLunarPerigeeBackgroundColorEditButton)

        # Label to tell the user that not all settings will be applied
        # on existing windows when the 'Okay' button is pressed.
        endl = os.linesep
        noteLabel = \
            QLabel("Note: Upon clicking the 'Okay' button, the new " + \
                   "settings may not be immediately " + \
                   endl + \
                   "applied to the open PriceChartDocuments.  " + \
                   "You may need to close and re-open " + \
                   endl + \
                   "the PriceChartDocuments to get the changes.")

        # Button for resetting all the above edit widgets.
        self.nonPlanetSymbolResetAllToDefaultButton = \
            QPushButton("Reset all the above to original default values")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.nonPlanetSymbolResetAllToDefaultButton)
        hlayout.addStretch()

        vlayout = QVBoxLayout()
        vlayout.addLayout(formLayout)
        vlayout.addSpacing(20)
        vlayout.addWidget(noteLabel)
        vlayout.addSpacing(10)
        vlayout.addLayout(hlayout)

        self.nonPlanetSymbolSettingsGroupBox.setLayout(vlayout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.nonPlanetSymbolSettingsGroupBox)
        self.nonPlanetSymbolSettingsGroupBox = scrollArea

        return self.nonPlanetSymbolSettingsGroupBox

    def _buildSignSymbolSettingsWidget(self):
        """Builds a QWidget for editing the settings of Zodiac Sign symbols as
        displayed in the UI.

        Returned widget is self.signSymbolSettingsGroupBox.
        """

        self.signSymbolSettingsGroupBox = QGroupBox("Zodiac Sign settings:")

        formLayout = QFormLayout()
        formLayout.setLabelAlignment(Qt.AlignLeft)

        # Aries
        self.planetAriesGlyphUnicodeLabel = \
            QLabel("Aries unicode glyph:")
        self.planetAriesGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAriesGlyphUnicodeLabel,
                   self.planetAriesGlyphUnicodeLineEdit)
        self.planetAriesGlyphFontSizeLabel = \
            QLabel("Aries glyph font size:")
        self.planetAriesGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetAriesGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetAriesGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetAriesGlyphFontSizeLabel,
                   self.planetAriesGlyphFontSizeSpinBox)
        self.planetAriesAbbreviationLabel = \
            QLabel("Aries abbreviation:")
        self.planetAriesAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAriesAbbreviationLabel,
                   self.planetAriesAbbreviationLineEdit)
        self.planetAriesForegroundColorLabel = \
            QLabel("Aries foreground color:")
        self.planetAriesForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAriesForegroundColorLabel,
                   self.planetAriesForegroundColorEditButton)
        self.planetAriesBackgroundColorLabel = \
            QLabel("Aries background color:")
        self.planetAriesBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAriesBackgroundColorLabel,
                   self.planetAriesBackgroundColorEditButton)

        # Taurus
        self.planetTaurusGlyphUnicodeLabel = \
            QLabel("Taurus unicode glyph:")
        self.planetTaurusGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTaurusGlyphUnicodeLabel,
                   self.planetTaurusGlyphUnicodeLineEdit)
        self.planetTaurusGlyphFontSizeLabel = \
            QLabel("Taurus glyph font size:")
        self.planetTaurusGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetTaurusGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetTaurusGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetTaurusGlyphFontSizeLabel,
                   self.planetTaurusGlyphFontSizeSpinBox)
        self.planetTaurusAbbreviationLabel = \
            QLabel("Taurus abbreviation:")
        self.planetTaurusAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetTaurusAbbreviationLabel,
                   self.planetTaurusAbbreviationLineEdit)
        self.planetTaurusForegroundColorLabel = \
            QLabel("Taurus foreground color:")
        self.planetTaurusForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTaurusForegroundColorLabel,
                   self.planetTaurusForegroundColorEditButton)
        self.planetTaurusBackgroundColorLabel = \
            QLabel("Taurus background color:")
        self.planetTaurusBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetTaurusBackgroundColorLabel,
                   self.planetTaurusBackgroundColorEditButton)

        # Gemini
        self.planetGeminiGlyphUnicodeLabel = \
            QLabel("Gemini unicode glyph:")
        self.planetGeminiGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGeminiGlyphUnicodeLabel,
                   self.planetGeminiGlyphUnicodeLineEdit)
        self.planetGeminiGlyphFontSizeLabel = \
            QLabel("Gemini glyph font size:")
        self.planetGeminiGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetGeminiGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetGeminiGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetGeminiGlyphFontSizeLabel,
                   self.planetGeminiGlyphFontSizeSpinBox)
        self.planetGeminiAbbreviationLabel = \
            QLabel("Gemini abbreviation:")
        self.planetGeminiAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetGeminiAbbreviationLabel,
                   self.planetGeminiAbbreviationLineEdit)
        self.planetGeminiForegroundColorLabel = \
            QLabel("Gemini foreground color:")
        self.planetGeminiForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGeminiForegroundColorLabel,
                   self.planetGeminiForegroundColorEditButton)
        self.planetGeminiBackgroundColorLabel = \
            QLabel("Gemini background color:")
        self.planetGeminiBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetGeminiBackgroundColorLabel,
                   self.planetGeminiBackgroundColorEditButton)

        # Cancer
        self.planetCancerGlyphUnicodeLabel = \
            QLabel("Cancer unicode glyph:")
        self.planetCancerGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCancerGlyphUnicodeLabel,
                   self.planetCancerGlyphUnicodeLineEdit)
        self.planetCancerGlyphFontSizeLabel = \
            QLabel("Cancer glyph font size:")
        self.planetCancerGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetCancerGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetCancerGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetCancerGlyphFontSizeLabel,
                   self.planetCancerGlyphFontSizeSpinBox)
        self.planetCancerAbbreviationLabel = \
            QLabel("Cancer abbreviation:")
        self.planetCancerAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCancerAbbreviationLabel,
                   self.planetCancerAbbreviationLineEdit)
        self.planetCancerForegroundColorLabel = \
            QLabel("Cancer foreground color:")
        self.planetCancerForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCancerForegroundColorLabel,
                   self.planetCancerForegroundColorEditButton)
        self.planetCancerBackgroundColorLabel = \
            QLabel("Cancer background color:")
        self.planetCancerBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCancerBackgroundColorLabel,
                   self.planetCancerBackgroundColorEditButton)

        # Leo
        self.planetLeoGlyphUnicodeLabel = \
            QLabel("Leo unicode glyph:")
        self.planetLeoGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetLeoGlyphUnicodeLabel,
                   self.planetLeoGlyphUnicodeLineEdit)
        self.planetLeoGlyphFontSizeLabel = \
            QLabel("Leo glyph font size:")
        self.planetLeoGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetLeoGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetLeoGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetLeoGlyphFontSizeLabel,
                   self.planetLeoGlyphFontSizeSpinBox)
        self.planetLeoAbbreviationLabel = \
            QLabel("Leo abbreviation:")
        self.planetLeoAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetLeoAbbreviationLabel,
                   self.planetLeoAbbreviationLineEdit)
        self.planetLeoForegroundColorLabel = \
            QLabel("Leo foreground color:")
        self.planetLeoForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetLeoForegroundColorLabel,
                   self.planetLeoForegroundColorEditButton)
        self.planetLeoBackgroundColorLabel = \
            QLabel("Leo background color:")
        self.planetLeoBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetLeoBackgroundColorLabel,
                   self.planetLeoBackgroundColorEditButton)

        # Virgo
        self.planetVirgoGlyphUnicodeLabel = \
            QLabel("Virgo unicode glyph:")
        self.planetVirgoGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVirgoGlyphUnicodeLabel,
                   self.planetVirgoGlyphUnicodeLineEdit)
        self.planetVirgoGlyphFontSizeLabel = \
            QLabel("Virgo glyph font size:")
        self.planetVirgoGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetVirgoGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetVirgoGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetVirgoGlyphFontSizeLabel,
                   self.planetVirgoGlyphFontSizeSpinBox)
        self.planetVirgoAbbreviationLabel = \
            QLabel("Virgo abbreviation:")
        self.planetVirgoAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetVirgoAbbreviationLabel,
                   self.planetVirgoAbbreviationLineEdit)
        self.planetVirgoForegroundColorLabel = \
            QLabel("Virgo foreground color:")
        self.planetVirgoForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVirgoForegroundColorLabel,
                   self.planetVirgoForegroundColorEditButton)
        self.planetVirgoBackgroundColorLabel = \
            QLabel("Virgo background color:")
        self.planetVirgoBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetVirgoBackgroundColorLabel,
                   self.planetVirgoBackgroundColorEditButton)

        # Libra
        self.planetLibraGlyphUnicodeLabel = \
            QLabel("Libra unicode glyph:")
        self.planetLibraGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetLibraGlyphUnicodeLabel,
                   self.planetLibraGlyphUnicodeLineEdit)
        self.planetLibraGlyphFontSizeLabel = \
            QLabel("Libra glyph font size:")
        self.planetLibraGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetLibraGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetLibraGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetLibraGlyphFontSizeLabel,
                   self.planetLibraGlyphFontSizeSpinBox)
        self.planetLibraAbbreviationLabel = \
            QLabel("Libra abbreviation:")
        self.planetLibraAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetLibraAbbreviationLabel,
                   self.planetLibraAbbreviationLineEdit)
        self.planetLibraForegroundColorLabel = \
            QLabel("Libra foreground color:")
        self.planetLibraForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetLibraForegroundColorLabel,
                   self.planetLibraForegroundColorEditButton)
        self.planetLibraBackgroundColorLabel = \
            QLabel("Libra background color:")
        self.planetLibraBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetLibraBackgroundColorLabel,
                   self.planetLibraBackgroundColorEditButton)

        # Scorpio
        self.planetScorpioGlyphUnicodeLabel = \
            QLabel("Scorpio unicode glyph:")
        self.planetScorpioGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetScorpioGlyphUnicodeLabel,
                   self.planetScorpioGlyphUnicodeLineEdit)
        self.planetScorpioGlyphFontSizeLabel = \
            QLabel("Scorpio glyph font size:")
        self.planetScorpioGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetScorpioGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetScorpioGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetScorpioGlyphFontSizeLabel,
                   self.planetScorpioGlyphFontSizeSpinBox)
        self.planetScorpioAbbreviationLabel = \
            QLabel("Scorpio abbreviation:")
        self.planetScorpioAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetScorpioAbbreviationLabel,
                   self.planetScorpioAbbreviationLineEdit)
        self.planetScorpioForegroundColorLabel = \
            QLabel("Scorpio foreground color:")
        self.planetScorpioForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetScorpioForegroundColorLabel,
                   self.planetScorpioForegroundColorEditButton)
        self.planetScorpioBackgroundColorLabel = \
            QLabel("Scorpio background color:")
        self.planetScorpioBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetScorpioBackgroundColorLabel,
                   self.planetScorpioBackgroundColorEditButton)

        # Sagittarius
        self.planetSagittariusGlyphUnicodeLabel = \
            QLabel("Sagittarius unicode glyph:")
        self.planetSagittariusGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSagittariusGlyphUnicodeLabel,
                   self.planetSagittariusGlyphUnicodeLineEdit)
        self.planetSagittariusGlyphFontSizeLabel = \
            QLabel("Sagittarius glyph font size:")
        self.planetSagittariusGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetSagittariusGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetSagittariusGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetSagittariusGlyphFontSizeLabel,
                   self.planetSagittariusGlyphFontSizeSpinBox)
        self.planetSagittariusAbbreviationLabel = \
            QLabel("Sagittarius abbreviation:")
        self.planetSagittariusAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetSagittariusAbbreviationLabel,
                   self.planetSagittariusAbbreviationLineEdit)
        self.planetSagittariusForegroundColorLabel = \
            QLabel("Sagittarius foreground color:")
        self.planetSagittariusForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSagittariusForegroundColorLabel,
                   self.planetSagittariusForegroundColorEditButton)
        self.planetSagittariusBackgroundColorLabel = \
            QLabel("Sagittarius background color:")
        self.planetSagittariusBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetSagittariusBackgroundColorLabel,
                   self.planetSagittariusBackgroundColorEditButton)

        # Capricorn
        self.planetCapricornGlyphUnicodeLabel = \
            QLabel("Capricorn unicode glyph:")
        self.planetCapricornGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCapricornGlyphUnicodeLabel,
                   self.planetCapricornGlyphUnicodeLineEdit)
        self.planetCapricornGlyphFontSizeLabel = \
            QLabel("Capricorn glyph font size:")
        self.planetCapricornGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetCapricornGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetCapricornGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetCapricornGlyphFontSizeLabel,
                   self.planetCapricornGlyphFontSizeSpinBox)
        self.planetCapricornAbbreviationLabel = \
            QLabel("Capricorn abbreviation:")
        self.planetCapricornAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetCapricornAbbreviationLabel,
                   self.planetCapricornAbbreviationLineEdit)
        self.planetCapricornForegroundColorLabel = \
            QLabel("Capricorn foreground color:")
        self.planetCapricornForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCapricornForegroundColorLabel,
                   self.planetCapricornForegroundColorEditButton)
        self.planetCapricornBackgroundColorLabel = \
            QLabel("Capricorn background color:")
        self.planetCapricornBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetCapricornBackgroundColorLabel,
                   self.planetCapricornBackgroundColorEditButton)

        # Aquarius
        self.planetAquariusGlyphUnicodeLabel = \
            QLabel("Aquarius unicode glyph:")
        self.planetAquariusGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAquariusGlyphUnicodeLabel,
                   self.planetAquariusGlyphUnicodeLineEdit)
        self.planetAquariusGlyphFontSizeLabel = \
            QLabel("Aquarius glyph font size:")
        self.planetAquariusGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetAquariusGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetAquariusGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetAquariusGlyphFontSizeLabel,
                   self.planetAquariusGlyphFontSizeSpinBox)
        self.planetAquariusAbbreviationLabel = \
            QLabel("Aquarius abbreviation:")
        self.planetAquariusAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetAquariusAbbreviationLabel,
                   self.planetAquariusAbbreviationLineEdit)
        self.planetAquariusForegroundColorLabel = \
            QLabel("Aquarius foreground color:")
        self.planetAquariusForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAquariusForegroundColorLabel,
                   self.planetAquariusForegroundColorEditButton)
        self.planetAquariusBackgroundColorLabel = \
            QLabel("Aquarius background color:")
        self.planetAquariusBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetAquariusBackgroundColorLabel,
                   self.planetAquariusBackgroundColorEditButton)

        # Pisces
        self.planetPiscesGlyphUnicodeLabel = \
            QLabel("Pisces unicode glyph:")
        self.planetPiscesGlyphUnicodeLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPiscesGlyphUnicodeLabel,
                   self.planetPiscesGlyphUnicodeLineEdit)
        self.planetPiscesGlyphFontSizeLabel = \
            QLabel("Pisces glyph font size:")
        self.planetPiscesGlyphFontSizeSpinBox = \
            QDoubleSpinBox()
        self.planetPiscesGlyphFontSizeSpinBox.setMinimum(0.01)
        self.planetPiscesGlyphFontSizeSpinBox.setMaximum(1000)
        formLayout.\
            addRow(self.planetPiscesGlyphFontSizeLabel,
                   self.planetPiscesGlyphFontSizeSpinBox)
        self.planetPiscesAbbreviationLabel = \
            QLabel("Pisces abbreviation:")
        self.planetPiscesAbbreviationLineEdit = \
            QLineEdit()
        formLayout.\
            addRow(self.planetPiscesAbbreviationLabel,
                   self.planetPiscesAbbreviationLineEdit)
        self.planetPiscesForegroundColorLabel = \
            QLabel("Pisces foreground color:")
        self.planetPiscesForegroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPiscesForegroundColorLabel,
                   self.planetPiscesForegroundColorEditButton)
        self.planetPiscesBackgroundColorLabel = \
            QLabel("Pisces background color:")
        self.planetPiscesBackgroundColorEditButton = \
            ColorEditPushButton()
        formLayout.\
            addRow(self.planetPiscesBackgroundColorLabel,
                   self.planetPiscesBackgroundColorEditButton)

        # Label to tell the user that not all settings will be applied
        # on existing windows when the 'Okay' button is pressed.
        endl = os.linesep
        noteLabel = \
            QLabel("Note: Upon clicking the 'Okay' button, the new " + \
                   "settings may not be immediately " + \
                   endl + \
                   "applied to the open PriceChartDocuments.  " + \
                   "You may need to close and re-open " + \
                   endl + \
                   "the PriceChartDocuments to get the changes.")

        # Button for resetting all the above edit widgets.
        self.signSymbolResetAllToDefaultButton = \
            QPushButton("Reset all the above to original default values")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.signSymbolResetAllToDefaultButton)
        hlayout.addStretch()

        vlayout = QVBoxLayout()
        vlayout.addLayout(formLayout)
        vlayout.addSpacing(20)
        vlayout.addWidget(noteLabel)
        vlayout.addSpacing(10)
        vlayout.addLayout(hlayout)

        self.signSymbolSettingsGroupBox.setLayout(vlayout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.signSymbolSettingsGroupBox)
        self.signSymbolSettingsGroupBox = scrollArea

        return self.signSymbolSettingsGroupBox

    def loadValuesFromSettings(self):
        """Loads the widgets with values from the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        self.log.debug("Entered loadValuesFromSettings()")

        self._priceBarLoadValuesFromSettings()
        self._planetSymbolLoadValuesFromSettings()
        self._nonPlanetSymbolLoadValuesFromSettings()
        self._signSymbolLoadValuesFromSettings()
        
        self.log.debug("Exiting loadValuesFromSettings()")
        
    def saveValuesToSettings(self):
        """Saves the values in the widgets to the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """
    
        self.log.debug("Entered saveValuesToSettings()")

        self._priceBarSaveValuesToSettings()
        self._planetSymbolSaveValuesToSettings()
        self._nonPlanetSymbolSaveValuesToSettings()
        self._signSymbolSaveValuesToSettings()
        
        self.log.debug("Exiting saveValuesToSettings()")


    def _priceBarLoadValuesFromSettings(self):
        """Loads the widgets with values from the QSettings object.
        This does it for the PriceBarChart settings.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()
    
        # PriceBarChart zoom-in/out scale factor (float).
        key = SettingsKeys.zoomScaleFactorSettingsKey 
        value = float(settings.value(key, \
            SettingsKeys.zoomScaleFactorSettingsDefValue))
        self.zoomScaleFactorSpinBox.setValue(value)

        # PriceBarChart higherPriceBarColor (QColor).
        key = SettingsKeys.higherPriceBarColorSettingsKey 
        value = QColor(settings.value(key, \
            SettingsKeys.higherPriceBarColorSettingsDefValue))
        self.higherPriceBarColorEditButton.setColor(value)

        # PriceBarChart lowerPriceBarColor (QColor).
        key = SettingsKeys.lowerPriceBarColorSettingsKey 
        value = QColor(settings.value(key, \
            SettingsKeys.lowerPriceBarColorSettingsDefValue))
        self.lowerPriceBarColorEditButton.setColor(value)

        # PriceBarChart barCountGraphicsItemColor (QColor).
        key = SettingsKeys.barCountGraphicsItemColorSettingsKey
        value = QColor(settings.value(key, \
            SettingsKeys.barCountGraphicsItemColorSettingsDefValue))
        self.barCountGraphicsItemColorEditButton.setColor(value)

        # PriceBarChart barCountGraphicsItemTextColor (QColor).
        key = SettingsKeys.barCountGraphicsItemTextColorSettingsKey
        value = QColor(settings.value(key, \
            SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue))
        self.barCountGraphicsItemTextColorEditButton.setColor(value)


    def _planetSymbolLoadValuesFromSettings(self):
        """Loads the widgets with values from the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()

        # Sun
        key = SettingsKeys.planetSunGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetSunGlyphUnicodeDefValue))
        self.planetSunGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetSunGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetSunGlyphFontSizeDefValue))
        self.planetSunGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetSunAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetSunAbbreviationDefValue))
        self.planetSunAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetSunForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetSunForegroundColorDefValue))
        self.planetSunForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetSunBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetSunBackgroundColorDefValue))
        self.planetSunBackgroundColorEditButton.\
            setColor(value)

        # Moon
        key = SettingsKeys.planetMoonGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMoonGlyphUnicodeDefValue))
        self.planetMoonGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMoonGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMoonGlyphFontSizeDefValue))
        self.planetMoonGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMoonAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMoonAbbreviationDefValue))
        self.planetMoonAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMoonForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMoonForegroundColorDefValue))
        self.planetMoonForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMoonBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMoonBackgroundColorDefValue))
        self.planetMoonBackgroundColorEditButton.\
            setColor(value)

        # Mercury
        key = SettingsKeys.planetMercuryGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMercuryGlyphUnicodeDefValue))
        self.planetMercuryGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMercuryGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMercuryGlyphFontSizeDefValue))
        self.planetMercuryGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMercuryAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMercuryAbbreviationDefValue))
        self.planetMercuryAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMercuryForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMercuryForegroundColorDefValue))
        self.planetMercuryForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMercuryBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMercuryBackgroundColorDefValue))
        self.planetMercuryBackgroundColorEditButton.\
            setColor(value)

        # Venus
        key = SettingsKeys.planetVenusGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetVenusGlyphUnicodeDefValue))
        self.planetVenusGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetVenusGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetVenusGlyphFontSizeDefValue))
        self.planetVenusGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetVenusAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetVenusAbbreviationDefValue))
        self.planetVenusAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetVenusForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetVenusForegroundColorDefValue))
        self.planetVenusForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetVenusBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetVenusBackgroundColorDefValue))
        self.planetVenusBackgroundColorEditButton.\
            setColor(value)

        # Earth
        key = SettingsKeys.planetEarthGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetEarthGlyphUnicodeDefValue))
        self.planetEarthGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetEarthGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetEarthGlyphFontSizeDefValue))
        self.planetEarthGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetEarthAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetEarthAbbreviationDefValue))
        self.planetEarthAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetEarthForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetEarthForegroundColorDefValue))
        self.planetEarthForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetEarthBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetEarthBackgroundColorDefValue))
        self.planetEarthBackgroundColorEditButton.\
            setColor(value)

        # Mars
        key = SettingsKeys.planetMarsGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMarsGlyphUnicodeDefValue))
        self.planetMarsGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMarsGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMarsGlyphFontSizeDefValue))
        self.planetMarsGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMarsAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMarsAbbreviationDefValue))
        self.planetMarsAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMarsForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMarsForegroundColorDefValue))
        self.planetMarsForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMarsBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMarsBackgroundColorDefValue))
        self.planetMarsBackgroundColorEditButton.\
            setColor(value)

        # Jupiter
        key = SettingsKeys.planetJupiterGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetJupiterGlyphUnicodeDefValue))
        self.planetJupiterGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetJupiterGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetJupiterGlyphFontSizeDefValue))
        self.planetJupiterGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetJupiterAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetJupiterAbbreviationDefValue))
        self.planetJupiterAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetJupiterForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetJupiterForegroundColorDefValue))
        self.planetJupiterForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetJupiterBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetJupiterBackgroundColorDefValue))
        self.planetJupiterBackgroundColorEditButton.\
            setColor(value)

        # Saturn
        key = SettingsKeys.planetSaturnGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetSaturnGlyphUnicodeDefValue))
        self.planetSaturnGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetSaturnGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetSaturnGlyphFontSizeDefValue))
        self.planetSaturnGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetSaturnAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetSaturnAbbreviationDefValue))
        self.planetSaturnAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetSaturnForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetSaturnForegroundColorDefValue))
        self.planetSaturnForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetSaturnBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetSaturnBackgroundColorDefValue))
        self.planetSaturnBackgroundColorEditButton.\
            setColor(value)

        # Uranus
        key = SettingsKeys.planetUranusGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetUranusGlyphUnicodeDefValue))
        self.planetUranusGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetUranusGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetUranusGlyphFontSizeDefValue))
        self.planetUranusGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetUranusAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetUranusAbbreviationDefValue))
        self.planetUranusAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetUranusForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetUranusForegroundColorDefValue))
        self.planetUranusForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetUranusBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetUranusBackgroundColorDefValue))
        self.planetUranusBackgroundColorEditButton.\
            setColor(value)

        # Neptune
        key = SettingsKeys.planetNeptuneGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetNeptuneGlyphUnicodeDefValue))
        self.planetNeptuneGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetNeptuneGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetNeptuneGlyphFontSizeDefValue))
        self.planetNeptuneGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetNeptuneAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetNeptuneAbbreviationDefValue))
        self.planetNeptuneAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetNeptuneForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetNeptuneForegroundColorDefValue))
        self.planetNeptuneForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetNeptuneBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetNeptuneBackgroundColorDefValue))
        self.planetNeptuneBackgroundColorEditButton.\
            setColor(value)

        # Pluto
        key = SettingsKeys.planetPlutoGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetPlutoGlyphUnicodeDefValue))
        self.planetPlutoGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetPlutoGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetPlutoGlyphFontSizeDefValue))
        self.planetPlutoGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetPlutoAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetPlutoAbbreviationDefValue))
        self.planetPlutoAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetPlutoForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetPlutoForegroundColorDefValue))
        self.planetPlutoForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetPlutoBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetPlutoBackgroundColorDefValue))
        self.planetPlutoBackgroundColorEditButton.\
            setColor(value)

        # MeanNorthNode
        key = SettingsKeys.planetMeanNorthNodeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanNorthNodeGlyphUnicodeDefValue))
        self.planetMeanNorthNodeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanNorthNodeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMeanNorthNodeGlyphFontSizeDefValue))
        self.planetMeanNorthNodeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanNorthNodeAbbreviationDefValue))
        self.planetMeanNorthNodeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanNorthNodeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanNorthNodeForegroundColorDefValue))
        self.planetMeanNorthNodeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMeanNorthNodeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanNorthNodeBackgroundColorDefValue))
        self.planetMeanNorthNodeBackgroundColorEditButton.\
            setColor(value)

        # MeanSouthNode
        key = SettingsKeys.planetMeanSouthNodeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanSouthNodeGlyphUnicodeDefValue))
        self.planetMeanSouthNodeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanSouthNodeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMeanSouthNodeGlyphFontSizeDefValue))
        self.planetMeanSouthNodeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMeanSouthNodeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanSouthNodeAbbreviationDefValue))
        self.planetMeanSouthNodeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanSouthNodeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanSouthNodeForegroundColorDefValue))
        self.planetMeanSouthNodeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMeanSouthNodeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanSouthNodeBackgroundColorDefValue))
        self.planetMeanSouthNodeBackgroundColorEditButton.\
            setColor(value)

        # TrueNorthNode
        key = SettingsKeys.planetTrueNorthNodeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetTrueNorthNodeGlyphUnicodeDefValue))
        self.planetTrueNorthNodeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetTrueNorthNodeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetTrueNorthNodeGlyphFontSizeDefValue))
        self.planetTrueNorthNodeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetTrueNorthNodeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetTrueNorthNodeAbbreviationDefValue))
        self.planetTrueNorthNodeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetTrueNorthNodeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetTrueNorthNodeForegroundColorDefValue))
        self.planetTrueNorthNodeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetTrueNorthNodeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetTrueNorthNodeBackgroundColorDefValue))
        self.planetTrueNorthNodeBackgroundColorEditButton.\
            setColor(value)

        # TrueSouthNode
        key = SettingsKeys.planetTrueSouthNodeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetTrueSouthNodeGlyphUnicodeDefValue))
        self.planetTrueSouthNodeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetTrueSouthNodeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetTrueSouthNodeGlyphFontSizeDefValue))
        self.planetTrueSouthNodeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetTrueSouthNodeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetTrueSouthNodeAbbreviationDefValue))
        self.planetTrueSouthNodeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetTrueSouthNodeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetTrueSouthNodeForegroundColorDefValue))
        self.planetTrueSouthNodeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetTrueSouthNodeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetTrueSouthNodeBackgroundColorDefValue))
        self.planetTrueSouthNodeBackgroundColorEditButton.\
            setColor(value)

        # Ceres
        key = SettingsKeys.planetCeresGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetCeresGlyphUnicodeDefValue))
        self.planetCeresGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetCeresGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetCeresGlyphFontSizeDefValue))
        self.planetCeresGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetCeresAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetCeresAbbreviationDefValue))
        self.planetCeresAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetCeresForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetCeresForegroundColorDefValue))
        self.planetCeresForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetCeresBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetCeresBackgroundColorDefValue))
        self.planetCeresBackgroundColorEditButton.\
            setColor(value)

        # Pallas
        key = SettingsKeys.planetPallasGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetPallasGlyphUnicodeDefValue))
        self.planetPallasGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetPallasGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetPallasGlyphFontSizeDefValue))
        self.planetPallasGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetPallasAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetPallasAbbreviationDefValue))
        self.planetPallasAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetPallasForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetPallasForegroundColorDefValue))
        self.planetPallasForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetPallasBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetPallasBackgroundColorDefValue))
        self.planetPallasBackgroundColorEditButton.\
            setColor(value)

        # Juno
        key = SettingsKeys.planetJunoGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetJunoGlyphUnicodeDefValue))
        self.planetJunoGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetJunoGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetJunoGlyphFontSizeDefValue))
        self.planetJunoGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetJunoAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetJunoAbbreviationDefValue))
        self.planetJunoAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetJunoForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetJunoForegroundColorDefValue))
        self.planetJunoForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetJunoBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetJunoBackgroundColorDefValue))
        self.planetJunoBackgroundColorEditButton.\
            setColor(value)

        # Vesta
        key = SettingsKeys.planetVestaGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetVestaGlyphUnicodeDefValue))
        self.planetVestaGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetVestaGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetVestaGlyphFontSizeDefValue))
        self.planetVestaGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetVestaAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetVestaAbbreviationDefValue))
        self.planetVestaAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetVestaForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetVestaForegroundColorDefValue))
        self.planetVestaForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetVestaBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetVestaBackgroundColorDefValue))
        self.planetVestaBackgroundColorEditButton.\
            setColor(value)

        # Chiron
        key = SettingsKeys.planetChironGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetChironGlyphUnicodeDefValue))
        self.planetChironGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetChironGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetChironGlyphFontSizeDefValue))
        self.planetChironGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetChironAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetChironAbbreviationDefValue))
        self.planetChironAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetChironForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetChironForegroundColorDefValue))
        self.planetChironForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetChironBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetChironBackgroundColorDefValue))
        self.planetChironBackgroundColorEditButton.\
            setColor(value)

        # Gulika
        key = SettingsKeys.planetGulikaGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetGulikaGlyphUnicodeDefValue))
        self.planetGulikaGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetGulikaGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetGulikaGlyphFontSizeDefValue))
        self.planetGulikaGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetGulikaAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetGulikaAbbreviationDefValue))
        self.planetGulikaAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetGulikaForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetGulikaForegroundColorDefValue))
        self.planetGulikaForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetGulikaBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetGulikaBackgroundColorDefValue))
        self.planetGulikaBackgroundColorEditButton.\
            setColor(value)

        # Mandi
        key = SettingsKeys.planetMandiGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMandiGlyphUnicodeDefValue))
        self.planetMandiGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMandiGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMandiGlyphFontSizeDefValue))
        self.planetMandiGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMandiAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMandiAbbreviationDefValue))
        self.planetMandiAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMandiForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMandiForegroundColorDefValue))
        self.planetMandiForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMandiBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMandiBackgroundColorDefValue))
        self.planetMandiBackgroundColorEditButton.\
            setColor(value)

        # MeanOfFive
        key = SettingsKeys.planetMeanOfFiveGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanOfFiveGlyphUnicodeDefValue))
        self.planetMeanOfFiveGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanOfFiveGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMeanOfFiveGlyphFontSizeDefValue))
        self.planetMeanOfFiveGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMeanOfFiveAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanOfFiveAbbreviationDefValue))
        self.planetMeanOfFiveAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanOfFiveForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanOfFiveForegroundColorDefValue))
        self.planetMeanOfFiveForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMeanOfFiveBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanOfFiveBackgroundColorDefValue))
        self.planetMeanOfFiveBackgroundColorEditButton.\
            setColor(value)

        # CycleOfEight
        key = SettingsKeys.planetCycleOfEightGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetCycleOfEightGlyphUnicodeDefValue))
        self.planetCycleOfEightGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetCycleOfEightGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetCycleOfEightGlyphFontSizeDefValue))
        self.planetCycleOfEightGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetCycleOfEightAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetCycleOfEightAbbreviationDefValue))
        self.planetCycleOfEightAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetCycleOfEightForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetCycleOfEightForegroundColorDefValue))
        self.planetCycleOfEightForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetCycleOfEightBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetCycleOfEightBackgroundColorDefValue))
        self.planetCycleOfEightBackgroundColorEditButton.\
            setColor(value)


    def _nonPlanetSymbolLoadValuesFromSettings(self):
        """Loads the widgets with values from the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()

        # Retrograde
        key = SettingsKeys.planetRetrogradeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetRetrogradeGlyphUnicodeDefValue))
        self.planetRetrogradeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetRetrogradeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetRetrogradeGlyphFontSizeDefValue))
        self.planetRetrogradeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetRetrogradeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetRetrogradeAbbreviationDefValue))
        self.planetRetrogradeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetRetrogradeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetRetrogradeForegroundColorDefValue))
        self.planetRetrogradeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetRetrogradeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetRetrogradeBackgroundColorDefValue))
        self.planetRetrogradeBackgroundColorEditButton.\
            setColor(value)

        # Ascendant
        key = SettingsKeys.planetAscendantGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetAscendantGlyphUnicodeDefValue))
        self.planetAscendantGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetAscendantGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetAscendantGlyphFontSizeDefValue))
        self.planetAscendantGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetAscendantAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetAscendantAbbreviationDefValue))
        self.planetAscendantAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetAscendantForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetAscendantForegroundColorDefValue))
        self.planetAscendantForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetAscendantBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetAscendantBackgroundColorDefValue))
        self.planetAscendantBackgroundColorEditButton.\
            setColor(value)

        # Midheaven
        key = SettingsKeys.planetMidheavenGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMidheavenGlyphUnicodeDefValue))
        self.planetMidheavenGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMidheavenGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMidheavenGlyphFontSizeDefValue))
        self.planetMidheavenGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMidheavenAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMidheavenAbbreviationDefValue))
        self.planetMidheavenAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMidheavenForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMidheavenForegroundColorDefValue))
        self.planetMidheavenForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMidheavenBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMidheavenBackgroundColorDefValue))
        self.planetMidheavenBackgroundColorEditButton.\
            setColor(value)

        # HoraLagna
        key = SettingsKeys.planetHoraLagnaGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetHoraLagnaGlyphUnicodeDefValue))
        self.planetHoraLagnaGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetHoraLagnaGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetHoraLagnaGlyphFontSizeDefValue))
        self.planetHoraLagnaGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetHoraLagnaAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetHoraLagnaAbbreviationDefValue))
        self.planetHoraLagnaAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetHoraLagnaForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetHoraLagnaForegroundColorDefValue))
        self.planetHoraLagnaForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetHoraLagnaBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetHoraLagnaBackgroundColorDefValue))
        self.planetHoraLagnaBackgroundColorEditButton.\
            setColor(value)

        # GhatiLagna
        key = SettingsKeys.planetGhatiLagnaGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetGhatiLagnaGlyphUnicodeDefValue))
        self.planetGhatiLagnaGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetGhatiLagnaGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetGhatiLagnaGlyphFontSizeDefValue))
        self.planetGhatiLagnaGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetGhatiLagnaAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetGhatiLagnaAbbreviationDefValue))
        self.planetGhatiLagnaAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetGhatiLagnaForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetGhatiLagnaForegroundColorDefValue))
        self.planetGhatiLagnaForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetGhatiLagnaBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetGhatiLagnaBackgroundColorDefValue))
        self.planetGhatiLagnaBackgroundColorEditButton.\
            setColor(value)

        # MeanLunarApogee
        key = SettingsKeys.planetMeanLunarApogeeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanLunarApogeeGlyphUnicodeDefValue))
        self.planetMeanLunarApogeeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanLunarApogeeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetMeanLunarApogeeGlyphFontSizeDefValue))
        self.planetMeanLunarApogeeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetMeanLunarApogeeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetMeanLunarApogeeAbbreviationDefValue))
        self.planetMeanLunarApogeeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetMeanLunarApogeeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanLunarApogeeForegroundColorDefValue))
        self.planetMeanLunarApogeeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetMeanLunarApogeeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetMeanLunarApogeeBackgroundColorDefValue))
        self.planetMeanLunarApogeeBackgroundColorEditButton.\
            setColor(value)

        # OsculatingLunarApogee
        key = SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeDefValue))
        self.planetOsculatingLunarApogeeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeDefValue))
        self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetOsculatingLunarApogeeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetOsculatingLunarApogeeAbbreviationDefValue))
        self.planetOsculatingLunarApogeeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetOsculatingLunarApogeeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetOsculatingLunarApogeeForegroundColorDefValue))
        self.planetOsculatingLunarApogeeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetOsculatingLunarApogeeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetOsculatingLunarApogeeBackgroundColorDefValue))
        self.planetOsculatingLunarApogeeBackgroundColorEditButton.\
            setColor(value)

        # InterpolatedLunarApogee
        key = SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeDefValue))
        self.planetInterpolatedLunarApogeeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeDefValue))
        self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetInterpolatedLunarApogeeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarApogeeAbbreviationDefValue))
        self.planetInterpolatedLunarApogeeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetInterpolatedLunarApogeeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarApogeeForegroundColorDefValue))
        self.planetInterpolatedLunarApogeeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorDefValue))
        self.planetInterpolatedLunarApogeeBackgroundColorEditButton.\
            setColor(value)

        # InterpolatedLunarPerigee
        key = SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeDefValue))
        self.planetInterpolatedLunarPerigeeGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeDefValue))
        self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationDefValue))
        self.planetInterpolatedLunarPerigeeAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorDefValue))
        self.planetInterpolatedLunarPerigeeForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorDefValue))
        self.planetInterpolatedLunarPerigeeBackgroundColorEditButton.\
            setColor(value)


    def _signSymbolLoadValuesFromSettings(self):
        """Loads the widgets with values from the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously.
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()

        # Aries
        key = SettingsKeys.signAriesGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signAriesGlyphUnicodeDefValue))
        self.planetAriesGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signAriesGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signAriesGlyphFontSizeDefValue))
        self.planetAriesGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signAriesAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signAriesAbbreviationDefValue))
        self.planetAriesAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signAriesForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signAriesForegroundColorDefValue))
        self.planetAriesForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signAriesBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signAriesBackgroundColorDefValue))
        self.planetAriesBackgroundColorEditButton.\
            setColor(value)

        # Taurus
        key = SettingsKeys.signTaurusGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signTaurusGlyphUnicodeDefValue))
        self.planetTaurusGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signTaurusGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signTaurusGlyphFontSizeDefValue))
        self.planetTaurusGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signTaurusAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signTaurusAbbreviationDefValue))
        self.planetTaurusAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signTaurusForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signTaurusForegroundColorDefValue))
        self.planetTaurusForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signTaurusBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signTaurusBackgroundColorDefValue))
        self.planetTaurusBackgroundColorEditButton.\
            setColor(value)

        # Gemini
        key = SettingsKeys.signGeminiGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signGeminiGlyphUnicodeDefValue))
        self.planetGeminiGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signGeminiGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signGeminiGlyphFontSizeDefValue))
        self.planetGeminiGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signGeminiAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signGeminiAbbreviationDefValue))
        self.planetGeminiAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signGeminiForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signGeminiForegroundColorDefValue))
        self.planetGeminiForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signGeminiBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signGeminiBackgroundColorDefValue))
        self.planetGeminiBackgroundColorEditButton.\
            setColor(value)

        # Cancer
        key = SettingsKeys.signCancerGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signCancerGlyphUnicodeDefValue))
        self.planetCancerGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signCancerGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signCancerGlyphFontSizeDefValue))
        self.planetCancerGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signCancerAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signCancerAbbreviationDefValue))
        self.planetCancerAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signCancerForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signCancerForegroundColorDefValue))
        self.planetCancerForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signCancerBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signCancerBackgroundColorDefValue))
        self.planetCancerBackgroundColorEditButton.\
            setColor(value)

        # Leo
        key = SettingsKeys.signLeoGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signLeoGlyphUnicodeDefValue))
        self.planetLeoGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signLeoGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signLeoGlyphFontSizeDefValue))
        self.planetLeoGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signLeoAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signLeoAbbreviationDefValue))
        self.planetLeoAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signLeoForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signLeoForegroundColorDefValue))
        self.planetLeoForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signLeoBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signLeoBackgroundColorDefValue))
        self.planetLeoBackgroundColorEditButton.\
            setColor(value)

        # Virgo
        key = SettingsKeys.signVirgoGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signVirgoGlyphUnicodeDefValue))
        self.planetVirgoGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signVirgoGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signVirgoGlyphFontSizeDefValue))
        self.planetVirgoGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signVirgoAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signVirgoAbbreviationDefValue))
        self.planetVirgoAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signVirgoForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signVirgoForegroundColorDefValue))
        self.planetVirgoForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signVirgoBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signVirgoBackgroundColorDefValue))
        self.planetVirgoBackgroundColorEditButton.\
            setColor(value)

        # Libra
        key = SettingsKeys.signLibraGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signLibraGlyphUnicodeDefValue))
        self.planetLibraGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signLibraGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signLibraGlyphFontSizeDefValue))
        self.planetLibraGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signLibraAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signLibraAbbreviationDefValue))
        self.planetLibraAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signLibraForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signLibraForegroundColorDefValue))
        self.planetLibraForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signLibraBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signLibraBackgroundColorDefValue))
        self.planetLibraBackgroundColorEditButton.\
            setColor(value)

        # Scorpio
        key = SettingsKeys.signScorpioGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signScorpioGlyphUnicodeDefValue))
        self.planetScorpioGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signScorpioGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signScorpioGlyphFontSizeDefValue))
        self.planetScorpioGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signScorpioAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signScorpioAbbreviationDefValue))
        self.planetScorpioAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signScorpioForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signScorpioForegroundColorDefValue))
        self.planetScorpioForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signScorpioBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signScorpioBackgroundColorDefValue))
        self.planetScorpioBackgroundColorEditButton.\
            setColor(value)

        # Sagittarius
        key = SettingsKeys.signSagittariusGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signSagittariusGlyphUnicodeDefValue))
        self.planetSagittariusGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signSagittariusGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signSagittariusGlyphFontSizeDefValue))
        self.planetSagittariusGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signSagittariusAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signSagittariusAbbreviationDefValue))
        self.planetSagittariusAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signSagittariusForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signSagittariusForegroundColorDefValue))
        self.planetSagittariusForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signSagittariusBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signSagittariusBackgroundColorDefValue))
        self.planetSagittariusBackgroundColorEditButton.\
            setColor(value)

        # Capricorn
        key = SettingsKeys.signCapricornGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signCapricornGlyphUnicodeDefValue))
        self.planetCapricornGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signCapricornGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signCapricornGlyphFontSizeDefValue))
        self.planetCapricornGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signCapricornAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signCapricornAbbreviationDefValue))
        self.planetCapricornAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signCapricornForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signCapricornForegroundColorDefValue))
        self.planetCapricornForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signCapricornBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signCapricornBackgroundColorDefValue))
        self.planetCapricornBackgroundColorEditButton.\
            setColor(value)

        # Aquarius
        key = SettingsKeys.signAquariusGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signAquariusGlyphUnicodeDefValue))
        self.planetAquariusGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signAquariusGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signAquariusGlyphFontSizeDefValue))
        self.planetAquariusGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signAquariusAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signAquariusAbbreviationDefValue))
        self.planetAquariusAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signAquariusForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signAquariusForegroundColorDefValue))
        self.planetAquariusForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signAquariusBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signAquariusBackgroundColorDefValue))
        self.planetAquariusBackgroundColorEditButton.\
            setColor(value)

        # Pisces
        key = SettingsKeys.signPiscesGlyphUnicodeKey
        value = str(settings.value(key, \
            SettingsKeys.signPiscesGlyphUnicodeDefValue))
        self.planetPiscesGlyphUnicodeLineEdit.\
            setText(value)

        key = SettingsKeys.signPiscesGlyphFontSizeKey
        value = float(settings.value(key, \
            SettingsKeys.signPiscesGlyphFontSizeDefValue))
        self.planetPiscesGlyphFontSizeSpinBox.\
            setValue(value)

        key = SettingsKeys.signPiscesAbbreviationKey
        value = str(settings.value(key, \
            SettingsKeys.signPiscesAbbreviationDefValue))
        self.planetPiscesAbbreviationLineEdit.\
            setText(value)

        key = SettingsKeys.signPiscesForegroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signPiscesForegroundColorDefValue))
        self.planetPiscesForegroundColorEditButton.\
            setColor(value)

        key = SettingsKeys.signPiscesBackgroundColorKey
        value = QColor(settings.value(key, \
            SettingsKeys.signPiscesBackgroundColorDefValue))
        self.planetPiscesBackgroundColorEditButton.\
            setColor(value)



    def _priceBarSaveValuesToSettings(self):
        """Saves the values in the widgets to the QSettings object.
        This does it for the PriceBarChart settings.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()
    
        # PriceBarChart zoom-in/out scale factor (float).
        key = SettingsKeys.zoomScaleFactorSettingsKey 
        newValue = self.zoomScaleFactorSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # PriceBarChart higherPriceBarColor (QColor).
        key = SettingsKeys.higherPriceBarColorSettingsKey 
        newValue = self.higherPriceBarColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # PriceBarChart lowerPriceBarColor (QColor).
        key = SettingsKeys.lowerPriceBarColorSettingsKey 
        newValue = self.lowerPriceBarColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # PriceBarChart barCountGraphicsItemTextColor (QColor).
        key = SettingsKeys.barCountGraphicsItemColorSettingsKey
        newValue = self.barCountGraphicsItemColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # PriceBarChart barCountGraphicsItemTextTextColor (QColor).
        key = SettingsKeys.barCountGraphicsItemTextColorSettingsKey
        newValue = self.barCountGraphicsItemTextColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)


    def _planetSymbolSaveValuesToSettings(self):
        """Saves the values in the widgets to the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()
    
        # Sun
        key = SettingsKeys.planetSunGlyphUnicodeKey
        newValue = \
            self.planetSunGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSunGlyphFontSizeKey
        newValue = \
            self.planetSunGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSunAbbreviationKey
        newValue = \
            self.planetSunAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSunForegroundColorKey
        newValue = \
            self.planetSunForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSunBackgroundColorKey
        newValue = \
            self.planetSunBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Moon
        key = SettingsKeys.planetMoonGlyphUnicodeKey
        newValue = \
            self.planetMoonGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMoonGlyphFontSizeKey
        newValue = \
            self.planetMoonGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMoonAbbreviationKey
        newValue = \
            self.planetMoonAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMoonForegroundColorKey
        newValue = \
            self.planetMoonForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMoonBackgroundColorKey
        newValue = \
            self.planetMoonBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Mercury
        key = SettingsKeys.planetMercuryGlyphUnicodeKey
        newValue = \
            self.planetMercuryGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)
            
        key = SettingsKeys.planetMercuryGlyphFontSizeKey
        newValue = \
            self.planetMercuryGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)
        
        key = SettingsKeys.planetMercuryAbbreviationKey
        newValue = \
            self.planetMercuryAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMercuryForegroundColorKey
        newValue = \
            self.planetMercuryForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMercuryBackgroundColorKey
        newValue = \
            self.planetMercuryBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Venus
        key = SettingsKeys.planetVenusGlyphUnicodeKey
        newValue = \
            self.planetVenusGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)
            
        key = SettingsKeys.planetVenusGlyphFontSizeKey
        newValue = \
            self.planetVenusGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)
        
        key = SettingsKeys.planetVenusAbbreviationKey
        newValue = \
                    self.planetVenusAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVenusForegroundColorKey
        newValue = \
            self.planetVenusForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVenusBackgroundColorKey
        newValue = \
            self.planetVenusBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Earth
        key = SettingsKeys.planetEarthGlyphUnicodeKey
        newValue = \
            self.planetEarthGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetEarthGlyphFontSizeKey
        newValue = \
            self.planetEarthGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetEarthAbbreviationKey
        newValue = \
            self.planetEarthAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetEarthForegroundColorKey
        newValue = \
            self.planetEarthForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetEarthBackgroundColorKey
        newValue = \
            self.planetEarthBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Mars
        key = SettingsKeys.planetMarsGlyphUnicodeKey
        newValue = \
            self.planetMarsGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMarsGlyphFontSizeKey
        newValue = \
            self.planetMarsGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMarsAbbreviationKey
        newValue = \
            self.planetMarsAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMarsForegroundColorKey
        newValue = \
            self.planetMarsForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMarsBackgroundColorKey
        newValue = \
            self.planetMarsBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Jupiter
        key = SettingsKeys.planetJupiterGlyphUnicodeKey
        newValue = \
            self.planetJupiterGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJupiterGlyphFontSizeKey
        newValue = \
            self.planetJupiterGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJupiterAbbreviationKey
        newValue = \
            self.planetJupiterAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJupiterForegroundColorKey
        newValue = \
            self.planetJupiterForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJupiterBackgroundColorKey
        newValue = \
            self.planetJupiterBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Saturn
        key = SettingsKeys.planetSaturnGlyphUnicodeKey
        newValue = \
            self.planetSaturnGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSaturnGlyphFontSizeKey
        newValue = \
            self.planetSaturnGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSaturnAbbreviationKey
        newValue = \
            self.planetSaturnAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSaturnForegroundColorKey
        newValue = \
            self.planetSaturnForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetSaturnBackgroundColorKey
        newValue = \
            self.planetSaturnBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Uranus
        key = SettingsKeys.planetUranusGlyphUnicodeKey
        newValue = \
            self.planetUranusGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetUranusGlyphFontSizeKey
        newValue = \
            self.planetUranusGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetUranusAbbreviationKey
        newValue = \
            self.planetUranusAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetUranusForegroundColorKey
        newValue = \
            self.planetUranusForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetUranusBackgroundColorKey
        newValue = \
            self.planetUranusBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Neptune
        key = SettingsKeys.planetNeptuneGlyphUnicodeKey
        newValue = \
            self.planetNeptuneGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetNeptuneGlyphFontSizeKey
        newValue = \
            self.planetNeptuneGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetNeptuneAbbreviationKey
        newValue = \
            self.planetNeptuneAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetNeptuneForegroundColorKey
        newValue = \
            self.planetNeptuneForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetNeptuneBackgroundColorKey
        newValue = \
            self.planetNeptuneBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Pluto
        key = SettingsKeys.planetPlutoGlyphUnicodeKey
        newValue = \
            self.planetPlutoGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPlutoGlyphFontSizeKey
        newValue = \
            self.planetPlutoGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPlutoAbbreviationKey
        newValue = \
            self.planetPlutoAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPlutoForegroundColorKey
        newValue = \
            self.planetPlutoForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPlutoBackgroundColorKey
        newValue = \
            self.planetPlutoBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # MeanNorthNode
        key = SettingsKeys.planetMeanNorthNodeGlyphUnicodeKey
        newValue = \
            self.planetMeanNorthNodeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanNorthNodeGlyphFontSizeKey
        newValue = \
            self.planetMeanNorthNodeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        newValue = \
            self.planetMeanNorthNodeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanNorthNodeForegroundColorKey
        newValue = \
            self.planetMeanNorthNodeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanNorthNodeBackgroundColorKey
        newValue = \
            self.planetMeanNorthNodeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # MeanSouthNode
        key = SettingsKeys.planetMeanSouthNodeGlyphUnicodeKey
        newValue = \
            self.planetMeanSouthNodeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanSouthNodeGlyphFontSizeKey
        newValue = \
            self.planetMeanSouthNodeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanSouthNodeAbbreviationKey
        newValue = \
            self.planetMeanSouthNodeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanSouthNodeForegroundColorKey
        newValue = \
            self.planetMeanSouthNodeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanSouthNodeBackgroundColorKey
        newValue = \
            self.planetMeanSouthNodeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # TrueNorthNode
        key = SettingsKeys.planetTrueNorthNodeGlyphUnicodeKey
        newValue = \
            self.planetTrueNorthNodeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueNorthNodeGlyphFontSizeKey
        newValue = \
            self.planetTrueNorthNodeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueNorthNodeAbbreviationKey
        newValue = \
            self.planetTrueNorthNodeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueNorthNodeForegroundColorKey
        newValue = \
            self.planetTrueNorthNodeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueNorthNodeBackgroundColorKey
        newValue = \
            self.planetTrueNorthNodeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # TrueSouthNode
        key = SettingsKeys.planetTrueSouthNodeGlyphUnicodeKey
        newValue = \
            self.planetTrueSouthNodeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueSouthNodeGlyphFontSizeKey
        newValue = \
            self.planetTrueSouthNodeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueSouthNodeAbbreviationKey
        newValue = \
            self.planetTrueSouthNodeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueSouthNodeForegroundColorKey
        newValue = \
            self.planetTrueSouthNodeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetTrueSouthNodeBackgroundColorKey
        newValue = \
            self.planetTrueSouthNodeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Ceres
        key = SettingsKeys.planetCeresGlyphUnicodeKey
        newValue = \
            self.planetCeresGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCeresGlyphFontSizeKey
        newValue = \
            self.planetCeresGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCeresAbbreviationKey
        newValue = \
            self.planetCeresAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCeresForegroundColorKey
        newValue = \
            self.planetCeresForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCeresBackgroundColorKey
        newValue = \
            self.planetCeresBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Pallas
        key = SettingsKeys.planetPallasGlyphUnicodeKey
        newValue = \
            self.planetPallasGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPallasGlyphFontSizeKey
        newValue = \
            self.planetPallasGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPallasAbbreviationKey
        newValue = \
            self.planetPallasAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPallasForegroundColorKey
        newValue = \
            self.planetPallasForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetPallasBackgroundColorKey
        newValue = \
            self.planetPallasBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Juno
        key = SettingsKeys.planetJunoGlyphUnicodeKey
        newValue = \
            self.planetJunoGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJunoGlyphFontSizeKey
        newValue = \
            self.planetJunoGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJunoAbbreviationKey
        newValue = \
            self.planetJunoAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJunoForegroundColorKey
        newValue = \
            self.planetJunoForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetJunoBackgroundColorKey
        newValue = \
            self.planetJunoBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Vesta
        key = SettingsKeys.planetVestaGlyphUnicodeKey
        newValue = \
            self.planetVestaGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVestaGlyphFontSizeKey
        newValue = \
            self.planetVestaGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVestaAbbreviationKey
        newValue = \
            self.planetVestaAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVestaForegroundColorKey
        newValue = \
            self.planetVestaForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetVestaBackgroundColorKey
        newValue = \
            self.planetVestaBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Chiron
        key = SettingsKeys.planetChironGlyphUnicodeKey
        newValue = \
            self.planetChironGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetChironGlyphFontSizeKey
        newValue = \
            self.planetChironGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetChironAbbreviationKey
        newValue = \
            self.planetChironAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetChironForegroundColorKey
        newValue = \
            self.planetChironForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetChironBackgroundColorKey
        newValue = \
            self.planetChironBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Gulika
        key = SettingsKeys.planetGulikaGlyphUnicodeKey
        newValue = \
            self.planetGulikaGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGulikaGlyphFontSizeKey
        newValue = \
            self.planetGulikaGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGulikaAbbreviationKey
        newValue = \
            self.planetGulikaAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGulikaForegroundColorKey
        newValue = \
            self.planetGulikaForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGulikaBackgroundColorKey
        newValue = \
            self.planetGulikaBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Mandi
        key = SettingsKeys.planetMandiGlyphUnicodeKey
        newValue = \
            self.planetMandiGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMandiGlyphFontSizeKey
        newValue = \
            self.planetMandiGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMandiAbbreviationKey
        newValue = \
            self.planetMandiAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMandiForegroundColorKey
        newValue = \
            self.planetMandiForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMandiBackgroundColorKey
        newValue = \
            self.planetMandiBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # MeanOfFive
        key = SettingsKeys.planetMeanOfFiveGlyphUnicodeKey
        newValue = \
            self.planetMeanOfFiveGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanOfFiveGlyphFontSizeKey
        newValue = \
            self.planetMeanOfFiveGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanOfFiveAbbreviationKey
        newValue = \
            self.planetMeanOfFiveAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanOfFiveForegroundColorKey
        newValue = \
            self.planetMeanOfFiveForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanOfFiveBackgroundColorKey
        newValue = \
            self.planetMeanOfFiveBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # CycleOfEight
        key = SettingsKeys.planetCycleOfEightGlyphUnicodeKey
        newValue = \
            self.planetCycleOfEightGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCycleOfEightGlyphFontSizeKey
        newValue = \
            self.planetCycleOfEightGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCycleOfEightAbbreviationKey
        newValue = \
            self.planetCycleOfEightAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCycleOfEightForegroundColorKey
        newValue = \
            self.planetCycleOfEightForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetCycleOfEightBackgroundColorKey
        newValue = \
            self.planetCycleOfEightBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)


    def _nonPlanetSymbolSaveValuesToSettings(self):
        """Saves the values in the widgets to the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()
    
        # Retrograde
        key = SettingsKeys.planetRetrogradeGlyphUnicodeKey
        newValue = \
            self.planetRetrogradeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetRetrogradeGlyphFontSizeKey
        newValue = \
            self.planetRetrogradeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetRetrogradeAbbreviationKey
        newValue = \
            self.planetRetrogradeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetRetrogradeForegroundColorKey
        newValue = \
            self.planetRetrogradeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetRetrogradeBackgroundColorKey
        newValue = \
            self.planetRetrogradeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Ascendant
        key = SettingsKeys.planetAscendantGlyphUnicodeKey
        newValue = \
            self.planetAscendantGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetAscendantGlyphFontSizeKey
        newValue = \
            self.planetAscendantGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetAscendantAbbreviationKey
        newValue = \
            self.planetAscendantAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetAscendantForegroundColorKey
        newValue = \
            self.planetAscendantForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetAscendantBackgroundColorKey
        newValue = \
            self.planetAscendantBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Midheaven
        key = SettingsKeys.planetMidheavenGlyphUnicodeKey
        newValue = \
            self.planetMidheavenGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMidheavenGlyphFontSizeKey
        newValue = \
            self.planetMidheavenGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMidheavenAbbreviationKey
        newValue = \
            self.planetMidheavenAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMidheavenForegroundColorKey
        newValue = \
            self.planetMidheavenForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMidheavenBackgroundColorKey
        newValue = \
            self.planetMidheavenBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # HoraLagna
        key = SettingsKeys.planetHoraLagnaGlyphUnicodeKey
        newValue = \
            self.planetHoraLagnaGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetHoraLagnaGlyphFontSizeKey
        newValue = \
            self.planetHoraLagnaGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetHoraLagnaAbbreviationKey
        newValue = \
            self.planetHoraLagnaAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetHoraLagnaForegroundColorKey
        newValue = \
            self.planetHoraLagnaForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetHoraLagnaBackgroundColorKey
        newValue = \
            self.planetHoraLagnaBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # GhatiLagna
        key = SettingsKeys.planetGhatiLagnaGlyphUnicodeKey
        newValue = \
            self.planetGhatiLagnaGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGhatiLagnaGlyphFontSizeKey
        newValue = \
            self.planetGhatiLagnaGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGhatiLagnaAbbreviationKey
        newValue = \
            self.planetGhatiLagnaAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGhatiLagnaForegroundColorKey
        newValue = \
            self.planetGhatiLagnaForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetGhatiLagnaBackgroundColorKey
        newValue = \
            self.planetGhatiLagnaBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # MeanLunarApogee
        key = SettingsKeys.planetMeanLunarApogeeGlyphUnicodeKey
        newValue = \
            self.planetMeanLunarApogeeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanLunarApogeeGlyphFontSizeKey
        newValue = \
            self.planetMeanLunarApogeeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanLunarApogeeAbbreviationKey
        newValue = \
            self.planetMeanLunarApogeeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanLunarApogeeForegroundColorKey
        newValue = \
            self.planetMeanLunarApogeeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetMeanLunarApogeeBackgroundColorKey
        newValue = \
            self.planetMeanLunarApogeeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # OsculatingLunarApogee
        key = SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeKey
        newValue = \
            self.planetOsculatingLunarApogeeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeKey
        newValue = \
            self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetOsculatingLunarApogeeAbbreviationKey
        newValue = \
            self.planetOsculatingLunarApogeeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetOsculatingLunarApogeeForegroundColorKey
        newValue = \
            self.planetOsculatingLunarApogeeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetOsculatingLunarApogeeBackgroundColorKey
        newValue = \
            self.planetOsculatingLunarApogeeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # InterpolatedLunarApogee
        key = SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeKey
        newValue = \
            self.planetInterpolatedLunarApogeeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeKey
        newValue = \
            self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarApogeeAbbreviationKey
        newValue = \
            self.planetInterpolatedLunarApogeeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarApogeeForegroundColorKey
        newValue = \
            self.planetInterpolatedLunarApogeeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorKey
        newValue = \
            self.planetInterpolatedLunarApogeeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # InterpolatedLunarPerigee
        key = SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeKey
        newValue = \
            self.planetInterpolatedLunarPerigeeGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeKey
        newValue = \
            self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationKey
        newValue = \
            self.planetInterpolatedLunarPerigeeAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorKey
        newValue = \
            self.planetInterpolatedLunarPerigeeForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorKey
        newValue = \
            self.planetInterpolatedLunarPerigeeBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)


    def _signSymbolSaveValuesToSettings(self):
        """Saves the values in the widgets to the QSettings object.

        This method uses QSettings and assumes that the
        calls to QCoreApplication.setOrganizationName(), and
        QCoreApplication.setApplicationName() have been called previously
        This is so that the QSettings constructor can be called without 
        any parameters specified.
        """

        settings = QSettings()
    
        # Aries
        key = SettingsKeys.signAriesGlyphUnicodeKey
        newValue = \
            self.planetAriesGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAriesGlyphFontSizeKey
        newValue = \
            self.planetAriesGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAriesAbbreviationKey
        newValue = \
            self.planetAriesAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAriesForegroundColorKey
        newValue = \
            self.planetAriesForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAriesBackgroundColorKey
        newValue = \
            self.planetAriesBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Taurus
        key = SettingsKeys.signTaurusGlyphUnicodeKey
        newValue = \
            self.planetTaurusGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signTaurusGlyphFontSizeKey
        newValue = \
            self.planetTaurusGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signTaurusAbbreviationKey
        newValue = \
            self.planetTaurusAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signTaurusForegroundColorKey
        newValue = \
            self.planetTaurusForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signTaurusBackgroundColorKey
        newValue = \
            self.planetTaurusBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Gemini
        key = SettingsKeys.signGeminiGlyphUnicodeKey
        newValue = \
            self.planetGeminiGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signGeminiGlyphFontSizeKey
        newValue = \
            self.planetGeminiGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signGeminiAbbreviationKey
        newValue = \
            self.planetGeminiAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signGeminiForegroundColorKey
        newValue = \
            self.planetGeminiForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signGeminiBackgroundColorKey
        newValue = \
            self.planetGeminiBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Cancer
        key = SettingsKeys.signCancerGlyphUnicodeKey
        newValue = \
            self.planetCancerGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCancerGlyphFontSizeKey
        newValue = \
            self.planetCancerGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCancerAbbreviationKey
        newValue = \
            self.planetCancerAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCancerForegroundColorKey
        newValue = \
            self.planetCancerForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCancerBackgroundColorKey
        newValue = \
            self.planetCancerBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Leo
        key = SettingsKeys.signLeoGlyphUnicodeKey
        newValue = \
            self.planetLeoGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLeoGlyphFontSizeKey
        newValue = \
            self.planetLeoGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLeoAbbreviationKey
        newValue = \
            self.planetLeoAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLeoForegroundColorKey
        newValue = \
            self.planetLeoForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLeoBackgroundColorKey
        newValue = \
            self.planetLeoBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Virgo
        key = SettingsKeys.signVirgoGlyphUnicodeKey
        newValue = \
            self.planetVirgoGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signVirgoGlyphFontSizeKey
        newValue = \
            self.planetVirgoGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signVirgoAbbreviationKey
        newValue = \
            self.planetVirgoAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signVirgoForegroundColorKey
        newValue = \
            self.planetVirgoForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signVirgoBackgroundColorKey
        newValue = \
            self.planetVirgoBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Libra
        key = SettingsKeys.signLibraGlyphUnicodeKey
        newValue = \
            self.planetLibraGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLibraGlyphFontSizeKey
        newValue = \
            self.planetLibraGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLibraAbbreviationKey
        newValue = \
            self.planetLibraAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLibraForegroundColorKey
        newValue = \
            self.planetLibraForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signLibraBackgroundColorKey
        newValue = \
            self.planetLibraBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Scorpio
        key = SettingsKeys.signScorpioGlyphUnicodeKey
        newValue = \
            self.planetScorpioGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signScorpioGlyphFontSizeKey
        newValue = \
            self.planetScorpioGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signScorpioAbbreviationKey
        newValue = \
            self.planetScorpioAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signScorpioForegroundColorKey
        newValue = \
            self.planetScorpioForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signScorpioBackgroundColorKey
        newValue = \
            self.planetScorpioBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Sagittarius
        key = SettingsKeys.signSagittariusGlyphUnicodeKey
        newValue = \
            self.planetSagittariusGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signSagittariusGlyphFontSizeKey
        newValue = \
            self.planetSagittariusGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signSagittariusAbbreviationKey
        newValue = \
            self.planetSagittariusAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signSagittariusForegroundColorKey
        newValue = \
            self.planetSagittariusForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signSagittariusBackgroundColorKey
        newValue = \
            self.planetSagittariusBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Capricorn
        key = SettingsKeys.signCapricornGlyphUnicodeKey
        newValue = \
            self.planetCapricornGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCapricornGlyphFontSizeKey
        newValue = \
            self.planetCapricornGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCapricornAbbreviationKey
        newValue = \
            self.planetCapricornAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCapricornForegroundColorKey
        newValue = \
            self.planetCapricornForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signCapricornBackgroundColorKey
        newValue = \
            self.planetCapricornBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Aquarius
        key = SettingsKeys.signAquariusGlyphUnicodeKey
        newValue = \
            self.planetAquariusGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAquariusGlyphFontSizeKey
        newValue = \
            self.planetAquariusGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAquariusAbbreviationKey
        newValue = \
            self.planetAquariusAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAquariusForegroundColorKey
        newValue = \
            self.planetAquariusForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signAquariusBackgroundColorKey
        newValue = \
            self.planetAquariusBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        # Pisces
        key = SettingsKeys.signPiscesGlyphUnicodeKey
        newValue = \
            self.planetPiscesGlyphUnicodeLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signPiscesGlyphFontSizeKey
        newValue = \
            self.planetPiscesGlyphFontSizeSpinBox.value()
        if settings.contains(key):
            oldValue = float(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signPiscesAbbreviationKey
        newValue = \
            self.planetPiscesAbbreviationLineEdit.text()
        if settings.contains(key):
            oldValue = str(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signPiscesForegroundColorKey
        newValue = \
            self.planetPiscesForegroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)

        key = SettingsKeys.signPiscesBackgroundColorKey
        newValue = \
            self.planetPiscesBackgroundColorEditButton.getColor()
        if settings.contains(key):
            oldValue = QColor(settings.value(key))
            if oldValue != newValue:
                settings.setValue(key, newValue)
        else:
            settings.setValue(key, newValue)


    def _handleZoomScaleFactorResetButtonClicked(self):
        """Called when the zoomScaleFactorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = SettingsKeys.zoomScaleFactorSettingsDefValue
        self.zoomScaleFactorSpinBox.setValue(value)
        

    def _handleHigherPriceBarColorResetButtonClicked(self):
        """Called when the higherPriceBarColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = SettingsKeys.higherPriceBarColorSettingsDefValue 
        self.higherPriceBarColorEditButton.setColor(value)

    def _handleLowerPriceBarColorResetButtonClicked(self):
        """Called when the lowerPriceBarColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = SettingsKeys.lowerPriceBarColorSettingsDefValue
        self.lowerPriceBarColorEditButton.setColor(value)

    def _handleBarCountGraphicsItemColorResetButtonClicked(self):
        """Called when the barCountGraphicsItemColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = SettingsKeys.barCountGraphicsItemColorSettingsDefValue
        self.barCountGraphicsItemColorEditButton.setColor(value)

    def _handleBarCountGraphicsItemTextColorResetButtonClicked(self):
        """Called when the barCountGraphicsItemTextColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue
        self.barCountGraphicsItemTextColorEditButton.setColor(value)

    def _handlePriceBarResetAllToDefaultButtonClicked(self):
        """Called when the priceBarResetAllToDefaultButton is clicked for
        the PriceBar settings.  Resets the all the widget values in this
        widget tab to the default values.
        """

        self._handleZoomScaleFactorResetButtonClicked()
        self._handleHigherPriceBarColorResetButtonClicked()
        self._handleLowerPriceBarColorResetButtonClicked()
        self._handleBarCountGraphicsItemColorResetButtonClicked()
        self._handleBarCountGraphicsItemTextColorResetButtonClicked()

    def _handlePlanetSymbolResetAllToDefaultButtonClicked(self):
        """Called when the planetSymbolResetAllToDefaultButton is clicked
        for the Planet Symbol settings.  
        Resets the all the widget values in this widget tab to the default
        values.
        """
        
        # Sun
        self.planetSunGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetSunGlyphUnicodeDefValue)
        self.planetSunGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetSunGlyphFontSizeDefValue)
        self.planetSunAbbreviationLineEdit.\
            setText(SettingsKeys.planetSunAbbreviationDefValue)
        self.planetSunForegroundColorEditButton.\
            setColor(SettingsKeys.planetSunForegroundColorDefValue)
        self.planetSunBackgroundColorEditButton.\
            setColor(SettingsKeys.planetSunBackgroundColorDefValue)

        # Moon
        self.planetMoonGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMoonGlyphUnicodeDefValue)
        self.planetMoonGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMoonGlyphFontSizeDefValue)
        self.planetMoonAbbreviationLineEdit.\
            setText(SettingsKeys.planetMoonAbbreviationDefValue)
        self.planetMoonForegroundColorEditButton.\
            setColor(SettingsKeys.planetMoonForegroundColorDefValue)
        self.planetMoonBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMoonBackgroundColorDefValue)

        # Mercury
        self.planetMercuryGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMercuryGlyphUnicodeDefValue)
        self.planetMercuryGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMercuryGlyphFontSizeDefValue)
        self.planetMercuryAbbreviationLineEdit.\
            setText(SettingsKeys.planetMercuryAbbreviationDefValue)
        self.planetMercuryForegroundColorEditButton.\
            setColor(SettingsKeys.planetMercuryForegroundColorDefValue)
        self.planetMercuryBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMercuryBackgroundColorDefValue)

        # Venus
        self.planetVenusGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetVenusGlyphUnicodeDefValue)
        self.planetVenusGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetVenusGlyphFontSizeDefValue)
        self.planetVenusAbbreviationLineEdit.\
            setText(SettingsKeys.planetVenusAbbreviationDefValue)
        self.planetVenusForegroundColorEditButton.\
            setColor(SettingsKeys.planetVenusForegroundColorDefValue)
        self.planetVenusBackgroundColorEditButton.\
            setColor(SettingsKeys.planetVenusBackgroundColorDefValue)

        # Earth
        self.planetEarthGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetEarthGlyphUnicodeDefValue)
        self.planetEarthGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetEarthGlyphFontSizeDefValue)
        self.planetEarthAbbreviationLineEdit.\
            setText(SettingsKeys.planetEarthAbbreviationDefValue)
        self.planetEarthForegroundColorEditButton.\
            setColor(SettingsKeys.planetEarthForegroundColorDefValue)
        self.planetEarthBackgroundColorEditButton.\
            setColor(SettingsKeys.planetEarthBackgroundColorDefValue)

        # Mars
        self.planetMarsGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMarsGlyphUnicodeDefValue)
        self.planetMarsGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMarsGlyphFontSizeDefValue)
        self.planetMarsAbbreviationLineEdit.\
            setText(SettingsKeys.planetMarsAbbreviationDefValue)
        self.planetMarsForegroundColorEditButton.\
            setColor(SettingsKeys.planetMarsForegroundColorDefValue)
        self.planetMarsBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMarsBackgroundColorDefValue)

        # Jupiter
        self.planetJupiterGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetJupiterGlyphUnicodeDefValue)
        self.planetJupiterGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetJupiterGlyphFontSizeDefValue)
        self.planetJupiterAbbreviationLineEdit.\
            setText(SettingsKeys.planetJupiterAbbreviationDefValue)
        self.planetJupiterForegroundColorEditButton.\
            setColor(SettingsKeys.planetJupiterForegroundColorDefValue)
        self.planetJupiterBackgroundColorEditButton.\
            setColor(SettingsKeys.planetJupiterBackgroundColorDefValue)

        # Saturn
        self.planetSaturnGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetSaturnGlyphUnicodeDefValue)
        self.planetSaturnGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetSaturnGlyphFontSizeDefValue)
        self.planetSaturnAbbreviationLineEdit.\
            setText(SettingsKeys.planetSaturnAbbreviationDefValue)
        self.planetSaturnForegroundColorEditButton.\
            setColor(SettingsKeys.planetSaturnForegroundColorDefValue)
        self.planetSaturnBackgroundColorEditButton.\
            setColor(SettingsKeys.planetSaturnBackgroundColorDefValue)

        # Uranus
        self.planetUranusGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetUranusGlyphUnicodeDefValue)
        self.planetUranusGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetUranusGlyphFontSizeDefValue)
        self.planetUranusAbbreviationLineEdit.\
            setText(SettingsKeys.planetUranusAbbreviationDefValue)
        self.planetUranusForegroundColorEditButton.\
            setColor(SettingsKeys.planetUranusForegroundColorDefValue)
        self.planetUranusBackgroundColorEditButton.\
            setColor(SettingsKeys.planetUranusBackgroundColorDefValue)

        # Neptune
        self.planetNeptuneGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetNeptuneGlyphUnicodeDefValue)
        self.planetNeptuneGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetNeptuneGlyphFontSizeDefValue)
        self.planetNeptuneAbbreviationLineEdit.\
            setText(SettingsKeys.planetNeptuneAbbreviationDefValue)
        self.planetNeptuneForegroundColorEditButton.\
            setColor(SettingsKeys.planetNeptuneForegroundColorDefValue)
        self.planetNeptuneBackgroundColorEditButton.\
            setColor(SettingsKeys.planetNeptuneBackgroundColorDefValue)

        # Pluto
        self.planetPlutoGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetPlutoGlyphUnicodeDefValue)
        self.planetPlutoGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetPlutoGlyphFontSizeDefValue)
        self.planetPlutoAbbreviationLineEdit.\
            setText(SettingsKeys.planetPlutoAbbreviationDefValue)
        self.planetPlutoForegroundColorEditButton.\
            setColor(SettingsKeys.planetPlutoForegroundColorDefValue)
        self.planetPlutoBackgroundColorEditButton.\
            setColor(SettingsKeys.planetPlutoBackgroundColorDefValue)

        # MeanNorthNode
        self.planetMeanNorthNodeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMeanNorthNodeGlyphUnicodeDefValue)
        self.planetMeanNorthNodeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMeanNorthNodeGlyphFontSizeDefValue)
        self.planetMeanNorthNodeAbbreviationLineEdit.\
            setText(SettingsKeys.planetMeanNorthNodeAbbreviationDefValue)
        self.planetMeanNorthNodeForegroundColorEditButton.\
            setColor(SettingsKeys.planetMeanNorthNodeForegroundColorDefValue)
        self.planetMeanNorthNodeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMeanNorthNodeBackgroundColorDefValue)

        # MeanSouthNode
        self.planetMeanSouthNodeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMeanSouthNodeGlyphUnicodeDefValue)
        self.planetMeanSouthNodeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMeanSouthNodeGlyphFontSizeDefValue)
        self.planetMeanSouthNodeAbbreviationLineEdit.\
            setText(SettingsKeys.planetMeanSouthNodeAbbreviationDefValue)
        self.planetMeanSouthNodeForegroundColorEditButton.\
            setColor(SettingsKeys.planetMeanSouthNodeForegroundColorDefValue)
        self.planetMeanSouthNodeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMeanSouthNodeBackgroundColorDefValue)

        # TrueNorthNode
        self.planetTrueNorthNodeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetTrueNorthNodeGlyphUnicodeDefValue)
        self.planetTrueNorthNodeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetTrueNorthNodeGlyphFontSizeDefValue)
        self.planetTrueNorthNodeAbbreviationLineEdit.\
            setText(SettingsKeys.planetTrueNorthNodeAbbreviationDefValue)
        self.planetTrueNorthNodeForegroundColorEditButton.\
            setColor(SettingsKeys.planetTrueNorthNodeForegroundColorDefValue)
        self.planetTrueNorthNodeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetTrueNorthNodeBackgroundColorDefValue)

        # TrueSouthNode
        self.planetTrueSouthNodeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetTrueSouthNodeGlyphUnicodeDefValue)
        self.planetTrueSouthNodeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetTrueSouthNodeGlyphFontSizeDefValue)
        self.planetTrueSouthNodeAbbreviationLineEdit.\
            setText(SettingsKeys.planetTrueSouthNodeAbbreviationDefValue)
        self.planetTrueSouthNodeForegroundColorEditButton.\
            setColor(SettingsKeys.planetTrueSouthNodeForegroundColorDefValue)
        self.planetTrueSouthNodeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetTrueSouthNodeBackgroundColorDefValue)

        # Ceres
        self.planetCeresGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetCeresGlyphUnicodeDefValue)
        self.planetCeresGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetCeresGlyphFontSizeDefValue)
        self.planetCeresAbbreviationLineEdit.\
            setText(SettingsKeys.planetCeresAbbreviationDefValue)
        self.planetCeresForegroundColorEditButton.\
            setColor(SettingsKeys.planetCeresForegroundColorDefValue)
        self.planetCeresBackgroundColorEditButton.\
            setColor(SettingsKeys.planetCeresBackgroundColorDefValue)

        # Pallas
        self.planetPallasGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetPallasGlyphUnicodeDefValue)
        self.planetPallasGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetPallasGlyphFontSizeDefValue)
        self.planetPallasAbbreviationLineEdit.\
            setText(SettingsKeys.planetPallasAbbreviationDefValue)
        self.planetPallasForegroundColorEditButton.\
            setColor(SettingsKeys.planetPallasForegroundColorDefValue)
        self.planetPallasBackgroundColorEditButton.\
            setColor(SettingsKeys.planetPallasBackgroundColorDefValue)

        # Juno
        self.planetJunoGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetJunoGlyphUnicodeDefValue)
        self.planetJunoGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetJunoGlyphFontSizeDefValue)
        self.planetJunoAbbreviationLineEdit.\
            setText(SettingsKeys.planetJunoAbbreviationDefValue)
        self.planetJunoForegroundColorEditButton.\
            setColor(SettingsKeys.planetJunoForegroundColorDefValue)
        self.planetJunoBackgroundColorEditButton.\
            setColor(SettingsKeys.planetJunoBackgroundColorDefValue)

        # Vesta
        self.planetVestaGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetVestaGlyphUnicodeDefValue)
        self.planetVestaGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetVestaGlyphFontSizeDefValue)
        self.planetVestaAbbreviationLineEdit.\
            setText(SettingsKeys.planetVestaAbbreviationDefValue)
        self.planetVestaForegroundColorEditButton.\
            setColor(SettingsKeys.planetVestaForegroundColorDefValue)
        self.planetVestaBackgroundColorEditButton.\
            setColor(SettingsKeys.planetVestaBackgroundColorDefValue)

        # Chiron
        self.planetChironGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetChironGlyphUnicodeDefValue)
        self.planetChironGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetChironGlyphFontSizeDefValue)
        self.planetChironAbbreviationLineEdit.\
            setText(SettingsKeys.planetChironAbbreviationDefValue)
        self.planetChironForegroundColorEditButton.\
            setColor(SettingsKeys.planetChironForegroundColorDefValue)
        self.planetChironBackgroundColorEditButton.\
            setColor(SettingsKeys.planetChironBackgroundColorDefValue)

        # Gulika
        self.planetGulikaGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetGulikaGlyphUnicodeDefValue)
        self.planetGulikaGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetGulikaGlyphFontSizeDefValue)
        self.planetGulikaAbbreviationLineEdit.\
            setText(SettingsKeys.planetGulikaAbbreviationDefValue)
        self.planetGulikaForegroundColorEditButton.\
            setColor(SettingsKeys.planetGulikaForegroundColorDefValue)
        self.planetGulikaBackgroundColorEditButton.\
            setColor(SettingsKeys.planetGulikaBackgroundColorDefValue)

        # Mandi
        self.planetMandiGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMandiGlyphUnicodeDefValue)
        self.planetMandiGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMandiGlyphFontSizeDefValue)
        self.planetMandiAbbreviationLineEdit.\
            setText(SettingsKeys.planetMandiAbbreviationDefValue)
        self.planetMandiForegroundColorEditButton.\
            setColor(SettingsKeys.planetMandiForegroundColorDefValue)
        self.planetMandiBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMandiBackgroundColorDefValue)

        # MeanOfFive
        self.planetMeanOfFiveGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMeanOfFiveGlyphUnicodeDefValue)
        self.planetMeanOfFiveGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMeanOfFiveGlyphFontSizeDefValue)
        self.planetMeanOfFiveAbbreviationLineEdit.\
            setText(SettingsKeys.planetMeanOfFiveAbbreviationDefValue)
        self.planetMeanOfFiveForegroundColorEditButton.\
            setColor(SettingsKeys.planetMeanOfFiveForegroundColorDefValue)
        self.planetMeanOfFiveBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMeanOfFiveBackgroundColorDefValue)

        # CycleOfEight
        self.planetCycleOfEightGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetCycleOfEightGlyphUnicodeDefValue)
        self.planetCycleOfEightGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetCycleOfEightGlyphFontSizeDefValue)
        self.planetCycleOfEightAbbreviationLineEdit.\
            setText(SettingsKeys.planetCycleOfEightAbbreviationDefValue)
        self.planetCycleOfEightForegroundColorEditButton.\
            setColor(SettingsKeys.planetCycleOfEightForegroundColorDefValue)
        self.planetCycleOfEightBackgroundColorEditButton.\
            setColor(SettingsKeys.planetCycleOfEightBackgroundColorDefValue)

    def _handleNonPlanetSymbolResetAllToDefaultButtonClicked(self):
        """Called when the nonPlanetSymbolResetAllToDefaultButton is clicked
        for the Non-Planet Symbol settings.  
        Resets the all the widget values in this widget tab to the default
        values.
        """
        
        # Retrograde
        self.planetRetrogradeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetRetrogradeGlyphUnicodeDefValue)
        self.planetRetrogradeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetRetrogradeGlyphFontSizeDefValue)
        self.planetRetrogradeAbbreviationLineEdit.\
            setText(SettingsKeys.planetRetrogradeAbbreviationDefValue)
        self.planetRetrogradeForegroundColorEditButton.\
            setColor(SettingsKeys.planetRetrogradeForegroundColorDefValue)
        self.planetRetrogradeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetRetrogradeBackgroundColorDefValue)

        # Ascendant
        self.planetAscendantGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetAscendantGlyphUnicodeDefValue)
        self.planetAscendantGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetAscendantGlyphFontSizeDefValue)
        self.planetAscendantAbbreviationLineEdit.\
            setText(SettingsKeys.planetAscendantAbbreviationDefValue)
        self.planetAscendantForegroundColorEditButton.\
            setColor(SettingsKeys.planetAscendantForegroundColorDefValue)
        self.planetAscendantBackgroundColorEditButton.\
            setColor(SettingsKeys.planetAscendantBackgroundColorDefValue)

        # Midheaven
        self.planetMidheavenGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMidheavenGlyphUnicodeDefValue)
        self.planetMidheavenGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMidheavenGlyphFontSizeDefValue)
        self.planetMidheavenAbbreviationLineEdit.\
            setText(SettingsKeys.planetMidheavenAbbreviationDefValue)
        self.planetMidheavenForegroundColorEditButton.\
            setColor(SettingsKeys.planetMidheavenForegroundColorDefValue)
        self.planetMidheavenBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMidheavenBackgroundColorDefValue)

        # HoraLagna
        self.planetHoraLagnaGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetHoraLagnaGlyphUnicodeDefValue)
        self.planetHoraLagnaGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetHoraLagnaGlyphFontSizeDefValue)
        self.planetHoraLagnaAbbreviationLineEdit.\
            setText(SettingsKeys.planetHoraLagnaAbbreviationDefValue)
        self.planetHoraLagnaForegroundColorEditButton.\
            setColor(SettingsKeys.planetHoraLagnaForegroundColorDefValue)
        self.planetHoraLagnaBackgroundColorEditButton.\
            setColor(SettingsKeys.planetHoraLagnaBackgroundColorDefValue)

        # GhatiLagna
        self.planetGhatiLagnaGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetGhatiLagnaGlyphUnicodeDefValue)
        self.planetGhatiLagnaGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetGhatiLagnaGlyphFontSizeDefValue)
        self.planetGhatiLagnaAbbreviationLineEdit.\
            setText(SettingsKeys.planetGhatiLagnaAbbreviationDefValue)
        self.planetGhatiLagnaForegroundColorEditButton.\
            setColor(SettingsKeys.planetGhatiLagnaForegroundColorDefValue)
        self.planetGhatiLagnaBackgroundColorEditButton.\
            setColor(SettingsKeys.planetGhatiLagnaBackgroundColorDefValue)

        # MeanLunarApogee
        self.planetMeanLunarApogeeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetMeanLunarApogeeGlyphUnicodeDefValue)
        self.planetMeanLunarApogeeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetMeanLunarApogeeGlyphFontSizeDefValue)
        self.planetMeanLunarApogeeAbbreviationLineEdit.\
            setText(SettingsKeys.planetMeanLunarApogeeAbbreviationDefValue)
        self.planetMeanLunarApogeeForegroundColorEditButton.\
            setColor(SettingsKeys.planetMeanLunarApogeeForegroundColorDefValue)
        self.planetMeanLunarApogeeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetMeanLunarApogeeBackgroundColorDefValue)

        # OsculatingLunarApogee
        self.planetOsculatingLunarApogeeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeDefValue)
        self.planetOsculatingLunarApogeeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeDefValue)
        self.planetOsculatingLunarApogeeAbbreviationLineEdit.\
            setText(SettingsKeys.planetOsculatingLunarApogeeAbbreviationDefValue)
        self.planetOsculatingLunarApogeeForegroundColorEditButton.\
            setColor(SettingsKeys.planetOsculatingLunarApogeeForegroundColorDefValue)
        self.planetOsculatingLunarApogeeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetOsculatingLunarApogeeBackgroundColorDefValue)

        # InterpolatedLunarApogee
        self.planetInterpolatedLunarApogeeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeDefValue)
        self.planetInterpolatedLunarApogeeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeDefValue)
        self.planetInterpolatedLunarApogeeAbbreviationLineEdit.\
            setText(SettingsKeys.planetInterpolatedLunarApogeeAbbreviationDefValue)
        self.planetInterpolatedLunarApogeeForegroundColorEditButton.\
            setColor(SettingsKeys.planetInterpolatedLunarApogeeForegroundColorDefValue)
        self.planetInterpolatedLunarApogeeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorDefValue)

        # InterpolatedLunarPerigee
        self.planetInterpolatedLunarPerigeeGlyphUnicodeLineEdit.\
            setText(SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeDefValue)
        self.planetInterpolatedLunarPerigeeGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeDefValue)
        self.planetInterpolatedLunarPerigeeAbbreviationLineEdit.\
            setText(SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationDefValue)
        self.planetInterpolatedLunarPerigeeForegroundColorEditButton.\
            setColor(SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorDefValue)
        self.planetInterpolatedLunarPerigeeBackgroundColorEditButton.\
            setColor(SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorDefValue)



    def _handleSignSymbolResetAllToDefaultButtonClicked(self):
        """Called when the signSymbolResetAllToDefaultButton is clicked
        for the Non-Planet Symbol settings.  
        Resets the all the widget values in this widget tab to the default
        values.
        """
        
        # Aries
        self.planetAriesGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signAriesGlyphUnicodeDefValue)
        self.planetAriesGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signAriesGlyphFontSizeDefValue)
        self.planetAriesAbbreviationLineEdit.\
            setText(SettingsKeys.signAriesAbbreviationDefValue)
        self.planetAriesForegroundColorEditButton.\
            setColor(SettingsKeys.signAriesForegroundColorDefValue)
        self.planetAriesBackgroundColorEditButton.\
            setColor(SettingsKeys.signAriesBackgroundColorDefValue)

        # Taurus
        self.planetTaurusGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signTaurusGlyphUnicodeDefValue)
        self.planetTaurusGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signTaurusGlyphFontSizeDefValue)
        self.planetTaurusAbbreviationLineEdit.\
            setText(SettingsKeys.signTaurusAbbreviationDefValue)
        self.planetTaurusForegroundColorEditButton.\
            setColor(SettingsKeys.signTaurusForegroundColorDefValue)
        self.planetTaurusBackgroundColorEditButton.\
            setColor(SettingsKeys.signTaurusBackgroundColorDefValue)

        # Gemini
        self.planetGeminiGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signGeminiGlyphUnicodeDefValue)
        self.planetGeminiGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signGeminiGlyphFontSizeDefValue)
        self.planetGeminiAbbreviationLineEdit.\
            setText(SettingsKeys.signGeminiAbbreviationDefValue)
        self.planetGeminiForegroundColorEditButton.\
            setColor(SettingsKeys.signGeminiForegroundColorDefValue)
        self.planetGeminiBackgroundColorEditButton.\
            setColor(SettingsKeys.signGeminiBackgroundColorDefValue)

        # Cancer
        self.planetCancerGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signCancerGlyphUnicodeDefValue)
        self.planetCancerGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signCancerGlyphFontSizeDefValue)
        self.planetCancerAbbreviationLineEdit.\
            setText(SettingsKeys.signCancerAbbreviationDefValue)
        self.planetCancerForegroundColorEditButton.\
            setColor(SettingsKeys.signCancerForegroundColorDefValue)
        self.planetCancerBackgroundColorEditButton.\
            setColor(SettingsKeys.signCancerBackgroundColorDefValue)

        # Leo
        self.planetLeoGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signLeoGlyphUnicodeDefValue)
        self.planetLeoGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signLeoGlyphFontSizeDefValue)
        self.planetLeoAbbreviationLineEdit.\
            setText(SettingsKeys.signLeoAbbreviationDefValue)
        self.planetLeoForegroundColorEditButton.\
            setColor(SettingsKeys.signLeoForegroundColorDefValue)
        self.planetLeoBackgroundColorEditButton.\
            setColor(SettingsKeys.signLeoBackgroundColorDefValue)

        # Virgo
        self.planetVirgoGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signVirgoGlyphUnicodeDefValue)
        self.planetVirgoGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signVirgoGlyphFontSizeDefValue)
        self.planetVirgoAbbreviationLineEdit.\
            setText(SettingsKeys.signVirgoAbbreviationDefValue)
        self.planetVirgoForegroundColorEditButton.\
            setColor(SettingsKeys.signVirgoForegroundColorDefValue)
        self.planetVirgoBackgroundColorEditButton.\
            setColor(SettingsKeys.signVirgoBackgroundColorDefValue)

        # Libra
        self.planetLibraGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signLibraGlyphUnicodeDefValue)
        self.planetLibraGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signLibraGlyphFontSizeDefValue)
        self.planetLibraAbbreviationLineEdit.\
            setText(SettingsKeys.signLibraAbbreviationDefValue)
        self.planetLibraForegroundColorEditButton.\
            setColor(SettingsKeys.signLibraForegroundColorDefValue)
        self.planetLibraBackgroundColorEditButton.\
            setColor(SettingsKeys.signLibraBackgroundColorDefValue)

        # Scorpio
        self.planetScorpioGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signScorpioGlyphUnicodeDefValue)
        self.planetScorpioGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signScorpioGlyphFontSizeDefValue)
        self.planetScorpioAbbreviationLineEdit.\
            setText(SettingsKeys.signScorpioAbbreviationDefValue)
        self.planetScorpioForegroundColorEditButton.\
            setColor(SettingsKeys.signScorpioForegroundColorDefValue)
        self.planetScorpioBackgroundColorEditButton.\
            setColor(SettingsKeys.signScorpioBackgroundColorDefValue)

        # Sagittarius
        self.planetSagittariusGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signSagittariusGlyphUnicodeDefValue)
        self.planetSagittariusGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signSagittariusGlyphFontSizeDefValue)
        self.planetSagittariusAbbreviationLineEdit.\
            setText(SettingsKeys.signSagittariusAbbreviationDefValue)
        self.planetSagittariusForegroundColorEditButton.\
            setColor(SettingsKeys.signSagittariusForegroundColorDefValue)
        self.planetSagittariusBackgroundColorEditButton.\
            setColor(SettingsKeys.signSagittariusBackgroundColorDefValue)

        # Capricorn
        self.planetCapricornGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signCapricornGlyphUnicodeDefValue)
        self.planetCapricornGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signCapricornGlyphFontSizeDefValue)
        self.planetCapricornAbbreviationLineEdit.\
            setText(SettingsKeys.signCapricornAbbreviationDefValue)
        self.planetCapricornForegroundColorEditButton.\
            setColor(SettingsKeys.signCapricornForegroundColorDefValue)
        self.planetCapricornBackgroundColorEditButton.\
            setColor(SettingsKeys.signCapricornBackgroundColorDefValue)

        # Aquarius
        self.planetAquariusGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signAquariusGlyphUnicodeDefValue)
        self.planetAquariusGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signAquariusGlyphFontSizeDefValue)
        self.planetAquariusAbbreviationLineEdit.\
            setText(SettingsKeys.signAquariusAbbreviationDefValue)
        self.planetAquariusForegroundColorEditButton.\
            setColor(SettingsKeys.signAquariusForegroundColorDefValue)
        self.planetAquariusBackgroundColorEditButton.\
            setColor(SettingsKeys.signAquariusBackgroundColorDefValue)

        # Pisces
        self.planetPiscesGlyphUnicodeLineEdit.\
            setText(SettingsKeys.signPiscesGlyphUnicodeDefValue)
        self.planetPiscesGlyphFontSizeSpinBox.\
            setValue(SettingsKeys.signPiscesGlyphFontSizeDefValue)
        self.planetPiscesAbbreviationLineEdit.\
            setText(SettingsKeys.signPiscesAbbreviationDefValue)
        self.planetPiscesForegroundColorEditButton.\
            setColor(SettingsKeys.signPiscesForegroundColorDefValue)
        self.planetPiscesBackgroundColorEditButton.\
            setColor(SettingsKeys.signPiscesBackgroundColorDefValue)


    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValuesToSettings()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class AppPreferencesEditDialog(QDialog):
    """QDialog for editing some of the app-wide preferenes.
    These values are retrieved and stored from the QSettings.
    """

    def __init__(self, parent=None):
        """Initializes the dialog and internal widget with the current
        settings."""

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.AppPreferencesEditDialog")

        self.setWindowTitle("Application Preferences")

        # Create the contents.
        self.appPreferencesEditWidget = AppPreferencesEditWidget()

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.appPreferencesEditWidget)
        self.setLayout(layout)

        self.appPreferencesEditWidget.okayButtonClicked.connect(self.accept)
        self.appPreferencesEditWidget.cancelButtonClicked.connect(self.reject)


class BirthInfoEditWidget(QWidget):
    """QWidget for editing a birth time or defining a new birth time."""

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.BirthInfoEditWidget")

        # Flag to determine if we have an internet connection and can reach
        # GeoNames web service.
        self.geoNamesEnabled = GeoNames.canConnectToWebService()

        if self.geoNamesEnabled:
            self.log.debug("Internet connection to GeoNames web service " + \
                           "is available.")
        else:
            self.log.info("Internet connection to GeoNames web service " + \
                          "is not available.")

        # Spacing amount for indenting inwards for some widgets.
        self.indentSpacing = 60

        # Birth time widgets.
        self.monthLabel = QLabel("&Month")
        self.monthLabel.setAlignment(Qt.AlignCenter)
        self.dayLabel = QLabel("&Day")
        self.dayLabel.setAlignment(Qt.AlignCenter)
        self.yearLabel = QLabel("&Year")
        self.yearLabel.setAlignment(Qt.AlignCenter)
        self.calendarLabel = QLabel("Calendar")
        self.calendarLabel.setAlignment(Qt.AlignCenter)
        self.hourLabel = QLabel("&Hour (0-23)")
        self.hourLabel.setAlignment(Qt.AlignCenter)
        self.minuteLabel = QLabel("M&inute (0-59)")
        self.minuteLabel.setAlignment(Qt.AlignCenter)
        self.secondLabel = QLabel("Second (0-59)")
        self.secondLabel.setAlignment(Qt.AlignCenter)
        self.monthSpinBox = QSpinBox()
        self.monthSpinBox.setMinimum(1)
        self.monthSpinBox.setMaximum(12)
        self.daySpinBox = QSpinBox()
        self.daySpinBox.setMinimum(1)
        self.daySpinBox.setMaximum(31)
        self.yearSpinBox = QSpinBox()
        # Setting minimum year to 2, because below that, the pytz localize()
        # function can cause an OverflowError exception to be raised.
        self.yearSpinBox.setMinimum(2)
        # Maximum year must be set, otherwise the spinbox defaults it to 100.
        self.yearSpinBox.setMaximum(9999)
        self.calendarComboBox = QComboBox()
        self.calendarComboBox.addItem("Gregorian")
        self.calendarComboBox.addItem("Julian")
        self.calendarComboBox.setCurrentIndex(0)
        self.hourSpinBox = QSpinBox()
        self.hourSpinBox.setMinimum(0)
        self.hourSpinBox.setMaximum(23)
        self.minuteSpinBox = QSpinBox()
        self.minuteSpinBox.setMinimum(0)
        self.minuteSpinBox.setMaximum(59)
        self.secondSpinBox = QSpinBox()
        self.secondSpinBox.setMinimum(0)
        self.secondSpinBox.setMaximum(59)

        # Set buddies for birth time widgets.
        self.monthLabel.setBuddy(self.monthSpinBox)
        self.dayLabel.setBuddy(self.daySpinBox)
        self.yearLabel.setBuddy(self.yearSpinBox)
        self.hourLabel.setBuddy(self.hourSpinBox)
        self.minuteLabel.setBuddy(self.minuteSpinBox)

        # Birth time layout.
        self.birthTimeLayout = QGridLayout()
        self.birthTimeLayout.addWidget(self.monthLabel, 0, 0)
        self.birthTimeLayout.addWidget(self.dayLabel, 0, 1)
        self.birthTimeLayout.addWidget(self.yearLabel, 0, 2)
        self.birthTimeLayout.addWidget(self.calendarLabel, 0, 3)
        self.birthTimeLayout.addWidget(self.monthSpinBox, 1, 0)
        self.birthTimeLayout.addWidget(self.daySpinBox, 1, 1)
        self.birthTimeLayout.addWidget(self.yearSpinBox, 1, 2)
        self.birthTimeLayout.addWidget(self.calendarComboBox, 1, 3)
        self.birthTimeLayout.addWidget(self.hourLabel, 2, 0)
        self.birthTimeLayout.addWidget(self.minuteLabel, 2, 1)
        self.birthTimeLayout.addWidget(self.secondLabel, 2, 2)
        self.birthTimeLayout.addWidget(self.hourSpinBox, 3, 0)
        self.birthTimeLayout.addWidget(self.minuteSpinBox, 3, 1)
        self.birthTimeLayout.addWidget(self.secondSpinBox, 3, 2)

        self.birthTimeGroupBox = QGroupBox("Birth Time")
        self.birthTimeGroupBox.setLayout(self.birthTimeLayout)

        # Birth place widgets.
        self.cityNameLabel = QLabel("City N&ame")
        self.cityNameLabel.setAlignment(Qt.AlignCenter)
        self.cityNameLineEdit = QLineEdit()
        self.cityNameLabel.setBuddy(self.cityNameLineEdit)
        self.searchInAllCountriesButton = \
            QPushButton("&Search in all countries")
        self.searchInUsaButton = QPushButton("Search in USA")
        self.cityNameLineEdit.returnPressed.\
            connect(self.searchInAllCountriesButton.click)
        self.countriesComboBox = QComboBox()
        self.countriesComboBox.addItem("", "")
        self.countriesComboBox.addItem("Afghanistan", "AF")
        self.countriesComboBox.addItem("Åland Islands", "AX")
        self.countriesComboBox.addItem("Albania", "AL")
        self.countriesComboBox.addItem("Algeria", "DZ")
        self.countriesComboBox.addItem("American Samoa", "AS")
        self.countriesComboBox.addItem("Andorra", "AD")
        self.countriesComboBox.addItem("Angola", "AO")
        self.countriesComboBox.addItem("Anguilla", "AI")
        self.countriesComboBox.addItem("Antarctica", "AQ")
        self.countriesComboBox.addItem("Antigua and Barbuda", "AG")
        self.countriesComboBox.addItem("Argentina", "AR")
        self.countriesComboBox.addItem("Armenia", "AM")
        self.countriesComboBox.addItem("Aruba", "AW")
        self.countriesComboBox.addItem("Australia", "AU")
        self.countriesComboBox.addItem("Austria", "AT")
        self.countriesComboBox.addItem("Azerbaijan", "AZ")
        self.countriesComboBox.addItem("Bahamas", "BS")
        self.countriesComboBox.addItem("Bahrain", "BH")
        self.countriesComboBox.addItem("Bangladesh", "BD")
        self.countriesComboBox.addItem("Barbados", "BB")
        self.countriesComboBox.addItem("Belarus", "BY")
        self.countriesComboBox.addItem("Belgium", "BE")
        self.countriesComboBox.addItem("Belize", "BZ")
        self.countriesComboBox.addItem("Benin", "BJ")
        self.countriesComboBox.addItem("Bermuda", "BM")
        self.countriesComboBox.addItem("Bhutan", "BT")
        self.countriesComboBox.addItem("Bolivia", "BO")
        self.countriesComboBox.addItem("Bosnia and Herzegovina", "BA")
        self.countriesComboBox.addItem("Botswana", "BW")
        self.countriesComboBox.addItem("Bouvet Island", "BV")
        self.countriesComboBox.addItem("Brazil", "BR")
        self.countriesComboBox.addItem("British Indian Ocean Territory", "IO")
        self.countriesComboBox.addItem("British Virgin Islands", "VG")
        self.countriesComboBox.addItem("Brunei", "BN")
        self.countriesComboBox.addItem("Bulgaria", "BG")
        self.countriesComboBox.addItem("Burkina Faso", "BF")
        self.countriesComboBox.addItem("Burundi", "BI")
        self.countriesComboBox.addItem("Cambodia", "KH")
        self.countriesComboBox.addItem("Cameroon", "CM")
        self.countriesComboBox.addItem("Canada", "CA")
        self.countriesComboBox.addItem("Cape Verde", "CV")
        self.countriesComboBox.addItem("Cayman Islands", "KY")
        self.countriesComboBox.addItem("Central African Republic", "CF")
        self.countriesComboBox.addItem("Chad", "TD")
        self.countriesComboBox.addItem("Chile", "CL")
        self.countriesComboBox.addItem("China", "CN")
        self.countriesComboBox.addItem("Christmas Island", "CX")
        self.countriesComboBox.addItem("Cocos [Keeling] Islands", "CC")
        self.countriesComboBox.addItem("Colombia", "CO")
        self.countriesComboBox.addItem("Comoros", "KM")
        self.countriesComboBox.addItem("Congo [DRC]", "CD")
        self.countriesComboBox.addItem("Congo [Republic]", "CG")
        self.countriesComboBox.addItem("Cook Islands", "CK")
        self.countriesComboBox.addItem("Costa Rica", "CR")
        self.countriesComboBox.addItem("Croatia", "HR")
        self.countriesComboBox.addItem("Cuba", "CU")
        self.countriesComboBox.addItem("Cyprus", "CY")
        self.countriesComboBox.addItem("Czech Republic", "CZ")
        self.countriesComboBox.addItem("Denmark", "DK")
        self.countriesComboBox.addItem("Djibouti", "DJ")
        self.countriesComboBox.addItem("Dominica", "DM")
        self.countriesComboBox.addItem("Dominican Republic", "DO")
        self.countriesComboBox.addItem("East Timor", "TL")
        self.countriesComboBox.addItem("Ecuador", "EC")
        self.countriesComboBox.addItem("Egypt", "EG")
        self.countriesComboBox.addItem("El Salvador", "SV")
        self.countriesComboBox.addItem("Equatorial Guinea", "GQ")
        self.countriesComboBox.addItem("Eritrea", "ER")
        self.countriesComboBox.addItem("Estonia", "EE")
        self.countriesComboBox.addItem("Ethiopia", "ET")
        self.countriesComboBox.addItem("Falkland Islands", "FK")
        self.countriesComboBox.addItem("Faroe Islands", "FO")
        self.countriesComboBox.addItem("Fiji", "FJ")
        self.countriesComboBox.addItem("Finland", "FI")
        self.countriesComboBox.addItem("France", "FR")
        self.countriesComboBox.addItem("French Guiana", "GF")
        self.countriesComboBox.addItem("French Polynesia", "PF")
        self.countriesComboBox.addItem("French Southern Territories", "TF")
        self.countriesComboBox.addItem("Gabon", "GA")
        self.countriesComboBox.addItem("Gambia", "GM")
        self.countriesComboBox.addItem("Georgia", "GE")
        self.countriesComboBox.addItem("Germany", "DE")
        self.countriesComboBox.addItem("Ghana", "GH")
        self.countriesComboBox.addItem("Gibraltar", "GI")
        self.countriesComboBox.addItem("Greece", "GR")
        self.countriesComboBox.addItem("Greenland", "GL")
        self.countriesComboBox.addItem("Grenada", "GD")
        self.countriesComboBox.addItem("Guadeloupe", "GP")
        self.countriesComboBox.addItem("Guam", "GU")
        self.countriesComboBox.addItem("Guatemala", "GT")
        self.countriesComboBox.addItem("Guernsey", "GG")
        self.countriesComboBox.addItem("Guinea-Bissau", "GW")
        self.countriesComboBox.addItem("Guinea", "GN")
        self.countriesComboBox.addItem("Guyana", "GY")
        self.countriesComboBox.addItem("Haiti", "HT")
        self.countriesComboBox.addItem("Heard Island and McDonald Islands", "HM")
        self.countriesComboBox.addItem("Honduras", "HN")
        self.countriesComboBox.addItem("Hong Kong", "HK")
        self.countriesComboBox.addItem("Hungary", "HU")
        self.countriesComboBox.addItem("Iceland", "IS")
        self.countriesComboBox.addItem("India", "IN")
        self.countriesComboBox.addItem("Indonesia", "ID")
        self.countriesComboBox.addItem("Iran", "IR")
        self.countriesComboBox.addItem("Iraq", "IQ")
        self.countriesComboBox.addItem("Ireland", "IE")
        self.countriesComboBox.addItem("Isle of Man", "IM")
        self.countriesComboBox.addItem("Israel", "IL")
        self.countriesComboBox.addItem("Italy", "IT")
        self.countriesComboBox.addItem("Ivory Coast", "CI")
        self.countriesComboBox.addItem("Jamaica", "JM")
        self.countriesComboBox.addItem("Japan", "JP")
        self.countriesComboBox.addItem("Jersey", "JE")
        self.countriesComboBox.addItem("Jordan", "JO")
        self.countriesComboBox.addItem("Kazakhstan", "KZ")
        self.countriesComboBox.addItem("Kenya", "KE")
        self.countriesComboBox.addItem("Kiribati", "KI")
        self.countriesComboBox.addItem("Kosovo", "XK")
        self.countriesComboBox.addItem("Kuwait", "KW")
        self.countriesComboBox.addItem("Kyrgyzstan", "KG")
        self.countriesComboBox.addItem("Laos", "LA")
        self.countriesComboBox.addItem("Latvia", "LV")
        self.countriesComboBox.addItem("Lebanon", "LB")
        self.countriesComboBox.addItem("Lesotho", "LS")
        self.countriesComboBox.addItem("Liberia", "LR")
        self.countriesComboBox.addItem("Libya", "LY")
        self.countriesComboBox.addItem("Liechtenstein", "LI")
        self.countriesComboBox.addItem("Lithuania", "LT")
        self.countriesComboBox.addItem("Luxembourg", "LU")
        self.countriesComboBox.addItem("Macau", "MO")
        self.countriesComboBox.addItem("Macedonia", "MK")
        self.countriesComboBox.addItem("Madagascar", "MG")
        self.countriesComboBox.addItem("Malawi", "MW")
        self.countriesComboBox.addItem("Malaysia", "MY")
        self.countriesComboBox.addItem("Maldives", "MV")
        self.countriesComboBox.addItem("Mali", "ML")
        self.countriesComboBox.addItem("Malta", "MT")
        self.countriesComboBox.addItem("Marshall Islands", "MH")
        self.countriesComboBox.addItem("Martinique", "MQ")
        self.countriesComboBox.addItem("Mauritania", "MR")
        self.countriesComboBox.addItem("Mauritius", "MU")
        self.countriesComboBox.addItem("Mayotte", "YT")
        self.countriesComboBox.addItem("Mexico", "MX")
        self.countriesComboBox.addItem("Micronesia", "FM")
        self.countriesComboBox.addItem("Moldova", "MD")
        self.countriesComboBox.addItem("Monaco", "MC")
        self.countriesComboBox.addItem("Mongolia", "MN")
        self.countriesComboBox.addItem("Montenegro", "ME")
        self.countriesComboBox.addItem("Montserrat", "MS")
        self.countriesComboBox.addItem("Morocco", "MA")
        self.countriesComboBox.addItem("Mozambique", "MZ")
        self.countriesComboBox.addItem("Myanmar [Burma]", "MM")
        self.countriesComboBox.addItem("Namibia", "NA")
        self.countriesComboBox.addItem("Nauru", "NR")
        self.countriesComboBox.addItem("Nepal", "NP")
        self.countriesComboBox.addItem("Netherlands Antilles", "AN")
        self.countriesComboBox.addItem("Netherlands", "NL")
        self.countriesComboBox.addItem("New Caledonia", "NC")
        self.countriesComboBox.addItem("New Zealand", "NZ")
        self.countriesComboBox.addItem("Nicaragua", "NI")
        self.countriesComboBox.addItem("Nigeria", "NG")
        self.countriesComboBox.addItem("Niger", "NE")
        self.countriesComboBox.addItem("Niue", "NU")
        self.countriesComboBox.addItem("Norfolk Island", "NF")
        self.countriesComboBox.addItem("Northern Mariana Islands", "MP")
        self.countriesComboBox.addItem("North Korea", "KP")
        self.countriesComboBox.addItem("Norway", "NO")
        self.countriesComboBox.addItem("Oman", "OM")
        self.countriesComboBox.addItem("Pakistan", "PK")
        self.countriesComboBox.addItem("Palau", "PW")
        self.countriesComboBox.addItem("Palestinian Territories", "PS")
        self.countriesComboBox.addItem("Panama", "PA")
        self.countriesComboBox.addItem("Papua New Guinea", "PG")
        self.countriesComboBox.addItem("Paraguay", "PY")
        self.countriesComboBox.addItem("Peru", "PE")
        self.countriesComboBox.addItem("Philippines", "PH")
        self.countriesComboBox.addItem("Pitcairn Islands", "PN")
        self.countriesComboBox.addItem("Poland", "PL")
        self.countriesComboBox.addItem("Portugal", "PT")
        self.countriesComboBox.addItem("Puerto Rico", "PR")
        self.countriesComboBox.addItem("Qatar", "QA")
        self.countriesComboBox.addItem("Réunion", "RE")
        self.countriesComboBox.addItem("Romania", "RO")
        self.countriesComboBox.addItem("Russia", "RU")
        self.countriesComboBox.addItem("Rwanda", "RW")
        self.countriesComboBox.addItem("Saint Barthélemy", "BL")
        self.countriesComboBox.addItem("Saint Helena", "SH")
        self.countriesComboBox.addItem("Saint Kitts and Nevis", "KN")
        self.countriesComboBox.addItem("Saint Lucia", "LC")
        self.countriesComboBox.addItem("Saint Martin", "MF")
        self.countriesComboBox.addItem("Saint Pierre and Miquelon", "PM")
        self.countriesComboBox.addItem("Saint Vincent and the Grenadines", "VC")
        self.countriesComboBox.addItem("Samoa", "WS")
        self.countriesComboBox.addItem("San Marino", "SM")
        self.countriesComboBox.addItem("São Tomé and Príncipe", "ST")
        self.countriesComboBox.addItem("Saudi Arabia", "SA")
        self.countriesComboBox.addItem("Senegal", "SN")
        self.countriesComboBox.addItem("Serbia and Montenegro", "CS")
        self.countriesComboBox.addItem("Serbia", "RS")
        self.countriesComboBox.addItem("Seychelles", "SC")
        self.countriesComboBox.addItem("Sierra Leone", "SL")
        self.countriesComboBox.addItem("Singapore", "SG")
        self.countriesComboBox.addItem("Slovakia", "SK")
        self.countriesComboBox.addItem("Slovenia", "SI")
        self.countriesComboBox.addItem("Solomon Islands", "SB")
        self.countriesComboBox.addItem("Somalia", "SO")
        self.countriesComboBox.addItem("South Africa", "ZA")
        self.countriesComboBox.addItem("South Georgia and the South Sandwich Islands", "GS")
        self.countriesComboBox.addItem("South Korea", "KR")
        self.countriesComboBox.addItem("Spain", "ES")
        self.countriesComboBox.addItem("Sri Lanka", "LK")
        self.countriesComboBox.addItem("Sudan", "SD")
        self.countriesComboBox.addItem("Suriname", "SR")
        self.countriesComboBox.addItem("Svalbard and Jan Mayen", "SJ")
        self.countriesComboBox.addItem("Swaziland", "SZ")
        self.countriesComboBox.addItem("Sweden", "SE")
        self.countriesComboBox.addItem("Switzerland", "CH")
        self.countriesComboBox.addItem("Syria", "SY")
        self.countriesComboBox.addItem("Taiwan", "TW")
        self.countriesComboBox.addItem("Tajikistan", "TJ")
        self.countriesComboBox.addItem("Tanzania", "TZ")
        self.countriesComboBox.addItem("Thailand", "TH")
        self.countriesComboBox.addItem("Togo", "TG")
        self.countriesComboBox.addItem("Tokelau", "TK")
        self.countriesComboBox.addItem("Tonga", "TO")
        self.countriesComboBox.addItem("Trinidad and Tobago", "TT")
        self.countriesComboBox.addItem("Tunisia", "TN")
        self.countriesComboBox.addItem("Turkey", "TR")
        self.countriesComboBox.addItem("Turkmenistan", "TM")
        self.countriesComboBox.addItem("Turks and Caicos Islands", "TC")
        self.countriesComboBox.addItem("Tuvalu", "TV")
        self.countriesComboBox.addItem("Uganda", "UG")
        self.countriesComboBox.addItem("Ukraine", "UA")
        self.countriesComboBox.addItem("United Arab Emirates", "AE")
        self.countriesComboBox.addItem("United Kingdom", "GB")
        self.countriesComboBox.addItem("United States", "US")
        self.countriesComboBox.addItem("Uruguay", "UY")
        self.countriesComboBox.addItem("U.S. Minor Outlying Islands", "UM")
        self.countriesComboBox.addItem("U.S. Virgin Islands", "VI")
        self.countriesComboBox.addItem("Uzbekistan", "UZ")
        self.countriesComboBox.addItem("Vanuatu", "VU")
        self.countriesComboBox.addItem("Vatican City", "VA")
        self.countriesComboBox.addItem("Venezuela", "VE")
        self.countriesComboBox.addItem("Vietnam", "VN")
        self.countriesComboBox.addItem("Wallis and Futuna", "WF")
        self.countriesComboBox.addItem("Western Sahara", "EH")
        self.countriesComboBox.addItem("Yemen", "YE")
        self.countriesComboBox.addItem("Zambia", "ZM")
        self.countriesComboBox.addItem("Zimbabwe", "ZW")

        self.searchInSpecifiedCountryButton = \
            QPushButton("Search in specified country")

        self.searchLocationLayout = QGridLayout()
        self.searchLocationLayout.addWidget(self.cityNameLabel, 0, 0)
        self.searchLocationLayout.addWidget(self.cityNameLineEdit, 1, 0)
        self.searchLocationLayout.addWidget(self.searchInAllCountriesButton, 
                                            1, 1)
        self.searchLocationLayout.addWidget(self.searchInUsaButton, 2, 1)
        self.searchLocationLayout.addWidget(self.countriesComboBox, 3, 0)
        self.searchLocationLayout.\
            addWidget(self.searchInSpecifiedCountryButton, 3, 1)

        self.birthPlaceSearchResultsLabel = QLabel("Search &results:")
        self.birthPlaceSearchResultsComboBox = QComboBox()
        self.birthPlaceSearchResultsLabel.\
            setBuddy(self.birthPlaceSearchResultsComboBox)
        # Disable the QComboBox until the results come in.
        self.birthPlaceSearchResultsComboBox.setEnabled(False)

        if self.geoNamesEnabled == False:
            self.geoNamesStatusLabel = \
                QLabel("<font color=\"red\">" + \
                       "Search functionality is disabled due to failed " + \
                       "network connection to GeoNames web service." + \
                       "</font>")
        else:
            self.geoNamesStatusLabel = QLabel("")

        self.geoNamesStatusLabel.setWordWrap(True)
        self.birthPlaceSearchResultsLayout = QVBoxLayout()
        self.birthPlaceSearchResultsLayout.addSpacing(20)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.birthPlaceSearchResultsLabel)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.birthPlaceSearchResultsComboBox)
        self.birthPlaceSearchResultsLayout.addSpacing(20)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.geoNamesStatusLabel)

        # Do I want to disable search widgets if the initial connect test
        # failed?  Maybe the second attempt via the search button will work.
        #if self.geoNamesEnabled == False:
        #    self.searchInUsaButton.setEnabled(False)
        #    self.searchInAllCountriesButton.setEnabled(False)
        #    self.searchInSpecifiedCountryButton.setEnabled(False)
        #    self.countriesComboBox.setEnabled(False)

        self.longitudeLabel = QLabel("&Longitude:")
        self.longitudeDegreesLabel = QLabel("Degrees (0-180)")
        self.longitudeMinutesLabel = QLabel("Minutes (0-59)")
        self.longitudeSecondsLabel = QLabel("Seconds (0-59)")

        self.longitudeDegreesSpinBox = QSpinBox()
        self.longitudeLabel.setBuddy(self.longitudeDegreesSpinBox)
        self.longitudeDegreesSpinBox.setMinimum(0)
        self.longitudeDegreesSpinBox.setMaximum(180)
        self.longitudeEastWestComboBox = QComboBox()
        self.longitudeEastWestComboBox.addItem("E", "E")
        self.longitudeEastWestComboBox.addItem("W", "W")
        self.longitudeEastWestComboBox.setCurrentIndex(0)
        self.longitudeMinutesSpinBox = QSpinBox()
        self.longitudeMinutesSpinBox.setMinimum(0)
        self.longitudeMinutesSpinBox.setMaximum(59)
        self.longitudeSecondsSpinBox = QSpinBox()
        self.longitudeSecondsSpinBox.setMinimum(0)
        self.longitudeSecondsSpinBox.setMaximum(59)

        self.lonGridLayout = QGridLayout()
        self.lonGridLayout.addWidget(self.longitudeDegreesLabel, 0, 1)
        self.lonGridLayout.addWidget(self.longitudeMinutesLabel, 0, 3)
        self.lonGridLayout.addWidget(self.longitudeSecondsLabel, 0, 4)
        self.lonGridLayout.addWidget(self.longitudeLabel, 1, 0)
        self.lonGridLayout.addWidget(self.longitudeDegreesSpinBox, 1, 1)
        self.lonGridLayout.addWidget(self.longitudeEastWestComboBox, 1, 2)
        self.lonGridLayout.addWidget(self.longitudeMinutesSpinBox, 1, 3)
        self.lonGridLayout.addWidget(self.longitudeSecondsSpinBox, 1, 4)

        self.longitudeDecimalFormatValueLabel = QLabel("")
        self.lonDecimalLayout = QHBoxLayout()
        self.lonDecimalLayout.addStretch()
        self.lonDecimalLayout.addWidget(self.longitudeDecimalFormatValueLabel)

        self.latitudeLabel = QLabel("Latit&ude:")
        self.latitudeDegreesLabel = QLabel("Degrees (0-90)")
        self.latitudeMinutesLabel = QLabel("Minutes (0-59)")
        self.latitudeSecondsLabel = QLabel("Seconds (0-59)")

        self.latitudeDegreesSpinBox = QSpinBox()
        self.latitudeLabel.setBuddy(self.latitudeDegreesSpinBox)
        self.latitudeDegreesSpinBox.setMinimum(0)
        self.latitudeDegreesSpinBox.setMaximum(90)
        self.latitudeNorthSouthComboBox = QComboBox()
        self.latitudeNorthSouthComboBox.addItem("N", "N")
        self.latitudeNorthSouthComboBox.addItem("S", "S")
        self.latitudeMinutesSpinBox = QSpinBox()
        self.latitudeMinutesSpinBox.setMinimum(0)
        self.latitudeMinutesSpinBox.setMaximum(59)
        self.latitudeSecondsSpinBox = QSpinBox()
        self.latitudeSecondsSpinBox.setMinimum(0)
        self.latitudeSecondsSpinBox.setMaximum(59)

        self.latGridLayout = QGridLayout()
        self.latGridLayout.addWidget(self.latitudeDegreesLabel, 0, 1)
        self.latGridLayout.addWidget(self.latitudeMinutesLabel, 0, 3)
        self.latGridLayout.addWidget(self.latitudeSecondsLabel, 0, 4)
        self.latGridLayout.addWidget(self.latitudeLabel, 1, 0)
        self.latGridLayout.addWidget(self.latitudeDegreesSpinBox, 1, 1)
        self.latGridLayout.addWidget(self.latitudeNorthSouthComboBox, 1, 2)
        self.latGridLayout.addWidget(self.latitudeMinutesSpinBox, 1, 3)
        self.latGridLayout.addWidget(self.latitudeSecondsSpinBox, 1, 4)
        self.latitudeDecimalFormatValueLabel = QLabel("")

        self.latDecimalLayout = QHBoxLayout()
        self.latDecimalLayout.addStretch()
        self.latDecimalLayout.addWidget(self.latitudeDecimalFormatValueLabel)

        self.latLonLayout = QVBoxLayout()
        self.latLonLayout.addLayout(self.lonGridLayout)
        self.latLonLayout.addLayout(self.lonDecimalLayout)
        self.latLonLayout.addLayout(self.latGridLayout)
        self.latLonLayout.addLayout(self.latDecimalLayout)

        self.elevationLabel = QLabel("Ele&vation:")
        self.elevationSpinBox = QSpinBox()
        self.elevationLabel.setBuddy(self.elevationSpinBox)
        # The dead sea is about -400 meters above sea level 
        # and mount everest is about 8850, so these settings should
        # cover just about all scenarios except for in-flight births.
        self.elevationSpinBox.setMinimum(-400)
        self.elevationSpinBox.setMaximum(10000)
        self.elevationSpinBox.setValue(0)
        self.elevationUnitsLabel = QLabel("meters above sea level")

        self.elevationLayout = QHBoxLayout()
        self.elevationLayout.addWidget(self.elevationLabel)
        self.elevationLayout.addWidget(self.elevationSpinBox)
        self.elevationLayout.addWidget(self.elevationUnitsLabel)

        self.birthLocationLayout = QVBoxLayout()
        self.birthLocationLayout.addLayout(self.searchLocationLayout)
        self.birthLocationLayout.addLayout(self.birthPlaceSearchResultsLayout)
        self.birthLocationLayout.addLayout(self.latLonLayout)
        self.birthLocationLayout.addLayout(self.elevationLayout)
        
        self.birthLocationGroupBox = QGroupBox("Birth Location")
        self.birthLocationGroupBox.setLayout(self.birthLocationLayout)
        

        # Timezone widgets.
        self.autodetectedOffsetRadioButton = \
            QRadioButton("Autodetected time&zone time offset")
        self.autodetectedOffsetRadioButton.setChecked(True)
        self.timezoneLabel = QLabel("Timezone: ")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)
        self.timezoneLayout = QHBoxLayout()
        self.timezoneLayout.addSpacing(self.indentSpacing)
        self.timezoneLayout.addWidget(self.timezoneLabel)
        self.timezoneLayout.addWidget(self.timezoneComboBox)

        self.timezoneOffsetLabel = QLabel("Time offset: ")
        self.timezoneOffsetValueLabel = QLabel("")
        self.timeOffsetValueLayout = QHBoxLayout()
        self.timeOffsetValueLayout.addSpacing(self.indentSpacing)
        self.timeOffsetValueLayout.addWidget(self.timezoneOffsetLabel)
        self.timeOffsetValueLayout.addWidget(self.timezoneOffsetValueLabel)

        self.manualEntryRadioButton = QRadioButton("Manual &Entry")
        self.timeOffsetHoursLabel = QLabel("Hours")
        self.timeOffsetHoursLabel.setAlignment(Qt.AlignCenter)
        self.timeOffsetMinutesLabel = QLabel("Minutes")
        self.timeOffsetMinutesLabel.setAlignment(Qt.AlignCenter)
        self.timeOffsetHoursSpinBox = QSpinBox()
        self.timeOffsetHoursSpinBox.setMinimum(0)
        self.timeOffsetHoursSpinBox.setMaximum(14)
        self.timeOffsetHoursSpinBox.setEnabled(False)
        self.timeOffsetMinutesSpinBox = QSpinBox()
        self.timeOffsetMinutesSpinBox.setMinimum(0)
        self.timeOffsetMinutesSpinBox.setMaximum(59)
        self.timeOffsetMinutesSpinBox.setEnabled(False)
        self.timeOffsetEastWestComboBox = QComboBox()
        self.timeOffsetEastWestComboBox.addItem("East of UTC", "E")
        self.timeOffsetEastWestComboBox.addItem("West of UTC", "W")
        self.timeOffsetEastWestComboBox.setEnabled(False)
        self.timeOffsetManualEntryGridLayout = QGridLayout()
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetHoursLabel, 0, 0)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetMinutesLabel, 0, 1)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetHoursSpinBox, 1, 0)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetMinutesSpinBox, 1, 1)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetEastWestComboBox, 1, 2)
        self.timeOffsetManualEntryLayout = QHBoxLayout()
        self.timeOffsetManualEntryLayout.addSpacing(self.indentSpacing)
        self.timeOffsetManualEntryLayout.\
            addLayout(self.timeOffsetManualEntryGridLayout)

        self.lmtRadioButton = \
            QRadioButton("Local Mean &Time (for really old dates)")
        
        self.timeOffsetLayout = QVBoxLayout()
        self.timeOffsetLayout.addWidget(self.autodetectedOffsetRadioButton)
        self.timeOffsetLayout.addLayout(self.timezoneLayout)
        self.timeOffsetLayout.addLayout(self.timeOffsetValueLayout)
        self.timeOffsetLayout.addWidget(self.manualEntryRadioButton)
        self.timeOffsetLayout.addLayout(self.timeOffsetManualEntryLayout)
        self.timeOffsetLayout.addWidget(self.lmtRadioButton)

        self.timeOffsetGroupBox = QGroupBox("Time Offset")
        self.timeOffsetGroupBox.setLayout(self.timeOffsetLayout)


        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.birthTimeGroupBox) 
        self.mainLayout.addWidget(self.birthLocationGroupBox) 
        self.mainLayout.addWidget(self.timeOffsetGroupBox) 
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        self.searchInAllCountriesButton.clicked.\
            connect(self._handleSearchInAllCountriesButtonClicked)
        self.searchInUsaButton.clicked.\
            connect(self._handleSearchInUsaButtonClicked)
        self.searchInSpecifiedCountryButton.clicked.\
            connect(self._handleSearchInSpecifiedCountryButtonClicked)

        self.birthPlaceSearchResultsComboBox.currentIndexChanged[int].\
            connect(self._handleSearchResultSelected)

        self.timezoneComboBox.currentIndexChanged[int].\
            connect(self._handleTimezoneComboBoxChanged)

        # Connect the birth time widgets being changed to the 
        # _handleBirthTimeWidgetsChanged slot.
        self.monthSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.daySpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.yearSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.calendarComboBox.currentIndexChanged[int].\
            connect(self._handleBirthTimeWidgetsChanged)
        self.hourSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.minuteSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.secondSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)


        # Connect the longitude widgets being changed to the slot to 
        # handle it.
        self.longitudeDegreesSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeEastWestComboBox.currentIndexChanged[int].\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeMinutesSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeSecondsSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)

        # Connect the latitude widgets being changed to the slot to 
        # handle it.
        self.latitudeDegreesSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeNorthSouthComboBox.currentIndexChanged[int].\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeMinutesSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeSecondsSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)

        # Connect radio buttons in the time offset groupbox.
        self.autodetectedOffsetRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)
        self.manualEntryRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)
        self.lmtRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)

        # Set the initial values/config in the widgets.

        # Select UTC timezone by default (this should be the last index).
        self.timezoneComboBox.\
            setCurrentIndex(self.timezoneComboBox.count() - 1)

        # Select the text in the first widget so that the user can 
        # immediately type to enter the value of the month.
        self.monthSpinBox.selectAll()


    def validate(self):
        """Validates the input values in the edit widgets.
        Currently this function always returns True since the 
        individual QSpinBox widgets and QComboBox widgets already have 
        validation to make sure they are valid values/format.
        """

        return True


    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.loadButton.setVisible(flag)
            self.cancelButton.setVisible(flag)


    def setBirthTimeWidgetValues(self, 
                                 year,
                                 month,
                                 day,
                                 hour,
                                 minute,
                                 second,
                                 calendar="Gregorian"):
        """Fills the birth time edit widgets with the values specified.

        Arguments:
        year    - int value for the year
        month   - int value for the month
        day     - int value for the day
        hour    - int value for the hour
        minute  - int value for the minute
        second  - int value for the second
        calendar - str value, for the calendar system used.
                   This is either 'Gregorian' or 'Julian'.
        """

        # Verify nothing is None.
        if (year == None or \
            month == None or \
            day == None or \
            hour == None or \
            minute == None or \
            second == None or \
            calendar == None):

            self.log.error("Parameters to setBirthTimeWidgetValues() " + 
                           "cannot be None.")
            return
        
        # These are int QSpinBoxes so force values to ints.
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        
        # Year.
        if (year >= self.yearSpinBox.minimum() and \
            year <= self.yearSpinBox.maximum()):

            self.yearSpinBox.setValue(year)
        else:
            self.log.warn("Year {} is outside the expected range [{}, {}].".\
                          format(year, 
                                 self.yearSpinBox.minimum(),
                                 self.yearSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.yearSpinBox.setValue(year)

        # Month.
        if (month >= self.monthSpinBox.minimum() and \
            month <= self.monthSpinBox.maximum()):

            self.monthSpinBox.setValue(month)
        else:
            self.log.warn("Month {} is outside the expected range [{}, {}].".\
                          format(month, 
                                 self.monthSpinBox.minimum(),
                                 self.monthSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.monthSpinBox.setValue(month)

        # Day.
        if (day >= self.daySpinBox.minimum() and \
            day <= self.daySpinBox.maximum()):

            self.daySpinBox.setValue(day)
        else:
            self.log.warn("Day {} is outside the expected range [{}, {}].".\
                          format(day, 
                                 self.daySpinBox.minimum(),
                                 self.daySpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.daySpinBox.setValue(day)

        # Hour.
        if (hour >= self.hourSpinBox.minimum() and \
            hour <= self.hourSpinBox.maximum()):

            self.hourSpinBox.setValue(hour)
        else:
            self.log.warn("Hour {} is outside the expected range [{}, {}].".\
                          format(hour, 
                                 self.hourSpinBox.minimum(),
                                 self.hourSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.hourSpinBox.setValue(hour)

        # Minute.
        if (minute >= self.minuteSpinBox.minimum() and \
            minute <= self.minuteSpinBox.maximum()):

            self.minuteSpinBox.setValue(minute)
        else:
            warnStr = "Minute {} is outside the expected range [{}, {}].".\
                      format(minute, 
                             self.minuteSpinBox.minimum(),
                             self.minuteSpinBox.maximum()) + \
                      "  Forcing it to be within the range."

            self.log.warn(warnStr)

            # The QSpinBox will force the value to be within range.
            self.minuteSpinBox.setValue(minute)

        # Second.
        if (second >= self.secondSpinBox.minimum() and \
            second <= self.secondSpinBox.maximum()):

            self.secondSpinBox.setValue(second)
        else:
            warnStr = "Second {} is outside the expected range [{}, {}].".\
                      format(second, 
                             self.secondSpinBox.minimum(),
                             self.secondSpinBox.maximum()) + \
                      "  Forcing it to be within the range."

            self.log.warn(warnStr)

            # The QSpinBox will force the value to be within range.
            self.secondSpinBox.setValue(second)

        # Calendar.
        index = self.calendarComboBox.findText(calendar)
        if (index != -1):
            self.calendarComboBox.setCurrentIndex(index)
        else:
            # Unrecognized calendar system specified.  
            warnStr = "Calendar system specified ({}) is not recognized.".\
                format(calendar)
            
            # Don't change anything in the widgets.


    def loadBirthInfo(self, birthInfoObj):
        """Loads the edit widgets with the data contained in the given
        BirthInfo object.

        Arguments:
        birthInfoObj - BirthInfo object containing data attributes for
        all the birth info fields that can be editted with this widget.
        """

        self.monthSpinBox.setValue(birthInfoObj.month)
        self.daySpinBox.setValue(birthInfoObj.day)
        self.yearSpinBox.setValue(birthInfoObj.year)

        # Try to find the index that matches the calendar string that is
        # stored in the BirthInfo object.
        indexToSet = \
            self.calendarComboBox.findText(birthInfoObj.calendar)

        # If the calendar type is not found, then default to whatever the
        # default is at widget creation.
        if indexToSet == -1:
            errStr = "Calendar type '" + birthInfoObj.calendar + \
                     "' is not supported.  Defaulting to " + \
                     self.calendarComboBox.currentText()
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
        else:
            # Valid index, so set the combo box.
            self.calendarComboBox.setCurrentIndex(indexToSet)

        self.hourSpinBox.setValue(birthInfoObj.hour)
        self.minuteSpinBox.setValue(birthInfoObj.minute)
        self.secondSpinBox.setValue(birthInfoObj.second)

        self.cityNameLineEdit.setText(birthInfoObj.locationName)

        # Try to find the index that matches the countryName string that is
        # stored in the BirthInfo object.
        indexToSet = \
            self.countriesComboBox.findText(birthInfoObj.countryName)

        if indexToSet == -1:
            # Couldn't find a match for the country name string.
            errStr = "Attempted to load an unknown country name: " + \
                birthInfoObj.countryName
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
        else:
            # Valid index, so set the combo box.
            self.countriesComboBox.setCurrentIndex(indexToSet)

        # No need to load anything into the
        # birthPlaceSearchResultsComboBox.

        # Convert longitude from a float value to degrees,
        # minutes, seconds and East/West polarity.
        (lonDegrees, lonMinutes, lonSeconds, lonPolarity) = \
            GeoInfo.longitudeToDegMinSec(birthInfoObj.longitudeDegrees)
        self.longitudeDegreesSpinBox.setValue(lonDegrees)
        index = self.longitudeEastWestComboBox.findText(lonPolarity)
        self.longitudeEastWestComboBox.setCurrentIndex(index)
        self.longitudeMinutesSpinBox.setValue(lonMinutes)
        self.longitudeSecondsSpinBox.setValue(lonSeconds)

        # Need to convert latitude from float value to degrees, minutes,
        # seconds and North/South polarity.
        (latDegrees, latMinutes, latSeconds, latPolarity) = \
            GeoInfo.latitudeToDegMinSec(birthInfoObj.latitudeDegrees)
        self.latitudeDegreesSpinBox.setValue(latDegrees)
        index = self.latitudeNorthSouthComboBox.findText(latPolarity)
        self.latitudeNorthSouthComboBox.setCurrentIndex(index)
        self.latitudeMinutesSpinBox.setValue(latMinutes)
        self.latitudeSecondsSpinBox.setValue(latSeconds)

        # Elevation.
        self.elevationSpinBox.setValue(birthInfoObj.elevation)

        # Timezone widgets.
        self.autodetectedOffsetRadioButton.\
            setChecked(birthInfoObj.timeOffsetAutodetectedRadioButtonState)
        self.manualEntryRadioButton.\
            setChecked(birthInfoObj.timeOffsetManualEntryRadioButtonState)
        self.lmtRadioButton.\
            setChecked(birthInfoObj.timeOffsetLMTRadioButtonState)

        index = self.timezoneComboBox.findText(birthInfoObj.timezoneName)
        if index != -1:
            self.timezoneComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the following timezone to load: '" + \
                birthInfoObj.timezoneName + "'"
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)

        # Create and set the string for the timezone offset label.
        self.timezoneOffsetValueLabel.\
            setText(birthInfoObj.timezoneOffsetAbbreviation + " " + \
                    birthInfoObj.timezoneOffsetValueStr)

        # Set the manual entry widgets.
        self.timeOffsetHoursSpinBox.\
            setValue(birthInfoObj.timezoneManualEntryHours)
        self.timeOffsetMinutesSpinBox.\
            setValue(birthInfoObj.timezoneManualEntryMinutes)
        index = self.timeOffsetEastWestComboBox.\
            findData(birthInfoObj.timezoneManualEntryEastWestComboBoxValue)
        if index != -1:
            self.timeOffsetEastWestComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the following manual entry timezone " + \
                "offset east/west text to load: '" + \
                birthInfoObj.timezoneManualEntryEastWestComboBoxValue + "'"
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)


    def getBirthInfo(self):
        """Extracts from all the widgets, the edit widget state and
        the birth information, and returns this information as 
        a BirthInfo object.

        Returns:
        BirthInfo - Fully populated BirthInfo object, holding the
        fields and state of this edit widget.
        """

        # Do some conversions first before creating the returned BirthInfo
        # object.

        # Get the longitude in degrees float value.
        longitudeDegrees = \
            GeoInfo.\
            longitudeToDegrees(self.longitudeDegreesSpinBox.value(),
                               self.longitudeMinutesSpinBox.value(),
                               self.longitudeSecondsSpinBox.value(),
                               str(self.longitudeEastWestComboBox.\
                                       currentText()))


        # Get the latitude in degrees float value.
        latitudeDegrees = \
            GeoInfo.\
            latitudeToDegrees(self.latitudeDegreesSpinBox.value(),
                              self.latitudeMinutesSpinBox.value(),
                              self.latitudeSecondsSpinBox.value(),
                              str(self.latitudeNorthSouthComboBox.\
                                      currentText()))

        # Get the timezone abbreviation and timezone offset.  We have to
        # jump through a bunch of hoops to get this.

        timezoneString = str(self.timezoneComboBox.currentText())
        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)
        # Get int values from the QSpinBox widgets.
        year = self.yearSpinBox.value()
        day = self.daySpinBox.value()
        month = self.monthSpinBox.value()
        hour = self.hourSpinBox.value()
        minute = self.minuteSpinBox.value()
        second = self.secondSpinBox.value()
        # Create the localized datetime object.
        datetimeObj = \
            datetime.datetime(year, month, day, hour, minute, second)
        localizedDatetimeObj = tzinfoObj.localize(datetimeObj)

        timezoneOffsetValueStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(localizedDatetimeObj)
        # Here tzname() won't return None because we explicitly specified a
        # pytz tzinfo to the datetime above.
        timezoneOffsetAbbreviation = localizedDatetimeObj.tzname()

        # Finally, create the BirthInfo object with all the required
        # inputs.
        
        rv = BirthInfo(self.yearSpinBox.value(),
                       self.monthSpinBox.value(),
                       self.daySpinBox.value(),
                       str(self.calendarComboBox.currentText()),
                       self.hourSpinBox.value(),
                       self.minuteSpinBox.value(),
                       self.secondSpinBox.value(),
                       str(self.cityNameLineEdit.text()),
                       str(self.countriesComboBox.currentText()),
                       longitudeDegrees,
                       latitudeDegrees,
                       self.elevationSpinBox.value(),
                       str(self.timezoneComboBox.currentText()),
                       timezoneOffsetAbbreviation,
                       timezoneOffsetValueStr,
                       self.timeOffsetHoursSpinBox.value(),
                       self.timeOffsetMinutesSpinBox.value(),
                       str(self.timeOffsetEastWestComboBox.\
                           itemData(self.timeOffsetEastWestComboBox.
                                    currentIndex())),
                       self.autodetectedOffsetRadioButton.isChecked(),
                       self.manualEntryRadioButton.isChecked(),
                       self.lmtRadioButton.isChecked())

        return rv


    def _handleSearchInAllCountriesButtonClicked(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.cityNameLineEdit.  Results that are returned are
        populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.debug("Entered _handleSearchInAllCountriesButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="",
                                       country="")
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            QMessageBox.warning(None, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        # Here we clear the country selected in the self.countriesComboBox 
        # that # is used for searching in a specified country.  We do this to
        # prevent the user from being confused about the fact that the 
        # results are for a search in all countries, not the country 
        # listened in that selection combo box.  
        # Index 0 here is just an empty string entry.
        self.countriesComboBox.setCurrentIndex(0)

        self.log.debug("Leaving _handleSearchInAllCountriesButtonClicked()")

    def _handleSearchInUsaButtonClicked(self):
        """Uses GeoNames to do a lookup of a location in the US based on the
        search string in self.cityNameLineEdit.  Results that are returned 
        are populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.debug("Entered _handleSearchInUsaButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="US",
                                       country="US")
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            parent = self
            QMessageBox.warning(parent, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        # Here we clear the country selected in the self.countriesComboBox 
        # that # is used for searching in a specified country.  We do this to
        # prevent the user from being confused about the fact that the 
        # results are for a search in all countries, not the country 
        # listened in that selection combo box.  
        # Index 0 here is just an empty string entry.
        self.countriesComboBox.setCurrentIndex(0)

        self.log.debug("Leaving _handleSearchInUsaButtonClicked()")


    def _handleSearchInSpecifiedCountryButtonClicked(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.cityNameLineEdit.  Results that are returned are
        populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.\
            debug("Entered _handleSearchInSpecifiedCountryButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)


        currIndex = self.countriesComboBox.currentIndex()
        countryName = self.countriesComboBox.itemText(currIndex)

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        countryCode = ""
        countryCodeQVariant = \
            self.countriesComboBox.itemData(currIndex)
        # Country code returned may be a QVariant storing a str 
        # or QString.
        if isinstance(countryCodeQVariant, QVariant):
            # This is a QVariant, so turn it into a PyObject first before
            # casting to str.
            countryCode = str(countryCodeQVariant.toPyObject())
        else:
            # It is just a str.  Wrap it again for safety's sake.
            countryCode = str(countryCodeQVariant)

        self.log.debug("countryName={}, countryCode={}".\
                       format(countryName, countryCode))

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="",
                                       country=countryCode)
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            parent = self
            QMessageBox.warning(parent, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        self.log.\
            debug("Leaving _handleSearchInSpecifiedCountryButtonClicked()")


    def _populateSearchResultsComboBox(self, geoInfos):
        """Populates self.birthPlaceSearchResultsComboBox with the 
        search results listed in the given list of GeoInfo objects.

        Arguments: 
        geoInfos - List of GeoNames.GeoInfo objects to use to populate 
                   the QComboBox.
        """

        self.log.debug("Entering _populateSearchResultsComboBox()")

        # Prepare the self.birthPlaceSearchResultsComboBox if there are new
        # results to populate it with.

        self.log.debug("Clearing birthPlaceSearchResultsComboBox...")
        # Clear the QComboBox of search results.
        self.birthPlaceSearchResultsComboBox.clear()

        if len(geoInfos) > 0:
            self.log.debug("Enabling birthPlaceSearchResultsComboBox...")
            # If the self.resultsComboBox is disabled, then enable it.
            if self.birthPlaceSearchResultsComboBox.isEnabled() == False:
                self.birthPlaceSearchResultsComboBox.setEnabled(True)

        # Populate the self.birthPlaceSearchResultsComboBox.
        for i in range(len(geoInfos)):
            geoInfo = geoInfos[i]

            displayStr = geoInfo.name
            if geoInfo.adminName1 != None and geoInfo.adminName1 != "":
                displayStr += ", " + geoInfo.adminName1
            if geoInfo.countryName != None and geoInfo.countryName != "":
                displayStr += ", " + geoInfo.countryName
            displayStr += " ({}, {})".format(geoInfo.latitudeStr(), 
                                             geoInfo.longitudeStr()) 
            if geoInfo.population != None and geoInfo.population != 0:
                displayStr += " (pop. {})".format(geoInfo.population)

            self.log.debug("Display name is: {}".format(displayStr))
            self.birthPlaceSearchResultsComboBox.addItem(displayStr, geoInfo)

        self.log.debug("Leaving _populateSearchResultsComboBox()")


    def _handleSearchResultSelected(self, index):
        """Determines which search result was selected, and populates
        the edit widgets with the info of that location.
        """

        self.log.debug("Entered _handleSearchResultSelected(index={})".\
                       format(index))

        # Only makes sense if the index selected is valid.  
        # Theoretically index should only be -1 on the very first load.
        if index == -1:
            return

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        maybeQVariant = self.birthPlaceSearchResultsComboBox.itemData(index)
        geoInfo = GeoInfo()
        if isinstance(maybeQVariant, QVariant):
            # This is really a QVariant, so use toPyObject().
            geoInfo = maybeQVariant.toPyObject()
        else:
            # PyQt converted it already for us.
            geoInfo = maybeQVariant

        # Make sure geoInfo is not None.  We need it in order to get the
        # timezone information.  It should never be None.
        if geoInfo == None:
            self.log.error("GeoInfo is None, when it should have " + \
                           "been an actual object!")
            return

        # Try to use the timezone in geoInfo first.  If that doesn't 
        # work, then the do a query for the timezone using the latitude and
        # longitude.
        if geoInfo.timezone != None and geoInfo.timezone != "":
            index = self.timezoneComboBox.findText(geoInfo.timezone)
            if index != -1:
                self.timezoneComboBox.setCurrentIndex(index)
            else:
                errStr = "Couldn't find timezone '" + geoInfo.timezone + \
                     "' returned by GeoNames in the pytz " + \
                     "list of timezones."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
        else:
            # Try to do the query ourselves from GeoNames.getTimezone().
            timezone = None
            try:
                timezone = GeoNames.getTimezone(geoInfo.latitude,
                                                geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't perform the search because " + \
                         "of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

            if timezone != None and timezone != "":
                index = self.timezoneComboBox.findText(geoInfo.timezone)
                if index != -1:
                    self.timezoneComboBox.setCurrentIndex(index)
                else:
                    errStr = "Couldn't find timezone '" + timezone + \
                         "' returned by GeoNames in the pytz " + \
                         "list of timezones."
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error", errStr)
            else:
                errStr = "GeoNames returned a null or empty timezone."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        
        # Set the longitude.
        (lonDegrees, lonMinutes, lonSeconds, lonPolarity) = \
            GeoInfo.longitudeToDegMinSec(geoInfo.longitude)
        self.longitudeDegreesSpinBox.setValue(lonDegrees)
        index = self.longitudeEastWestComboBox.findText(lonPolarity)
        self.longitudeEastWestComboBox.setCurrentIndex(index)
        self.longitudeMinutesSpinBox.setValue(lonMinutes)
        self.longitudeSecondsSpinBox.setValue(lonSeconds)

        # Set the latitude.
        (latDegrees, latMinutes, latSeconds, latPolarity) = \
            GeoInfo.latitudeToDegMinSec(geoInfo.latitude)
        self.latitudeDegreesSpinBox.setValue(latDegrees)
        index = self.latitudeNorthSouthComboBox.findText(latPolarity)
        self.latitudeNorthSouthComboBox.setCurrentIndex(index)
        self.latitudeMinutesSpinBox.setValue(latMinutes)
        self.latitudeSecondsSpinBox.setValue(latSeconds)

        # Set the elevation.
        elevation = 0
        if geoInfo.elevation != None:
            elevation = geoInfo.elevation
        else:
            # Try to obtain elevation via the GeoNames.getElevation() method.
            try:
                elevation = GeoNames.getElevation(geoInfo.latitude,
                                                  geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't get the elevation for lat={}, lon={} ".\
                        format(geoInfo.latitude, geoInfo.longitude) + \
                        "because of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

                # Set the elevation to 0.
                elevation = 0

        # Set the spinbox.
        if elevation == None or elevation == -9999.0:
            # Elevation is -9999.0 when it is in the ocean or if 
            # there was no data for this location.  
            
            # Here we'll just force the elevation to zero.

            logStr = "Elevation for lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to be zero."

            self.log.info(logStr)

            elevation = 0

        elif elevation < self.elevationSpinBox.minimum():
            # Set it to the minimum.
            logStr = "Elevation returned for " + \
               "lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to the minimum."
            self.log.info(logStr)

            elevation = self.elevationSpinBox.minimum()

        elif elevation > self.elevationSpinBox.maximum():
            # Set it to the maximum.
            logStr = "Elevation returned for " + \
               "lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to the maximum."

            self.log.info(logStr)

            elevation = self.elevationSpinBox.maximum()

        # Set the spinbox.
        self.elevationSpinBox.setValue(int(elevation))

        self.log.debug("Leaving _handleSearchResultSelected()")


    def _handleLongitudeEditWidgetChanged(self):
        """Recalculates the longitude as a float and displays it in 
        the QLabel that holds this value 
        (self.longitudeDecimalFormatValueLabel).
        """

        self.log.debug("Entered _handleLongitudeEditWidgetChanged()")

        degreesInt = self.longitudeDegreesSpinBox.value()
        minutesInt = self.longitudeMinutesSpinBox.value()
        secondsInt = self.longitudeSecondsSpinBox.value()
        polarityStr = str(self.longitudeEastWestComboBox.currentText()) 

        # Do the calculation.
        longitudeFloat = \
            GeoInfo.longitudeToDegrees(degreesInt,
                                       minutesInt,
                                       secondsInt,
                                       polarityStr)

        # Set the QLabel widget.
        self.longitudeDecimalFormatValueLabel.\
            setText("{}".format(longitudeFloat))

        self.log.debug("Leaving _handleLongitudeEditWidgetChanged()")
   
    def _handleLatitudeEditWidgetChanged(self):
        """Recalculates the latitude as a float and displays it in 
        the QLabel that holds this value
        (self.latitudeDecimalFormatValueLabel)
        """

        self.log.debug("Entered _handleLatitudeEditWidgetChanged()")

        degreesInt = self.latitudeDegreesSpinBox.value()
        minutesInt = self.latitudeMinutesSpinBox.value()
        secondsInt = self.latitudeSecondsSpinBox.value()
        polarityStr = str(self.latitudeNorthSouthComboBox.currentText()) 

        # Do the calculation.
        latitudeFloat = \
            GeoInfo.latitudeToDegrees(degreesInt,
                                       minutesInt,
                                       secondsInt,
                                       polarityStr)

        # Set the QLabel widget.
        self.latitudeDecimalFormatValueLabel.\
            setText("{}".format(latitudeFloat))

        self.log.debug("Leaving _handleLatitudeEditWidgetChanged()")

    def _handleTimezoneComboBoxChanged(self, index):
        """Sets the self.timezoneOffsetValueLabel to hold the actual 
        offset amount based off the date and timezone set in the widgets.

        If the radio button for 'Manual Entry' is not selected 
        (the widgets for manual entry are disabled), then this function 
        fills in the value in those widgets.  This is just for convenience 
        so that mods from the auto-detected value can be done.
        """

        self.log.debug("Entered _handleTimezoneComboBoxChanged()")

        # Get the timezone string from the QComboBox (and convert from 
        # QString to str).
        timezoneString = str(self.timezoneComboBox.currentText())

        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Get int values from the QSpinBox widgets.
        year = self.yearSpinBox.value()
        day = self.daySpinBox.value()
        month = self.monthSpinBox.value()
        hour = self.hourSpinBox.value()
        minute = self.minuteSpinBox.value()
        second = self.secondSpinBox.value()

        # Create the localized datetime object.
        datetimeObj = \
            datetime.datetime(year, month, day, hour, minute, second)
        localizedDatetimeObj = tzinfoObj.localize(datetimeObj)


        # Here we are creating the string that will be displayed in the label
        # holding the timezone and time offset info.

        # String that holds the time offset from UTC.
        offsetStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(localizedDatetimeObj)

        # Here tzname() won't return None because we explicitly specified a
        # pytz tzinfo to the datetime above.
        timeOffsetString = \
            localizedDatetimeObj.tzname() + " " + offsetStr

        # Set the label.
        self.timezoneOffsetValueLabel.setText(timeOffsetString)

        if self.manualEntryRadioButton.isChecked() == False:
            # Manual Entry widgets are disabled for user input.
            # Here we'll update the widgets' values.

            timeOffsetValueString = offsetStr

            if timeOffsetValueString[0:1] == "+":
                # West of UTC.
                index = self.timeOffsetEastWestComboBox.\
                    findText("West of UTC")
                self.timeOffsetEastWestComboBox.setCurrentIndex(index)
            elif timeOffsetValueString[0:1] == "-":
                # East of UTC.
                index = self.timeOffsetEastWestComboBox.\
                    findText("East of UTC")
                self.timeOffsetEastWestComboBox.setCurrentIndex(index)

            absoluteHoursOffset = int(timeOffsetValueString[1:3])
            absoluteMinutesOffset = int(timeOffsetValueString[3:5])

            self.timeOffsetHoursSpinBox.setValue(absoluteHoursOffset)
            self.timeOffsetMinutesSpinBox.setValue(absoluteMinutesOffset)

        self.log.debug("Leaving _handleTimezoneComboBoxChanged()")

    def _handleBirthTimeWidgetsChanged(self):
        """When the birth time widgets change, the time offset should be
        updated if it is set on 'Autodetected timezone time offset'.  
        This is because certain dates/times will fall under daylight 
        savings and thus the offset will be changed.
        """

        self.log.debug("Entered _handleBirthTimeWidgetsChanged()")

        # Find out what the timezone index is selected.
        index = self.timezoneComboBox.currentIndex()

        # Call the _handleTimezoneComboBoxChanged as if the timezone 
        # changed.  That function will make the necessary calls to update
        # the time offset used.
        self._handleTimezoneComboBoxChanged(index)

        self.log.debug("Leaving _handleBirthTimeWidgetsChanged()")

    def _handleTimeOffsetRadioButtonClicked(self):
        """Called when a radio button is clicked in the 'Time Offset'
        QGroupBox.  This function disables widgets that are under
        the radio button that is not selected.
        """

        self.log.debug("Entered _handleTimeOffsetRadioButtonClicked()")

        # The radio buttons are exclusive, so we can do the logic 
        # like below.

        shouldEnable = self.autodetectedOffsetRadioButton.isChecked()
        self.timezoneComboBox.setEnabled(shouldEnable)

        shouldEnable = self.manualEntryRadioButton.isChecked()
        self.timeOffsetHoursSpinBox.setEnabled(shouldEnable)
        self.timeOffsetMinutesSpinBox.setEnabled(shouldEnable)
        self.timeOffsetEastWestComboBox.setEnabled(shouldEnable)

        self.log.debug("Leaving _handleTimeOffsetRadioButtonClicked()")



    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked.
        This function validates the input widgets and emits 
        self.okayButtonClicked if the input has been validated
        successfully.
        """

        if self.validate() == True:
            self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked.
        This function does nothing but emit the 
        self.cancelButtonClicked signal.
        """

        self.cancelButtonClicked.emit()

class BirthInfoEditDialog(QDialog):
    """QDialog for editing a birth time of defining a new birth time."""

    def __init__(self, birthInfo=BirthInfo(), parent=None):
        """Initializes the QDialog with the info from birthInfo.

        Paraters:
        birthInfo - BirthInfo object to load the widgets with.
        parent    - QWidget parent.
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.BirthInfoEditDialog")

        # Create the contents.
        self.birthInfoEditWidget = BirthInfoEditWidget()
        self.birthInfoEditWidget.loadBirthInfo(birthInfo)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.birthInfoEditWidget)
        self.setLayout(layout)

        self.birthInfoEditWidget.okayButtonClicked.connect(self.accept)
        self.birthInfoEditWidget.cancelButtonClicked.connect(self.reject)


    def getBirthInfo(self):
        """Returns the BirthInfo object as is/was displayed in the widgets.
        """

        return self.birthInfoEditWidget.getBirthInfo()

class PriceBarChartScalingEditWidget(QWidget):
    """QWidget for editing the scaling used in a PriceBarChart.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, priceBarChartScaling, parent=None):
        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartScalingEditWidget")

        # Save off the PriceBarChartScaling object.
        self.priceBarChartScaling = priceBarChartScaling

        # QGroupBox to hold the edit widgets and form.
        self.groupBox = \
            QGroupBox("PriceBarChart Scaling:")

        # Name.
        self.nameLabel = QLabel("Name:")
        self.nameLineEdit = QLineEdit()

        # Description.
        self.descriptionLabel = QLabel("Description:")
        self.descriptionLineEdit = QLineEdit()

        # unitsOfTime (float).
        self.unitsOfTimeLabel = \
            QLabel("Units of time (dx):")
        self.unitsOfTimeSpinBox = QDoubleSpinBox()
        self.unitsOfTimeSpinBox.setDecimals(4)
        self.unitsOfTimeSpinBox.setMinimum(0.000001)
        self.unitsOfTimeSpinBox.setMaximum(100000.0)
        self.unitsOfTimeSpinBox.setValue(1)

        # unitsOfPrice (float).
        self.unitsOfPriceLabel = \
            QLabel("Units of price (dy):")
        self.unitsOfPriceSpinBox = QDoubleSpinBox()
        self.unitsOfPriceSpinBox.setDecimals(4)
        self.unitsOfPriceSpinBox.setMinimum(0.000001)
        self.unitsOfPriceSpinBox.setMaximum(100000.0)
        self.unitsOfPriceSpinBox.setValue(1)

        # viewScalingX (float).
        self.viewScalingXLabel = \
            QLabel("GraphicsView scalingX (sx):")
        self.viewScalingXSpinBox = QDoubleSpinBox()
        self.viewScalingXSpinBox.setDecimals(4)
        self.viewScalingXSpinBox.setMinimum(0.000001)
        self.viewScalingXSpinBox.setMaximum(100000.0)
        self.viewScalingXSpinBox.setValue(1)

        # viewScalingY (float).
        self.viewScalingYLabel = \
            QLabel("GraphicsView scalingY (sy):")
        self.viewScalingYSpinBox = QDoubleSpinBox()
        self.viewScalingYSpinBox.setDecimals(4)
        self.viewScalingYSpinBox.setMinimum(0.000001)
        self.viewScalingYSpinBox.setMaximum(100000.0)
        self.viewScalingYSpinBox.setValue(1)

        # Form layout.
        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignLeft)
        self.formLayout.addRow(self.nameLabel, self.nameLineEdit)
        self.formLayout.addRow(self.descriptionLabel, 
                               self.descriptionLineEdit)
        self.formLayout.addRow(self.unitsOfTimeLabel, 
                               self.unitsOfTimeSpinBox)
        self.formLayout.addRow(self.unitsOfPriceLabel, 
                               self.unitsOfPriceSpinBox)
        self.formLayout.addRow(self.viewScalingXLabel,
                               self.viewScalingXSpinBox)
        self.formLayout.addRow(self.viewScalingYLabel,
                               self.viewScalingYSpinBox)
        
        self.groupBox.setLayout(self.formLayout)

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
        # settings.
        self.loadScaling(self.priceBarChartScaling)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)


    def loadScaling(self, priceBarChartScaling):
        """Loads the widgets with values from the given
        PriceBarChartScaling object.
        """

        self.log.debug("Entered loadScaling()")

        # Check inputs.
        if priceBarChartScaling == None:
            self.log.error("Invalid parameter to loadScaling().  " + \
                           "priceBarChartScaling can't be None.")
            self.log.debug("Exiting loadScaling()")
            return
        else:
            self.priceBarChartScaling = priceBarChartScaling 

        self.nameLineEdit.setText(self.priceBarChartScaling.name)
        self.descriptionLineEdit.\
            setText(self.priceBarChartScaling.description)
        self.unitsOfTimeSpinBox.\
            setValue(self.priceBarChartScaling.getUnitsOfTime())
        self.unitsOfPriceSpinBox.\
            setValue(self.priceBarChartScaling.getUnitsOfPrice())
        self.viewScalingXSpinBox.\
            setValue(self.priceBarChartScaling.getViewScalingX())
        self.viewScalingYSpinBox.\
            setValue(self.priceBarChartScaling.getViewScalingY())
        
        self.log.debug("Exiting loadScaling()")
        
    def saveScaling(self):
        """Saves the values in the widgets to the 
        PriceBarChartScaling object passed in this class's constructor.
        """
    
        self.log.debug("Entered saveScaling()")

        self.priceBarChartScaling.name = self.nameLineEdit.text()
        self.priceBarChartScaling.description = \
            self.descriptionLineEdit.text()
        self.priceBarChartScaling.\
            setUnitsOfTime(self.unitsOfTimeSpinBox.value())
        self.priceBarChartScaling.\
            setUnitsOfPrice(self.unitsOfPriceSpinBox.value())
        self.priceBarChartScaling.\
            setViewScalingX(self.viewScalingXSpinBox.value())
        self.priceBarChartScaling.\
            setViewScalingY(self.viewScalingYSpinBox.value())

        self.log.debug("Exiting saveScaling()")

    def getPriceBarChartScaling(self):
        """Returns the internally stored PriceBarChartScaling object.
        This may or may not represent what is in the widgets, depending on
        whether or not saveScaling has been called.
        """

        return self.priceBarChartScaling

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveScaling()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartScalingEditDialog(QDialog):
    """QDialog for editing a PriceBarChartScaling object's class members.
    """

    def __init__(self, priceBarChartScaling, parent=None):
        """Initializes the dialog and internal widget with the current
        scaling object."""

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartScalingEditDialog")

        self.setWindowTitle("PriceBarChart Scaling")

        # Save a reference to the PriceBarChartScaling object.
        self.priceBarChartScaling = priceBarChartScaling

        # Create the contents.
        self.priceBarChartScalingEditWidget = \
            PriceBarChartScalingEditWidget(self.priceBarChartScaling)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.priceBarChartScalingEditWidget)
        self.setLayout(layout)

        self.priceBarChartScalingEditWidget.okayButtonClicked.\
            connect(self.accept)
        self.priceBarChartScalingEditWidget.cancelButtonClicked.\
            connect(self.reject)

    def getPriceBarChartScaling(self):
        """Returns the internally stored PriceBarChartScaling object."""

        scaling = \
            self.priceBarChartScalingEditWidget.getPriceBarChartScaling()
        
        return scaling

class PriceBarChartScalingsListEditWidget(QWidget):
    """QWidget for editing the list of scalings used in a PriceBarChart.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, 
                 priceBarChartScalings=[], 
                 priceBarChartScalingsIndex=-1, 
                 parent=None):
        """Initializes the edit widget with the given values.

        Arguments:

        priceBarChartScalings - List of PriceBarChartScaling objects.
                                This is the list of scalings we are editing.

        priceBarChartScalingsIndex - int value holding the index of the
                                     currently selected scaling.  
                                     This value is an index into the
                                     priceBarChartScalings list.
        parent - QWidget parent
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartScalingsListEditWidget")

        # Save off the list of PriceBarChartScalings.
        self.priceBarChartScalings = list(priceBarChartScalings)

        # Save off the index of the currently selected scaling.
        self.priceBarChartScalingsIndex = priceBarChartScalingsIndex

        self.scalingsListGroupBox = \
            QGroupBox("List of PriceBarChart scalings:")

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout to hold the list widget.
        self.listWidgetLayout = QVBoxLayout()
        self.listWidgetLayout.addWidget(self.listWidget)

        self.scalingsListGroupBox.setLayout(self.listWidgetLayout)
        
        # GroupBox holding info about the selected scaling from the list.
        self.selectedScalingGroupBox = QGroupBox("Selected scaling:")

        # Widgets for displaying the selected scaling from the list.
        self.selectedScalingNameLabel = QLabel("Name:")
        self.selectedScalingNameValueLabel = QLabel()
        
        self.selectedScalingDescriptionLabel = QLabel("Description:")
        self.selectedScalingDescriptionTextEdit = QTextEdit()
        self.selectedScalingDescriptionTextEdit.setAcceptRichText(False)
        self.selectedScalingDescriptionTextEdit.setEnabled(False)
        self.selectedScalingDescriptionTextEdit.setTextColor(Qt.black)
        self.selectedScalingDescriptionTextEdit.setMaximumHeight(80)
        
        self.selectedScalingUnitsOfTimeLabel = QLabel("Units of time:")
        self.selectedScalingUnitsOfTimeValueLabel = QLabel()
        self.selectedScalingUnitsOfPriceLabel = QLabel("Units of price:")
        self.selectedScalingUnitsOfPriceValueLabel = QLabel()
        
        self.selectedScalingViewScalingXLabel = QLabel("GraphicsView scalingX:")
        self.selectedScalingViewScalingXValueLabel = QLabel()
        self.selectedScalingViewScalingYLabel = QLabel("GraphicsView scalingY:")
        self.selectedScalingViewScalingYValueLabel = QLabel()

        # Grid layout.  
        self.selectedScalingGridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignment.
        al = Qt.AlignLeft

        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingNameLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingNameValueLabel, r, 1, al)
        r += 1
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingDescriptionLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingDescriptionTextEdit, r, 1, al)
        r += 1
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingUnitsOfTimeLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingUnitsOfTimeValueLabel, r, 1, al)
        r += 1
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingUnitsOfPriceLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingUnitsOfPriceValueLabel, r, 1, al)
        r += 1
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingViewScalingXLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingViewScalingXValueLabel, r, 1, al)
        r += 1
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingViewScalingYLabel, r, 0, al)
        self.selectedScalingGridLayout.\
            addWidget(self.selectedScalingViewScalingYValueLabel, r, 1, al)
        r += 1

        
        self.selectedScalingGroupBox.\
            setLayout(self.selectedScalingGridLayout)


        # GroupBox holding the scaling that is/will be applied to the
        # PriceBarChart.
        self.currentScalingGroupBox = QGroupBox("Current scaling:")

        # Widgets for displaying the current scaling.
        self.currentScalingNameLabel = QLabel("Name:")
        self.currentScalingNameValueLabel = QLabel()
        
        self.currentScalingDescriptionLabel = QLabel("Description:")
        self.currentScalingDescriptionTextEdit = QTextEdit()
        self.currentScalingDescriptionTextEdit.setAcceptRichText(False)
        self.currentScalingDescriptionTextEdit.setEnabled(False)
        self.currentScalingDescriptionTextEdit.setTextColor(Qt.black)
        self.currentScalingDescriptionTextEdit.setMaximumHeight(80)
        
        self.currentScalingUnitsOfTimeLabel = QLabel("Units of time:")
        self.currentScalingUnitsOfTimeValueLabel = QLabel()
        self.currentScalingUnitsOfPriceLabel = QLabel("Units of price:")
        self.currentScalingUnitsOfPriceValueLabel = QLabel()

        self.currentScalingViewScalingXLabel = QLabel("GraphicsView scalingX:")
        self.currentScalingViewScalingXValueLabel = QLabel()
        self.currentScalingViewScalingYLabel = QLabel("GraphicsView scalingY:")
        self.currentScalingViewScalingYValueLabel = QLabel()
        
        # Grid layout.  
        self.currentScalingGridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignment.
        al = Qt.AlignLeft

        self.currentScalingGridLayout.\
            addWidget(self.currentScalingNameLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingNameValueLabel, r, 1, al)
        r += 1
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingDescriptionLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingDescriptionTextEdit, r, 1, al)
        r += 1
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingUnitsOfTimeLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingUnitsOfTimeValueLabel, r, 1, al)
        r += 1
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingUnitsOfPriceLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingUnitsOfPriceValueLabel, r, 1, al)
        r += 1
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingViewScalingXLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingViewScalingXValueLabel, r, 1, al)
        r += 1
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingViewScalingYLabel, r, 0, al)
        self.currentScalingGridLayout.\
            addWidget(self.currentScalingViewScalingYValueLabel, r, 1, al)
        r += 1

        self.currentScalingGroupBox.\
            setLayout(self.currentScalingGridLayout)

        # Buttons for doing actions like adding, removing, and editing a
        # scaling, etc.

        self.addScalingButton = QPushButton("&Add Scaling")
        self.removeScalingButton = QPushButton("&Remove Scaling")
        self.editScalingButton = QPushButton("&Edit Scaling")
        self.moveSelectedScalingUpButton = QPushButton("Move scaling &up")
        self.moveSelectedScalingDownButton = QPushButton("Move scaling &down")
        self.setSelectedAsCurrentButton = \
            QPushButton("&Set selected scaling as current")

        self.buttonsOnRightLayout = QVBoxLayout()
        self.buttonsOnRightLayout.addWidget(self.addScalingButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.removeScalingButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.editScalingButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedScalingUpButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedScalingDownButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.setSelectedAsCurrentButton)
        self.buttonsOnRightLayout.addStretch()

        self.centerAreaLayout = QVBoxLayout()
        self.centerAreaLayout.addWidget(self.selectedScalingGroupBox)
        self.centerAreaLayout.addWidget(self.currentScalingGroupBox)

        self.mainWidgetsLayout = QHBoxLayout()
        self.mainWidgetsLayout.addWidget(self.scalingsListGroupBox)
        self.mainWidgetsLayout.addLayout(self.centerAreaLayout)
        self.mainWidgetsLayout.addLayout(self.buttonsOnRightLayout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)


        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.mainWidgetsLayout) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.
        self.listWidget.itemSelectionChanged.\
            connect(self._handleScalingSelected)
        self.listWidget.itemDoubleClicked.\
            connect(self._handleEditScalingButtonClicked)
        self.addScalingButton.clicked.\
            connect(self._handleAddScalingButtonClicked)
        self.removeScalingButton.clicked.\
            connect(self._handleRemoveScalingButtonClicked)
        self.editScalingButton.clicked.\
            connect(self._handleEditScalingButtonClicked)
        self.moveSelectedScalingUpButton.clicked.\
            connect(self._handleMoveScalingUpButtonClicked)
        self.moveSelectedScalingDownButton.clicked.\
            connect(self._handleMoveScalingDownButtonClicked)
        self.setSelectedAsCurrentButton.clicked.\
            connect(self._handleSetSelectedAsCurrentButtonClicked)

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadScalings(self.priceBarChartScalings,
                          self.priceBarChartScalingsIndex)


    def loadScalings(self, 
                     priceBarChartScalings,
                     priceBarChartScalingsIndex):
        """Loads the widgets with values from the given arguments.

        Arguments:

        priceBarChartScalings - List of PriceBarChartScaling objects.
                                This is the list of scalings we are editing.

        priceBarChartScalingsIndex - int value holding the index of the
                                     currently selected scaling.  
                                     This value is an index into the
                                     priceBarChartScalings list.
        """

        self.log.debug("Entered loadScalings()")

        # Save off the values.
        self.priceBarChartScalings = list(priceBarChartScalings)
        self.priceBarChartScalingsIndex = priceBarChartScalingsIndex

        # Populate the QListWidget with the scalings.
        self.listWidget.clear()
        for scaling in self.priceBarChartScalings:
            self._appendScalingAsListWidgetItem(scaling, False)

        # Find which item to select.
        index = self.priceBarChartScalingsIndex
        if index >= 0 and index < len(self.priceBarChartScalings):
            # Valid index value.

            # Set the current index's scaling as also the one that is
            # selected in the list.
            self.listWidget.setCurrentRow(index)

            # Populate the widgets for the current.
            currentScaling = self.priceBarChartScalings[index]

            self.currentScalingNameValueLabel.\
                setText(currentScaling.name)
            self.currentScalingDescriptionTextEdit.\
                setPlainText(currentScaling.description)
            self.currentScalingUnitsOfTimeValueLabel.\
                setText("{}".format(currentScaling.getUnitsOfTime()))
            self.currentScalingUnitsOfPriceValueLabel.\
                setText("{}".format(currentScaling.getUnitsOfPrice()))
            self.currentScalingViewScalingXValueLabel.\
                setText("{}".format(currentScaling.getViewScalingX()))
            self.currentScalingViewScalingYValueLabel.\
                setText("{}".format(currentScaling.getViewScalingY()))
                        
        self.log.debug("Exiting loadScalings()")
        
    def saveScalings(self):
        """Ensures the values in the widgets are saved to their underlying
        variables, such that subsequent calls to
        getPriceBarChartScalings() and getPriceBarChartScalingsIndex()
        will return valid values for what has changed.
        """
    
        self.log.debug("Entered saveScaling()")

        # Actually, we directly change the underlying member variable
        # whenever it is modified, so no internal changes are required
        # here.

        self.log.debug("Exiting saveScaling()")

    def getPriceBarChartScalings(self):
        """Returns the internally stored list of PriceBarChartScaling
        objects.  This may or may not represent what is in the widgets,
        depending on whether or not saveScalings has been called recently.
        """

        return self.priceBarChartScalings

    def getPriceBarChartScalingsIndex(self):
        """Returns the index for the current scaling to use within the
        list of PriceBarChartScaling objects.  This may or may not
        represent what is in the widgets, depending on whether or not
        saveScalings has been called recently.
        """

        return self.priceBarChartScalingsIndex

    def _appendScalingAsListWidgetItem(self, 
                                       priceBarChartScaling, 
                                       selectItem=True):
        """Appends the given PriceBarChartScaling object to the
        QListWidget as a QListWidgetItem.

        Arguments:
        
        priceBarChartScaling - PriceBarChartScaling object who's
        information will be appended to the self.listWidget QListWidget.
        This function does not modify self.priceBarChartScalings list, so
        if this is intended, the caller needs to do that themselves
        manually.

        selectItem - bool flag that indicates whether the item should be
        selected after being created and appended to the list.
        """

        scaling = priceBarChartScaling

        listWidgetItem = QListWidgetItem()

        scalingStr = scaling.name + \
            " (dx={}, dy={}, sx={}, sy={})".\
            format(scaling.getUnitsOfTime(),
                   scaling.getUnitsOfPrice(),
                   scaling.getViewScalingX(),
                   scaling.getViewScalingY())
        listWidgetItem.setText(scalingStr)

        self.listWidget.addItem(listWidgetItem)
        
        if selectItem == True:
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)


    def _handleScalingSelected(self):
        """Called when a scaling is selected in the QListWidget.
        This will update the QLabels to tell the user the properties of
        what is selected.
        """

        # Find which item is selected.
        index = self.listWidget.currentRow()
        if index >= 0 and index < len(self.priceBarChartScalings):
            # Valid index value.

            # Set the current index's scaling as also the one that is
            # selected in the list.
            self.listWidget.setCurrentRow(index)

            # Get the scaling.
            selectedScaling = self.priceBarChartScalings[index]
            currentScaling = self.priceBarChartScalings[index]

            # Populate the widgets for the selected.
            self.selectedScalingNameValueLabel.\
                setText(selectedScaling.name)
            self.selectedScalingDescriptionTextEdit.\
                setPlainText(selectedScaling.description)
            self.selectedScalingUnitsOfTimeValueLabel.\
                setText("{}".format(selectedScaling.getUnitsOfTime()))
            self.selectedScalingUnitsOfPriceValueLabel.\
                setText("{}".format(selectedScaling.getUnitsOfPrice()))
            self.selectedScalingViewScalingXValueLabel.\
                setText("{}".format(selectedScaling.getViewScalingX()))
            self.selectedScalingViewScalingYValueLabel.\
                setText("{}".format(selectedScaling.getViewScalingY()))

    def _handleAddScalingButtonClicked(self):
        """Called when the 'Add Scaling' button is clicked."""

        # Create a new scaling object for editing.
        scaling = PriceBarChartScaling()
        
        # Create a dialog and allow the user to edit it.
        dialog = PriceBarChartScalingEditDialog(scaling)

        if dialog.exec_() == QDialog.Accepted:
            # Add the scaling object to the list.
            self.priceBarChartScalings.append(scaling)

            # Append and select the scaling object in the QListWidget.
            self._appendScalingAsListWidgetItem(scaling, True)

    def _handleRemoveScalingButtonClicked(self):
        """Called when the 'Remove Scaling' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        if row >= 0 and row < self.listWidget.count():
            # It is a valid row.

            # First remove the item from the QListWidget.
            self.listWidget.takeItem(row)

            # If there is another item after that one in the list, then
            # select that one as the current, otherwise select the index
            # before.
            if self.listWidget.item(row) != None:
                # There an item after this one, so set that one as the
                # current.
                self.listWidget.setCurrentRow(row)
            else:
                # The one we just removed was the last item in the
                # list.  Select the one before it if it exists,
                # otherwise, clear out the display fields.
                if row != 0:
                    self.listWidget.setCurrentRow(row - 1)
                else:
                    self.selectedScalingNameValueLabel.setText("")
                    self.selectedScalingDescriptionTextEdit.setPlainText("")
                    self.selectedScalingUnitsOfTimeValueLabel.setText("")
                    self.selectedScalingUnitsOfPriceValueLabel.setText("")
                    self.selectedScalingViewScalingXValueLabel.setText("")
                    self.selectedScalingViewScalingYValueLabel.setText("")

            # Do some book-keeping to remove that scaling from the
            # internal list as well.
            self.priceBarChartScalings.pop(row)

            # Update the self.priceBarChartScalingsIndex for the currently
            # applied scaling, if that index needs to be updated.

            # If the item removed was a lower index than the current
            # scaling index, then all we need to do is decrement the
            # index.  The scaling pointed to does not change.
            if self.priceBarChartScalingsIndex > row:
                self.priceBarChartScalingsIndex -= 1

            elif self.priceBarChartScalingsIndex == row:
                # This means that the row removed was what used to be the
                # current scaling to be applied.  A new one needs to be
                # chosen for the current scaling.

                # See if the 'row' index is still a valid index into the
                # list.
                if row < len(self.priceBarChartScalings):
                    # This wasn't the last item.  Keep the row number.
                    
                    # Populate the widgets for the current.
                    self.priceBarChartScalingsIndex = row
                    currentScaling = self.priceBarChartScalings[row]

                    self.currentScalingNameValueLabel.\
                        setText(currentScaling.name)
                    self.currentScalingDescriptionTextEdit.\
                        setPlainText(currentScaling.description)
                    self.currentScalingUnitsOfTimeValueLabel.\
                        setText("{}".format(currentScaling.getUnitsOfTime()))
                    self.currentScalingUnitsOfPriceValueLabel.\
                        setText("{}".format(currentScaling.getUnitsOfPrice()))
                    self.currentScalingViewScalingXValueLabel.\
                        setText("{}".format(currentScaling.getViewScalingX()))
                    self.currentScalingViewScalingYValueLabel.\
                        setText("{}".format(currentScaling.getViewScalingY()))
                                    
                else:
                    # The current scaling index was the one that was
                    # removed.  We have to use the index before this one,
                    # if it is valid.

                    if (row - 1) >= 0:
                        # This will still be valid if we choose the row
                        # before it.
                        self.priceBarChartScalingsIndex = row - 1
                    else:
                        self.priceBarChartScalingsIndex = -1

                    if self.priceBarChartScalingsIndex == -1:
                        # The user removed the last scaling in the list.
                        # Blank everything out.
                        self.currentScalingNameValueLabel.setText("")
                        self.currentScalingDescriptionTextEdit.\
                            setPlainText("")
                        self.currentScalingUnitsOfTimeValueLabel.\
                            setText("")
                        self.currentScalingUnitsOfPriceValueLabel.\
                            setText("")
                        self.currentScalingViewScalingXValueLabel.\
                            setText("")
                        self.currentScalingViewScalingYValueLabel.\
                            setText("")
                    else:
                        # Update the display fields for the new current
                        # scaling.
                        currentScaling = \
                            self.priceBarChartScalings[self.\
                                priceBarChartScalingsIndex]

                        self.currentScalingNameValueLabel.\
                            setText(currentScaling.name)
                        self.currentScalingDescriptionTextEdit.\
                            setPlainText(currentScaling.description)
                        self.currentScalingUnitsOfTimeValueLabel.\
                            setText("{}".format(currentScaling.\
                                                getUnitsOfTime()))
                        self.currentScalingUnitsOfPriceValueLabel.\
                            setText("{}".format(currentScaling.\
                                                getUnitsOfPrice()))
                        self.currentScalingViewScalingXValueLabel.\
                            setText("{}".format(currentScaling.\
                                                getViewScalingX()))
                        self.currentScalingViewScalingYValueLabel.\
                            setText("{}".format(currentScaling.\
                                                getViewScalingY()))
            else:
                # This means the current scaling index was a lower index
                # than the one that was removed.  Nothing needs to be done
                # for this case.
                pass


    def _handleEditScalingButtonClicked(self):
        """Called when the 'Edit Scaling' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Get the scaling object for editing.
        scaling = self.priceBarChartScalings[row]
        
        # Create a dialog and allow the user to edit it.
        dialog = PriceBarChartScalingEditDialog(scaling)

        if dialog.exec_() == QDialog.Accepted:
            self.priceBarChartScalings[row] = scaling

            # Get the QListWidgetItem so we can update the text of it.
            listWidgetItem = self.listWidget.item(row)
            scalingStr = scaling.name + \
                " (dx={}, dy={}, sx={}, sy={})".\
                format(scaling.getUnitsOfTime(), 
                       scaling.getUnitsOfPrice(),
                       scaling.getViewScalingX(),
                       scaling.getViewScalingY())
            listWidgetItem.setText(scalingStr)

            # If this scaling is the current one, then update the current
            # widgets as well.
            if row == self.priceBarChartScalingsIndex:
                currentScaling = self.priceBarChartScalings[row]

                # Update the widgets with the values.
                self.currentScalingNameValueLabel.\
                    setText(currentScaling.name)
                self.currentScalingDescriptionTextEdit.\
                    setPlainText(currentScaling.description)
                self.currentScalingUnitsOfTimeValueLabel.\
                    setText("{}".format(currentScaling.getUnitsOfTime()))
                self.currentScalingUnitsOfPriceValueLabel.\
                    setText("{}".format(currentScaling.getUnitsOfPrice()))
                self.currentScalingViewScalingXValueLabel.\
                    setText("{}".format(currentScaling.getViewScalingX()))
                self.currentScalingViewScalingYValueLabel.\
                    setText("{}".format(currentScaling.getViewScalingY()))
                
            # Update the widgets for this selection.
            self._handleScalingSelected()


    def _handleMoveScalingUpButtonClicked(self):
        """Called when the 'Move scaling up' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected scaling is not the top entry in the
        # QListWidget.
        if row > 0:
            # It is not the top row yet, so we can do a swap to move it
            # higher.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, currItem)

            # Swap the scalings in the list.
            scalingA = self.priceBarChartScalings[row]
            scalingB = self.priceBarChartScalings[row - 1]
            self.priceBarChartScalings[row] = scalingB
            self.priceBarChartScalings[row - 1] = scalingA

            # Update the currentScaling if required.
            if self.priceBarChartScalingsIndex == row:
                self.priceBarChartScalingsIndex -= 1
            elif self.priceBarChartScalingsIndex == row - 1:
                self.priceBarChartScalingsIndex += 1
                
            # Set the selected row as the same underlying scaling.
            self.listWidget.setCurrentRow(row - 1)

    def _handleMoveScalingDownButtonClicked(self):
        """Called when the 'Move scaling down' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected scaling is not the bottom entry in
        # the QListWidget.
        if row < (self.listWidget.count() - 1) and row >= 0:
            # It is not the bottom row yet, so we can do a swap to move it
            # lower.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, currItem)

            # Swap the scalings in the list.
            scalingA = self.priceBarChartScalings[row]
            scalingB = self.priceBarChartScalings[row + 1]
            self.priceBarChartScalings[row] = scalingB
            self.priceBarChartScalings[row + 1] = scalingA

            # Update the currentScaling if required.
            if self.priceBarChartScalingsIndex == row:
                self.priceBarChartScalingsIndex += 1
            elif self.priceBarChartScalingsIndex == row + 1:
                self.priceBarChartScalingsIndex -= 1
                
            # Set the selected row as the same underlying scaling.
            self.listWidget.setCurrentRow(row + 1)

    def _handleSetSelectedAsCurrentButtonClicked(self):
        """Called when the 'Set selected scaling as current' 
        button is clicked.
        This will update the QLabels to tell the user the properties of
        what is selected as being the currently applied scaling.
        """

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Update the index.
        self.priceBarChartScalingsIndex = row

        # Get the actual scaling.
        currentScaling = self.priceBarChartScalings[row]

        # Update the widgets with the values.
        self.currentScalingNameValueLabel.\
            setText(currentScaling.name)
        self.currentScalingDescriptionTextEdit.\
            setPlainText(currentScaling.description)
        self.currentScalingUnitsOfTimeValueLabel.\
            setText("{}".format(currentScaling.getUnitsOfTime()))
        self.currentScalingUnitsOfPriceValueLabel.\
            setText("{}".format(currentScaling.getUnitsOfPrice()))
        self.currentScalingViewScalingXValueLabel.\
            setText("{}".format(currentScaling.getViewScalingX()))
        self.currentScalingViewScalingYValueLabel.\
            setText("{}".format(currentScaling.getViewScalingY()))

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        # Check to see if there is a current scaling set.
        if self.priceBarChartScalingsIndex == -1:
            # Have a pop-up that says there must be a current scaling set.
            QMessageBox.information(None, "Whoops!",
                "There is no current scaling set!  " + \
                os.linesep + os.linesep + \
                "Please go back and make sure a scaling is set as current.")
        else:
            self.saveScalings()
            self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartScalingsListEditDialog(QDialog):
    """QDialog for editing a list of PriceBarChartScaling objects and the
    current scaling to use in the PriceBarChart.
    """

    def __init__(self, 
                 priceBarChartScalings=[],
                 priceBarChartScalingsIndex=-1, 
                 parent=None):
        """Initializes the dialog and internal widgets with the given
        values.
        
        Arguments:

        priceBarChartScalings - List of PriceBarChartScaling objects.
                                This is the list of scalings we are editing.

        priceBarChartScalingsIndex - int value holding the index of the
                                     currently selected scaling.  
                                     This value is an index into the
                                     priceBarChartScalings list.
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartScalingsListEditDialog")

        self.setWindowTitle("PriceBarChart Scaling")

        # Create the contents.
        self.priceBarChartScalingsListEditWidget = \
            PriceBarChartScalingsListEditWidget(priceBarChartScalings,
                                                priceBarChartScalingsIndex)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.priceBarChartScalingsListEditWidget)
        self.setLayout(layout)

        self.priceBarChartScalingsListEditWidget.okayButtonClicked.\
            connect(self.accept)
        self.priceBarChartScalingsListEditWidget.cancelButtonClicked.\
            connect(self.reject)

    def getPriceBarChartScalings(self):
        """Returns the internally stored list of PriceBarChartScaling
        objects.  This is only meaningful if the user has accepted the
        dialog.
        """

        return self.priceBarChartScalingsListEditWidget.\
                getPriceBarChartScalings()

    def getPriceBarChartScalingsIndex(self):
        """Returns the internally stored index to the of PriceBarChartScaling
        objects.  The index represents which scaling should be used in the
        PriceBarChart.  This is only meaningful if the user has accepted
        the dialog.
        """

        return self.priceBarChartScalingsListEditWidget.\
                getPriceBarChartScalingsIndex()


class PriceBarChartSettingsEditWidget(QWidget):
    """QWidget for editing a PriceBarChartSettings object's class members.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, priceBarChartSettings, parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartSettings object.
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartSettingsEditWidget")

        # Save off the PriceBarChartSettings object.
        self.priceBarChartSettings = priceBarChartSettings

        # QGroupBox to hold the edit widgets and form for
        # PriceBarGraphicsItem.
        self.priceBarGraphicsItemGroupBox = \
            self._buildPriceBarGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for BarCountGraphicsItem.
        self.barCountGraphicsItemGroupBox = \
            self._buildBarCountGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # TimeMeasurementGraphicsItem.
        self.timeMeasurementGraphicsItemGroupBox1 = \
            self._buildTimeMeasurementGraphicsItemGroupBox1()
        self.timeMeasurementGraphicsItemGroupBox2 = \
            self._buildTimeMeasurementGraphicsItemGroupBox2()

        # QGroupBox to hold the edit widgets and form for
        # TimeModalScaleGraphicsItem.
        self.timeModalScaleGraphicsItemGroupBox = \
            self._buildTimeModalScaleGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # PriceModalScaleGraphicsItem.
        self.priceModalScaleGraphicsItemGroupBox = \
            self._buildPriceModalScaleGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for TextGraphicsItem.
        self.textGraphicsItemGroupBox = \
            self._buildTextGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # PriceTimeInfoGraphicsItem.
        self.priceTimeInfoGraphicsItemGroupBox = \
            self._buildPriceTimeInfoGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # PriceMeasurementGraphicsItem.
        self.priceMeasurementGraphicsItemGroupBox = \
            self._buildPriceMeasurementGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # TimeRetracementGraphicsItem.
        self.timeRetracementGraphicsItemGroupBox = \
            self._buildTimeRetracementGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # PriceRetracementGraphicsItem.
        self.priceRetracementGraphicsItemGroupBox = \
            self._buildPriceRetracementGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # PriceTimeVectorGraphicsItem.
        self.priceTimeVectorGraphicsItemGroupBox = \
            self._buildPriceTimeVectorGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # LineSegmentGraphicsItem.
        self.lineSegmentGraphicsItemGroupBox = \
            self._buildLineSegmentGraphicsItemGroupBox()

        # QGroupBox to hold the edit widgets and form for
        # OctaveFanGraphicsItem.
        self.octaveFanGraphicsItemGroupBox = \
            self._buildOctaveFanGraphicsItemGroupBox()

        # Create a QTabWidget to stack all the settings editing
        # widgets.
        self.tabWidget = QTabWidget()
        
        self.tabWidget.addTab(self.priceBarGraphicsItemGroupBox,
                              QIcon(":/images/rluu/priceBar.png"),
                              "")

        self.tabWidget.addTab(self.barCountGraphicsItemGroupBox,
                              QIcon(":/images/rluu/barCount.png"),
                              "")
        
        self.tabWidget.addTab(self.timeMeasurementGraphicsItemGroupBox1,
                              QIcon(":/images/rluu/timeMeasurement.png"),
                              "(1)")
        
        self.tabWidget.addTab(self.timeMeasurementGraphicsItemGroupBox2,
                              QIcon(":/images/rluu/timeMeasurement.png"),
                              "(2)")

        self.tabWidget.addTab(self.timeModalScaleGraphicsItemGroupBox,
                              QIcon(":/images/rluu/timeModalScale.png"),
                              "")

        self.tabWidget.addTab(self.priceModalScaleGraphicsItemGroupBox,
                              QIcon(":/images/rluu/priceModalScale.png"),
                              "")

        self.tabWidget.addTab(self.textGraphicsItemGroupBox,
                              QIcon(":/images/tango-icon-theme-0.8.90/32x32/mimetypes/font-x-generic.png"),
                              "")

        self.tabWidget.addTab(self.priceTimeInfoGraphicsItemGroupBox,
                              QIcon(":/images/rluu/priceTimeInfo.png"),
                              "")

        self.tabWidget.addTab(self.priceMeasurementGraphicsItemGroupBox,
                              QIcon(":/images/rluu/priceMeasurement.png"),
                              "")

        self.tabWidget.addTab(self.timeRetracementGraphicsItemGroupBox,
                              QIcon(":/images/rluu/timeRetracement.png"),
                              "")

        self.tabWidget.addTab(self.priceRetracementGraphicsItemGroupBox,
                              QIcon(":/images/rluu/priceRetracement.png"),
                              "")

        self.tabWidget.addTab(self.priceTimeVectorGraphicsItemGroupBox,
                              QIcon(":/images/rluu/ptv.png"),
                              "")

        self.tabWidget.addTab(self.lineSegmentGraphicsItemGroupBox,
                              QIcon(":/images/rluu/lineSegment.png"),
                              "")

        self.tabWidget.addTab(self.octaveFanGraphicsItemGroupBox,
                              QIcon(":/images/rluu/octaveFan.png"),
                              "")

        # Buttons at bottom.
        self.resetAllToDefaultButton = \
            QPushButton("Reset all to original default values")
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addWidget(self.resetAllToDefaultButton)
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadValuesFromSettings(self.priceBarChartSettings)

        # Connect signals and slots.

        self.timeMeasurementGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemDefaultFontModifyButtonClicked)
        self.textGraphicsItemDefaultFontModifyButton.clicked.connect(\
            self._handleTextGraphicsItemDefaultFontModifyButtonClicked)
        self.priceTimeInfoGraphicsItemDefaultFontModifyButton.clicked.connect(\
            self._handlePriceTimeInfoGraphicsItemDefaultFontModifyButtonClicked)
        self.priceMeasurementGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemDefaultFontModifyButtonClicked)
        self.timeRetracementGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemDefaultFontModifyButtonClicked)
        self.priceRetracementGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemDefaultFontModifyButtonClicked)
        self.priceTimeVectorGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeVectorGraphicsItemDefaultFontModifyButtonClicked)
        self.lineSegmentGraphicsItemDefaultFontModifyButton.clicked.\
            connect(\
            self.\
            _handleLineSegmentGraphicsItemDefaultFontModifyButtonClicked)
        
        # Connect reset buttons.
        self.priceBarGraphicsItemPenWidthResetButton.clicked.\
            connect(self._handlePriceBarPenWidthResetButtonClicked)
        self.priceBarGraphicsItemLeftExtensionWidthResetButton.clicked.\
            connect(self._handlePriceBarLeftExtensionWidthResetButtonClicked)
        self.priceBarGraphicsItemRightExtensionWidthResetButton.clicked.\
            connect(self._handlePriceBarRightExtensionWidthResetButtonClicked)
        self.barCountGraphicsItemBarHeightResetButton.clicked.\
            connect(self._handleBarCountGraphicsItemBarHeightResetButtonClicked)
        self.barCountGraphicsItemFontSizeResetButton.clicked.\
            connect(self._handleBarCountGraphicsItemFontSizeResetButtonClicked)
        self.barCountGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self._handleBarCountGraphicsItemTextXScalingResetButtonClicked)
        self.barCountGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self._handleBarCountGraphicsItemTextYScalingResetButtonClicked)
        self.timeMeasurementGraphicsItemBarHeightResetButton.clicked.\
            connect(\
            self._handleTimeMeasurementGraphicsItemBarHeightResetButtonClicked)
        self.timeMeasurementGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemTextXScalingResetButtonClicked)
        self.timeMeasurementGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemTextYScalingResetButtonClicked)
        self.timeMeasurementGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemDefaultFontResetButtonClicked)
        self.timeMeasurementGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemDefaultTextColorResetButtonClicked)
        self.timeMeasurementGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemDefaultColorResetButtonClicked)
        self.timeMeasurementGraphicsItemGroupBox1CheckAllButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemGroupBox1CheckAllButtonClicked)
        self.timeMeasurementGraphicsItemGroupBox1UncheckAllButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemGroupBox1UncheckAllButtonClicked)
        self.timeMeasurementGraphicsItemGroupBox2CheckAllButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemGroupBox2CheckAllButtonClicked)
        self.timeMeasurementGraphicsItemGroupBox2UncheckAllButton.clicked.\
            connect(\
            self.\
            _handleTimeMeasurementGraphicsItemGroupBox2UncheckAllButtonClicked)
        self.timeModalScaleGraphicsItemColorResetButton.clicked.\
            connect(\
            self._handleTimeModalScaleGraphicsItemColorResetButtonClicked)
        self.timeModalScaleGraphicsItemTextColorResetButton.clicked.\
            connect(\
            self._handleTimeModalScaleGraphicsItemTextColorResetButtonClicked)
        self.timeModalScaleGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self._handleTimeModalScaleGraphicsItemTextXScalingResetButtonClicked)
        self.timeModalScaleGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self._handleTimeModalScaleGraphicsItemTextYScalingResetButtonClicked)
        self.timeModalScaleGraphicsItemTextEnabledFlagResetButton.clicked.\
            connect(\
            self._handleTimeModalScaleGraphicsItemTextEnabledFlagResetButtonClicked)
        self.priceModalScaleGraphicsItemColorResetButton.clicked.\
            connect(\
            self._handlePriceModalScaleGraphicsItemColorResetButtonClicked)
        self.priceModalScaleGraphicsItemTextColorResetButton.clicked.\
            connect(\
            self._handlePriceModalScaleGraphicsItemTextColorResetButtonClicked)
        self.priceModalScaleGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self._handlePriceModalScaleGraphicsItemTextXScalingResetButtonClicked)
        self.priceModalScaleGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self._handlePriceModalScaleGraphicsItemTextYScalingResetButtonClicked)
        self.priceModalScaleGraphicsItemTextEnabledFlagResetButton.clicked.\
            connect(\
            self._handlePriceModalScaleGraphicsItemTextEnabledFlagResetButtonClicked)
        self.textGraphicsItemDefaultFontResetButton.clicked.\
            connect(self._handleTextGraphicsItemDefaultFontResetButtonClicked)
        self.textGraphicsItemDefaultColorResetButton.clicked.\
            connect(self._handleTextGraphicsItemDefaultColorResetButtonClicked)
        self.textGraphicsItemDefaultXScalingResetButton.clicked.\
            connect(\
            self._handleTextGraphicsItemDefaultXScalingResetButtonClicked)
        self.textGraphicsItemDefaultYScalingResetButton.clicked.\
            connect(\
            self._handleTextGraphicsItemDefaultYScalingResetButtonClicked)
        self.priceTimeInfoGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self._handlePriceTimeInfoGraphicsItemDefaultFontResetButtonClicked)
        self.priceTimeInfoGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self._handlePriceTimeInfoGraphicsItemDefaultColorResetButtonClicked)
        self.priceTimeInfoGraphicsItemDefaultXScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeInfoGraphicsItemDefaultXScalingResetButtonClicked)
        self.priceTimeInfoGraphicsItemDefaultYScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeInfoGraphicsItemDefaultYScalingResetButtonClicked)
        self.priceMeasurementGraphicsItemBarWidthResetButton.clicked.\
            connect(\
            self._handlePriceMeasurementGraphicsItemBarWidthResetButtonClicked)
        self.priceMeasurementGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemTextXScalingResetButtonClicked)
        self.priceMeasurementGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemTextYScalingResetButtonClicked)
        self.priceMeasurementGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemDefaultFontResetButtonClicked)
        self.priceMeasurementGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemDefaultTextColorResetButtonClicked)
        self.priceMeasurementGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self.\
            _handlePriceMeasurementGraphicsItemDefaultColorResetButtonClicked)
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton.\
            clicked.connect(\
            self.\
            _handlePriceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton)
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton.\
            clicked.connect(\
            self.\
            _handlePriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton)
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton.clicked.connect(\
            self.\
            _handlePriceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton)
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton.clicked.connect(\
            self.\
            _handlePriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton)
        self.timeRetracementGraphicsItemBarHeightResetButton.clicked.\
            connect(\
            self._handleTimeRetracementGraphicsItemBarHeightResetButtonClicked)
        self.timeRetracementGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemTextXScalingResetButtonClicked)
        self.timeRetracementGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemTextYScalingResetButtonClicked)
        self.timeRetracementGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemDefaultFontResetButtonClicked)
        self.timeRetracementGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemDefaultTextColorResetButtonClicked)
        self.timeRetracementGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemDefaultColorResetButtonClicked)
        self.timeRetracementGraphicsItemShowFullLinesFlagResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemShowFullLinesFlagResetButton)
        self.timeRetracementGraphicsItemShowTimeTextFlagResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemShowTimeTextFlagResetButton)
        self.timeRetracementGraphicsItemShowPercentTextFlagResetButton.clicked.\
            connect(\
            self.\
            _handleTimeRetracementGraphicsItemShowPercentTextFlagResetButton)
        # No reset buttons are created for TimeRetracementGraphicsItem Ratios,
        # so no need to connect signals for them.


        self.priceRetracementGraphicsItemBarWidthResetButton.clicked.\
            connect(\
            self._handlePriceRetracementGraphicsItemBarWidthResetButtonClicked)
        self.priceRetracementGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemTextXScalingResetButtonClicked)
        self.priceRetracementGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemTextYScalingResetButtonClicked)
        self.priceRetracementGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemDefaultFontResetButtonClicked)
        self.priceRetracementGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemDefaultTextColorResetButtonClicked)
        self.priceRetracementGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemDefaultColorResetButtonClicked)
        self.priceRetracementGraphicsItemShowFullLinesFlagResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemShowFullLinesFlagResetButton)
        self.priceRetracementGraphicsItemShowPriceTextFlagResetButton.clicked.\
            connect(\
            self.\
            _handlePriceRetracementGraphicsItemShowPriceTextFlagResetButton)
        self.priceRetracementGraphicsItemShowPercentTextFlagResetButton.\
            clicked.connect(\
            self.\
            _handlePriceRetracementGraphicsItemShowPercentTextFlagResetButton)
        # No reset buttons are created for PriceRetracementGraphicsItem Ratios,
        # so no need to connect signals for them.

        self.priceTimeVectorGraphicsItemBarWidthResetButton.clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemBarWidthResetButtonClicked)
        self.priceTimeVectorGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeVectorGraphicsItemTextXScalingResetButtonClicked)
        self.priceTimeVectorGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeVectorGraphicsItemTextYScalingResetButtonClicked)
        self.priceTimeVectorGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handlePriceTimeVectorGraphicsItemDefaultFontResetButtonClicked)
        self.priceTimeVectorGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemDefaultColorResetButtonClicked)
        self.priceTimeVectorGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemDefaultTextColorResetButtonClicked)
        self.priceTimeVectorGraphicsItemShowDistanceTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemShowDistanceTextFlagResetButton)
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton)
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton)
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton)
        self.priceTimeVectorGraphicsItemTiltedTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemTiltedTextFlagResetButton)
        self.priceTimeVectorGraphicsItemAngleTextFlagResetButton.\
            clicked.\
            connect(\
            self._handlePriceTimeVectorGraphicsItemAngleTextFlagResetButton)
        
        self.lineSegmentGraphicsItemBarWidthResetButton.clicked.\
            connect(\
            self._handleLineSegmentGraphicsItemBarWidthResetButtonClicked)
        self.lineSegmentGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self.\
            _handleLineSegmentGraphicsItemTextXScalingResetButtonClicked)
        self.lineSegmentGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self.\
            _handleLineSegmentGraphicsItemTextYScalingResetButtonClicked)
        self.lineSegmentGraphicsItemDefaultFontResetButton.clicked.\
            connect(\
            self.\
            _handleLineSegmentGraphicsItemDefaultFontResetButtonClicked)
        self.lineSegmentGraphicsItemDefaultColorResetButton.clicked.\
            connect(\
            self._handleLineSegmentGraphicsItemDefaultColorResetButtonClicked)
        self.lineSegmentGraphicsItemDefaultTextColorResetButton.clicked.\
            connect(\
            self._handleLineSegmentGraphicsItemDefaultTextColorResetButtonClicked)
        self.lineSegmentGraphicsItemTiltedTextFlagResetButton.\
            clicked.\
            connect(\
            self._handleLineSegmentGraphicsItemTiltedTextFlagResetButton)
        self.lineSegmentGraphicsItemAngleTextFlagResetButton.\
            clicked.\
            connect(\
            self._handleLineSegmentGraphicsItemAngleTextFlagResetButton)
        
        self.octaveFanGraphicsItemColorResetButton.clicked.\
            connect(\
            self._handleOctaveFanGraphicsItemColorResetButtonClicked)
        self.octaveFanGraphicsItemTextColorResetButton.clicked.\
            connect(\
            self._handleOctaveFanGraphicsItemTextColorResetButtonClicked)
        self.octaveFanGraphicsItemTextXScalingResetButton.clicked.\
            connect(\
            self._handleOctaveFanGraphicsItemTextXScalingResetButtonClicked)
        self.octaveFanGraphicsItemTextYScalingResetButton.clicked.\
            connect(\
            self._handleOctaveFanGraphicsItemTextYScalingResetButtonClicked)
        self.octaveFanGraphicsItemTextEnabledFlagResetButton.clicked.\
            connect(\
            self._handleOctaveFanGraphicsItemTextEnabledFlagResetButtonClicked)

        self.resetAllToDefaultButton.clicked.\
            connect(self._handleResetAllToDefaultButtonClicked)

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)


    def _buildPriceBarGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceBarGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceBarGraphicsItemGroupBox = \
            QGroupBox("PriceBarGraphicsItem settings:")

        # priceBarGraphicsItemPenWidth (float).
        self.priceBarGraphicsItemPenWidthLabel = \
            QLabel("PriceBarGraphicsItem pen width:")
        self.priceBarGraphicsItemPenWidthSpinBox = QDoubleSpinBox()
        self.priceBarGraphicsItemPenWidthSpinBox.setMinimum(0.0)
        self.priceBarGraphicsItemPenWidthSpinBox.setMaximum(1000.0)
        self.priceBarGraphicsItemPenWidthResetButton = \
            QPushButton("Reset to default")

        # priceBarGraphicsItemLeftExtensionWidth (float).
        self.priceBarGraphicsItemLeftExtensionWidthLabel = \
            QLabel("PriceBarGraphicsItem left extension width:")
        self.priceBarGraphicsItemLeftExtensionWidthSpinBox = QDoubleSpinBox()
        self.priceBarGraphicsItemLeftExtensionWidthSpinBox.setMinimum(0.0)
        self.priceBarGraphicsItemLeftExtensionWidthSpinBox.setMaximum(1000.0)
        self.priceBarGraphicsItemLeftExtensionWidthResetButton = \
            QPushButton("Reset to default")

        # priceBarGraphicsItemRightExtensionWidth (float).
        self.priceBarGraphicsItemRightExtensionWidthLabel = \
            QLabel("PriceBarGraphicsItem right extension width:")
        self.priceBarGraphicsItemRightExtensionWidthSpinBox = QDoubleSpinBox()
        self.priceBarGraphicsItemRightExtensionWidthSpinBox.setMinimum(0.0)
        self.priceBarGraphicsItemRightExtensionWidthSpinBox.setMaximum(1000.0)
        self.priceBarGraphicsItemRightExtensionWidthResetButton = \
            QPushButton("Reset to default")

        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.priceBarGraphicsItemPenWidthLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceBarGraphicsItemPenWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(self.priceBarGraphicsItemPenWidthResetButton, 
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.priceBarGraphicsItemLeftExtensionWidthLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceBarGraphicsItemLeftExtensionWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(self.priceBarGraphicsItemLeftExtensionWidthResetButton, 
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.priceBarGraphicsItemRightExtensionWidthLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceBarGraphicsItemRightExtensionWidthSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.priceBarGraphicsItemRightExtensionWidthResetButton, 
             r, 2, ar)
        r += 1

        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.priceBarGraphicsItemGroupBox.setLayout(layout)

        return self.priceBarGraphicsItemGroupBox

    def _buildBarCountGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a BarCountGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.barCountGraphicsItemGroupBox = \
            QGroupBox("BarCountGraphicsItem settings:")

        # barCountGraphicsItemBarHeight (float).
        self.barCountGraphicsItemBarHeightLabel = \
            QLabel("BarCountGraphicsItem bar height: ")
        self.barCountGraphicsItemBarHeightSpinBox = QDoubleSpinBox()
        self.barCountGraphicsItemBarHeightSpinBox.setMinimum(0.0)
        self.barCountGraphicsItemBarHeightSpinBox.setMaximum(1000.0)
        self.barCountGraphicsItemBarHeightResetButton = \
            QPushButton("Reset to default")
                                             
        # barCountGraphicsItemFontSize (float).
        self.barCountGraphicsItemFontSizeLabel = \
            QLabel("BarCountGraphicsItem font size: ")
        self.barCountGraphicsItemFontSizeSpinBox = QDoubleSpinBox()
        self.barCountGraphicsItemFontSizeSpinBox.setMinimum(0.01)
        self.barCountGraphicsItemFontSizeSpinBox.setMaximum(1000.0)
        self.barCountGraphicsItemFontSizeResetButton = \
            QPushButton("Reset to default")
                                             
        # barCountGraphicsItemTextXScaling (float).
        self.barCountGraphicsItemTextXScalingLabel = \
            QLabel("BarCountGraphicsItem text X scaling: ")
        self.barCountGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.barCountGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.barCountGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.barCountGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # barCountGraphicsItemTextYScaling (float).
        self.barCountGraphicsItemTextYScalingLabel = \
            QLabel("BarCountGraphicsItem text Y scaling: ")
        self.barCountGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.barCountGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.barCountGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.barCountGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.barCountGraphicsItemBarHeightLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemBarHeightSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.barCountGraphicsItemBarHeightResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.barCountGraphicsItemFontSizeLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemFontSizeSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.barCountGraphicsItemFontSizeResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.barCountGraphicsItemTextXScalingResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.barCountGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.barCountGraphicsItemTextYScalingResetButton, 
             r, 2, ar)
        r += 1

        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.barCountGraphicsItemGroupBox.setLayout(layout)
        
        return self.barCountGraphicsItemGroupBox

    def _buildTimeMeasurementGraphicsItemGroupBox1(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a TimeMeasurementGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.timeMeasurementGraphicsItemGroupBox1 = \
            QGroupBox("TimeMeasurementGraphicsItem settings (page 1):")

        # timeMeasurementGraphicsItemBarHeight (float).
        self.timeMeasurementGraphicsItemBarHeightLabel = \
            QLabel("TimeMeasurementGraphicsItem bar height: ")
        self.timeMeasurementGraphicsItemBarHeightSpinBox = QDoubleSpinBox()
        self.timeMeasurementGraphicsItemBarHeightSpinBox.setMinimum(0.0)
        self.timeMeasurementGraphicsItemBarHeightSpinBox.setMaximum(1000.0)
        self.timeMeasurementGraphicsItemBarHeightResetButton = \
            QPushButton("Reset to default")
                                             
        # timeMeasurementGraphicsItemTextXScaling (float).
        self.timeMeasurementGraphicsItemTextXScalingLabel = \
            QLabel("TimeMeasurementGraphicsItem text X scaling: ")
        self.timeMeasurementGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.timeMeasurementGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.timeMeasurementGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.timeMeasurementGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # timeMeasurementGraphicsItemTextYScaling (float).
        self.timeMeasurementGraphicsItemTextYScalingLabel = \
            QLabel("TimeMeasurementGraphicsItem text Y scaling: ")
        self.timeMeasurementGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.timeMeasurementGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.timeMeasurementGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.timeMeasurementGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # timeMeasurementGraphicsItemDefaultFont (QFont)
        self.timeMeasurementGraphicsItemDefaultFont = QFont()
        self.timeMeasurementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTimeMeasurementGraphicsItemDefaultFontDescription)
        self.timeMeasurementGraphicsItemDefaultFontLabel = \
            QLabel("TimeMeasurementGraphicsItem default font:")
        self.timeMeasurementGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.timeMeasurementGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # timeMeasurementGraphicsItemDefaultTextColor (QColor)
        self.timeMeasurementGraphicsItemDefaultTextColorLabel = \
            QLabel("TimeMeasurementGraphicsItem default text color:")
        self.timeMeasurementGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.timeMeasurementGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # timeMeasurementGraphicsItemDefaultColor (QColor)
        self.timeMeasurementGraphicsItemDefaultColorLabel = \
            QLabel("TimeMeasurementGraphicsItem default color:")
        self.timeMeasurementGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.timeMeasurementGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")

        # Button for checkmarking all of the below checkboxes.
        self.timeMeasurementGraphicsItemGroupBox1CheckAllButton = \
            QPushButton("Check all below")
        
        # Button for un-checkmarking all of the below checkboxes.
        self.timeMeasurementGraphicsItemGroupBox1UncheckAllButton = \
            QPushButton("Uncheck all below")
        
        # timeMeasurementGraphicsItemShowBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowBarsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show bars text:")
        self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrt bars text:")
        self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrd bars text:")
        self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowHoursTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show hours text:")
        self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrt hours text:")
        self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrd hours text:")
        self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowDaysTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show days text:")
        self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrt days text:")
        self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrd days text:")
        self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowWeeksTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show weeks text:")
        self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrt weeks text:")
        self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrd weeks text:")
        self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMonthsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show months text:")
        self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrt months text:")
        self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem showSqrd months text:")
        self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowTimeRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show time range text:")
        self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show sqrt time range text:")
        self.timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show sqrd time range text:")
        self.timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show scaled value range text:")
        self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of scaled value range text:")
        self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of scaled value range text:")
        self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemBarHeightLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeMeasurementGraphicsItemBarHeightSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemBarHeightResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeMeasurementGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeMeasurementGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeMeasurementGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemGroupBox1CheckAllButton,
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemGroupBox1UncheckAllButton,
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowBarsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowHoursTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowDaysTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowWeeksTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMonthsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowTimeRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.\
            timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.\
            timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.\
            timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.\
            timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox, 
            r, 1, ar)

        groupBox1Layout = QVBoxLayout()
        groupBox1Layout.addLayout(gridLayout)
        groupBox1Layout.addStretch()
        
        self.timeMeasurementGraphicsItemGroupBox1.setLayout(groupBox1Layout)
        
        return self.timeMeasurementGraphicsItemGroupBox1
    
    def _buildTimeMeasurementGraphicsItemGroupBox2(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a TimeMeasurementGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.timeMeasurementGraphicsItemGroupBox2 = \
            QGroupBox("TimeMeasurementGraphicsItem settings (page 2):")

        # Button for checkmarking all of the below checkboxes.
        self.timeMeasurementGraphicsItemGroupBox2CheckAllButton = \
            QPushButton("Check all below")
        
        # Button for un-checkmarking all of the below checkboxes.
        self.timeMeasurementGraphicsItemGroupBox2UncheckAllButton = \
            QPushButton("Uncheck all below")
        
        # timeMeasurementGraphicsItemShowAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowAyanaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "ayana (6 months/Sun) text:")
        self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of ayana (6 months/Sun) text:")
        self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of ayana (6 months/Sun) text:")
        self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMuhurtaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "muhurta (48 minutes/Moon) text:")
        self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of muhurta (48 minutes/Moon) text:")
        self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of muhurta (48 minutes/Moon) text:")
        self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowVaraTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "vara (24-hour day/Mars) text:")
        self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of vara (24-hour day/Mars) text:")
        self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of vara (24-hour day/Mars) text:")
        self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowRtuTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "rtu (season of 2 months/Mercury) text:")
        self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of rtu (season of 2 months/Mercury) text:")
        self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of rtu (season of 2 months/Mercury) text:")
        self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMasaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "masa (lunar synodic month/Jupiter) text:")
        self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of masa (lunar synodic month/Jupiter) text:")
        self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of masa (lunar synodic month/Jupiter) text:")
        self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowPaksaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "paksa (fortnight/Venus) text:")
        self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of paksa (fortnight/Venus) text:")
        self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of paksa (fortnight/Venus) text:")
        self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSamaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sama (year/Saturn) text:")
        self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrtSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrt of sama (year/Saturn) text:")
        self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # timeMeasurementGraphicsItemShowSqrdSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagLabel = \
            QLabel("TimeMeasurementGraphicsItem show " +
                   "sqrd of sama (year/Saturn) text:")
        self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox = \
            QCheckBox()
        self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    

        checkUncheckButtonsLayout = QHBoxLayout()
        checkUncheckButtonsLayout.addStretch()
        checkUncheckButtonsLayout.addWidget(\
            self.timeMeasurementGraphicsItemGroupBox2CheckAllButton)
        checkUncheckButtonsLayout.addWidget(\
            self.timeMeasurementGraphicsItemGroupBox2UncheckAllButton)
        
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowAyanaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMuhurtaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowVaraTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowRtuTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMasaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowPaksaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSamaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox, 
            r, 1, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox, 
            r, 1, ar)


        groupBox2Layout = QVBoxLayout()
        groupBox2Layout.addLayout(checkUncheckButtonsLayout)
        groupBox2Layout.addLayout(gridLayout)
        groupBox2Layout.addStretch()
        
        self.timeMeasurementGraphicsItemGroupBox2.setLayout(groupBox2Layout)
        
        return self.timeMeasurementGraphicsItemGroupBox2
    
    def _buildTimeModalScaleGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a TimeModalScaleGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.timeModalScaleGraphicsItemGroupBox = \
            QGroupBox("TimeModalScaleGraphicsItem settings:")

        # PriceBarChart timeModalScaleGraphicsItemColor (QColor).
        self.timeModalScaleGraphicsItemColorLabel = \
            QLabel("TimeModalScaleGraphicsItem color: ")
        self.timeModalScaleGraphicsItemColorEditButton = ColorEditPushButton()
        self.timeModalScaleGraphicsItemColorResetButton = \
            QPushButton("Reset to default")
        
        # PriceBarChart timeModalScaleGraphicsItemTextColor (QColor).
        self.timeModalScaleGraphicsItemTextColorLabel = \
            QLabel("TimeModalScaleGraphicsItem text color: ")
        self.timeModalScaleGraphicsItemTextColorEditButton = \
            ColorEditPushButton()
        self.timeModalScaleGraphicsItemTextColorResetButton = \
            QPushButton("Reset to default")
        
        # timeModalScaleGraphicsItemTextXScaling (float).
        self.timeModalScaleGraphicsItemTextXScalingLabel = \
            QLabel("TimeModalScaleGraphicsItem text X scaling: ")
        self.timeModalScaleGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.timeModalScaleGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.timeModalScaleGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.timeModalScaleGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # timeModalScaleGraphicsItemTextYScaling (float).
        self.timeModalScaleGraphicsItemTextYScalingLabel = \
            QLabel("TimeModalScaleGraphicsItem text Y scaling: ")
        self.timeModalScaleGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.timeModalScaleGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.timeModalScaleGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.timeModalScaleGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # timeModalScaleGraphicsItemTextEnabledFlag (bool).
        self.timeModalScaleGraphicsItemTextEnabledFlagLabel = \
            QLabel("TimeModalScaleGraphicsItem text is enabled: ")
        self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox = \
            QCheckBox()
        self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.timeModalScaleGraphicsItemTextEnabledFlagResetButton = \
            QPushButton("Reset to default")
        
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeModalScaleGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeModalScaleGraphicsItemTextYScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextEnabledFlagLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeModalScaleGraphicsItemTextEnabledFlagResetButton, 
            r, 2, ar)

        r += 1


        self.timeModalScaleGraphicsItemRotateDownButton = \
            QPushButton("Rotate Down")
        self.timeModalScaleGraphicsItemRotateUpButton = \
            QPushButton("Rotate Up")
        self.timeModalScaleGraphicsItemCheckMarkAllButton = \
            QPushButton("Check All")
        self.timeModalScaleGraphicsItemCheckMarkNoneButton = \
            QPushButton("Check None")
        self.timeModalScaleGraphicsItemMusicalRatiosResetButton = \
            QPushButton("Reset to default")
        
        rotateButtonsLayout = QHBoxLayout()
        rotateButtonsLayout.addWidget(\
            self.timeModalScaleGraphicsItemRotateDownButton)
        rotateButtonsLayout.addWidget(\
            self.timeModalScaleGraphicsItemRotateUpButton)
        rotateButtonsLayout.addWidget(\
            self.timeModalScaleGraphicsItemCheckMarkAllButton)
        rotateButtonsLayout.addWidget(\
            self.timeModalScaleGraphicsItemCheckMarkNoneButton)
        rotateButtonsLayout.addWidget(\
            self.timeModalScaleGraphicsItemMusicalRatiosResetButton)
        rotateButtonsLayout.addStretch()
        
        # Layout for the musical ratio intervals.
        self.timeModalScaleGraphicsItemMusicalRatiosGridLayout = QGridLayout()

        # Holds a list of MusicalRatio objects that is the 'working
        # copy' in this edit widget.  This gets saved to the
        # underlying self.priceBarChartSettings object upon clicking okay.
        self.timeModalScaleGraphicsItemMusicalRatios = list()
        
        # Holds the list of QCheckBox objects corresponding to the
        # MusicalRatios (ordered) in the artifact. 
        self.timeModalScaleGraphicsItemCheckBoxes = []
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addLayout(rotateButtonsLayout)
        layout.addLayout(\
            self.timeModalScaleGraphicsItemMusicalRatiosGridLayout)
        layout.addStretch()
        
        self.timeModalScaleGraphicsItemGroupBox.setLayout(layout)

        # Connect signals and slots.
        self.timeModalScaleGraphicsItemRotateDownButton.clicked.connect(\
            self._handleTimeModalScaleGraphicsItemRotateDownButtonClicked)
        self.timeModalScaleGraphicsItemRotateUpButton.clicked.connect(\
            self._handleTimeModalScaleGraphicsItemRotateUpButtonClicked)
        self.timeModalScaleGraphicsItemCheckMarkAllButton.clicked.connect(\
            self._handleTimeModalScaleGraphicsItemCheckMarkAllButtonClicked)
        self.timeModalScaleGraphicsItemCheckMarkNoneButton.clicked.connect(\
            self._handleTimeModalScaleGraphicsItemCheckMarkNoneButtonClicked)
        self.timeModalScaleGraphicsItemMusicalRatiosResetButton.clicked.\
            connect(\
            self.\
            _handleTimeModalScaleGraphicsItemMusicalRatiosResetButtonClicked)

        
        return self.timeModalScaleGraphicsItemGroupBox

    def _buildPriceModalScaleGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceModalScaleGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceModalScaleGraphicsItemGroupBox = \
            QGroupBox("PriceModalScaleGraphicsItem settings:")

        # PriceBarChart priceModalScaleGraphicsItemColor (QColor).
        self.priceModalScaleGraphicsItemColorLabel = \
            QLabel("PriceModalScaleGraphicsItem color: ")
        self.priceModalScaleGraphicsItemColorEditButton = ColorEditPushButton()
        self.priceModalScaleGraphicsItemColorResetButton = \
            QPushButton("Reset to default")
        
        # PriceBarChart priceModalScaleGraphicsItemTextColor (QColor).
        self.priceModalScaleGraphicsItemTextColorLabel = \
            QLabel("PriceModalScaleGraphicsItem text color: ")
        self.priceModalScaleGraphicsItemTextColorEditButton = \
            ColorEditPushButton()
        self.priceModalScaleGraphicsItemTextColorResetButton = \
            QPushButton("Reset to default")
        
        # priceModalScaleGraphicsItemTextXScaling (float).
        self.priceModalScaleGraphicsItemTextXScalingLabel = \
            QLabel("PriceModalScaleGraphicsItem text X scaling: ")
        self.priceModalScaleGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.priceModalScaleGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.priceModalScaleGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.priceModalScaleGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceModalScaleGraphicsItemTextYScaling (float).
        self.priceModalScaleGraphicsItemTextYScalingLabel = \
            QLabel("PriceModalScaleGraphicsItem text Y scaling: ")
        self.priceModalScaleGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.priceModalScaleGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.priceModalScaleGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.priceModalScaleGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceModalScaleGraphicsItemTextEnabledFlag (bool).
        self.priceModalScaleGraphicsItemTextEnabledFlagLabel = \
            QLabel("PriceModalScaleGraphicsItem text is enabled: ")
        self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox = \
            QCheckBox()
        self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceModalScaleGraphicsItemTextEnabledFlagResetButton = \
            QPushButton("Reset to default")
        
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceModalScaleGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceModalScaleGraphicsItemTextYScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextEnabledFlagLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceModalScaleGraphicsItemTextEnabledFlagResetButton, 
            r, 2, ar)

        r += 1


        self.priceModalScaleGraphicsItemRotateDownButton = \
            QPushButton("Rotate Down")
        self.priceModalScaleGraphicsItemRotateUpButton = \
            QPushButton("Rotate Up")
        self.priceModalScaleGraphicsItemCheckMarkAllButton = \
            QPushButton("Check All")
        self.priceModalScaleGraphicsItemCheckMarkNoneButton = \
            QPushButton("Check None")
        self.priceModalScaleGraphicsItemMusicalRatiosResetButton = \
            QPushButton("Reset to default")
        
        rotateButtonsLayout = QHBoxLayout()
        rotateButtonsLayout.addWidget(\
            self.priceModalScaleGraphicsItemRotateDownButton)
        rotateButtonsLayout.addWidget(\
            self.priceModalScaleGraphicsItemRotateUpButton)
        rotateButtonsLayout.addWidget(\
            self.priceModalScaleGraphicsItemCheckMarkAllButton)
        rotateButtonsLayout.addWidget(\
            self.priceModalScaleGraphicsItemCheckMarkNoneButton)
        rotateButtonsLayout.addWidget(\
            self.priceModalScaleGraphicsItemMusicalRatiosResetButton)
        rotateButtonsLayout.addStretch()
        
        # Layout for the musical ratio intervals.
        self.priceModalScaleGraphicsItemMusicalRatiosGridLayout = QGridLayout()

        # Holds a list of MusicalRatio objects that is the 'working
        # copy' in this edit widget.  This gets saved to the
        # underlying self.priceBarChartSettings object upon clicking okay.
        self.priceModalScaleGraphicsItemMusicalRatios = list()
        
        # Holds the list of QCheckBox objects corresponding to the
        # MusicalRatios (ordered) in the artifact. 
        self.priceModalScaleGraphicsItemCheckBoxes = []
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addLayout(rotateButtonsLayout)
        layout.addLayout(\
            self.priceModalScaleGraphicsItemMusicalRatiosGridLayout)
        layout.addStretch()
        
        self.priceModalScaleGraphicsItemGroupBox.setLayout(layout)

        # Connect signals and slots.
        self.priceModalScaleGraphicsItemRotateDownButton.clicked.connect(\
            self._handlePriceModalScaleGraphicsItemRotateDownButtonClicked)
        self.priceModalScaleGraphicsItemRotateUpButton.clicked.connect(\
            self._handlePriceModalScaleGraphicsItemRotateUpButtonClicked)
        self.priceModalScaleGraphicsItemCheckMarkAllButton.clicked.connect(\
            self._handlePriceModalScaleGraphicsItemCheckMarkAllButtonClicked)
        self.priceModalScaleGraphicsItemCheckMarkNoneButton.clicked.connect(\
            self._handlePriceModalScaleGraphicsItemCheckMarkNoneButtonClicked)
        self.priceModalScaleGraphicsItemMusicalRatiosResetButton.clicked.\
            connect(\
            self.\
            _handlePriceModalScaleGraphicsItemMusicalRatiosResetButtonClicked)

        
        return self.priceModalScaleGraphicsItemGroupBox

    def _buildTextGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a TextGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.textGraphicsItemGroupBox = \
            QGroupBox("TextGraphicsItem settings:")

        # textGraphicsItemDefaultFont (QFont)
        self.textGraphicsItemDefaultFont = QFont()
        self.textGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTextGraphicsItemDefaultFontDescription)
        self.textGraphicsItemDefaultFontLabel = \
            QLabel("TextGraphicsItem default font:")
        self.textGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.textGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # textGraphicsItemDefaultColor (QColor)
        self.textGraphicsItemDefaultColorLabel = \
            QLabel("TextGraphicsItem default color:")
        self.textGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.textGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # textGraphicsItemDefaultXScaling (float).
        self.textGraphicsItemDefaultXScalingLabel = \
            QLabel("TextGraphicsItem default X scaling: ")
        self.textGraphicsItemDefaultXScalingSpinBox = QDoubleSpinBox()
        self.textGraphicsItemDefaultXScalingSpinBox.setMinimum(0.0001)
        self.textGraphicsItemDefaultXScalingSpinBox.setMaximum(1000.0)
        self.textGraphicsItemDefaultXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # textGraphicsItemDefaultYScaling (float).
        self.textGraphicsItemDefaultYScalingLabel = \
            QLabel("TextGraphicsItem default Y scaling: ")
        self.textGraphicsItemDefaultYScalingSpinBox = QDoubleSpinBox()
        self.textGraphicsItemDefaultYScalingSpinBox.setMinimum(0.0001)
        self.textGraphicsItemDefaultYScalingSpinBox.setMaximum(1000.0)
        self.textGraphicsItemDefaultYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.textGraphicsItemDefaultFontLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.textGraphicsItemDefaultFontResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultColorLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultColorEditButton, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.textGraphicsItemDefaultColorResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.textGraphicsItemDefaultXScalingResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.textGraphicsItemDefaultYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.textGraphicsItemDefaultYScalingResetButton, 
             r, 2, ar)
        r += 1

        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.textGraphicsItemGroupBox.setLayout(layout)
        
        return self.textGraphicsItemGroupBox
    
    def _buildPriceTimeInfoGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceTimeInfoGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceTimeInfoGraphicsItemGroupBox = \
            QGroupBox("PriceTimeInfoGraphicsItem settings:")

        # priceTimeInfoGraphicsItemDefaultFont (QFont)
        self.priceTimeInfoGraphicsItemDefaultFont = QFont()
        self.priceTimeInfoGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceTimeInfoGraphicsItemDefaultFontDescription)
        self.priceTimeInfoGraphicsItemDefaultFontLabel = \
            QLabel("PriceTimeInfoGraphicsItem default font:")
        self.priceTimeInfoGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.priceTimeInfoGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # priceTimeInfoGraphicsItemDefaultColor (QColor)
        self.priceTimeInfoGraphicsItemDefaultColorLabel = \
            QLabel("PriceTimeInfoGraphicsItem default color:")
        self.priceTimeInfoGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.priceTimeInfoGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # priceTimeInfoGraphicsItemDefaultXScaling (float).
        self.priceTimeInfoGraphicsItemDefaultXScalingLabel = \
            QLabel("PriceTimeInfoGraphicsItem default X scaling: ")
        self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox = QDoubleSpinBox()
        self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox.setMinimum(0.0001)
        self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox.setMaximum(1000.0)
        self.priceTimeInfoGraphicsItemDefaultXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceTimeInfoGraphicsItemDefaultYScaling (float).
        self.priceTimeInfoGraphicsItemDefaultYScalingLabel = \
            QLabel("PriceTimeInfoGraphicsItem default Y scaling: ")
        self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox = QDoubleSpinBox()
        self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox.setMinimum(0.0001)
        self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox.setMaximum(1000.0)
        self.priceTimeInfoGraphicsItemDefaultYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceTimeInfoGraphicsItemShowTimestampFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimestampFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show timestamp:")
        self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowPriceFlag (bool).
        self.priceTimeInfoGraphicsItemShowPriceFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show price:")
        self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtPriceFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtPriceFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show sqrt(price):")
        self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show time-elapsed-since-birth:")
        self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem " +
                   "show sqrt(time-elapsed-since-birth):")
        self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Unchecked)

        # priceTimeInfoGraphicsItemShowPriceScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show price scaled value:")
        self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        
        # priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show sqrt price scaled value:")
        self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        
        # priceTimeInfoGraphicsItemShowTimeScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show time scaled value:")
        self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        
        # priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show sqrt time scaled value:")
        self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        
        # priceTimeInfoGraphicsItemShowLineToInfoPointFlag (bool).
        self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagLabel = \
            QLabel("PriceTimeInfoGraphicsItem show line to InfoPoint:")
        self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox = \
            QCheckBox()
        self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultFontLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.priceTimeInfoGraphicsItemDefaultFontResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultColorLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultColorEditButton, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.priceTimeInfoGraphicsItemDefaultColorResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.priceTimeInfoGraphicsItemDefaultXScalingResetButton, 
             r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.addWidget\
            (self.priceTimeInfoGraphicsItemDefaultYScalingResetButton, 
             r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemShowTimestampFlagLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox, 
                      r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemShowPriceFlagLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox, 
                      r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtPriceFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox, 
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox,
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox, 
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox, 
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox,
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox,
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagLabel,
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox,
            r, 1, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox, 
            r, 1, ar)
        

        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.priceTimeInfoGraphicsItemGroupBox.setLayout(layout)

        return self.priceTimeInfoGraphicsItemGroupBox

    def _buildPriceMeasurementGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceMeasurementGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceMeasurementGraphicsItemGroupBox = \
            QGroupBox("PriceMeasurementGraphicsItem settings:")

        # priceMeasurementGraphicsItemBarWidth (float).
        self.priceMeasurementGraphicsItemBarWidthLabel = \
            QLabel("PriceMeasurementGraphicsItem bar width: ")
        self.priceMeasurementGraphicsItemBarWidthSpinBox = QDoubleSpinBox()
        self.priceMeasurementGraphicsItemBarWidthSpinBox.setMinimum(0.0)
        self.priceMeasurementGraphicsItemBarWidthSpinBox.setMaximum(1000.0)
        self.priceMeasurementGraphicsItemBarWidthResetButton = \
            QPushButton("Reset to default")
                                             
        # priceMeasurementGraphicsItemTextXScaling (float).
        self.priceMeasurementGraphicsItemTextXScalingLabel = \
            QLabel("PriceMeasurementGraphicsItem text X scaling: ")
        self.priceMeasurementGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.priceMeasurementGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.priceMeasurementGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.priceMeasurementGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceMeasurementGraphicsItemTextYScaling (float).
        self.priceMeasurementGraphicsItemTextYScalingLabel = \
            QLabel("PriceMeasurementGraphicsItem text Y scaling: ")
        self.priceMeasurementGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.priceMeasurementGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.priceMeasurementGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.priceMeasurementGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # priceMeasurementGraphicsItemDefaultFont (QFont)
        self.priceMeasurementGraphicsItemDefaultFont = QFont()
        self.priceMeasurementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceMeasurementGraphicsItemDefaultFontDescription)
        self.priceMeasurementGraphicsItemDefaultFontLabel = \
            QLabel("PriceMeasurementGraphicsItem default font:")
        self.priceMeasurementGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.priceMeasurementGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # priceMeasurementGraphicsItemDefaultTextColor (QColor)
        self.priceMeasurementGraphicsItemDefaultTextColorLabel = \
            QLabel("PriceMeasurementGraphicsItem default text color:")
        self.priceMeasurementGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.priceMeasurementGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # priceMeasurementGraphicsItemDefaultColor (QColor)
        self.priceMeasurementGraphicsItemDefaultColorLabel = \
            QLabel("PriceMeasurementGraphicsItem default color:")
        self.priceMeasurementGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.priceMeasurementGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # priceMeasurementGraphicsItemShowPriceRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlagLabel = \
            QLabel("PriceMeasurementGraphicsItem show price range text:")
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox = \
            QCheckBox()
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagLabel = \
            QLabel("PriceMeasurementGraphicsItem show sqrt price range text:")
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox = \
            QCheckBox()
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagLabel = \
            QLabel("PriceMeasurementGraphicsItem show scaled value range text:")
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox = QCheckBox()
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton = QPushButton("Reset to default")
    
        # priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagLabel = \
            QLabel("PriceMeasurementGraphicsItem show " +
                   "sqrt of scaled value range text:")
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox = QCheckBox()
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton = QPushButton("Reset to default")
    
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemBarWidthLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceMeasurementGraphicsItemBarWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemBarWidthResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceMeasurementGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceMeasurementGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceMeasurementGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.\
            priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.\
            priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.\
            priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton, 
            r, 2, ar)

        r += 1
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.priceMeasurementGraphicsItemGroupBox.setLayout(layout)
        
        return self.priceMeasurementGraphicsItemGroupBox
    
    def _buildTimeRetracementGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a TimeRetracementGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.timeRetracementGraphicsItemGroupBox = \
            QGroupBox("TimeRetracementGraphicsItem settings:")

        # timeRetracementGraphicsItemBarHeight (float).
        self.timeRetracementGraphicsItemBarHeightLabel = \
            QLabel("TimeRetracementGraphicsItem bar height: ")
        self.timeRetracementGraphicsItemBarHeightSpinBox = QDoubleSpinBox()
        self.timeRetracementGraphicsItemBarHeightSpinBox.setMinimum(0.0)
        self.timeRetracementGraphicsItemBarHeightSpinBox.setMaximum(1000.0)
        self.timeRetracementGraphicsItemBarHeightResetButton = \
            QPushButton("Reset to default")
                                             
        # timeRetracementGraphicsItemTextXScaling (float).
        self.timeRetracementGraphicsItemTextXScalingLabel = \
            QLabel("TimeRetracementGraphicsItem text X scaling: ")
        self.timeRetracementGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.timeRetracementGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.timeRetracementGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.timeRetracementGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # timeRetracementGraphicsItemTextYScaling (float).
        self.timeRetracementGraphicsItemTextYScalingLabel = \
            QLabel("TimeRetracementGraphicsItem text Y scaling: ")
        self.timeRetracementGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.timeRetracementGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.timeRetracementGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.timeRetracementGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # timeRetracementGraphicsItemDefaultFont (QFont)
        self.timeRetracementGraphicsItemDefaultFont = QFont()
        self.timeRetracementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTimeRetracementGraphicsItemDefaultFontDescription)
        self.timeRetracementGraphicsItemDefaultFontLabel = \
            QLabel("TimeRetracementGraphicsItem default font:")
        self.timeRetracementGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.timeRetracementGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # timeRetracementGraphicsItemDefaultTextColor (QColor)
        self.timeRetracementGraphicsItemDefaultTextColorLabel = \
            QLabel("TimeRetracementGraphicsItem default text color:")
        self.timeRetracementGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.timeRetracementGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # timeRetracementGraphicsItemDefaultColor (QColor)
        self.timeRetracementGraphicsItemDefaultColorLabel = \
            QLabel("TimeRetracementGraphicsItem default color:")
        self.timeRetracementGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.timeRetracementGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # timeRetracementGraphicsItemShowFullLinesFlag (bool).
        self.timeRetracementGraphicsItemShowFullLinesFlagLabel = \
            QLabel("TimeRetracementGraphicsItem show full lines:")
        self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox = \
            QCheckBox()
        self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.timeRetracementGraphicsItemShowFullLinesFlagResetButton = \
            QPushButton("Reset to default")
    
        # timeRetracementGraphicsItemShowTimeTextFlag (bool).
        self.timeRetracementGraphicsItemShowTimeTextFlagLabel = \
            QLabel("TimeRetracementGraphicsItem show time text:")
        self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox = \
            QCheckBox()
        self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.timeRetracementGraphicsItemShowTimeTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # timeRetracementGraphicsItemShowPercentTextFlag (bool).
        self.timeRetracementGraphicsItemShowPercentTextFlagLabel = \
            QLabel("TimeRetracementGraphicsItem show percent text:")
        self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox = \
            QCheckBox()
        self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.timeRetracementGraphicsItemShowPercentTextFlagResetButton = \
            QPushButton("Reset to default")

        # TimeRetracement Ratios.
        # There are no reset buttons for the ratios, just labels and checkboxes.
        self.timeRetracementGraphicsItemRatioLabels = []
        self.timeRetracementGraphicsItemRatioCheckBoxes = []
        
        for ratio in \
            self.priceBarChartSettings.timeRetracementGraphicsItemRatios:

            label = QLabel("TimeRetracementGraphicsItem ratio " +
                           ratio.getDescription() + " enabled:")
            checkBox = QCheckBox()

            self.timeRetracementGraphicsItemRatioLabels.append(label)
            self.timeRetracementGraphicsItemRatioCheckBoxes.append(checkBox)
        

        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemBarHeightLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeRetracementGraphicsItemBarHeightSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemBarHeightResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeRetracementGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeRetracementGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.timeRetracementGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowFullLinesFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowFullLinesFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowTimeTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowTimeTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowPercentTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.timeRetracementGraphicsItemShowPercentTextFlagResetButton, 
            r, 2, ar)

        r += 1
        for i in range(len(self.priceBarChartSettings.\
                           timeRetracementGraphicsItemRatios)):
            gridLayout.\
                addWidget(\
                self.timeRetracementGraphicsItemRatioLabels[i], 
                r, 0, al)
            gridLayout.\
                addWidget(\
                self.timeRetracementGraphicsItemRatioCheckBoxes[i],
                r, 1, ar)
            r += 1

        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.timeRetracementGraphicsItemGroupBox.setLayout(layout)
        
        return self.timeRetracementGraphicsItemGroupBox
    
    def _buildPriceRetracementGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceRetracementGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceRetracementGraphicsItemGroupBox = \
            QGroupBox("PriceRetracementGraphicsItem settings:")

        # priceRetracementGraphicsItemBarWidth (float).
        self.priceRetracementGraphicsItemBarWidthLabel = \
            QLabel("PriceRetracementGraphicsItem bar width: ")
        self.priceRetracementGraphicsItemBarWidthSpinBox = QDoubleSpinBox()
        self.priceRetracementGraphicsItemBarWidthSpinBox.setMinimum(0.0)
        self.priceRetracementGraphicsItemBarWidthSpinBox.setMaximum(1000.0)
        self.priceRetracementGraphicsItemBarWidthResetButton = \
            QPushButton("Reset to default")
                                             
        # priceRetracementGraphicsItemTextXScaling (float).
        self.priceRetracementGraphicsItemTextXScalingLabel = \
            QLabel("PriceRetracementGraphicsItem text X scaling: ")
        self.priceRetracementGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.priceRetracementGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.priceRetracementGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.priceRetracementGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceRetracementGraphicsItemTextYScaling (float).
        self.priceRetracementGraphicsItemTextYScalingLabel = \
            QLabel("PriceRetracementGraphicsItem text Y scaling: ")
        self.priceRetracementGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.priceRetracementGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.priceRetracementGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.priceRetracementGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # priceRetracementGraphicsItemDefaultFont (QFont)
        self.priceRetracementGraphicsItemDefaultFont = QFont()
        self.priceRetracementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceRetracementGraphicsItemDefaultFontDescription)
        self.priceRetracementGraphicsItemDefaultFontLabel = \
            QLabel("PriceRetracementGraphicsItem default font:")
        self.priceRetracementGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.priceRetracementGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # priceRetracementGraphicsItemDefaultTextColor (QColor)
        self.priceRetracementGraphicsItemDefaultTextColorLabel = \
            QLabel("PriceRetracementGraphicsItem default text color:")
        self.priceRetracementGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.priceRetracementGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # priceRetracementGraphicsItemDefaultColor (QColor)
        self.priceRetracementGraphicsItemDefaultColorLabel = \
            QLabel("PriceRetracementGraphicsItem default color:")
        self.priceRetracementGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.priceRetracementGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # priceRetracementGraphicsItemShowFullLinesFlag (bool).
        self.priceRetracementGraphicsItemShowFullLinesFlagLabel = \
            QLabel("PriceRetracementGraphicsItem show full lines:")
        self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox = \
            QCheckBox()
        self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceRetracementGraphicsItemShowFullLinesFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceRetracementGraphicsItemShowPriceTextFlag (bool).
        self.priceRetracementGraphicsItemShowPriceTextFlagLabel = \
            QLabel("PriceRetracementGraphicsItem show price text:")
        self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox = \
            QCheckBox()
        self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceRetracementGraphicsItemShowPriceTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceRetracementGraphicsItemShowPercentTextFlag (bool).
        self.priceRetracementGraphicsItemShowPercentTextFlagLabel = \
            QLabel("PriceRetracementGraphicsItem show percent text:")
        self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox = \
            QCheckBox()
        self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceRetracementGraphicsItemShowPercentTextFlagResetButton = \
            QPushButton("Reset to default")

        # PriceRetracement Ratios.
        # There are no reset buttons for the ratios, just labels and checkboxes.
        self.priceRetracementGraphicsItemRatioLabels = []
        self.priceRetracementGraphicsItemRatioCheckBoxes = []
        
        for ratio in \
            self.priceBarChartSettings.priceRetracementGraphicsItemRatios:

            label = QLabel("PriceRetracementGraphicsItem ratio " +
                           ratio.getDescription() + " enabled:")
            checkBox = QCheckBox()

            self.priceRetracementGraphicsItemRatioLabels.append(label)
            self.priceRetracementGraphicsItemRatioCheckBoxes.append(checkBox)
        

        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemBarWidthLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceRetracementGraphicsItemBarWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemBarWidthResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceRetracementGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceRetracementGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceRetracementGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowFullLinesFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowFullLinesFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPriceTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPriceTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPercentTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceRetracementGraphicsItemShowPercentTextFlagResetButton, 
            r, 2, ar)

        r += 1
        for i in range(len(self.priceBarChartSettings.\
                           priceRetracementGraphicsItemRatios)):
            gridLayout.\
                addWidget(\
                self.priceRetracementGraphicsItemRatioLabels[i], 
                r, 0, al)
            gridLayout.\
                addWidget(\
                self.priceRetracementGraphicsItemRatioCheckBoxes[i],
                r, 1, ar)
            r += 1

        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.priceRetracementGraphicsItemGroupBox.setLayout(layout)
        
        return self.priceRetracementGraphicsItemGroupBox
    
    def _buildPriceTimeVectorGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a PriceTimeVectorGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.priceTimeVectorGraphicsItemGroupBox = \
            QGroupBox("PriceTimeVectorGraphicsItem settings:")

        # priceTimeVectorGraphicsItemBarWidth (float).
        self.priceTimeVectorGraphicsItemBarWidthLabel = \
            QLabel("PriceTimeVectorGraphicsItem bar width: ")
        self.priceTimeVectorGraphicsItemBarWidthSpinBox = QDoubleSpinBox()
        self.priceTimeVectorGraphicsItemBarWidthSpinBox.setMinimum(0.0)
        self.priceTimeVectorGraphicsItemBarWidthSpinBox.setMaximum(1000.0)
        self.priceTimeVectorGraphicsItemBarWidthResetButton = \
            QPushButton("Reset to default")
                                             
        # priceTimeVectorGraphicsItemTextXScaling (float).
        self.priceTimeVectorGraphicsItemTextXScalingLabel = \
            QLabel("PriceTimeVectorGraphicsItem text X scaling: ")
        self.priceTimeVectorGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.priceTimeVectorGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.priceTimeVectorGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.priceTimeVectorGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # priceTimeVectorGraphicsItemTextYScaling (float).
        self.priceTimeVectorGraphicsItemTextYScalingLabel = \
            QLabel("PriceTimeVectorGraphicsItem text Y scaling: ")
        self.priceTimeVectorGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.priceTimeVectorGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.priceTimeVectorGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.priceTimeVectorGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # priceTimeVectorGraphicsItemDefaultFont (QFont)
        self.priceTimeVectorGraphicsItemDefaultFont = QFont()
        self.priceTimeVectorGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceTimeVectorGraphicsItemDefaultFontDescription)
        self.priceTimeVectorGraphicsItemDefaultFontLabel = \
            QLabel("PriceTimeVectorGraphicsItem default font:")
        self.priceTimeVectorGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.priceTimeVectorGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # priceTimeVectorGraphicsItemDefaultTextColor (QColor)
        self.priceTimeVectorGraphicsItemDefaultTextColorLabel = \
            QLabel("PriceTimeVectorGraphicsItem default text color:")
        self.priceTimeVectorGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.priceTimeVectorGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # priceTimeVectorGraphicsItemDefaultColor (QColor)
        self.priceTimeVectorGraphicsItemDefaultColorLabel = \
            QLabel("PriceTimeVectorGraphicsItem default color:")
        self.priceTimeVectorGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.priceTimeVectorGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # priceTimeVectorGraphicsItemShowDistanceTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowDistanceTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem show distance text:")
        self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemShowDistanceTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem show sqrt distance text:")
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem show distance text:")
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem show sqrt distance text:")
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton = \
            QPushButton("Reset to default")
    
        # priceTimeVectorGraphicsItemTiltedTextFlag (bool).
        self.priceTimeVectorGraphicsItemTiltedTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem tilted text:")
        self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemTiltedTextFlagResetButton = \
            QPushButton("Reset to default")

        # priceTimeVectorGraphicsItemAngleTextFlag (bool).
        self.priceTimeVectorGraphicsItemAngleTextFlagLabel = \
            QLabel("PriceTimeVectorGraphicsItem angle text:")
        self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox = \
            QCheckBox()
        self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.priceTimeVectorGraphicsItemAngleTextFlagResetButton = \
            QPushButton("Reset to default")

        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemBarWidthLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeVectorGraphicsItemBarWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemBarWidthResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeVectorGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeVectorGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.priceTimeVectorGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTiltedTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemTiltedTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemAngleTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.priceTimeVectorGraphicsItemAngleTextFlagResetButton, 
            r, 2, ar)

        r += 1
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.priceTimeVectorGraphicsItemGroupBox.setLayout(layout)
        
        return self.priceTimeVectorGraphicsItemGroupBox
    
    def _buildLineSegmentGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a LineSegmentGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.lineSegmentGraphicsItemGroupBox = \
            QGroupBox("LineSegmentGraphicsItem settings:")

        # lineSegmentGraphicsItemBarWidth (float).
        self.lineSegmentGraphicsItemBarWidthLabel = \
            QLabel("LineSegmentGraphicsItem bar width: ")
        self.lineSegmentGraphicsItemBarWidthSpinBox = QDoubleSpinBox()
        self.lineSegmentGraphicsItemBarWidthSpinBox.setMinimum(0.0)
        self.lineSegmentGraphicsItemBarWidthSpinBox.setMaximum(1000.0)
        self.lineSegmentGraphicsItemBarWidthResetButton = \
            QPushButton("Reset to default")
                                             
        # lineSegmentGraphicsItemTextXScaling (float).
        self.lineSegmentGraphicsItemTextXScalingLabel = \
            QLabel("LineSegmentGraphicsItem text X scaling: ")
        self.lineSegmentGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.lineSegmentGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.lineSegmentGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.lineSegmentGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # lineSegmentGraphicsItemTextYScaling (float).
        self.lineSegmentGraphicsItemTextYScalingLabel = \
            QLabel("LineSegmentGraphicsItem text Y scaling: ")
        self.lineSegmentGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.lineSegmentGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.lineSegmentGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.lineSegmentGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")

        # lineSegmentGraphicsItemDefaultFont (QFont)
        self.lineSegmentGraphicsItemDefaultFont = QFont()
        self.lineSegmentGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultLineSegmentGraphicsItemDefaultFontDescription)
        self.lineSegmentGraphicsItemDefaultFontLabel = \
            QLabel("LineSegmentGraphicsItem default font:")
        self.lineSegmentGraphicsItemDefaultFontModifyButton = \
            QPushButton("Modify")
        self.lineSegmentGraphicsItemDefaultFontResetButton = \
            QPushButton("Reset to default")
        
        # lineSegmentGraphicsItemDefaultTextColor (QColor)
        self.lineSegmentGraphicsItemDefaultTextColorLabel = \
            QLabel("LineSegmentGraphicsItem default text color:")
        self.lineSegmentGraphicsItemDefaultTextColorEditButton = \
            ColorEditPushButton()
        self.lineSegmentGraphicsItemDefaultTextColorResetButton = \
            QPushButton("Reset to default")
        
        # lineSegmentGraphicsItemDefaultColor (QColor)
        self.lineSegmentGraphicsItemDefaultColorLabel = \
            QLabel("LineSegmentGraphicsItem default color:")
        self.lineSegmentGraphicsItemDefaultColorEditButton = \
            ColorEditPushButton()
        self.lineSegmentGraphicsItemDefaultColorResetButton = \
            QPushButton("Reset to default")
        
        # lineSegmentGraphicsItemTiltedTextFlag (bool).
        self.lineSegmentGraphicsItemTiltedTextFlagLabel = \
            QLabel("LineSegmentGraphicsItem tilted text:")
        self.lineSegmentGraphicsItemTiltedTextFlagCheckBox = \
            QCheckBox()
        self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.lineSegmentGraphicsItemTiltedTextFlagResetButton = \
            QPushButton("Reset to default")

        # lineSegmentGraphicsItemAngleTextFlag (bool).
        self.lineSegmentGraphicsItemAngleTextFlagLabel = \
            QLabel("LineSegmentGraphicsItem angle text:")
        self.lineSegmentGraphicsItemAngleTextFlagCheckBox = \
            QCheckBox()
        self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.lineSegmentGraphicsItemAngleTextFlagResetButton = \
            QPushButton("Reset to default")

        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemBarWidthLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.lineSegmentGraphicsItemBarWidthSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemBarWidthResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTextXScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.lineSegmentGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTextYScalingLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.lineSegmentGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTextYScalingResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultFontLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(self.lineSegmentGraphicsItemDefaultFontModifyButton, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultFontResetButton, 
            r, 2, ar)
        
        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultTextColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultTextColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultTextColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultColorLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultColorEditButton, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemDefaultColorResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTiltedTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTiltedTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemTiltedTextFlagResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemAngleTextFlagLabel, 
            r, 0, al)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemAngleTextFlagCheckBox, 
            r, 1, ar)
        gridLayout.\
            addWidget(\
            self.lineSegmentGraphicsItemAngleTextFlagResetButton, 
            r, 2, ar)

        r += 1
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addStretch()
        
        self.lineSegmentGraphicsItemGroupBox.setLayout(layout)
        
        return self.lineSegmentGraphicsItemGroupBox
    
    def _buildOctaveFanGraphicsItemGroupBox(self):
        """Builds the groupbox containing info to edit the
        PriceBarChartSettings related to a OctaveFanGraphicsItem.

        Returns:
        QGroupBox obj containing all the created widgets.
        """

        self.octaveFanGraphicsItemGroupBox = \
            QGroupBox("OctaveFanGraphicsItem settings:")

        # PriceBarChart octaveFanGraphicsItemColor (QColor).
        self.octaveFanGraphicsItemColorLabel = \
            QLabel("OctaveFanGraphicsItem color: ")
        self.octaveFanGraphicsItemColorEditButton = ColorEditPushButton()
        self.octaveFanGraphicsItemColorResetButton = \
            QPushButton("Reset to default")
        
        # PriceBarChart octaveFanGraphicsItemTextColor (QColor).
        self.octaveFanGraphicsItemTextColorLabel = \
            QLabel("OctaveFanGraphicsItem text color: ")
        self.octaveFanGraphicsItemTextColorEditButton = \
            ColorEditPushButton()
        self.octaveFanGraphicsItemTextColorResetButton = \
            QPushButton("Reset to default")
        
        # octaveFanGraphicsItemTextXScaling (float).
        self.octaveFanGraphicsItemTextXScalingLabel = \
            QLabel("OctaveFanGraphicsItem text X scaling: ")
        self.octaveFanGraphicsItemTextXScalingSpinBox = QDoubleSpinBox()
        self.octaveFanGraphicsItemTextXScalingSpinBox.setMinimum(0.0001)
        self.octaveFanGraphicsItemTextXScalingSpinBox.setMaximum(1000.0)
        self.octaveFanGraphicsItemTextXScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # octaveFanGraphicsItemTextYScaling (float).
        self.octaveFanGraphicsItemTextYScalingLabel = \
            QLabel("OctaveFanGraphicsItem text Y scaling: ")
        self.octaveFanGraphicsItemTextYScalingSpinBox = QDoubleSpinBox()
        self.octaveFanGraphicsItemTextYScalingSpinBox.setMinimum(0.0001)
        self.octaveFanGraphicsItemTextYScalingSpinBox.setMaximum(1000.0)
        self.octaveFanGraphicsItemTextYScalingResetButton = \
            QPushButton("Reset to default")
                                             
        # octaveFanGraphicsItemTextEnabledFlag (bool).
        self.octaveFanGraphicsItemTextEnabledFlagLabel = \
            QLabel("OctaveFanGraphicsItem text is enabled: ")
        self.octaveFanGraphicsItemTextEnabledFlagCheckBox = \
            QCheckBox()
        self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
            setCheckState(Qt.Unchecked)
        self.octaveFanGraphicsItemTextEnabledFlagResetButton = \
            QPushButton("Reset to default")
        
        # Grid layout.
        gridLayout = QGridLayout()
        r = 0
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        gridLayout.\
            addWidget(self.octaveFanGraphicsItemColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextColorLabel,
                      r, 0, al)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextColorEditButton,
                      r, 1, ar)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextColorResetButton,
                      r, 2, ar)
        r += 1
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextXScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextXScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.octaveFanGraphicsItemTextXScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextYScalingLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextYScalingSpinBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.octaveFanGraphicsItemTextYScalingResetButton, 
            r, 2, ar)

        r += 1
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextEnabledFlagLabel, 
                      r, 0, al)
        gridLayout.\
            addWidget(self.octaveFanGraphicsItemTextEnabledFlagCheckBox, 
                      r, 1, ar)
        gridLayout.\
            addWidget(\
            self.octaveFanGraphicsItemTextEnabledFlagResetButton, 
            r, 2, ar)

        r += 1


        self.octaveFanGraphicsItemRotateDownButton = \
            QPushButton("Rotate Down")
        self.octaveFanGraphicsItemRotateUpButton = \
            QPushButton("Rotate Up")
        self.octaveFanGraphicsItemCheckMarkAllButton = \
            QPushButton("Check All")
        self.octaveFanGraphicsItemCheckMarkNoneButton = \
            QPushButton("Check None")
        self.octaveFanGraphicsItemMusicalRatiosResetButton = \
            QPushButton("Reset to default")
        
        rotateButtonsLayout = QHBoxLayout()
        rotateButtonsLayout.addWidget(\
            self.octaveFanGraphicsItemRotateDownButton)
        rotateButtonsLayout.addWidget(\
            self.octaveFanGraphicsItemRotateUpButton)
        rotateButtonsLayout.addWidget(\
            self.octaveFanGraphicsItemCheckMarkAllButton)
        rotateButtonsLayout.addWidget(\
            self.octaveFanGraphicsItemCheckMarkNoneButton)
        rotateButtonsLayout.addWidget(\
            self.octaveFanGraphicsItemMusicalRatiosResetButton)
        rotateButtonsLayout.addStretch()
        
        # Layout for the musical ratio intervals.
        self.octaveFanGraphicsItemMusicalRatiosGridLayout = QGridLayout()

        # Holds a list of MusicalRatio objects that is the 'working
        # copy' in this edit widget.  This gets saved to the
        # underlying self.priceBarChartSettings object upon clicking okay.
        self.octaveFanGraphicsItemMusicalRatios = list()
        
        # Holds the list of QCheckBox objects corresponding to the
        # MusicalRatios (ordered) in the artifact. 
        self.octaveFanGraphicsItemCheckBoxes = []
        
        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addLayout(rotateButtonsLayout)
        layout.addLayout(\
            self.octaveFanGraphicsItemMusicalRatiosGridLayout)
        layout.addStretch()
        
        self.octaveFanGraphicsItemGroupBox.setLayout(layout)

        # Connect signals and slots.
        self.octaveFanGraphicsItemRotateDownButton.clicked.connect(\
            self._handleOctaveFanGraphicsItemRotateDownButtonClicked)
        self.octaveFanGraphicsItemRotateUpButton.clicked.connect(\
            self._handleOctaveFanGraphicsItemRotateUpButtonClicked)
        self.octaveFanGraphicsItemCheckMarkAllButton.clicked.connect(\
            self._handleOctaveFanGraphicsItemCheckMarkAllButtonClicked)
        self.octaveFanGraphicsItemCheckMarkNoneButton.clicked.connect(\
            self._handleOctaveFanGraphicsItemCheckMarkNoneButtonClicked)
        self.octaveFanGraphicsItemMusicalRatiosResetButton.clicked.\
            connect(\
            self.\
            _handleOctaveFanGraphicsItemMusicalRatiosResetButtonClicked)

        
        return self.octaveFanGraphicsItemGroupBox

    def loadValuesFromSettings(self, priceBarChartSettings):
        """Loads the widgets with values from the given
        PriceBarChartSettings object.
        """

        self.log.debug("Entered loadValuesFromSettings()")

        # Check inputs.
        if priceBarChartSettings == None:
            self.log.error("Invalid parameter to " + \
                           "loadValuesFromSettings().  " + \
                           "priceBarChartSettings can't be None.")
            self.log.debug("Exiting loadValuesFromSettings()")
            return
        else:
            self.priceBarChartSettings = priceBarChartSettings 


        # priceBarGraphicsItemPenWidth (float).
        self.priceBarGraphicsItemPenWidthSpinBox.\
            setValue(self.priceBarChartSettings.priceBarGraphicsItemPenWidth)

        # priceBarGraphicsItemLeftExtensionWidth (float).
        self.priceBarGraphicsItemLeftExtensionWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceBarGraphicsItemLeftExtensionWidth)

        # priceBarGraphicsItemRightExtensionWidth (float).
        self.priceBarGraphicsItemRightExtensionWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceBarGraphicsItemRightExtensionWidth)

        # barCountGraphicsItemBarHeight (float).
        self.barCountGraphicsItemBarHeightSpinBox.\
            setValue(self.priceBarChartSettings.\
                        barCountGraphicsItemBarHeight)

        # barCountGraphicsItemFontSize (float).
        self.barCountGraphicsItemFontSizeSpinBox.\
            setValue(self.priceBarChartSettings.\
                        barCountGraphicsItemFontSize)

        # barCountGraphicsItemTextXScaling (float).
        self.barCountGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        barCountGraphicsItemTextXScaling)

        # barCountGraphicsItemTextYScaling (float).
        self.barCountGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        barCountGraphicsItemTextYScaling)

        # timeMeasurementGraphicsItemBarHeight (float).
        self.timeMeasurementGraphicsItemBarHeightSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeMeasurementGraphicsItemBarHeight)

        # timeMeasurementGraphicsItemTextXScaling (float).
        self.timeMeasurementGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeMeasurementGraphicsItemTextXScaling)

        # timeMeasurementGraphicsItemTextYScaling (float).
        self.timeMeasurementGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeMeasurementGraphicsItemTextYScaling)

        # timeMeasurementGraphicsItemDefaultFontDescription (str)
        self.timeMeasurementGraphicsItemDefaultFont = QFont()
        self.timeMeasurementGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       timeMeasurementGraphicsItemDefaultFontDescription)

        # timeMeasurementGraphicsItemDefaultTextColor (QColor).
        self.timeMeasurementGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeMeasurementGraphicsItemDefaultTextColor)

        # timeMeasurementGraphicsItemDefaultColor (QColor).
        self.timeMeasurementGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeMeasurementGraphicsItemDefaultColor)

        # timeMeasurementGraphicsItemShowBarsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowBarsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtBarsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtBarsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdBarsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdBarsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowHoursTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowHoursTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtHoursTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtHoursTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdHoursTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdHoursTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowDaysTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowDaysTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtDaysTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtDaysTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdDaysTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdDaysTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowWeeksTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowWeeksTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtWeeksTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtWeeksTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdWeeksTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdWeeksTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowMonthsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowMonthsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtMonthsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtMonthsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdMonthsTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdMonthsTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowTimeRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowTimeRangeTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag == True:
            
            self.\
                timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.\
                timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag == True:
            
            self.\
                timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.\
                timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowScaledValueRangeTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowAyanaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowAyanaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtAyanaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtAyanaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdAyanaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdAyanaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowMuhurtaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowMuhurtaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowVaraTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowVaraTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtVaraTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtVaraTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdVaraTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdVaraTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowRtuTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowRtuTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtRtuTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtRtuTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdRtuTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdRtuTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowMasaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowMasaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtMasaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtMasaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdMasaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdMasaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowPaksaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowPaksaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtPaksaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtPaksaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdPaksaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdPaksaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSamaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSamaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrtSamaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrtSamaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeMeasurementGraphicsItemShowSqrdSamaTextFlag (bool).
        if self.priceBarChartSettings.\
           timeMeasurementGraphicsItemShowSqrdSamaTextFlag == True:
            
            self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeModalScaleGraphicsItemColor (QColor).
        self.timeModalScaleGraphicsItemColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeModalScaleGraphicsItemBarColor)

        # timeModalScaleGraphicsItemTextColor (QColor).
        self.timeModalScaleGraphicsItemTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeModalScaleGraphicsItemTextColor)

        # timeModalScaleGraphicsItemTextXScaling (float).
        self.timeModalScaleGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeModalScaleGraphicsItemTextXScaling)

        # timeModalScaleGraphicsItemTextYScaling (float).
        self.timeModalScaleGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeModalScaleGraphicsItemTextYScaling)

        # timeModalScaleGraphicsItemTextEnabledFlag (bool).
        if self.priceBarChartSettings.\
           timeModalScaleGraphicsItemTextEnabledFlag == True:

            self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeModalScaleGraphicsItemMusicalRatios (list of MusicalRatio)
        self.timeModalScaleGraphicsItemMusicalRatios = \
            copy.deepcopy(self.priceBarChartSettings.\
                          timeModalScaleGraphicsItemMusicalRatios)
        self._timeModalScaleGraphicsItemReloadMusicalRatiosGrid(\
            self.timeModalScaleGraphicsItemMusicalRatios)
        
        # priceModalScaleGraphicsItemColor (QColor).
        self.priceModalScaleGraphicsItemColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceModalScaleGraphicsItemBarColor)

        # priceModalScaleGraphicsItemTextColor (QColor).
        self.priceModalScaleGraphicsItemTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceModalScaleGraphicsItemTextColor)

        # priceModalScaleGraphicsItemTextXScaling (float).
        self.priceModalScaleGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceModalScaleGraphicsItemTextXScaling)

        # priceModalScaleGraphicsItemTextYScaling (float).
        self.priceModalScaleGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceModalScaleGraphicsItemTextYScaling)

        # priceModalScaleGraphicsItemTextEnabledFlag (bool).
        if self.priceBarChartSettings.\
           priceModalScaleGraphicsItemTextEnabledFlag == True:

            self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)
        
        # priceModalScaleGraphicsItemMusicalRatios (list of MusicalRatio)
        self.priceModalScaleGraphicsItemMusicalRatios = \
            copy.deepcopy(self.priceBarChartSettings.\
                          priceModalScaleGraphicsItemMusicalRatios)
        self._priceModalScaleGraphicsItemReloadMusicalRatiosGrid(\
            self.priceModalScaleGraphicsItemMusicalRatios)
        
        # textGraphicsItemDefaultFont (QFont)
        self.textGraphicsItemDefaultFont = QFont()
        self.textGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       textGraphicsItemDefaultFontDescription)
        
        # textGraphicsItemDefaultColor (QColor)
        self.textGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     textGraphicsItemDefaultColor)
        
        # textGraphicsItemDefaultXScaling (float).
        self.textGraphicsItemDefaultXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                     textGraphicsItemDefaultXScaling)
        
        # textGraphicsItemDefaultYScaling (float).
        self.textGraphicsItemDefaultYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                     textGraphicsItemDefaultYScaling)
        
        # priceTimeInfoGraphicsItemDefaultFont (QFont)
        self.priceTimeInfoGraphicsItemDefaultFont = QFont()
        self.priceTimeInfoGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       priceTimeInfoGraphicsItemDefaultFontDescription)
        
        # priceTimeInfoGraphicsItemDefaultColor (QColor)
        self.priceTimeInfoGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceTimeInfoGraphicsItemDefaultColor)
        
        # priceTimeInfoGraphicsItemDefaultXScaling (float).
        self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                     priceTimeInfoGraphicsItemDefaultXScaling)
        
        # priceTimeInfoGraphicsItemDefaultYScaling (float).
        self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                     priceTimeInfoGraphicsItemDefaultYScaling)

        # priceTimeInfoGraphicsItemShowTimestampFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowTimestampFlag == True:

            self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox.\
                setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowPriceFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowPriceFlag == True:

            self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox.\
                setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtPriceFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowSqrtPriceFlag == True:

            self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox.\
                setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag == True:

            self.\
            priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag == True:
            
            self.\
            priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox.\
            setCheckState(Qt.Unchecked)

        # priceTimeInfoGraphicsItemShowPriceScaledValueFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowPriceScaledValueFlag == True:
            
            self.\
            priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag == True:
            
            self.\
            priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowTimeScaledValueFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowTimeScaledValueFlag == True:
            
            self.\
            priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag == True:
            
            self.\
            priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Checked)
        else:
            self.\
            priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox.\
            setCheckState(Qt.Unchecked)
    
        # priceTimeInfoGraphicsItemShowLineToInfoPointFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeInfoGraphicsItemShowLineToInfoPointFlag == True:

            self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceMeasurementGraphicsItemBarWidth (float).
        self.priceMeasurementGraphicsItemBarWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceMeasurementGraphicsItemDefaultBarWidth)

        # priceMeasurementGraphicsItemTextXScaling (float).
        self.priceMeasurementGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceMeasurementGraphicsItemDefaultTextXScaling)

        # priceMeasurementGraphicsItemTextYScaling (float).
        self.priceMeasurementGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceMeasurementGraphicsItemDefaultTextYScaling)

        # priceMeasurementGraphicsItemDefaultFontDescription (str)
        self.priceMeasurementGraphicsItemDefaultFont = QFont()
        self.priceMeasurementGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       priceMeasurementGraphicsItemDefaultFontDescription)

        # priceMeasurementGraphicsItemDefaultTextColor (QColor).
        self.priceMeasurementGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceMeasurementGraphicsItemDefaultTextColor)

        # priceMeasurementGraphicsItemDefaultColor (QColor).
        self.priceMeasurementGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceMeasurementGraphicsItemDefaultColor)

        # priceMeasurementGraphicsItemShowPriceRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           priceMeasurementGraphicsItemShowPriceRangeTextFlag == True:
            
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag == True:
            
            self.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           priceMeasurementGraphicsItemShowScaledValueRangeTextFlag == True:
            
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        if self.priceBarChartSettings.\
           priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag == True:
            
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeRetracementGraphicsItemBarHeight (float).
        self.timeRetracementGraphicsItemBarHeightSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeRetracementGraphicsItemBarHeight)

        # timeRetracementGraphicsItemTextXScaling (float).
        self.timeRetracementGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeRetracementGraphicsItemTextXScaling)

        # timeRetracementGraphicsItemTextYScaling (float).
        self.timeRetracementGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        timeRetracementGraphicsItemTextYScaling)

        # timeRetracementGraphicsItemDefaultFontDescription (str)
        self.timeRetracementGraphicsItemDefaultFont = QFont()
        self.timeRetracementGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       timeRetracementGraphicsItemDefaultFontDescription)

        # timeRetracementGraphicsItemDefaultTextColor (QColor).
        self.timeRetracementGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeRetracementGraphicsItemDefaultTextColor)

        # timeRetracementGraphicsItemDefaultColor (QColor).
        self.timeRetracementGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     timeRetracementGraphicsItemDefaultColor)

        # timeRetracementGraphicsItemShowFullLinesFlag (bool).
        if self.priceBarChartSettings.\
           timeRetracementGraphicsItemShowFullLinesFlag == True:
            
            self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeRetracementGraphicsItemShowTimeTextFlag (bool).
        if self.priceBarChartSettings.\
           timeRetracementGraphicsItemShowTimeTextFlag == True:
            
            self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # timeRetracementGraphicsItemShowPercentTextFlag (bool).
        if self.priceBarChartSettings.\
           timeRetracementGraphicsItemShowPercentTextFlag == True:
            
            self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # TimeRetracement Ratios.
        for i in range(len(self.priceBarChartSettings.\
                           timeRetracementGraphicsItemRatios)):
            # Check the checkbox if the ratio is enabled.
            ratio = \
                self.priceBarChartSettings.timeRetracementGraphicsItemRatios[i]

            if ratio.isEnabled():
                self.timeRetracementGraphicsItemRatioCheckBoxes[i].\
                    setCheckState(Qt.Checked)
            else:
                self.timeRetracementGraphicsItemRatioCheckBoxes[i].\
                    setCheckState(Qt.Unchecked)
        
        # priceRetracementGraphicsItemBarWidth (float).
        self.priceRetracementGraphicsItemBarWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceRetracementGraphicsItemBarWidth)

        # priceRetracementGraphicsItemTextXScaling (float).
        self.priceRetracementGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceRetracementGraphicsItemTextXScaling)

        # priceRetracementGraphicsItemTextYScaling (float).
        self.priceRetracementGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceRetracementGraphicsItemTextYScaling)

        # priceRetracementGraphicsItemDefaultFontDescription (str)
        self.priceRetracementGraphicsItemDefaultFont = QFont()
        self.priceRetracementGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       priceRetracementGraphicsItemDefaultFontDescription)

        # priceRetracementGraphicsItemDefaultTextColor (QColor).
        self.priceRetracementGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceRetracementGraphicsItemDefaultTextColor)

        # priceRetracementGraphicsItemDefaultColor (QColor).
        self.priceRetracementGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceRetracementGraphicsItemDefaultColor)

        # priceRetracementGraphicsItemShowFullLinesFlag (bool).
        if self.priceBarChartSettings.\
           priceRetracementGraphicsItemShowFullLinesFlag == True:
            
            self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceRetracementGraphicsItemShowPriceTextFlag (bool).
        if self.priceBarChartSettings.\
           priceRetracementGraphicsItemShowPriceTextFlag == True:
            
            self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceRetracementGraphicsItemShowPercentTextFlag (bool).
        if self.priceBarChartSettings.\
           priceRetracementGraphicsItemShowPercentTextFlag == True:
            
            self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # PriceRetracement Ratios.
        for i in range(len(self.priceBarChartSettings.\
                           priceRetracementGraphicsItemRatios)):
            # Check the checkbox if the ratio is enabled.
            ratio = \
                self.priceBarChartSettings.priceRetracementGraphicsItemRatios[i]

            if ratio.isEnabled():
                self.priceRetracementGraphicsItemRatioCheckBoxes[i].\
                    setCheckState(Qt.Checked)
            else:
                self.priceRetracementGraphicsItemRatioCheckBoxes[i].\
                    setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemBarWidth (float).
        self.priceTimeVectorGraphicsItemBarWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceTimeVectorGraphicsItemBarWidth)

        # priceTimeVectorGraphicsItemTextXScaling (float).
        self.priceTimeVectorGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceTimeVectorGraphicsItemTextXScaling)

        # priceTimeVectorGraphicsItemTextYScaling (float).
        self.priceTimeVectorGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        priceTimeVectorGraphicsItemTextYScaling)

        # priceTimeVectorGraphicsItemDefaultFontDescription (str)
        self.priceTimeVectorGraphicsItemDefaultFont = QFont()
        self.priceTimeVectorGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       priceTimeVectorGraphicsItemDefaultFontDescription)

        # priceTimeVectorGraphicsItemTextColor (QColor).
        self.priceTimeVectorGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceTimeVectorGraphicsItemTextColor)

        # priceTimeVectorGraphicsItemColor (QColor).
        self.priceTimeVectorGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     priceTimeVectorGraphicsItemColor)

        # priceTimeVectorGraphicsItemShowDistanceTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemShowDistanceTextFlag == True:
            
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag == True:
            
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag == True:
            
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag == True:
            
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemTiltedTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemTiltedTextFlag == True:
            
            self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # priceTimeVectorGraphicsItemAngleTextFlag (bool).
        if self.priceBarChartSettings.\
           priceTimeVectorGraphicsItemAngleTextFlag == True:
            
            self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # lineSegmentGraphicsItemBarWidth (float).
        self.lineSegmentGraphicsItemBarWidthSpinBox.\
            setValue(self.priceBarChartSettings.\
                        lineSegmentGraphicsItemBarWidth)

        # lineSegmentGraphicsItemTextXScaling (float).
        self.lineSegmentGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        lineSegmentGraphicsItemTextXScaling)

        # lineSegmentGraphicsItemTextYScaling (float).
        self.lineSegmentGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        lineSegmentGraphicsItemTextYScaling)

        # lineSegmentGraphicsItemDefaultFontDescription (str)
        self.lineSegmentGraphicsItemDefaultFont = QFont()
        self.lineSegmentGraphicsItemDefaultFont.\
            fromString(self.priceBarChartSettings.\
                       lineSegmentGraphicsItemDefaultFontDescription)

        # lineSegmentGraphicsItemTextColor (QColor).
        self.lineSegmentGraphicsItemDefaultTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     lineSegmentGraphicsItemTextColor)

        # lineSegmentGraphicsItemColor (QColor).
        self.lineSegmentGraphicsItemDefaultColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     lineSegmentGraphicsItemColor)

        # lineSegmentGraphicsItemTiltedTextFlag (bool).
        if self.priceBarChartSettings.\
           lineSegmentGraphicsItemTiltedTextFlag == True:
            
            self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # lineSegmentGraphicsItemAngleTextFlag (bool).
        if self.priceBarChartSettings.\
           lineSegmentGraphicsItemAngleTextFlag == True:
            
            self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # octaveFanGraphicsItemColor (QColor).
        self.octaveFanGraphicsItemColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     octaveFanGraphicsItemBarColor)

        # octaveFanGraphicsItemTextColor (QColor).
        self.octaveFanGraphicsItemTextColorEditButton.\
            setColor(self.priceBarChartSettings.\
                     octaveFanGraphicsItemTextColor)

        # octaveFanGraphicsItemTextXScaling (float).
        self.octaveFanGraphicsItemTextXScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        octaveFanGraphicsItemTextXScaling)

        # octaveFanGraphicsItemTextYScaling (float).
        self.octaveFanGraphicsItemTextYScalingSpinBox.\
            setValue(self.priceBarChartSettings.\
                        octaveFanGraphicsItemTextYScaling)

        # octaveFanGraphicsItemTextEnabledFlag (bool).
        if self.priceBarChartSettings.\
           octaveFanGraphicsItemTextEnabledFlag == True:

            self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)

        # octaveFanGraphicsItemMusicalRatios (list of MusicalRatio)
        self.octaveFanGraphicsItemMusicalRatios = \
            copy.deepcopy(self.priceBarChartSettings.\
                          octaveFanGraphicsItemMusicalRatios)
        self._octaveFanGraphicsItemReloadMusicalRatiosGrid(\
            self.octaveFanGraphicsItemMusicalRatios)
        
        self.log.debug("Exiting loadValuesFromSettings()")
        
    def saveValuesToSettings(self):
        """Saves the values in the widgets to the 
        PriceBarChartSettings object passed in this class's constructor.
        """
    
        self.log.debug("Entered saveValuesToSettings()")

        # priceBarGraphicsItemPenWidth (float).
        self.priceBarChartSettings.priceBarGraphicsItemPenWidth = \
            float(self.priceBarGraphicsItemPenWidthSpinBox.value())

        # priceBarGraphicsItemLeftExtensionWidth (float).
        self.priceBarChartSettings.priceBarGraphicsItemLeftExtensionWidth = \
            float(self.priceBarGraphicsItemLeftExtensionWidthSpinBox.value())
       
        # priceBarGraphicsItemRightExtensionWidth (float).
        self.priceBarChartSettings.priceBarGraphicsItemRightExtensionWidth = \
            float(self.priceBarGraphicsItemRightExtensionWidthSpinBox.value())

        # barCountGraphicsItemBarHeight (float).
        self.priceBarChartSettings.barCountGraphicsItemBarHeight = \
            float(self.barCountGraphicsItemBarHeightSpinBox.value())

        # barCountGraphicsItemFontSize (float).
        self.priceBarChartSettings.barCountGraphicsItemFontSize = \
            float(self.barCountGraphicsItemFontSizeSpinBox.value())

        # barCountGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.barCountGraphicsItemTextXScaling = \
            float(self.barCountGraphicsItemTextXScalingSpinBox.value())

        # barCountGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.barCountGraphicsItemTextYScaling = \
            float(self.barCountGraphicsItemTextYScalingSpinBox.value())

        # timeMeasurementGraphicsItemBarHeight (float).
        self.priceBarChartSettings.timeMeasurementGraphicsItemBarHeight = \
            float(self.timeMeasurementGraphicsItemBarHeightSpinBox.value())

        # timeMeasurementGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.timeMeasurementGraphicsItemTextXScaling = \
            float(self.timeMeasurementGraphicsItemTextXScalingSpinBox.value())

        # timeMeasurementGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.timeMeasurementGraphicsItemTextYScaling = \
            float(self.timeMeasurementGraphicsItemTextYScalingSpinBox.value())

        # timeMeasurementGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultFontDescription = \
            self.timeMeasurementGraphicsItemDefaultFont.toString()

        # timeMeasurementGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultTextColor = \
            self.timeMeasurementGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # timeMeasurementGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultColor = \
            self.timeMeasurementGraphicsItemDefaultColorEditButton.\
            getColor()

        # timeMeasurementGraphicsItemShowBarsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowBarsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowBarsTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtBarsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtBarsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtBarsTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdBarsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdBarsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdBarsTextFlag = False

        # timeMeasurementGraphicsItemShowHoursTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowHoursTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowHoursTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtHoursTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtHoursTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtHoursTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdHoursTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdHoursTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdHoursTextFlag = False

        # timeMeasurementGraphicsItemShowDaysTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowDaysTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowDaysTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtDaysTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtDaysTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtDaysTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdDaysTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdDaysTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdDaysTextFlag = False

        # timeMeasurementGraphicsItemShowWeeksTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowWeeksTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowWeeksTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtWeeksTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtWeeksTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtWeeksTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdWeeksTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdWeeksTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdWeeksTextFlag = False

        # timeMeasurementGraphicsItemShowMonthsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMonthsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMonthsTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtMonthsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMonthsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMonthsTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdMonthsTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMonthsTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMonthsTextFlag = False

        # timeMeasurementGraphicsItemShowTimeRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowTimeRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowTimeRangeTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag = False

        # timeMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowScaledValueRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowScaledValueRangeTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag = False

        # timeMeasurementGraphicsItemShowAyanaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowAyanaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowAyanaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtAyanaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtAyanaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtAyanaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdAyanaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdAyanaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdAyanaTextFlag = False

        # timeMeasurementGraphicsItemShowMuhurtaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMuhurtaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMuhurtaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag = False

        # timeMeasurementGraphicsItemShowVaraTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowVaraTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowVaraTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtVaraTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtVaraTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtVaraTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdVaraTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdVaraTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdVaraTextFlag = False

        # timeMeasurementGraphicsItemShowRtuTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowRtuTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowRtuTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtRtuTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtRtuTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtRtuTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdRtuTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdRtuTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdRtuTextFlag = False

        # timeMeasurementGraphicsItemShowMasaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMasaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowMasaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtMasaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMasaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtMasaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdMasaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMasaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdMasaTextFlag = False

        # timeMeasurementGraphicsItemShowPaksaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowPaksaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowPaksaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtPaksaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtPaksaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtPaksaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdPaksaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdPaksaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdPaksaTextFlag = False

        # timeMeasurementGraphicsItemShowSamaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSamaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSamaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrtSamaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtSamaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrtSamaTextFlag = False

        # timeMeasurementGraphicsItemShowSqrdSamaTextFlag (bool).
        if self.timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdSamaTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeMeasurementGraphicsItemShowSqrdSamaTextFlag = False

        # timeModalScaleGraphicsItemTextColor (QColor).
        self.priceBarChartSettings.timeModalScaleGraphicsItemBarColor = \
            self.timeModalScaleGraphicsItemColorEditButton.getColor()

        # timeModalScaleGraphicsItemTextTextColor (QColor).
        self.priceBarChartSettings.timeModalScaleGraphicsItemTextColor = \
            self.timeModalScaleGraphicsItemTextColorEditButton.getColor()
            
        # timeModalScaleGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.timeModalScaleGraphicsItemTextXScaling = \
            float(self.timeModalScaleGraphicsItemTextXScalingSpinBox.value())

        # timeModalScaleGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.timeModalScaleGraphicsItemTextYScaling = \
            float(self.timeModalScaleGraphicsItemTextYScalingSpinBox.value())
        
        # timeModalScaleGraphicsItemTextEnabledFlag (bool).
        if self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
           checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                timeModalScaleGraphicsItemTextEnabledFlag = True
        else:
            self.priceBarChartSettings.\
                timeModalScaleGraphicsItemTextEnabledFlag = False
        
        # timeModalScaleGraphicsItemMusicalRatios (list of MusicalRatio)
        self.priceBarChartSettings.timeModalScaleGraphicsItemMusicalRatios = \
            self.timeModalScaleGraphicsItemMusicalRatios
           
        # priceModalScaleGraphicsItemTextColor (QColor).
        self.priceBarChartSettings.priceModalScaleGraphicsItemBarColor = \
            self.priceModalScaleGraphicsItemColorEditButton.getColor()

        # priceModalScaleGraphicsItemTextTextColor (QColor).
        self.priceBarChartSettings.priceModalScaleGraphicsItemTextColor = \
            self.priceModalScaleGraphicsItemTextColorEditButton.getColor()
            
        # priceModalScaleGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.priceModalScaleGraphicsItemTextXScaling = \
            float(self.priceModalScaleGraphicsItemTextXScalingSpinBox.value())

        # priceModalScaleGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.priceModalScaleGraphicsItemTextYScaling = \
            float(self.priceModalScaleGraphicsItemTextYScalingSpinBox.value())
        
        # priceModalScaleGraphicsItemTextEnabledFlag (bool).
        if self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
           checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                priceModalScaleGraphicsItemTextEnabledFlag = True
        else:
            self.priceBarChartSettings.\
                priceModalScaleGraphicsItemTextEnabledFlag = False
        
        # priceModalScaleGraphicsItemMusicalRatios (list of MusicalRatio)
        self.priceBarChartSettings.priceModalScaleGraphicsItemMusicalRatios = \
            self.priceModalScaleGraphicsItemMusicalRatios
           
        # textGraphicsItemDefaultFont (QFont)
        self.priceBarChartSettings.\
            textGraphicsItemDefaultFontDescription = \
            self.textGraphicsItemDefaultFont.toString()

        # textGraphicsItemDefaultColor (QColor)
        self.priceBarChartSettings.textGraphicsItemDefaultColor = \
            self.textGraphicsItemDefaultColorEditButton.getColor()

        # textGraphicsItemDefaultXScaling (float).
        self.priceBarChartSettings.textGraphicsItemDefaultXScaling = \
            float(self.textGraphicsItemDefaultXScalingSpinBox.value())
        
        # textGraphicsItemDefaultYScaling (float).
        self.priceBarChartSettings.textGraphicsItemDefaultYScaling = \
            float(self.textGraphicsItemDefaultYScalingSpinBox.value())
        
        # priceTimeInfoGraphicsItemDefaultFont (QFont)
        self.priceBarChartSettings.\
            priceTimeInfoGraphicsItemDefaultFontDescription = \
            self.priceTimeInfoGraphicsItemDefaultFont.toString()

        # priceTimeInfoGraphicsItemDefaultColor (QColor)
        self.priceBarChartSettings.priceTimeInfoGraphicsItemDefaultColor = \
            self.priceTimeInfoGraphicsItemDefaultColorEditButton.getColor()

        # priceTimeInfoGraphicsItemDefaultXScaling (float).
        self.priceBarChartSettings.priceTimeInfoGraphicsItemDefaultXScaling = \
            float(self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox.value())
        
        # priceTimeInfoGraphicsItemDefaultYScaling (float).
        self.priceBarChartSettings.priceTimeInfoGraphicsItemDefaultYScaling = \
            float(self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox.value())

        # priceTimeInfoGraphicsItemShowTimestampFlag (bool).
        if self.priceTimeInfoGraphicsItemShowTimestampFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimestampFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimestampFlag = False
            
        # priceTimeInfoGraphicsItemShowPriceFlag (bool).
        if self.priceTimeInfoGraphicsItemShowPriceFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowPriceFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowPriceFlag = False

        # priceTimeInfoGraphicsItemShowSqrtPriceFlag (bool).
        if self.priceTimeInfoGraphicsItemShowSqrtPriceFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtPriceFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtPriceFlag = False

        # priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag (bool).
        if self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag = False

        # priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag (bool).
        if self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlagCheckBox.checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag = \
                True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag = \
                False

        # priceTimeInfoGraphicsItemShowPriceScaledValueFlag (bool).
        if self.priceTimeInfoGraphicsItemShowPriceScaledValueFlagCheckBox.checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowPriceScaledValueFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowPriceScaledValueFlag = False

        # priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag (bool).
        if self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlagCheckBox.checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag = False

        # priceTimeInfoGraphicsItemShowTimeScaledValueFlag (bool).
        if self.priceTimeInfoGraphicsItemShowTimeScaledValueFlagCheckBox.checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimeScaledValueFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowTimeScaledValueFlag = False

        # priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag (bool).
        if self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlagCheckBox.checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag = False

        # priceTimeInfoGraphicsItemShowLineToInfoPointFlag (bool).
        if self.priceTimeInfoGraphicsItemShowLineToInfoPointFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowLineToInfoPointFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeInfoGraphicsItemShowLineToInfoPointFlag = False

        # priceMeasurementGraphicsItemBarWidth (float).
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultBarWidth = \
            float(self.priceMeasurementGraphicsItemBarWidthSpinBox.value())

        # priceMeasurementGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultTextXScaling = \
            float(self.priceMeasurementGraphicsItemTextXScalingSpinBox.value())

        # priceMeasurementGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultTextYScaling = \
            float(self.priceMeasurementGraphicsItemTextYScalingSpinBox.value())

        # priceMeasurementGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultFontDescription = \
            self.priceMeasurementGraphicsItemDefaultFont.toString()

        # priceMeasurementGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultTextColor = \
            self.priceMeasurementGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # priceMeasurementGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultColor = \
            self.priceMeasurementGraphicsItemDefaultColorEditButton.\
            getColor()

        # priceMeasurementGraphicsItemShowPriceRangeTextFlag (bool).
        if self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowPriceRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowPriceRangeTextFlag = False

        # priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag (bool).
        if self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag = False

        # priceMeasurementGraphicsItemShowScaledValueRangeTextFlag (bool).
        if self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowScaledValueRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowScaledValueRangeTextFlag = False

        # priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag (bool).
        if self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = False

        # timeRetracementGraphicsItemBarHeight (float).
        self.priceBarChartSettings.timeRetracementGraphicsItemBarHeight = \
            float(self.timeRetracementGraphicsItemBarHeightSpinBox.value())

        # timeRetracementGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.timeRetracementGraphicsItemTextXScaling = \
            float(self.timeRetracementGraphicsItemTextXScalingSpinBox.value())

        # timeRetracementGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.timeRetracementGraphicsItemTextYScaling = \
            float(self.timeRetracementGraphicsItemTextYScalingSpinBox.value())

        # timeRetracementGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultFontDescription = \
            self.timeRetracementGraphicsItemDefaultFont.toString()

        # timeRetracementGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultTextColor = \
            self.timeRetracementGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # timeRetracementGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultColor = \
            self.timeRetracementGraphicsItemDefaultColorEditButton.\
            getColor()

        # timeRetracementGraphicsItemShowFullLinesFlag (bool).
        if self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowFullLinesFlag = True
        else:
            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowFullLinesFlag = False

        # timeRetracementGraphicsItemShowTimeTextFlag (bool).
        if self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowTimeTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowTimeTextFlag = False

        # timeRetracementGraphicsItemShowPercentTextFlag (bool).
        if self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowPercentTextFlag = True
        else:
            self.priceBarChartSettings.\
                timeRetracementGraphicsItemShowPercentTextFlag = False

        # TimeRetracement Ratios.
        for i in range(len(self.priceBarChartSettings.\
                           timeRetracementGraphicsItemRatios)):
            
            if self.timeRetracementGraphicsItemRatioCheckBoxes[i].\
               checkState() == Qt.Checked:

                self.priceBarChartSettings.\
                    timeRetracementGraphicsItemRatios[i].setEnabled(True)
            else:
                self.priceBarChartSettings.\
                    timeRetracementGraphicsItemRatios[i].setEnabled(False)
        
        # priceRetracementGraphicsItemBarWidth (float).
        self.priceBarChartSettings.priceRetracementGraphicsItemBarWidth = \
            float(self.priceRetracementGraphicsItemBarWidthSpinBox.value())

        # priceRetracementGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.priceRetracementGraphicsItemTextXScaling = \
            float(self.priceRetracementGraphicsItemTextXScalingSpinBox.value())

        # priceRetracementGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.priceRetracementGraphicsItemTextYScaling = \
            float(self.priceRetracementGraphicsItemTextYScalingSpinBox.value())

        # priceRetracementGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultFontDescription = \
            self.priceRetracementGraphicsItemDefaultFont.toString()

        # priceRetracementGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultTextColor = \
            self.priceRetracementGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # priceRetracementGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            priceRetracementGraphicsItemDefaultColor = \
            self.priceRetracementGraphicsItemDefaultColorEditButton.\
            getColor()

        # priceRetracementGraphicsItemShowFullLinesFlag (bool).
        if self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowFullLinesFlag = True
        else:
            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowFullLinesFlag = False

        # priceRetracementGraphicsItemShowPriceTextFlag (bool).
        if self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowPriceTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowPriceTextFlag = False

        # priceRetracementGraphicsItemShowPercentTextFlag (bool).
        if self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowPercentTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceRetracementGraphicsItemShowPercentTextFlag = False

        # PriceRetracement Ratios.
        for i in range(len(self.priceBarChartSettings.\
                           priceRetracementGraphicsItemRatios)):
            
            if self.priceRetracementGraphicsItemRatioCheckBoxes[i].\
               checkState() == Qt.Checked:

                self.priceBarChartSettings.\
                    priceRetracementGraphicsItemRatios[i].setEnabled(True)
            else:
                self.priceBarChartSettings.\
                    priceRetracementGraphicsItemRatios[i].setEnabled(False)

        # priceTimeVectorGraphicsItemBarWidth (float).
        self.priceBarChartSettings.priceTimeVectorGraphicsItemBarWidth = \
            float(self.priceTimeVectorGraphicsItemBarWidthSpinBox.value())

        # priceTimeVectorGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.priceTimeVectorGraphicsItemTextXScaling = \
            float(self.priceTimeVectorGraphicsItemTextXScalingSpinBox.value())

        # priceTimeVectorGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.priceTimeVectorGraphicsItemTextYScaling = \
            float(self.priceTimeVectorGraphicsItemTextYScalingSpinBox.value())

        # priceTimeVectorGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            priceTimeVectorGraphicsItemDefaultFontDescription = \
            self.priceTimeVectorGraphicsItemDefaultFont.toString()

        # priceTimeVectorGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            priceTimeVectorGraphicsItemDefaultTextColor = \
            self.priceTimeVectorGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # priceTimeVectorGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            priceTimeVectorGraphicsItemDefaultColor = \
            self.priceTimeVectorGraphicsItemDefaultColorEditButton.\
            getColor()

        # priceTimeVectorGraphicsItemShowDistanceTextFlag (bool).
        if self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowDistanceTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowDistanceTextFlag = False

        # priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag (bool).
        if self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag = False

        # priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag (bool).
        if self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag = False

        # priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag (bool).
        if self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag = False

        # priceTimeVectorGraphicsItemTiltedTextFlag (bool).
        if self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemTiltedTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemTiltedTextFlag = False

        # priceTimeVectorGraphicsItemAngleTextFlag (bool).
        if self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemAngleTextFlag = True
        else:
            self.priceBarChartSettings.\
                priceTimeVectorGraphicsItemAngleTextFlag = False

        # lineSegmentGraphicsItemBarWidth (float).
        self.priceBarChartSettings.lineSegmentGraphicsItemBarWidth = \
            float(self.lineSegmentGraphicsItemBarWidthSpinBox.value())

        # lineSegmentGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.lineSegmentGraphicsItemTextXScaling = \
            float(self.lineSegmentGraphicsItemTextXScalingSpinBox.value())

        # lineSegmentGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.lineSegmentGraphicsItemTextYScaling = \
            float(self.lineSegmentGraphicsItemTextYScalingSpinBox.value())

        # lineSegmentGraphicsItemDefaultFontDescription (str)
        self.priceBarChartSettings.\
            lineSegmentGraphicsItemDefaultFontDescription = \
            self.lineSegmentGraphicsItemDefaultFont.toString()

        # lineSegmentGraphicsItemDefaultTextColor (QColor).
        self.priceBarChartSettings.\
            lineSegmentGraphicsItemDefaultTextColor = \
            self.lineSegmentGraphicsItemDefaultTextColorEditButton.\
            getColor()

        # lineSegmentGraphicsItemDefaultColor (QColor).
        self.priceBarChartSettings.\
            lineSegmentGraphicsItemDefaultColor = \
            self.lineSegmentGraphicsItemDefaultColorEditButton.\
            getColor()

        # lineSegmentGraphicsItemTiltedTextFlag (bool).
        if self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                lineSegmentGraphicsItemTiltedTextFlag = True
        else:
            self.priceBarChartSettings.\
                lineSegmentGraphicsItemTiltedTextFlag = False

        # lineSegmentGraphicsItemAngleTextFlag (bool).
        if self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
           checkState() == Qt.Checked:

            self.priceBarChartSettings.\
                lineSegmentGraphicsItemAngleTextFlag = True
        else:
            self.priceBarChartSettings.\
                lineSegmentGraphicsItemAngleTextFlag = False

        # octaveFanGraphicsItemTextColor (QColor).
        self.priceBarChartSettings.octaveFanGraphicsItemBarColor = \
            self.octaveFanGraphicsItemColorEditButton.getColor()

        # octaveFanGraphicsItemTextTextColor (QColor).
        self.priceBarChartSettings.octaveFanGraphicsItemTextColor = \
            self.octaveFanGraphicsItemTextColorEditButton.getColor()
            
        # octaveFanGraphicsItemTextXScaling (float).
        self.priceBarChartSettings.octaveFanGraphicsItemTextXScaling = \
            float(self.octaveFanGraphicsItemTextXScalingSpinBox.value())

        # octaveFanGraphicsItemTextYScaling (float).
        self.priceBarChartSettings.octaveFanGraphicsItemTextYScaling = \
            float(self.octaveFanGraphicsItemTextYScalingSpinBox.value())
        
        # octaveFanGraphicsItemTextEnabledFlag (bool).
        if self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
           checkState() == Qt.Checked:
            
            self.priceBarChartSettings.\
                octaveFanGraphicsItemTextEnabledFlag = True
        else:
            self.priceBarChartSettings.\
                octaveFanGraphicsItemTextEnabledFlag = False
        
        # octaveFanGraphicsItemMusicalRatios (list of MusicalRatio)
        self.priceBarChartSettings.octaveFanGraphicsItemMusicalRatios = \
            self.octaveFanGraphicsItemMusicalRatios
        
        self.log.debug("Exiting saveValuesToSettings()")


    def _handleTimeMeasurementGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.timeMeasurementGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.timeMeasurementGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.timeMeasurementGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handleTextGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.textGraphicsItemDefaultFontModifyPushButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.textGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.textGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handlePriceTimeInfoGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.priceTimeInfoGraphicsItemDefaultFontModifyPushButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.priceTimeInfoGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.priceTimeInfoGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handlePriceMeasurementGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.priceMeasurementGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.priceMeasurementGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.priceMeasurementGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handleTimeRetracementGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.timeRetracementGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.timeRetracementGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.timeRetracementGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handlePriceRetracementGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.priceRetracementGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.priceRetracementGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.priceRetracementGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handlePriceTimeVectorGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.priceTimeVectorGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.priceTimeVectorGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.priceTimeVectorGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handleLineSegmentGraphicsItemDefaultFontModifyButtonClicked(self):
        """Called when the
        self.lineSegmentGraphicsItemDefaultFontModifyButton button is
        clicked.  Brings up a dialog for editing the font, and saves
        it if the dialog is accepted.
        """

        dialog = QFontDialog(self.lineSegmentGraphicsItemDefaultFont)

        rv = dialog.exec_()

        if rv == QDialog.Accepted:
            # Store the font in the member variable (not in the artifact).
            self.lineSegmentGraphicsItemDefaultFont = dialog.selectedFont()
        
    def _handlePriceBarPenWidthResetButtonClicked(self):
        """Called when the penWidthResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = PriceBarChartSettings.defaultPriceBarGraphicsItemPenWidth
        self.priceBarGraphicsItemPenWidthSpinBox.setValue(value)

    def _handlePriceBarLeftExtensionWidthResetButtonClicked(self):
        """Called when the leftExtensionWidthResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = PriceBarChartSettings.\
                    defaultPriceBarGraphicsItemLeftExtensionWidth
        self.priceBarGraphicsItemLeftExtensionWidthSpinBox.setValue(value)

    def _handlePriceBarRightExtensionWidthResetButtonClicked(self):
        """Called when the rightExtensionWidthResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = PriceBarChartSettings.\
                    defaultPriceBarGraphicsItemRightExtensionWidth
        self.priceBarGraphicsItemRightExtensionWidthSpinBox.setValue(value)

    def _handleBarCountGraphicsItemBarHeightResetButtonClicked(self):
        """Called when the barCountGraphicsItemBarHeightResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemBarHeight

        self.barCountGraphicsItemBarHeightSpinBox.setValue(value)

    def _handleBarCountGraphicsItemFontSizeResetButtonClicked(self):
        """Called when the barCountGraphicsItemFontSizeResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemFontSize

        self.barCountGraphicsItemFontSizeSpinBox.setValue(value)

    def _handleBarCountGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the barCountGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextXScaling

        self.barCountGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleBarCountGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the barCountGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextYScaling

        self.barCountGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleTimeMeasurementGraphicsItemBarHeightResetButtonClicked(self):
        """Called when the timeMeasurementGraphicsItemBarHeightResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemBarHeight

        self.timeMeasurementGraphicsItemBarHeightSpinBox.setValue(value)

    def _handleTimeMeasurementGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the timeMeasurementGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling

        self.timeMeasurementGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleTimeMeasurementGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the timeMeasurementGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling

        self.timeMeasurementGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleTimeMeasurementGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.timeMeasurementGraphicsItemDefaultFont = QFont()
        self.timeMeasurementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTimeMeasurementGraphicsItemDefaultFontDescription)
        
    def _handleTimeMeasurementGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeMeasurementGraphicsItemDefaultTextColor

        self.timeMeasurementGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handleTimeMeasurementGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeMeasurementGraphicsItemDefaultColor

        self.timeMeasurementGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handleTimeMeasurementGraphicsItemGroupBox1CheckAllButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemGroupBox1CheckAllButton is clicked.
        Sets the checkboxes in the groupbox page to be all checked.
        """

        checkState = Qt.Checked
        
        self.\
            timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)


    def _handleTimeMeasurementGraphicsItemGroupBox1UncheckAllButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemGroupBox1CheckAllButton is clicked.
        Sets the checkboxes in the groupbox page to be all unchecked.
        """

        checkState = Qt.Unchecked
        
        self.\
            timeMeasurementGraphicsItemShowBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdBarsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdHoursTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdDaysTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdWeeksTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMonthsTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlagCheckBox.\
            setCheckState(checkState)


    def _handleTimeMeasurementGraphicsItemGroupBox2CheckAllButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemGroupBox2CheckAllButton is clicked.
        Sets the checkboxes in the groupbox page to be all checked.
        """

        checkState = Qt.Checked

        self.\
            timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
            setCheckState(checkState)
        
        
    def _handleTimeMeasurementGraphicsItemGroupBox2UncheckAllButtonClicked(self):
        """Called when the
        timeMeasurementGraphicsItemGroupBox2CheckAllButton is clicked.
        Sets the checkboxes in the groupbox page to be all unchecked.
        """

        checkState = Qt.Unchecked
        
        self.\
            timeMeasurementGraphicsItemShowAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdAyanaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdVaraTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdRtuTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdMasaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdPaksaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSamaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrtSamaTextFlagCheckBox.\
            setCheckState(checkState)
        self.\
            timeMeasurementGraphicsItemShowSqrdSamaTextFlagCheckBox.\
            setCheckState(checkState)


    def _timeModalScaleGraphicsItemReloadMusicalRatiosGrid(self,
                                                           musicalRatios):
        """Clears and recreates the
        self.timeModalScaleGraphicsItemMusicalRatiosGridLayout
        according to the values in 'musicalRatios'.

        Arguments:
        
        musicalRatios - list of MusicalRatio objects to use to
                        populate the grid layout.
        """

        musicalRatiosGridLayout = \
            self.timeModalScaleGraphicsItemMusicalRatiosGridLayout
        
        # Remove any old widgets that were in the grid layout from
        # the grid layout..
        for r in range(musicalRatiosGridLayout.rowCount()):
            for c in range(musicalRatiosGridLayout.columnCount()):
                # Get the QLayoutItem.
                item = musicalRatiosGridLayout.itemAtPosition(r, c)
                if item != None:
                    # Get the widget in the layout item.
                    widget = item.widget()
                    if widget != None:
                        widget.setEnabled(False)
                        widget.setVisible(False)
                        widget.setParent(None)

                        # Actually remove the widget from the
                        # QGridLayout.  
                        musicalRatiosGridLayout.removeWidget(widget)
                                
        # Row.
        r = 0
        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        # Create the musical ratio items in the
        # musicalRatiosGridLayout QGridLayout.
        self.timeModalScaleGraphicsItemMusicalRatios = musicalRatios
        numMusicalRatios = len(self.timeModalScaleGraphicsItemMusicalRatios)

        # Clear the checkboxes list.
        self.timeModalScaleGraphicsItemCheckBoxes = []

        rangeUsed = range(numMusicalRatios)
            
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
            checkBox.stateChanged.connect(\
                self._handleTimeModalScaleGraphicsItemCheckMarkToggled)
            
            # Append to our list of checkboxes so that we can
            # reference them later and see what values are used in
            # them.  
            self.timeModalScaleGraphicsItemCheckBoxes.append(checkBox)
            
            descriptionLabel = QLabel(musicalRatio.getDescription())

            # Actually add the widgets to the grid layout.
            musicalRatiosGridLayout.\
                addWidget(checkBox, r, 0, al)
            musicalRatiosGridLayout.\
                addWidget(descriptionLabel, r, 1, al)

            r += 1


    def _handleTimeModalScaleGraphicsItemCheckMarkToggled(self):
        """Called when the user checkmarks or uncheckmarks a musical
        ratio checkbox in the TimeModalScaleGraphicsItem groupbox widgets.
        This will update the internally kept musicalRatio values.
        """

        # Go through all the musicalRatios in the widget, and set them
        # as enabled or disabled in the artifact, based on the check
        # state of the QCheckBox objects in self.checkBoxes.
        for i in range(len(self.timeModalScaleGraphicsItemCheckBoxes)):
            oldValue = \
                self.timeModalScaleGraphicsItemMusicalRatios[i].isEnabled()
            
            newValue = None
            if self.timeModalScaleGraphicsItemCheckBoxes[i].\
                   checkState() == Qt.Checked:
                
                newValue = True
            else:
                newValue = False
            
            if oldValue != newValue:
                self.log.debug("Updating enabled state of " +
                               "timeModalScaleGraphicsItemMusicalRatio" +
                               "[{}] from {} to {}".\
                               format(i, oldValue, newValue))
                self.timeModalScaleGraphicsItemMusicalRatios[i].\
                    setEnabled(newValue)
            else:
                #self.log.debug("No update to " +
                #               "timeModalScaleGraphicsItemMusicalRatio" +
                #               "[{}]".format(i))
                pass
        
    def _handleTimeModalScaleGraphicsItemRotateDownButtonClicked(self):
        """Called when the 'Rotate Down' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.timeModalScaleGraphicsItemMusicalRatios

        # Put the last musical ratio in the front.
        if len(musicalRatios) > 0:
            lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
            musicalRatios.insert(0, lastRatio)

        # Reload the musicalRatiosGrid.
        self._timeModalScaleGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handleTimeModalScaleGraphicsItemRotateUpButtonClicked(self):
        """Called when the 'Rotate Up' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.timeModalScaleGraphicsItemMusicalRatios
        
        # Put the first musical ratio in the back.
        if len(musicalRatios) > 0:
            firstRatio = musicalRatios.pop(0)
            musicalRatios.append(firstRatio)
        
        # Reload the musicalRatiosGrid.
        self._timeModalScaleGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handleTimeModalScaleGraphicsItemCheckMarkAllButtonClicked(self):
        """Called when the 'Check All' button is clicked."""

        for checkBox in self.timeModalScaleGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Checked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleTimeModalScaleGraphicsItemCheckMarkToggled()
        
    def _handleTimeModalScaleGraphicsItemCheckMarkNoneButtonClicked(self):
        """Called when the 'Check None' button is clicked."""

        for checkBox in self.timeModalScaleGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Unchecked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleTimeModalScaleGraphicsItemCheckMarkToggled()

    def _handleTimeModalScaleGraphicsItemColorResetButtonClicked(self):
        """Called when the timeModalScaleGraphicsItemColorResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarColor
        
        self.timeModalScaleGraphicsItemColorEditButton.setColor(value)

    def _handleTimeModalScaleGraphicsItemTextColorResetButtonClicked(self):
        """Called when the
        timeModalScaleGraphicsItemTextColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextColor
        
        self.timeModalScaleGraphicsItemTextColorEditButton.setColor(value)

    def _handleTimeModalScaleGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the timeModalScaleGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextXScaling

        self.timeModalScaleGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleTimeModalScaleGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the timeModalScaleGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextYScaling

        self.timeModalScaleGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleTimeModalScaleGraphicsItemTextEnabledFlagResetButtonClicked(self):
        """Called when the timeModalScaleGraphicsItemTextEnabledFlagResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextEnabledFlag

        if value == True:
            self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)

    def _handleTimeModalScaleGraphicsItemMusicalRatiosResetButtonClicked(self):
        """Called when the 'Reset to default' button is clicked for
        the TimeModalScaleGraphicsItem's MusicalRatios.
        """

        value = \
            copy.deepcopy(PriceBarChartSettings.\
                          defaultTimeModalScaleGraphicsItemMusicalRatios)
        
        self.timeModalScaleGraphicsItemMusicalRatios = value
        
        self._timeModalScaleGraphicsItemReloadMusicalRatiosGrid(\
            self.timeModalScaleGraphicsItemMusicalRatios)
        
    def _priceModalScaleGraphicsItemReloadMusicalRatiosGrid(self,
                                                           musicalRatios):
        """Clears and recreates the
        self.priceModalScaleGraphicsItemMusicalRatiosGridLayout
        according to the values in 'musicalRatios'.

        Arguments:
        
        musicalRatios - list of MusicalRatio objects to use to
                        populate the grid layout.
        """

        musicalRatiosGridLayout = \
            self.priceModalScaleGraphicsItemMusicalRatiosGridLayout
        
        # Remove any old widgets that were in the grid layout from
        # the grid layout..
        for r in range(musicalRatiosGridLayout.rowCount()):
            for c in range(musicalRatiosGridLayout.columnCount()):
                # Get the QLayoutItem.
                item = musicalRatiosGridLayout.itemAtPosition(r, c)
                if item != None:
                    # Get the widget in the layout item.
                    widget = item.widget()
                    if widget != None:
                        widget.setEnabled(False)
                        widget.setVisible(False)
                        widget.setParent(None)

                        # Actually remove the widget from the
                        # QGridLayout.  
                        musicalRatiosGridLayout.removeWidget(widget)
                                
        # Row.
        r = 0
        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        # Create the musical ratio items in the
        # musicalRatiosGridLayout QGridLayout.
        self.priceModalScaleGraphicsItemMusicalRatios = musicalRatios
        numMusicalRatios = len(self.priceModalScaleGraphicsItemMusicalRatios)

        # Clear the checkboxes list.
        self.priceModalScaleGraphicsItemCheckBoxes = []

        rangeUsed = range(numMusicalRatios)
            
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
            checkBox.stateChanged.connect(\
                self._handlePriceModalScaleGraphicsItemCheckMarkToggled)
            
            # Append to our list of checkboxes so that we can
            # reference them later and see what values are used in
            # them.  
            self.priceModalScaleGraphicsItemCheckBoxes.append(checkBox)
            
            descriptionLabel = QLabel(musicalRatio.getDescription())

            # Actually add the widgets to the grid layout.
            musicalRatiosGridLayout.\
                addWidget(checkBox, r, 0, al)
            musicalRatiosGridLayout.\
                addWidget(descriptionLabel, r, 1, al)

            r += 1


    def _handlePriceModalScaleGraphicsItemCheckMarkToggled(self):
        """Called when the user checkmarks or uncheckmarks a musical
        ratio checkbox in the PriceModalScaleGraphicsItem groupbox widgets.
        This will update the internally kept musicalRatio values.
        """

        # Go through all the musicalRatios in the widget, and set them
        # as enabled or disabled in the artifact, based on the check
        # state of the QCheckBox objects in self.checkBoxes.
        for i in range(len(self.priceModalScaleGraphicsItemCheckBoxes)):
            oldValue = \
                self.priceModalScaleGraphicsItemMusicalRatios[i].isEnabled()
            
            newValue = None
            if self.priceModalScaleGraphicsItemCheckBoxes[i].\
                   checkState() == Qt.Checked:
                
                newValue = True
            else:
                newValue = False
            
            if oldValue != newValue:
                self.log.debug("Updating enabled state of " +
                               "priceModalScaleGraphicsItemMusicalRatio" +
                               "[{}] from {} to {}".\
                               format(i, oldValue, newValue))
                self.priceModalScaleGraphicsItemMusicalRatios[i].\
                    setEnabled(newValue)
            else:
                #self.log.debug("No update to " +
                #               "priceModalScaleGraphicsItemMusicalRatio" +
                #               "[{}]".format(i))
                pass
        
    def _handlePriceModalScaleGraphicsItemRotateDownButtonClicked(self):
        """Called when the 'Rotate Down' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.priceModalScaleGraphicsItemMusicalRatios

        # Put the last musical ratio in the front.
        if len(musicalRatios) > 0:
            lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
            musicalRatios.insert(0, lastRatio)

        # Reload the musicalRatiosGrid.
        self._priceModalScaleGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handlePriceModalScaleGraphicsItemRotateUpButtonClicked(self):
        """Called when the 'Rotate Up' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.priceModalScaleGraphicsItemMusicalRatios
        
        # Put the first musical ratio in the back.
        if len(musicalRatios) > 0:
            firstRatio = musicalRatios.pop(0)
            musicalRatios.append(firstRatio)
        
        # Reload the musicalRatiosGrid.
        self._priceModalScaleGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handlePriceModalScaleGraphicsItemCheckMarkAllButtonClicked(self):
        """Called when the 'Check All' button is clicked."""

        for checkBox in self.priceModalScaleGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Checked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handlePriceModalScaleGraphicsItemCheckMarkToggled()
        
    def _handlePriceModalScaleGraphicsItemCheckMarkNoneButtonClicked(self):
        """Called when the 'Check None' button is clicked."""

        for checkBox in self.priceModalScaleGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Unchecked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handlePriceModalScaleGraphicsItemCheckMarkToggled()

    def _handlePriceModalScaleGraphicsItemColorResetButtonClicked(self):
        """Called when the priceModalScaleGraphicsItemColorResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarColor
        
        self.priceModalScaleGraphicsItemColorEditButton.setColor(value)

    def _handlePriceModalScaleGraphicsItemTextColorResetButtonClicked(self):
        """Called when the
        priceModalScaleGraphicsItemTextColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextColor
        
        self.priceModalScaleGraphicsItemTextColorEditButton.setColor(value)

    def _handlePriceModalScaleGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the priceModalScaleGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextXScaling

        self.priceModalScaleGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handlePriceModalScaleGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the priceModalScaleGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextYScaling

        self.priceModalScaleGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handlePriceModalScaleGraphicsItemTextEnabledFlagResetButtonClicked(self):
        """Called when the priceModalScaleGraphicsItemTextEnabledFlagResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextEnabledFlag

        if value == True:
            self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceModalScaleGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)

    def _handlePriceModalScaleGraphicsItemMusicalRatiosResetButtonClicked(self):
        """Called when the 'Reset to default' button is clicked for
        the PriceModalScaleGraphicsItem's MusicalRatios.
        """

        value = \
            copy.deepcopy(PriceBarChartSettings.\
                          defaultPriceModalScaleGraphicsItemMusicalRatios)
        
        self.priceModalScaleGraphicsItemMusicalRatios = value
        
        self._priceModalScaleGraphicsItemReloadMusicalRatiosGrid(\
            self.priceModalScaleGraphicsItemMusicalRatios)
        
    def _handleTextGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the textGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.textGraphicsItemDefaultFont = QFont()
        self.textGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTextGraphicsItemDefaultFontDescription)
        
    def _handleTextGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the textGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTextGraphicsItemDefaultColor

        self.textGraphicsItemDefaultColorEditButton.setColor(value)

    def _handleTextGraphicsItemDefaultXScalingResetButtonClicked(self):
        """Called when the textGraphicsItemDefaultXScalingResetButton is
        clicked.  Resets the internal value to the default value.
        """

        value = PriceBarChartSettings.\
                defaultTextGraphicsItemDefaultXScaling

        self.textGraphicsItemDefaultXScalingSpinBox.setValue(value)
        
    def _handleTextGraphicsItemDefaultYScalingResetButtonClicked(self):
        """Called when the textGraphicsItemDefaultYScalingResetButton is
        clicked.  Resets the internal value to the default value.
        """

        value = PriceBarChartSettings.\
                defaultTextGraphicsItemDefaultYScaling

        self.textGraphicsItemDefaultYScalingSpinBox.setValue(value)
        
    def _handlePriceTimeInfoGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        priceTimeInfoGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.priceTimeInfoGraphicsItemDefaultFont = QFont()
        self.priceTimeInfoGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceTimeInfoGraphicsItemDefaultFontDescription)
        
    def _handlePriceTimeInfoGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        priceTimeInfoGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeInfoGraphicsItemDefaultColor

        self.priceTimeInfoGraphicsItemDefaultColorEditButton.setColor(value)

    def _handlePriceTimeInfoGraphicsItemDefaultXScalingResetButtonClicked(self):
        """Called when the
        priceTimeInfoGraphicsItemDefaultXScalingResetButton is
        clicked.  Resets the internal value to the default value.
        """

        value = PriceBarChartSettings.\
                defaultPriceTimeInfoGraphicsItemDefaultXScaling

        self.priceTimeInfoGraphicsItemDefaultXScalingSpinBox.setValue(value)
        
    def _handlePriceTimeInfoGraphicsItemDefaultYScalingResetButtonClicked(self):
        """Called when the
        priceTimeInfoGraphicsItemDefaultYScalingResetButton is
        clicked.  Resets the internal value to the default value.
        """

        value = PriceBarChartSettings.\
                defaultPriceTimeInfoGraphicsItemDefaultYScaling

        self.priceTimeInfoGraphicsItemDefaultYScalingSpinBox.setValue(value)
        
    def _handlePriceMeasurementGraphicsItemBarWidthResetButtonClicked(self):
        """Called when the priceMeasurementGraphicsItemBarWidthResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemBarWidth

        self.priceMeasurementGraphicsItemBarWidthSpinBox.setValue(value)

    def _handlePriceMeasurementGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the priceMeasurementGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextXScaling

        self.priceMeasurementGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handlePriceMeasurementGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the priceMeasurementGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextYScaling

        self.priceMeasurementGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handlePriceMeasurementGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        priceMeasurementGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.priceMeasurementGraphicsItemDefaultFont = QFont()
        self.priceMeasurementGraphicsItemDefaultFont.\
            fromString(\
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultFontDescription)
        
    def _handlePriceMeasurementGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        priceMeasurementGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemDefaultTextColor

        self.priceMeasurementGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handlePriceMeasurementGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        priceMeasurementGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemDefaultColor

        self.priceMeasurementGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handlePriceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton(self):
        """Called when the
        priceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag

        if value == True:
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton(self):
        """Called when the
        priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag

        if value == True:
            self.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.\
                priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton(self):
        """Called when the
        priceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag

        if value == True:
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton(self):
        """Called when the
        priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag

        if value == True:
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handleTimeRetracementGraphicsItemBarHeightResetButtonClicked(self):
        """Called when the timeRetracementGraphicsItemBarHeightResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemBarHeight

        self.timeRetracementGraphicsItemBarHeightSpinBox.setValue(value)

    def _handleTimeRetracementGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the timeRetracementGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextXScaling

        self.timeRetracementGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleTimeRetracementGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the timeRetracementGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextYScaling

        self.timeRetracementGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleTimeRetracementGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        timeRetracementGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.timeRetracementGraphicsItemDefaultFont = QFont()
        self.timeRetracementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultTimeRetracementGraphicsItemDefaultFontDescription)
        
    def _handleTimeRetracementGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        timeRetracementGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeRetracementGraphicsItemDefaultTextColor

        self.timeRetracementGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handleTimeRetracementGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        timeRetracementGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeRetracementGraphicsItemDefaultColor

        self.timeRetracementGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handleTimeRetracementGraphicsItemShowFullLinesFlagResetButton(self):
        """Called when the
        timeRetracementGraphicsItemShowFullLinesFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeRetracementGraphicsItemShowFullLinesFlag

        if value == True:
            self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handleTimeRetracementGraphicsItemShowTimeTextFlagResetButton(self):
        """Called when the
        timeRetracementGraphicsItemShowTimeTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeRetracementGraphicsItemShowTimeTextFlag

        if value == True:
            self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowTimeTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handleTimeRetracementGraphicsItemShowPercentTextFlagResetButton(self):
        """Called when the
        timeRetracementGraphicsItemShowPercentTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultTimeRetracementGraphicsItemShowPercentTextFlag

        if value == True:
            self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.timeRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceRetracementGraphicsItemBarWidthResetButtonClicked(self):
        """Called when the priceRetracementGraphicsItemBarWidthResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemBarWidth

        self.priceRetracementGraphicsItemBarWidthSpinBox.setValue(value)

    def _handlePriceRetracementGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the priceRetracementGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextXScaling

        self.priceRetracementGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handlePriceRetracementGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the priceRetracementGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextYScaling

        self.priceRetracementGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handlePriceRetracementGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        priceRetracementGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.priceRetracementGraphicsItemDefaultFont = QFont()
        self.priceRetracementGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceRetracementGraphicsItemDefaultFontDescription)
        
    def _handlePriceRetracementGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        priceRetracementGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceRetracementGraphicsItemDefaultTextColor

        self.priceRetracementGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handlePriceRetracementGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        priceRetracementGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceRetracementGraphicsItemDefaultColor

        self.priceRetracementGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handlePriceRetracementGraphicsItemShowFullLinesFlagResetButton(self):
        """Called when the
        priceRetracementGraphicsItemShowFullLinesFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceRetracementGraphicsItemShowFullLinesFlag

        if value == True:
            self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowFullLinesFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceRetracementGraphicsItemShowPriceTextFlagResetButton(self):
        """Called when the
        priceRetracementGraphicsItemShowPriceTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceRetracementGraphicsItemShowPriceTextFlag

        if value == True:
            self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowPriceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceRetracementGraphicsItemShowPercentTextFlagResetButton(self):
        """Called when the
        priceRetracementGraphicsItemShowPercentTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceRetracementGraphicsItemShowPercentTextFlag

        if value == True:
            self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceRetracementGraphicsItemShowPercentTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemBarWidthResetButtonClicked(self):
        """Called when the priceTimeVectorGraphicsItemBarWidthResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemBarWidth

        self.priceTimeVectorGraphicsItemBarWidthSpinBox.setValue(value)

    def _handlePriceTimeVectorGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the priceTimeVectorGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemTextXScaling

        self.priceTimeVectorGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handlePriceTimeVectorGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the priceTimeVectorGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemTextYScaling

        self.priceTimeVectorGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handlePriceTimeVectorGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        priceTimeVectorGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.priceTimeVectorGraphicsItemDefaultFont = QFont()
        self.priceTimeVectorGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultPriceTimeVectorGraphicsItemDefaultFontDescription)
        
    def _handlePriceTimeVectorGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        priceTimeVectorGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemDefaultTextColor

        self.priceTimeVectorGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handlePriceTimeVectorGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        priceTimeVectorGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemDefaultColor

        self.priceTimeVectorGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handlePriceTimeVectorGraphicsItemShowDistanceTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemShowDistanceTextFlagResetButton is
        clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowDistanceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemShowSqrtDistanceTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemTiltedTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemTiltedTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemTiltedTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handlePriceTimeVectorGraphicsItemAngleTextFlagResetButton(self):
        """Called when the
        priceTimeVectorGraphicsItemAngleTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultPriceTimeVectorGraphicsItemAngleTextFlag

        if value == True:
            self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.priceTimeVectorGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handleLineSegmentGraphicsItemBarWidthResetButtonClicked(self):
        """Called when the lineSegmentGraphicsItemBarWidthResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemBarWidth

        self.lineSegmentGraphicsItemBarWidthSpinBox.setValue(value)

    def _handleLineSegmentGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the lineSegmentGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemTextXScaling

        self.lineSegmentGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleLineSegmentGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the lineSegmentGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemTextYScaling

        self.lineSegmentGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleLineSegmentGraphicsItemDefaultFontResetButtonClicked(self):
        """Called when the
        lineSegmentGraphicsItemDefaultFontResetButton is clicked.
        Resets the internal value to the default value.
        """

        self.lineSegmentGraphicsItemDefaultFont = QFont()
        self.lineSegmentGraphicsItemDefaultFont.\
            fromString(PriceBarChartSettings.\
                       defaultLineSegmentGraphicsItemDefaultFontDescription)
        
    def _handleLineSegmentGraphicsItemDefaultTextColorResetButtonClicked(self):
        """Called when the
        lineSegmentGraphicsItemDefaultTextColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultLineSegmentGraphicsItemDefaultTextColor

        self.lineSegmentGraphicsItemDefaultTextColorEditButton.\
            setColor(value)

    def _handleLineSegmentGraphicsItemDefaultColorResetButtonClicked(self):
        """Called when the
        lineSegmentGraphicsItemDefaultColorResetButton is clicked.
        Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultLineSegmentGraphicsItemDefaultColor

        self.lineSegmentGraphicsItemDefaultColorEditButton.\
            setColor(value)

    def _handleLineSegmentGraphicsItemTiltedTextFlagResetButton(self):
        """Called when the
        lineSegmentGraphicsItemTiltedTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultLineSegmentGraphicsItemTiltedTextFlag

        if value == True:
            self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.lineSegmentGraphicsItemTiltedTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _handleLineSegmentGraphicsItemAngleTextFlagResetButton(self):
        """Called when the
        lineSegmentGraphicsItemAngleTextFlagResetButton
        is clicked.  Resets the internal value to the default value.
        """

        value = \
              PriceBarChartSettings.\
              defaultLineSegmentGraphicsItemAngleTextFlag

        if value == True:
            self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.lineSegmentGraphicsItemAngleTextFlagCheckBox.\
                setCheckState(Qt.Unchecked)
            
    def _octaveFanGraphicsItemReloadMusicalRatiosGrid(self,
                                                           musicalRatios):
        """Clears and recreates the
        self.octaveFanGraphicsItemMusicalRatiosGridLayout
        according to the values in 'musicalRatios'.

        Arguments:
        
        musicalRatios - list of MusicalRatio objects to use to
                        populate the grid layout.
        """

        musicalRatiosGridLayout = \
            self.octaveFanGraphicsItemMusicalRatiosGridLayout
        
        # Remove any old widgets that were in the grid layout from
        # the grid layout..
        for r in range(musicalRatiosGridLayout.rowCount()):
            for c in range(musicalRatiosGridLayout.columnCount()):
                # Get the QLayoutItem.
                item = musicalRatiosGridLayout.itemAtPosition(r, c)
                if item != None:
                    # Get the widget in the layout item.
                    widget = item.widget()
                    if widget != None:
                        widget.setEnabled(False)
                        widget.setVisible(False)
                        widget.setParent(None)

                        # Actually remove the widget from the
                        # QGridLayout.  
                        musicalRatiosGridLayout.removeWidget(widget)
                                
        # Row.
        r = 0
        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        # Create the musical ratio items in the
        # musicalRatiosGridLayout QGridLayout.
        self.octaveFanGraphicsItemMusicalRatios = musicalRatios
        numMusicalRatios = len(self.octaveFanGraphicsItemMusicalRatios)

        # Clear the checkboxes list.
        self.octaveFanGraphicsItemCheckBoxes = []

        rangeUsed = range(numMusicalRatios)
            
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
            checkBox.stateChanged.connect(\
                self._handleOctaveFanGraphicsItemCheckMarkToggled)
            
            # Append to our list of checkboxes so that we can
            # reference them later and see what values are used in
            # them.  
            self.octaveFanGraphicsItemCheckBoxes.append(checkBox)
            
            descriptionLabel = QLabel(musicalRatio.getDescription())

            # Actually add the widgets to the grid layout.
            musicalRatiosGridLayout.\
                addWidget(checkBox, r, 0, al)
            musicalRatiosGridLayout.\
                addWidget(descriptionLabel, r, 1, al)

            r += 1


    def _handleOctaveFanGraphicsItemCheckMarkToggled(self):
        """Called when the user checkmarks or uncheckmarks a musical
        ratio checkbox in the OctaveFanGraphicsItem groupbox widgets.
        This will update the internally kept musicalRatio values.
        """

        # Go through all the musicalRatios in the widget, and set them
        # as enabled or disabled in the artifact, based on the check
        # state of the QCheckBox objects in self.checkBoxes.
        for i in range(len(self.octaveFanGraphicsItemCheckBoxes)):
            oldValue = \
                self.octaveFanGraphicsItemMusicalRatios[i].isEnabled()
            
            newValue = None
            if self.octaveFanGraphicsItemCheckBoxes[i].\
                   checkState() == Qt.Checked:
                
                newValue = True
            else:
                newValue = False
            
            if oldValue != newValue:
                self.log.debug("Updating enabled state of " +
                               "octaveFanGraphicsItemMusicalRatio" +
                               "[{}] from {} to {}".\
                               format(i, oldValue, newValue))
                self.octaveFanGraphicsItemMusicalRatios[i].\
                    setEnabled(newValue)
            else:
                #self.log.debug("No update to " +
                #               "octaveFanGraphicsItemMusicalRatio" +
                #               "[{}]".format(i))
                pass
        
    def _handleOctaveFanGraphicsItemRotateDownButtonClicked(self):
        """Called when the 'Rotate Down' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.octaveFanGraphicsItemMusicalRatios

        # Put the last musical ratio in the front.
        if len(musicalRatios) > 0:
            lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
            musicalRatios.insert(0, lastRatio)

        # Reload the musicalRatiosGrid.
        self._octaveFanGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handleOctaveFanGraphicsItemRotateUpButtonClicked(self):
        """Called when the 'Rotate Up' button is clicked."""

        # Get all the musicalRatios.
        musicalRatios = self.octaveFanGraphicsItemMusicalRatios
        
        # Put the first musical ratio in the back.
        if len(musicalRatios) > 0:
            firstRatio = musicalRatios.pop(0)
            musicalRatios.append(firstRatio)
        
        # Reload the musicalRatiosGrid.
        self._octaveFanGraphicsItemReloadMusicalRatiosGrid(musicalRatios)
    
    def _handleOctaveFanGraphicsItemCheckMarkAllButtonClicked(self):
        """Called when the 'Check All' button is clicked."""

        for checkBox in self.octaveFanGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Checked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleOctaveFanGraphicsItemCheckMarkToggled()
        
    def _handleOctaveFanGraphicsItemCheckMarkNoneButtonClicked(self):
        """Called when the 'Check None' button is clicked."""

        for checkBox in self.octaveFanGraphicsItemCheckBoxes:
            checkBox.setCheckState(Qt.Unchecked)

        # Call this to update the internal artifact object according
        # to what the widgets have set (in this case, the 'enabled'
        # checkboxes).
        self._handleOctaveFanGraphicsItemCheckMarkToggled()

    def _handleOctaveFanGraphicsItemColorResetButtonClicked(self):
        """Called when the octaveFanGraphicsItemColorResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemBarColor
        
        self.octaveFanGraphicsItemColorEditButton.setColor(value)

    def _handleOctaveFanGraphicsItemTextColorResetButtonClicked(self):
        """Called when the
        octaveFanGraphicsItemTextColorResetButton is clicked.
        Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextColor
        
        self.octaveFanGraphicsItemTextColorEditButton.setColor(value)

    def _handleOctaveFanGraphicsItemTextXScalingResetButtonClicked(self):
        """Called when the octaveFanGraphicsItemTextXScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextXScaling

        self.octaveFanGraphicsItemTextXScalingSpinBox.setValue(value)

    def _handleOctaveFanGraphicsItemTextYScalingResetButtonClicked(self):
        """Called when the octaveFanGraphicsItemTextYScalingResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextYScaling

        self.octaveFanGraphicsItemTextYScalingSpinBox.setValue(value)

    def _handleOctaveFanGraphicsItemTextEnabledFlagResetButtonClicked(self):
        """Called when the octaveFanGraphicsItemTextEnabledFlagResetButton
        is clicked.  Resets the widget value to the default value.
        """

        value = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextEnabledFlag

        if value == True:
            self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Checked)
        else:
            self.octaveFanGraphicsItemTextEnabledFlagCheckBox.\
                setCheckState(Qt.Unchecked)

    def _handleOctaveFanGraphicsItemMusicalRatiosResetButtonClicked(self):
        """Called when the 'Reset to default' button is clicked for
        the OctaveFanGraphicsItem's MusicalRatios.
        """

        value = \
            copy.deepcopy(PriceBarChartSettings.\
                          defaultOctaveFanGraphicsItemMusicalRatios)
        
        self.octaveFanGraphicsItemMusicalRatios = value
        
        self._octaveFanGraphicsItemReloadMusicalRatiosGrid(\
            self.octaveFanGraphicsItemMusicalRatios)
        
    def _handleResetAllToDefaultButtonClicked(self):
        """Called when the resetAllToDefaultButton is clicked.
        Resets the all the widget values in this widget to the default
        values.
        """

        self._handlePriceBarPenWidthResetButtonClicked()
        self._handlePriceBarLeftExtensionWidthResetButtonClicked()
        self._handlePriceBarRightExtensionWidthResetButtonClicked()
        
        self._handleBarCountGraphicsItemBarHeightResetButtonClicked()
        self._handleBarCountGraphicsItemFontSizeResetButtonClicked()
        self._handleBarCountGraphicsItemTextXScalingResetButtonClicked()
        self._handleBarCountGraphicsItemTextYScalingResetButtonClicked()
        
        self._handleTimeMeasurementGraphicsItemBarHeightResetButtonClicked()
        self._handleTimeMeasurementGraphicsItemTextXScalingResetButtonClicked()
        self._handleTimeMeasurementGraphicsItemTextYScalingResetButtonClicked()
        self._handleTimeMeasurementGraphicsItemDefaultFontResetButtonClicked()
        self._handleTimeMeasurementGraphicsItemDefaultTextColorResetButtonClicked()
        self._handleTimeMeasurementGraphicsItemDefaultColorResetButtonClicked()
        
        self._handleTimeModalScaleGraphicsItemColorResetButtonClicked()
        self._handleTimeModalScaleGraphicsItemTextColorResetButtonClicked()
        self._handleTimeModalScaleGraphicsItemTextXScalingResetButtonClicked()
        self._handleTimeModalScaleGraphicsItemTextYScalingResetButtonClicked()
        self._handleTimeModalScaleGraphicsItemTextEnabledFlagResetButtonClicked()
        self._handleTimeModalScaleGraphicsItemMusicalRatiosResetButtonClicked()
        
        self._handlePriceModalScaleGraphicsItemColorResetButtonClicked()
        self._handlePriceModalScaleGraphicsItemTextColorResetButtonClicked()
        self._handlePriceModalScaleGraphicsItemTextXScalingResetButtonClicked()
        self._handlePriceModalScaleGraphicsItemTextYScalingResetButtonClicked()
        self._handlePriceModalScaleGraphicsItemTextEnabledFlagResetButtonClicked()
        self._handlePriceModalScaleGraphicsItemMusicalRatiosResetButtonClicked()
        
        self._handleTextGraphicsItemDefaultFontResetButtonClicked()
        self._handleTextGraphicsItemDefaultColorResetButtonClicked()
        self._handleTextGraphicsItemDefaultXScalingResetButtonClicked()
        self._handleTextGraphicsItemDefaultYScalingResetButtonClicked()
        
        self._handlePriceTimeInfoGraphicsItemDefaultFontResetButtonClicked()
        self._handlePriceTimeInfoGraphicsItemDefaultColorResetButtonClicked()
        self._handlePriceTimeInfoGraphicsItemDefaultXScalingResetButtonClicked()
        self._handlePriceTimeInfoGraphicsItemDefaultYScalingResetButtonClicked()

        self._handlePriceMeasurementGraphicsItemBarWidthResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemTextXScalingResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemTextYScalingResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemDefaultFontResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemDefaultTextColorResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemDefaultColorResetButtonClicked()
        self._handlePriceMeasurementGraphicsItemShowPriceRangeTextFlagResetButton()
        self._handlePriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlagResetButton()
        self._handlePriceMeasurementGraphicsItemShowScaledValueRangeTextFlagResetButton()
        self._handlePriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlagResetButton()
        
        self._handleTimeRetracementGraphicsItemBarHeightResetButtonClicked()
        self._handleTimeRetracementGraphicsItemTextXScalingResetButtonClicked()
        self._handleTimeRetracementGraphicsItemTextYScalingResetButtonClicked()
        self._handleTimeRetracementGraphicsItemDefaultFontResetButtonClicked()
        self._handleTimeRetracementGraphicsItemDefaultTextColorResetButtonClicked()
        self._handleTimeRetracementGraphicsItemDefaultColorResetButtonClicked()
        self._handleTimeRetracementGraphicsItemShowFullLinesFlagResetButton()
        self._handleTimeRetracementGraphicsItemShowTimeTextFlagResetButton()
        self._handleTimeRetracementGraphicsItemShowPercentTextFlagResetButton()
        
        self._handlePriceRetracementGraphicsItemBarWidthResetButtonClicked()
        self._handlePriceRetracementGraphicsItemTextXScalingResetButtonClicked()
        self._handlePriceRetracementGraphicsItemTextYScalingResetButtonClicked()
        self._handlePriceRetracementGraphicsItemDefaultFontResetButtonClicked()
        self._handlePriceRetracementGraphicsItemDefaultTextColorResetButtonClicked()
        self._handlePriceRetracementGraphicsItemDefaultColorResetButtonClicked()
        self._handlePriceRetracementGraphicsItemShowFullLinesFlagResetButton()
        self._handlePriceRetracementGraphicsItemShowPriceTextFlagResetButton()
        self._handlePriceRetracementGraphicsItemShowPercentTextFlagResetButton()

        self._handlePriceTimeVectorGraphicsItemBarWidthResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemTextXScalingResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemTextYScalingResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemDefaultFontResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemDefaultTextColorResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemDefaultColorResetButtonClicked()
        self._handlePriceTimeVectorGraphicsItemShowDistanceTextFlagResetButton()
        self._handlePriceTimeVectorGraphicsItemShowSqrtDistanceTextFlagResetButton()
        self._handlePriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlagResetButton()
        self._handlePriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlagResetButton()
        self._handlePriceTimeVectorGraphicsItemTiltedTextFlagResetButton()
        self._handlePriceTimeVectorGraphicsItemAngleTextFlagResetButton()

        self._handleLineSegmentGraphicsItemBarWidthResetButtonClicked()
        self._handleLineSegmentGraphicsItemTextXScalingResetButtonClicked()
        self._handleLineSegmentGraphicsItemTextYScalingResetButtonClicked()
        self._handleLineSegmentGraphicsItemDefaultFontResetButtonClicked()
        self._handleLineSegmentGraphicsItemDefaultTextColorResetButtonClicked()
        self._handleLineSegmentGraphicsItemDefaultColorResetButtonClicked()
        self._handleLineSegmentGraphicsItemTiltedTextFlagResetButton()
        self._handleLineSegmentGraphicsItemAngleTextFlagResetButton()

        self._handleOctaveFanGraphicsItemColorResetButtonClicked()
        self._handleOctaveFanGraphicsItemTextColorResetButtonClicked()
        self._handleOctaveFanGraphicsItemTextXScalingResetButtonClicked()
        self._handleOctaveFanGraphicsItemTextYScalingResetButtonClicked()
        self._handleOctaveFanGraphicsItemTextEnabledFlagResetButtonClicked()
        self._handleOctaveFanGraphicsItemMusicalRatiosResetButtonClicked()

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValuesToSettings()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()



class PriceBarChartSettingsEditDialog(QDialog):
    """QDialog for editing a PriceBarChartSettings object's class members.
    """

    def __init__(self, priceBarChartSettings, parent=None):
        """Initializes the dialog and internal widget with the current
        settings."""

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartSettingsEditDialog")

        self.setWindowTitle("PriceBarChart Settings")

        # Save a reference to the PriceBarChartSettings object.
        self.priceBarChartSettings = priceBarChartSettings

        # Create the contents.
        self.priceBarChartSettingsEditWidget = \
            PriceBarChartSettingsEditWidget(self.priceBarChartSettings)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.priceBarChartSettingsEditWidget)
        self.setLayout(layout)

        self.priceBarChartSettingsEditWidget.okayButtonClicked.\
            connect(self.accept)
        self.priceBarChartSettingsEditWidget.cancelButtonClicked.\
            connect(self.reject)

class PriceChartDocumentDataEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceChartDocumentData.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, priceChartDocumentData, parent=None):
        """QWidget for editing some of the fields of a
        PriceChartDocumentData object.  
        
        Note:  The object passed in gets modified if the user clicks the
        'Okay' button.
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentDataEditWidget")

        # Save off the PriceChartDocumentData object.
        self.priceChartDocumentData = priceChartDocumentData

        # QGroupBox to hold the edit widgets and form.
        self.pcddGroupBox = QGroupBox("PriceChartDocument Data:")

        # Description.
        self.descriptionLabel = QLabel("&Description:")
        self.descriptionLineEdit = QLineEdit()
        self.descriptionLabel.setBuddy(self.descriptionLineEdit)

        self.userNotesLabel = QLabel("&User notes:")
        self.userNotesTextEdit = QTextEdit()
        self.userNotesTextEdit.setAcceptRichText(False)
        self.userNotesLabel.setBuddy(self.userNotesTextEdit)
        
        # Form layout.
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.descriptionLabel,
                               self.descriptionLineEdit)
        self.formLayout.addRow(self.userNotesLabel,
                               self.userNotesTextEdit)

        self.pcddGroupBox.setLayout(self.formLayout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.pcddGroupBox) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Now that all the widgets are created, load the values.
        self.loadValues(self.priceChartDocumentData)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)


    def loadValues(self, priceChartDocumentData):
        """Loads the widgets with values from the given
        priceChartDocumentData object.
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if priceChartDocumentData == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  " + \
                           "priceChartDocumentData can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        else:
            self.priceChartDocumentData = priceChartDocumentData

        # Set the widgets.

        # Description.
        self.descriptionLineEdit.\
            setText(self.priceChartDocumentData.getDescription())

        # User notes.
        self.userNotesTextEdit.\
            setPlainText(self.priceChartDocumentData.getUserNotes())

        self.log.debug("Exiting loadValues()")
        
    def saveValues(self):
        """Saves the values in the widgets to the 
        PriceChartDocumentData object passed in this class's constructor.
        """
    
        self.log.debug("Entered saveValues()")

        # Description.
        self.priceChartDocumentData.\
            setDescription(self.descriptionLineEdit.text())

        # User notes.
        self.priceChartDocumentData.\
            setUserNotes(self.userNotesTextEdit.toPlainText())

        self.log.debug("Exiting saveValues()")


    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()



class PriceChartDocumentDataEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceChartDocumentData.
    """

    def __init__(self, priceChartDocumentData, parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceChartDocumentData.
        
        Note:  The object passed in gets modified if the user clicks the
        'Okay' button.
        """

        super().__init__(parent)

        # Logger object.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentDataEditDialog")

        self.setWindowTitle("Edit PriceChartDocument Data")

        # Save a reference to the PriceChartDocumentData object.
        self.priceChartDocumentData = priceChartDocumentData

        # Create the contents.
        self.priceChartDocumentDataEditWidget = \
            PriceChartDocumentDataEditWidget(self.priceChartDocumentData)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.priceChartDocumentDataEditWidget)
        self.setLayout(layout)

        self.priceChartDocumentDataEditWidget.okayButtonClicked.\
            connect(self.accept)
        self.priceChartDocumentDataEditWidget.cancelButtonClicked.\
            connect(self.reject)


class TimestampEditWidget(QWidget):
    """QWidget for editing/displaying timestamps.
    
    This includes the ability to set whether or not it is in daylight
    savings time or not.
    """

    # Signal emitted when timestamp value in the widget is changed.
    valueChanged = QtCore.pyqtSignal()
    
    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, timestamp=None, parent=None):
        """Initializes the widgets to hold the datetime.datetime in
        the timestamp variable.

        Arguments:
        
        timestamp - datetime.datetime object with a non-None pytz
                    timezone.  If timestamp is None, then the
                    timestamp initialized is the current time in UTC.
        """
        
        super().__init__(parent)
        
        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.TimestampEditWidget")

        # If timestamp is None, use the current time in UTC.
        if timestamp == None:
            self.log.debug("Timestamp entered to TimestampEditWidget " +
                           "is None, so using the current UTC time.")
            timestamp = datetime.datetime.now(pytz.utc)
            
        # Do some input checking.
        if not isinstance(timestamp, datetime.datetime):
            msg = "Argument 'timestamp' is expected to be a " + \
                  "datetime.datetime object."
            self.log.error(msg)
            QMessageBox.warning(self, "Programmer error", msg)
            return
        elif timestamp.tzinfo == None:
            msg = "Argument 'timestamp' is expected to have " + \
                  "tzinfo set in the datetime.datetime object as " + \
                  "a pytz.timezone object."
            self.log.error(msg)
            QMessageBox.warning(self, "Programmer error", msg)
            return
        
        # Holds the the timestamp as a datetime.datetime object.  Set
        # to 'timestamp' value via the loadTimestamp() function, which
        # is called in this function below.
        # This value is only modified after that if save is called.
        self.dt = None

        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("Timestamp:")
        
        # Date and time.
        self.datetimeLabel = QLabel("Date and Time:")
        self.datetimeEditWidget = QDateTimeEdit()
        self.datetimeEditWidget.setDisplayFormat("yyyy/MM/dd hh:mm:ss AP")
        self.datetimeEditWidget.setCalendarPopup(True)
        self.datetimeEditWidget.setMinimumDate(QDate(101, 1, 1))

        # Timezone.
        self.timezoneLabel = QLabel("Timezone:")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)

        # Daylight savings modes.
        self.daylightLabel = QLabel("Daylight savings:")
        self.daylightComboBox = QComboBox()
        
        # Form layout.
        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignLeft)
        self.formLayout.addRow(self.datetimeLabel, self.datetimeEditWidget)
        self.formLayout.addRow(self.timezoneLabel, self.timezoneComboBox)
        self.formLayout.addRow(self.daylightLabel, self.daylightComboBox)

        self.groupBox.setLayout(self.formLayout)

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

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.datetimeEditWidget.dateTimeChanged.\
            connect(self.updateDaylightComboBox)
        self.timezoneComboBox.currentIndexChanged.\
            connect(self.updateDaylightComboBox)

        # Propagate notification that something changed upwards, if
        # anyone is listening.
        self.datetimeEditWidget.dateTimeChanged.\
            connect(self.valueChanged)
        self.timezoneComboBox.currentIndexChanged.\
            connect(self.valueChanged)
        self.daylightComboBox.currentIndexChanged.\
            connect(self.valueChanged)
        
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        # Force an update of the DaylightComboBox so that it gets populated.
        self.updateDaylightComboBox()
        
        # Now that all the widgets are created, load the values from the
        # timestamp.
        self.loadTimestamp(timestamp)
        
    def setReadOnly(self, readOnlyFlag):
        """Sets whether or not the widgets can be edit-able by the user.

        Arguments:
        
        readOnlyFlag - bool value.  If True, then the widgets are not
                       editable. If False, then the widgets are editable.
        """

        # Set the widgets as readOnly or not.
        self.datetimeEditWidget.setEnabled(not readOnlyFlag)
        self.timezoneComboBox.setEnabled(not readOnlyFlag)
        self.daylightComboBox.setEnabled(not readOnlyFlag)

        # If the readOnly is not enabled, then after enabling the
        # widgets we care about, run self.updateDaylightComboBox, to get
        # the daylightComboBox into enabled or disabled mode, depending
        # of whether or not daylight savings mode is ambiguous or not
        # for that timezone.
        if readOnlyFlag == False:
            self.updateDaylightComboBox()
            

    def _getAllTzNamesForTimezone(self, tz):
        """Returns a list of str objects, which consist of all the possible
        tznames (e.g, "EST", "EDT"), that are possible in a given timezone.
        The timezone to test against is the pytz.timezone in 'tz'.

        Arguments:

        tz - pytz.timezone object to get the possible tznames from.
        """

        # Return value.
        tznames = []

        # Go through the first day of each month and try to find
        # unique strings for the tzname.  I'm just doing this because
        # it's fast, and I believe all timezones implement their
        # daylight savings time for a span of more than one month a
        # year.
        year = 2010
        day = 1

        for i in range(12):
            month = i + 1
            dt = datetime.datetime(year, month, day, tzinfo=None)
            try:
                name = tz.tzname(dt)
                if name not in tznames:
                    tznames.append(name)
            except pytz.InvalidTimeError as e:
                # Ignore.
                pass

        return sorted(tznames)
    
    def updateDaylightComboBox(self):
        """Updates the daylight savings combo box because the
        timestamp has changed or the timezone has changed.

        This field is only enabled if the timezone has more than one
        tzname (for daylight saving time and standard time).  If we
        can arrive at whether we are in DST time or standard time,
        then this widget will be set to the appropriate selection, and
        the combobox disabled.  If the timestamp and timezone settings
        make the daylightComboBox ambiguous, then the widget becomes
        enabled and user may select which one he/she wants.

        In otherwords, this widget is 'smart'.
        """

        self.log.debug("Entered updateDaylightComboBox()")
        
        # Construct a datetime.datetime object from the QDateTimeEdit
        # widget's current values.
        qdatetime = self.datetimeEditWidget.dateTime()
        qdate = qdatetime.date()
        qtime = qdatetime.time()

        dt = datetime.datetime(qdate.year(), qdate.month(), qdate.day(),
                               qtime.hour(), qtime.minute(), qtime.second())
        
        timezoneString = str(self.timezoneComboBox.currentText())
        
        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Populate with possible tznames.
        tznames = self._getAllTzNamesForTimezone(tzinfoObj)

        # See if there is any difference between the tznames obtained
        # and what is in the daylightComboBoxes.  If the entries are
        # the same, we don't need to clear and re-add them.
        needsRepopulate = False
        if len(tznames) > 0 and len(tznames) == self.daylightComboBox.count():
            for i in range(len(tznames)):
                if tznames[i] != self.daylightComboBox.itemText(i):
                    needsRepopulate = True
        else:
            needsRepopulate = True

        if needsRepopulate == True:
            self.daylightComboBox.clear()
            self.daylightComboBox.addItems(tznames)
            if len(tznames) < 2:
                self.daylightComboBox.setEnabled(False)

        # Find out if the timestamp is ambiguous.
        try:
            temp = tzinfoObj.localize(dt, is_dst=None)
            
            # If it got here, that means the timestamp is not ambiguous.
            # Select the relevant daylight savings/standard time tzname.
            tznameStr = temp.tzname()

            index = self.daylightComboBox.findText(tznameStr)
            if index != -1:
                # Set the index only if it is not currently on this index.
                if self.daylightComboBox.currentIndex() != index:
                    self.daylightComboBox.setCurrentIndex(index)

            else:
                errStr = "Couldn't find the tzname " + tznameStr + \
                         " in the combo box list of tznames."
                self.log.error(errStr)
                #QMessageBox.warning(None, "Error", errStr)
            
        except pytz.InvalidTimeError as e:
            # Timestamp is ambiguous in terms of daylight savings time.
            
            # Select the first entry in the combo box, and enable the
            # combo box so the user can pick which one he/she wants.
            if self.daylightComboBox.count() > 0:
                # Only select it if it is not already on this index.
                index = 0
                if self.daylightComboBox.currentIndex() != index:
                    self.daylightComboBox.setCurrentIndex(index)

                self.daylightComboBox.setEnabled(True)
            else:
                errStr = "Timestamp is ambiguous and there are " + \
                         "no possible find the tznames?!?  " + \
                         "How can this be?  There must be a " + \
                         "logic error in my code somewhere..."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        # If there is only one valid choice, (which we assume is
        # currently selected, then disable the combo box.
        if self.daylightComboBox.count() == 1:
            self.daylightComboBox.setEnabled(False)
            
        self.log.debug("Exiting updateDaylightComboBox()")
        
    def loadTimestamp(self, timestamp):
        """Loads the widgets with values from the given
        datetime.datetime object.
        """

        self.log.debug("Entered loadTimestamp()")

        # Check inputs.
        if timestamp == None:
            self.log.error("Invalid parameter to loadTimestamp().  " + \
                           "timestamp can't be None.")
            self.log.debug("Exiting loadTimestamp()")
            return
        elif self.dt is timestamp:
            self.log.debug("Timestamps are the same object.  " +
                           "No need to load anything new.  dt: " +
                           Ephemeris.datetimeToStr(self.dt))
            return
        else:
            if self.dt != None:
                self.log.debug("Old timestamp was: " +
                               Ephemeris.datetimeToStr(self.dt))
            self.log.debug("Loading timestamp: " +
                           Ephemeris.datetimeToStr(timestamp))
            self.dt = timestamp 


        # Convert the datetime object to the equivalent qdatetime.
        # Note: Here we are assuming timespec UTC.  This is only for
        # the information internal to QDateTimeEdit.  We keep the
        # actual timezone information in self.dt.
        date = QDate(self.dt.year, self.dt.month, self.dt.day)
        time = QTime(self.dt.hour, self.dt.minute, self.dt.second)
        timespec = Qt.UTC
        qdatetime = QDateTime(date, time, timespec)

        # Set the timestamp.
        self.datetimeEditWidget.setDateTime(qdatetime)

        # Select the timezone.
        index = self.timezoneComboBox.findText(self.dt.tzinfo.zone)
        if index != -1:
            self.timezoneComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find timezone '" + self.dt.tzinfo.zone + \
                     "' in the pytz list of timezones."
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
            return

        # Call update on the daylight combo box, just so we can get it
        # populated with the correct tznames.  That function may or
        # may not set the current index to match self.dt, so we'll
        # have to manually select the tzname ourselves.
        self.updateDaylightComboBox()

        tznameStr = self.dt.tzname()
        index = self.daylightComboBox.findText(tznameStr)
        if index != -1:
            self.daylightComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the tzname " + tznameStr + \
                     " in the combo box list of tznames."
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)


        self.log.debug("Exiting loadTimestamp()")
        
    def saveTimestamp(self):
        """Saves the values in the widgets to the 
        PriceBarChartScaling object passed in this class's constructor.
        """
    
        self.log.debug("Entered saveTimestamp()")

        # Get from the QDateTimeEdit the primitives of the timestamp.
        qdatetime = self.datetimeEditWidget.dateTime()
        qdate = qdatetime.date()
        qtime = qdatetime.time()
        year = qdate.year()
        month = qdate.month()
        day = qdate.day()
        hour = qtime.hour()
        minute = qtime.minute()
        second = qtime.second()

        # Create a native datetime with no tzinfo set.
        dt = datetime.datetime(year, month, day, hour, minute, second, \
                               tzinfo=None)
        
        # Get from the timezone combobox the Timezone string.
        timezoneString = str(self.timezoneComboBox.currentText())

        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Get whether it is in daylightSavings or not.
        
        # Here we have to replicate how we set the values in order to
        # get them, because with the pytz api, there is no other way
        # to test if it is in daylight savings time without actually
        # localizing a datetime.datetime.

        # Find out if the timestamp is ambiguous.
        try:
            localizedDt = tzinfoObj.localize(dt, is_dst=None)
            
            # If it got here, that means the timestamp is not ambiguous.
            self.dt = localizedDt
            
        except pytz.InvalidTimeError as e:
            # Timestamp is ambiguous in terms of daylight savings time.

            # See the tzname for is_dst=True and see what it is for
            # is_dst=False.
            dtDstTrue = tzinfoObj.localize(dt, is_dst=True)
            dtDstFalse = tzinfoObj.localize(dt, is_dst=False)
            
            # Compare this with what is selected in
            # self.daylightComboBox to determine if it is in
            # daylightSavings or not.
            daylightText = self.daylightComboBox.currentText()

            if daylightText == dtDstTrue.tzname():
                self.dt = dtDstTrue
            elif daylightText == dtDstFalse.tzname():
                self.dt = dtDstFalse
            else:
                errStr = "Timestamp NOT saved.  " + os.linesep + \
                         "The timestamp is ambiguous and the " + \
                         "tznames for is_dst=True and is_dst=False " + \
                         "don't match any of the possible tznames " + \
                         "in the self.daylightComboBox!  " + \
                         "This problem needs to be debugged."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        self.log.debug("Exiting saveTimestamp()")

    def getTimestamp(self):
        """Gets and returns the timestamp as saved in this widget.
        This value only matches what is in the widgets if nothing has
        changed, or if saveTimestamp() has been called previous to
        calling this function.

        Returns:

        datetime.datetime object with it's date and time set, and with
        tzinfo set to a valid pytz.timezone object.
        """

        return self.dt
        
    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveTimestamp()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class TimestampEditDialog(QDialog):
    """QDialog for editing timestamps.
    
    This includes the timezone information (and whether in daylight
    savings or not).
    """

    def __init__(self, timestamp, parent=None):
        """Initializes the internal widgets to hold the
        datetime.datetime in the timestamp variable.

        Arguments:
        timestamp - datetime.datetime object with a non-None pytz timezone.
        """
        
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.TimestampEditDialog")

        self.setWindowTitle("Timestamp")

        # Save a reference to the datetime.datetime timestamp.
        self.dt = timestamp
        
        # Create the contents.
        self.editWidget = TimestampEditWidget(self.dt)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getTimestamp(self):
        """Returns the internally stored timestamp.

        Returns:

        datetime.datetime object with the tzinfo set to a pytz.timezone.
        This datetime.datetime is the timestamp as edited by the dialog.
        """

        self.dt = self.editWidget.getTimestamp()
        
        return self.dt

    
class PriceBarTagEditWidget(QWidget):
    """QWidget for editing the tags on a PriceBar.
    
    The tags associated with a PriceBar are just a list of strings
    that may have meaning to that particular PriceBar.
    
    For example, different schemes can be used, for example,"H",
    used for a high within 5 bars... and "LL" used for a
    low within 10 bars, etc.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, tags=[], parent=None):
        """Initializes the edit widget with the given values.

        Arguments:

        tags   - list of str objects.
                 This is the list of tag strings we are editing.

        parent - QWidget parent
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarTagEditWidget")

        # Save off the list of tags.
        self.tags = list(tags)

        self.tagsListGroupBox = \
            QGroupBox("List of PriceBar tags:")

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout to hold the list widget.
        self.listWidgetLayout = QVBoxLayout()
        self.listWidgetLayout.addWidget(self.listWidget)

        self.tagsListGroupBox.setLayout(self.listWidgetLayout)
        
        # Buttons for doing actions like adding, removing, and editing a
        # tag, etc.

        self.addTagButton = QPushButton("&Add Tag")
        self.removeTagButton = QPushButton("&Remove Tag")
        self.editTagButton = QPushButton("&Edit Tag")
        self.moveSelectedTagUpButton = QPushButton("Move Tag &up")
        self.moveSelectedTagDownButton = QPushButton("Move Tag &down")

        self.buttonsOnRightLayout = QVBoxLayout()
        self.buttonsOnRightLayout.addWidget(self.addTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.removeTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.editTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedTagUpButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedTagDownButton)
        self.buttonsOnRightLayout.addStretch()

        self.mainWidgetsLayout = QHBoxLayout()
        self.mainWidgetsLayout.addWidget(self.tagsListGroupBox)
        self.mainWidgetsLayout.addLayout(self.buttonsOnRightLayout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.mainWidgetsLayout) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.
        self.listWidget.itemDoubleClicked.\
            connect(self._handleEditTagButtonClicked)
        self.addTagButton.clicked.\
            connect(self._handleAddTagButtonClicked)
        self.removeTagButton.clicked.\
            connect(self._handleRemoveTagButtonClicked)
        self.editTagButton.clicked.\
            connect(self._handleEditTagButtonClicked)
        self.moveSelectedTagUpButton.clicked.\
            connect(self._handleMoveTagUpButtonClicked)
        self.moveSelectedTagDownButton.clicked.\
            connect(self._handleMoveTagDownButtonClicked)

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadTags(self.tags)


    def loadTags(self, tags):
        """Loads the widgets with values from the given arguments.

        Arguments:

        tags - list of str objects.
        """

        self.log.debug("Entered loadTags()")

        # Save off the values.
        self.tags = list(tags)

        # Populate the QListWidget with the tags.
        self.listWidget.clear()
        for tag in self.tags:
            self._appendTagAsListWidgetItem(tag, False)

        if self.listWidget.count() > 0:
            self.listWidget.setCurrentRow(0)

        self.log.debug("Exiting loadTags()")
        
    def saveTags(self):
        """Ensures the values in the widgets are saved to their
        underlying variables, such that subsequent calls to getTags()
        will return valid values for what has changed.
        """
    
        self.log.debug("Entered saveTag()")

        self.tags = []

        numTags = self.listWidget.count()
        
        for i in range(numTags):
            item = self.listWidget.item(i)
            
            self.tags.append(item.text())
        
        self.log.debug("Exiting saveTag()")


    def getTags(self):
        """Returns the internally stored list of tags which are really
        just a list of str objects.  This may or may not represent
        what is in the widgets, depending on whether or not saveTags
        has been called recently.
        """

        return self.tags

    def _appendTagAsListWidgetItem(self, tag, selectItem=True):
        """Appends the given Tag str object to the
        QListWidget as a QListWidgetItem.

        Arguments:
        
        tag - str which represents the PriceBar tag.

        selectItem - bool flag that indicates whether the item should be
        selected after being created and appended to the list.
        """

        listWidgetItem = QListWidgetItem()

        listWidgetItem.setText(tag)

        self.listWidget.addItem(listWidgetItem)
        
        if selectItem == True:
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)


    def _handleAddTagButtonClicked(self):
        """Called when the 'Add Tag' button is clicked."""

        # Create a dialog and allow the user to edit it.
        accepted = False

        parent = self
        title = "New Tag"
        label = "Tag:"
        echoMode = QLineEdit.Normal
        initialText = ""
        
        (text, accepted) = \
            QInputDialog.getText(parent, title, label, echoMode, initialText)
        
        if accepted == True:
            tag = text.strip()
            if tag != "":
                self._appendTagAsListWidgetItem(tag, True)

    def _handleRemoveTagButtonClicked(self):
        """Called when the 'Remove Tag' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        if row >= 0 and row < self.listWidget.count():
            # It is a valid row.

            # First remove the item from the QListWidget.
            self.listWidget.takeItem(row)

            # If there is another item after that one in the list, then
            # select that one as the current, otherwise select the index
            # before.
            if self.listWidget.item(row) != None:
                # There an item after this one, so set that one as the
                # current.
                self.listWidget.setCurrentRow(row)
            else:
                # The one we just removed was the last item in the
                # list.  Select the one before it if it exists,
                # otherwise, clear out the display fields.
                if row != 0:
                    self.listWidget.setCurrentRow(row - 1)

    def _handleEditTagButtonClicked(self):
        """Called when the 'Edit Tag' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Get the selected item.
        item = self.listWidget.item(row)
        
        # Get the str for editing.
        tag = item.text()
        
        # Create a dialog and allow the user to edit it.
        accepted = False

        parent = self
        title = "Edit Tag"
        label = "Tag:"
        echoMode = QLineEdit.Normal
        initialText = tag
        
        (text, accepted) = \
            QInputDialog.getText(parent, title, label, echoMode, initialText)
        
        if accepted == True:
            text = text.strip()
            if text != "" and text != tag:
                item.setText(text)

    def _handleMoveTagUpButtonClicked(self):
        """Called when the 'Move tag up' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected tag is not the top entry in the
        # QListWidget.
        if row > 0:
            # It is not the top row yet, so we can do a swap to move it
            # higher.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, currItem)

            # Set the selected row as the same underlying tag.
            self.listWidget.setCurrentRow(row - 1)

    def _handleMoveTagDownButtonClicked(self):
        """Called when the 'Move tag down' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected tag is not the bottom entry in
        # the QListWidget.
        if row < (self.listWidget.count() - 1) and row >= 0:
            # It is not the bottom row yet, so we can do a swap to move it
            # lower.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, currItem)

            # Set the selected row as the same underlying tag.
            self.listWidget.setCurrentRow(row + 1)

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveTags()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()

class PriceBarTagEditDialog(QDialog):
    """QDialog for editing the tags on a PriceBar.

    The tags associated with a PriceBar are just a list of strings
    that may have meaning to that particular PriceBar.
    
    For example, different schemes can be used, for example,"H",
    used for a high within 5 bars... and "LL" used for a
    low within 10 bars, etc.
    """

    def __init__(self, tags=[], parent=None):
        """Initializes the internal edit widget with the given values.

        Arguments:

        tags   - list of str objects.
                 This is the list of tag strings we are editing.

        parent - QWidget parent
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widget.PriceBarTagEditDialog")

        self.setWindowTitle("PriceBar Tags")

        # Save a reference to the PriceBarChartScaling object.
        self.tags = tags

        # Create the contents.
        self.editWidget = PriceBarTagEditWidget(self.tags)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getTags(self):
        """Returns the internally stored tags.

        Returns:

        list of str objects.  Each str object in the list is a tag.
        """

        self.tags = self.editWidget.getTags()
        
        return self.tags


class PriceBarEditWidget(QWidget):
    """QWidget for editing the a PriceBar."""

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, priceBar, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarEditWidget")

        # Save off the PriceBarChartScaling object.
        self.priceBar = priceBar

        # Read-Only flag.
        self.readOnlyFlag = False

        # PriceBar tags, stored in this variable instead of an edit widget.
        # Upon loading a new PriceBar, this variable is set.
        self.tags = []
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = \
            QGroupBox("PriceBar:")

        # Timestamp.
        self.timestampEditWidget = TimestampEditWidget()
        self.timestampEditWidget.okayButton.setVisible(False)
        self.timestampEditWidget.cancelButton.setVisible(False)

        # Open price.
        self.openPriceLabel = QLabel("Open Price:")
        self.openPriceSpinBox = QDoubleSpinBox()
        self.openPriceSpinBox.setMinimum(0.0)
        self.openPriceSpinBox.setMaximum(999999999.0)

        # High price.
        self.highPriceLabel = QLabel("High Price:")
        self.highPriceSpinBox = QDoubleSpinBox()
        self.highPriceSpinBox.setMinimum(0.0)
        self.highPriceSpinBox.setMaximum(999999999.0)

        # Low price.
        self.lowPriceLabel = QLabel("Low Price:")
        self.lowPriceSpinBox = QDoubleSpinBox()
        self.lowPriceSpinBox.setMinimum(0.0)
        self.lowPriceSpinBox.setMaximum(999999999.0)

        # Close price.
        self.closePriceLabel = QLabel("Close Price:")
        self.closePriceSpinBox = QDoubleSpinBox()
        self.closePriceSpinBox.setMinimum(0.0)
        self.closePriceSpinBox.setMaximum(999999999.0)

        # Open interest.
        self.openInterestLabel = QLabel("Open Interest:")
        self.openInterestSpinBox = QDoubleSpinBox()
        self.openInterestSpinBox.setMinimum(0.0)
        self.openInterestSpinBox.setMaximum(999999999.0)

        # Volume.
        self.volumeLabel = QLabel("Volume:")
        self.volumeSpinBox = QDoubleSpinBox()
        self.volumeSpinBox.setMinimum(0.0)
        self.volumeSpinBox.setMaximum(999999999.0)

        # Tags.
        self.tagsListWidget = QListWidget()
        self.tagsListWidget.clear()
        self.tagsListWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout and groupbox to hold the tags list widget.
        self.listWidgetLayout = QVBoxLayout()
        self.listWidgetLayout.addWidget(self.tagsListWidget)
        self.tagsListGroupBox = QGroupBox("Tags:")
        self.tagsListGroupBox.setLayout(self.listWidgetLayout)
        self.tagsListEditButton = QPushButton("Edit Tags")

        # Set widgets in the layouts.
        self.timestampLayout = QVBoxLayout()
        self.timestampLayout.addWidget(self.timestampEditWidget)

        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignLeft)
        self.formLayout.addRow(self.openPriceLabel, 
                               self.openPriceSpinBox)
        self.formLayout.addRow(self.highPriceLabel, 
                               self.highPriceSpinBox)
        self.formLayout.addRow(self.lowPriceLabel, 
                               self.lowPriceSpinBox)
        self.formLayout.addRow(self.closePriceLabel, 
                               self.closePriceSpinBox)
        self.formLayout.addRow(self.openInterestLabel, 
                               self.openInterestSpinBox)
        self.formLayout.addRow(self.volumeLabel, 
                               self.volumeSpinBox)

        self.tagsFormLayout = QFormLayout()
        self.tagsFormLayout.setLabelAlignment(Qt.AlignLeft)
        self.tagsFormLayout.addRow(self.tagsListGroupBox, 
                                   self.tagsListEditButton)

        self.priceActionGroupBox = QGroupBox("Price Action:")
        self.priceActionGroupBox.setLayout(self.formLayout)

        self.editWidgetsLayout = QVBoxLayout()
        self.editWidgetsLayout.addLayout(self.timestampLayout)
        self.editWidgetsLayout.addWidget(self.priceActionGroupBox)
        self.editWidgetsLayout.addLayout(self.tagsFormLayout)
        
        self.groupBox.setLayout(self.editWidgetsLayout)

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
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadPriceBar(self.priceBar)

        # Connect signals and slots.
        self.tagsListEditButton.clicked.\
            connect(self._handleTagsListEditButtonClicked)
        
        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setReadOnly(self, readOnlyFlag):
        """Sets the flag that indicates that this widget is in
        read-only mode.  The effect of this is that the user cannot
        edit any of the fields in the PriceBar.
        """
        
        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.timestampEditWidget.setReadOnly(self.readOnlyFlag)
        self.openPriceSpinBox.setEnabled(not self.readOnlyFlag)
        self.highPriceSpinBox.setEnabled(not self.readOnlyFlag)
        self.lowPriceSpinBox.setEnabled(not self.readOnlyFlag)
        self.closePriceSpinBox.setEnabled(not self.readOnlyFlag)
        self.openInterestSpinBox.setEnabled(not self.readOnlyFlag)
        self.volumeSpinBox.setEnabled(not self.readOnlyFlag)
        self.tagsListEditButton.setEnabled(not self.readOnlyFlag)

        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self, readOnlyFlag):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadPriceBar(self, priceBar):
        """Loads the widgets with values from the given
        PriceBar object.
        """

        self.log.debug("Entered loadPriceBar()")

        # Check inputs.
        if priceBar == None:
            self.log.error("Invalid parameter to loadPriceBar().  " + \
                           "priceBar can't be None.")
            self.log.debug("Exiting priceBar()")
            return
        else:
            self.priceBar = priceBar 

        self.timestampEditWidget.loadTimestamp(self.priceBar.timestamp)
        self.openPriceSpinBox.setValue(self.priceBar.open)
        self.highPriceSpinBox.setValue(self.priceBar.high)
        self.lowPriceSpinBox.setValue(self.priceBar.low)
        self.closePriceSpinBox.setValue(self.priceBar.close)
        self.openInterestSpinBox.setValue(self.priceBar.oi)
        self.volumeSpinBox.setValue(self.priceBar.vol)

        self.tags = list(self.priceBar.tags)
        
        # Populate the tagsListWidget with the str objects in
        # self.priceBar.tags.
        self.tagsListWidget.clear();
        for tag in self.tags:
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setText(tag)
            self.tagsListWidget.addItem(listWidgetItem)
        if self.tagsListWidget.count() > 0:
            self.tagsListWidget.setCurrentRow(0)
            
        self.log.debug("Exiting loadPriceBar()")
        
    def savePriceBar(self):
        """Saves the values in the widgets to the 
        PriceBar object passed in this class's constructor.
        """
    
        self.log.debug("Entered savePriceBar()")
        
        self.priceBar.timestamp = self.timestampEditWidget.getTimestamp()
        self.priceBar.open = self.openPriceSpinBox.value()
        self.priceBar.high = self.highPriceSpinBox.value()
        self.priceBar.low = self.lowPriceSpinBox.value()
        self.priceBar.close = self.closePriceSpinBox.value()
        self.priceBar.oi = self.openInterestSpinBox.value()
        self.priceBar.vol = self.volumeSpinBox.value()
        self.priceBar.tags = self.tags

        self.log.debug("Exiting savePriceBar()")

    def getPriceBar(self):
        """Returns the internally stored PriceBar object.
        This may or may not represent what is in the widgets, depending on
        whether or not savePriceBar() has been called.
        """

        return self.priceBar

    def setOkayCancelButtonsVisible(self, visibleFlag):
        """Hides or shows the Okay and Cancel buttons depending on the
        value of visibleFlag.

        Arguments:
        
        visibleFlag - bool value for whether or not to show the Okay
        and Cancel buttons.  If True, then the buttons are visible.
        If False, then the buttons are hidden.  The buttons are
        visible by default.
        """

        self.okayButton.setVisible(visibleFlag)
        self.cancelButton.setVisible(visibleFlag)

    def getOkayCancelButtonsVisible(self):
        """Returns whether or not the Okay and Cancel buttons are visible.

        Returns:
        bool value for whether or not the okay and cancel buttons are visible.
        """

        if self.okayButton.isVisible() and self.cancelButton.isVisible():
            return True
        else:
            return False

    def _handleTagsListEditButtonClicked(self):
        """Called when the 'Edit Tags' button is clicked.
        Opens up a dialog for editing the list of tags.
        """

        dialog = PriceBarTagEditDialog(self.tags, self)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # Set to self.tags, the values from the QDialog.
            self.tags = dialog.getTags()

            # Clear the list of tags displayed, reset them with the
            # new values.
            self.tagsListWidget.clear();
            for tag in self.tags:
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setText(tag)
                self.tagsListWidget.addItem(listWidgetItem)
            if self.tagsListWidget.count() > 0:
                self.tagsListWidget.setCurrentRow(0)
        
        
    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        # Only save if the readOnlyFlag is False.
        if self.readOnlyFlag == False:
            self.timestampEditWidget.saveTimestamp()
            self.savePriceBar()

        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarEditDialog(QDialog):
    """QDialog for editing a PriceBar (the fields in it)."""

    def __init__(self, priceBar, readOnly=False, parent=None):
        """Initializes the internal widgets to hold the
        PriceBar in the priceBar variable.

        Arguments:
        
        priceBar - PriceBar object to edit or view in the dialog.
        
        readOnly - bool value for whether or not the user is allowed
                   to edit the fields in the given PriceBar.  If the
                   value is True, then the buttons and widgets allow
                   for modification.  If the value is False, then the
                   fields are viewable only.
        """
        
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarEditDialog")

        self.setWindowTitle("PriceBar")

        # Save a reference to the PriceBar.
        self.priceBar = priceBar

        # Save the readOnly preference.
        self.readOnly = readOnly
        
        # Create the contents.
        self.editWidget = PriceBarEditWidget(self.priceBar)
        self.editWidget.setReadOnly(self.readOnly)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getPriceBar(self):
        """Returns the internally stored timestamp.

        Returns:
        PriceBar holding the edited PriceBar.  If the widget is in
        ReadOnly mode, or the user clicked the Cancel button, then the
        PriceBar is unchanged.
        """

        self.priceBar = self.editWidget.getPriceBar()
        
        return self.priceBar

    def loadPriceBar(self, priceBar):
        """Loads the widgets with values from the given
        PriceBar object.

        Arguments:
        priceBar - PriceBar object to load into the widgets.
        """

        self.priceBar = priceBar
        self.editWidget.loadPriceBar(self.priceBar)
        
    def setReadOnly(self, readOnly):
        """Sets the readOnly flag to the value given in 'readOnly'.

        Arguments:
        readOnly - bool value.  If True, then the widgets are made to
        be unmodifiable.  If False, then the widgets can be changed
        and the priceBar can be modified.
        """
        
        self.readOnly = readOnly
        self.editWidget.setReadOnly(self.readOnly)

    def getReadOnly(self):
        """Returns the current setting of the readOnly flag.

        Returns:
        bool value representing whether or not the PriceBar can be modified.
        """

        return self.readOnly


def testPriceChartDocumentLoadDataFileWizardPage():
    print("Running " + inspect.stack()[0][3] + "()")
    loadDataFileWizardPage = \
        PriceChartDocumentLoadDataFileWizardPage()
    loadDataFileWizardPage.show()

def testLoadDataFileWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    loadDataFileWidget = LoadDataFileWidget()
    loadDataFileWidget.show()

def testPriceChartDocumentLocationTimezoneWizardPage():
    print("Running " + inspect.stack()[0][3] + "()")
    locationTimezoneWizardPage = \
        PriceChartDocumentLocationTimezoneWizardPage()
    locationTimezoneWizardPage.show()

def testLocationTimezoneEditWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    locationTimezoneEditWidget = LocationTimezoneEditWidget()
    locationTimezoneEditWidget.show()

def testBirthInfoEditWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    bew = BirthInfoEditWidget()
    bew.show()

def testBirthInfoEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    bied = BirthInfoEditDialog()
    if bied.exec_() == QDialog.Accepted:
        print("Accepted!")
        print("BirthInfo accepted is: " + bied.getBirthInfo().toString())
    else:
        print("Rejected!")

        
def testPriceChartDocumentWizard():
    print("Running " + inspect.stack()[0][3] + "()")
    wizard = PriceChartDocumentWizard()
    
    returnVal = wizard.exec_()
    
    if returnVal == QDialog.Accepted:
        print("Accepted!");
        print("Data filename is: " + wizard.field("dataFilename"))
        print("Data num lines to skip is: {}".\
            format(wizard.field("dataNumLinesToSkip")))
        print("Timezone is: " + wizard.field("timezone"))
    else:
        print("Rejected!")

    
def testPriceBarChartScalingsListEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    scaling1 = PriceBarChartScaling(name="Identity", 
                                    description="1description",
                                    unitsOfTime=4.0, 
                                    unitsOfPrice=8.0)
    scaling2 = PriceBarChartScaling(name="2", 
                                    description="2description",
                                    unitsOfTime=2.0, 
                                    unitsOfPrice=4.0)
    scaling3 = PriceBarChartScaling(name="3", 
                                    description="3description dQt::RichText	1The text string is interpreted as a rich text string. Qt::AutoText",
                                    unitsOfTime=1.0, 
                                    unitsOfPrice=2.0)
    scaling4 = PriceBarChartScaling(name="4", 
                                    description="4description",
                                    unitsOfTime=4.0, 
                                    unitsOfPrice=4.0)
    scaling5 = PriceBarChartScaling(name="5", 
                                    description="5description",
                                    unitsOfTime=2.0, 
                                    unitsOfPrice=2.0)
    scaling6 = PriceBarChartScaling(name="6", 
                                    description="6description",
                                    unitsOfTime=1.0, 
                                    unitsOfPrice=1.0)
    
    scalings = [scaling1, scaling2, scaling3, scaling4, scaling5, scaling6]
    index = 1

    dialog = PriceBarChartScalingsListEditDialog(scalings, index)

    returnVal = dialog.exec_()

    if returnVal == QDialog.Accepted:
        print("Accepted!");

        scalings = dialog.getPriceBarChartScalings()
        index = dialog.getPriceBarChartScalingsIndex()
    else:
        print("Rejected!")


    for i in range(len(scalings)):
        print("Scaling is: " + scalings[i].toString())
    print("Index of 'current' is: {}".format(index))
    
def testTimestampEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")

    # Different timestamps to try:
    dt = datetime.datetime.now(pytz.timezone("US/Eastern"))
    dt = datetime.datetime.now(pytz.utc)

    print("Timestamp before: {}".format(Ephemeris.datetimeToStr(dt)))
    
    dialog = TimestampEditDialog(dt)

    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted.")
    else:
        print("Rejected.")
    print("Timestamp after: {}".format(Ephemeris.datetimeToStr(dt)))

    dt = dialog.getTimestamp()
    print("Timestamp new: {}".format(Ephemeris.datetimeToStr(dt)))
        
def testPriceBarTagEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")

    tags = ["hello", "myname_is", "a happy camper", "LLLL", "HH"]
    print("Tags before: {}".format(tags))
    
    dialog = PriceBarTagEditDialog(tags)
    
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
        tags = dialog.getTags()
        print("Tags after: {}".format(tags))
    else:
        print("Rejected")
        tags = dialog.getTags()
        print("Tags after: {}".format(tags))

def testPriceBarEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")

    pb1tags = ["HH", "L", "LLLL", "HappyTag"]
    pb1 = PriceBar(datetime.datetime.now(pytz.utc),
                   5, 9, 1, 5, 100, 200, pb1tags)
    
    pb2tags = ["LL", "HL", "HHHH", "Tag324"]
    pb2 = PriceBar(datetime.datetime.now(pytz.utc),
                   5, 10, 2, 5, 200, 400, pb2tags)

    pb3tags = ["asdf", "qwer", "z", "ZXXXZ"]
    pb3 = PriceBar(datetime.datetime.now(pytz.utc),
                   5, 8, 3, 5, 300, 600, pb3tags)

    print("PriceBar before: {}".format(pb1.toString()))

    #dialog = PriceBarEditDialog(pb1, readOnly=True)
    dialog = PriceBarEditDialog(pb1, readOnly=False)
    
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")

    print("PriceBar: {}".format(pb1.toString()))
    pb1 = dialog.getPriceBar()
    print("PriceBar after mods: {}".format(pb1.toString()))
    
    priceBars = []
    priceBars.append(pb1)
    priceBars.append(pb2)
    priceBars.append(pb3)
    


# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
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

    #testPriceChartDocumentLoadDataFileWizardPage()
    #testLoadDataFileWidget()
    #testPriceChartDocumentLocationTimezoneWizardPage()
    #testLocationTimezoneEditWidget()
    #testBirthInfoEditWidget()
    #testBirthInfoEditDialog()
    #testPriceChartDocumentWizard()
    #testPriceBarChartScalingsListEditDialog()
    #testTimestampEditDialog()
    #testPriceBarTagEditDialog()
    #testPriceBarEditDialog()
    

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()


    #app.exec_()
    

