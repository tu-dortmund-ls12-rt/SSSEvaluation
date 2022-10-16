from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math

def pickColor(ischeme):
	color = ''
	schemes = [
		'EDA','PROPORTIONAL','SEIFDA-MILP',
		'SCEDF','SCRM','SCAIR-RM','SCAIR-OPA','EDAGMF-OPA','MILP-ReleaseJitter','SRSR',
		'PASS-OPA','RSS','UDLEDF','WLAEDF','RTEDF','UNIFRAMEWORK','SUSPOBL','SUSPJIT','SUSPBLOCK','BURST-RM','UPPAAL'
		'NC']
	colors = [
		'#0ff1ce','#696969','#bada55',
		'#7fe5f0','#ff0000','#ff80ed','#407294','#c39797','#420420','#133337',
		'#065535','#f08080','#5ac18e','#666666','#6897bb','#f7347a','#576675','#ffc0cb','#81d8d0','#ac25e2','#b4eeb4',
		'#008080',
		'#696966','#ffd700','#ffa500','#8a2be2','#00ffff','#ff7373','#40e0d0','#0000ff',
		'#d3ffce','#c6e2ff','#b0e0e6','#fa8072','#003366','#ffff00','#ffb6c1','#8b0000',
		'#800000','#800080','#7fffd4','#00ff00','#cccccc','#0a75ad','#ffff66','#000080',
		'#ffc3a0','#20b2aa','#333333','#66cdaa','#ff6666','#ff00ff','#ff7f50','#088da5',
		'#4ca3dd','#468499','#047806','#008000','#f6546a','#cbbeb5','#00ced1','#101010',
		'#660066','#b6fcd5','#daa520','#990000','#0e2f44','#808080',
		]
	if ischeme in schemes:
		index = schemes.index(ischeme)
		color = colors[index]
	else:
		if ischeme.__contains__('SEIFDA-minD'):
			color = '#ffd700'
		elif ischeme.__contains__('SEIFDA-PBminD'):
			color = '#c6e2ff'
		elif ischeme.__contains__('SEIFDA-maxD'):
			color = '#800080'
		elif ischeme.__contains__('Oblivious-IUB'):
			color = '#20b2aa'
		elif ischeme.__contains__('Clairvoyant-SSSD'):
			color = '#66cdaa'
		elif ischeme.__contains__('Oblivious-MP'):
			color = '#ffa500'
		elif ischeme.__contains__('Clairvoyant-PDAB'):
			color = '#b0e0e6'
		else:
			color = '#0FF0F0'
	return color

def pickMarker(ischeme):
	marker = ''
	schemes = [
		'EDA','PROPORTIONAL','SEIFDA-MILP',
		'SCEDF','SCRM','SCAIR-RM','SCAIR-OPA','EDAGMF-OPA','MILP-ReleaseJitter','SRSR',
		'PASS-OPA','RSS','UDLEDF','WLAEDF','RTEDF','UNIFRAMEWORK','SUSPOBL','SUSPJIT','SUSPBLOCK',
		'NC']
	markers = [
		".",",","o",
		"v","^","<",">","1","2","3",
		"4","8","s","p","P","*","h","H","+",
		"x",
		"X","D","d","|","_","."]

	if ischeme in schemes:
		index = schemes.index(ischeme)
		marker = markers[index]
	else: 
		if ischeme.__contains__('SEIFDA-minD'):
			marker = "X"
		elif ischeme.__contains__('SEIFDA-PBminD'):
			marker = "D"
		elif ischeme.__contains__('SEIFDA-maxD'):
			marker = "d"
		elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('DnD'):
			marker = "|"
		elif ischeme.__contains__('PATH-minD') and ischeme.__contains__('D=D'):
			marker = "_"
		elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('DnD'):
			marker = "."
		elif ischeme.__contains__('PATH-PBminD') and ischeme.__contains__('D=D'):
			marker = ","
		else:
			marker = "o"
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

