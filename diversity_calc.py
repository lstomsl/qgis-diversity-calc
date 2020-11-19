# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DiversityCalc
                                 A QGIS plugin
 Calculates biodiversity indexes (Richness, Shannons, and Simpsons)
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Miller Mountain LLC
        email                : mmllc@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QTreeWidgetItem

from qgis.core import QgsMapLayerProxyModel, QgsFieldProxyModel, QgsMessageLog, Qgis

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .diversity_calc_dialog import DiversityCalcDialog
from .diversity_results_dialog import DlgResults
from .diversity_functions import dc_summarizePoly, dc_mergeDictionaries, dc_resultString, dc_richness, dc_evenness, dc_shannons, dc_simpsons
import os.path


class DiversityCalc:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DiversityCalc_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Diversity Calculator')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DiversityCalc', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/diversity_calc/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Diversity Calculator'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Diversity Calculator'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = DiversityCalcDialog()

            self.dlg.mcbPoly.setFilters(QgsMapLayerProxyModel.PolygonLayer)
            self.dlg.mcbPoint.setFilters(QgsMapLayerProxyModel.PointLayer)

            self.dlg.fcbCategory.setFilters(QgsFieldProxyModel.String)
            self.dlg.fcbSpecies.setFilters(QgsFieldProxyModel.String)

            self.dlg.fcbCategory.setLayer(self.dlg.mcbPoly.currentLayer())
            self.dlg.fcbSpecies.setLayer(self.dlg.mcbPoint.currentLayer())

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        if result:
            # Get required input parameters from the dialog
            lyrPoly = self.dlg.mcbPoly.currentLayer()
            lyrPoint = self.dlg.mcbPoint.currentLayer()

            fldCategory = self.dlg.fcbCategory.currentField()
            fldSpecies = self.dlg.fcbSpecies.currentField()

            dctMain = {}
            # Loop through poly features
            for poly in lyrPoly.getFeatures():
                sCategory = poly.attribute(fldCategory)
                QgsMessageLog.logMessage("Category: {}".format(sCategory), "Diversity Calculator", level=Qgis.Info)
                # Call dc_summarizePoly in diversity_functions.py to generate a summary dictionary
                dctSummary = dc_summarizePoly(poly, lyrPoint, fldSpecies)
                QgsMessageLog.logMessage("Summary: {}".format(dctSummary), "Diversity Calculator", level=Qgis.Info)
                # Call dc_mergeDictionaries in diversity_functions.py to merge summary dictionary into the main results
                dctMain = dc_mergeDictionaries(dctMain, sCategory, dctSummary)

            # create a results dialog with a treewidget to show results
            dlgResults = DlgResults()

            # populate treewidget with results
            for category, summary in dctMain.items():
                total = sum(summary.values())
                twiCat = QTreeWidgetItem(dlgResults.trwResults, [category, str(total), str(dc_richness(summary)), "{:3.3f}".format(dc_evenness(summary)), "{:3.3f}".format(dc_shannons(summary)), "{:3.3f}".format(dc_simpsons(summary))])
                for species, obs in summary.items():
                    twiCat.addChild(QTreeWidgetItem(twiCat, [species, str(obs)]))
                dlgResults.trwResults.addTopLevelItem(twiCat)

            dlgResults.show()
            dlgResults.exec_()





