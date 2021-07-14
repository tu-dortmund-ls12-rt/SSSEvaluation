from __future__ import division
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import sys
import numpy as np
from schedTest import tgPath, SCEDF, SCRM, EDA, PROPORTIONAL, NC, SEIFDA, Audsley, rad, PATH, mipx
from schedTest import RSS, UDLEDF, WLAEDF, RTEDF, UNIFRAMEWORK, FixedPriority, GMFPA, SRSR, Biondi, Uppaal
from effsstsPlot import effsstsPlot
import os
import datetime
import pickle
from multiprocessing import Pool
from pathlib import Path

gSeed = datetime.datetime.now()
gPrefixdata = ''
gTasksetpath = ''
gRuntest = True
gPlotdata = True
gPlotall = True
gTaskChoice = ''
gNumberOfTaskSets = 100
gNumberOfTasksPerSet = 10
gUStart = 0
gUEnd = 100
gUStep = 5
gNumberOfSegs = 2
gSchemes = []
gSLenMinValue = 0.01
gSLenMaxValue = 0.1
garwrap = []
gthread = 1

gmultiplot = ''
gmpCheck = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        choice_list = ['Generate Tasksets', 'Generate and Save Tasksets', 'Load Tasksets']
        choice_plot = ['Tasks per Set', 'Number of Segments', 'Suspension Length']


        VerticalSize = 1024
        HorizontalSize = 660
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Evaluation Framework for Self-Suspending Task Systems")
        MainWindow.resize(VerticalSize, HorizontalSize)
        MainWindow.setMaximumWidth(VerticalSize)
        MainWindow.setMaximumHeight(HorizontalSize)
        MainWindow.setMinimumWidth(VerticalSize)
        MainWindow.setMinimumHeight(HorizontalSize)



        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        
        self.groupBox_general = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_general.setGeometry(QtCore.QRect(12, 12, 1000, 100))
        self.groupBox_general.setObjectName("groupBox_general")
        self.groupBox_general.setTitle("General")

        self.runtests = QtWidgets.QCheckBox(self.groupBox_general)
        self.runtests.setGeometry(QtCore.QRect(12, 32, 91, 25))
        self.runtests.setChecked(True)
        self.runtests.setObjectName("runtests")
        self.runtests.setText("Run Tests")

        self.combobox_input = QtWidgets.QComboBox(self.groupBox_general)
        self.combobox_input.setGeometry(QtCore.QRect(110, 32, 225, 25))
        self.combobox_input.setObjectName("combobox_input")
        self.combobox_input.addItems(choice_list)
        self.combobox_input.currentIndexChanged.connect(lambda: selectionchange(self.combobox_input))

        self.loadtasks_title = QtWidgets.QLabel(self.groupBox_general)
        self.loadtasks_title.setGeometry(QtCore.QRect(345, 32, 90, 25))
        self.loadtasks_title.setObjectName("loadtasks_title")
        self.loadtasks_title.setText("File Name:")
        self.loadtasks_title.hide()

        self.tasksetdatapath = QtWidgets.QLineEdit(self.groupBox_general)
        self.tasksetdatapath.setGeometry(QtCore.QRect(425, 32, 365, 25))
        self.tasksetdatapath.setObjectName("tasksetdatapath")
        self.tasksetdatapath.setText("Ts-100-Tn-10-Ust-5-Ssl-0.01-0.1-Seg-2-.pkl")
        self.tasksetdatapath.hide()

        self.label_threadcount = QtWidgets.QLabel(self.groupBox_general)
        self.label_threadcount.setGeometry(QtCore.QRect(800, 32, 100, 25))
        self.label_threadcount.setObjectName("label_threadcount")
        self.label_threadcount.setText("Threadcount:")

        self.threadcount = QtWidgets.QLineEdit(self.groupBox_general)
        self.threadcount.setGeometry(QtCore.QRect(895, 32, 95, 25))
        self.threadcount.setObjectName("threadcount")
        self.threadcount.setText("1")
        
        self.label_prefixdatapath = QtWidgets.QLabel(self.groupBox_general)
        self.label_prefixdatapath.setGeometry(QtCore.QRect(12, 65, 115, 25))
        self.label_prefixdatapath.setObjectName("label_prefixdatapath")
        self.label_prefixdatapath.setText("Prefix Data Path:")

        self.prefixdatapath = QtWidgets.QLineEdit(self.groupBox_general)
        self.prefixdatapath.setGeometry(QtCore.QRect(131, 65, 660, 25))
        self.prefixdatapath.setObjectName("prefixdatapath")
        self.prefixdatapath.setText("effsstsPlot/Data")

        self.label_seed = QtWidgets.QLabel(self.groupBox_general)
        self.label_seed.setGeometry(QtCore.QRect(800, 65, 40, 25))
        self.label_seed.setObjectName("label_seed")
        self.label_seed.setText("Seed:")

        self.seed = QtWidgets.QLineEdit(self.groupBox_general)
        self.seed.setGeometry(QtCore.QRect(845, 65, 145, 25))
        self.seed.setObjectName("seed")



        self.groupbox_configurations = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox_configurations.setGeometry(QtCore.QRect(12, 122, 1000, 100))
        self.groupbox_configurations.setObjectName("groupbox_configurations")
        self.groupbox_configurations.setTitle("Configurations")

        self.label_tasksetsperconfiguration = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_tasksetsperconfiguration.setGeometry(QtCore.QRect(12, 32, 198, 25))
        self.label_tasksetsperconfiguration.setObjectName("label_tasksetsperconfiguration") # task sets per configuration
        self.label_tasksetsperconfiguration.setText("Task Sets per Configuration:")

        self.tasksetsperconfig = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.tasksetsperconfig.setGeometry(QtCore.QRect(210, 32, 55, 25))
        self.tasksetsperconfig.setMaximum(1000)
        self.tasksetsperconfig.setProperty("value", 100)
        self.tasksetsperconfig.setObjectName("tasksetsperconfig")

        self.label_taskperset = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_taskperset.setGeometry(QtCore.QRect(12, 65, 198, 25))
        self.label_taskperset.setObjectName("label_taskperset") # tasks per set
        self.label_taskperset.setText("Tasks per Set:")

        self.tasksperset = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.tasksperset.setGeometry(QtCore.QRect(210, 65, 55, 25))
        self.tasksperset.setMaximum(100)
        self.tasksperset.setProperty("value", 10)
        self.tasksperset.setObjectName("tasksperset")

        self.label_utilizationstartvalue = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_utilizationstartvalue.setGeometry(QtCore.QRect(275, 32, 155, 25))
        self.label_utilizationstartvalue.setObjectName("label_utilizationstartvalue") # utilization start value
        self.label_utilizationstartvalue.setText("Utilization Start Value:")

        self.utilstart = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilstart.setGeometry(QtCore.QRect(435, 32, 55, 25))
        self.utilstart.setMaximum(100)
        self.utilstart.setProperty("value", 0)
        self.utilstart.setObjectName("utilstart")

        self.label_utilizationendvalue = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_utilizationendvalue.setGeometry(QtCore.QRect(275, 65, 155, 25))
        self.label_utilizationendvalue.setObjectName("label_utilizationendvalue") # utilization end value
        self.label_utilizationendvalue.setText("Utilization End Value:")

        self.utilend = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilend.setGeometry(QtCore.QRect(435, 65, 55, 25)) #util end value
        self.utilend.setMaximum(100)
        self.utilend.setProperty("value", 100)
        self.utilend.setObjectName("utilend")

        self.label_utilizationstep = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_utilizationstep.setGeometry(QtCore.QRect(500, 32, 160, 25))
        self.label_utilizationstep.setObjectName("label_utilizationstep") # utilization step
        self.label_utilizationstep.setText("Utilization Step:")
        
        self.utilstep = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilstep.setGeometry(QtCore.QRect(660, 32, 55, 25))
        self.utilstep.setMaximum(100)
        self.utilstep.setProperty("value", 5)
        self.utilstep.setObjectName("utilstep")

        self.label_numberofsegments = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_numberofsegments.setGeometry(QtCore.QRect(500, 65, 155, 25))
        self.label_numberofsegments.setObjectName("label_numberofsegments") # num_of_segment
        self.label_numberofsegments.setText("Number of Segments:")

        self.numberofsegs = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.numberofsegs.setGeometry(QtCore.QRect(660, 65, 55, 25))
        self.numberofsegs.setMaximum(100)
        self.numberofsegs.setProperty("value", 2)
        self.numberofsegs.setObjectName("numberofsegs")

        self.label_suspensionminvalue = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_suspensionminvalue.setGeometry(QtCore.QRect(725, 32, 210, 25))
        self.label_suspensionminvalue.setObjectName("label_suspensionminvalue") # suspension length min value
        self.label_suspensionminvalue.setText("Suspension Length Min Value:")
        
        self.slengthminvalue = QtWidgets.QDoubleSpinBox(self.groupbox_configurations)
        self.slengthminvalue.setGeometry(QtCore.QRect(935, 32, 55, 25))
        self.slengthminvalue.setMaximum(1.0)
        self.slengthminvalue.setSingleStep(0.01)
        self.slengthminvalue.setProperty("value", 0.01)
        self.slengthminvalue.setObjectName("slengthminvalue")

        self.label_suspensionmaxvalue = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_suspensionmaxvalue.setGeometry(QtCore.QRect(725, 65, 210, 25)) 
        self.label_suspensionmaxvalue.setObjectName("label_suspensionmaxvalue") # suspension length max
        self.label_suspensionmaxvalue.setText("Suspension Length Max Value:")

        self.slengthmaxvalue = QtWidgets.QDoubleSpinBox(self.groupbox_configurations)
        self.slengthmaxvalue.setGeometry(QtCore.QRect(935, 65, 55, 25))
        self.slengthmaxvalue.setMaximum(1.0)
        self.slengthmaxvalue.setSingleStep(0.01)
        self.slengthmaxvalue.setProperty("value", 0.1)
        self.slengthmaxvalue.setObjectName("slengthmaxvalue")



        self.groupbox_schedulability_tests = QtWidgets.QGroupBox(self.centralwidget) #Schedulability tests
        self.groupbox_schedulability_tests.setGeometry(QtCore.QRect(12, 232, 1000, 228))
        self.groupbox_schedulability_tests.setObjectName("groupbox_schedulability_tests")
        self.groupbox_schedulability_tests.setTitle("Schedulability tests")



        self.tabs = QtWidgets.QTabWidget(self.groupbox_schedulability_tests)
        self.tabs.setGeometry(QtCore.QRect(1, 21, 999, 207))
        self.tabs.setObjectName("tabs")



        self.scrollArea_1 = QtWidgets.QScrollArea(self.tabs)   # FRD Segmented
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollArea_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_1.setObjectName("scrollAreaWidgetContents_1")

        self.formLayoutWidget_1 = QtWidgets.QWidget(self.scrollAreaWidgetContents_1)
        self.formLayoutWidget_1.setObjectName("formLayoutWidget_1")

        self.formLayout_1 = QtWidgets.QFormLayout(self.formLayoutWidget_1)
        self.formLayout_1.setObjectName("formLayout_1")

        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)
        self.scrollAreaWidgetContents_1.setLayout(self.formLayout_1)

        self.tabs.addTab(self.scrollArea_1,"FRD Segmented")

        self.seifdamind = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.seifdamind.setObjectName("seifdamind")
        self.seifdamind.setText("SEIFDA-minD-")
        self.seifdamind.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the minimum x')
        self.formLayout_1.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.seifdamind)

        self.seifdamindg = QtWidgets.QSpinBox(self.formLayoutWidget_1)
        self.seifdamindg.setMaximum(5)
        self.seifdamindg.setProperty("value", 1)
        self.seifdamindg.setObjectName("seifdamindg")
        self.formLayout_1.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.seifdamindg)

        self.seifdamaxd = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.seifdamaxd.setObjectName("seifdamaxd")
        self.seifdamaxd.setText("SEIFDA-maxD-")
        self.seifdamaxd.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the maximum x')
        self.formLayout_1.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.seifdamaxd)

        self.seifdamaxdg = QtWidgets.QSpinBox(self.formLayoutWidget_1)
        self.seifdamaxdg.setMaximum(5)
        self.seifdamaxdg.setProperty("value", 1)
        self.seifdamaxdg.setObjectName("seifdamaxdg")
        self.formLayout_1.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.seifdamaxdg)

        self.seifdapbmind = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.seifdapbmind.setObjectName("seifdapbmind")
        self.seifdapbmind.setText("SEIFDA-PBminD-")
        self.seifdapbmind.setToolTip('Shortest Execution Interval First Deadline Assignment - Proportionally-Bounded-Min x')
        self.formLayout_1.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.seifdapbmind)
        
        self.seifdapbmindg = QtWidgets.QSpinBox(self.formLayoutWidget_1)
        self.seifdapbmindg.setMaximum(5)
        self.seifdapbmindg.setProperty("value", 1)
        self.seifdapbmindg.setObjectName("seifdapbmindg")
        self.formLayout_1.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.seifdapbmindg)

        self.eda = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.eda.setObjectName("eda")
        self.eda.setText("EDA")
        self.eda.setToolTip('Equal relative Deadline Assignment (EDA)') 
        self.formLayout_1.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.eda)

        self.proportional = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.proportional.setObjectName("proportional")
        self.proportional.setText("PROPORTIONAL")
        self.proportional.setToolTip('Proportional relative deadline assignment')
        self.formLayout_1.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.proportional)

        self.seifdamip = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.seifdamip.setObjectName("seifdamip")
        self.seifdamip.setText("SEIFDA-MILP")
        self.seifdamip.setToolTip('Shortest Execution Interval First Deadline Assignment - MILP')
        self.formLayout_1.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.seifdamip)

        self.gmfpa = QtWidgets.QCheckBox(self.formLayoutWidget_1)
        self.gmfpa.setObjectName("gmfpa")
        self.gmfpa.setText("GMFPA-")
        self.gmfpa.setToolTip('Generalized Multiframe Task Model with Parameter Adaptation - Set granularity of time steps')
        self.formLayout_1.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.gmfpa)

        self.gmfpag = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_1)
        self.gmfpag.setMaximum(1.0)
        self.gmfpag.setSingleStep(0.01)
        self.gmfpag.setProperty("value", 0.5)
        self.gmfpag.setObjectName("gmfpag")
        self.formLayout_1.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.gmfpag)



        self.scrollArea_2 = QtWidgets.QScrollArea(self.tabs)   # FRD Hybrid
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.formLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.formLayoutWidget_2.setObjectName("formLayoutWidget")

        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName("formLayout_2")

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollAreaWidgetContents_2.setLayout(self.formLayout_2)

        self.tabs.addTab(self.scrollArea_2,"FRD Hybrid")

        self.pathminddd = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.pathminddd.setObjectName("pathminddd")
        self.pathminddd.setText("Oblivious-IUB-")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pathminddd)

        self.pathminddd.setToolTip('Pattern Oblivious Individual Upper Bounds')
        self.pathmindddg = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        self.pathmindddg.setMaximum(5)
        self.pathmindddg.setProperty("value", 1)
        self.pathmindddg.setObjectName("pathmindddg")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pathmindddg)

        self.pathminddnd = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.pathminddnd.setObjectName("pathminddnd")
        self.pathminddnd.setText("Clairvoyant-SSSD-")
        self.pathminddnd.setToolTip('Pattern-Clairvoyant Shorter Segment Shorter Deadline')
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pathminddnd)

        self.pathminddndg = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        self.pathminddndg.setMaximum(5)
        self.pathminddndg.setProperty("value", 1)
        self.pathminddndg.setObjectName("pathminddndg")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pathminddndg)

        self.pathpbminddd = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.pathpbminddd.setObjectName("pathpbminddd")
        self.pathpbminddd.setText("Oblivious-MP-")
        self.pathpbminddd.setToolTip('Pattern-Oblivious Multiple Paths')
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pathpbminddd)

        self.pathpbmindddg = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        self.pathpbmindddg.setMaximum(5)
        self.pathpbmindddg.setProperty("value", 1)
        self.pathpbmindddg.setObjectName("pathpbmindddg")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pathpbmindddg)

        self.pathpbminddnd = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.pathpbminddnd.setObjectName("pathpbminddnd")
        self.pathpbminddnd.setText("Clairvoyant-PDAB-")
        self.pathpbminddnd.setToolTip('Pattern-Clairvoyant Proportional Deadline with A Bias')
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pathpbminddnd)

        self.pathpbminddndg = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        self.pathpbminddndg.setMaximum(5)
        self.pathpbminddndg.setProperty("value", 1)
        self.pathpbminddndg.setObjectName("pathpbminddndg")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pathpbminddndg)



        self.scrollArea_3 = QtWidgets.QScrollArea(self.tabs)   # Segmented
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollArea_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")

        self.formLayoutWidget_3 = QtWidgets.QWidget(self.scrollAreaWidgetContents_3)
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")

        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName("formLayout_3")

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.scrollAreaWidgetContents_3.setLayout(self.formLayout_3)

        self.tabs.addTab(self.scrollArea_3,"Segmented")

        self.scedf = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.scedf.setObjectName("scedf")
        self.scedf.setText("SCEDF")
        self.scedf.setToolTip('Suspension as Computation Earliest-Deadline-First (SCEDF)')
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.scedf)

        self.scrm = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.scrm.setObjectName("scrm")
        self.scrm.setText("SCRM")
        self.scrm.setToolTip('Suspension as Computation Rate-Monotonic (SCRM)')
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.scrm)
        
        self.scairrm = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.scairrm.setObjectName("scairrm")
        self.scairrm.setText("SCAIR-RM")
        self.scairrm.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Rate-Monotonic (RM)')
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.scairrm)
        
        self.scairopa = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.scairopa.setObjectName("scairopa")
        self.scairopa.setText("SCAIR-OPA")
        self.scairopa.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Optimal Priority Assignment (OPA) ')
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.scairopa)
        
        self.frdgmfopa = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.frdgmfopa.setObjectName("frdgmfopa")
        self.frdgmfopa.setText("FRDGMF-OPA")
        self.frdgmfopa.setToolTip('Fixed Relative Deadline (FRD) and Generalized Multiframe (GMF) Optimal Priority Assignment (OPA) ')
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.frdgmfopa)
        
        self.biondi = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.biondi.setObjectName("Biondi")
        self.biondi.setText("BIONDI")
        self.biondi.setToolTip('Alessandros Method. Biondi (RTSS 2016)')
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.biondi)
        
        self.srsr = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.srsr.setObjectName("srsr")
        self.srsr.setText("SRSR")
        self.srsr.setToolTip('Schedulability Analysis with synchronous release sequence refinement')
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.srsr)



        self.scrollArea_4 = QtWidgets.QScrollArea(self.tabs)   # Dynamic
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollArea_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")

        self.formLayoutWidget_4 = QtWidgets.QWidget(self.scrollAreaWidgetContents_4)
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")

        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setObjectName("formLayout_4")

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.scrollAreaWidgetContents_4.setLayout(self.formLayout_4)

        self.tabs.addTab(self.scrollArea_4,"Dynamic")

        self.passopa = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.passopa.setObjectName("passopa")
        self.passopa.setText("PASS-OPA")
        self.passopa.setToolTip('Priority Assignment algorithm for Self-Suspending Systems - Optimal-Priority Assignment')
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passopa)

        self.rss = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.rss.setObjectName("rss")
        self.rss.setText("RSS")
        self.rss.setToolTip('Utilization-based Schedulability Test')
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rss)
        
        self.udledf = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.udledf.setObjectName("udledf")
        self.udledf.setText("UDLEDF")
        self.udledf.setToolTip('')
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.udledf)
        
        self.wlaedf = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.wlaedf.setObjectName("wlaedf")
        self.wlaedf.setText("WLAEDF")
        self.wlaedf.setToolTip('Workload-based Schedulability Test')
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.wlaedf)
        
        self.rtedf = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.rtedf.setObjectName("rtedf")
        self.rtedf.setText("RTEDF")
        self.rtedf.setToolTip('Response-Time-Based Schedulability Test')
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rtedf)
        
        self.uniframework = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.uniframework.setObjectName("uniframework")
        self.uniframework.setText("UNIFRAMEWORK")
        self.uniframework.setToolTip('Unified Response Time Analysis Framework')
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.uniframework)
        
        self.suspobl = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.suspobl.setObjectName("suspobl")
        self.suspobl.setText("SUSPOBL")
        self.suspobl.setToolTip('Suspension Oblivious')
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.suspobl)

        self.suspjit = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.suspjit.setObjectName("suspjit")
        self.suspjit.setText("SUSPJIT")
        self.suspjit.setToolTip('Schedulability with Suspension as Jitter')
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.suspjit)

        self.suspblock = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.suspblock.setObjectName("suspblock")
        self.suspblock.setText("SUSPBLOCK")
        self.suspblock.setToolTip('Schedulability with Suspension as Blocking Time')
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.suspblock)

        self.uppaal = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.uppaal.setObjectName("uppaal")
        self.uppaal.setText("UPPAAL")
        self.uppaal.setToolTip('Exact Schedulability Test for Non-Preemptive Self-Suspending Real-Time Tasks with UPPAAL model checker')
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.uppaal)



        self.scrollArea_5 = QtWidgets.QScrollArea(self.tabs)   # General
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollArea_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")

        self.formLayoutWidget_5 = QtWidgets.QWidget(self.scrollAreaWidgetContents_5)
        self.formLayoutWidget_5.setObjectName("formLayoutWidget_5")

        self.formLayout_5 = QtWidgets.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setObjectName("formLayout_5")

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.scrollAreaWidgetContents_5.setLayout(self.formLayout_5)

        self.tabs.addTab(self.scrollArea_5,"General")

        self.nc = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.nc.setObjectName("nc")
        self.nc.setText("NC")
        self.nc.setToolTip('Necessary Condition')
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nc)



        self.groupbox_plots = QtWidgets.QGroupBox(self.centralwidget)  # multi plot
        self.groupbox_plots.setGeometry(QtCore.QRect(12, 470, 1000, 130))
        self.groupbox_plots.setObjectName("groupbox_plots")
        self.groupbox_plots.setTitle("Plots")
        
        self.plotdata = QtWidgets.QCheckBox(self.groupbox_plots)
        self.plotdata.setGeometry(QtCore.QRect(12, 30, 160, 25))
        self.plotdata.setChecked(True)
        self.plotdata.setObjectName("plotdata")
        self.plotdata.setText("Plot selected Tests")

        self.plotall = QtWidgets.QCheckBox(self.groupbox_plots)
        self.plotall.setGeometry(QtCore.QRect(172, 30, 180, 25))
        self.plotall.setChecked(True)
        self.plotall.setObjectName("plotall")
        self.plotall.setText("Combine selected Tests")

        self.mp_check = QtWidgets.QCheckBox(self.groupbox_plots)
        self.mp_check.setGeometry(QtCore.QRect(12, 63, 190, 25))
        self.mp_check.setObjectName("mp_check")
        self.mp_check.setText("Combine available Tests")
        self.mp_check.setToolTip('Plots')
        self.mp_check.stateChanged.connect(lambda: selectionchange_plot(self.combobox_plot))

        self.label_mp_control = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_control.setGeometry(QtCore.QRect(211, 63, 130, 25))
        self.label_mp_control.setObjectName("label_mp")
        self.label_mp_control.setText("Control Parameter:")

        self.combobox_plot = QtWidgets.QComboBox(self.groupbox_plots)
        self.combobox_plot.setGeometry(QtCore.QRect(351, 63, 180, 25))
        self.combobox_plot.setObjectName("combobox_plot")
        self.combobox_plot.addItems(choice_plot)
        self.combobox_plot.currentIndexChanged.connect(lambda: selectionchange_plot(self.combobox_plot))

        self.label_mp = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp.setGeometry(QtCore.QRect(12, 96, 50, 25))
        self.label_mp.setObjectName("label_mp")
        self.label_mp.setText("Values:")

        self.tasksperset_p1 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p1.setGeometry(QtCore.QRect(74, 96, 50, 25))
        self.tasksperset_p1.setMaximum(100)
        self.tasksperset_p1.setProperty("value", 10)
        self.tasksperset_p1.setObjectName("tasksperset")

        self.tasksperset_p2 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p2.setGeometry(QtCore.QRect(136, 96, 50, 25))
        self.tasksperset_p2.setMaximum(100)
        self.tasksperset_p2.setProperty("value", 10)
        self.tasksperset_p2.setObjectName("tasksperset")

        self.tasksperset_p3 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p3.setGeometry(QtCore.QRect(198, 96, 50, 25))
        self.tasksperset_p3.setMaximum(100)
        self.tasksperset_p3.setProperty("value", 10)
        self.tasksperset_p3.setObjectName("tasksperset")

        self.numberofsegs_p1 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p1.setGeometry(QtCore.QRect(74, 96, 50, 25))
        self.numberofsegs_p1.setMaximum(100)
        self.numberofsegs_p1.setProperty("value", 2)
        self.numberofsegs_p1.setObjectName("numberofsegs")

        self.numberofsegs_p2 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p2.setGeometry(QtCore.QRect(136, 96, 50, 25))
        self.numberofsegs_p2.setMaximum(100)
        self.numberofsegs_p2.setProperty("value", 2)
        self.numberofsegs_p2.setObjectName("numberofsegs")

        self.numberofsegs_p3 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p3.setGeometry(QtCore.QRect(198, 96, 50, 25))
        self.numberofsegs_p3.setMaximum(100)
        self.numberofsegs_p3.setProperty("value", 2)
        self.numberofsegs_p3.setObjectName("numberofsegs")

        self.label_mp_max = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_max.setGeometry(QtCore.QRect(12, 96, 80, 25))
        self.label_mp_max.setObjectName("label_mp_max")
        self.label_mp_max.setText("Max Values:")
        self.label_mp_max.hide()

        self.slengthmaxvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p1.setGeometry(QtCore.QRect(104, 96, 55, 25))
        self.slengthmaxvalue_p1.setMaximum(1.0)
        self.slengthmaxvalue_p1.setSingleStep(0.01)
        self.slengthmaxvalue_p1.setProperty("value", 0.1)
        self.slengthmaxvalue_p1.setObjectName("slengthmaxvalue")

        self.slengthmaxvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p2.setGeometry(QtCore.QRect(171, 96, 55, 25))
        self.slengthmaxvalue_p2.setMaximum(1.0)
        self.slengthmaxvalue_p2.setSingleStep(0.01)
        self.slengthmaxvalue_p2.setProperty("value", 0.1)
        self.slengthmaxvalue_p2.setObjectName("slengthmaxvalue")
        
        self.slengthmaxvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p3.setGeometry(QtCore.QRect(238, 96, 55, 25))
        self.slengthmaxvalue_p3.setMaximum(1.0)
        self.slengthmaxvalue_p3.setSingleStep(0.01)
        self.slengthmaxvalue_p3.setProperty("value", 0.1)
        self.slengthmaxvalue_p3.setObjectName("slengthmaxvalue")

        self.label_mp_min = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_min.setGeometry(QtCore.QRect(305, 96, 80, 25))
        self.label_mp_min.setObjectName("label_mp_max")
        self.label_mp_min.setText("Min Values:")
        self.label_mp_min.hide()

        self.slengthminvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p1.setGeometry(QtCore.QRect(397, 96, 55, 25))
        self.slengthminvalue_p1.setMaximum(1.0)
        self.slengthminvalue_p1.setSingleStep(0.01)
        self.slengthminvalue_p1.setProperty("value", 0.01)
        self.slengthminvalue_p1.setObjectName("slengthminvalue")

        self.slengthminvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p2.setGeometry(QtCore.QRect(464, 96, 55, 25))
        self.slengthminvalue_p2.setMaximum(1.0)
        self.slengthminvalue_p2.setSingleStep(0.01)
        self.slengthminvalue_p2.setProperty("value", 0.01)
        self.slengthminvalue_p2.setObjectName("slengthminvalue")

        self.slengthminvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p3.setGeometry(QtCore.QRect(531, 96, 55, 25))
        self.slengthminvalue_p3.setMaximum(1.0)
        self.slengthminvalue_p3.setSingleStep(0.01)
        self.slengthminvalue_p3.setProperty("value", 0.01)
        self.slengthminvalue_p3.setObjectName("slengthminvalue")

        for i in range(1, 4):
            slmax = 'slengthmaxvalue_p' + str(i)
            slmin = 'slengthminvalue_p' + str(i)
            numseg = 'numberofsegs_p' + str(i)
            a = getattr(self, slmax)
            b = getattr(self, slmin)
            c = getattr(self, numseg)
            a.hide()
            b.hide()
            c.hide()
            
        self.label_mp_control.hide()
        self.combobox_plot.hide()
        self.label_mp.hide()
    
        self.tasksperset_p1.hide()
        self.tasksperset_p2.hide()
        self.tasksperset_p3.hide()
        self.numberofsegs_p1.hide()
        self.numberofsegs_p2.hide()
        self.numberofsegs_p3.hide()
        self.label_mp_max.hide()
        self.slengthmaxvalue_p1.hide()
        self.slengthmaxvalue_p2.hide()
        self.slengthmaxvalue_p3.hide()
        self.label_mp_min.hide()
        self.slengthminvalue_p1.hide()
        self.slengthminvalue_p2.hide()
        self.slengthminvalue_p3.hide()
        
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setToolTip('Button to run the settings')
        self.run.setGeometry(QtCore.QRect(812, 610, 200, 25))
        self.run.setObjectName("run")
        self.run.setText("Run")

        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setToolTip('Exit the framework')
        self.exit.setGeometry(QtCore.QRect(12, 610, 200, 25))
        self.exit.setObjectName("exit")
        self.exit.setText("Exit")



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1030, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setText("Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setText("Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.setText("Close")
        self.actionClose.setShortcut("Ctrl+F4")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setText("Quit")
        self.actionFramework_Help = QtWidgets.QAction(MainWindow)
        self.actionFramework_Help.setObjectName("actionFramework_Help")
        self.actionFramework_Help.setText("Framework Help")
        self.actionAbout_Framework = QtWidgets.QAction(MainWindow)
        self.actionAbout_Framework.setObjectName("actionAbout_Framework")
        self.actionAbout_Framework.setText("About Framework")


        def selectionchange(com_b):
            if com_b.currentText() == 'Load Tasksets':
                self.loadtasks_title.show()
                self.tasksetdatapath.show()
            else:
                self.loadtasks_title.hide()
                self.tasksetdatapath.hide()


        def selectionchange_plot( com_b):

            
            if not(self.mp_check.isChecked()):
                self.label_mp_control.hide()
                self.combobox_plot.hide()
                self.label_mp.hide()
            
                self.tasksperset_p1.hide()
                self.tasksperset_p2.hide()
                self.tasksperset_p3.hide()
                self.numberofsegs_p1.hide()
                self.numberofsegs_p2.hide()
                self.numberofsegs_p3.hide()
                self.label_mp_max.hide()
                self.slengthmaxvalue_p1.hide()
                self.slengthmaxvalue_p2.hide()
                self.slengthmaxvalue_p3.hide()
                self.label_mp_min.hide()
                self.slengthminvalue_p1.hide()
                self.slengthminvalue_p2.hide()
                self.slengthminvalue_p3.hide()
            else:
                self.label_mp_control.show()
                self.combobox_plot.show()
                self.label_mp.show()


                if com_b.currentText() =='Suspension Length':
                    self.label_mp_max.show()
                    self.label_mp_min.show()
                    self.label_mp.hide()
                else:
                    self.label_mp_max.hide()
                    self.label_mp_min.hide()
                    self.label_mp.show()
        
                for i in range(1, 4):
                    slmax = 'slengthmaxvalue_p' + str(i)
                    slmin = 'slengthminvalue_p' + str(i)
                    numseg = 'numberofsegs_p' + str(i)
                    numtasks = 'tasksperset_p' + str(i)

                    aslmax = getattr(self, slmax)
                    aslmin = getattr(self, slmin)
                    anums = getattr(self, numseg)
                    anumt = getattr(self, numtasks)
                    if com_b.currentText() == 'Tasks per Set':
                        aslmax.hide()
                        aslmin.hide()
                        anums.hide()
                        anumt.show()
                    elif com_b.currentText() == 'Number of Segments':
                        aslmax.hide()
                        aslmin.hide()
                        anums.show()
                        anumt.hide()
                    elif com_b.currentText() == 'Suspension Length':
                        aslmax.show()
                        aslmin.show()
                        anums.hide()
                        anumt.hide()   

        def clickMethod(self):
            global gPrefixdata
            global gRuntest
            global gPlotdata
            global gNumberOfTaskSets
            global gNumberOfTasksPerSet
            global gUStart
            global gUEnd
            global gUStep
            global gNumberOfSegs
            global gSchemes
            global gSLenMinValue
            global gSLenMaxValue
            global gPlotall
            global gTaskChoice
            global gmpCheck

            del gSchemes[:]
            setSchemes()

            #print(gSchemes)

        def clickexit(self):
            app.quit()

        self.run.clicked.connect(clickMethod)
        self.exit.clicked.connect(clickexit)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def setSchemes():
            global gPrefixdata
            global gTasksetpath
            global gRuntest
            global gPlotdata
            global gNumberOfTaskSets
            global gNumberOfTasksPerSet
            global gUStart
            global gUEnd
            global gUStep
            global gNumberOfSegs
            global gSchemes
            global gSLenMinValue
            global gSLenMaxValue
            global gPlotall
            global gSeed
            global gTaskChoice
            global garwrap
            global gthread

            global gmultiplot
            global gmpCheck

            ###GENERAL###
            gRuntest = self.runtests.isChecked()
            gPlotdata = self.plotdata.isChecked()
            gPlotall = self.plotall.isChecked()
            gTaskChoice = self.combobox_input.currentText()

            gPrefixdata = self.prefixdatapath.text()
            gTasksetpath = self.tasksetdatapath.text()

            ###CONFIGURATION###
            gNumberOfTaskSets = self.tasksetsperconfig.value()
            gNumberOfTasksPerSet = self.tasksperset.value()
            gUStart = self.utilstart.value()
            gUEnd = self.utilend.value()
            gUStep = self.utilstep.value()
            gNumberOfSegs = self.numberofsegs.value()
            gSLenMinValue = self.slengthminvalue.value()
            gSLenMaxValue = self.slengthmaxvalue.value()
            if self.seed.text() != '':
                gSeed = self.seed.text()
            else:
                gSeed = datetime.datetime.now()
            if self.threadcount.text() != '':
                gthread = int(self.threadcount.text())
            else:
                gthread = 1
            ###MultiPlot###
            gmultiplot = self.combobox_plot.currentText()
            if gmultiplot == 'Tasks per Set':
                garwrap = [self.tasksperset_p1.value(), self.tasksperset_p2.value(), self.tasksperset_p3.value()]
            elif gmultiplot == 'Number of Segments':
                garwrap = [self.numberofsegs_p1.value(), self.numberofsegs_p2.value(), self.numberofsegs_p3.value()]
            elif gmultiplot == 'Suspension Length':
                garwrap = [self.slengthminvalue_p1.value(), self.slengthminvalue_p2.value(), self.slengthminvalue_p3.value(),
                           self.slengthmaxvalue_p1.value(), self.slengthmaxvalue_p2.value(), self.slengthmaxvalue_p3.value()]
            gmpCheck = self.mp_check.isChecked()

            #khchen init error window and fill in the concept later
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)

            ###SCHEDULABILITY TESTS###
            if self.seifdamind.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-minD test fails")
                    error_msg.setInformativeText('SEIFDA-minD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-minD-' + str(self.seifdamindg.value()))
            if self.seifdamaxd.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamaxd.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-maxD test fails")
                    error_msg.setInformativeText('SEIFDA-maxD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-maxD-' + str(self.seifdamaxdg.value()))
            if self.seifdapbmind.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdapbmind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-PBminD test fails")
                    error_msg.setInformativeText('SEIFDA-PBminD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-PBminD-' + str(self.seifdapbmindg.value()))
            if self.seifdamip.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamip.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-MILP test fails")
                    error_msg.setInformativeText('SEIFDA-MILP does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-MILP')
            if self.eda.isChecked():
                gSchemes.append('EDA')
            if self.proportional.isChecked():
                gSchemes.append('PROPORTIONAL')
            if self.nc.isChecked():
                if gNumberOfSegs > 2:
                    self.nc.setChecked(False)
                    error_msg = QtWidgets.QMessageBox()
                    error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                    error_msg.setWindowTitle("NC won't work!")
                    error_msg.setInformativeText('Necessary Condition does not work for more than two segements.')
                    #error_msg.setDetailedText("Necessary Condition only works for two segements of computation.")
                    error_msg.exec_()
                else:
                    gSchemes.append('NC')
            if self.biondi.isChecked():
                gSchemes.append('BIONDI')
            if self.passopa.isChecked():
                gSchemes.append('PASS-OPA')
            if self.scedf.isChecked():
                gSchemes.append('SCEDF')
            if self.scrm.isChecked():
                gSchemes.append('SCRM')
            if self.scairrm.isChecked():
                gSchemes.append('SCAIR-RM')
            if self.scairopa.isChecked():
                gSchemes.append('SCAIR-OPA')
            if self.frdgmfopa.isChecked():
                gSchemes.append('FRDGMF-OPA')
            if self.pathminddd.isChecked():
                gSchemes.append('Oblivious-IUB-' + str(self.pathmindddg.value()))
            if self.pathminddnd.isChecked():
                gSchemes.append('Clairvoyant-SSSD-' + str(self.pathminddndg.value()))
            if self.pathpbminddd.isChecked():
                gSchemes.append('Oblivious-MP-' + str(self.pathpbmindddg.value()))
            if self.pathpbminddnd.isChecked():
                gSchemes.append('Clairvoyant-PDAB-' + str(self.pathpbminddndg.value()))
            if self.rss.isChecked():
                gSchemes.append('RSS')
            if self.udledf.isChecked():
                gSchemes.append('UDLEDF')
            if self.wlaedf.isChecked():
                gSchemes.append('WLAEDF')
            if self.rtedf.isChecked():
                gSchemes.append('RTEDF')
            if self.uniframework.isChecked():
                gSchemes.append('UNIFRAMEWORK')
            if self.suspobl.isChecked():
                gSchemes.append('SUSPOBL')
            if self.suspjit.isChecked():
                gSchemes.append('SUSPJIT')
            if self.suspblock.isChecked():
                gSchemes.append('SUSPBLOCK')
            if self.uppaal.isChecked():
                gSchemes.append('UPPAAL')
            if self.gmfpa.isChecked():
                gSchemes.append('GMFPA-' + str(self.gmfpag.value()))
            if self.srsr.isChecked():
                if gNumberOfSegs > 2:
                    self.srsr.setChecked(False)
                    error_msg = QtWidgets.QMessageBox()
                    error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                    error_msg.setWindowTitle("SRSR won't work!")
                    error_msg.setInformativeText('Necessary Condition does not work for more than two segements.')
                    #error_msg.setDetailedText("Necessary Condition only works for two segements of computation.")
                    error_msg.exec_()
                else:
                    gSchemes.append('SRSR')
            if gRuntest:
                #khchen
                if len(gSchemes) != 0:
                    try:
                        tasksets_util = tasksetConfiguration()
                        MainWindow.statusBar().showMessage('Testing the given configurations...')
                        schedulabilityTest(tasksets_util)
                        MainWindow.statusBar().showMessage('Finish')
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no selection to test.')

            if gPlotdata:
                if len(gSchemes) != 0:
                    try:
                        effsstsPlot.effsstsPlotAll(gPrefixdata, gPlotall, gSchemes, gSLenMinValue, gSLenMaxValue, gNumberOfSegs,
                                                   gUStart, gUEnd, gUStep, gNumberOfTasksPerSet)
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no plot to draw.')
            if gmpCheck:
                if len(gSchemes) != 0:
                    try:
                        effsstsPlot.effsstsPlotAllmulti(gPrefixdata, gPlotall, gmultiplot, garwrap, gSchemes, gSLenMinValue, gSLenMaxValue, gNumberOfSegs,
                                                   gUStart, gUEnd, gUStep, gNumberOfTasksPerSet)
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no plot to draw.')

            #MainWindow.statusBar().showMessage('Ready')

