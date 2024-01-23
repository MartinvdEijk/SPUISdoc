# %% Define
import sys
import os
import numpy as numpy
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Define yes/no prompt
def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()  # raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
def query_value(question, default=0.0):
    """
    Ask a input value question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is a float.
    """
    if default == 0.0:
        prompt = " [float] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()  # raw_input().lower()
        if default is not None and choice == '':
            return default
        elif any(c.isalpha() for c in choice):
            sys.stdout.write("Please respond with a float.\n")
        else:
            return float(choice)

def read_spuisin(in_file):
    """
    Read input file for SPUIS and return contents in dictionary.

    "inpfile" is the location of the input file to be read. It must be
    formatted to SPUIS specifications and can include comments.

    Contents of the input file will be returned in a dictionary using
    keys similar to those used in SPUIS.
    """
    print('Reading SPUIS input file...')
    print('Filename: %s' % in_file)
    tmp = []
    with open(in_file) as f:
        for line in f:
            if not line.strip().startswith('*'):
                # Save uncommented lines in temporary
                tmp.append(line)
    itmp = iter(tmp)
    spuisin = {}
    for itmpline in itmp:
        # Calculation method
        spuisin['bm'] = int(itmpline.split('\n')[0])
        itmpline = next(itmp)

        # Number of runs
        spuisin['nr'] = int(itmpline.split('\n')[0])
        itmpline = next(itmp)

        # Water levels and flow rate
        wsbeqt = numpy.ndarray([spuisin['nr'], 2], dtype=float)  # create temporary list
        for ii in range(spuisin['nr']):
            wsbeqt[ii] = itmpline.split('\n')[0].split()
            itmpline = next(itmp)
        spuisin['wsbeqt'] = wsbeqt

        # Number of slices
        spuisin['nx'] = int(itmpline.split('\n')[0])
        itmpline = next(itmp)

        # Slices
        slices = numpy.ndarray([spuisin['nx'], 4],
                               dtype=object)  # create temporary list which combines integers and floats
        for ii in range(spuisin['nx']):
            slices[ii] = itmpline.split('\n')[0].split()
            itmpline = next(itmp)
        spuisin['slices'] = slices

        # Discharge relation
        ar = numpy.ndarray([1, (spuisin['nx'] - 1)], dtype=int)
        ar[0] = list(map(int, itmpline.split('\n')[0].split()))
        spuisin['ar'] = ar
        itmpline = next(itmp)

        # Number of profiles
        spuisin['np'] = int(itmpline.split('\n')[0])
        itmpline = next(itmp)

        # Profile properties
        for ii in range(spuisin['np']):
            tmpname = 'profile' + str(ii)
            tmpprofile = {}
            tmpprofile['ip'] = int(itmpline.split('\n')[0].split()[0])
            tmpprofile['ny'] = int(itmpline.split('\n')[0].split()[1])
            tmpprofile['rb'] = float(itmpline.split('\n')[0].split()[2])
            profy = numpy.ndarray([tmpprofile['ny'], 3], dtype=float)
            for jj in range(tmpprofile['ny']):
                itmpline = next(itmp)
                profy[jj] = itmpline.split('\n')[0].split()
            tmpprofile['profy'] = profy
            spuisin[tmpname] = tmpprofile
            # Use try because profiles are at the end of the file
            try:
                itmpline = next(itmp)
            except StopIteration:
                print('Reached end of input file, returning parameters...')
                print('Finished reading SPUIS input file.')
                break
    return spuisin


