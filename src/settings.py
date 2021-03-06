


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class SettingsKeys():
    """Static class that holds keys that are used in the QSettings storage."""

    
    # QSettings key for the defaultPriceBarDataOpenDirectory.
    defaultPriceBarDataOpenDirectorySettingsKey = \
        "ui/defaultPriceBarDataOpenDirectory"

    # QSettings key for zoomScaleFactor (float).
    zoomScaleFactorSettingsKey = \
        "ui/pricebarchart/zoomScaleFactor"

    # QSettings default value for zoomScaleFactor (float).
    zoomScaleFactorSettingsDefValue = 1.2
    
    # QSettings key for the higherPriceBarColor (QColor object).
    higherPriceBarColorSettingsKey = \
        "ui/pricebarchart/higherPriceBarColor"

    # QSettings default value for the higherPriceBarColor (QColor object).
    higherPriceBarColorSettingsDefValue = QColor(0, 128, 0, 255)

    # QSettings key for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsKey = \
        "ui/pricebarchart/lowerPriceBarColor"

    # QSettings default value for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsDefValue = QColor(128, 0, 0, 255)

    # QSettings key for the computation model of LookbackMultiples
    # (LookbackMultipleCalcModel Enum, expressed as a str).
    lookbackMultipleCalcModelKey = \
        "lookbackmultiple/calcModel"
    
    # QSettings default value for the computation model of LookbackMultiples
    # (LookbackMultipleCalcModel Enum, expressed as a str).
    lookbackMultipleCalcModelDefValue = \
        "LookbackMultipleCalcModel.local_parallel"
    
    # QSettings key for the server address used for LookbackMultiple
    # calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerAddressKey = \
        "lookbackmultiple/serverAddress"
    
    # QSettings default value for the server address used for
    # LookbackMultiple calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerAddressDefValue = "localhost"
    
    # QSettings key for the server port used for LookbackMultiple
    # calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerPortKey = \
        "lookbackmultiple/serverPort"
    
    # QSettings default value for the server port used for
    # LookbackMultiple calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerPortDefValue = 1940
    
    # QSettings key for the server auth key used for LookbackMultiple
    # calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerAuthKeyKey = \
        "lookbackmultiple/serverAuthKey"
    
    # QSettings default value for the server auth key used for
    # LookbackMultiple calculation, running parallel distributed.
    lookbackMultipleCalcRemoteServerAuthKeyDefValue = "password"
    
    # QSettings key for the BarCountGraphicsItem color (QColor object).
    barCountGraphicsItemColorSettingsKey = \
        "ui/pricebarchart/barCountGraphicsItemColor"

    # QSettings default value for the BarCountGraphicsItem color (QColor object).
    barCountGraphicsItemColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the BarCountGraphicsItem text color (QColor object).
    barCountGraphicsItemTextColorSettingsKey = \
        "ui/pricebarchart/barCountGraphicsItemTextColor"

    # QSettings default value for the BarCountGraphicsItem text color (QColor object).
    barCountGraphicsItemTextColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the ModalScaleGraphicsItem color (QColor object).
    modalScaleGraphicsItemColorSettingsKey = \
        "ui/pricebarchart/modalScaleGraphicsItemColor"

    # QSettings default value for the ModalScaleGraphicsItem color (QColor object).
    modalScaleGraphicsItemColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the ModalScaleGraphicsItem text color (QColor object).
    modalScaleGraphicsItemTextColorSettingsKey = \
        "ui/pricebarchart/modalScaleGraphicsItemTextColor"

    # QSettings default value for the ModalScaleGraphicsItem text color (QColor object).
    modalScaleGraphicsItemTextColorSettingsDefValue = QColor(Qt.black)


    # QSettings key for the planet glyph unicode of the Retrograde.
    planetRetrogradeGlyphUnicodeKey = \
        "ui/astrology/retrogradeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Retrograde.
    planetRetrogradeGlyphUnicodeDefValue = "\u211e"

    # QSettings key for the planet glyph font size of the Retrograde.
    planetRetrogradeGlyphFontSizeKey = \
        "ui/astrology/retrogradeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Retrograde.
    planetRetrogradeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Retrograde.
    planetRetrogradeAbbreviationKey = \
        "ui/astrology/retrogradeAbbreviation"

    # QSettings default value for the planet abbreviation of the Retrograde.
    planetRetrogradeAbbreviationDefValue = "Rx"

    # QSettings key for the foreground color of the Retrograde.
    planetRetrogradeForegroundColorKey = \
        "ui/astrology/retrogradeForegroundColor"

    # QSettings default value for the foreground color of the Retrograde.
    planetRetrogradeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Retrograde.
    planetRetrogradeBackgroundColorKey = \
        "ui/astrology/retrogradeBackgroundColor"

    # QSettings default value for the background color of the Retrograde.
    planetRetrogradeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H1.
    planetH1GlyphUnicodeKey = \
        "ui/astrology/H1GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H1.
    planetH1GlyphUnicodeDefValue = "As"

    # QSettings key for the planet glyph font size of the H1.
    planetH1GlyphFontSizeKey = \
        "ui/astrology/H1GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H1.
    planetH1GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H1.
    planetH1AbbreviationKey = \
        "ui/astrology/H1Abbreviation"

    # QSettings default value for the planet abbreviation of the H1.
    planetH1AbbreviationDefValue = "As"

    # QSettings key for the foreground color of the H1.
    planetH1ForegroundColorKey = \
        "ui/astrology/H1ForegroundColor"

    # QSettings default value for the foreground color of the H1.
    planetH1ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H1.
    planetH1BackgroundColorKey = \
        "ui/astrology/H1BackgroundColor"

    # QSettings default value for the background color of the H1.
    planetH1BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeKey = \
        "ui/astrology/H2GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeDefValue = "H2"

    # QSettings key for the planet glyph font size of the H2.
    planetH2GlyphFontSizeKey = \
        "ui/astrology/H2GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H2.
    planetH2GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H2.
    planetH2AbbreviationKey = \
        "ui/astrology/H2Abbreviation"

    # QSettings default value for the planet abbreviation of the H2.
    planetH2AbbreviationDefValue = "H2"

    # QSettings key for the foreground color of the H2.
    planetH2ForegroundColorKey = \
        "ui/astrology/H2ForegroundColor"

    # QSettings default value for the foreground color of the H2.
    planetH2ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H2.
    planetH2BackgroundColorKey = \
        "ui/astrology/H2BackgroundColor"

    # QSettings default value for the background color of the H2.
    planetH2BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeKey = \
        "ui/astrology/H3GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeDefValue = "H3"

    # QSettings key for the planet glyph font size of the H3.
    planetH3GlyphFontSizeKey = \
        "ui/astrology/H3GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H3.
    planetH3GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H3.
    planetH3AbbreviationKey = \
        "ui/astrology/H3Abbreviation"

    # QSettings default value for the planet abbreviation of the H3.
    planetH3AbbreviationDefValue = "H3"

    # QSettings key for the foreground color of the H3.
    planetH3ForegroundColorKey = \
        "ui/astrology/H3ForegroundColor"

    # QSettings default value for the foreground color of the H3.
    planetH3ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H3.
    planetH3BackgroundColorKey = \
        "ui/astrology/H3BackgroundColor"

    # QSettings default value for the background color of the H3.
    planetH3BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeKey = \
        "ui/astrology/H4GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeDefValue = "H4"

    # QSettings key for the planet glyph font size of the H4.
    planetH4GlyphFontSizeKey = \
        "ui/astrology/H4GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H4.
    planetH4GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H4.
    planetH4AbbreviationKey = \
        "ui/astrology/H4Abbreviation"

    # QSettings default value for the planet abbreviation of the H4.
    planetH4AbbreviationDefValue = "H4"

    # QSettings key for the foreground color of the H4.
    planetH4ForegroundColorKey = \
        "ui/astrology/H4ForegroundColor"

    # QSettings default value for the foreground color of the H4.
    planetH4ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H4.
    planetH4BackgroundColorKey = \
        "ui/astrology/H4BackgroundColor"

    # QSettings default value for the background color of the H4.
    planetH4BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeKey = \
        "ui/astrology/H5GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeDefValue = "H5"

    # QSettings key for the planet glyph font size of the H5.
    planetH5GlyphFontSizeKey = \
        "ui/astrology/H5GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H5.
    planetH5GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H5.
    planetH5AbbreviationKey = \
        "ui/astrology/H5Abbreviation"

    # QSettings default value for the planet abbreviation of the H5.
    planetH5AbbreviationDefValue = "H5"

    # QSettings key for the foreground color of the H5.
    planetH5ForegroundColorKey = \
        "ui/astrology/H5ForegroundColor"

    # QSettings default value for the foreground color of the H5.
    planetH5ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H5.
    planetH5BackgroundColorKey = \
        "ui/astrology/H5BackgroundColor"

    # QSettings default value for the background color of the H5.
    planetH5BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeKey = \
        "ui/astrology/H6GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeDefValue = "H6"

    # QSettings key for the planet glyph font size of the H6.
    planetH6GlyphFontSizeKey = \
        "ui/astrology/H6GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H6.
    planetH6GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H6.
    planetH6AbbreviationKey = \
        "ui/astrology/H6Abbreviation"

    # QSettings default value for the planet abbreviation of the H6.
    planetH6AbbreviationDefValue = "H6"

    # QSettings key for the foreground color of the H6.
    planetH6ForegroundColorKey = \
        "ui/astrology/H6ForegroundColor"

    # QSettings default value for the foreground color of the H6.
    planetH6ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H6.
    planetH6BackgroundColorKey = \
        "ui/astrology/H6BackgroundColor"

    # QSettings default value for the background color of the H6.
    planetH6BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeKey = \
        "ui/astrology/H7GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeDefValue = "H7"

    # QSettings key for the planet glyph font size of the H7.
    planetH7GlyphFontSizeKey = \
        "ui/astrology/H7GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H7.
    planetH7GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H7.
    planetH7AbbreviationKey = \
        "ui/astrology/H7Abbreviation"

    # QSettings default value for the planet abbreviation of the H7.
    planetH7AbbreviationDefValue = "H7"

    # QSettings key for the foreground color of the H7.
    planetH7ForegroundColorKey = \
        "ui/astrology/H7ForegroundColor"

    # QSettings default value for the foreground color of the H7.
    planetH7ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H7.
    planetH7BackgroundColorKey = \
        "ui/astrology/H7BackgroundColor"

    # QSettings default value for the background color of the H7.
    planetH7BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeKey = \
        "ui/astrology/H8GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeDefValue = "H8"

    # QSettings key for the planet glyph font size of the H8.
    planetH8GlyphFontSizeKey = \
        "ui/astrology/H8GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H8.
    planetH8GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H8.
    planetH8AbbreviationKey = \
        "ui/astrology/H8Abbreviation"

    # QSettings default value for the planet abbreviation of the H8.
    planetH8AbbreviationDefValue = "H8"

    # QSettings key for the foreground color of the H8.
    planetH8ForegroundColorKey = \
        "ui/astrology/H8ForegroundColor"

    # QSettings default value for the foreground color of the H8.
    planetH8ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H8.
    planetH8BackgroundColorKey = \
        "ui/astrology/H8BackgroundColor"

    # QSettings default value for the background color of the H8.
    planetH8BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeKey = \
        "ui/astrology/H9GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeDefValue = "H9"

    # QSettings key for the planet glyph font size of the H9.
    planetH9GlyphFontSizeKey = \
        "ui/astrology/H9GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H9.
    planetH9GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H9.
    planetH9AbbreviationKey = \
        "ui/astrology/H9Abbreviation"

    # QSettings default value for the planet abbreviation of the H9.
    planetH9AbbreviationDefValue = "H9"

    # QSettings key for the foreground color of the H9.
    planetH9ForegroundColorKey = \
        "ui/astrology/H9ForegroundColor"

    # QSettings default value for the foreground color of the H9.
    planetH9ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H9.
    planetH9BackgroundColorKey = \
        "ui/astrology/H9BackgroundColor"

    # QSettings default value for the background color of the H9.
    planetH9BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeKey = \
        "ui/astrology/H10GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeDefValue = "H10"

    # QSettings key for the planet glyph font size of the H10.
    planetH10GlyphFontSizeKey = \
        "ui/astrology/H10GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H10.
    planetH10GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H10.
    planetH10AbbreviationKey = \
        "ui/astrology/H10Abbreviation"

    # QSettings default value for the planet abbreviation of the H10.
    planetH10AbbreviationDefValue = "H10"

    # QSettings key for the foreground color of the H10.
    planetH10ForegroundColorKey = \
        "ui/astrology/H10ForegroundColor"

    # QSettings default value for the foreground color of the H10.
    planetH10ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H10.
    planetH10BackgroundColorKey = \
        "ui/astrology/H10BackgroundColor"

    # QSettings default value for the background color of the H10.
    planetH10BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeKey = \
        "ui/astrology/H11GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeDefValue = "H11"

    # QSettings key for the planet glyph font size of the H11.
    planetH11GlyphFontSizeKey = \
        "ui/astrology/H11GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H11.
    planetH11GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H11.
    planetH11AbbreviationKey = \
        "ui/astrology/H11Abbreviation"

    # QSettings default value for the planet abbreviation of the H11.
    planetH11AbbreviationDefValue = "H11"

    # QSettings key for the foreground color of the H11.
    planetH11ForegroundColorKey = \
        "ui/astrology/H11ForegroundColor"

    # QSettings default value for the foreground color of the H11.
    planetH11ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H11.
    planetH11BackgroundColorKey = \
        "ui/astrology/H11BackgroundColor"

    # QSettings default value for the background color of the H11.
    planetH11BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeKey = \
        "ui/astrology/H12GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeDefValue = "H12"

    # QSettings key for the planet glyph font size of the H12.
    planetH12GlyphFontSizeKey = \
        "ui/astrology/H12GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H12.
    planetH12GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H12.
    planetH12AbbreviationKey = \
        "ui/astrology/H12Abbreviation"

    # QSettings default value for the planet abbreviation of the H12.
    planetH12AbbreviationDefValue = "H12"

    # QSettings key for the foreground color of the H12.
    planetH12ForegroundColorKey = \
        "ui/astrology/H12ForegroundColor"

    # QSettings default value for the foreground color of the H12.
    planetH12ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H12.
    planetH12BackgroundColorKey = \
        "ui/astrology/H12BackgroundColor"

    # QSettings default value for the background color of the H12.
    planetH12BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the ARMC.
    planetARMCGlyphUnicodeKey = \
        "ui/astrology/ARMCGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the ARMC.
    planetARMCGlyphUnicodeDefValue = "ARMC"

    # QSettings key for the planet glyph font size of the ARMC.
    planetARMCGlyphFontSizeKey = \
        "ui/astrology/ARMCGlyphFontSize"

    # QSettings default value for the planet glyph font size of the ARMC.
    planetARMCGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the ARMC.
    planetARMCAbbreviationKey = \
        "ui/astrology/ARMCAbbreviation"

    # QSettings default value for the planet abbreviation of the ARMC.
    planetARMCAbbreviationDefValue = "ARMC"

    # QSettings key for the foreground color of the ARMC.
    planetARMCForegroundColorKey = \
        "ui/astrology/ARMCForegroundColor"

    # QSettings default value for the foreground color of the ARMC.
    planetARMCForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the ARMC.
    planetARMCBackgroundColorKey = \
        "ui/astrology/ARMCBackgroundColor"

    # QSettings default value for the background color of the ARMC.
    planetARMCBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Vertex.
    planetVertexGlyphUnicodeKey = \
        "ui/astrology/VertexGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Vertex.
    planetVertexGlyphUnicodeDefValue = "Vx"

    # QSettings key for the planet glyph font size of the Vertex.
    planetVertexGlyphFontSizeKey = \
        "ui/astrology/VertexGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Vertex.
    planetVertexGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Vertex.
    planetVertexAbbreviationKey = \
        "ui/astrology/VertexAbbreviation"

    # QSettings default value for the planet abbreviation of the Vertex.
    planetVertexAbbreviationDefValue = "Vertex"

    # QSettings key for the foreground color of the Vertex.
    planetVertexForegroundColorKey = \
        "ui/astrology/VertexForegroundColor"

    # QSettings default value for the foreground color of the Vertex.
    planetVertexForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Vertex.
    planetVertexBackgroundColorKey = \
        "ui/astrology/VertexBackgroundColor"

    # QSettings default value for the background color of the Vertex.
    planetVertexBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the EquatorialAscendant.
    planetEquatorialAscendantGlyphUnicodeKey = \
        "ui/astrology/EquatorialAscendantGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the EquatorialAscendant.
    planetEquatorialAscendantGlyphUnicodeDefValue = "EquatorialAscendant"

    # QSettings key for the planet glyph font size of the EquatorialAscendant.
    planetEquatorialAscendantGlyphFontSizeKey = \
        "ui/astrology/EquatorialAscendantGlyphFontSize"

    # QSettings default value for the planet glyph font size of the EquatorialAscendant.
    planetEquatorialAscendantGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the EquatorialAscendant.
    planetEquatorialAscendantAbbreviationKey = \
        "ui/astrology/EquatorialAscendantAbbreviation"

    # QSettings default value for the planet abbreviation of the EquatorialAscendant.
    planetEquatorialAscendantAbbreviationDefValue = "EquatorialAscendant"

    # QSettings key for the foreground color of the EquatorialAscendant.
    planetEquatorialAscendantForegroundColorKey = \
        "ui/astrology/EquatorialAscendantForegroundColor"

    # QSettings default value for the foreground color of the EquatorialAscendant.
    planetEquatorialAscendantForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the EquatorialAscendant.
    planetEquatorialAscendantBackgroundColorKey = \
        "ui/astrology/EquatorialAscendantBackgroundColor"

    # QSettings default value for the background color of the EquatorialAscendant.
    planetEquatorialAscendantBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the CoAscendant1.
    planetCoAscendant1GlyphUnicodeKey = \
        "ui/astrology/CoAscendant1GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the CoAscendant1.
    planetCoAscendant1GlyphUnicodeDefValue = "CoAscendant1"

    # QSettings key for the planet glyph font size of the CoAscendant1.
    planetCoAscendant1GlyphFontSizeKey = \
        "ui/astrology/CoAscendant1GlyphFontSize"

    # QSettings default value for the planet glyph font size of the CoAscendant1.
    planetCoAscendant1GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the CoAscendant1.
    planetCoAscendant1AbbreviationKey = \
        "ui/astrology/CoAscendant1Abbreviation"

    # QSettings default value for the planet abbreviation of the CoAscendant1.
    planetCoAscendant1AbbreviationDefValue = "CoAscendant1"

    # QSettings key for the foreground color of the CoAscendant1.
    planetCoAscendant1ForegroundColorKey = \
        "ui/astrology/CoAscendant1ForegroundColor"

    # QSettings default value for the foreground color of the CoAscendant1.
    planetCoAscendant1ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the CoAscendant1.
    planetCoAscendant1BackgroundColorKey = \
        "ui/astrology/CoAscendant1BackgroundColor"

    # QSettings default value for the background color of the CoAscendant1.
    planetCoAscendant1BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the CoAscendant2.
    planetCoAscendant2GlyphUnicodeKey = \
        "ui/astrology/CoAscendant2GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the CoAscendant2.
    planetCoAscendant2GlyphUnicodeDefValue = "CoAscendant2"

    # QSettings key for the planet glyph font size of the CoAscendant2.
    planetCoAscendant2GlyphFontSizeKey = \
        "ui/astrology/CoAscendant2GlyphFontSize"

    # QSettings default value for the planet glyph font size of the CoAscendant2.
    planetCoAscendant2GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the CoAscendant2.
    planetCoAscendant2AbbreviationKey = \
        "ui/astrology/CoAscendant2Abbreviation"

    # QSettings default value for the planet abbreviation of the CoAscendant2.
    planetCoAscendant2AbbreviationDefValue = "CoAscendant2"

    # QSettings key for the foreground color of the CoAscendant2.
    planetCoAscendant2ForegroundColorKey = \
        "ui/astrology/CoAscendant2ForegroundColor"

    # QSettings default value for the foreground color of the CoAscendant2.
    planetCoAscendant2ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the CoAscendant2.
    planetCoAscendant2BackgroundColorKey = \
        "ui/astrology/CoAscendant2BackgroundColor"

    # QSettings default value for the background color of the CoAscendant2.
    planetCoAscendant2BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the PolarAscendant.
    planetPolarAscendantGlyphUnicodeKey = \
        "ui/astrology/PolarAscendantGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the PolarAscendant.
    planetPolarAscendantGlyphUnicodeDefValue = "PolarAscendant"

    # QSettings key for the planet glyph font size of the PolarAscendant.
    planetPolarAscendantGlyphFontSizeKey = \
        "ui/astrology/PolarAscendantGlyphFontSize"

    # QSettings default value for the planet glyph font size of the PolarAscendant.
    planetPolarAscendantGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the PolarAscendant.
    planetPolarAscendantAbbreviationKey = \
        "ui/astrology/PolarAscendantAbbreviation"

    # QSettings default value for the planet abbreviation of the PolarAscendant.
    planetPolarAscendantAbbreviationDefValue = "PolarAscendant"

    # QSettings key for the foreground color of the PolarAscendant.
    planetPolarAscendantForegroundColorKey = \
        "ui/astrology/PolarAscendantForegroundColor"

    # QSettings default value for the foreground color of the PolarAscendant.
    planetPolarAscendantForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the PolarAscendant.
    planetPolarAscendantBackgroundColorKey = \
        "ui/astrology/PolarAscendantBackgroundColor"

    # QSettings default value for the background color of the PolarAscendant.
    planetPolarAscendantBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeKey = \
        "ui/astrology/HoraLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeDefValue = "HL"

    # QSettings key for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeKey = \
        "ui/astrology/HoraLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationKey = \
        "ui/astrology/HoraLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationDefValue = "HL"

    # QSettings key for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorKey = \
        "ui/astrology/HoraLagnaForegroundColor"

    # QSettings default value for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorKey = \
        "ui/astrology/HoraLagnaBackgroundColor"

    # QSettings default value for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeKey = \
        "ui/astrology/GhatiLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeDefValue = "GL"

    # QSettings key for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeKey = \
        "ui/astrology/GhatiLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationKey = \
        "ui/astrology/GhatiLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationDefValue = "GL"

    # QSettings key for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorKey = \
        "ui/astrology/GhatiLagnaForegroundColor"

    # QSettings default value for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorKey = \
        "ui/astrology/GhatiLagnaBackgroundColor"

    # QSettings default value for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/MeanLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeDefValue = "MLA"

    # QSettings key for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/MeanLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationKey = \
        "ui/astrology/MeanLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationDefValue = "MLA"

    # QSettings key for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorKey = \
        "ui/astrology/MeanLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorKey = \
        "ui/astrology/MeanLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/OsculatingLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeDefValue = "OLA"

    # QSettings key for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/OsculatingLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationKey = \
        "ui/astrology/OsculatingLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationDefValue = "OLA"

    # QSettings key for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorKey = \
        "ui/astrology/OsculatingLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorKey = \
        "ui/astrology/OsculatingLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/InterpolatedLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeDefValue = "ILA"

    # QSettings key for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/InterpolatedLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationKey = \
        "ui/astrology/InterpolatedLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationDefValue = "ILA"

    # QSettings key for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorKey = \
        "ui/astrology/InterpolatedLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorKey = \
        "ui/astrology/InterpolatedLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeKey = \
        "ui/astrology/InterpolatedLunarPerigeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeDefValue = "ILP"

    # QSettings key for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeKey = \
        "ui/astrology/InterpolatedLunarPerigeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationKey = \
        "ui/astrology/InterpolatedLunarPerigeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationDefValue = "ILP"

    # QSettings key for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorKey = \
        "ui/astrology/InterpolatedLunarPerigeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorKey = \
        "ui/astrology/InterpolatedLunarPerigeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeKey = \
        "ui/astrology/SunGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeDefValue = "\u2609"

    # QSettings key for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeKey = \
        "ui/astrology/SunGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Sun.
    planetSunAbbreviationKey = \
        "ui/astrology/SunAbbreviation"

    # QSettings default value for the planet abbreviation of the Sun.
    planetSunAbbreviationDefValue = "Su"

    # QSettings key for the foreground color of the Sun.
    planetSunForegroundColorKey = \
        "ui/astrology/SunForegroundColor"

    # QSettings default value for the foreground color of the Sun.
    planetSunForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sun.
    planetSunBackgroundColorKey = \
        "ui/astrology/SunBackgroundColor"

    # QSettings default value for the background color of the Sun.
    planetSunBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeKey = \
        "ui/astrology/MoonGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeDefValue = "\u263d"

    # QSettings key for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeKey = \
        "ui/astrology/MoonGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Moon.
    planetMoonAbbreviationKey = \
        "ui/astrology/MoonAbbreviation"

    # QSettings default value for the planet abbreviation of the Moon.
    planetMoonAbbreviationDefValue = "Mo"

    # QSettings key for the foreground color of the Moon.
    planetMoonForegroundColorKey = \
        "ui/astrology/MoonForegroundColor"

    # QSettings default value for the foreground color of the Moon.
    planetMoonForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Moon.
    planetMoonBackgroundColorKey = \
        "ui/astrology/MoonBackgroundColor"

    # QSettings default value for the background color of the Moon.
    planetMoonBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeKey = \
        "ui/astrology/MercuryGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeDefValue = "\u263f"

    # QSettings key for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeKey = \
        "ui/astrology/MercuryGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationKey = \
        "ui/astrology/MercuryAbbreviation"

    # QSettings default value for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationDefValue = "Me"

    # QSettings key for the foreground color of the Mercury.
    planetMercuryForegroundColorKey = \
        "ui/astrology/MercuryForegroundColor"

    # QSettings default value for the foreground color of the Mercury.
    planetMercuryForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mercury.
    planetMercuryBackgroundColorKey = \
        "ui/astrology/MercuryBackgroundColor"

    # QSettings default value for the background color of the Mercury.
    planetMercuryBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeKey = \
        "ui/astrology/VenusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeDefValue = "\u2640"

    # QSettings key for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeKey = \
        "ui/astrology/VenusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Venus.
    planetVenusAbbreviationKey = \
        "ui/astrology/VenusAbbreviation"

    # QSettings default value for the planet abbreviation of the Venus.
    planetVenusAbbreviationDefValue = "Ve"

    # QSettings key for the foreground color of the Venus.
    planetVenusForegroundColorKey = \
        "ui/astrology/VenusForegroundColor"

    # QSettings default value for the foreground color of the Venus.
    planetVenusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Venus.
    planetVenusBackgroundColorKey = \
        "ui/astrology/VenusBackgroundColor"

    # QSettings default value for the background color of the Venus.
    planetVenusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeKey = \
        "ui/astrology/EarthGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeDefValue = "\u2d32"

    # QSettings key for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeKey = \
        "ui/astrology/EarthGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Earth.
    planetEarthAbbreviationKey = \
        "ui/astrology/EarthAbbreviation"

    # QSettings default value for the planet abbreviation of the Earth.
    planetEarthAbbreviationDefValue = "Ea"

    # QSettings key for the foreground color of the Earth.
    planetEarthForegroundColorKey = \
        "ui/astrology/EarthForegroundColor"

    # QSettings default value for the foreground color of the Earth.
    planetEarthForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Earth.
    planetEarthBackgroundColorKey = \
        "ui/astrology/EarthBackgroundColor"

    # QSettings default value for the background color of the Earth.
    planetEarthBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeKey = \
        "ui/astrology/MarsGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeDefValue = "\u2642"

    # QSettings key for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeKey = \
        "ui/astrology/MarsGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mars.
    planetMarsAbbreviationKey = \
        "ui/astrology/MarsAbbreviation"

    # QSettings default value for the planet abbreviation of the Mars.
    planetMarsAbbreviationDefValue = "Ma"

    # QSettings key for the foreground color of the Mars.
    planetMarsForegroundColorKey = \
        "ui/astrology/MarsForegroundColor"

    # QSettings default value for the foreground color of the Mars.
    planetMarsForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mars.
    planetMarsBackgroundColorKey = \
        "ui/astrology/MarsBackgroundColor"

    # QSettings default value for the background color of the Mars.
    planetMarsBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeKey = \
        "ui/astrology/JupiterGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeDefValue = "\u2643"

    # QSettings key for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeKey = \
        "ui/astrology/JupiterGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationKey = \
        "ui/astrology/JupiterAbbreviation"

    # QSettings default value for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationDefValue = "Ju"

    # QSettings key for the foreground color of the Jupiter.
    planetJupiterForegroundColorKey = \
        "ui/astrology/JupiterForegroundColor"

    # QSettings default value for the foreground color of the Jupiter.
    planetJupiterForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Jupiter.
    planetJupiterBackgroundColorKey = \
        "ui/astrology/JupiterBackgroundColor"

    # QSettings default value for the background color of the Jupiter.
    planetJupiterBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeKey = \
        "ui/astrology/SaturnGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeDefValue = "\u2644"

    # QSettings key for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeKey = \
        "ui/astrology/SaturnGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationKey = \
        "ui/astrology/SaturnAbbreviation"

    # QSettings default value for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Saturn.
    planetSaturnForegroundColorKey = \
        "ui/astrology/SaturnForegroundColor"

    # QSettings default value for the foreground color of the Saturn.
    planetSaturnForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Saturn.
    planetSaturnBackgroundColorKey = \
        "ui/astrology/SaturnBackgroundColor"

    # QSettings default value for the background color of the Saturn.
    planetSaturnBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeKey = \
        "ui/astrology/UranusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeDefValue = "\u2645"

    # QSettings key for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeKey = \
        "ui/astrology/UranusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Uranus.
    planetUranusAbbreviationKey = \
        "ui/astrology/UranusAbbreviation"

    # QSettings default value for the planet abbreviation of the Uranus.
    planetUranusAbbreviationDefValue = "Ur"

    # QSettings key for the foreground color of the Uranus.
    planetUranusForegroundColorKey = \
        "ui/astrology/UranusForegroundColor"

    # QSettings default value for the foreground color of the Uranus.
    planetUranusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Uranus.
    planetUranusBackgroundColorKey = \
        "ui/astrology/UranusBackgroundColor"

    # QSettings default value for the background color of the Uranus.
    planetUranusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeKey = \
        "ui/astrology/NeptuneGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeDefValue = "\u2646"

    # QSettings key for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeKey = \
        "ui/astrology/NeptuneGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationKey = \
        "ui/astrology/NeptuneAbbreviation"

    # QSettings default value for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationDefValue = "Ne"

    # QSettings key for the foreground color of the Neptune.
    planetNeptuneForegroundColorKey = \
        "ui/astrology/NeptuneForegroundColor"

    # QSettings default value for the foreground color of the Neptune.
    planetNeptuneForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Neptune.
    planetNeptuneBackgroundColorKey = \
        "ui/astrology/NeptuneBackgroundColor"

    # QSettings default value for the background color of the Neptune.
    planetNeptuneBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeKey = \
        "ui/astrology/PlutoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeDefValue = "\u2647"

    # QSettings key for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeKey = \
        "ui/astrology/PlutoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationKey = \
        "ui/astrology/PlutoAbbreviation"

    # QSettings default value for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationDefValue = "Pl"

    # QSettings key for the foreground color of the Pluto.
    planetPlutoForegroundColorKey = \
        "ui/astrology/PlutoForegroundColor"

    # QSettings default value for the foreground color of the Pluto.
    planetPlutoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pluto.
    planetPlutoBackgroundColorKey = \
        "ui/astrology/PlutoBackgroundColor"

    # QSettings default value for the background color of the Pluto.
    planetPlutoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeKey = \
        "ui/astrology/MeanNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeKey = \
        "ui/astrology/MeanNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationKey = \
        "ui/astrology/MeanNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationDefValue = "Ra"

    # QSettings key for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorKey = \
        "ui/astrology/MeanNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorKey = \
        "ui/astrology/MeanNorthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeKey = \
        "ui/astrology/MeanSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeKey = \
        "ui/astrology/MeanSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationKey = \
        "ui/astrology/MeanSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationDefValue = "Ke"

    # QSettings key for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorKey = \
        "ui/astrology/MeanSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorKey = \
        "ui/astrology/MeanSouthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeKey = \
        "ui/astrology/TrueNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeKey = \
        "ui/astrology/TrueNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationKey = \
        "ui/astrology/TrueNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationDefValue = "TrueNNode"

    # QSettings key for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorKey = \
        "ui/astrology/TrueNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorKey = \
        "ui/astrology/TrueNorthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeKey = \
        "ui/astrology/TrueSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeKey = \
        "ui/astrology/TrueSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationKey = \
        "ui/astrology/TrueSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationDefValue = "TrueSNode"

    # QSettings key for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorKey = \
        "ui/astrology/TrueSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorKey = \
        "ui/astrology/TrueSouthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeKey = \
        "ui/astrology/CeresGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeDefValue = "\u26b3"

    # QSettings key for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeKey = \
        "ui/astrology/CeresGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Ceres.
    planetCeresAbbreviationKey = \
        "ui/astrology/CeresAbbreviation"

    # QSettings default value for the planet abbreviation of the Ceres.
    planetCeresAbbreviationDefValue = "Ce"

    # QSettings key for the foreground color of the Ceres.
    planetCeresForegroundColorKey = \
        "ui/astrology/CeresForegroundColor"

    # QSettings default value for the foreground color of the Ceres.
    planetCeresForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Ceres.
    planetCeresBackgroundColorKey = \
        "ui/astrology/CeresBackgroundColor"

    # QSettings default value for the background color of the Ceres.
    planetCeresBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeKey = \
        "ui/astrology/PallasGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeDefValue = "\u26b4"

    # QSettings key for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeKey = \
        "ui/astrology/PallasGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pallas.
    planetPallasAbbreviationKey = \
        "ui/astrology/PallasAbbreviation"

    # QSettings default value for the planet abbreviation of the Pallas.
    planetPallasAbbreviationDefValue = "Pa"

    # QSettings key for the foreground color of the Pallas.
    planetPallasForegroundColorKey = \
        "ui/astrology/PallasForegroundColor"

    # QSettings default value for the foreground color of the Pallas.
    planetPallasForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pallas.
    planetPallasBackgroundColorKey = \
        "ui/astrology/PallasBackgroundColor"

    # QSettings default value for the background color of the Pallas.
    planetPallasBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeKey = \
        "ui/astrology/JunoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeDefValue = "\u26b5"

    # QSettings key for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeKey = \
        "ui/astrology/JunoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Juno.
    planetJunoAbbreviationKey = \
        "ui/astrology/JunoAbbreviation"

    # QSettings default value for the planet abbreviation of the Juno.
    planetJunoAbbreviationDefValue = "Jun"

    # QSettings key for the foreground color of the Juno.
    planetJunoForegroundColorKey = \
        "ui/astrology/JunoForegroundColor"

    # QSettings default value for the foreground color of the Juno.
    planetJunoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Juno.
    planetJunoBackgroundColorKey = \
        "ui/astrology/JunoBackgroundColor"

    # QSettings default value for the background color of the Juno.
    planetJunoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeKey = \
        "ui/astrology/VestaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeKey = \
        "ui/astrology/VestaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Vesta.
    planetVestaAbbreviationKey = \
        "ui/astrology/VestaAbbreviation"

    # QSettings default value for the planet abbreviation of the Vesta.
    planetVestaAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Vesta.
    planetVestaForegroundColorKey = \
        "ui/astrology/VestaForegroundColor"

    # QSettings default value for the foreground color of the Vesta.
    planetVestaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Vesta.
    planetVestaBackgroundColorKey = \
        "ui/astrology/VestaBackgroundColor"

    # QSettings default value for the background color of the Vesta.
    planetVestaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Isis.
    planetIsisGlyphUnicodeKey = \
        "ui/astrology/IsisGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Isis.
    planetIsisGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Isis.
    planetIsisGlyphFontSizeKey = \
        "ui/astrology/IsisGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Isis.
    planetIsisGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Isis.
    planetIsisAbbreviationKey = \
        "ui/astrology/IsisAbbreviation"

    # QSettings default value for the planet abbreviation of the Isis.
    planetIsisAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Isis.
    planetIsisForegroundColorKey = \
        "ui/astrology/IsisForegroundColor"

    # QSettings default value for the foreground color of the Isis.
    planetIsisForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Isis.
    planetIsisBackgroundColorKey = \
        "ui/astrology/IsisBackgroundColor"

    # QSettings default value for the background color of the Isis.
    planetIsisBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Nibiru.
    planetNibiruGlyphUnicodeKey = \
        "ui/astrology/NibiruGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Nibiru.
    planetNibiruGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Nibiru.
    planetNibiruGlyphFontSizeKey = \
        "ui/astrology/NibiruGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Nibiru.
    planetNibiruGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Nibiru.
    planetNibiruAbbreviationKey = \
        "ui/astrology/NibiruAbbreviation"

    # QSettings default value for the planet abbreviation of the Nibiru.
    planetNibiruAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Nibiru.
    planetNibiruForegroundColorKey = \
        "ui/astrology/NibiruForegroundColor"

    # QSettings default value for the foreground color of the Nibiru.
    planetNibiruForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Nibiru.
    planetNibiruBackgroundColorKey = \
        "ui/astrology/NibiruBackgroundColor"

    # QSettings default value for the background color of the Nibiru.
    planetNibiruBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeKey = \
        "ui/astrology/ChironGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeDefValue = "\u26b7"

    # QSettings key for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeKey = \
        "ui/astrology/ChironGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Chiron.
    planetChironAbbreviationKey = \
        "ui/astrology/ChironAbbreviation"

    # QSettings default value for the planet abbreviation of the Chiron.
    planetChironAbbreviationDefValue = "Chi"

    # QSettings key for the foreground color of the Chiron.
    planetChironForegroundColorKey = \
        "ui/astrology/ChironForegroundColor"

    # QSettings default value for the foreground color of the Chiron.
    planetChironForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Chiron.
    planetChironBackgroundColorKey = \
        "ui/astrology/ChironBackgroundColor"

    # QSettings default value for the background color of the Chiron.
    planetChironBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeKey = \
        "ui/astrology/GulikaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeDefValue = "Gk"

    # QSettings key for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeKey = \
        "ui/astrology/GulikaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationKey = \
        "ui/astrology/GulikaAbbreviation"

    # QSettings default value for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationDefValue = "Gk"

    # QSettings key for the foreground color of the Gulika.
    planetGulikaForegroundColorKey = \
        "ui/astrology/GulikaForegroundColor"

    # QSettings default value for the foreground color of the Gulika.
    planetGulikaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gulika.
    planetGulikaBackgroundColorKey = \
        "ui/astrology/GulikaBackgroundColor"

    # QSettings default value for the background color of the Gulika.
    planetGulikaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeKey = \
        "ui/astrology/MandiGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeDefValue = "Md"

    # QSettings key for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeKey = \
        "ui/astrology/MandiGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mandi.
    planetMandiAbbreviationKey = \
        "ui/astrology/MandiAbbreviation"

    # QSettings default value for the planet abbreviation of the Mandi.
    planetMandiAbbreviationDefValue = "Md"

    # QSettings key for the foreground color of the Mandi.
    planetMandiForegroundColorKey = \
        "ui/astrology/MandiForegroundColor"

    # QSettings default value for the foreground color of the Mandi.
    planetMandiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mandi.
    planetMandiBackgroundColorKey = \
        "ui/astrology/MandiBackgroundColor"

    # QSettings default value for the background color of the Mandi.
    planetMandiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeKey = \
        "ui/astrology/MeanOfFiveGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeDefValue = "MOF"

    # QSettings key for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeKey = \
        "ui/astrology/MeanOfFiveGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationKey = \
        "ui/astrology/MeanOfFiveAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationDefValue = "MOF"

    # QSettings key for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorKey = \
        "ui/astrology/MeanOfFiveForegroundColor"

    # QSettings default value for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorKey = \
        "ui/astrology/MeanOfFiveBackgroundColor"

    # QSettings default value for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeKey = \
        "ui/astrology/CycleOfEightGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeDefValue = "COE"

    # QSettings key for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeKey = \
        "ui/astrology/CycleOfEightGlyphFontSize"

    # QSettings default value for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationKey = \
        "ui/astrology/CycleOfEightAbbreviation"

    # QSettings default value for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationDefValue = "COE"

    # QSettings key for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorKey = \
        "ui/astrology/CycleOfEightForegroundColor"

    # QSettings default value for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorKey = \
        "ui/astrology/CycleOfEightBackgroundColor"

    # QSettings default value for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeKey = \
        "ui/astrology/AvgMaJuSaUrNePlGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeKey = \
        "ui/astrology/AvgMaJuSaUrNePlGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationKey = \
        "ui/astrology/AvgMaJuSaUrNePlAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorKey = \
        "ui/astrology/AvgMaJuSaUrNePlForegroundColor"

    # QSettings default value for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorKey = \
        "ui/astrology/AvgMaJuSaUrNePlBackgroundColor"

    # QSettings default value for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeKey = \
        "ui/astrology/AvgJuSaUrNeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeDefValue = "AvgJuSaUrNe"

    # QSettings key for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeKey = \
        "ui/astrology/AvgJuSaUrNeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationKey = \
        "ui/astrology/AvgJuSaUrNeAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationDefValue = "AvgJuSaUrNe"

    # QSettings key for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorKey = \
        "ui/astrology/AvgJuSaUrNeForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorKey = \
        "ui/astrology/AvgJuSaUrNeBackgroundColor"

    # QSettings default value for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeKey = \
        "ui/astrology/AvgJuSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeDefValue = "AvgJuSa"

    # QSettings key for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeKey = \
        "ui/astrology/AvgJuSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationKey = \
        "ui/astrology/AvgJuSaAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationDefValue = "AvgJuSa"

    # QSettings key for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorKey = \
        "ui/astrology/AvgJuSaForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorKey = \
        "ui/astrology/AvgJuSaBackgroundColor"

    # QSettings default value for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AsSu.
    planetAsSuGlyphUnicodeKey = \
        "ui/astrology/AsSuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AsSu.
    planetAsSuGlyphUnicodeDefValue = "AsSu"

    # QSettings key for the planet glyph font size of the AsSu.
    planetAsSuGlyphFontSizeKey = \
        "ui/astrology/AsSuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AsSu.
    planetAsSuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AsSu.
    planetAsSuAbbreviationKey = \
        "ui/astrology/AsSuAbbreviation"

    # QSettings default value for the planet abbreviation of the AsSu.
    planetAsSuAbbreviationDefValue = "AsSu"

    # QSettings key for the foreground color of the AsSu.
    planetAsSuForegroundColorKey = \
        "ui/astrology/AsSuForegroundColor"

    # QSettings default value for the foreground color of the AsSu.
    planetAsSuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AsSu.
    planetAsSuBackgroundColorKey = \
        "ui/astrology/AsSuBackgroundColor"

    # QSettings default value for the background color of the AsSu.
    planetAsSuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AsMo.
    planetAsMoGlyphUnicodeKey = \
        "ui/astrology/AsMoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AsMo.
    planetAsMoGlyphUnicodeDefValue = "AsMo"

    # QSettings key for the planet glyph font size of the AsMo.
    planetAsMoGlyphFontSizeKey = \
        "ui/astrology/AsMoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AsMo.
    planetAsMoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AsMo.
    planetAsMoAbbreviationKey = \
        "ui/astrology/AsMoAbbreviation"

    # QSettings default value for the planet abbreviation of the AsMo.
    planetAsMoAbbreviationDefValue = "AsMo"

    # QSettings key for the foreground color of the AsMo.
    planetAsMoForegroundColorKey = \
        "ui/astrology/AsMoForegroundColor"

    # QSettings default value for the foreground color of the AsMo.
    planetAsMoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AsMo.
    planetAsMoBackgroundColorKey = \
        "ui/astrology/AsMoBackgroundColor"

    # QSettings default value for the background color of the AsMo.
    planetAsMoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MoSu.
    planetMoSuGlyphUnicodeKey = \
        "ui/astrology/MoSuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MoSu.
    planetMoSuGlyphUnicodeDefValue = "MoSu"

    # QSettings key for the planet glyph font size of the MoSu.
    planetMoSuGlyphFontSizeKey = \
        "ui/astrology/MoSuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MoSu.
    planetMoSuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MoSu.
    planetMoSuAbbreviationKey = \
        "ui/astrology/MoSuAbbreviation"

    # QSettings default value for the planet abbreviation of the MoSu.
    planetMoSuAbbreviationDefValue = "MoSu"

    # QSettings key for the foreground color of the MoSu.
    planetMoSuForegroundColorKey = \
        "ui/astrology/MoSuForegroundColor"

    # QSettings default value for the foreground color of the MoSu.
    planetMoSuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MoSu.
    planetMoSuBackgroundColorKey = \
        "ui/astrology/MoSuBackgroundColor"

    # QSettings default value for the background color of the MoSu.
    planetMoSuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeVe.
    planetMeVeGlyphUnicodeKey = \
        "ui/astrology/MeVeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeVe.
    planetMeVeGlyphUnicodeDefValue = "MeVe"

    # QSettings key for the planet glyph font size of the MeVe.
    planetMeVeGlyphFontSizeKey = \
        "ui/astrology/MeVeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeVe.
    planetMeVeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeVe.
    planetMeVeAbbreviationKey = \
        "ui/astrology/MeVeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeVe.
    planetMeVeAbbreviationDefValue = "MeVe"

    # QSettings key for the foreground color of the MeVe.
    planetMeVeForegroundColorKey = \
        "ui/astrology/MeVeForegroundColor"

    # QSettings default value for the foreground color of the MeVe.
    planetMeVeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeVe.
    planetMeVeBackgroundColorKey = \
        "ui/astrology/MeVeBackgroundColor"

    # QSettings default value for the background color of the MeVe.
    planetMeVeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeEa.
    planetMeEaGlyphUnicodeKey = \
        "ui/astrology/MeEaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeEa.
    planetMeEaGlyphUnicodeDefValue = "MeEa"

    # QSettings key for the planet glyph font size of the MeEa.
    planetMeEaGlyphFontSizeKey = \
        "ui/astrology/MeEaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeEa.
    planetMeEaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeEa.
    planetMeEaAbbreviationKey = \
        "ui/astrology/MeEaAbbreviation"

    # QSettings default value for the planet abbreviation of the MeEa.
    planetMeEaAbbreviationDefValue = "MeEa"

    # QSettings key for the foreground color of the MeEa.
    planetMeEaForegroundColorKey = \
        "ui/astrology/MeEaForegroundColor"

    # QSettings default value for the foreground color of the MeEa.
    planetMeEaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeEa.
    planetMeEaBackgroundColorKey = \
        "ui/astrology/MeEaBackgroundColor"

    # QSettings default value for the background color of the MeEa.
    planetMeEaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeMa.
    planetMeMaGlyphUnicodeKey = \
        "ui/astrology/MeMaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeMa.
    planetMeMaGlyphUnicodeDefValue = "MeMa"

    # QSettings key for the planet glyph font size of the MeMa.
    planetMeMaGlyphFontSizeKey = \
        "ui/astrology/MeMaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeMa.
    planetMeMaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeMa.
    planetMeMaAbbreviationKey = \
        "ui/astrology/MeMaAbbreviation"

    # QSettings default value for the planet abbreviation of the MeMa.
    planetMeMaAbbreviationDefValue = "MeMa"

    # QSettings key for the foreground color of the MeMa.
    planetMeMaForegroundColorKey = \
        "ui/astrology/MeMaForegroundColor"

    # QSettings default value for the foreground color of the MeMa.
    planetMeMaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeMa.
    planetMeMaBackgroundColorKey = \
        "ui/astrology/MeMaBackgroundColor"

    # QSettings default value for the background color of the MeMa.
    planetMeMaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeJu.
    planetMeJuGlyphUnicodeKey = \
        "ui/astrology/MeJuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeJu.
    planetMeJuGlyphUnicodeDefValue = "MeJu"

    # QSettings key for the planet glyph font size of the MeJu.
    planetMeJuGlyphFontSizeKey = \
        "ui/astrology/MeJuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeJu.
    planetMeJuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeJu.
    planetMeJuAbbreviationKey = \
        "ui/astrology/MeJuAbbreviation"

    # QSettings default value for the planet abbreviation of the MeJu.
    planetMeJuAbbreviationDefValue = "MeJu"

    # QSettings key for the foreground color of the MeJu.
    planetMeJuForegroundColorKey = \
        "ui/astrology/MeJuForegroundColor"

    # QSettings default value for the foreground color of the MeJu.
    planetMeJuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeJu.
    planetMeJuBackgroundColorKey = \
        "ui/astrology/MeJuBackgroundColor"

    # QSettings default value for the background color of the MeJu.
    planetMeJuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeSa.
    planetMeSaGlyphUnicodeKey = \
        "ui/astrology/MeSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeSa.
    planetMeSaGlyphUnicodeDefValue = "MeSa"

    # QSettings key for the planet glyph font size of the MeSa.
    planetMeSaGlyphFontSizeKey = \
        "ui/astrology/MeSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeSa.
    planetMeSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeSa.
    planetMeSaAbbreviationKey = \
        "ui/astrology/MeSaAbbreviation"

    # QSettings default value for the planet abbreviation of the MeSa.
    planetMeSaAbbreviationDefValue = "MeSa"

    # QSettings key for the foreground color of the MeSa.
    planetMeSaForegroundColorKey = \
        "ui/astrology/MeSaForegroundColor"

    # QSettings default value for the foreground color of the MeSa.
    planetMeSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeSa.
    planetMeSaBackgroundColorKey = \
        "ui/astrology/MeSaBackgroundColor"

    # QSettings default value for the background color of the MeSa.
    planetMeSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeUr.
    planetMeUrGlyphUnicodeKey = \
        "ui/astrology/MeUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeUr.
    planetMeUrGlyphUnicodeDefValue = "MeUr"

    # QSettings key for the planet glyph font size of the MeUr.
    planetMeUrGlyphFontSizeKey = \
        "ui/astrology/MeUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeUr.
    planetMeUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeUr.
    planetMeUrAbbreviationKey = \
        "ui/astrology/MeUrAbbreviation"

    # QSettings default value for the planet abbreviation of the MeUr.
    planetMeUrAbbreviationDefValue = "MeUr"

    # QSettings key for the foreground color of the MeUr.
    planetMeUrForegroundColorKey = \
        "ui/astrology/MeUrForegroundColor"

    # QSettings default value for the foreground color of the MeUr.
    planetMeUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeUr.
    planetMeUrBackgroundColorKey = \
        "ui/astrology/MeUrBackgroundColor"

    # QSettings default value for the background color of the MeUr.
    planetMeUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the VeEa.
    planetVeEaGlyphUnicodeKey = \
        "ui/astrology/VeEaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the VeEa.
    planetVeEaGlyphUnicodeDefValue = "VeEa"

    # QSettings key for the planet glyph font size of the VeEa.
    planetVeEaGlyphFontSizeKey = \
        "ui/astrology/VeEaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the VeEa.
    planetVeEaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the VeEa.
    planetVeEaAbbreviationKey = \
        "ui/astrology/VeEaAbbreviation"

    # QSettings default value for the planet abbreviation of the VeEa.
    planetVeEaAbbreviationDefValue = "VeEa"

    # QSettings key for the foreground color of the VeEa.
    planetVeEaForegroundColorKey = \
        "ui/astrology/VeEaForegroundColor"

    # QSettings default value for the foreground color of the VeEa.
    planetVeEaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the VeEa.
    planetVeEaBackgroundColorKey = \
        "ui/astrology/VeEaBackgroundColor"

    # QSettings default value for the background color of the VeEa.
    planetVeEaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the VeMa.
    planetVeMaGlyphUnicodeKey = \
        "ui/astrology/VeMaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the VeMa.
    planetVeMaGlyphUnicodeDefValue = "VeMa"

    # QSettings key for the planet glyph font size of the VeMa.
    planetVeMaGlyphFontSizeKey = \
        "ui/astrology/VeMaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the VeMa.
    planetVeMaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the VeMa.
    planetVeMaAbbreviationKey = \
        "ui/astrology/VeMaAbbreviation"

    # QSettings default value for the planet abbreviation of the VeMa.
    planetVeMaAbbreviationDefValue = "VeMa"

    # QSettings key for the foreground color of the VeMa.
    planetVeMaForegroundColorKey = \
        "ui/astrology/VeMaForegroundColor"

    # QSettings default value for the foreground color of the VeMa.
    planetVeMaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the VeMa.
    planetVeMaBackgroundColorKey = \
        "ui/astrology/VeMaBackgroundColor"

    # QSettings default value for the background color of the VeMa.
    planetVeMaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the VeJu.
    planetVeJuGlyphUnicodeKey = \
        "ui/astrology/VeJuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the VeJu.
    planetVeJuGlyphUnicodeDefValue = "VeJu"

    # QSettings key for the planet glyph font size of the VeJu.
    planetVeJuGlyphFontSizeKey = \
        "ui/astrology/VeJuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the VeJu.
    planetVeJuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the VeJu.
    planetVeJuAbbreviationKey = \
        "ui/astrology/VeJuAbbreviation"

    # QSettings default value for the planet abbreviation of the VeJu.
    planetVeJuAbbreviationDefValue = "VeJu"

    # QSettings key for the foreground color of the VeJu.
    planetVeJuForegroundColorKey = \
        "ui/astrology/VeJuForegroundColor"

    # QSettings default value for the foreground color of the VeJu.
    planetVeJuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the VeJu.
    planetVeJuBackgroundColorKey = \
        "ui/astrology/VeJuBackgroundColor"

    # QSettings default value for the background color of the VeJu.
    planetVeJuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the VeSa.
    planetVeSaGlyphUnicodeKey = \
        "ui/astrology/VeSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the VeSa.
    planetVeSaGlyphUnicodeDefValue = "VeSa"

    # QSettings key for the planet glyph font size of the VeSa.
    planetVeSaGlyphFontSizeKey = \
        "ui/astrology/VeSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the VeSa.
    planetVeSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the VeSa.
    planetVeSaAbbreviationKey = \
        "ui/astrology/VeSaAbbreviation"

    # QSettings default value for the planet abbreviation of the VeSa.
    planetVeSaAbbreviationDefValue = "VeSa"

    # QSettings key for the foreground color of the VeSa.
    planetVeSaForegroundColorKey = \
        "ui/astrology/VeSaForegroundColor"

    # QSettings default value for the foreground color of the VeSa.
    planetVeSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the VeSa.
    planetVeSaBackgroundColorKey = \
        "ui/astrology/VeSaBackgroundColor"

    # QSettings default value for the background color of the VeSa.
    planetVeSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the VeUr.
    planetVeUrGlyphUnicodeKey = \
        "ui/astrology/VeUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the VeUr.
    planetVeUrGlyphUnicodeDefValue = "VeUr"

    # QSettings key for the planet glyph font size of the VeUr.
    planetVeUrGlyphFontSizeKey = \
        "ui/astrology/VeUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the VeUr.
    planetVeUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the VeUr.
    planetVeUrAbbreviationKey = \
        "ui/astrology/VeUrAbbreviation"

    # QSettings default value for the planet abbreviation of the VeUr.
    planetVeUrAbbreviationDefValue = "VeUr"

    # QSettings key for the foreground color of the VeUr.
    planetVeUrForegroundColorKey = \
        "ui/astrology/VeUrForegroundColor"

    # QSettings default value for the foreground color of the VeUr.
    planetVeUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the VeUr.
    planetVeUrBackgroundColorKey = \
        "ui/astrology/VeUrBackgroundColor"

    # QSettings default value for the background color of the VeUr.
    planetVeUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the EaMa.
    planetEaMaGlyphUnicodeKey = \
        "ui/astrology/EaMaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the EaMa.
    planetEaMaGlyphUnicodeDefValue = "EaMa"

    # QSettings key for the planet glyph font size of the EaMa.
    planetEaMaGlyphFontSizeKey = \
        "ui/astrology/EaMaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the EaMa.
    planetEaMaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the EaMa.
    planetEaMaAbbreviationKey = \
        "ui/astrology/EaMaAbbreviation"

    # QSettings default value for the planet abbreviation of the EaMa.
    planetEaMaAbbreviationDefValue = "EaMa"

    # QSettings key for the foreground color of the EaMa.
    planetEaMaForegroundColorKey = \
        "ui/astrology/EaMaForegroundColor"

    # QSettings default value for the foreground color of the EaMa.
    planetEaMaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the EaMa.
    planetEaMaBackgroundColorKey = \
        "ui/astrology/EaMaBackgroundColor"

    # QSettings default value for the background color of the EaMa.
    planetEaMaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the EaJu.
    planetEaJuGlyphUnicodeKey = \
        "ui/astrology/EaJuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the EaJu.
    planetEaJuGlyphUnicodeDefValue = "EaJu"

    # QSettings key for the planet glyph font size of the EaJu.
    planetEaJuGlyphFontSizeKey = \
        "ui/astrology/EaJuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the EaJu.
    planetEaJuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the EaJu.
    planetEaJuAbbreviationKey = \
        "ui/astrology/EaJuAbbreviation"

    # QSettings default value for the planet abbreviation of the EaJu.
    planetEaJuAbbreviationDefValue = "EaJu"

    # QSettings key for the foreground color of the EaJu.
    planetEaJuForegroundColorKey = \
        "ui/astrology/EaJuForegroundColor"

    # QSettings default value for the foreground color of the EaJu.
    planetEaJuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the EaJu.
    planetEaJuBackgroundColorKey = \
        "ui/astrology/EaJuBackgroundColor"

    # QSettings default value for the background color of the EaJu.
    planetEaJuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the EaSa.
    planetEaSaGlyphUnicodeKey = \
        "ui/astrology/EaSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the EaSa.
    planetEaSaGlyphUnicodeDefValue = "EaSa"

    # QSettings key for the planet glyph font size of the EaSa.
    planetEaSaGlyphFontSizeKey = \
        "ui/astrology/EaSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the EaSa.
    planetEaSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the EaSa.
    planetEaSaAbbreviationKey = \
        "ui/astrology/EaSaAbbreviation"

    # QSettings default value for the planet abbreviation of the EaSa.
    planetEaSaAbbreviationDefValue = "EaSa"

    # QSettings key for the foreground color of the EaSa.
    planetEaSaForegroundColorKey = \
        "ui/astrology/EaSaForegroundColor"

    # QSettings default value for the foreground color of the EaSa.
    planetEaSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the EaSa.
    planetEaSaBackgroundColorKey = \
        "ui/astrology/EaSaBackgroundColor"

    # QSettings default value for the background color of the EaSa.
    planetEaSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the EaUr.
    planetEaUrGlyphUnicodeKey = \
        "ui/astrology/EaUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the EaUr.
    planetEaUrGlyphUnicodeDefValue = "EaUr"

    # QSettings key for the planet glyph font size of the EaUr.
    planetEaUrGlyphFontSizeKey = \
        "ui/astrology/EaUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the EaUr.
    planetEaUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the EaUr.
    planetEaUrAbbreviationKey = \
        "ui/astrology/EaUrAbbreviation"

    # QSettings default value for the planet abbreviation of the EaUr.
    planetEaUrAbbreviationDefValue = "EaUr"

    # QSettings key for the foreground color of the EaUr.
    planetEaUrForegroundColorKey = \
        "ui/astrology/EaUrForegroundColor"

    # QSettings default value for the foreground color of the EaUr.
    planetEaUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the EaUr.
    planetEaUrBackgroundColorKey = \
        "ui/astrology/EaUrBackgroundColor"

    # QSettings default value for the background color of the EaUr.
    planetEaUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MaJu.
    planetMaJuGlyphUnicodeKey = \
        "ui/astrology/MaJuGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MaJu.
    planetMaJuGlyphUnicodeDefValue = "MaJu"

    # QSettings key for the planet glyph font size of the MaJu.
    planetMaJuGlyphFontSizeKey = \
        "ui/astrology/MaJuGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MaJu.
    planetMaJuGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MaJu.
    planetMaJuAbbreviationKey = \
        "ui/astrology/MaJuAbbreviation"

    # QSettings default value for the planet abbreviation of the MaJu.
    planetMaJuAbbreviationDefValue = "MaJu"

    # QSettings key for the foreground color of the MaJu.
    planetMaJuForegroundColorKey = \
        "ui/astrology/MaJuForegroundColor"

    # QSettings default value for the foreground color of the MaJu.
    planetMaJuForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MaJu.
    planetMaJuBackgroundColorKey = \
        "ui/astrology/MaJuBackgroundColor"

    # QSettings default value for the background color of the MaJu.
    planetMaJuBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MaSa.
    planetMaSaGlyphUnicodeKey = \
        "ui/astrology/MaSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MaSa.
    planetMaSaGlyphUnicodeDefValue = "MaSa"

    # QSettings key for the planet glyph font size of the MaSa.
    planetMaSaGlyphFontSizeKey = \
        "ui/astrology/MaSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MaSa.
    planetMaSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MaSa.
    planetMaSaAbbreviationKey = \
        "ui/astrology/MaSaAbbreviation"

    # QSettings default value for the planet abbreviation of the MaSa.
    planetMaSaAbbreviationDefValue = "MaSa"

    # QSettings key for the foreground color of the MaSa.
    planetMaSaForegroundColorKey = \
        "ui/astrology/MaSaForegroundColor"

    # QSettings default value for the foreground color of the MaSa.
    planetMaSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MaSa.
    planetMaSaBackgroundColorKey = \
        "ui/astrology/MaSaBackgroundColor"

    # QSettings default value for the background color of the MaSa.
    planetMaSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MaUr.
    planetMaUrGlyphUnicodeKey = \
        "ui/astrology/MaUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MaUr.
    planetMaUrGlyphUnicodeDefValue = "MaUr"

    # QSettings key for the planet glyph font size of the MaUr.
    planetMaUrGlyphFontSizeKey = \
        "ui/astrology/MaUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MaUr.
    planetMaUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MaUr.
    planetMaUrAbbreviationKey = \
        "ui/astrology/MaUrAbbreviation"

    # QSettings default value for the planet abbreviation of the MaUr.
    planetMaUrAbbreviationDefValue = "MaUr"

    # QSettings key for the foreground color of the MaUr.
    planetMaUrForegroundColorKey = \
        "ui/astrology/MaUrForegroundColor"

    # QSettings default value for the foreground color of the MaUr.
    planetMaUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MaUr.
    planetMaUrBackgroundColorKey = \
        "ui/astrology/MaUrBackgroundColor"

    # QSettings default value for the background color of the MaUr.
    planetMaUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the JuSa.
    planetJuSaGlyphUnicodeKey = \
        "ui/astrology/JuSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the JuSa.
    planetJuSaGlyphUnicodeDefValue = "JuSa"

    # QSettings key for the planet glyph font size of the JuSa.
    planetJuSaGlyphFontSizeKey = \
        "ui/astrology/JuSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the JuSa.
    planetJuSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the JuSa.
    planetJuSaAbbreviationKey = \
        "ui/astrology/JuSaAbbreviation"

    # QSettings default value for the planet abbreviation of the JuSa.
    planetJuSaAbbreviationDefValue = "JuSa"

    # QSettings key for the foreground color of the JuSa.
    planetJuSaForegroundColorKey = \
        "ui/astrology/JuSaForegroundColor"

    # QSettings default value for the foreground color of the JuSa.
    planetJuSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the JuSa.
    planetJuSaBackgroundColorKey = \
        "ui/astrology/JuSaBackgroundColor"

    # QSettings default value for the background color of the JuSa.
    planetJuSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the JuUr.
    planetJuUrGlyphUnicodeKey = \
        "ui/astrology/JuUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the JuUr.
    planetJuUrGlyphUnicodeDefValue = "JuUr"

    # QSettings key for the planet glyph font size of the JuUr.
    planetJuUrGlyphFontSizeKey = \
        "ui/astrology/JuUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the JuUr.
    planetJuUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the JuUr.
    planetJuUrAbbreviationKey = \
        "ui/astrology/JuUrAbbreviation"

    # QSettings default value for the planet abbreviation of the JuUr.
    planetJuUrAbbreviationDefValue = "JuUr"

    # QSettings key for the foreground color of the JuUr.
    planetJuUrForegroundColorKey = \
        "ui/astrology/JuUrForegroundColor"

    # QSettings default value for the foreground color of the JuUr.
    planetJuUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the JuUr.
    planetJuUrBackgroundColorKey = \
        "ui/astrology/JuUrBackgroundColor"

    # QSettings default value for the background color of the JuUr.
    planetJuUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the SaUr.
    planetSaUrGlyphUnicodeKey = \
        "ui/astrology/SaUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the SaUr.
    planetSaUrGlyphUnicodeDefValue = "SaUr"

    # QSettings key for the planet glyph font size of the SaUr.
    planetSaUrGlyphFontSizeKey = \
        "ui/astrology/SaUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the SaUr.
    planetSaUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the SaUr.
    planetSaUrAbbreviationKey = \
        "ui/astrology/SaUrAbbreviation"

    # QSettings default value for the planet abbreviation of the SaUr.
    planetSaUrAbbreviationDefValue = "SaUr"

    # QSettings key for the foreground color of the SaUr.
    planetSaUrForegroundColorKey = \
        "ui/astrology/SaUrForegroundColor"

    # QSettings default value for the foreground color of the SaUr.
    planetSaUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the SaUr.
    planetSaUrBackgroundColorKey = \
        "ui/astrology/SaUrBackgroundColor"

    # QSettings default value for the background color of the SaUr.
    planetSaUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the SaUr.
    planetSaUrGlyphUnicodeKey = \
        "ui/astrology/SaUrGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the SaUr.
    planetSaUrGlyphUnicodeDefValue = "SaUr"

    # QSettings key for the planet glyph font size of the SaUr.
    planetSaUrGlyphFontSizeKey = \
        "ui/astrology/SaUrGlyphFontSize"

    # QSettings default value for the planet glyph font size of the SaUr.
    planetSaUrGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the SaUr.
    planetSaUrAbbreviationKey = \
        "ui/astrology/SaUrAbbreviation"

    # QSettings default value for the planet abbreviation of the SaUr.
    planetSaUrAbbreviationDefValue = "SaUr"

    # QSettings key for the foreground color of the SaUr.
    planetSaUrForegroundColorKey = \
        "ui/astrology/SaUrForegroundColor"

    # QSettings default value for the foreground color of the SaUr.
    planetSaUrForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the SaUr.
    planetSaUrBackgroundColorKey = \
        "ui/astrology/SaUrBackgroundColor"

    # QSettings default value for the background color of the SaUr.
    planetSaUrBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeKey = \
        "ui/astrology/AriesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeDefValue = "\u2648"

    # QSettings key for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeKey = \
        "ui/astrology/AriesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aries.
    signAriesAbbreviationKey = \
        "ui/astrology/AriesAbbreviation"

    # QSettings default value for the sign abbreviation of the Aries.
    signAriesAbbreviationDefValue = "Ar"

    # QSettings key for the foreground color of the Aries.
    signAriesForegroundColorKey = \
        "ui/astrology/AriesForegroundColor"

    # QSettings default value for the foreground color of the Aries.
    signAriesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aries.
    signAriesBackgroundColorKey = \
        "ui/astrology/AriesBackgroundColor"

    # QSettings default value for the background color of the Aries.
    signAriesBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeKey = \
        "ui/astrology/TaurusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeDefValue = "\u2649"

    # QSettings key for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeKey = \
        "ui/astrology/TaurusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Taurus.
    signTaurusAbbreviationKey = \
        "ui/astrology/TaurusAbbreviation"

    # QSettings default value for the sign abbreviation of the Taurus.
    signTaurusAbbreviationDefValue = "Ta"

    # QSettings key for the foreground color of the Taurus.
    signTaurusForegroundColorKey = \
        "ui/astrology/TaurusForegroundColor"

    # QSettings default value for the foreground color of the Taurus.
    signTaurusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Taurus.
    signTaurusBackgroundColorKey = \
        "ui/astrology/TaurusBackgroundColor"

    # QSettings default value for the background color of the Taurus.
    signTaurusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeKey = \
        "ui/astrology/GeminiGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeDefValue = "\u264a"

    # QSettings key for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeKey = \
        "ui/astrology/GeminiGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Gemini.
    signGeminiAbbreviationKey = \
        "ui/astrology/GeminiAbbreviation"

    # QSettings default value for the sign abbreviation of the Gemini.
    signGeminiAbbreviationDefValue = "Ge"

    # QSettings key for the foreground color of the Gemini.
    signGeminiForegroundColorKey = \
        "ui/astrology/GeminiForegroundColor"

    # QSettings default value for the foreground color of the Gemini.
    signGeminiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gemini.
    signGeminiBackgroundColorKey = \
        "ui/astrology/GeminiBackgroundColor"

    # QSettings default value for the background color of the Gemini.
    signGeminiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeKey = \
        "ui/astrology/CancerGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeDefValue = "\u264b"

    # QSettings key for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeKey = \
        "ui/astrology/CancerGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Cancer.
    signCancerAbbreviationKey = \
        "ui/astrology/CancerAbbreviation"

    # QSettings default value for the sign abbreviation of the Cancer.
    signCancerAbbreviationDefValue = "Ca"

    # QSettings key for the foreground color of the Cancer.
    signCancerForegroundColorKey = \
        "ui/astrology/CancerForegroundColor"

    # QSettings default value for the foreground color of the Cancer.
    signCancerForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Cancer.
    signCancerBackgroundColorKey = \
        "ui/astrology/CancerBackgroundColor"

    # QSettings default value for the background color of the Cancer.
    signCancerBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeKey = \
        "ui/astrology/LeoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeDefValue = "\u264c"

    # QSettings key for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeKey = \
        "ui/astrology/LeoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Leo.
    signLeoAbbreviationKey = \
        "ui/astrology/LeoAbbreviation"

    # QSettings default value for the sign abbreviation of the Leo.
    signLeoAbbreviationDefValue = "Le"

    # QSettings key for the foreground color of the Leo.
    signLeoForegroundColorKey = \
        "ui/astrology/LeoForegroundColor"

    # QSettings default value for the foreground color of the Leo.
    signLeoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Leo.
    signLeoBackgroundColorKey = \
        "ui/astrology/LeoBackgroundColor"

    # QSettings default value for the background color of the Leo.
    signLeoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeKey = \
        "ui/astrology/VirgoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeDefValue = "\u264d"

    # QSettings key for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeKey = \
        "ui/astrology/VirgoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Virgo.
    signVirgoAbbreviationKey = \
        "ui/astrology/VirgoAbbreviation"

    # QSettings default value for the sign abbreviation of the Virgo.
    signVirgoAbbreviationDefValue = "Vi"

    # QSettings key for the foreground color of the Virgo.
    signVirgoForegroundColorKey = \
        "ui/astrology/VirgoForegroundColor"

    # QSettings default value for the foreground color of the Virgo.
    signVirgoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Virgo.
    signVirgoBackgroundColorKey = \
        "ui/astrology/VirgoBackgroundColor"

    # QSettings default value for the background color of the Virgo.
    signVirgoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeKey = \
        "ui/astrology/LibraGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeDefValue = "\u264e"

    # QSettings key for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeKey = \
        "ui/astrology/LibraGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Libra.
    signLibraAbbreviationKey = \
        "ui/astrology/LibraAbbreviation"

    # QSettings default value for the sign abbreviation of the Libra.
    signLibraAbbreviationDefValue = "Li"

    # QSettings key for the foreground color of the Libra.
    signLibraForegroundColorKey = \
        "ui/astrology/LibraForegroundColor"

    # QSettings default value for the foreground color of the Libra.
    signLibraForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Libra.
    signLibraBackgroundColorKey = \
        "ui/astrology/LibraBackgroundColor"

    # QSettings default value for the background color of the Libra.
    signLibraBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeKey = \
        "ui/astrology/ScorpioGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeDefValue = "\u264f"

    # QSettings key for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeKey = \
        "ui/astrology/ScorpioGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationKey = \
        "ui/astrology/ScorpioAbbreviation"

    # QSettings default value for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationDefValue = "Sc"

    # QSettings key for the foreground color of the Scorpio.
    signScorpioForegroundColorKey = \
        "ui/astrology/ScorpioForegroundColor"

    # QSettings default value for the foreground color of the Scorpio.
    signScorpioForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Scorpio.
    signScorpioBackgroundColorKey = \
        "ui/astrology/ScorpioBackgroundColor"

    # QSettings default value for the background color of the Scorpio.
    signScorpioBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeKey = \
        "ui/astrology/SagittariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeDefValue = "\u2650"

    # QSettings key for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeKey = \
        "ui/astrology/SagittariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationKey = \
        "ui/astrology/SagittariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Sagittarius.
    signSagittariusForegroundColorKey = \
        "ui/astrology/SagittariusForegroundColor"

    # QSettings default value for the foreground color of the Sagittarius.
    signSagittariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sagittarius.
    signSagittariusBackgroundColorKey = \
        "ui/astrology/SagittariusBackgroundColor"

    # QSettings default value for the background color of the Sagittarius.
    signSagittariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeKey = \
        "ui/astrology/CapricornGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeDefValue = "\u2651"

    # QSettings key for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeKey = \
        "ui/astrology/CapricornGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationKey = \
        "ui/astrology/CapricornAbbreviation"

    # QSettings default value for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationDefValue = "Cp"

    # QSettings key for the foreground color of the Capricorn.
    signCapricornForegroundColorKey = \
        "ui/astrology/CapricornForegroundColor"

    # QSettings default value for the foreground color of the Capricorn.
    signCapricornForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Capricorn.
    signCapricornBackgroundColorKey = \
        "ui/astrology/CapricornBackgroundColor"

    # QSettings default value for the background color of the Capricorn.
    signCapricornBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeKey = \
        "ui/astrology/AquariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeDefValue = "\u2652"

    # QSettings key for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeKey = \
        "ui/astrology/AquariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationKey = \
        "ui/astrology/AquariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationDefValue = "Aq"

    # QSettings key for the foreground color of the Aquarius.
    signAquariusForegroundColorKey = \
        "ui/astrology/AquariusForegroundColor"

    # QSettings default value for the foreground color of the Aquarius.
    signAquariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aquarius.
    signAquariusBackgroundColorKey = \
        "ui/astrology/AquariusBackgroundColor"

    # QSettings default value for the background color of the Aquarius.
    signAquariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeKey = \
        "ui/astrology/PiscesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeDefValue = "\u2653"

    # QSettings key for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeKey = \
        "ui/astrology/PiscesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Pisces.
    signPiscesAbbreviationKey = \
        "ui/astrology/PiscesAbbreviation"

    # QSettings default value for the sign abbreviation of the Pisces.
    signPiscesAbbreviationDefValue = "Pi"

    # QSettings key for the foreground color of the Pisces.
    signPiscesForegroundColorKey = \
        "ui/astrology/PiscesForegroundColor"

    # QSettings default value for the foreground color of the Pisces.
    signPiscesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pisces.
    signPiscesBackgroundColorKey = \
        "ui/astrology/PiscesBackgroundColor"

    # QSettings default value for the background color of the Pisces.
    signPiscesBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for aspects enabled on astrology chart 1.
    aspectAstrologyChart1EnabledKey = \
        "ui/astrology/aspectAstrologyChart1Enabled"

    # QSettings default value for aspect enabled on astrology chart 1.
    aspectAstrologyChart1EnabledDefValue = \
        True
    
    # QSettings key for aspects enabled on astrology chart 2.
    aspectAstrologyChart2EnabledKey = \
        "ui/astrology/aspectAstrologyChart2Enabled"

    # QSettings default value for aspect enabled on astrology chart 2.
    aspectAstrologyChart2EnabledDefValue = \
        True
    
    # QSettings key for aspects enabled on astrology chart 3.
    aspectAstrologyChart3EnabledKey = \
        "ui/astrology/aspectAstrologyChart3Enabled"

    # QSettings default value for aspect enabled on astrology chart 3.
    aspectAstrologyChart3EnabledDefValue = \
        True

    # QSettings key for aspects enabled between astrology chart 1 and 2.
    aspectBtwnAstrologyChart1And2EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart1And2Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 1 and 2.
    aspectBtwnAstrologyChart1And2EnabledDefValue = \
        False
    
    # QSettings key for aspects enabled between astrology chart 1 and 3.
    aspectBtwnAstrologyChart1And3EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart1And3Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 1 and 3.
    aspectBtwnAstrologyChart1And3EnabledDefValue = \
        False
    
    # QSettings key for aspects enabled between astrology chart 2 and 3.
    aspectBtwnAstrologyChart2And3EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart2And3Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 2 and 3.
    aspectBtwnAstrologyChart2And3EnabledDefValue = \
        False

    
    # QSettings key for the aspect Conjunction name.
    aspectConjunctionNameKey = \
        "ui/astrology/aspectConjunctionName"

    # QSettings default value for the aspect Conjunction name.
    aspectConjunctionNameDefValue = \
        "Conjunction"
    
    # QSettings key for the aspect Conjunction angle.
    aspectConjunctionAngleKey = \
        "ui/astrology/aspectConjunctionAngle"

    # QSettings default value for the aspect Conjunction angle (float).
    aspectConjunctionAngleDefValue = float(0.0)
    
    # QSettings key for the aspect Conjunction being enabled.
    aspectConjunctionEnabledKey = \
        "ui/astrology/aspectConjunctionEnabled"

    # QSettings default value for the aspect Conjunction being enabled.
    aspectConjunctionEnabledDefValue = True
    
    # QSettings key for the aspect Conjunction color.
    aspectConjunctionColorKey = \
        "ui/astrology/aspectConjunctionColor"

    # QSettings default value for the aspect Conjunction color.
    aspectConjunctionColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Conjunction orb in degrees.
    aspectConjunctionOrbKey = \
        "ui/astrology/aspectConjunctionOrb"

    # QSettings default value for the aspect Conjunction orb in degrees (float).
    aspectConjunctionOrbDefValue = float(6.0)


    
    # QSettings key for the aspect Opposition name.
    aspectOppositionNameKey = \
        "ui/astrology/aspectOppositionName"

    # QSettings default value for the aspect Opposition name.
    aspectOppositionNameDefValue = \
        "Opposition"
    
    # QSettings key for the aspect Opposition angle.
    aspectOppositionAngleKey = \
        "ui/astrology/aspectOppositionAngle"

    # QSettings default value for the aspect Opposition angle (float).
    aspectOppositionAngleDefValue = float(180.0)
    
    # QSettings key for the aspect Opposition being enabled.
    aspectOppositionEnabledKey = \
        "ui/astrology/aspectOppositionEnabled"

    # QSettings default value for the aspect Opposition being enabled.
    aspectOppositionEnabledDefValue = True
    
    # QSettings key for the aspect Opposition color.
    aspectOppositionColorKey = \
        "ui/astrology/aspectOppositionColor"

    # QSettings default value for the aspect Opposition color.
    aspectOppositionColorDefValue = QColor(Qt.blue)

    # QSettings key for the aspect Opposition orb in degrees.
    aspectOppositionOrbKey = \
        "ui/astrology/aspectOppositionOrb"

    # QSettings default value for the aspect Opposition orb in degrees (float).
    aspectOppositionOrbDefValue = float(6.0)



    # QSettings key for the aspect Square name.
    aspectSquareNameKey = \
        "ui/astrology/aspectSquareName"

    # QSettings default value for the aspect Square name.
    aspectSquareNameDefValue = \
        "Square"
    
    # QSettings key for the aspect Square angle.
    aspectSquareAngleKey = \
        "ui/astrology/aspectSquareAngle"

    # QSettings default value for the aspect Square angle (float).
    aspectSquareAngleDefValue = float(90.0)
    
    # QSettings key for the aspect Square being enabled.
    aspectSquareEnabledKey = \
        "ui/astrology/aspectSquareEnabled"

    # QSettings default value for the aspect Square being enabled.
    aspectSquareEnabledDefValue = True
    
    # QSettings key for the aspect Square color.
    aspectSquareColorKey = \
        "ui/astrology/aspectSquareColor"

    # QSettings default value for the aspect Square color.
    aspectSquareColorDefValue = QColor(Qt.red)

    # QSettings key for the aspect Square orb in degrees.
    aspectSquareOrbKey = \
        "ui/astrology/aspectSquareOrb"

    # QSettings default value for the aspect Square orb in degrees (float).
    aspectSquareOrbDefValue = float(6.0)



    # QSettings key for the aspect Trine name.
    aspectTrineNameKey = \
        "ui/astrology/aspectTrineName"

    # QSettings default value for the aspect Trine name.
    aspectTrineNameDefValue = \
        "Trine"
    
    # QSettings key for the aspect Trine angle.
    aspectTrineAngleKey = \
        "ui/astrology/aspectTrineAngle"

    # QSettings default value for the aspect Trine angle (float).
    aspectTrineAngleDefValue = float(120.0)
    
    # QSettings key for the aspect Trine being enabled.
    aspectTrineEnabledKey = \
        "ui/astrology/aspectTrineEnabled"

    # QSettings default value for the aspect Trine being enabled.
    aspectTrineEnabledDefValue = True
    
    # QSettings key for the aspect Trine color.
    aspectTrineColorKey = \
        "ui/astrology/aspectTrineColor"

    # QSettings default value for the aspect Trine color.
    aspectTrineColorDefValue = QColor(Qt.darkGreen)

    # QSettings key for the aspect Trine orb in degrees.
    aspectTrineOrbKey = \
        "ui/astrology/aspectTrineOrb"

    # QSettings default value for the aspect Trine orb in degrees (float).
    aspectTrineOrbDefValue = float(6.0)



    # QSettings key for the aspect Sextile name.
    aspectSextileNameKey = \
        "ui/astrology/aspectSextileName"

    # QSettings default value for the aspect Sextile name.
    aspectSextileNameDefValue = \
        "Sextile"
    
    # QSettings key for the aspect Sextile angle.
    aspectSextileAngleKey = \
        "ui/astrology/aspectSextileAngle"

    # QSettings default value for the aspect Sextile angle (float).
    aspectSextileAngleDefValue = float(60.0)
    
    # QSettings key for the aspect Sextile being enabled.
    aspectSextileEnabledKey = \
        "ui/astrology/aspectSextileEnabled"

    # QSettings default value for the aspect Sextile being enabled.
    aspectSextileEnabledDefValue = True
    
    # QSettings key for the aspect Sextile color.
    aspectSextileColorKey = \
        "ui/astrology/aspectSextileColor"

    # QSettings default value for the aspect Sextile color.
    aspectSextileColorDefValue = QColor(Qt.darkCyan)

    # QSettings key for the aspect Sextile orb in degrees.
    aspectSextileOrbKey = \
        "ui/astrology/aspectSextileOrb"

    # QSettings default value for the aspect Sextile orb in degrees (float).
    aspectSextileOrbDefValue = float(5.0)



    # QSettings key for the aspect Inconjunct name.
    aspectInconjunctNameKey = \
        "ui/astrology/aspectInconjunctName"

    # QSettings default value for the aspect Inconjunct name.
    aspectInconjunctNameDefValue = \
        "Inconjunct"
    
    # QSettings key for the aspect Inconjunct angle.
    aspectInconjunctAngleKey = \
        "ui/astrology/aspectInconjunctAngle"

    # QSettings default value for the aspect Inconjunct angle (float).
    aspectInconjunctAngleDefValue = float(150.0)
    
    # QSettings key for the aspect Inconjunct being enabled.
    aspectInconjunctEnabledKey = \
        "ui/astrology/aspectInconjunctEnabled"

    # QSettings default value for the aspect Inconjunct being enabled.
    aspectInconjunctEnabledDefValue = False
    
    # QSettings key for the aspect Inconjunct color.
    aspectInconjunctColorKey = \
        "ui/astrology/aspectInconjunctColor"

    # QSettings default value for the aspect Inconjunct color.
    aspectInconjunctColorDefValue = QColor(Qt.magenta)

    # QSettings key for the aspect Inconjunct orb in degrees.
    aspectInconjunctOrbKey = \
        "ui/astrology/aspectInconjunctOrb"

    # QSettings default value for the aspect Inconjunct orb in degrees (float).
    aspectInconjunctOrbDefValue = float(3.0)



    # QSettings key for the aspect Semisextile name.
    aspectSemisextileNameKey = \
        "ui/astrology/aspectSemisextileName"

    # QSettings default value for the aspect Semisextile name.
    aspectSemisextileNameDefValue = \
        "Semisextile"
    
    # QSettings key for the aspect Semisextile angle.
    aspectSemisextileAngleKey = \
        "ui/astrology/aspectSemisextileAngle"

    # QSettings default value for the aspect Semisextile angle (float).
    aspectSemisextileAngleDefValue = float(30.0)
    
    # QSettings key for the aspect Semisextile being enabled.
    aspectSemisextileEnabledKey = \
        "ui/astrology/aspectSemisextileEnabled"

    # QSettings default value for the aspect Semisextile being enabled.
    aspectSemisextileEnabledDefValue = False
    
    # QSettings key for the aspect Semisextile color.
    aspectSemisextileColorKey = \
        "ui/astrology/aspectSemisextileColor"

    # QSettings default value for the aspect Semisextile color.
    aspectSemisextileColorDefValue = QColor(Qt.magenta)

    # QSettings key for the aspect Semisextile orb in degrees.
    aspectSemisextileOrbKey = \
        "ui/astrology/aspectSemisextileOrb"

    # QSettings default value for the aspect Semisextile orb in degrees (float).
    aspectSemisextileOrbDefValue = float(3.0)



    # QSettings key for the aspect Semisquare name.
    aspectSemisquareNameKey = \
        "ui/astrology/aspectSemisquareName"

    # QSettings default value for the aspect Semisquare name.
    aspectSemisquareNameDefValue = \
        "Semisquare"
    
    # QSettings key for the aspect Semisquare angle.
    aspectSemisquareAngleKey = \
        "ui/astrology/aspectSemisquareAngle"

    # QSettings default value for the aspect Semisquare angle (float).
    aspectSemisquareAngleDefValue = float(45.0)
    
    # QSettings key for the aspect Semisquare being enabled.
    aspectSemisquareEnabledKey = \
        "ui/astrology/aspectSemisquareEnabled"

    # QSettings default value for the aspect Semisquare being enabled.
    aspectSemisquareEnabledDefValue = False
    
    # QSettings key for the aspect Semisquare color.
    aspectSemisquareColorKey = \
        "ui/astrology/aspectSemisquareColor"

    # QSettings default value for the aspect Semisquare color.
    aspectSemisquareColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Semisquare orb in degrees.
    aspectSemisquareOrbKey = \
        "ui/astrology/aspectSemisquareOrb"

    # QSettings default value for the aspect Semisquare orb in degrees (float).
    aspectSemisquareOrbDefValue = float(3.0)



    # QSettings key for the aspect Sesquiquadrate name.
    aspectSesquiquadrateNameKey = \
        "ui/astrology/aspectSesquiquadrateName"

    # QSettings default value for the aspect Sesquiquadrate name.
    aspectSesquiquadrateNameDefValue = \
        "Sesquiquadrate"
    
    # QSettings key for the aspect Sesquiquadrate angle.
    aspectSesquiquadrateAngleKey = \
        "ui/astrology/aspectSesquiquadrateAngle"

    # QSettings default value for the aspect Sesquiquadrate angle (float).
    aspectSesquiquadrateAngleDefValue = float(135.0)
    
    # QSettings key for the aspect Sesquiquadrate being enabled.
    aspectSesquiquadrateEnabledKey = \
        "ui/astrology/aspectSesquiquadrateEnabled"

    # QSettings default value for the aspect Sesquiquadrate being enabled.
    aspectSesquiquadrateEnabledDefValue = False
    
    # QSettings key for the aspect Sesquiquadrate color.
    aspectSesquiquadrateColorKey = \
        "ui/astrology/aspectSesquiquadrateColor"

    # QSettings default value for the aspect Sesquiquadrate color.
    aspectSesquiquadrateColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Sesquiquadrate orb in degrees.
    aspectSesquiquadrateOrbKey = \
        "ui/astrology/aspectSesquiquadrateOrb"

    # QSettings default value for the aspect Sesquiquadrate orb in degrees (float).
    aspectSesquiquadrateOrbDefValue = float(3.0)



    # QSettings key for enabled astrologychart calculations for H1.
    planetH1CalculationsEnabledKey = \
        "ui/astrology/H1CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H1.
    planetH1CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H2.
    planetH2CalculationsEnabledKey = \
        "ui/astrology/H2CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H2.
    planetH2CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H3.
    planetH3CalculationsEnabledKey = \
        "ui/astrology/H3CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H3.
    planetH3CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H4.
    planetH4CalculationsEnabledKey = \
        "ui/astrology/H4CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H4.
    planetH4CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H5.
    planetH5CalculationsEnabledKey = \
        "ui/astrology/H5CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H5.
    planetH5CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H6.
    planetH6CalculationsEnabledKey = \
        "ui/astrology/H6CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H6.
    planetH6CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H7.
    planetH7CalculationsEnabledKey = \
        "ui/astrology/H7CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H7.
    planetH7CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H8.
    planetH8CalculationsEnabledKey = \
        "ui/astrology/H8CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H8.
    planetH8CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H9.
    planetH9CalculationsEnabledKey = \
        "ui/astrology/H9CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H9.
    planetH9CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H10.
    planetH10CalculationsEnabledKey = \
        "ui/astrology/H10CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H10.
    planetH10CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H11.
    planetH11CalculationsEnabledKey = \
        "ui/astrology/H11CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H11.
    planetH11CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H12.
    planetH12CalculationsEnabledKey = \
        "ui/astrology/H12CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H12.
    planetH12CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for ARMC.
    planetARMCCalculationsEnabledKey = \
        "ui/astrology/ARMCCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for ARMC.
    planetARMCCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Vertex.
    planetVertexCalculationsEnabledKey = \
        "ui/astrology/VertexCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Vertex.
    planetVertexCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for EquatorialAscendant.
    planetEquatorialAscendantCalculationsEnabledKey = \
        "ui/astrology/EquatorialAscendantCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for EquatorialAscendant.
    planetEquatorialAscendantCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for CoAscendant1.
    planetCoAscendant1CalculationsEnabledKey = \
        "ui/astrology/CoAscendant1CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for CoAscendant1.
    planetCoAscendant1CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for CoAscendant2.
    planetCoAscendant2CalculationsEnabledKey = \
        "ui/astrology/CoAscendant2CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for CoAscendant2.
    planetCoAscendant2CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for PolarAscendant.
    planetPolarAscendantCalculationsEnabledKey = \
        "ui/astrology/PolarAscendantCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for PolarAscendant.
    planetPolarAscendantCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for HoraLagna.
    planetHoraLagnaCalculationsEnabledKey = \
        "ui/astrology/HoraLagnaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for HoraLagna.
    planetHoraLagnaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for GhatiLagna.
    planetGhatiLagnaCalculationsEnabledKey = \
        "ui/astrology/GhatiLagnaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for GhatiLagna.
    planetGhatiLagnaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeanLunarApogee.
    planetMeanLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/MeanLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanLunarApogee.
    planetMeanLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for OsculatingLunarApogee.
    planetOsculatingLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/OsculatingLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for OsculatingLunarApogee.
    planetOsculatingLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/InterpolatedLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeCalculationsEnabledKey = \
        "ui/astrology/InterpolatedLunarPerigeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Sun.
    planetSunCalculationsEnabledKey = \
        "ui/astrology/SunCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Sun.
    planetSunCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Moon.
    planetMoonCalculationsEnabledKey = \
        "ui/astrology/MoonCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Moon.
    planetMoonCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Mercury.
    planetMercuryCalculationsEnabledKey = \
        "ui/astrology/MercuryCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mercury.
    planetMercuryCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Venus.
    planetVenusCalculationsEnabledKey = \
        "ui/astrology/VenusCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Venus.
    planetVenusCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Earth.
    planetEarthCalculationsEnabledKey = \
        "ui/astrology/EarthCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Earth.
    planetEarthCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Mars.
    planetMarsCalculationsEnabledKey = \
        "ui/astrology/MarsCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mars.
    planetMarsCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Jupiter.
    planetJupiterCalculationsEnabledKey = \
        "ui/astrology/JupiterCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Jupiter.
    planetJupiterCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Saturn.
    planetSaturnCalculationsEnabledKey = \
        "ui/astrology/SaturnCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Saturn.
    planetSaturnCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Uranus.
    planetUranusCalculationsEnabledKey = \
        "ui/astrology/UranusCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Uranus.
    planetUranusCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Neptune.
    planetNeptuneCalculationsEnabledKey = \
        "ui/astrology/NeptuneCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Neptune.
    planetNeptuneCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Pluto.
    planetPlutoCalculationsEnabledKey = \
        "ui/astrology/PlutoCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Pluto.
    planetPlutoCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for MeanNorthNode.
    planetMeanNorthNodeCalculationsEnabledKey = \
        "ui/astrology/MeanNorthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanNorthNode.
    planetMeanNorthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for MeanSouthNode.
    planetMeanSouthNodeCalculationsEnabledKey = \
        "ui/astrology/MeanSouthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanSouthNode.
    planetMeanSouthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for TrueNorthNode.
    planetTrueNorthNodeCalculationsEnabledKey = \
        "ui/astrology/TrueNorthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for TrueNorthNode.
    planetTrueNorthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for TrueSouthNode.
    planetTrueSouthNodeCalculationsEnabledKey = \
        "ui/astrology/TrueSouthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for TrueSouthNode.
    planetTrueSouthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Ceres.
    planetCeresCalculationsEnabledKey = \
        "ui/astrology/CeresCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Ceres.
    planetCeresCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Pallas.
    planetPallasCalculationsEnabledKey = \
        "ui/astrology/PallasCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Pallas.
    planetPallasCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Juno.
    planetJunoCalculationsEnabledKey = \
        "ui/astrology/JunoCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Juno.
    planetJunoCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Vesta.
    planetVestaCalculationsEnabledKey = \
        "ui/astrology/VestaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Vesta.
    planetVestaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Isis.
    planetIsisCalculationsEnabledKey = \
        "ui/astrology/IsisCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Isis.
    planetIsisCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Nibiru.
    planetNibiruCalculationsEnabledKey = \
        "ui/astrology/NibiruCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Nibiru.
    planetNibiruCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Chiron.
    planetChironCalculationsEnabledKey = \
        "ui/astrology/ChironCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Chiron.
    planetChironCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Gulika.
    planetGulikaCalculationsEnabledKey = \
        "ui/astrology/GulikaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Gulika.
    planetGulikaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Mandi.
    planetMandiCalculationsEnabledKey = \
        "ui/astrology/MandiCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mandi.
    planetMandiCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeanOfFive.
    planetMeanOfFiveCalculationsEnabledKey = \
        "ui/astrology/MeanOfFiveCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanOfFive.
    planetMeanOfFiveCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for CycleOfEight.
    planetCycleOfEightCalculationsEnabledKey = \
        "ui/astrology/CycleOfEightCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for CycleOfEight.
    planetCycleOfEightCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlCalculationsEnabledKey = \
        "ui/astrology/AvgMaJuSaUrNePlCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgJuSaUrNe.
    planetAvgJuSaUrNeCalculationsEnabledKey = \
        "ui/astrology/AvgJuSaUrNeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgJuSaUrNe.
    planetAvgJuSaUrNeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgJuSa.
    planetAvgJuSaCalculationsEnabledKey = \
        "ui/astrology/AvgJuSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgJuSa.
    planetAvgJuSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AsSu.
    planetAsSuCalculationsEnabledKey = \
        "ui/astrology/AsSuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AsSu.
    planetAsSuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AsMo.
    planetAsMoCalculationsEnabledKey = \
        "ui/astrology/AsMoCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AsMo.
    planetAsMoCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MoSu.
    planetMoSuCalculationsEnabledKey = \
        "ui/astrology/MoSuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MoSu.
    planetMoSuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeVe.
    planetMeVeCalculationsEnabledKey = \
        "ui/astrology/MeVeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeVe.
    planetMeVeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeEa.
    planetMeEaCalculationsEnabledKey = \
        "ui/astrology/MeEaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeEa.
    planetMeEaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeMa.
    planetMeMaCalculationsEnabledKey = \
        "ui/astrology/MeMaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeMa.
    planetMeMaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeJu.
    planetMeJuCalculationsEnabledKey = \
        "ui/astrology/MeJuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeJu.
    planetMeJuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeSa.
    planetMeSaCalculationsEnabledKey = \
        "ui/astrology/MeSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeSa.
    planetMeSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeUr.
    planetMeUrCalculationsEnabledKey = \
        "ui/astrology/MeUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeUr.
    planetMeUrCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for VeEa.
    planetVeEaCalculationsEnabledKey = \
        "ui/astrology/VeEaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for VeEa.
    planetVeEaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for VeMa.
    planetVeMaCalculationsEnabledKey = \
        "ui/astrology/VeMaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for VeMa.
    planetVeMaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for VeJu.
    planetVeJuCalculationsEnabledKey = \
        "ui/astrology/VeJuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for VeJu.
    planetVeJuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for VeSa.
    planetVeSaCalculationsEnabledKey = \
        "ui/astrology/VeSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for VeSa.
    planetVeSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for VeUr.
    planetVeUrCalculationsEnabledKey = \
        "ui/astrology/VeUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for VeUr.
    planetVeUrCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for EaMa.
    planetEaMaCalculationsEnabledKey = \
        "ui/astrology/EaMaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for EaMa.
    planetEaMaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for EaJu.
    planetEaJuCalculationsEnabledKey = \
        "ui/astrology/EaJuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for EaJu.
    planetEaJuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for EaSa.
    planetEaSaCalculationsEnabledKey = \
        "ui/astrology/EaSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for EaSa.
    planetEaSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for EaUr.
    planetEaUrCalculationsEnabledKey = \
        "ui/astrology/EaUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for EaUr.
    planetEaUrCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MaJu.
    planetMaJuCalculationsEnabledKey = \
        "ui/astrology/MaJuCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MaJu.
    planetMaJuCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MaSa.
    planetMaSaCalculationsEnabledKey = \
        "ui/astrology/MaSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MaSa.
    planetMaSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MaUr.
    planetMaUrCalculationsEnabledKey = \
        "ui/astrology/MaUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MaUr.
    planetMaUrCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for JuSa.
    planetJuSaCalculationsEnabledKey = \
        "ui/astrology/JuSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for JuSa.
    planetJuSaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for JuUr.
    planetJuUrCalculationsEnabledKey = \
        "ui/astrology/JuUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for JuUr.
    planetJuUrCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for SaUr.
    planetSaUrCalculationsEnabledKey = \
        "ui/astrology/SaUrCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for SaUr.
    planetSaUrCalculationsEnabledDefValue = \
        False



    # QSettings key for the display flag in PlanetaryInfoTable for H1.
    planetH1EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H1EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H1.
    planetH1EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H2.
    planetH2EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H2EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H2.
    planetH2EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H3.
    planetH3EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H3EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H3.
    planetH3EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H4.
    planetH4EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H4EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H4.
    planetH4EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H5.
    planetH5EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H5EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H5.
    planetH5EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H6.
    planetH6EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H6EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H6.
    planetH6EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H7.
    planetH7EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H7EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H7.
    planetH7EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H8.
    planetH8EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H8EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H8.
    planetH8EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H9.
    planetH9EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H9EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H9.
    planetH9EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H10.
    planetH10EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H10EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H10.
    planetH10EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H11.
    planetH11EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H11EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H11.
    planetH11EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H12.
    planetH12EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/H12EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H12.
    planetH12EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for ARMC.
    planetARMCEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/ARMCEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for ARMC.
    planetARMCEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Vertex.
    planetVertexEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VertexEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Vertex.
    planetVertexEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for EquatorialAscendant.
    planetEquatorialAscendantEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EquatorialAscendantEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for EquatorialAscendant.
    planetEquatorialAscendantEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for CoAscendant1.
    planetCoAscendant1EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/CoAscendant1EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for CoAscendant1.
    planetCoAscendant1EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for CoAscendant2.
    planetCoAscendant2EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/CoAscendant2EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for CoAscendant2.
    planetCoAscendant2EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for PolarAscendant.
    planetPolarAscendantEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/PolarAscendantEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for PolarAscendant.
    planetPolarAscendantEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for HoraLagna.
    planetHoraLagnaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/HoraLagnaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for HoraLagna.
    planetHoraLagnaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for GhatiLagna.
    planetGhatiLagnaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/GhatiLagnaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for GhatiLagna.
    planetGhatiLagnaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeanLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Sun.
    planetSunEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/SunEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Sun.
    planetSunEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Moon.
    planetMoonEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MoonEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Moon.
    planetMoonEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mercury.
    planetMercuryEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MercuryEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mercury.
    planetMercuryEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Venus.
    planetVenusEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VenusEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Venus.
    planetVenusEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Earth.
    planetEarthEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EarthEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Earth.
    planetEarthEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mars.
    planetMarsEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MarsEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mars.
    planetMarsEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Jupiter.
    planetJupiterEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/JupiterEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Jupiter.
    planetJupiterEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Saturn.
    planetSaturnEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/SaturnEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Saturn.
    planetSaturnEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Uranus.
    planetUranusEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/UranusEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Uranus.
    planetUranusEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Neptune.
    planetNeptuneEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/NeptuneEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Neptune.
    planetNeptuneEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Pluto.
    planetPlutoEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/PlutoEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Pluto.
    planetPlutoEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanNorthNode.
    planetMeanNorthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeanNorthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanNorthNode.
    planetMeanNorthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanSouthNode.
    planetMeanSouthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeanSouthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanSouthNode.
    planetMeanSouthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for TrueNorthNode.
    planetTrueNorthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/TrueNorthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for TrueNorthNode.
    planetTrueNorthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for TrueSouthNode.
    planetTrueSouthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/TrueSouthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for TrueSouthNode.
    planetTrueSouthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Ceres.
    planetCeresEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/CeresEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Ceres.
    planetCeresEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Pallas.
    planetPallasEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/PallasEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Pallas.
    planetPallasEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Juno.
    planetJunoEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/JunoEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Juno.
    planetJunoEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Vesta.
    planetVestaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VestaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Vesta.
    planetVestaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Isis.
    planetIsisEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/IsisEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Isis.
    planetIsisEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Nibiru.
    planetNibiruEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/NibiruEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Nibiru.
    planetNibiruEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Chiron.
    planetChironEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/ChironEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Chiron.
    planetChironEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Gulika.
    planetGulikaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/GulikaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Gulika.
    planetGulikaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mandi.
    planetMandiEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MandiEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mandi.
    planetMandiEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanOfFive.
    planetMeanOfFiveEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeanOfFiveEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanOfFive.
    planetMeanOfFiveEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for CycleOfEight.
    planetCycleOfEightEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/CycleOfEightEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for CycleOfEight.
    planetCycleOfEightEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgJuSa.
    planetAvgJuSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/AvgJuSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgJuSa.
    planetAvgJuSaEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AsSu.
    planetAsSuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/AsSuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AsSu.
    planetAsSuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for AsMo.
    planetAsMoEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/AsMoEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AsMo.
    planetAsMoEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MoSu.
    planetMoSuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MoSuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MoSu.
    planetMoSuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeVe.
    planetMeVeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeVeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeVe.
    planetMeVeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeEa.
    planetMeEaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeEaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeEa.
    planetMeEaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeMa.
    planetMeMaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeMaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeMa.
    planetMeMaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeJu.
    planetMeJuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeJuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeJu.
    planetMeJuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeSa.
    planetMeSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeSa.
    planetMeSaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeUr.
    planetMeUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MeUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeUr.
    planetMeUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for VeEa.
    planetVeEaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VeEaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for VeEa.
    planetVeEaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for VeMa.
    planetVeMaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VeMaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for VeMa.
    planetVeMaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for VeJu.
    planetVeJuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VeJuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for VeJu.
    planetVeJuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for VeSa.
    planetVeSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VeSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for VeSa.
    planetVeSaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for VeUr.
    planetVeUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/VeUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for VeUr.
    planetVeUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for EaMa.
    planetEaMaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EaMaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for EaMa.
    planetEaMaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for EaJu.
    planetEaJuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EaJuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for EaJu.
    planetEaJuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for EaSa.
    planetEaSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EaSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for EaSa.
    planetEaSaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for EaUr.
    planetEaUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/EaUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for EaUr.
    planetEaUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MaJu.
    planetMaJuEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MaJuEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MaJu.
    planetMaJuEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MaSa.
    planetMaSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MaSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MaSa.
    planetMaSaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MaUr.
    planetMaUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/MaUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MaUr.
    planetMaUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for JuSa.
    planetJuSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/JuSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for JuSa.
    planetJuSaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for JuUr.
    planetJuUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/JuUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for JuUr.
    planetJuUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for SaUr.
    planetSaUrEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/SaUrEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for SaUr.
    planetSaUrEnabledForPlanetaryInfoTableDefValue = \
        False
    
    
    
    # QSettings key for the display flag in Declination for H1.
    planetH1EnabledForDeclinationKey = \
        "ui/astrology/H1EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H1.
    planetH1EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H2.
    planetH2EnabledForDeclinationKey = \
        "ui/astrology/H2EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H2.
    planetH2EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H3.
    planetH3EnabledForDeclinationKey = \
        "ui/astrology/H3EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H3.
    planetH3EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H4.
    planetH4EnabledForDeclinationKey = \
        "ui/astrology/H4EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H4.
    planetH4EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H5.
    planetH5EnabledForDeclinationKey = \
        "ui/astrology/H5EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H5.
    planetH5EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H6.
    planetH6EnabledForDeclinationKey = \
        "ui/astrology/H6EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H6.
    planetH6EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H7.
    planetH7EnabledForDeclinationKey = \
        "ui/astrology/H7EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H7.
    planetH7EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H8.
    planetH8EnabledForDeclinationKey = \
        "ui/astrology/H8EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H8.
    planetH8EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H9.
    planetH9EnabledForDeclinationKey = \
        "ui/astrology/H9EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H9.
    planetH9EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H10.
    planetH10EnabledForDeclinationKey = \
        "ui/astrology/H10EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H10.
    planetH10EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H11.
    planetH11EnabledForDeclinationKey = \
        "ui/astrology/H11EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H11.
    planetH11EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H12.
    planetH12EnabledForDeclinationKey = \
        "ui/astrology/H12EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H12.
    planetH12EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for ARMC.
    planetARMCEnabledForDeclinationKey = \
        "ui/astrology/ARMCEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for ARMC.
    planetARMCEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Vertex.
    planetVertexEnabledForDeclinationKey = \
        "ui/astrology/VertexEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Vertex.
    planetVertexEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for EquatorialAscendant.
    planetEquatorialAscendantEnabledForDeclinationKey = \
        "ui/astrology/EquatorialAscendantEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for EquatorialAscendant.
    planetEquatorialAscendantEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for CoAscendant1.
    planetCoAscendant1EnabledForDeclinationKey = \
        "ui/astrology/CoAscendant1EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for CoAscendant1.
    planetCoAscendant1EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for CoAscendant2.
    planetCoAscendant2EnabledForDeclinationKey = \
        "ui/astrology/CoAscendant2EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for CoAscendant2.
    planetCoAscendant2EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for PolarAscendant.
    planetPolarAscendantEnabledForDeclinationKey = \
        "ui/astrology/PolarAscendantEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for PolarAscendant.
    planetPolarAscendantEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for HoraLagna.
    planetHoraLagnaEnabledForDeclinationKey = \
        "ui/astrology/HoraLagnaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for HoraLagna.
    planetHoraLagnaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for GhatiLagna.
    planetGhatiLagnaEnabledForDeclinationKey = \
        "ui/astrology/GhatiLagnaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for GhatiLagna.
    planetGhatiLagnaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/MeanLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForDeclinationKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Sun.
    planetSunEnabledForDeclinationKey = \
        "ui/astrology/SunEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Sun.
    planetSunEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Moon.
    planetMoonEnabledForDeclinationKey = \
        "ui/astrology/MoonEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Moon.
    planetMoonEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Mercury.
    planetMercuryEnabledForDeclinationKey = \
        "ui/astrology/MercuryEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mercury.
    planetMercuryEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Venus.
    planetVenusEnabledForDeclinationKey = \
        "ui/astrology/VenusEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Venus.
    planetVenusEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Earth.
    planetEarthEnabledForDeclinationKey = \
        "ui/astrology/EarthEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Earth.
    planetEarthEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Mars.
    planetMarsEnabledForDeclinationKey = \
        "ui/astrology/MarsEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mars.
    planetMarsEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Jupiter.
    planetJupiterEnabledForDeclinationKey = \
        "ui/astrology/JupiterEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Jupiter.
    planetJupiterEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Saturn.
    planetSaturnEnabledForDeclinationKey = \
        "ui/astrology/SaturnEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Saturn.
    planetSaturnEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Uranus.
    planetUranusEnabledForDeclinationKey = \
        "ui/astrology/UranusEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Uranus.
    planetUranusEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Neptune.
    planetNeptuneEnabledForDeclinationKey = \
        "ui/astrology/NeptuneEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Neptune.
    planetNeptuneEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Pluto.
    planetPlutoEnabledForDeclinationKey = \
        "ui/astrology/PlutoEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Pluto.
    planetPlutoEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for MeanNorthNode.
    planetMeanNorthNodeEnabledForDeclinationKey = \
        "ui/astrology/MeanNorthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanNorthNode.
    planetMeanNorthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanSouthNode.
    planetMeanSouthNodeEnabledForDeclinationKey = \
        "ui/astrology/MeanSouthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanSouthNode.
    planetMeanSouthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for TrueNorthNode.
    planetTrueNorthNodeEnabledForDeclinationKey = \
        "ui/astrology/TrueNorthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for TrueNorthNode.
    planetTrueNorthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for TrueSouthNode.
    planetTrueSouthNodeEnabledForDeclinationKey = \
        "ui/astrology/TrueSouthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for TrueSouthNode.
    planetTrueSouthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Ceres.
    planetCeresEnabledForDeclinationKey = \
        "ui/astrology/CeresEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Ceres.
    planetCeresEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Pallas.
    planetPallasEnabledForDeclinationKey = \
        "ui/astrology/PallasEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Pallas.
    planetPallasEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Juno.
    planetJunoEnabledForDeclinationKey = \
        "ui/astrology/JunoEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Juno.
    planetJunoEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Vesta.
    planetVestaEnabledForDeclinationKey = \
        "ui/astrology/VestaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Vesta.
    planetVestaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Isis.
    planetIsisEnabledForDeclinationKey = \
        "ui/astrology/IsisEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Isis.
    planetIsisEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Nibiru.
    planetNibiruEnabledForDeclinationKey = \
        "ui/astrology/NibiruEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Nibiru.
    planetNibiruEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Chiron.
    planetChironEnabledForDeclinationKey = \
        "ui/astrology/ChironEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Chiron.
    planetChironEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Gulika.
    planetGulikaEnabledForDeclinationKey = \
        "ui/astrology/GulikaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Gulika.
    planetGulikaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Mandi.
    planetMandiEnabledForDeclinationKey = \
        "ui/astrology/MandiEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mandi.
    planetMandiEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanOfFive.
    planetMeanOfFiveEnabledForDeclinationKey = \
        "ui/astrology/MeanOfFiveEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanOfFive.
    planetMeanOfFiveEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for CycleOfEight.
    planetCycleOfEightEnabledForDeclinationKey = \
        "ui/astrology/CycleOfEightEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for CycleOfEight.
    planetCycleOfEightEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForDeclinationKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForDeclinationKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgJuSa.
    planetAvgJuSaEnabledForDeclinationKey = \
        "ui/astrology/AvgJuSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgJuSa.
    planetAvgJuSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AsSu.
    planetAsSuEnabledForDeclinationKey = \
        "ui/astrology/AsSuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AsSu.
    planetAsSuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AsMo.
    planetAsMoEnabledForDeclinationKey = \
        "ui/astrology/AsMoEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AsMo.
    planetAsMoEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MoSu.
    planetMoSuEnabledForDeclinationKey = \
        "ui/astrology/MoSuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MoSu.
    planetMoSuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeVe.
    planetMeVeEnabledForDeclinationKey = \
        "ui/astrology/MeVeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeVe.
    planetMeVeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeEa.
    planetMeEaEnabledForDeclinationKey = \
        "ui/astrology/MeEaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeEa.
    planetMeEaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeMa.
    planetMeMaEnabledForDeclinationKey = \
        "ui/astrology/MeMaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeMa.
    planetMeMaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeJu.
    planetMeJuEnabledForDeclinationKey = \
        "ui/astrology/MeJuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeJu.
    planetMeJuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeSa.
    planetMeSaEnabledForDeclinationKey = \
        "ui/astrology/MeSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeSa.
    planetMeSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeUr.
    planetMeUrEnabledForDeclinationKey = \
        "ui/astrology/MeUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeUr.
    planetMeUrEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for VeEa.
    planetVeEaEnabledForDeclinationKey = \
        "ui/astrology/VeEaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for VeEa.
    planetVeEaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for VeMa.
    planetVeMaEnabledForDeclinationKey = \
        "ui/astrology/VeMaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for VeMa.
    planetVeMaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for VeJu.
    planetVeJuEnabledForDeclinationKey = \
        "ui/astrology/VeJuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for VeJu.
    planetVeJuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for VeSa.
    planetVeSaEnabledForDeclinationKey = \
        "ui/astrology/VeSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for VeSa.
    planetVeSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for VeUr.
    planetVeUrEnabledForDeclinationKey = \
        "ui/astrology/VeUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for VeUr.
    planetVeUrEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for EaMa.
    planetEaMaEnabledForDeclinationKey = \
        "ui/astrology/EaMaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for EaMa.
    planetEaMaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for EaJu.
    planetEaJuEnabledForDeclinationKey = \
        "ui/astrology/EaJuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for EaJu.
    planetEaJuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for EaSa.
    planetEaSaEnabledForDeclinationKey = \
        "ui/astrology/EaSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for EaSa.
    planetEaSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for EaUr.
    planetEaUrEnabledForDeclinationKey = \
        "ui/astrology/EaUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for EaUr.
    planetEaUrEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MaJu.
    planetMaJuEnabledForDeclinationKey = \
        "ui/astrology/MaJuEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MaJu.
    planetMaJuEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MaSa.
    planetMaSaEnabledForDeclinationKey = \
        "ui/astrology/MaSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MaSa.
    planetMaSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MaUr.
    planetMaUrEnabledForDeclinationKey = \
        "ui/astrology/MaUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MaUr.
    planetMaUrEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for JuSa.
    planetJuSaEnabledForDeclinationKey = \
        "ui/astrology/JuSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for JuSa.
    planetJuSaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for JuUr.
    planetJuUrEnabledForDeclinationKey = \
        "ui/astrology/JuUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for JuUr.
    planetJuUrEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for SaUr.
    planetSaUrEnabledForDeclinationKey = \
        "ui/astrology/SaUrEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for SaUr.
    planetSaUrEnabledForDeclinationDefValue = \
        False
    


    # QSettings key for the display flag in Latitude for H1.
    planetH1EnabledForLatitudeKey = \
        "ui/astrology/H1EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H1.
    planetH1EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H2.
    planetH2EnabledForLatitudeKey = \
        "ui/astrology/H2EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H2.
    planetH2EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H3.
    planetH3EnabledForLatitudeKey = \
        "ui/astrology/H3EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H3.
    planetH3EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H4.
    planetH4EnabledForLatitudeKey = \
        "ui/astrology/H4EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H4.
    planetH4EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H5.
    planetH5EnabledForLatitudeKey = \
        "ui/astrology/H5EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H5.
    planetH5EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H6.
    planetH6EnabledForLatitudeKey = \
        "ui/astrology/H6EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H6.
    planetH6EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H7.
    planetH7EnabledForLatitudeKey = \
        "ui/astrology/H7EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H7.
    planetH7EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H8.
    planetH8EnabledForLatitudeKey = \
        "ui/astrology/H8EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H8.
    planetH8EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H9.
    planetH9EnabledForLatitudeKey = \
        "ui/astrology/H9EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H9.
    planetH9EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H10.
    planetH10EnabledForLatitudeKey = \
        "ui/astrology/H10EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H10.
    planetH10EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H11.
    planetH11EnabledForLatitudeKey = \
        "ui/astrology/H11EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H11.
    planetH11EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H12.
    planetH12EnabledForLatitudeKey = \
        "ui/astrology/H12EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H12.
    planetH12EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for ARMC.
    planetARMCEnabledForLatitudeKey = \
        "ui/astrology/ARMCEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for ARMC.
    planetARMCEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Vertex.
    planetVertexEnabledForLatitudeKey = \
        "ui/astrology/VertexEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Vertex.
    planetVertexEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for EquatorialAscendant.
    planetEquatorialAscendantEnabledForLatitudeKey = \
        "ui/astrology/EquatorialAscendantEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for EquatorialAscendant.
    planetEquatorialAscendantEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for CoAscendant1.
    planetCoAscendant1EnabledForLatitudeKey = \
        "ui/astrology/CoAscendant1EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for CoAscendant1.
    planetCoAscendant1EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for CoAscendant2.
    planetCoAscendant2EnabledForLatitudeKey = \
        "ui/astrology/CoAscendant2EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for CoAscendant2.
    planetCoAscendant2EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for PolarAscendant.
    planetPolarAscendantEnabledForLatitudeKey = \
        "ui/astrology/PolarAscendantEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for PolarAscendant.
    planetPolarAscendantEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for HoraLagna.
    planetHoraLagnaEnabledForLatitudeKey = \
        "ui/astrology/HoraLagnaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for HoraLagna.
    planetHoraLagnaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for GhatiLagna.
    planetGhatiLagnaEnabledForLatitudeKey = \
        "ui/astrology/GhatiLagnaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for GhatiLagna.
    planetGhatiLagnaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/MeanLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForLatitudeKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Sun.
    planetSunEnabledForLatitudeKey = \
        "ui/astrology/SunEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Sun.
    planetSunEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Moon.
    planetMoonEnabledForLatitudeKey = \
        "ui/astrology/MoonEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Moon.
    planetMoonEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Mercury.
    planetMercuryEnabledForLatitudeKey = \
        "ui/astrology/MercuryEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mercury.
    planetMercuryEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Venus.
    planetVenusEnabledForLatitudeKey = \
        "ui/astrology/VenusEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Venus.
    planetVenusEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Earth.
    planetEarthEnabledForLatitudeKey = \
        "ui/astrology/EarthEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Earth.
    planetEarthEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Mars.
    planetMarsEnabledForLatitudeKey = \
        "ui/astrology/MarsEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mars.
    planetMarsEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Jupiter.
    planetJupiterEnabledForLatitudeKey = \
        "ui/astrology/JupiterEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Jupiter.
    planetJupiterEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Saturn.
    planetSaturnEnabledForLatitudeKey = \
        "ui/astrology/SaturnEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Saturn.
    planetSaturnEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Uranus.
    planetUranusEnabledForLatitudeKey = \
        "ui/astrology/UranusEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Uranus.
    planetUranusEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Neptune.
    planetNeptuneEnabledForLatitudeKey = \
        "ui/astrology/NeptuneEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Neptune.
    planetNeptuneEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Pluto.
    planetPlutoEnabledForLatitudeKey = \
        "ui/astrology/PlutoEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Pluto.
    planetPlutoEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for MeanNorthNode.
    planetMeanNorthNodeEnabledForLatitudeKey = \
        "ui/astrology/MeanNorthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanNorthNode.
    planetMeanNorthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanSouthNode.
    planetMeanSouthNodeEnabledForLatitudeKey = \
        "ui/astrology/MeanSouthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanSouthNode.
    planetMeanSouthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for TrueNorthNode.
    planetTrueNorthNodeEnabledForLatitudeKey = \
        "ui/astrology/TrueNorthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for TrueNorthNode.
    planetTrueNorthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for TrueSouthNode.
    planetTrueSouthNodeEnabledForLatitudeKey = \
        "ui/astrology/TrueSouthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for TrueSouthNode.
    planetTrueSouthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Ceres.
    planetCeresEnabledForLatitudeKey = \
        "ui/astrology/CeresEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Ceres.
    planetCeresEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Pallas.
    planetPallasEnabledForLatitudeKey = \
        "ui/astrology/PallasEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Pallas.
    planetPallasEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Juno.
    planetJunoEnabledForLatitudeKey = \
        "ui/astrology/JunoEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Juno.
    planetJunoEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Vesta.
    planetVestaEnabledForLatitudeKey = \
        "ui/astrology/VestaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Vesta.
    planetVestaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Isis.
    planetIsisEnabledForLatitudeKey = \
        "ui/astrology/IsisEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Isis.
    planetIsisEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Nibiru.
    planetNibiruEnabledForLatitudeKey = \
        "ui/astrology/NibiruEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Nibiru.
    planetNibiruEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Chiron.
    planetChironEnabledForLatitudeKey = \
        "ui/astrology/ChironEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Chiron.
    planetChironEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Gulika.
    planetGulikaEnabledForLatitudeKey = \
        "ui/astrology/GulikaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Gulika.
    planetGulikaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Mandi.
    planetMandiEnabledForLatitudeKey = \
        "ui/astrology/MandiEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mandi.
    planetMandiEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanOfFive.
    planetMeanOfFiveEnabledForLatitudeKey = \
        "ui/astrology/MeanOfFiveEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanOfFive.
    planetMeanOfFiveEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for CycleOfEight.
    planetCycleOfEightEnabledForLatitudeKey = \
        "ui/astrology/CycleOfEightEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for CycleOfEight.
    planetCycleOfEightEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForLatitudeKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForLatitudeKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgJuSa.
    planetAvgJuSaEnabledForLatitudeKey = \
        "ui/astrology/AvgJuSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgJuSa.
    planetAvgJuSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AsSu.
    planetAsSuEnabledForLatitudeKey = \
        "ui/astrology/AsSuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AsSu.
    planetAsSuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AsMo.
    planetAsMoEnabledForLatitudeKey = \
        "ui/astrology/AsMoEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AsMo.
    planetAsMoEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MoSu.
    planetMoSuEnabledForLatitudeKey = \
        "ui/astrology/MoSuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MoSu.
    planetMoSuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeVe.
    planetMeVeEnabledForLatitudeKey = \
        "ui/astrology/MeVeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeVe.
    planetMeVeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeEa.
    planetMeEaEnabledForLatitudeKey = \
        "ui/astrology/MeEaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeEa.
    planetMeEaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeMa.
    planetMeMaEnabledForLatitudeKey = \
        "ui/astrology/MeMaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeMa.
    planetMeMaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeJu.
    planetMeJuEnabledForLatitudeKey = \
        "ui/astrology/MeJuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeJu.
    planetMeJuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeSa.
    planetMeSaEnabledForLatitudeKey = \
        "ui/astrology/MeSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeSa.
    planetMeSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeUr.
    planetMeUrEnabledForLatitudeKey = \
        "ui/astrology/MeUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeUr.
    planetMeUrEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for VeEa.
    planetVeEaEnabledForLatitudeKey = \
        "ui/astrology/VeEaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for VeEa.
    planetVeEaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for VeMa.
    planetVeMaEnabledForLatitudeKey = \
        "ui/astrology/VeMaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for VeMa.
    planetVeMaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for VeJu.
    planetVeJuEnabledForLatitudeKey = \
        "ui/astrology/VeJuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for VeJu.
    planetVeJuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for VeSa.
    planetVeSaEnabledForLatitudeKey = \
        "ui/astrology/VeSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for VeSa.
    planetVeSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for VeUr.
    planetVeUrEnabledForLatitudeKey = \
        "ui/astrology/VeUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for VeUr.
    planetVeUrEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for EaMa.
    planetEaMaEnabledForLatitudeKey = \
        "ui/astrology/EaMaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for EaMa.
    planetEaMaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for EaJu.
    planetEaJuEnabledForLatitudeKey = \
        "ui/astrology/EaJuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for EaJu.
    planetEaJuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for EaSa.
    planetEaSaEnabledForLatitudeKey = \
        "ui/astrology/EaSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for EaSa.
    planetEaSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for EaUr.
    planetEaUrEnabledForLatitudeKey = \
        "ui/astrology/EaUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for EaUr.
    planetEaUrEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MaJu.
    planetMaJuEnabledForLatitudeKey = \
        "ui/astrology/MaJuEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MaJu.
    planetMaJuEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MaSa.
    planetMaSaEnabledForLatitudeKey = \
        "ui/astrology/MaSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MaSa.
    planetMaSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MaUr.
    planetMaUrEnabledForLatitudeKey = \
        "ui/astrology/MaUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MaUr.
    planetMaUrEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for JuSa.
    planetJuSaEnabledForLatitudeKey = \
        "ui/astrology/JuSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for JuSa.
    planetJuSaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for JuUr.
    planetJuUrEnabledForLatitudeKey = \
        "ui/astrology/JuUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for JuUr.
    planetJuUrEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for SaUr.
    planetSaUrEnabledForLatitudeKey = \
        "ui/astrology/SaUrEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for SaUr.
    planetSaUrEnabledForLatitudeDefValue = \
        False
    

    
    # QSettings key for the display flag in GeoSidRadixChart for H1.
    planetH1EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H1EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H1.
    planetH1EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H2.
    planetH2EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H2EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H2.
    planetH2EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H3.
    planetH3EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H3EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H3.
    planetH3EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H4.
    planetH4EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H4EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H4.
    planetH4EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H5.
    planetH5EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H5EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H5.
    planetH5EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H6.
    planetH6EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H6EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H6.
    planetH6EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H7.
    planetH7EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H7EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H7.
    planetH7EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H8.
    planetH8EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H8EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H8.
    planetH8EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H9.
    planetH9EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H9EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H9.
    planetH9EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H10.
    planetH10EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H10EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H10.
    planetH10EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H11.
    planetH11EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H11EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H11.
    planetH11EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H12.
    planetH12EnabledForGeoSidRadixChartKey = \
        "ui/astrology/H12EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H12.
    planetH12EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for ARMC.
    planetARMCEnabledForGeoSidRadixChartKey = \
        "ui/astrology/ARMCEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for ARMC.
    planetARMCEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Vertex.
    planetVertexEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VertexEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Vertex.
    planetVertexEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EquatorialAscendantEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForGeoSidRadixChartKey = \
        "ui/astrology/CoAscendant1EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForGeoSidRadixChartKey = \
        "ui/astrology/CoAscendant2EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForGeoSidRadixChartKey = \
        "ui/astrology/PolarAscendantEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/HoraLagnaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/GhatiLagnaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeanLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Sun.
    planetSunEnabledForGeoSidRadixChartKey = \
        "ui/astrology/SunEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Sun.
    planetSunEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Moon.
    planetMoonEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MoonEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Moon.
    planetMoonEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Mercury.
    planetMercuryEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MercuryEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mercury.
    planetMercuryEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Venus.
    planetVenusEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VenusEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Venus.
    planetVenusEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Earth.
    planetEarthEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EarthEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Earth.
    planetEarthEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for Mars.
    planetMarsEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MarsEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mars.
    planetMarsEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Jupiter.
    planetJupiterEnabledForGeoSidRadixChartKey = \
        "ui/astrology/JupiterEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Jupiter.
    planetJupiterEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Saturn.
    planetSaturnEnabledForGeoSidRadixChartKey = \
        "ui/astrology/SaturnEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Saturn.
    planetSaturnEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Uranus.
    planetUranusEnabledForGeoSidRadixChartKey = \
        "ui/astrology/UranusEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Uranus.
    planetUranusEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Neptune.
    planetNeptuneEnabledForGeoSidRadixChartKey = \
        "ui/astrology/NeptuneEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Neptune.
    planetNeptuneEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Pluto.
    planetPlutoEnabledForGeoSidRadixChartKey = \
        "ui/astrology/PlutoEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Pluto.
    planetPlutoEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeanNorthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeanSouthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/TrueNorthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/TrueSouthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Ceres.
    planetCeresEnabledForGeoSidRadixChartKey = \
        "ui/astrology/CeresEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Ceres.
    planetCeresEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Pallas.
    planetPallasEnabledForGeoSidRadixChartKey = \
        "ui/astrology/PallasEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Pallas.
    planetPallasEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Juno.
    planetJunoEnabledForGeoSidRadixChartKey = \
        "ui/astrology/JunoEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Juno.
    planetJunoEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Vesta.
    planetVestaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VestaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Vesta.
    planetVestaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Isis.
    planetIsisEnabledForGeoSidRadixChartKey = \
        "ui/astrology/IsisEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Isis.
    planetIsisEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Nibiru.
    planetNibiruEnabledForGeoSidRadixChartKey = \
        "ui/astrology/NibiruEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Nibiru.
    planetNibiruEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Chiron.
    planetChironEnabledForGeoSidRadixChartKey = \
        "ui/astrology/ChironEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Chiron.
    planetChironEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Gulika.
    planetGulikaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/GulikaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Gulika.
    planetGulikaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Mandi.
    planetMandiEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MandiEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mandi.
    planetMandiEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeanOfFiveEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoSidRadixChartKey = \
        "ui/astrology/CycleOfEightEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/AvgJuSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AsSu.
    planetAsSuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/AsSuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AsSu.
    planetAsSuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for AsMo.
    planetAsMoEnabledForGeoSidRadixChartKey = \
        "ui/astrology/AsMoEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AsMo.
    planetAsMoEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MoSu.
    planetMoSuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MoSuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MoSu.
    planetMoSuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeVe.
    planetMeVeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeVeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeVe.
    planetMeVeEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeEa.
    planetMeEaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeEaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeEa.
    planetMeEaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeMa.
    planetMeMaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeMaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeMa.
    planetMeMaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeJu.
    planetMeJuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeJuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeJu.
    planetMeJuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeSa.
    planetMeSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeSa.
    planetMeSaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MeUr.
    planetMeUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MeUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeUr.
    planetMeUrEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for VeEa.
    planetVeEaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VeEaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for VeEa.
    planetVeEaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for VeMa.
    planetVeMaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VeMaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for VeMa.
    planetVeMaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for VeJu.
    planetVeJuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VeJuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for VeJu.
    planetVeJuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for VeSa.
    planetVeSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VeSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for VeSa.
    planetVeSaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for VeUr.
    planetVeUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/VeUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for VeUr.
    planetVeUrEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for EaMa.
    planetEaMaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EaMaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for EaMa.
    planetEaMaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for EaJu.
    planetEaJuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EaJuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for EaJu.
    planetEaJuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for EaSa.
    planetEaSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EaSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for EaSa.
    planetEaSaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for EaUr.
    planetEaUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/EaUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for EaUr.
    planetEaUrEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MaJu.
    planetMaJuEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MaJuEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MaJu.
    planetMaJuEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MaSa.
    planetMaSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MaSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MaSa.
    planetMaSaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for MaUr.
    planetMaUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/MaUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MaUr.
    planetMaUrEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for JuSa.
    planetJuSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/JuSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for JuSa.
    planetJuSaEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for JuUr.
    planetJuUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/JuUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for JuUr.
    planetJuUrEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for SaUr.
    planetSaUrEnabledForGeoSidRadixChartKey = \
        "ui/astrology/SaUrEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for SaUr.
    planetSaUrEnabledForGeoSidRadixChartDefValue = \
        False
    

    
    # QSettings key for the display flag in GeoTropRadixChart for H1.
    planetH1EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H1EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H1.
    planetH1EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H2.
    planetH2EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H2EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H2.
    planetH2EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H3.
    planetH3EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H3EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H3.
    planetH3EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H4.
    planetH4EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H4EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H4.
    planetH4EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H5.
    planetH5EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H5EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H5.
    planetH5EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H6.
    planetH6EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H6EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H6.
    planetH6EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H7.
    planetH7EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H7EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H7.
    planetH7EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H8.
    planetH8EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H8EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H8.
    planetH8EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H9.
    planetH9EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H9EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H9.
    planetH9EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H10.
    planetH10EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H10EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H10.
    planetH10EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H11.
    planetH11EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H11EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H11.
    planetH11EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H12.
    planetH12EnabledForGeoTropRadixChartKey = \
        "ui/astrology/H12EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H12.
    planetH12EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for ARMC.
    planetARMCEnabledForGeoTropRadixChartKey = \
        "ui/astrology/ARMCEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for ARMC.
    planetARMCEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Vertex.
    planetVertexEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VertexEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Vertex.
    planetVertexEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EquatorialAscendantEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForGeoTropRadixChartKey = \
        "ui/astrology/CoAscendant1EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForGeoTropRadixChartKey = \
        "ui/astrology/CoAscendant2EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForGeoTropRadixChartKey = \
        "ui/astrology/PolarAscendantEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/HoraLagnaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/GhatiLagnaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeanLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Sun.
    planetSunEnabledForGeoTropRadixChartKey = \
        "ui/astrology/SunEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Sun.
    planetSunEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Moon.
    planetMoonEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MoonEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Moon.
    planetMoonEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Mercury.
    planetMercuryEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MercuryEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mercury.
    planetMercuryEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Venus.
    planetVenusEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VenusEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Venus.
    planetVenusEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Earth.
    planetEarthEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EarthEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Earth.
    planetEarthEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for Mars.
    planetMarsEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MarsEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mars.
    planetMarsEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Jupiter.
    planetJupiterEnabledForGeoTropRadixChartKey = \
        "ui/astrology/JupiterEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Jupiter.
    planetJupiterEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Saturn.
    planetSaturnEnabledForGeoTropRadixChartKey = \
        "ui/astrology/SaturnEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Saturn.
    planetSaturnEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Uranus.
    planetUranusEnabledForGeoTropRadixChartKey = \
        "ui/astrology/UranusEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Uranus.
    planetUranusEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Neptune.
    planetNeptuneEnabledForGeoTropRadixChartKey = \
        "ui/astrology/NeptuneEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Neptune.
    planetNeptuneEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Pluto.
    planetPlutoEnabledForGeoTropRadixChartKey = \
        "ui/astrology/PlutoEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Pluto.
    planetPlutoEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeanNorthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeanSouthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/TrueNorthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/TrueSouthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Ceres.
    planetCeresEnabledForGeoTropRadixChartKey = \
        "ui/astrology/CeresEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Ceres.
    planetCeresEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Pallas.
    planetPallasEnabledForGeoTropRadixChartKey = \
        "ui/astrology/PallasEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Pallas.
    planetPallasEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Juno.
    planetJunoEnabledForGeoTropRadixChartKey = \
        "ui/astrology/JunoEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Juno.
    planetJunoEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Vesta.
    planetVestaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VestaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Vesta.
    planetVestaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Isis.
    planetIsisEnabledForGeoTropRadixChartKey = \
        "ui/astrology/IsisEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Isis.
    planetIsisEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Nibiru.
    planetNibiruEnabledForGeoTropRadixChartKey = \
        "ui/astrology/NibiruEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Nibiru.
    planetNibiruEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Chiron.
    planetChironEnabledForGeoTropRadixChartKey = \
        "ui/astrology/ChironEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Chiron.
    planetChironEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Gulika.
    planetGulikaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/GulikaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Gulika.
    planetGulikaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Mandi.
    planetMandiEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MandiEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mandi.
    planetMandiEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeanOfFiveEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoTropRadixChartKey = \
        "ui/astrology/CycleOfEightEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/AvgJuSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AsSu.
    planetAsSuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/AsSuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AsSu.
    planetAsSuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for AsMo.
    planetAsMoEnabledForGeoTropRadixChartKey = \
        "ui/astrology/AsMoEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AsMo.
    planetAsMoEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MoSu.
    planetMoSuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MoSuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MoSu.
    planetMoSuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeVe.
    planetMeVeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeVeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeVe.
    planetMeVeEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeEa.
    planetMeEaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeEaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeEa.
    planetMeEaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeMa.
    planetMeMaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeMaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeMa.
    planetMeMaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeJu.
    planetMeJuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeJuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeJu.
    planetMeJuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeSa.
    planetMeSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeSa.
    planetMeSaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MeUr.
    planetMeUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MeUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeUr.
    planetMeUrEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for VeEa.
    planetVeEaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VeEaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for VeEa.
    planetVeEaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for VeMa.
    planetVeMaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VeMaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for VeMa.
    planetVeMaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for VeJu.
    planetVeJuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VeJuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for VeJu.
    planetVeJuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for VeSa.
    planetVeSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VeSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for VeSa.
    planetVeSaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for VeUr.
    planetVeUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/VeUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for VeUr.
    planetVeUrEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for EaMa.
    planetEaMaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EaMaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for EaMa.
    planetEaMaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for EaJu.
    planetEaJuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EaJuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for EaJu.
    planetEaJuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for EaSa.
    planetEaSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EaSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for EaSa.
    planetEaSaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for EaUr.
    planetEaUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/EaUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for EaUr.
    planetEaUrEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MaJu.
    planetMaJuEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MaJuEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MaJu.
    planetMaJuEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MaSa.
    planetMaSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MaSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MaSa.
    planetMaSaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for MaUr.
    planetMaUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/MaUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MaUr.
    planetMaUrEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for JuSa.
    planetJuSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/JuSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for JuSa.
    planetJuSaEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for JuUr.
    planetJuUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/JuUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for JuUr.
    planetJuUrEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for SaUr.
    planetSaUrEnabledForGeoTropRadixChartKey = \
        "ui/astrology/SaUrEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for SaUr.
    planetSaUrEnabledForGeoTropRadixChartDefValue = \
        False
    

    
    # QSettings key for the display flag in HelioTropRadixChart for H1.
    planetH1EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H1EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H1.
    planetH1EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H2.
    planetH2EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H2EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H2.
    planetH2EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H3.
    planetH3EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H3EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H3.
    planetH3EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H4.
    planetH4EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H4EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H4.
    planetH4EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H5.
    planetH5EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H5EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H5.
    planetH5EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H6.
    planetH6EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H6EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H6.
    planetH6EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H7.
    planetH7EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H7EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H7.
    planetH7EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H8.
    planetH8EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H8EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H8.
    planetH8EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H9.
    planetH9EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H9EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H9.
    planetH9EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H10.
    planetH10EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H10EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H10.
    planetH10EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H11.
    planetH11EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H11EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H11.
    planetH11EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for H12.
    planetH12EnabledForHelioTropRadixChartKey = \
        "ui/astrology/H12EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for H12.
    planetH12EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for ARMC.
    planetARMCEnabledForHelioTropRadixChartKey = \
        "ui/astrology/ARMCEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for ARMC.
    planetARMCEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Vertex.
    planetVertexEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VertexEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Vertex.
    planetVertexEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EquatorialAscendantEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for EquatorialAscendant.
    planetEquatorialAscendantEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForHelioTropRadixChartKey = \
        "ui/astrology/CoAscendant1EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for CoAscendant1.
    planetCoAscendant1EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForHelioTropRadixChartKey = \
        "ui/astrology/CoAscendant2EnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for CoAscendant2.
    planetCoAscendant2EnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForHelioTropRadixChartKey = \
        "ui/astrology/PolarAscendantEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for PolarAscendant.
    planetPolarAscendantEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/HoraLagnaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/GhatiLagnaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeanLunarApogeeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/OsculatingLunarApogeeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/InterpolatedLunarApogeeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/InterpolatedLunarPerigeeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Sun.
    planetSunEnabledForHelioTropRadixChartKey = \
        "ui/astrology/SunEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Sun.
    planetSunEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Moon.
    planetMoonEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MoonEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Moon.
    planetMoonEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Mercury.
    planetMercuryEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MercuryEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Mercury.
    planetMercuryEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Venus.
    planetVenusEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VenusEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Venus.
    planetVenusEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Earth.
    planetEarthEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EarthEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Earth.
    planetEarthEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Mars.
    planetMarsEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MarsEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Mars.
    planetMarsEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Jupiter.
    planetJupiterEnabledForHelioTropRadixChartKey = \
        "ui/astrology/JupiterEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Jupiter.
    planetJupiterEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Saturn.
    planetSaturnEnabledForHelioTropRadixChartKey = \
        "ui/astrology/SaturnEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Saturn.
    planetSaturnEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Uranus.
    planetUranusEnabledForHelioTropRadixChartKey = \
        "ui/astrology/UranusEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Uranus.
    planetUranusEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Neptune.
    planetNeptuneEnabledForHelioTropRadixChartKey = \
        "ui/astrology/NeptuneEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Neptune.
    planetNeptuneEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for Pluto.
    planetPlutoEnabledForHelioTropRadixChartKey = \
        "ui/astrology/PlutoEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Pluto.
    planetPlutoEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeanNorthNodeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeanSouthNodeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/TrueNorthNodeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/TrueSouthNodeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Ceres.
    planetCeresEnabledForHelioTropRadixChartKey = \
        "ui/astrology/CeresEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Ceres.
    planetCeresEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Pallas.
    planetPallasEnabledForHelioTropRadixChartKey = \
        "ui/astrology/PallasEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Pallas.
    planetPallasEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Juno.
    planetJunoEnabledForHelioTropRadixChartKey = \
        "ui/astrology/JunoEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Juno.
    planetJunoEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Vesta.
    planetVestaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VestaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Vesta.
    planetVestaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Isis.
    planetIsisEnabledForHelioTropRadixChartKey = \
        "ui/astrology/IsisEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Isis.
    planetIsisEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Nibiru.
    planetNibiruEnabledForHelioTropRadixChartKey = \
        "ui/astrology/NibiruEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Nibiru.
    planetNibiruEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Chiron.
    planetChironEnabledForHelioTropRadixChartKey = \
        "ui/astrology/ChironEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Chiron.
    planetChironEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Gulika.
    planetGulikaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/GulikaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Gulika.
    planetGulikaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for Mandi.
    planetMandiEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MandiEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for Mandi.
    planetMandiEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeanOfFiveEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForHelioTropRadixChartKey = \
        "ui/astrology/CycleOfEightEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForHelioTropRadixChartKey = \
        "ui/astrology/AvgMaJuSaUrNePlEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/AvgJuSaUrNeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/AvgJuSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForHelioTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioTropRadixChart for AsSu.
    planetAsSuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/AsSuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for AsSu.
    planetAsSuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for AsMo.
    planetAsMoEnabledForHelioTropRadixChartKey = \
        "ui/astrology/AsMoEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for AsMo.
    planetAsMoEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MoSu.
    planetMoSuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MoSuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MoSu.
    planetMoSuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeVe.
    planetMeVeEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeVeEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeVe.
    planetMeVeEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeEa.
    planetMeEaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeEaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeEa.
    planetMeEaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeMa.
    planetMeMaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeMaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeMa.
    planetMeMaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeJu.
    planetMeJuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeJuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeJu.
    planetMeJuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeSa.
    planetMeSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeSa.
    planetMeSaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MeUr.
    planetMeUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MeUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MeUr.
    planetMeUrEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for VeEa.
    planetVeEaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VeEaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for VeEa.
    planetVeEaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for VeMa.
    planetVeMaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VeMaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for VeMa.
    planetVeMaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for VeJu.
    planetVeJuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VeJuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for VeJu.
    planetVeJuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for VeSa.
    planetVeSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VeSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for VeSa.
    planetVeSaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for VeUr.
    planetVeUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/VeUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for VeUr.
    planetVeUrEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for EaMa.
    planetEaMaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EaMaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for EaMa.
    planetEaMaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for EaJu.
    planetEaJuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EaJuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for EaJu.
    planetEaJuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for EaSa.
    planetEaSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EaSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for EaSa.
    planetEaSaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for EaUr.
    planetEaUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/EaUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for EaUr.
    planetEaUrEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MaJu.
    planetMaJuEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MaJuEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MaJu.
    planetMaJuEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MaSa.
    planetMaSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MaSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MaSa.
    planetMaSaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for MaUr.
    planetMaUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/MaUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for MaUr.
    planetMaUrEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for JuSa.
    planetJuSaEnabledForHelioTropRadixChartKey = \
        "ui/astrology/JuSaEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for JuSa.
    planetJuSaEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for JuUr.
    planetJuUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/JuUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for JuUr.
    planetJuUrEnabledForHelioTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioTropRadixChart for SaUr.
    planetSaUrEnabledForHelioTropRadixChartKey = \
        "ui/astrology/SaUrEnabledForHelioTropRadixChart"
    
    # QSettings default value for the display flag in HelioTropRadixChart for SaUr.
    planetSaUrEnabledForHelioTropRadixChartDefValue = \
        False
    

    
##############################################################################