def tasksetConfiguration():
    global gNumberOfTaskSets
    global gNumberOfTasksPerSet
    global gUStep
    global gUStart
    global gUEnd
    global gSLenMaxValue
    global gSLenMinValue
    global gNumberOfSegs
    global gSeed

    tasksets_difutil = []

    if gTaskChoice == 'Generate Tasksets' or gTaskChoice == 'Generate and Save Tasksets':
        random.seed(gSeed)
        for u in range(gUStart, gUEnd+gUStep, gUStep):
            tasksets = []
            for _ in range(0, gNumberOfTaskSets):
                #percentageU = u * gUStep / 100
                percentageU = u / 100
                tasks = tgPath.taskGeneration_p(gNumberOfTasksPerSet, percentageU, gSLenMinValue, gSLenMaxValue, vRatio=1,
                                                seed=gSeed, numLog=int(2), numsegs=gNumberOfSegs)
                sortedTasks = sorted(tasks, key=lambda item: item['period'])
                tasksets.append(sortedTasks)
            tasksets_difutil.append(tasksets)
        if gTaskChoice == 'Generate and Save Tasksets':
            file_name = 'Ts-'+ str(gNumberOfTaskSets) + '-Tn-' \
                        + str(gNumberOfTasksPerSet) + '-Ust-' + str(gUStep) +\
                        '-Ssl-' + str(gSLenMinValue) + '-' + \
                        str(gSLenMaxValue) + '-Seg-'+str(gNumberOfSegs)+'-.pkl'
            MainWindow.statusBar().showMessage('File saved as: ' + file_name)
            info = [gNumberOfTaskSets, gNumberOfTasksPerSet, gUStep, gUStart, gUEnd, gSLenMinValue, gSLenMaxValue, gNumberOfSegs, gSeed ]
            with open('./tasksets/saves/'+file_name, 'wb') as f:
                pickle.dump([tasksets_difutil,info] , f)
    elif gTaskChoice == 'Load Tasksets':
        # if len(gTasksetpath) != 0:
        file_name = gTasksetpath
        with open('./tasksets/saves/'+file_name, 'rb') as f:
                data = pickle.load(f)
        tasksets_difutil = data[0]
        info = data[1]
        gNumberOfTaskSets = int(info[0])
        gNumberOfTasksPerSet = int(info[1])
        gUStep = int(info[2])
        gUStart = int(info[3])
        gUEnd = int(info[4])
        gSLenMinValue = float(info[5])
        gSLenMaxValue = float(info[6])
        gNumberOfSegs = int(info[7])
        gSeed = info[8]
    random.seed(gSeed)
    return tasksets_difutil

