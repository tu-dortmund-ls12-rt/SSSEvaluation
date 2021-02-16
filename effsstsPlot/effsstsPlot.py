from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math

def pickColor(ischeme):
    color = ''
    if ischeme == 'EDA':
        color = '#000000'
    elif ischeme == 'PROPORTIONAL':
        color = '#800000'
    elif ischeme == 'PASS-OPA':
        color = '#000080'
    elif ischeme == 'SCEDF':
        color = '#808000'
    elif ischeme == 'SCRM':
        color = '#FF69B4'
    elif ischeme == 'SCAIR':
        color = '#008000'
    elif ischeme == 'MIP':
        color = '#42F4AA'
    elif ischeme == 'SCAIR-RM':
        color = '#A742F4'
    elif ischeme == 'SCAIR-OPA':
        color = '#C97089'
    elif ischeme == 'Combo-SJSB':
        color = '#B93049'
    elif ischeme == 'RSS':
        color = '#816000'
    elif ischeme == 'UDLEDF':
        color = '#824000'
    elif ischeme == 'WLAEDF':
        color = '#832000'
    elif ischeme.__contains__('SEIFDA-minD'):
        color = '#0000FF'
    elif ischeme.__contains__('SEIFDA-PBminD'):
        color = '#BC4968'
    elif ischeme.__contains__('SEIFDA-maxD'):
        color = '#00FFFF'
    elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('DnD'):
        color = '#808080'
    elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('D=D'):
        color = '#FF0000'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('DnD'):
        color = '#800080'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('D=D'):
        color = '#00FF00'
    else:
        color = '#008080'
    return color

def pickMarker(ischeme):
    marker = ''
    if ischeme == 'EDA':
        marker = 's'
    elif ischeme == 'PROPORTIONAL':
        marker = '1'
    elif ischeme == 'PASS-OPA':
        marker = '8'
    elif ischeme == 'SCEDF':
        marker = '>'
    elif ischeme == 'SCRM':
        marker = '^'
    elif ischeme == 'SCAIR':
        marker = 'h'
    elif ischeme == 'MIP':
        marker = 'p'
    elif ischeme == 'SCAIR-RM':
        marker = '2'
    elif ischeme == 'SCAIR-OPA':
        marker = '3'
    elif ischeme == 'Combo-SJSB':
        marker = '4'
    elif ischeme == 'RSS':
        marker = 'p'
    elif ischeme == 'UDLEDF':
        marker = 'o'
    elif ischeme == 'WLAEDF':
        marker = 'H'
    elif ischeme.__contains__('SEIFDA-minD'):
        marker = 'o'
    elif ischeme.__contains__('SEIFDA-PBminD'):
        marker = 'H'
    elif ischeme.__contains__('SEIFDA-maxD'):
        marker = 'x'
    elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('DnD'):
        marker = 'D'
    elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('D=D'):
        marker = '*'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('DnD'):
        marker = '+'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('D=D'):
        marker = 'v'
    else:
        marker = '<'
    return marker

def pickName(ischeme):
    name = ''
    if ischeme.__contains__('PATH-minD') and ischeme.__contains__('DnD'):
        name = 'Clairvoyant-SSSD'
    elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('D=D'):
        name = 'Oblivious-IUB'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('DnD'):
        name = 'Clairvoyant-PDAB'
    elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('D=D'):
        name = 'Oblivious-MP'
    else:
        name = ischeme
    return name

