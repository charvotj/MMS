import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

fonts_setting = {
        # Use LaTeX to write all text
        "text.usetex": True,
        "font.family": "serif",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 12,
        "font.size": 12,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10
    }
plt.rcParams.update(fonts_setting)

def main():
    data = pd.read_csv('9/tex/data/koncentrace.csv')
    objem_nadoby = math.pi*(1.4/2)**2*2 # [l]
    data['C_vyp'] = data['V_actn']*(22.4*0.79)/(58*objem_nadoby) # [ppm]
    data['C_abs_err'] = data['C_mer'] - data['C_vyp']
    data['C_rel_err'] = data['C_abs_err'] / data['C_vyp'] * 100

    print(data)
    plot_mer(data) 
    plot_kalib(data) 
    make_latex_table(data,'9/tex/tables/hodnoty.tex')


def make_latex_table(data:pd.DataFrame,filename):
    latex_data=pd.DataFrame({
        r"přídavek":data['pridavek'],
        r"$V_{aceton}\ [\mu l]$":data['V_actn'],
        r'$C_{vypoctena}\ [ppm]$':[f'{float(i):.3f}'.replace('.',',') for i in data['C_vyp']],
        r"$C_{merena}\ [ppm]$":data['C_mer'],
    })

    latex_table = latex_data.to_latex(index=False, 
                            # float_format="%.3f",
                            decimal=',',
                            column_format='cccc')
    
    with open(filename,'w') as f:
        f.write(latex_table)

def plot_mer(data):
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['V_actn'], data['C_mer'], marker='x', linestyle='none')
    ax.set_xlabel(r"$V_{aceton}\ [\mu l]$")
    ax.set_ylabel(r"$C_{mereno}\ [ppm]$")
    # linear regression with anotattion
    [reg_data, coefficients] = make_regression(data['V_actn'], data['C_mer'])
    ax.plot(data['V_actn'], reg_data, color='blue', label='Lineární regrese', linestyle='--')
    coef_str = {}
    coef_str[0] = f"{coefficients[0]:.3f}".replace(',',' ').replace('.',',')
    coef_str[1] = f"{coefficients[1]:.3f}".replace(',',' ').replace('.',',')
    ax.annotate(r"$C_{mereno}$" + f"= {coef_str[0]}"+ r"$\cdot V_{aceton}$ + " + f"{coef_str[1]}", xy=(0.1, 0.9), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    ax.grid()
    # ax.set_xlim(-90, 90)
    # ax.set_ylim(-90, 90)
    # ax.set_xticks(np.arange(-90, 91, 30))
    # ax.set_yticks(np.arange(-90, 91, 30))
    plt.tight_layout()
    #plt.show()
    fig.savefig('9/tex/img/konc-mer.pdf')
    

def plot_kalib(data):
    # calcuate difference between X and Y
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['C_mer'], data['C_vyp'], marker='x', linestyle='none')
    ax.set_xlabel(r'$C_{mereno}\ [ppm]$')
    ax.set_ylabel(r'$C_{vypocteno}\ [ppm]$')
    # linear regression with anotattion
    [reg_data, coefficients] = make_regression(data['C_mer'], data['C_vyp'])
    ax.plot(data['C_mer'], reg_data, color='blue', label='Lineární regrese', linestyle='--')
    coef_str = {}
    coef_str[0] = f"{1000*coefficients[0]:.3f}".replace(',',' ').replace('.',',')
    coef_str[1] = f"{100*coefficients[1]:.3f}".replace(',',' ').replace('.',',')
    ax.annotate(r"$C_{vyp}" + f"= {coef_str[0]} "+ r"\cdot 10^{-3} \cdot C_{mer} " + f"{coef_str[1]}"+r'\cdot 10^{-2} $', xy=(0.1, 0.9), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    ax.grid()
    plt.tight_layout()
    #plt.show()

    fig.savefig('9/tex/img/konc-kalib.pdf')

def plot_nak(data):
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['deg'], data['nak'], marker='x', linestyle='none')
    ax.set_xlabel(r"$\theta_{nastaveno}\ [^\circ]$")
    ax.set_ylabel(r"$\theta_{mereno}\ [^\circ]$")
    #ax.set_title('Naklon')
    # linear regression with anotattion
    [reg_data, coefficients] = make_regression(data['deg'], data['nak'])
    ax.plot(data['deg'], reg_data, color='blue', label='Lineární regrese', linestyle='--')
    ax.annotate(r"$\theta_{nastaveno}$" + f"= {coefficients[0]:.3f}"+ r"$\cdot \theta_{mereno}$ + " + f"{coefficients[1]:.3f}", xy=(0.1, 0.9), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    ax.grid()
    ax.set_xlim(-90, 90)
    ax.set_ylim(-90, 90)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.set_yticks(np.arange(-90, 91, 30))
    plt.tight_layout()
    #plt.show()
    fig.savefig('10/tex/img/naklon-kalib.pdf')
    


    diff = data['deg'] - data['nak']
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['deg'], diff, marker='x', linestyle='none')
    ax.set_xlabel(r'$\theta_{nastaveno}\ [^\circ]$')
    ax.set_ylabel(r'$\Delta \theta \ [^\circ]$')
    ax.axhline(y=0.22, color='r', linestyle='--')
    ax.axhline(y=-0.22, color='r', linestyle='--')
    ax.set_ylim(-2, 2)
    ax.set_xlim(-90, 90)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.grid()
    # add legend for the red lines - rozmezí výrobce, and add legend fot the plot
    ax.legend(['Data', 'Rozmezí výrobce'])

    plt.tight_layout()
    #plt.show()
    plt.savefig('10/tex/img/naklon-korek.pdf')
    #for i in range(len(diff)):
    #    print(f"deg: {data['deg'][i]}, nak: {data['nak'][i]} , diff: {diff[i]}")
    #fig.savefig('naklon.png')