def schedulabilityTest(Tasksets_util):
    pool = Pool(gthread)
    #sspropotions = ['10']
    #periodlogs = ['2']
    for ischeme in gSchemes:
        x = np.arange(gUStart, gUEnd+gUStep, gUStep)
        #y = np.zeros(int(100 / gUStep) + 1)
        y = np.zeros(int((gUEnd-gUStart) / gUStep)+1)
        print(y)
        ifskip = False
        for u, tasksets in enumerate(Tasksets_util, start=0):  # iterate through taskset
            print("Scheme:", ischeme, "Task-sets:", gNumberOfTaskSets, "Tasks per Set:", gNumberOfTasksPerSet, "U:", gUStart + u * gUStep, "SSLength:", str(
                gSLenMinValue), " - ", str(gSLenMaxValue), "Num. of segments:", gNumberOfSegs)
            if u == 0:
                y[u] = 1
                continue
            if u * gUStep == 100:
                y[u] = 0
                continue
            if ifskip == True:
                print("acceptanceRatio:", 0)
                y[u] = 0
                continue
            
            numfail = 0
            splitTasks = np.array_split(tasksets,gthread)
            results = [pool.apply_async(switchTest, args=(splitTasks[i],ischeme,i,)) for i in range(len(splitTasks))]
            output = [p.get() for p in results]
            numfail = sum(output)

            acceptanceRatio = 1 - (numfail / gNumberOfTaskSets)
            print("acceptanceRatio:", acceptanceRatio)
            y[u] = acceptanceRatio
            if acceptanceRatio == 0:
                ifskip = True

        plotPath = gPrefixdata + '/' + str(gSLenMinValue) + '-' + str(gSLenMaxValue) + '/' + str(gNumberOfSegs) + '/'
        plotfile = gPrefixdata + '/' + str(gSLenMinValue) + '-' + str(gSLenMaxValue) + '/' + str(
            gNumberOfSegs) + '/' + ischeme + str(gNumberOfTasksPerSet)

        if not os.path.exists(plotPath):
            os.makedirs(plotPath)
        np.save(plotfile, np.array([x, y]))
 
