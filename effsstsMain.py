from __future__ import division
from PyQt5 import QtCore, QtGui, QtWidgets
import effssts
import random
import sys
import getopt
import numpy as np
from schedTest import tgPath, SCEDF, EDA, PROPORTIONAL, NC, SEIFDA, Audsley, rad, PATH, mipx, combo, rt
from effsstsPlot import effsstsPlot
import os
import datetime
import cPickle as pickle

gSeed = datetime.datetime.now()
gPrefixdata = ''
gTasksetpath = ''
gRuntest = True
gPlotdata = True
gPlotall = True
gTaskChoice = ''
gTotBucket = 100
gTasksinBkt = 10
gUStart = 0
gUEnd = 100
gUStep = 5
gSSofftypes = 2
gSchemes = []
gMinsstype = 0.01
gMaxsstype = 0.1
gNumberofruns = 1
garwrap = []

gmultiplot = ''
gmpCheck = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        choice_list = ['Generate Tasksets', 'Generate and Save Tasksets', 'Load Tasksets']
        choice_plot = ['Tasks per set', 'Number of Segments', 'Suspension Length']
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(11, 11, 925, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.prefixdatapath = QtWidgets.QLineEdit(self.groupBox_2)
        self.prefixdatapath.setGeometry(QtCore.QRect(131, 60, 391, 20))
        self.prefixdatapath.setObjectName("prefixdatapath")
        self.seed = QtWidgets.QLineEdit(self.groupBox_2)
        self.seed.setGeometry(QtCore.QRect(601, 60, 40, 20))
        self.seed.setObjectName("seed")
        self.runtests = QtWidgets.QCheckBox(self.groupBox_2)
        self.runtests.setGeometry(QtCore.QRect(12, 23, 90, 17))
        self.runtests.setChecked(True)
        self.runtests.setObjectName("runtests")
        self.plotdata = QtWidgets.QCheckBox(self.groupBox_2)
        self.plotdata.setGeometry(QtCore.QRect(110, 23, 100, 17))
        self.plotdata.setChecked(True)
        self.plotdata.setObjectName("plotdata")
        self.plotall = QtWidgets.QCheckBox(self.groupBox_2)
        self.plotall.setGeometry(QtCore.QRect(202, 23, 70, 17))
        self.plotall.setChecked(True)
        self.plotall.setObjectName("plotall")
        self.combobox_input = QtWidgets.QComboBox(self.groupBox_2)
        self.combobox_input.setGeometry(QtCore.QRect(12, 100, 215, 17))
        self.combobox_input.setObjectName("combobox_input")
        self.combobox_input.addItems(choice_list)
        self.combobox_input.currentIndexChanged.connect(lambda: selectionchange(self.combobox_input))


        self.tasksetdatapath = QtWidgets.QLineEdit(self.groupBox_2)
        self.tasksetdatapath.setGeometry(QtCore.QRect(375, 100, 480, 20))
        self.tasksetdatapath.setObjectName("tasksetdatapath")
        self.tasksetdatapath.hide()
        self.loadtasks_title = QtWidgets.QLabel(self.groupBox_2)
        self.loadtasks_title.setGeometry(QtCore.QRect(235, 100, 150, 16))
        self.loadtasks_title.setObjectName("loadtasks_title")
        self.loadtasks_title.hide()
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(12, 60, 150, 16))
        self.label_5.setObjectName("label_5")

        #khchen
        self.label_seed = QtWidgets.QLabel(self.groupBox_2)
        self.label_seed.setGeometry(QtCore.QRect(560, 60, 43, 16))
        self.label_seed.setObjectName("label_seed")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 150, 925, 81))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(15, 23, 220, 18))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(15, 53, 220, 18))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(267, 23, 150, 18))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(267, 53, 150, 18))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(440, 53, 160, 18)) #num_of_segment
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(440, 23, 130, 18))
        self.label_11.setObjectName("label_11")
        self.utilstep = QtWidgets.QSpinBox(self.groupBox_3)
        self.utilstep.setGeometry(QtCore.QRect(595, 23, 43, 20))
        self.utilstep.setMaximum(100)
        self.utilstep.setProperty("value", 5)
        self.utilstep.setObjectName("utilstep")
        self.tasksetsperconfig = QtWidgets.QSpinBox(self.groupBox_3)
        self.tasksetsperconfig.setGeometry(QtCore.QRect(208, 23, 50, 20))
        self.tasksetsperconfig.setMaximum(100)
        self.tasksetsperconfig.setProperty("value", 100)
        self.tasksetsperconfig.setObjectName("tasksetsperconfig")
        self.tasksperset = QtWidgets.QSpinBox(self.groupBox_3)
        self.tasksperset.setGeometry(QtCore.QRect(208, 53, 50, 20))
        self.tasksperset.setMaximum(100)
        self.tasksperset.setProperty("value", 10)
        self.tasksperset.setObjectName("tasksperset")
        self.utilstart = QtWidgets.QSpinBox(self.groupBox_3)
        self.utilstart.setGeometry(QtCore.QRect(380, 23, 50, 20))
        self.utilstart.setMaximum(100)
        self.utilstart.setProperty("value", 0)
        self.utilstart.setObjectName("utilstart")
        self.utilend = QtWidgets.QSpinBox(self.groupBox_3)
        self.utilend.setGeometry(QtCore.QRect(380, 53, 50, 20)) #util end value
        self.utilend.setMaximum(100)
        self.utilend.setProperty("value", 100)
        self.utilend.setObjectName("utilend")
        self.numberofsegs = QtWidgets.QSpinBox(self.groupBox_3)
        self.numberofsegs.setGeometry(QtCore.QRect(595, 53, 43, 20))
        self.numberofsegs.setMaximum(100)
        self.numberofsegs.setProperty("value", 2)
        self.numberofsegs.setObjectName("numberofsegs")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(650, 23, 210, 20))
        self.label.setObjectName("label")
        self.slengthmaxvalue = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.slengthmaxvalue.setGeometry(QtCore.QRect(860, 53, 50, 20))
        self.slengthmaxvalue.setMaximum(1.0)
        self.slengthmaxvalue.setSingleStep(0.01)
        self.slengthmaxvalue.setProperty("value", 0.1)
        self.slengthmaxvalue.setObjectName("slengthmaxvalue")
        self.slengthminvalue = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.slengthminvalue.setGeometry(QtCore.QRect(860, 23, 50, 20))
        self.slengthminvalue.setMaximum(1.0)
        self.slengthminvalue.setSingleStep(0.01)
        self.slengthminvalue.setProperty("value", 0.01)
        self.slengthminvalue.setObjectName("slengthminvalue")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(650, 53, 210, 18)) #suspension length max
        self.label_3.setObjectName("label_3")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setToolTip('Button to run the settings')
        self.run.setGeometry(QtCore.QRect(860, 570, 75, 23))
        self.run.setObjectName("run")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setToolTip('Exit the framework')
        self.exit.setGeometry(QtCore.QRect(770, 570, 75, 23))
        self.exit.setObjectName("exit")
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget) #Schedulability tests
        self.groupBox_7.setGeometry(QtCore.QRect(10, 240, 925, 203))
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_7) #General
        self.groupBox_6.setGeometry(QtCore.QRect(795, 20, 81, 175))
        self.groupBox_6.setObjectName("groupBox_6")
        self.nc = QtWidgets.QCheckBox(self.groupBox_6)
        self.nc.setGeometry(QtCore.QRect(10, 25, 47, 17))
        self.nc.setObjectName("nc")
        self.nc.setToolTip('Necessary Condition')

        self.groupBox = QtWidgets.QGroupBox(self.groupBox_7)  #FRD Hybrid
        self.groupBox.setGeometry(QtCore.QRect(235, 21, 211, 175))
        self.groupBox.setObjectName("groupBox")
        self.pathminddndg = QtWidgets.QSpinBox(self.groupBox)
        self.pathminddndg.setGeometry(QtCore.QRect(160, 50, 31, 20))
        self.pathminddndg.setMaximum(5)
        self.pathminddndg.setProperty("value", 1)
        self.pathminddndg.setObjectName("pathminddndg")
        self.pathminddd = QtWidgets.QCheckBox(self.groupBox)
        self.pathminddd.setGeometry(QtCore.QRect(7, 25, 127, 17))
        self.pathminddd.setObjectName("pathminddd")
        self.pathminddd.setToolTip('Pattern Oblivious Individual Upper Bounds')
        self.pathmindddg = QtWidgets.QSpinBox(self.groupBox)
        self.pathmindddg.setGeometry(QtCore.QRect(160, 25, 31, 20))
        self.pathmindddg.setMaximum(5)
        self.pathmindddg.setProperty("value", 1)
        self.pathmindddg.setObjectName("pathmindddg")
        self.pathminddnd = QtWidgets.QCheckBox(self.groupBox)
        self.pathminddnd.setGeometry(QtCore.QRect(7, 50, 137, 17))
        self.pathminddnd.setObjectName("pathminddnd")
        self.pathminddnd.setToolTip('Pattern-Clairvoyant Shorter Segment Shorter Deadline')
        self.pathpbminddndg = QtWidgets.QSpinBox(self.groupBox)
        self.pathpbminddndg.setGeometry(QtCore.QRect(160, 100, 31, 20))
        self.pathpbminddndg.setMaximum(5)
        self.pathpbminddndg.setProperty("value", 1)
        self.pathpbminddndg.setObjectName("pathpbminddndg")
        self.pathpbminddd = QtWidgets.QCheckBox(self.groupBox)
        self.pathpbminddd.setGeometry(QtCore.QRect(7, 75, 137, 17))
        self.pathpbminddd.setObjectName("pathpbminddd")
        self.pathpbminddd.setToolTip('Pattern-Oblivious Multiple Paths')
        self.pathpbmindddg = QtWidgets.QSpinBox(self.groupBox)
        self.pathpbmindddg.setGeometry(QtCore.QRect(160, 75, 31, 20))
        self.pathpbmindddg.setMaximum(5)
        self.pathpbmindddg.setProperty("value", 1)
        self.pathpbmindddg.setObjectName("pathpbmindddg")
        self.pathpbminddnd = QtWidgets.QCheckBox(self.groupBox)
        self.pathpbminddnd.setGeometry(QtCore.QRect(7, 100, 148, 17))
        self.pathpbminddnd.setObjectName("pathpbminddnd")
        self.pathpbminddnd.setToolTip('Pattern-Clairvoyant Proportional Deadline with A Bias')

        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_7) #Segmented
        self.groupBox_4.setGeometry(QtCore.QRect(455, 21, 181, 175))
        self.groupBox_4.setObjectName("groupBox_4")
        self.scedf = QtWidgets.QCheckBox(self.groupBox_4)
        self.scedf.setGeometry(QtCore.QRect(10, 75, 75, 17))
        self.scedf.setObjectName("scedf")
        self.scedf.setToolTip('Suspension as Computation Earliest-Deadline-First (SCEDF)')
        self.scrm = QtWidgets.QCheckBox(self.groupBox_4)
        self.scrm.setGeometry(QtCore.QRect(10, 100, 61, 17))
        self.scrm.setObjectName("scrm")
        self.scrm.setToolTip('Suspension as Computation Rate-Monotonic (SCRM)')
        self.scairrm = QtWidgets.QCheckBox(self.groupBox_4)
        self.scairrm.setGeometry(QtCore.QRect(10, 25, 93, 17))
        self.scairrm.setObjectName("scairrm")
        self.scairrm.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Rate-Monotonic (RM)')
        self.scairopa = QtWidgets.QCheckBox(self.groupBox_4)
        self.scairopa.setGeometry(QtCore.QRect(10, 50, 99, 17))
        self.scairopa.setObjectName("scairopa")
        self.scairopa.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Optimal Priority Assignment (OPA) ')
        self.biondi = QtWidgets.QCheckBox(self.groupBox_4)
        self.biondi.setGeometry(QtCore.QRect(10, 125, 160, 17))
        self.biondi.setObjectName("Biondi")
        self.biondi.setToolTip('Alessandros Method. Biondi (RTSS 2016)')

        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_7) #FRD Segmented
        self.groupBox_5.setGeometry(QtCore.QRect(12, 21, 216, 175))
        self.groupBox_5.setObjectName("groupBox_5")
        self.proportional = QtWidgets.QCheckBox(self.groupBox_5)
        self.proportional.setGeometry(QtCore.QRect(20, 125, 140, 17))
        self.proportional.setObjectName("proportional")
        self.proportional.setToolTip('Proportional relative deadline assignment')
        self.seifdamaxdg = QtWidgets.QSpinBox(self.groupBox_5)
        self.seifdamaxdg.setGeometry(QtCore.QRect(165, 50, 31, 20))
        self.seifdamaxdg.setMaximum(5)
        self.seifdamaxdg.setProperty("value", 1)
        self.seifdamaxdg.setObjectName("seifdamaxdg")
        self.seifdamind = QtWidgets.QCheckBox(self.groupBox_5)
        self.seifdamind.setGeometry(QtCore.QRect(20, 25, 170, 17))
        self.seifdamind.setObjectName("seifdamind")
        self.seifdamind.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the minimum x')
        self.seifdamip = QtWidgets.QCheckBox(self.groupBox_5)
        self.seifdamip.setGeometry(QtCore.QRect(20, 150, 170, 17))
        self.seifdamip.setObjectName("seifdamip")
        self.seifdamip.setToolTip('Shortest Execution Interval First Deadline Assignment - MILP')
        self.seifdamaxd = QtWidgets.QCheckBox(self.groupBox_5)
        self.seifdamaxd.setGeometry(QtCore.QRect(20, 50, 170, 17))
        self.seifdamaxd.setObjectName("seifdamaxd")
        self.seifdamaxd.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the maximum x')
        self.seifdapbmindg = QtWidgets.QSpinBox(self.groupBox_5)
        self.seifdapbmindg.setGeometry(QtCore.QRect(165, 75, 31, 20))
        self.seifdapbmindg.setMaximum(5)
        self.seifdapbmindg.setProperty("value", 1)
        self.seifdapbmindg.setObjectName("seifdapbmindg")
        self.seifdamindg = QtWidgets.QSpinBox(self.groupBox_5)
        self.seifdamindg.setGeometry(QtCore.QRect(165, 25, 31, 20))
        self.seifdamindg.setMaximum(5)
        self.seifdamindg.setProperty("value", 1)
        self.seifdamindg.setObjectName("seifdamindg")
        self.seifdapbmind = QtWidgets.QCheckBox(self.groupBox_5)
        self.seifdapbmind.setGeometry(QtCore.QRect(20, 75, 140, 17))
        self.seifdapbmind.setObjectName("seifdapbmind")
        self.seifdapbmind.setToolTip('Shortest Execution Interval First Deadline Assignment - Proportionally-Bounded-Min x')
        self.eda = QtWidgets.QCheckBox(self.groupBox_5)
        self.eda.setGeometry(QtCore.QRect(20, 100, 50, 17))
        self.eda.setObjectName("eda")
        self.eda.setToolTip('Equal relative Deadline Assignment (EDA)') #Dynamic
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_8.setGeometry(QtCore.QRect(645, 20, 141, 175))
        self.groupBox_8.setObjectName("groupBox_8")
        self.passopa = QtWidgets.QCheckBox(self.groupBox_8)
        self.passopa.setGeometry(QtCore.QRect(10, 25, 103, 17))
        self.passopa.setObjectName("passopa")
        self.passopa.setToolTip('Priority Assignment algorithm for Self-Suspending Systems - Optimal-Priority Assignment')

        self.groupBox_multiplot = QtWidgets.QGroupBox(self.centralwidget)  # multi plot
        self.groupBox_multiplot.setGeometry(QtCore.QRect(10, 446, 925, 120))
        self.groupBox_multiplot.setObjectName("groupBox_multiplot")
        self.combobox_plot = QtWidgets.QComboBox(self.groupBox_multiplot)
        self.combobox_plot.setGeometry(QtCore.QRect(150, 58, 240, 25))
        self.combobox_plot.setObjectName("combobox_plot")
        self.combobox_plot.addItems(choice_plot)
        self.combobox_plot.currentIndexChanged.connect(lambda: selectionchange_plot(self.combobox_plot))

        self.label_mp = QtWidgets.QLabel(self.groupBox_multiplot)
        self.label_mp.setGeometry(QtCore.QRect(400, 58, 70, 20))
        self.label_mp.setObjectName("label_mp")
        self.label_mp_control = QtWidgets.QLabel(self.groupBox_multiplot)
        self.label_mp_control.setGeometry(QtCore.QRect(12, 58, 130, 20))
        self.label_mp_control.setObjectName("label_mp")

        self.tasksperset_p1 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.tasksperset_p1.setGeometry(QtCore.QRect(460, 58, 50, 20))
        self.tasksperset_p1.setMaximum(100)
        self.tasksperset_p1.setProperty("value", 10)
        self.tasksperset_p1.setObjectName("tasksperset")
        self.tasksperset_p2 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.tasksperset_p2.setGeometry(QtCore.QRect(520, 58, 50, 20))
        self.tasksperset_p2.setMaximum(100)
        self.tasksperset_p2.setProperty("value", 10)
        self.tasksperset_p2.setObjectName("tasksperset")
        self.tasksperset_p3 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.tasksperset_p3.setGeometry(QtCore.QRect(580, 58, 50, 20))
        self.tasksperset_p3.setMaximum(100)
        self.tasksperset_p3.setProperty("value", 10)
        self.tasksperset_p3.setObjectName("tasksperset")

        self.numberofsegs_p1 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.numberofsegs_p1.setGeometry(QtCore.QRect(460, 58, 50, 20))
        self.numberofsegs_p1.setMaximum(100)
        self.numberofsegs_p1.setProperty("value", 2)
        self.numberofsegs_p1.setObjectName("numberofsegs")
        self.numberofsegs_p2 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.numberofsegs_p2.setGeometry(QtCore.QRect(520, 58, 50, 20))
        self.numberofsegs_p2.setMaximum(100)
        self.numberofsegs_p2.setProperty("value", 2)
        self.numberofsegs_p2.setObjectName("numberofsegs")
        self.numberofsegs_p3 = QtWidgets.QSpinBox(self.groupBox_multiplot)
        self.numberofsegs_p3.setGeometry(QtCore.QRect(580, 58, 50, 20))
        self.numberofsegs_p3.setMaximum(100)
        self.numberofsegs_p3.setProperty("value", 2)
        self.numberofsegs_p3.setObjectName("numberofsegs")

        self.slengthmaxvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthmaxvalue_p1.setGeometry(QtCore.QRect(485, 58, 55, 20))
        self.slengthmaxvalue_p1.setMaximum(1.0)
        self.slengthmaxvalue_p1.setSingleStep(0.01)
        self.slengthmaxvalue_p1.setProperty("value", 0.1)
        self.slengthmaxvalue_p1.setObjectName("slengthmaxvalue")
        self.slengthmaxvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthmaxvalue_p2.setGeometry(QtCore.QRect(545, 58, 55, 20))
        self.slengthmaxvalue_p2.setMaximum(1.0)
        self.slengthmaxvalue_p2.setSingleStep(0.01)
        self.slengthmaxvalue_p2.setProperty("value", 0.1)
        self.slengthmaxvalue_p2.setObjectName("slengthmaxvalue")
        self.slengthmaxvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthmaxvalue_p3.setGeometry(QtCore.QRect(605, 58, 55, 20))
        self.slengthmaxvalue_p3.setMaximum(1.0)
        self.slengthmaxvalue_p3.setSingleStep(0.01)
        self.slengthmaxvalue_p3.setProperty("value", 0.1)
        self.slengthmaxvalue_p3.setObjectName("slengthmaxvalue")
        self.label_mp_max = QtWidgets.QLabel(self.groupBox_multiplot)
        self.label_mp_max.setGeometry(QtCore.QRect(400, 58, 140, 20))
        self.label_mp_max.setObjectName("label_mp_max")
        self.label_mp_min = QtWidgets.QLabel(self.groupBox_multiplot)
        self.label_mp_min.setGeometry(QtCore.QRect(400, 88, 140, 20))
        self.label_mp_min.setObjectName("label_mp_max")
        self.label_mp_max.hide()
        self.label_mp_min.hide()

        self.slengthminvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthminvalue_p1.setGeometry(QtCore.QRect(485, 88, 55, 20))
        self.slengthminvalue_p1.setMaximum(1.0)
        self.slengthminvalue_p1.setSingleStep(0.01)
        self.slengthminvalue_p1.setProperty("value", 0.01)
        self.slengthminvalue_p1.setObjectName("slengthminvalue")
        self.slengthminvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthminvalue_p2.setGeometry(QtCore.QRect(545, 88, 55, 20))
        self.slengthminvalue_p2.setMaximum(1.0)
        self.slengthminvalue_p2.setSingleStep(0.01)
        self.slengthminvalue_p2.setProperty("value", 0.01)
        self.slengthminvalue_p2.setObjectName("slengthminvalue")
        self.slengthminvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupBox_multiplot)
        self.slengthminvalue_p3.setGeometry(QtCore.QRect(605, 88, 55, 20))
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

        self.mp_check = QtWidgets.QCheckBox(self.groupBox_multiplot)
        self.mp_check.setGeometry(QtCore.QRect(12, 28, 150, 20))
        self.mp_check.setObjectName("mp_check")
        self.mp_check.setToolTip('Multiple Plot')

        #khchen
        self.combosjsb = QtWidgets.QCheckBox(self.groupBox_8)
        self.combosjsb.setGeometry(QtCore.QRect(10, 50, 113, 17))
        self.combosjsb.setObjectName("combosjsb")
        self.combosjsb.setToolTip('Combining Jitter and Blocking')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionFramework_Help = QtWidgets.QAction(MainWindow)
        self.actionFramework_Help.setObjectName("actionFramework_Help")
        self.actionAbout_Framework = QtWidgets.QAction(MainWindow)
        self.actionAbout_Framework.setObjectName("actionAbout_Framework")



        def clickMethod(self):
            global gPrefixdata
            global gRuntest
            global gPlotdata
            global gTotBucket
            global gTasksinBkt
            global gUStart
            global gUEnd
            global gUStep
            global gSSofftypes
            global gSchemes
            global gMinsstype
            global gMaxsstype
            global gPlotall
            global gTaskChoice
            global gmpCheck

            del gSchemes[:]
            setSchemes()

            #print gSchemes


        def selectionchange(com_b):
            if com_b.currentText() == 'Load Tasksets':
                self.loadtasks_title.show()
                self.tasksetdatapath.show()
            else:
                self.loadtasks_title.hide()
                self.tasksetdatapath.hide()


        def selectionchange_plot( com_b):
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
                if com_b.currentText() == 'Tasks per set':
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




        def clickexit(self):
            app.quit()

        self.run.clicked.connect(clickMethod)
        self.exit.clicked.connect(clickexit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def setSchemes():
            global gPrefixdata
            global gTasksetpath
            global gRuntest
            global gPlotdata
            global gTotBucket
            global gTasksinBkt
            global gUStart
            global gUEnd
            global gUStep
            global gSSofftypes
            global gSchemes
            global gMinsstype
            global gMaxsstype
            global gPlotall
            global gSeed
            global gTaskChoice
            global garwrap

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
            gTotBucket = self.tasksetsperconfig.value()
            gTasksinBkt = self.tasksperset.value()
            gUStart = self.utilstart.value()
            gUEnd = self.utilend.value()
            gUStep = self.utilstep.value()
            gSSofftypes = self.numberofsegs.value()
            gMinsstype = self.slengthminvalue.value()
            gMaxsstype = self.slengthmaxvalue.value()
            if self.seed.text() != '':
                gSeed = self.seed.text()
            else:
                gSeed = datetime.datetime.now()
            ###MultiPlot###
            gmultiplot = self.combobox_plot.currentText()
            if gmultiplot == 'Tasks per set':
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
                if gSSofftypes > 2:
                    self.seifdamind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-minD test fails")
                    error_msg.setInformativeText('SEIFDA-minD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-minD-' + str(self.seifdamindg.value()))
            if self.seifdamaxd.isChecked():
                if gSSofftypes > 2:
                    self.seifdamaxd.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-maxD test fails")
                    error_msg.setInformativeText('SEIFDA-maxD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-maxD-' + str(self.seifdamaxdg.value()))
            if self.seifdapbmind.isChecked():
                if gSSofftypes > 2:
                    self.seifdapbmind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-PBminD test fails")
                    error_msg.setInformativeText('SEIFDA-PBminD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-PBminD-' + str(self.seifdapbmindg.value()))
            if self.seifdamip.isChecked():
                if gSSofftypes > 2:
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
                if gSSofftypes > 2:
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
                gSchemes.append('Biondi')
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
            if self.pathminddd.isChecked():
                gSchemes.append(
                    'PATH-minD-' + str(self.pathmindddg.value()) + '-D=D')
            if self.pathminddnd.isChecked():
                gSchemes.append(
                    'PATH-minD-' + str(self.pathminddndg.value()) + '-DnD')
            if self.pathpbminddd.isChecked():
                gSchemes.append('PATH-PBminD-' + str(self.pathpbmindddg.value()) + '-D=D')
            if self.pathpbminddnd.isChecked():
                gSchemes.append('PATH-PBminD-' + str(self.pathpbminddndg.value()) + '-DnD')
            #khchen Combo-SJSB
            if self.combosjsb.isChecked():
                gSchemes.append('Combo-SJSB')

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
                        effsstsPlot.effsstsPlotAll(gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype, gSSofftypes,
                                                   gUStart, gUEnd, gUStep, gTasksinBkt, gmpCheck, gmultiplot, garwrap)
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no plot to draw.')

            #MainWindow.statusBar().showMessage('Ready')


        def tasksetConfiguration():
            global gTotBucket
            global gTasksinBkt
            global gUStep
            global gMaxsstype
            global gMinsstype
            global gSSofftypes
            global gSeed

            tasksets_difutil = []

            
            random.seed(gSeed)

            if gTaskChoice == 'Generate Tasksets' or gTaskChoice == 'Generate and Save Tasksets':
                y = np.zeros(int(100 / gUStep) + 1)
                for u in xrange(0, len(y), 1):
                    tasksets = []
                    for i in xrange(0, gTotBucket, 1):
                        percentageU = u * gUStep / 100
                        tasks = tgPath.taskGeneration_p(gTasksinBkt, percentageU, gMinsstype, gMaxsstype, vRatio=1,
                                                        seed=gSeed, numLog=int(2), numsegs=gSSofftypes)
                        sortedTasks = sorted(tasks, key=lambda item: item['period'])
                        tasksets.append(sortedTasks)
                    tasksets_difutil.append(tasksets)

                if gTaskChoice == 'Generate and Save Tasksets':
                    file_name = 'TspCon_'+ str(gTotBucket) + '_TpTs_' \
                                + str(gTasksinBkt) + '_Utilst_' + str(gUStep) +\
                                '_Minss_' + str(gMinsstype) + '_Maxss_' + \
                                str(gMaxsstype) + '_Seg_'+str(gSSofftypes)+'_.pkl'
                    MainWindow.statusBar().showMessage('File saved as: ' + file_name)
                    info = [gTotBucket, gTasksinBkt, gUStep, gMinsstype, gMaxsstype, gSSofftypes, gSeed ]
                    with open('./genTasksets/'+file_name, 'wb') as f:
                        pickle.dump([tasksets_difutil,info] , f)

            elif gTaskChoice == 'Load Tasksets':
                # if len(gTasksetpath) != 0:
                file_name = gTasksetpath
                with open('./genTasksets/'+file_name, 'rb') as f:
                     data = pickle.load(f)
                tasksets_difutil = data[0]
                info = data[1]
                gTotBucket = int(info[0])
                gTasksinBkt = int(info[1])
                gUStep = int(info[2])
                gMinsstype = float(info[3])
                gMaxsstype = float(info[4])
                gSSofftypes = int(info[5])
                gSeed = info[6]

            return tasksets_difutil



        def schedulabilityTest(Tasksets_util):
            sspropotions = ['10']
            periodlogs = ['2']
            for ischeme in gSchemes:
                x = np.arange(0, int(100 / gUStep) + 1)
                y = np.zeros(int(100 / gUStep) + 1)
                ifskip = False
                for u, tasksets in enumerate(Tasksets_util, start=0):  # iterate through taskset
                    print "Scheme:", ischeme, "Task-sets:", gTotBucket, "Tasks per set:", gTasksinBkt, "U:", u * gUStep, "SSLength:", str(
                        gMinsstype), " - ", str(gMaxsstype), "Num. of segments:", gSSofftypes
                    if u == 0:
                        y[u] = 1
                        continue
                    if u * gUStep == 100:
                        y[u] = 0
                        continue
                    numfail = 0
                    if ifskip == True:
                        print "acceptanceRatio:", 0
                        y[u] = 0
                        continue

                    for tasks in tasksets:  # iterate for each taskset
                        if ischeme == 'SCEDF':
                            if SCEDF.SC_EDF(tasks) == False:
                                numfail += 1
                        elif ischeme == 'SCRM':
                            if SEIFDA.SC_RM(tasks) == False:
                                numfail += 1
                        elif ischeme == 'PASS-OPA':
                            if Audsley.Audsley(tasks) == False:
                                numfail += 1
                        elif ischeme == 'SEIFDA-MILP':
                            if mipx.mip(tasks) == False:
                                numfail += 1
                        elif ischeme.split('-')[0] == 'SEIFDA':
                            if SEIFDA.greedy(tasks, ischeme) == False:
                                numfail += 1
                        elif ischeme.split('-')[0] == 'PATH':
                            if PATH.PATH(tasks, ischeme) == False:
                                numfail += 1
                        elif ischeme == 'EDA':
                            if EDA.EDA(tasks, gSSofftypes) == False:
                                numfail += 1
                        elif ischeme == 'PROPORTIONAL':
                            if PROPORTIONAL.PROPORTIONAL(tasks, gSSofftypes) == False:
                                numfail += 1
                        elif ischeme == 'NC':
                            if NC.NC(tasks) == False:
                                numfail += 1
                        elif ischeme == 'SCAIR-RM':
                            if rad.scair_dm(tasks) == False:
                                numfail += 1
                        elif ischeme == 'SCAIR-OPA':
                            if rad.Audsley(tasks, ischeme) == False:  # sorted tasks
                                numfail += 1
                        elif ischeme == 'Biondi':
                            if rt.Biondi(tasks) == False:
                                numfail += 1
                        # khchen
                        elif ischeme == 'Combo-SJSB':
                            if combo.sjsb(tasks) == False:  # sorted tasks
                                numfail += 1
                        elif ischeme == 'Combo-SJSB':
                            if combo.sjsb(tasks) == False:  # sorted tasks
                                numfail += 1
                        else:
                            assert ischeme, 'not vaild ischeme'

                    acceptanceRatio = 1 - (numfail / gTotBucket)
                    print "acceptanceRatio:", acceptanceRatio
                    y[u] = acceptanceRatio
                    if acceptanceRatio == 0:
                        ifskip = True

                plotPath = gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype) + '/' + str(gSSofftypes) + '/'
                plotfile = gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype) + '/' + str(
                    gSSofftypes) + '/' + ischeme + str(gTasksinBkt)

                if not os.path.exists(plotPath):
                    os.makedirs(plotPath)

                np.save(plotfile, np.array([x, y]))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Evaluation Framework for Self-Suspending Task Systems"))
        self.groupBox_2.setTitle(_translate("MainWindow", "General"))
        self.prefixdatapath.setText(_translate("MainWindow", "effsstsPlot/Data"))
        self.tasksetdatapath.setText(_translate("MainWindow", "TspCon_100_TpTs_10_Utilst_5_Minss_0.01_Maxss_0.1_Seg_2_.pkl"))
        self.runtests.setText(_translate("MainWindow", "Run Tests"))
        self.plotdata.setText(_translate("MainWindow", "Plot Data"))
        self.plotall.setText(_translate("MainWindow", "Plot All"))
        self.label_5.setText(_translate("MainWindow", "Prefix Data Path:"))
        self.loadtasks_title.setText(_translate("MainWindow", "Tasksets File Name:"))
        #khchen
        self.label_seed.setText(_translate("MainWindow", "Seed:"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Configurations"))
        self.label_6.setText(_translate("MainWindow", "Task Sets per Configuration:"))
        self.label_7.setText(_translate("MainWindow", "Tasks per Set:"))
        self.label_8.setText(_translate("MainWindow", "Utilization Start:"))
        self.label_9.setText(_translate("MainWindow", "Utilization End:"))
        self.label_10.setText(_translate("MainWindow", "Number of Segments:"))
        self.label_11.setText(_translate("MainWindow", "Utilization Step:"))
        self.label.setText(_translate("MainWindow", "Suspension Length Min Value:"))
        self.label_3.setText(_translate("MainWindow", "Suspension Length Max Value:"))
        self.run.setText(_translate("MainWindow", "Run"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Schedulability tests"))
        self.groupBox_multiplot.setTitle(_translate("MainWindow", "Multiple plots"))
        self.groupBox_6.setTitle(_translate("MainWindow", "General"))
        self.nc.setText(_translate("MainWindow", "NC"))
        self.biondi.setText(_translate("MainWindow", "Biondi RTSS 16"))
        self.groupBox.setTitle(_translate("MainWindow", "FRD Hybrid"))
        self.pathminddd.setText(_translate("MainWindow", "Oblivious-IUB"))
        self.pathminddnd.setText(_translate("MainWindow", "Clairvoyant-SSSD"))
        self.pathpbminddd.setText(_translate("MainWindow", "Oblivious-MP"))
        self.pathpbminddnd.setText(_translate("MainWindow", "Clairvoyant-PDAB"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Segmented"))
        self.scedf.setText(_translate("MainWindow", "SCEDF"))
        self.scrm.setText(_translate("MainWindow", "SCRM"))
        self.scairrm.setText(_translate("MainWindow", "SCAIR-RM"))
        self.combosjsb.setText(_translate("MainWindow", "Combo-SJSB"))
        self.seifdamip.setText(_translate("MainWindow", "SEIFDA-MILP"))
        self.scairopa.setText(_translate("MainWindow", "SCAIR-OPA"))
        self.groupBox_5.setTitle(_translate("MainWindow", "FRD Segmented"))
        self.proportional.setText(_translate("MainWindow", "Proportional"))
        self.seifdamind.setText(_translate("MainWindow", "SEIFDA-minD-"))
        self.seifdamaxd.setText(_translate("MainWindow", "SEIFDA-maxD-"))
        self.seifdapbmind.setText(_translate("MainWindow", "SEIFDA-PBminD-"))
        self.eda.setText(_translate("MainWindow", "EDA"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Dynamic"))
        self.label_mp.setText(_translate("MainWindow", "Values:"))
        self.label_mp_control.setText(_translate("MainWindow", "Control Parameter:"))
        self.label_mp_min.setText(_translate("MainWindow", "Min Values:"))
        self.label_mp_max.setText(_translate("MainWindow", "Max Values:"))
        self.mp_check.setText(_translate("MainWindow", "Multiple Plots"))
        self.passopa.setText(_translate("MainWindow", "PASS-OPA"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+F4"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionFramework_Help.setText(_translate("MainWindow", "Framework Help"))
        self.actionAbout_Framework.setText(_translate("MainWindow", "About Framework"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #khchen
    MainWindow.statusBar().showMessage('Ready')
    MainWindow.show()
    sys.exit(app.exec_())