def read_spuisout(spuisinput, uqh_file, uws_file):
    """
    Read output files for SPUIS and return contents.

    "spuisinput" is the input of the calculation created by read_spuisin.

    Contents of the output files will be returned in Pandas dataframe(s).
    """
    marker = 'A'  # marker for splitting

    # Read uqh file into dataframe
    with open(uqh_file) as uqh:
        print('Opened uqh-file.')
        uqhtxt = uqh.read()
    print('Closed uqh-file.')
    data = StringIO(uqhtxt)
    header = uqhtxt.split('\n')[0].split()
    uqh_df = pd.read_csv(data, names=header, sep=r"\s+", skiprows=1)
    data.close()

    # Read uws file into dataframe
    with open(uws_file) as uws:
        print('Opened uws-file.')
        uwstxt = uws.read()
        header = uwstxt.split(marker)[1].split('\n')[0].split()[1:]
        uws_df = pd.DataFrame(columns=header)  # create empty dataframe
    print('Closed uws-file.')
    for ii in range(1, len(uwstxt.split(marker))):
        uwstxt = str.replace(uwstxt, '-', ' -')  # replace to work around limited space in output file
        uwstxt = str.replace(uwstxt, '******', ' NaN')  # replace to not f* up the plots
        data = StringIO(uwstxt.split(marker)[ii])
        header = uwstxt.split(marker)[ii].split('\n')[0].split()[1:]
        tmp_df = pd.read_csv(data, names=header, sep=r"\s+", skiprows=2)

        #        tmp_df = pd.read_csv(data, names=header, delim_whitespace=True, skiprows=2)
        data.close()
        uws_df = pd.concat([uws_df, tmp_df], ignore_index=True)

    return uqh_df, uws_df


def align_y_axis(ax1, ax2):
    """
    Sets tick marks of twinx axes to line up with the number of total tick
    marks of the primary axis.

    ax1 and ax2 are the matplotlib axes.

    Spacing between the tick marks will be
    based on a factor of the default tick spacing chosen by matplotlib. The
    number of ticks is based on the number on the primary axis. Code adapted
    from Scott Howard via Stackoverflow:
    https://stackoverflow.com/questions/26752464/how-do-i-align-gridlines-for-two-y-axis-scales-using-matplotlib
    """

    # Obtain current tick spacing on both axes
    minresax1 = ax1.get_yticks()[1] - ax1.get_yticks()[0]
    minresax2 = ax2.get_yticks()[1] - ax2.get_yticks()[0]

    # Obtain number of ticks on primary axis
    nticks = len(ax1.get_yticks())

    # Obtain current tick limits
    ax1ylims = ax1.get_yticks()
    ax2ylims = ax2.get_yticks()

    # Calculate factors
    ax1factor = minresax1 * (nticks - 1)
    ax2factor = minresax2 * (nticks - 1)

    # Set new ticks
    ax1.set_yticks(numpy.linspace(ax1ylims[0],
                                  ax1ylims[-1] + (ax1factor - (ax1ylims[-1] -
                                                               ax1ylims[0]) % ax1factor) % ax1factor,
                                  nticks))
    ax2.set_yticks(numpy.linspace(ax2ylims[0],
                                  ax2ylims[-1] + (ax2factor -
                                                  (ax2ylims[-1] - ax2ylims[0]) % ax2factor) %
                                  ax2factor,
                                  nticks))


def align_x_axis(ax1, ax2):
    """
    Sets tick marks of twiny axes to line up with the number of total tick
    marks of the primary axis.

    ax1 and ax2 are the matplotlib axes.

    Spacing between the tick marks will be based on a factor of the default
    tick spacing chosen by matplotlib. The number of ticks is based on the
    number on the primary axis. Code adapted from Scott Howard via
    Stackoverflow:
    https://stackoverflow.com/questions/26752464/how-do-i-align-gridlines-for-two-y-axis-scales-using-matplotlib
    """

    # Obtain current tick spacing on both axes
    minresax1 = ax1.get_xticks()[1] - ax1.get_xticks()[0]
    minresax2 = ax2.get_xticks()[1] - ax2.get_xticks()[0]

    # Obtain number of ticks on primary axis
    nticks = len(ax1.get_xticks())

    # Obtain current tick limits
    ax1xlims = ax1.get_xticks()
    ax2xlims = ax2.get_xticks()

    # Calculate factors
    ax1factor = minresax1 * (nticks - 1)
    ax2factor = minresax2 * (nticks - 1)

    # Set new ticks
    ax1.set_xticks(numpy.linspace(ax1xlims[0],
                                  ax1xlims[-1] + (ax1factor - (ax1xlims[-1] -
                                                               ax1xlims[0]) % ax1factor) % ax1factor,
                                  nticks))
    ax2.set_xticks(numpy.linspace(ax2xlims[0],
                                  ax2xlims[-1] + (ax2factor - (ax2xlims[-1] -
                                                               ax2xlims[0]) % ax2factor) % ax2factor,
                                  nticks))


