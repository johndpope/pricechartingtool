


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor


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
        "ui/astrology/h1GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H1.
    planetH1GlyphUnicodeDefValue = "As"

    # QSettings key for the planet glyph font size of the H1.
    planetH1GlyphFontSizeKey = \
        "ui/astrology/h1GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H1.
    planetH1GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H1.
    planetH1AbbreviationKey = \
        "ui/astrology/h1Abbreviation"

    # QSettings default value for the planet abbreviation of the H1.
    planetH1AbbreviationDefValue = "As"

    # QSettings key for the foreground color of the H1.
    planetH1ForegroundColorKey = \
        "ui/astrology/h1ForegroundColor"

    # QSettings default value for the foreground color of the H1.
    planetH1ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H1.
    planetH1BackgroundColorKey = \
        "ui/astrology/h1BackgroundColor"

    # QSettings default value for the background color of the H1.
    planetH1BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeKey = \
        "ui/astrology/h2GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeDefValue = "H2"

    # QSettings key for the planet glyph font size of the H2.
    planetH2GlyphFontSizeKey = \
        "ui/astrology/h2GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H2.
    planetH2GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H2.
    planetH2AbbreviationKey = \
        "ui/astrology/h2Abbreviation"

    # QSettings default value for the planet abbreviation of the H2.
    planetH2AbbreviationDefValue = "H2"

    # QSettings key for the foreground color of the H2.
    planetH2ForegroundColorKey = \
        "ui/astrology/h2ForegroundColor"

    # QSettings default value for the foreground color of the H2.
    planetH2ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H2.
    planetH2BackgroundColorKey = \
        "ui/astrology/h2BackgroundColor"

    # QSettings default value for the background color of the H2.
    planetH2BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeKey = \
        "ui/astrology/h3GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeDefValue = "H3"

    # QSettings key for the planet glyph font size of the H3.
    planetH3GlyphFontSizeKey = \
        "ui/astrology/h3GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H3.
    planetH3GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H3.
    planetH3AbbreviationKey = \
        "ui/astrology/h3Abbreviation"

    # QSettings default value for the planet abbreviation of the H3.
    planetH3AbbreviationDefValue = "H3"

    # QSettings key for the foreground color of the H3.
    planetH3ForegroundColorKey = \
        "ui/astrology/h3ForegroundColor"

    # QSettings default value for the foreground color of the H3.
    planetH3ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H3.
    planetH3BackgroundColorKey = \
        "ui/astrology/h3BackgroundColor"

    # QSettings default value for the background color of the H3.
    planetH3BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeKey = \
        "ui/astrology/h4GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeDefValue = "H4"

    # QSettings key for the planet glyph font size of the H4.
    planetH4GlyphFontSizeKey = \
        "ui/astrology/h4GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H4.
    planetH4GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H4.
    planetH4AbbreviationKey = \
        "ui/astrology/h4Abbreviation"

    # QSettings default value for the planet abbreviation of the H4.
    planetH4AbbreviationDefValue = "H4"

    # QSettings key for the foreground color of the H4.
    planetH4ForegroundColorKey = \
        "ui/astrology/h4ForegroundColor"

    # QSettings default value for the foreground color of the H4.
    planetH4ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H4.
    planetH4BackgroundColorKey = \
        "ui/astrology/h4BackgroundColor"

    # QSettings default value for the background color of the H4.
    planetH4BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeKey = \
        "ui/astrology/h5GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeDefValue = "H5"

    # QSettings key for the planet glyph font size of the H5.
    planetH5GlyphFontSizeKey = \
        "ui/astrology/h5GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H5.
    planetH5GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H5.
    planetH5AbbreviationKey = \
        "ui/astrology/h5Abbreviation"

    # QSettings default value for the planet abbreviation of the H5.
    planetH5AbbreviationDefValue = "H5"

    # QSettings key for the foreground color of the H5.
    planetH5ForegroundColorKey = \
        "ui/astrology/h5ForegroundColor"

    # QSettings default value for the foreground color of the H5.
    planetH5ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H5.
    planetH5BackgroundColorKey = \
        "ui/astrology/h5BackgroundColor"

    # QSettings default value for the background color of the H5.
    planetH5BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeKey = \
        "ui/astrology/h6GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeDefValue = "H6"

    # QSettings key for the planet glyph font size of the H6.
    planetH6GlyphFontSizeKey = \
        "ui/astrology/h6GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H6.
    planetH6GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H6.
    planetH6AbbreviationKey = \
        "ui/astrology/h6Abbreviation"

    # QSettings default value for the planet abbreviation of the H6.
    planetH6AbbreviationDefValue = "H6"

    # QSettings key for the foreground color of the H6.
    planetH6ForegroundColorKey = \
        "ui/astrology/h6ForegroundColor"

    # QSettings default value for the foreground color of the H6.
    planetH6ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H6.
    planetH6BackgroundColorKey = \
        "ui/astrology/h6BackgroundColor"

    # QSettings default value for the background color of the H6.
    planetH6BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeKey = \
        "ui/astrology/h7GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeDefValue = "H7"

    # QSettings key for the planet glyph font size of the H7.
    planetH7GlyphFontSizeKey = \
        "ui/astrology/h7GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H7.
    planetH7GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H7.
    planetH7AbbreviationKey = \
        "ui/astrology/h7Abbreviation"

    # QSettings default value for the planet abbreviation of the H7.
    planetH7AbbreviationDefValue = "H7"

    # QSettings key for the foreground color of the H7.
    planetH7ForegroundColorKey = \
        "ui/astrology/h7ForegroundColor"

    # QSettings default value for the foreground color of the H7.
    planetH7ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H7.
    planetH7BackgroundColorKey = \
        "ui/astrology/h7BackgroundColor"

    # QSettings default value for the background color of the H7.
    planetH7BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeKey = \
        "ui/astrology/h8GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeDefValue = "H8"

    # QSettings key for the planet glyph font size of the H8.
    planetH8GlyphFontSizeKey = \
        "ui/astrology/h8GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H8.
    planetH8GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H8.
    planetH8AbbreviationKey = \
        "ui/astrology/h8Abbreviation"

    # QSettings default value for the planet abbreviation of the H8.
    planetH8AbbreviationDefValue = "H8"

    # QSettings key for the foreground color of the H8.
    planetH8ForegroundColorKey = \
        "ui/astrology/h8ForegroundColor"

    # QSettings default value for the foreground color of the H8.
    planetH8ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H8.
    planetH8BackgroundColorKey = \
        "ui/astrology/h8BackgroundColor"

    # QSettings default value for the background color of the H8.
    planetH8BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeKey = \
        "ui/astrology/h9GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeDefValue = "H9"

    # QSettings key for the planet glyph font size of the H9.
    planetH9GlyphFontSizeKey = \
        "ui/astrology/h9GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H9.
    planetH9GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H9.
    planetH9AbbreviationKey = \
        "ui/astrology/h9Abbreviation"

    # QSettings default value for the planet abbreviation of the H9.
    planetH9AbbreviationDefValue = "H9"

    # QSettings key for the foreground color of the H9.
    planetH9ForegroundColorKey = \
        "ui/astrology/h9ForegroundColor"

    # QSettings default value for the foreground color of the H9.
    planetH9ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H9.
    planetH9BackgroundColorKey = \
        "ui/astrology/h9BackgroundColor"

    # QSettings default value for the background color of the H9.
    planetH9BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeKey = \
        "ui/astrology/h10GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeDefValue = "H10"

    # QSettings key for the planet glyph font size of the H10.
    planetH10GlyphFontSizeKey = \
        "ui/astrology/h10GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H10.
    planetH10GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H10.
    planetH10AbbreviationKey = \
        "ui/astrology/h10Abbreviation"

    # QSettings default value for the planet abbreviation of the H10.
    planetH10AbbreviationDefValue = "H10"

    # QSettings key for the foreground color of the H10.
    planetH10ForegroundColorKey = \
        "ui/astrology/h10ForegroundColor"

    # QSettings default value for the foreground color of the H10.
    planetH10ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H10.
    planetH10BackgroundColorKey = \
        "ui/astrology/h10BackgroundColor"

    # QSettings default value for the background color of the H10.
    planetH10BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeKey = \
        "ui/astrology/h11GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeDefValue = "H11"

    # QSettings key for the planet glyph font size of the H11.
    planetH11GlyphFontSizeKey = \
        "ui/astrology/h11GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H11.
    planetH11GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H11.
    planetH11AbbreviationKey = \
        "ui/astrology/h11Abbreviation"

    # QSettings default value for the planet abbreviation of the H11.
    planetH11AbbreviationDefValue = "H11"

    # QSettings key for the foreground color of the H11.
    planetH11ForegroundColorKey = \
        "ui/astrology/h11ForegroundColor"

    # QSettings default value for the foreground color of the H11.
    planetH11ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H11.
    planetH11BackgroundColorKey = \
        "ui/astrology/h11BackgroundColor"

    # QSettings default value for the background color of the H11.
    planetH11BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeKey = \
        "ui/astrology/h12GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeDefValue = "H12"

    # QSettings key for the planet glyph font size of the H12.
    planetH12GlyphFontSizeKey = \
        "ui/astrology/h12GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H12.
    planetH12GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H12.
    planetH12AbbreviationKey = \
        "ui/astrology/h12Abbreviation"

    # QSettings default value for the planet abbreviation of the H12.
    planetH12AbbreviationDefValue = "H12"

    # QSettings key for the foreground color of the H12.
    planetH12ForegroundColorKey = \
        "ui/astrology/h12ForegroundColor"

    # QSettings default value for the foreground color of the H12.
    planetH12ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H12.
    planetH12BackgroundColorKey = \
        "ui/astrology/h12BackgroundColor"

    # QSettings default value for the background color of the H12.
    planetH12BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeKey = \
        "ui/astrology/horaLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeDefValue = "HL"

    # QSettings key for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeKey = \
        "ui/astrology/horaLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationKey = \
        "ui/astrology/horaLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationDefValue = "HL"

    # QSettings key for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorKey = \
        "ui/astrology/horaLagnaForegroundColor"

    # QSettings default value for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorKey = \
        "ui/astrology/horaLagnaBackgroundColor"

    # QSettings default value for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeKey = \
        "ui/astrology/ghatiLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeDefValue = "GL"

    # QSettings key for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeKey = \
        "ui/astrology/ghatiLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationKey = \
        "ui/astrology/ghatiLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationDefValue = "GL"

    # QSettings key for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorKey = \
        "ui/astrology/ghatiLagnaForegroundColor"

    # QSettings default value for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorKey = \
        "ui/astrology/ghatiLagnaBackgroundColor"

    # QSettings default value for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/meanLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeDefValue = "MLA"

    # QSettings key for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/meanLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationKey = \
        "ui/astrology/meanLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationDefValue = "MLA"

    # QSettings key for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorKey = \
        "ui/astrology/meanLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorKey = \
        "ui/astrology/meanLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeDefValue = "OLA"

    # QSettings key for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationKey = \
        "ui/astrology/osculatingLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationDefValue = "OLA"

    # QSettings key for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorKey = \
        "ui/astrology/osculatingLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorKey = \
        "ui/astrology/osculatingLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeDefValue = "ILA"

    # QSettings key for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationDefValue = "ILA"

    # QSettings key for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeDefValue = "ILP"

    # QSettings key for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarPerigeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationDefValue = "ILP"

    # QSettings key for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeKey = \
        "ui/astrology/sunGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeDefValue = "\u2609"

    # QSettings key for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeKey = \
        "ui/astrology/sunGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Sun.
    planetSunAbbreviationKey = \
        "ui/astrology/sunAbbreviation"

    # QSettings default value for the planet abbreviation of the Sun.
    planetSunAbbreviationDefValue = "Su"

    # QSettings key for the foreground color of the Sun.
    planetSunForegroundColorKey = \
        "ui/astrology/sunForegroundColor"

    # QSettings default value for the foreground color of the Sun.
    planetSunForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sun.
    planetSunBackgroundColorKey = \
        "ui/astrology/sunBackgroundColor"

    # QSettings default value for the background color of the Sun.
    planetSunBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeKey = \
        "ui/astrology/moonGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeDefValue = "\u263d"

    # QSettings key for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeKey = \
        "ui/astrology/moonGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Moon.
    planetMoonAbbreviationKey = \
        "ui/astrology/moonAbbreviation"

    # QSettings default value for the planet abbreviation of the Moon.
    planetMoonAbbreviationDefValue = "Mo"

    # QSettings key for the foreground color of the Moon.
    planetMoonForegroundColorKey = \
        "ui/astrology/moonForegroundColor"

    # QSettings default value for the foreground color of the Moon.
    planetMoonForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Moon.
    planetMoonBackgroundColorKey = \
        "ui/astrology/moonBackgroundColor"

    # QSettings default value for the background color of the Moon.
    planetMoonBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeKey = \
        "ui/astrology/mercuryGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeDefValue = "\u263f"

    # QSettings key for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeKey = \
        "ui/astrology/mercuryGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationKey = \
        "ui/astrology/mercuryAbbreviation"

    # QSettings default value for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationDefValue = "Me"

    # QSettings key for the foreground color of the Mercury.
    planetMercuryForegroundColorKey = \
        "ui/astrology/mercuryForegroundColor"

    # QSettings default value for the foreground color of the Mercury.
    planetMercuryForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mercury.
    planetMercuryBackgroundColorKey = \
        "ui/astrology/mercuryBackgroundColor"

    # QSettings default value for the background color of the Mercury.
    planetMercuryBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeKey = \
        "ui/astrology/venusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeDefValue = "\u2640"

    # QSettings key for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeKey = \
        "ui/astrology/venusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Venus.
    planetVenusAbbreviationKey = \
        "ui/astrology/venusAbbreviation"

    # QSettings default value for the planet abbreviation of the Venus.
    planetVenusAbbreviationDefValue = "Ve"

    # QSettings key for the foreground color of the Venus.
    planetVenusForegroundColorKey = \
        "ui/astrology/venusForegroundColor"

    # QSettings default value for the foreground color of the Venus.
    planetVenusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Venus.
    planetVenusBackgroundColorKey = \
        "ui/astrology/venusBackgroundColor"

    # QSettings default value for the background color of the Venus.
    planetVenusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeKey = \
        "ui/astrology/earthGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeDefValue = "\u2d32"

    # QSettings key for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeKey = \
        "ui/astrology/earthGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Earth.
    planetEarthAbbreviationKey = \
        "ui/astrology/earthAbbreviation"

    # QSettings default value for the planet abbreviation of the Earth.
    planetEarthAbbreviationDefValue = "Ea"

    # QSettings key for the foreground color of the Earth.
    planetEarthForegroundColorKey = \
        "ui/astrology/earthForegroundColor"

    # QSettings default value for the foreground color of the Earth.
    planetEarthForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Earth.
    planetEarthBackgroundColorKey = \
        "ui/astrology/earthBackgroundColor"

    # QSettings default value for the background color of the Earth.
    planetEarthBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeKey = \
        "ui/astrology/marsGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeDefValue = "\u2642"

    # QSettings key for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeKey = \
        "ui/astrology/marsGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mars.
    planetMarsAbbreviationKey = \
        "ui/astrology/marsAbbreviation"

    # QSettings default value for the planet abbreviation of the Mars.
    planetMarsAbbreviationDefValue = "Ma"

    # QSettings key for the foreground color of the Mars.
    planetMarsForegroundColorKey = \
        "ui/astrology/marsForegroundColor"

    # QSettings default value for the foreground color of the Mars.
    planetMarsForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mars.
    planetMarsBackgroundColorKey = \
        "ui/astrology/marsBackgroundColor"

    # QSettings default value for the background color of the Mars.
    planetMarsBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeKey = \
        "ui/astrology/jupiterGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeDefValue = "\u2643"

    # QSettings key for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeKey = \
        "ui/astrology/jupiterGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationKey = \
        "ui/astrology/jupiterAbbreviation"

    # QSettings default value for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationDefValue = "Ju"

    # QSettings key for the foreground color of the Jupiter.
    planetJupiterForegroundColorKey = \
        "ui/astrology/jupiterForegroundColor"

    # QSettings default value for the foreground color of the Jupiter.
    planetJupiterForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Jupiter.
    planetJupiterBackgroundColorKey = \
        "ui/astrology/jupiterBackgroundColor"

    # QSettings default value for the background color of the Jupiter.
    planetJupiterBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeKey = \
        "ui/astrology/saturnGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeDefValue = "\u2644"

    # QSettings key for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeKey = \
        "ui/astrology/saturnGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationKey = \
        "ui/astrology/saturnAbbreviation"

    # QSettings default value for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Saturn.
    planetSaturnForegroundColorKey = \
        "ui/astrology/saturnForegroundColor"

    # QSettings default value for the foreground color of the Saturn.
    planetSaturnForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Saturn.
    planetSaturnBackgroundColorKey = \
        "ui/astrology/saturnBackgroundColor"

    # QSettings default value for the background color of the Saturn.
    planetSaturnBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeKey = \
        "ui/astrology/uranusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeDefValue = "\u2645"

    # QSettings key for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeKey = \
        "ui/astrology/uranusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Uranus.
    planetUranusAbbreviationKey = \
        "ui/astrology/uranusAbbreviation"

    # QSettings default value for the planet abbreviation of the Uranus.
    planetUranusAbbreviationDefValue = "Ur"

    # QSettings key for the foreground color of the Uranus.
    planetUranusForegroundColorKey = \
        "ui/astrology/uranusForegroundColor"

    # QSettings default value for the foreground color of the Uranus.
    planetUranusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Uranus.
    planetUranusBackgroundColorKey = \
        "ui/astrology/uranusBackgroundColor"

    # QSettings default value for the background color of the Uranus.
    planetUranusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeKey = \
        "ui/astrology/neptuneGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeDefValue = "\u2646"

    # QSettings key for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeKey = \
        "ui/astrology/neptuneGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationKey = \
        "ui/astrology/neptuneAbbreviation"

    # QSettings default value for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationDefValue = "Ne"

    # QSettings key for the foreground color of the Neptune.
    planetNeptuneForegroundColorKey = \
        "ui/astrology/neptuneForegroundColor"

    # QSettings default value for the foreground color of the Neptune.
    planetNeptuneForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Neptune.
    planetNeptuneBackgroundColorKey = \
        "ui/astrology/neptuneBackgroundColor"

    # QSettings default value for the background color of the Neptune.
    planetNeptuneBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeKey = \
        "ui/astrology/plutoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeDefValue = "\u2647"

    # QSettings key for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeKey = \
        "ui/astrology/plutoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationKey = \
        "ui/astrology/plutoAbbreviation"

    # QSettings default value for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationDefValue = "Pl"

    # QSettings key for the foreground color of the Pluto.
    planetPlutoForegroundColorKey = \
        "ui/astrology/plutoForegroundColor"

    # QSettings default value for the foreground color of the Pluto.
    planetPlutoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pluto.
    planetPlutoBackgroundColorKey = \
        "ui/astrology/plutoBackgroundColor"

    # QSettings default value for the background color of the Pluto.
    planetPlutoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeKey = \
        "ui/astrology/meanNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeKey = \
        "ui/astrology/meanNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationKey = \
        "ui/astrology/meanNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationDefValue = "Ra"

    # QSettings key for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorKey = \
        "ui/astrology/meanNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorKey = \
        "ui/astrology/meanNorthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeKey = \
        "ui/astrology/meanSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeKey = \
        "ui/astrology/meanSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationKey = \
        "ui/astrology/meanSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationDefValue = "Ke"

    # QSettings key for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorKey = \
        "ui/astrology/meanSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorKey = \
        "ui/astrology/meanSouthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeKey = \
        "ui/astrology/trueNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeKey = \
        "ui/astrology/trueNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationKey = \
        "ui/astrology/trueNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationDefValue = "TrueNNode"

    # QSettings key for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorKey = \
        "ui/astrology/trueNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorKey = \
        "ui/astrology/trueNorthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeKey = \
        "ui/astrology/trueSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeKey = \
        "ui/astrology/trueSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationKey = \
        "ui/astrology/trueSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationDefValue = "TrueSNode"

    # QSettings key for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorKey = \
        "ui/astrology/trueSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorKey = \
        "ui/astrology/trueSouthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeKey = \
        "ui/astrology/ceresGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeDefValue = "\u26b3"

    # QSettings key for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeKey = \
        "ui/astrology/ceresGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Ceres.
    planetCeresAbbreviationKey = \
        "ui/astrology/ceresAbbreviation"

    # QSettings default value for the planet abbreviation of the Ceres.
    planetCeresAbbreviationDefValue = "Ce"

    # QSettings key for the foreground color of the Ceres.
    planetCeresForegroundColorKey = \
        "ui/astrology/ceresForegroundColor"

    # QSettings default value for the foreground color of the Ceres.
    planetCeresForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Ceres.
    planetCeresBackgroundColorKey = \
        "ui/astrology/ceresBackgroundColor"

    # QSettings default value for the background color of the Ceres.
    planetCeresBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeKey = \
        "ui/astrology/pallasGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeDefValue = "\u26b4"

    # QSettings key for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeKey = \
        "ui/astrology/pallasGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pallas.
    planetPallasAbbreviationKey = \
        "ui/astrology/pallasAbbreviation"

    # QSettings default value for the planet abbreviation of the Pallas.
    planetPallasAbbreviationDefValue = "Pa"

    # QSettings key for the foreground color of the Pallas.
    planetPallasForegroundColorKey = \
        "ui/astrology/pallasForegroundColor"

    # QSettings default value for the foreground color of the Pallas.
    planetPallasForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pallas.
    planetPallasBackgroundColorKey = \
        "ui/astrology/pallasBackgroundColor"

    # QSettings default value for the background color of the Pallas.
    planetPallasBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeKey = \
        "ui/astrology/junoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeDefValue = "\u26b5"

    # QSettings key for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeKey = \
        "ui/astrology/junoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Juno.
    planetJunoAbbreviationKey = \
        "ui/astrology/junoAbbreviation"

    # QSettings default value for the planet abbreviation of the Juno.
    planetJunoAbbreviationDefValue = "Jun"

    # QSettings key for the foreground color of the Juno.
    planetJunoForegroundColorKey = \
        "ui/astrology/junoForegroundColor"

    # QSettings default value for the foreground color of the Juno.
    planetJunoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Juno.
    planetJunoBackgroundColorKey = \
        "ui/astrology/junoBackgroundColor"

    # QSettings default value for the background color of the Juno.
    planetJunoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeKey = \
        "ui/astrology/vestaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeKey = \
        "ui/astrology/vestaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Vesta.
    planetVestaAbbreviationKey = \
        "ui/astrology/vestaAbbreviation"

    # QSettings default value for the planet abbreviation of the Vesta.
    planetVestaAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Vesta.
    planetVestaForegroundColorKey = \
        "ui/astrology/vestaForegroundColor"

    # QSettings default value for the foreground color of the Vesta.
    planetVestaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Vesta.
    planetVestaBackgroundColorKey = \
        "ui/astrology/vestaBackgroundColor"

    # QSettings default value for the background color of the Vesta.
    planetVestaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeKey = \
        "ui/astrology/chironGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeDefValue = "\u26b7"

    # QSettings key for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeKey = \
        "ui/astrology/chironGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Chiron.
    planetChironAbbreviationKey = \
        "ui/astrology/chironAbbreviation"

    # QSettings default value for the planet abbreviation of the Chiron.
    planetChironAbbreviationDefValue = "Chi"

    # QSettings key for the foreground color of the Chiron.
    planetChironForegroundColorKey = \
        "ui/astrology/chironForegroundColor"

    # QSettings default value for the foreground color of the Chiron.
    planetChironForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Chiron.
    planetChironBackgroundColorKey = \
        "ui/astrology/chironBackgroundColor"

    # QSettings default value for the background color of the Chiron.
    planetChironBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeKey = \
        "ui/astrology/gulikaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeDefValue = "Gk"

    # QSettings key for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeKey = \
        "ui/astrology/gulikaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationKey = \
        "ui/astrology/gulikaAbbreviation"

    # QSettings default value for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationDefValue = "Gk"

    # QSettings key for the foreground color of the Gulika.
    planetGulikaForegroundColorKey = \
        "ui/astrology/gulikaForegroundColor"

    # QSettings default value for the foreground color of the Gulika.
    planetGulikaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gulika.
    planetGulikaBackgroundColorKey = \
        "ui/astrology/gulikaBackgroundColor"

    # QSettings default value for the background color of the Gulika.
    planetGulikaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeKey = \
        "ui/astrology/mandiGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeDefValue = "Md"

    # QSettings key for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeKey = \
        "ui/astrology/mandiGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mandi.
    planetMandiAbbreviationKey = \
        "ui/astrology/mandiAbbreviation"

    # QSettings default value for the planet abbreviation of the Mandi.
    planetMandiAbbreviationDefValue = "Md"

    # QSettings key for the foreground color of the Mandi.
    planetMandiForegroundColorKey = \
        "ui/astrology/mandiForegroundColor"

    # QSettings default value for the foreground color of the Mandi.
    planetMandiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mandi.
    planetMandiBackgroundColorKey = \
        "ui/astrology/mandiBackgroundColor"

    # QSettings default value for the background color of the Mandi.
    planetMandiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeKey = \
        "ui/astrology/meanOfFiveGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeDefValue = "MOF"

    # QSettings key for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeKey = \
        "ui/astrology/meanOfFiveGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationKey = \
        "ui/astrology/meanOfFiveAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationDefValue = "MOF"

    # QSettings key for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorKey = \
        "ui/astrology/meanOfFiveForegroundColor"

    # QSettings default value for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorKey = \
        "ui/astrology/meanOfFiveBackgroundColor"

    # QSettings default value for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeKey = \
        "ui/astrology/cycleOfEightGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeDefValue = "COE"

    # QSettings key for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeKey = \
        "ui/astrology/cycleOfEightGlyphFontSize"

    # QSettings default value for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationKey = \
        "ui/astrology/cycleOfEightAbbreviation"

    # QSettings default value for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationDefValue = "COE"

    # QSettings key for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorKey = \
        "ui/astrology/cycleOfEightForegroundColor"

    # QSettings default value for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorKey = \
        "ui/astrology/cycleOfEightBackgroundColor"

    # QSettings default value for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeKey = \
        "ui/astrology/avgMaJuSaUrNePlGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeKey = \
        "ui/astrology/avgMaJuSaUrNePlGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationKey = \
        "ui/astrology/avgMaJuSaUrNePlAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorKey = \
        "ui/astrology/avgMaJuSaUrNePlForegroundColor"

    # QSettings default value for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorKey = \
        "ui/astrology/avgMaJuSaUrNePlBackgroundColor"

    # QSettings default value for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeKey = \
        "ui/astrology/avgJuSaUrNeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeDefValue = "AvgJuSaUrNe"

    # QSettings key for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeKey = \
        "ui/astrology/avgJuSaUrNeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationKey = \
        "ui/astrology/avgJuSaUrNeAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationDefValue = "AvgJuSaUrNe"

    # QSettings key for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorKey = \
        "ui/astrology/avgJuSaUrNeForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorKey = \
        "ui/astrology/avgJuSaUrNeBackgroundColor"

    # QSettings default value for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeKey = \
        "ui/astrology/avgJuSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeDefValue = "AvgJuSa"

    # QSettings key for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeKey = \
        "ui/astrology/avgJuSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationKey = \
        "ui/astrology/avgJuSaAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationDefValue = "AvgJuSa"

    # QSettings key for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorKey = \
        "ui/astrology/avgJuSaForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorKey = \
        "ui/astrology/avgJuSaBackgroundColor"

    # QSettings default value for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeKey = \
        "ui/astrology/ariesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeDefValue = "\u2648"

    # QSettings key for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeKey = \
        "ui/astrology/ariesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aries.
    signAriesAbbreviationKey = \
        "ui/astrology/ariesAbbreviation"

    # QSettings default value for the sign abbreviation of the Aries.
    signAriesAbbreviationDefValue = "Ar"

    # QSettings key for the foreground color of the Aries.
    signAriesForegroundColorKey = \
        "ui/astrology/ariesForegroundColor"

    # QSettings default value for the foreground color of the Aries.
    signAriesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aries.
    signAriesBackgroundColorKey = \
        "ui/astrology/ariesBackgroundColor"

    # QSettings default value for the background color of the Aries.
    signAriesBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeKey = \
        "ui/astrology/taurusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeDefValue = "\u2649"

    # QSettings key for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeKey = \
        "ui/astrology/taurusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Taurus.
    signTaurusAbbreviationKey = \
        "ui/astrology/taurusAbbreviation"

    # QSettings default value for the sign abbreviation of the Taurus.
    signTaurusAbbreviationDefValue = "Ta"

    # QSettings key for the foreground color of the Taurus.
    signTaurusForegroundColorKey = \
        "ui/astrology/taurusForegroundColor"

    # QSettings default value for the foreground color of the Taurus.
    signTaurusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Taurus.
    signTaurusBackgroundColorKey = \
        "ui/astrology/taurusBackgroundColor"

    # QSettings default value for the background color of the Taurus.
    signTaurusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeKey = \
        "ui/astrology/geminiGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeDefValue = "\u264a"

    # QSettings key for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeKey = \
        "ui/astrology/geminiGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Gemini.
    signGeminiAbbreviationKey = \
        "ui/astrology/geminiAbbreviation"

    # QSettings default value for the sign abbreviation of the Gemini.
    signGeminiAbbreviationDefValue = "Ge"

    # QSettings key for the foreground color of the Gemini.
    signGeminiForegroundColorKey = \
        "ui/astrology/geminiForegroundColor"

    # QSettings default value for the foreground color of the Gemini.
    signGeminiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gemini.
    signGeminiBackgroundColorKey = \
        "ui/astrology/geminiBackgroundColor"

    # QSettings default value for the background color of the Gemini.
    signGeminiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeKey = \
        "ui/astrology/cancerGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeDefValue = "\u264b"

    # QSettings key for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeKey = \
        "ui/astrology/cancerGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Cancer.
    signCancerAbbreviationKey = \
        "ui/astrology/cancerAbbreviation"

    # QSettings default value for the sign abbreviation of the Cancer.
    signCancerAbbreviationDefValue = "Ca"

    # QSettings key for the foreground color of the Cancer.
    signCancerForegroundColorKey = \
        "ui/astrology/cancerForegroundColor"

    # QSettings default value for the foreground color of the Cancer.
    signCancerForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Cancer.
    signCancerBackgroundColorKey = \
        "ui/astrology/cancerBackgroundColor"

    # QSettings default value for the background color of the Cancer.
    signCancerBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeKey = \
        "ui/astrology/leoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeDefValue = "\u264c"

    # QSettings key for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeKey = \
        "ui/astrology/leoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Leo.
    signLeoAbbreviationKey = \
        "ui/astrology/leoAbbreviation"

    # QSettings default value for the sign abbreviation of the Leo.
    signLeoAbbreviationDefValue = "Le"

    # QSettings key for the foreground color of the Leo.
    signLeoForegroundColorKey = \
        "ui/astrology/leoForegroundColor"

    # QSettings default value for the foreground color of the Leo.
    signLeoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Leo.
    signLeoBackgroundColorKey = \
        "ui/astrology/leoBackgroundColor"

    # QSettings default value for the background color of the Leo.
    signLeoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeKey = \
        "ui/astrology/virgoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeDefValue = "\u264d"

    # QSettings key for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeKey = \
        "ui/astrology/virgoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Virgo.
    signVirgoAbbreviationKey = \
        "ui/astrology/virgoAbbreviation"

    # QSettings default value for the sign abbreviation of the Virgo.
    signVirgoAbbreviationDefValue = "Vi"

    # QSettings key for the foreground color of the Virgo.
    signVirgoForegroundColorKey = \
        "ui/astrology/virgoForegroundColor"

    # QSettings default value for the foreground color of the Virgo.
    signVirgoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Virgo.
    signVirgoBackgroundColorKey = \
        "ui/astrology/virgoBackgroundColor"

    # QSettings default value for the background color of the Virgo.
    signVirgoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeKey = \
        "ui/astrology/libraGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeDefValue = "\u264e"

    # QSettings key for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeKey = \
        "ui/astrology/libraGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Libra.
    signLibraAbbreviationKey = \
        "ui/astrology/libraAbbreviation"

    # QSettings default value for the sign abbreviation of the Libra.
    signLibraAbbreviationDefValue = "Li"

    # QSettings key for the foreground color of the Libra.
    signLibraForegroundColorKey = \
        "ui/astrology/libraForegroundColor"

    # QSettings default value for the foreground color of the Libra.
    signLibraForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Libra.
    signLibraBackgroundColorKey = \
        "ui/astrology/libraBackgroundColor"

    # QSettings default value for the background color of the Libra.
    signLibraBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeKey = \
        "ui/astrology/scorpioGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeDefValue = "\u264f"

    # QSettings key for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeKey = \
        "ui/astrology/scorpioGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationKey = \
        "ui/astrology/scorpioAbbreviation"

    # QSettings default value for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationDefValue = "Sc"

    # QSettings key for the foreground color of the Scorpio.
    signScorpioForegroundColorKey = \
        "ui/astrology/scorpioForegroundColor"

    # QSettings default value for the foreground color of the Scorpio.
    signScorpioForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Scorpio.
    signScorpioBackgroundColorKey = \
        "ui/astrology/scorpioBackgroundColor"

    # QSettings default value for the background color of the Scorpio.
    signScorpioBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeKey = \
        "ui/astrology/sagittariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeDefValue = "\u2650"

    # QSettings key for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeKey = \
        "ui/astrology/sagittariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationKey = \
        "ui/astrology/sagittariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Sagittarius.
    signSagittariusForegroundColorKey = \
        "ui/astrology/sagittariusForegroundColor"

    # QSettings default value for the foreground color of the Sagittarius.
    signSagittariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sagittarius.
    signSagittariusBackgroundColorKey = \
        "ui/astrology/sagittariusBackgroundColor"

    # QSettings default value for the background color of the Sagittarius.
    signSagittariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeKey = \
        "ui/astrology/capricornGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeDefValue = "\u2651"

    # QSettings key for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeKey = \
        "ui/astrology/capricornGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationKey = \
        "ui/astrology/capricornAbbreviation"

    # QSettings default value for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationDefValue = "Cp"

    # QSettings key for the foreground color of the Capricorn.
    signCapricornForegroundColorKey = \
        "ui/astrology/capricornForegroundColor"

    # QSettings default value for the foreground color of the Capricorn.
    signCapricornForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Capricorn.
    signCapricornBackgroundColorKey = \
        "ui/astrology/capricornBackgroundColor"

    # QSettings default value for the background color of the Capricorn.
    signCapricornBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeKey = \
        "ui/astrology/aquariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeDefValue = "\u2652"

    # QSettings key for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeKey = \
        "ui/astrology/aquariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationKey = \
        "ui/astrology/aquariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationDefValue = "Aq"

    # QSettings key for the foreground color of the Aquarius.
    signAquariusForegroundColorKey = \
        "ui/astrology/aquariusForegroundColor"

    # QSettings default value for the foreground color of the Aquarius.
    signAquariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aquarius.
    signAquariusBackgroundColorKey = \
        "ui/astrology/aquariusBackgroundColor"

    # QSettings default value for the background color of the Aquarius.
    signAquariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeKey = \
        "ui/astrology/piscesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeDefValue = "\u2653"

    # QSettings key for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeKey = \
        "ui/astrology/piscesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Pisces.
    signPiscesAbbreviationKey = \
        "ui/astrology/piscesAbbreviation"

    # QSettings default value for the sign abbreviation of the Pisces.
    signPiscesAbbreviationDefValue = "Pi"

    # QSettings key for the foreground color of the Pisces.
    signPiscesForegroundColorKey = \
        "ui/astrology/piscesForegroundColor"

    # QSettings default value for the foreground color of the Pisces.
    signPiscesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pisces.
    signPiscesBackgroundColorKey = \
        "ui/astrology/piscesBackgroundColor"

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