def effsstsPlot(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    """
    prints all plots
    """
    # sstype= ['S','M','L','0.15']
    # ssofftypes = [2, 3, 5]
    ssoprops = ['2', '5', '8']

    figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # prefix="effsstsPlot/data/"

    # for three sub-plot, fixed
    # fig = plt.figure(figsize=(13, 4))
    fig = plt.figure()
    # create a virtual outer subsplot for putting big x-ylabel
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)

    ax.set_xlabel('Utilization (%)', size=15)
    ax.set_ylabel('Acceptance Ratio', size=15)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False,
                   bottom=False, left=False, right=False)

    i = 1
    for ischeme in schemes:
        ifile = prefix+"/"+str(minsstype)+"-"+str(maxsstype)+"/"+str(ssofftypes)+"/"+ischeme+ str(numberoftasks) +".npy"
        data = np.load(ifile)
        x = data[0][0::1]
        y = data[1][0::1]
        us = int(math.ceil(ustart/ustep))
        ue = int(math.floor(uend/ustep))
        print(x)
        print(y)
        x=x[us:ue+1]
        y=y[us:ue+1]
        ax.plot(x, y,
                '-',
                color=pickColor(ischeme),
                marker=pickMarker(ischeme),
                markersize=4,
                markevery=1,
                fillstyle='none',
                label=pickName(ischeme),
                linewidth=1.0,
                clip_on=False)
        if i == 1:
            ax.legend(bbox_to_anchor=(0.5, 1.11),
                        loc=10,
                        markerscale=1.5,
                        ncol=3,
                        borderaxespad=0.,
                        prop={'size': 10})

    ax.set_title('No. of tasks: '+str(numberoftasks)+', Self-suspension length: ' +
                    str(minsstype)+"-"+str(maxsstype)+', No. of segments: '+str(ssofftypes), size=10, y=0.99)
    ax.grid()
    i += 1
    #fig.savefig(prefix+"/"+isstype+"/"+issofftypes +
        #           "/"+ischeme+".pdf", bbox_inches='tight')

    #plt.show()
    if plotall:
        fig.savefig(prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    else:
        fig.savefig(prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/' + schemes[0] + '[' +  str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    #sys.exit()


def effsstsPlotmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    """
    prints all plots
    """
    # sstype= ['S','M','L','0.15']
    # ssofftypes = [2, 3, 5]
    ssoprops = ['2', '5', '8']

    figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # prefix="effsstsPlot/data/"

    # for three sub-plot, fixed
    # fig = plt.figure(figsize=(13, 4))
    #fig = plt.figure()
    # create a virtual outer subsplot for putting big x-ylabel
    # ax = fig.add_subplot(111)
    # fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)
    if id_par == 'Tasks per set':
        numberoftasks = par_values

    elif id_par == 'Number of Segments':
        ssofftypes = par_values
        print
        'ns1: ', ssofftypes[0]
    elif id_par == 'Suspension Length':
        minsstype = par_values[0:3]
        maxsstype = par_values[3:6]

    fig = plt.figure(figsize=(18, 12))
    for c in range(3):
        ax = fig.add_subplot(2, 3, (c + 1))

        ax.set_xlabel('Utilization (%)', size=10)
        ax.set_ylabel('Acceptance Ratio', size=10)
        ax.spines['top'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.tick_params(labelcolor='black', top=False,
                       bottom=False, left=False, right=False)
        i = 1
        for ischeme in schemes:
            if id_par == 'Tasks per set':
                ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
                    ssofftypes) + "/" + ischeme + str(numberoftasks[c]) + ".npy"
            elif id_par == 'Number of Segments':
                ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
                    ssofftypes[c]) + "/" + ischeme + str(numberoftasks) + ".npy"
            elif id_par == 'Suspension Length':
                ifile = prefix + "/" + str(minsstype[c]) + "-" + str(maxsstype[c]) + "/" + str(
                    ssofftypes) + "/" + ischeme + str(numberoftasks) + ".npy"
            data = np.load(ifile)
            x = data[0][0::1]
            y = data[1][0::1]
            us = int(math.ceil(ustart/ustep))
            ue = int(math.floor(uend/ustep))
            print(x)
            print(y)
            x=x[us:ue+1]
            y=y[us:ue+1]
            ax.plot(x, y,
                    '-',
                    color=pickColor(ischeme),
                    marker=pickMarker(ischeme),
                    markersize=4,
                    markevery=1,
                    fillstyle='none',
                    label=pickName(ischeme),
                    linewidth=1.0,
                    clip_on=False)
            if c==1:
                ax.legend(bbox_to_anchor=(0.5, 1.11),
                          loc=10,
                          markerscale=1.5,
                          ncol=3,
                          borderaxespad=0.,
                          prop={'size': 10})
            if i == 1:
                ax.grid()
            i += 1

    fig.suptitle('No. of tasks: '+str(numberoftasks)+', Self-suspension length: ' +
                    str(minsstype)+"-"+str(maxsstype)+', No. of segments: '+str(ssofftypes), size=16, y=0.99)
    # ax.grid()

    #fig.savefig(prefix+"/"+isstype+"/"+issofftypes +
        #           "/"+ischeme+".pdf", bbox_inches='tight')

    #plt.show()
    if plotall:
        fig.savefig(prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    else:
        fig.savefig(prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/' + schemes[0] + '[' +  str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')


def effsstsPlotAll(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    print('-------------------------------------------------------')
    print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
    print('-------------------------------------------------------')
    for scheme in schemes:
        effsstsPlot(prefix, False, scheme.split(), minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)
    if (plotall):
        effsstsPlot(prefix, True, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)

def effsstsPlotAllmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    print('-------------------------------------------------------')
    print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
    print('-------------------------------------------------------')
    for scheme in schemes:
        effsstsPlotmulti(prefix, False, id_par, par_values, scheme.split(), minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)
    if (plotall):
        effsstsPlotmulti(prefix, True, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)

if __name__ == '__main__':
    args = sys.argv
    print(args)
    testSchemes = ['EDA', 'NC', 'SCEDF', 'PASS-OPA']
    testSelfSuspendingType= ['S','M','L']
    testNumberofSegments = [2]
    effsstsPlotAll(args[1], True, testSchemes, testSelfSuspendingType, testNumberofSegments, 1, 99, 5, 10)