def make_regression(x_data, y_data):
    # Perform linear regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    reg_data = slope * np.array(x_data) + intercept
    return [reg_data, coefficients]


if __name__ == "__main__":
    main()





'''
    plt.plot(real_l, make_regression(real_l, l), color='blue', label='Lineární regrese', linestyle='--') 
    coefficients = np.polyfit(real_l, l, 1) 
    plt.annotate(r"$l_{nastaveno}$" + f"= {coefficients[0]:.3f}"+ r"$\cdot l_{mereno}$" + f"{coefficients[1]:.3f}", xy=(0.1, 0.9), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))


# load data from csv file
# F;Zr;Zim this is my data

data2 = pd.read_csv('2.csv', sep=';')
data3 = pd.read_csv('3.csv', sep=';')

# Scale the resistance values to kilohms
data['Zr'] = data['Zr'] / 1000
data['Zim'] = data['Zim'] / 1000
data2['Zr'] = data2['Zr'] / 1000
data2['Zim'] = data2['Zim'] / 1000
data3['Zr'] = data3['Zr'] / 1000
data3['Zim'] = data3['Zim'] / 1000

# create a figure and axis  
fig, ax = plt.subplots(figsize=(5, 3))
# plot them, Zr is x and Zim is y
ax.plot(data2['Zr'], -data2['Zim'], label='Vzorek 2', marker='x')
ax.plot(data3['Zr'], -data3['Zim'], label='Vzorek 3', marker='x')
# set a title and labels
ax.set_title("Nyquistova křivka")
ax.set_xlabel(r'$Z_{r}\; [k\Omega]$')
ax.set_ylabel(r'$Z_{im}\; [k\Omega]$')

# show a legend
ax.legend()

# show the plot
plt.tight_layout()
plt.show()

# save the plot as a file
fig.savefig('plot12.png')

# now plot only data 1 as a new plot 
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(data['Zr'], -data['Zim'], label='Vzorek 1', marker='x')
ax.set_xlabel(r'$Z_{r}\; [k\Omega]$')
ax.set_ylabel(r'$Z_{im}\; [k\Omega]$') 
ax.set_title("Nyquistova křivka")
ax.legend()
plt.tight_layout()
plt.show()
fig.savefig('plot1.png')

fig, ax = plt.subplots(figsize=(5, 3))
resistance1 = np.sqrt(data['Zr']**2 + data['Zim']**2)
resistance2 = np.sqrt(data2['Zr']**2 + data2['Zim']**2)
resistance3 = np.sqrt(data3['Zr']**2 + data3['Zim']**2)

ax.plot(data2['F'], resistance2, label='Vzorek 2', marker='x')
ax.plot(data3['F'], resistance3, label='Vzorek 3', marker='x')
ax.set_xscale('log')
ax.set_xlabel(r'$f\; [Hz]$')
ax.set_ylabel(r'$|Z|\; [k\Omega]$')
ax.set_title("Závislost impedance na frekvenci")
ax.legend()
plt.tight_layout()
plt.show()
fig.savefig('plot23_resistance.png')

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(data['F'], resistance1, label='Vzorek 1', marker='x')
ax.set_xscale('log')
ax.set_xlabel(r'$f\; [Hz]$')
ax.set_ylabel(r'$|Z|\; [k\Omega]$')
ax.set_title("Závislost impedance na frekvenci")
ax.legend()
plt.tight_layout()
plt.show()
fig.savefig('plot1_resistance.png')


# can you put all the plots that i done into one figure? on a A4 paper?
# Define colors for each "vzorek"
color_vzorek2 = 'blue'
color_vzorek3 = 'green'
color_vzorek1 = 'red'

# yes, you can use the subplots function to create a grid of plots
fig, ax = plt.subplots(2, 2, figsize=(8.27, 11.69))
# plot them, Zr is x and Zim is y
ax[0, 0].plot(data2['Zr'], -data2['Zim'], label='Vzorek 2', marker='x', color=color_vzorek2)
ax[0, 0].plot(data3['Zr'], -data3['Zim'], label='Vzorek 3', marker='x', color=color_vzorek3)
ax[0, 0].set_title("Nyquistova křivka")
ax[0, 0].set_xlabel(r'$Z_{r}\; [k\Omega]$')
ax[0, 0].set_ylabel(r'$Z_{im}\; [k\Omega]$')
ax[0, 0].legend()

ax[0, 1].plot(data['Zr'], -data['Zim'], label='Vzorek 1', marker='x', color=color_vzorek1)
ax[0, 1].set_xlabel(r'$Z_{r}\; [k\Omega]$')
ax[0, 1].set_ylabel(r'$Z_{im}\; [k\Omega]$')
ax[0, 1].set_title("Nyquistova křivka")
ax[0, 1].legend()

ax[1, 0].plot(data2['F'], resistance2, label='Vzorek 2', marker='x', color=color_vzorek2)
ax[1, 0].plot(data3['F'], resistance3, label='Vzorek 3', marker='x', color=color_vzorek3)
ax[1, 0].set_xscale('log')
ax[1, 0].set_xlabel(r'$f\; [Hz]$')
ax[1, 0].set_ylabel(r'$|Z|\; [k\Omega]$')
ax[1, 0].set_title("Závislost impedance na frekvenci")
ax[1, 0].legend()

ax[1, 1].plot(data['F'], resistance1, label='Vzorek 1', marker='x', color=color_vzorek1)
ax[1, 1].set_xscale('log')
ax[1, 1].set_xlabel(r'$f\; [Hz]$')
ax[1, 1].set_ylabel(r'$|Z|\; [k\Omega]$')
ax[1, 1].set_title("Závislost impedance na frekvenci")
ax[1, 1].legend()

plt.tight_layout()
plt.show()
# pdf is a vector format, so it is better for printing
fig.savefig('all_plots.pdf')



'''