def plot_spuis(in_file, spuisinput, uqh_df, uws_df, **keyword_parameters):
    """
    Plot a graphical representation of the output from the SPUIS calculation.
    Two types of plots will be generated, one showing the discharge as a
    function of head difference for each case and one showng the results
    for each case of the water levels, energy head, average flow velocity and
    Froude number.

    in_file_path is the location of the input file, the plots will be saved
    here.
    spuisinput is the input of spuis as generated by read_spuisin.
    uqh_df and uws_df is the output of spuis as generated by read_spuisout.
    """

    # Check existence of keyword parameter
    if ('save' in keyword_parameters):
        saveyn = keyword_parameters['save']
    else:
        saveyn = 'False'

    # saveyn is True, turn interactive mode off (don't show the plots)
    if saveyn:
        plt.ioff()
        # Get filename of input file
        fname, ext = os.path.splitext(os.path.basename(in_file))
    else:
        plt.ion()

    # Plot profiles
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(projection='3d')
    ax0.set_aspect('equal')
    for ii in range(spuisinput['nx']):
        slicex = spuisinput['slices'][ii][1]  # obtain horizontal position of slice
        slicez = spuisinput['slices'][ii][2]  # obtain bottom level of slice
        profnum = int(spuisinput['slices'][ii][3])  # obtain profile number of slice
        profname = 'profile' + str(profnum - 1)  # profile name in dict

        proftmp = spuisinput[profname]

        ax0.plot3D(proftmp['profy'][:, 1] / 2.,
                   numpy.ones(numpy.shape(proftmp['profy'][:, 1])) * float(slicex),
                   float(slicez) + proftmp['profy'][:, 0], color='tab:blue')
        ax0.plot3D(-proftmp['profy'][:, 1] / 2.,
                   numpy.ones(numpy.shape(proftmp['profy'][:, 1])) * float(slicex),
                   float(slicez) + proftmp['profy'][:, 0], color='tab:blue')
    # Create cubic bounding box to simulate equal aspect ratio (from tauran
    # at https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to)
    X = ax0.get_xbound()
    Y = ax0.get_ybound()
    Z = ax0.get_zbound()
    max_range = numpy.array([max(X) - min(X), max(Y) - min(Y), max(Z) - min(Z)]).max()
    mid_x = (max(X) + min(X)) * 0.5
    mid_y = (max(Y) + min(Y)) * 0.5
    mid_z = (max(Z) + min(Z)) * 0.5
    ax0.set_xlim(mid_x - max_range, mid_x + max_range)
    ax0.set_ylim(mid_y - max_range, mid_y + max_range)
    ax0.set_zlim(mid_z - max_range, mid_z + max_range)

    # Save zero figure
    in_file_path = os.path.dirname(os.path.realpath(in_file))
    if saveyn:
        prof_png = in_file_path + '\\' + fname + '_prof.png'
        fig0.savefig(prof_png)  # , bbox_inches='tight', pad_inches=0)
        print('Profile figure saved.')
    else:
        fig0.show()

    # Relation head difference and flow rate
    fig1 = plt.figure()
    ax1 = plt.gca()
    plt.grid()
    #    maxylim = numpy.ceil(max(uqh_df['debiet'])/25.)*25.
    #    ax1.set_ylim((0.0, maxylim ))
    plt.title('Debiet als functie van verval', horizontalalignment='center')
    plt.xlabel('Verval [m]')
    plt.ylabel('Debiet [m$^3$/s]')
    plt.plot(uqh_df['verval'], uqh_df['debiet'],
             ls='-', marker='o', mfc="None", color='tab:blue')

    # Save first figure
    in_file_path = os.path.dirname(os.path.realpath(in_file))
    if saveyn:
        uqh_png = in_file_path + '\\' + fname + '_uqh.png'
        fig1.savefig(uqh_png)  # , bbox_inches='tight', pad_inches=0)
        print('UQH figure saved.')
    else:
        fig1.show()

    # Plot figures with water levels
    for ii in range(spuisinput['nr']):
        # Help variables for data selection from output file
        blckstart = ii * spuisinput['nx']
        blckend = ii * spuisinput['nx'] + spuisinput['nx']

        # Create figure and subplots and define subplot axes positions
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('legend', **{'fontsize': 8})
        fig2 = plt.figure()
        fig2.set_size_inches(8.27, 11.69)
        fig2.canvas.manager.set_window_title('Resultaat bij debiet van ' + str(
            uqh_df['debiet'][ii]) + ' [m3.s-1]')  # , horizontalalignment='center') # plot title

        ax1 = fig2.add_subplot(311)
        ax1.set_position([0.15, 0.75, 0.7, 0.2])
        ax1.get_xaxis().set_ticklabels([])
        ax1.xaxis.label.set_size(9)
        ax1.yaxis.label.set_size(9)
        #        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        ax2 = fig2.add_subplot(312, sharex=ax1)
        ax2.set_position([0.15, 0.475, 0.7, 0.2])
        ax2.xaxis.label.set_size(9)
        ax2.yaxis.label.set_size(9)
        #        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        ax3 = fig2.add_subplot(313)
        ax3.set_position([0.15, 0.20, 0.7, 0.2])
        ax3.xaxis.label.set_size(9)
        ax3.yaxis.label.set_size(9)
        ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        ax4 = fig2.add_subplot(111)
        ax4.set_position([0.70, 0.04, 0.25, 0.12])
        ax4.xaxis.label.set_size(7)
        ax4.yaxis.label.set_size(7)

        # Plot 1: flow width (stroomvoerende breedte)
        ax1.grid()  # create grid
        ax1.set_ylabel('Stroomvoerende breedte [m]')  # create yaxis label
        ax1.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['brwopp'],
                 ls='-', marker='+', label='Breedte')

        # Plot 2: Water level and energy head
        ax2.grid()  # create grid
        ax2.set_ylabel('Niveau [NAP+m]')  # create yaxis label
        ax2.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['energh'],
                 ls='-', color='tab:red',
                 label='Energiehoogte')  # plot energy head
        ax2.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['ws'],
                 ls='-', color='tab:blue',
                 label='Waterstand')  # plot water level
        ax2.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['zb'] +
                 uws_df[blckstart:blckend]['grensd'],
                 ls='--', color='tab:green',
                 label='Grensdiepte')  # plot critical depth
        ax2.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['zb'],
                 ls='-', color='tab:brown',
                 label='Bodem')  # plot bottom
        # Make legend using labels
        lns2, lbls2 = ax2.get_legend_handles_labels()
        leg2 = ax2.legend(lns2, lbls2,
                          bbox_to_anchor=(1, 1.02), loc=4, borderaxespad=0.)
        leg2.draw_frame(False)  # include legend without frame

        # Plot 3: Average velocity and Froude number using two y-axes
        color1 = 'tab:blue'
        color2 = 'tab:red'
        ax3.grid()  # create grid
        ax3.set_xlabel('X-positie [m]')  # create axis labels
        ax3.set_ylabel('Stroomsnelheid [m/s]')
        # Plot on first axis
        ax3.plot(uws_df[blckstart:blckend]['xd'],
                 uws_df[blckstart:blckend]['v'], ls='-',
                 label='Stroomsnelheid', color=color1)
        # Second axis
        ax32 = ax3.twinx()  # create second axis
        ax32.set_position(ax3.get_position())  # use position of other axis
        ax32.xaxis.label.set_size(9)
        ax32.yaxis.label.set_size(9)
        ax32.set_ylabel('Froudegetal [-]')
        # Plot on second axis
        ax32.plot(uws_df[blckstart:blckend]['xd'],
                  uws_df[blckstart:blckend]['froude'], ls='-',
                  label='Froudegetal', color=color2)
        # Adjust axis ticks to get same tick positions on both axes
        align_y_axis(ax3, ax32)
        # Make legend using labels from both axes
        lns31, lbls31 = ax3.get_legend_handles_labels()
        lns32, lbls32 = ax32.get_legend_handles_labels()
        leg3 = ax3.legend(lns31 + lns32, lbls31 + lbls32,
                          bbox_to_anchor=(1, 1.02), loc=4, borderaxespad=0.)
        leg3.draw_frame(False)  # include legend without frame

        # Plot 4
        ax4.grid()  # create grid
        ax4.set_xlabel('Verval [m]')  # create axis labels
        ax4.set_ylabel('Debiet [m$^3$/s]')
        ax4.plot(uqh_df['verval'], uqh_df['debiet'],
                 ls='-', marker='o', mfc="None", color='tab:blue')
        ax4.plot(uqh_df['verval'][ii], uqh_df['debiet'][ii],
                 ls='-', marker='o', color='tab:red')

        # Add text below plots
        t1_xpos = 0.05
        t2_xpos = 0.35
        t3_xpos = 0.44

        ypos1 = 0.1
        ypos2 = ypos1 - 0.02
        ypos3 = ypos2 - 0.02
        ypos4 = ypos3 - 0.02
        ypos5 = ypos4 - 0.02

        qtmp = uqh_df['debiet'][ii]  # Values to fill in
        hdtmp = uqh_df['ws(nx)'][ii]
        hutmp = uqh_df['ws(1)'][ii]
        dhtmp = uqh_df['verval'][ii]
        Htmp = uws_df.loc[blckstart, 'energh']

        fig2.text(t1_xpos, ypos1, 'Debiet',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t2_xpos, ypos1, ': ' + format(qtmp, '.1f'),
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t3_xpos, ypos1, '[m$^3$/s]',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)

        fig2.text(t1_xpos, ypos2, 'Benedenwaterstand',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t2_xpos, ypos2, ': ' + format(hdtmp, '.3g'),
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t3_xpos, ypos2, '[NAP+m]',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)

        fig2.text(t1_xpos, ypos3, 'Bovenwaterstand',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t2_xpos, ypos3, ': ' + format(hutmp, '.3g'),
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t3_xpos, ypos3, '[NAP+m]',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)

        fig2.text(t1_xpos, ypos4, 'Verval',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t2_xpos, ypos4, ': ' + format(dhtmp, '.3g'),
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t3_xpos, ypos4, '[m]',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)

        fig2.text(t1_xpos, ypos5, 'Energiehoogte bovenstrooms',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t2_xpos, ypos5, ': ' + format(Htmp, '.3g'),
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)
        fig2.text(t3_xpos, ypos5, '[NAP+m]',
                  verticalalignment='bottom', horizontalalignment='left',
                  color='black', fontsize=10)

        # Save other figures
        if saveyn:
            uws_png = in_file_path + '\\' + fname + '_uws_' + str(ii + 1).zfill(2) + 'of' + str(
                spuisinput['nr']) + '.png'
            fig2.savefig(uws_png)  # , bbox_inches='tight', pad_inches=0)
            print('UWS figure ' + str(ii + 1) + ' of ' + str(spuisinput['nr']) + ' saved.')
        else:
            fig2.show()

    # Close figures
    if saveyn:
        plt.close('all')