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
    # Budeš si muset asi upravit cesty k input output souborům
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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



def make_regression(x_data, y_data):
    # Perform linear regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    reg_data = slope * np.array(x_data) + intercept
    return [reg_data, coefficients]


if __name__ == "__main__":
    main()