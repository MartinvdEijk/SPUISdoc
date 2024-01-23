# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 15:54:21 2018

@author: loor

Script to read input file and run program of Spuis. First attempt to script the
running of Spuis, including file selection, running and plotting of output.
Based on experience improvements of workflow can probably be implemented.
"""

#%% Packages
import sys
import os
import tkinter as tk
from tkinter import filedialog
import numpy as numpy
import shutil
import time
import matplotlib.pyplot as plt
import subprocess

#%% Set constants (Directory with code
spuisdir = os.getcwd()+'/SPUIS401'
spuisEXE = 'SPUIS401.exe'

#%% Functions
sys.path.insert(1, spuisdir)
import py.POSTPROC as pp

#%% Options
print('')
saveyn = pp.query_yes_no('Save figures?', default="no")

print('')
inpmeth = pp.query_yes_no('Use a single input file? Alternative is selecting a folder containing input files', default="yes")

#%% File selection (single file or single directory containing multiple files)
print('')
if inpmeth:
    # Define options for selecting a file
    file_opt = options = {}
    options['filetypes'] = [('SPUIS input files', '.in'), ('all files', '.*')]
    options['title'] = 'Select SPUIS input file'
    
    # Open file selection dialog
    print('Selecting file...')
    root = tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    root.attributes("-topmost", True)
    in_file = tk.filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), **file_opt) # show an "Open" dialog box and return the path to the selected file
    if not in_file:
        raise ValueError('No file selected.')
    in_files = []
    in_files.append(in_file)
    print('Files selected: %s' % ', '.join(map(str, in_files)))
else:
    # Open directory selection dialog
    print('Selecting directory...')
    root = tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    root.attributes("-topmost", True)
    dirname = tk.filedialog.Directory(parent=root).show()
    if not dirname:
        raise ValueError('No directory selected.')
    else:
        in_files = [] # empty list, selected files will be appended
        in_filestmp = [] # empty list, selected files will be appended
        for in_file in os.listdir(dirname):
            if in_file.endswith('.in'):
                in_files.append(os.path.realpath(os.path.join(dirname, in_file)))
                in_filestmp.append(in_file)
        print('Directory selected: %s' %(os.path.realpath(dirname)))
        print('Files selected: [%s]' % ', '.join(map(str, in_filestmp)))
print('')

# Iterate over input files
for in_file in in_files:
    print('')
    # Run SPUIS
        # Prepare file system
            # Get directory of input file
    in_file_path = os.path.dirname(os.path.realpath(in_file))
            # Get filename of input file
    fname, ext = os.path.splitext(os.path.basename(in_file))
            # Get location and input for SPUIScode
    spuisrun = spuisEXE
    work_file_base = 'work'
    cwdir = os.getcwd()

        # Print information
    print('Working directory        : ' + cwdir)
    print('Location of input file   : ' + in_file_path)
    print('Input filename           : ' + fname + ext)
    print('Location of SPUIS py     : ' + spuisdir)
    print('Executable name          : ' + spuisrun)
    print('')
    
        # Run exe
    # print('Starting SPUIS...')
    # os.chdir(spuisdir+'/') # for some reason necessary to change to directory
    #
    # try:
    #     from SPUIS401 import spuis401  # import the code
    #     spuis401(in_file, work_file_base)
    # except FileNotFoundError:
    #     print("Execution file not found for SPUIS")
    # time.sleep(1) # wait a second to make sure output files are written

        # Run exe
    print('Starting SPUIS...')
    workin = spuisdir + '\\work.in'
    shutil.copyfile(in_file, workin)
    os.chdir(spuisdir) # for some reason necessary to change to directory
    try:
        spuisout = subprocess.check_output([spuisrun, work_file_base+'.in', work_file_base+'.uin', work_file_base+'.uws', work_file_base+'.uqh'],
                                           stderr=subprocess.PIPE, text=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("Status: SPUIS failed", exc.returncode, exc.output)
    else:
        # error in SPUIS not captured using above method, checking output for error instead. Ugly, need to change this!
        if 'terminated' in spuisout:
            print("Status: SPUIS failed")
            raise ValueError("CLI output: \n{}\n".format(spuisout))
        else:
            print("CLI output: \n{}\n".format(spuisout)) # Print output of SPUIS
            print('Finished SPUIS calculation.')
            print('')
    time.sleep(1) # wait a s

    #% Read output of SPUIS
    spuisinput = pp.read_spuisin(in_file)
    print('Reading SPUIS output files...')
    uin_file = work_file_base+'.uin'
    uqh_file = work_file_base+'.uqh'
    uws_file = work_file_base+'.uws'
    uqh_df, uws_df = pp.read_spuisout(spuisinput, uqh_file, uws_file)
    print('Done.')
    print('')
    
    os.chdir(cwdir) # change back to previous directory
        
    #% Move output files back to original location of input file
    print('Moving files...')
    for tmp_file in os.listdir(spuisdir):
        if tmp_file.startswith('work'):
            if tmp_file.split('.')[1] == 'in':
                os.remove(os.path.join(spuisdir, tmp_file))
            else:
                shutil.move(os.path.join(spuisdir, tmp_file), in_file[:-2] + tmp_file.split('.')[1])
    print('Done.')
    print('')
    
    #% Plot results
    pp.plot_spuis(in_file, spuisinput, uqh_df, uws_df, save=saveyn)
    print('')
    
    #%% Calculate discharge coefficient when subcritical flow
    # Engineers assume that the pressure is zero at the gate opening and following equation is obtained for discharge
    # Because it is not exactly zero, a coefficients is needed. When critical flow, set to zero.
    # Formula:   Q = mu A sqrt(2 g dh) > mu = Q / A / sqrt(2 g dh)
    # A: Sluice-gate opening area, dh: difference sill height and upstream flow depth
    
    uqh_copy = uqh_df.copy()
    uqh_copy["mu"] = numpy.nan
    uqh_copy["verval2"] = numpy.nan
    uqh_copy["mu2"] = numpy.nan

    # Sluice-gate opening area (constant for all runs)
    culvA = pp.query_value('Sluice-gate opening area?', default=0.0)

    for ii in range(spuisinput['nr']):
        #% Calculate new head difference
        blckstart = ii*spuisinput['nx']
        blckend = ii*spuisinput['nx']+spuisinput['nx']-1

        #% Add upstream velocity head to water level to get far-field water level (or just get total energy head)
        # wsup = uws_df.loc[blckstart, 'ws'] + numpy.power(uws_df.loc[blckstart, 'v'], 2)/2/9.81
        wsup = uws_df.loc[blckstart, 'energh']

        #% Take downstream water level, implying K=1 from last section to far-field water level
        wsdown = uws_df.loc[blckend, 'ws']
        uqh_copy.loc[ii,'verval2'] = wsup - wsdown

        #% Area of flow
        # TODO: Why volumetric?
        # print('')
        # culvA = 18.*8.*8.
        # culvA = 5.*12.*(uws_df.loc[blckstart+13, 'ws'] + 4.65)
        
        #% Calculate discharge coefficient
        if not uqh_copy.loc[ii, 'icrit']: # check is critical flow is present
            mutmp = uqh_copy.loc[ii,'debiet'] / culvA / numpy.sqrt(2*9.81*abs(uqh_copy.loc[ii, 'verval']))
            mutmp2 = uqh_copy.loc[ii,'debiet'] / culvA / numpy.sqrt(2*9.81*abs(uqh_copy.loc[ii, 'verval2']))
            uqh_copy.loc[ii,'mu'] = mutmp
            uqh_copy.loc[ii,'mu2'] = mutmp2
        else:
            uqh_copy.loc[ii,'mu'] = 1e-15
            uqh_copy.loc[ii,'mu2'] = 1e-15


    #% Relation flow rate and discharge coefficient
    figmu1 = plt.figure()
    ax = plt.gca()
    plt.grid()
    maxylim = numpy.ceil(max(uqh_copy[['mu', 'mu2']].max(axis=0))/0.05)*0.05
    minylim = numpy.floor(min(uqh_copy[['mu', 'mu2']].min(axis=0))/0.05)*0.05
    ax.set_ylim((minylim, maxylim))    
    plt.title('Afvoercoefficient als functie van debiet', horizontalalignment='center')
    plt.xlabel('Debiet [m$^3$/s]')
    plt.ylabel('Afvoercoëfficiënt [-]')
    plt.plot(uqh_copy['debiet'], uqh_copy['mu'], label='Lokaal',
             ls='-', marker='o', mfc="None", color='tab:blue')
#    plt.plot(uqh_copy['debiet'], uqh_copy['mu2'], label='Far field', 
#             ls='-', marker='o', mfc="None", color='tab:red')
    
    #% Relation head difference and discharge coefficient
    figmu2 = plt.figure()
    ax = plt.gca()
    plt.grid()
#    maxylim = numpy.ceil(max(uqh_copy['mu'])/0.05)*0.05
#    minylim = numpy.floor(min(uqh_copy['mu'])/0.05)*0.05
    ax.set_ylim((minylim, maxylim))    
    plt.title('Afvoercoefficient als functie van verval', horizontalalignment='center')
    plt.xlabel('Verval [m]')
    plt.ylabel('Afvoercoëfficiënt [-]')
    plt.plot(uqh_copy['verval'], uqh_copy['mu'], label='Lokaal',
             ls='-', marker='o', mfc="None", color='tab:blue')
#    plt.plot(uqh_copy['verval2'], uqh_copy['mu2'], label='Far field',
#             ls='-', marker='o', mfc="None", color='tab:red')
    
    # Save discharge coefficient figures
    in_file_path = os.path.dirname(os.path.realpath(in_file))
    mu1_png = in_file_path + '\\' + fname + '_mu1.png'
    mu2_png = in_file_path + '\\' + fname + '_mu2.png'
    figmu1.savefig(mu1_png)#, bbox_inches='tight', pad_inches=0)
    figmu2.savefig(mu2_png)#, bbox_inches='tight', pad_inches=0)
    print('Mu figures figure saved.')
    plt.close()
    plt.close()
print('Done.')
print('')


    