def switchTest(tasksets,ischeme,i):
    counter = 0
    for tasks in tasksets:
        if ischeme == 'SCEDF':
            if SCEDF.SC_EDF(tasks) == False:
                counter += 1
        elif ischeme == 'SCRM':
            if SCRM.SC_RM(tasks) == False:
                counter += 1
        elif ischeme == 'PASS-OPA':
            if Audsley.Audsley(tasks,ischeme) == False:
                counter += 1
        elif ischeme == 'SEIFDA-MILP':
            if mipx.mip(tasks) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'SEIFDA':
            if SEIFDA.greedy(tasks, ischeme) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'Oblivious' or ischeme.split('-')[0] == 'Clairvoyant'  :
            if PATH.PATH(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'EDA':
            if EDA.EDA(tasks, gNumberOfSegs) == False:
                counter += 1
        elif ischeme == 'PROPORTIONAL':
            if PROPORTIONAL.PROPORTIONAL(tasks, gNumberOfSegs) == False:
                counter += 1
        elif ischeme == 'NC':
            if NC.NC(tasks) == False:
                counter += 1
        elif ischeme == 'SRSR':
            if SRSR.SRSR(tasks) == False:
                counter += 1
        elif ischeme == 'SCAIR-RM':
            if rad.scair_dm(tasks) == False:
                counter += 1
        elif ischeme == 'SCAIR-OPA':
            if Audsley.Audsley(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'FRDGMF-OPA':
            if Audsley.Audsley(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'BIONDI':
            if Biondi.Biondi(tasks) == False:
                counter += 1
        elif ischeme == 'RSS':
            if RSS.RSS(tasks) == False:
                counter += 1
        elif ischeme == 'UDLEDF':
            if UDLEDF.UDLEDF(tasks) == False:
                counter += 1
        elif ischeme == 'WLAEDF':
            if WLAEDF.WLAEDF(tasks) == False:
                counter += 1
        elif ischeme == 'RTEDF':
            if RTEDF.RTEDF(tasks) == False:
                counter += 1
        elif ischeme == 'UNIFRAMEWORK':
            if UNIFRAMEWORK.UniFramework(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPOBL':
            if FixedPriority.SuspObl(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPJIT':
            if FixedPriority.SuspJit(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPBLOCK':
            if FixedPriority.SuspBlock(tasks) == False:
                counter += 1
        elif ischeme == 'UPPAAL':
            if Uppaal.Uppaal(tasks,i) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'GMFPA':
            if GMFPA.GMFPA(tasks,ischeme) == False:
                counter += 1
        else:
            assert ischeme, 'not vaild ischeme'
    return counter

def evaluate_multiple_tasksets_multiple_schemes(tasksets, ischemes):
    result = [[True if switchTest([taskset],ischeme,0)==0 else False for ischeme in ischemes] for taskset in tasksets]
    #print(result)
    return result

def evaluate_single_taskset_multiple_schemes(taskset, ischemes):
    result = [True if switchTest([taskset],ischeme,0)==0 else False for ischeme in ischemes]
    #print(result)
    return result

def evaluate_single_taskset_single_scheme(taskset, ischeme):
    result = True if switchTest([taskset],ischeme,0)==0 else False
    #print(result)
    return result

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('images/icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #khchen
    MainWindow.statusBar().showMessage('Ready')
    MainWindow.show()
    sys.exit(app.exec_())