def effsstsPlot(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset):
	"""
	prints all plots
	"""
	# sstype= ['S','M','L','0.15']
	# ssofftypes = [2, 3, 5]
	#ssoprops = ['2', '5', '8']

	#figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
	# prefix="effsstsPlot/data/"

	# for three sub-plot, fixed
	# fig = plt.figure(figsize=(13, 4))
	fig = plt.figure()
	# create a virtual outer subsplot for putting big x-ylabel
	ax = fig.add_subplot(111)
	fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)

	ax.set_xlabel('Execution Time', size=15)
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
		data = np.load(ifile, allow_pickle=True)
		x = data[0][0::1]
		y = data[1][0::1]
		print(x)
		print(y)
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

	ax.set_title('No. of tasks: '+str(numberoftasks)+', Tasksets per configuration: ' +
					str(taskperset)+', Granularity: '+str(ssofftypes), size=10, y=0.99)
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


def effsstsPlotmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset):
	"""
	prints all plots
	"""
	# sstype= ['S','M','L','0.15']
	# ssofftypes = [2, 3, 5]
	#ssoprops = ['2', '5', '8']

	#figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
	# prefix="effsstsPlot/data/"

	# for three sub-plot, fixed
	# fig = plt.figure(figsize=(13, 4))
	# fig = plt.figure()
	# create a virtual outer subsplot for putting big x-ylabel
	# ax = fig.add_subplot(111)
	# fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)
	if id_par == 'Tasks per Set':
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

		ax.set_xlabel('Execution Time', size=10)
		ax.set_ylabel('Acceptance Ratio', size=10)
		ax.spines['top'].set_color('black')
		ax.spines['bottom'].set_color('black')
		ax.spines['left'].set_color('black')
		ax.spines['right'].set_color('black')
		ax.tick_params(labelcolor='black', top=False,
					bottom=False, left=False, right=False)
		i = 1
		for ischeme in schemes:
			if id_par == 'Tasks per Set':
				ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
					ssofftypes) + "/" + ischeme + str(numberoftasks[c]) + ".npy"
			elif id_par == 'Number of Segments':
				ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
					ssofftypes[c]) + "/" + ischeme + str(numberoftasks) + ".npy"
			elif id_par == 'Suspension Length':
				ifile = prefix + "/" + str(minsstype[c]) + "-" + str(maxsstype[c]) + "/" + str(
					ssofftypes) + "/" + ischeme + str(numberoftasks) + ".npy"
			data = [0]
			try:
				data = np.load(ifile)
			except:
				print("Data not loaded")
			if np.all(data)==False:
				if id_par == 'Tasks per Set':
					raise Exception("Run "+str(ischeme)+" with "+str(numberoftasks[c])+" "+str(id_par)+" first")
				elif id_par == 'Number of Segments':
					raise Exception("Run "+str(ischeme)+" with "+str(ssofftypes[c])+" Segments first")
				elif id_par == 'Suspension Length':
					raise Exception("Run "+str(ischeme)+" with Suspension Interval of ["+str(minsstype[c])+","+str(maxsstype[c])+"] first")
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

	fig.suptitle('No. of tasks: '+str(numberoftasks)+', Tasksets per configuration: ' +
					str(taskperset)+', Granularity: '+str(ssofftypes), size=16, y=0.99)
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


def effsstsPlotAll(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset):
	print('-------------------------------------------------------')
	print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
	print('-------------------------------------------------------')
	for scheme in schemes:
		effsstsPlot(prefix, False, scheme.split(), minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset)
	if (plotall):
		effsstsPlot(prefix, True, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset)

def effsstsPlotAllmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset):
	print('-------------------------------------------------------')
	print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
	print('-------------------------------------------------------')
	for scheme in schemes:
		effsstsPlotmulti(prefix, False, id_par, par_values, scheme.split(), minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset)
	if (plotall):
		effsstsPlotmulti(prefix, True, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, taskperset)

if __name__ == '__main__':
	args = sys.argv
	print(args)
	testSchemes = ['EDA', 'NC', 'SCEDF', 'PASS-OPA']
	testSelfSuspendingType= ['S','M','L']
	testNumberofSegments = [2]
	effsstsPlotAll(args[1], True, testSchemes, testSelfSuspendingType, testNumberofSegments, 1, 10, 5, 10,10)