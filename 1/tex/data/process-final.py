import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def main():
    # combined_plots()
    # plot_calibratuion_curve()
    plot_all_dist()
    plot_calibration_curve_YX()
    plot_two_barriers()
    plot_reflectance()

def load_excel(path:str)->pd.DataFrame:
    df = pd.read_excel('1/tex/data/'+path, skiprows=3, usecols='G:I', names=['t', 'u', 'db'])
    return df

def load_t_v(path:str)->float:
    t = pd.read_excel('1/tex/data/'+path, usecols='D', nrows=1, skiprows=4).iloc[0, 0]
    v = 331.6+t*0.61 
    return t, v

#Já , pod je gpt lepsi
'''def plot_reflectance():
    plt.figure()
    degrees = {'0': 0, '22,5':22.5, '45':45, '67,5': 67.5}
    materials = ['deska', 'lispena', 'profilpena']
    colors = ['red', 'blue', 'green']  # Add colors for each material
    for degree in degrees.keys():
        for i, material in enumerate(materials):
            df = load_excel(f'odrazivost/{material}{degree}deg.xlsx')
            print(f'{degree}_{material}')
            print(df['u'].max())
            print(degrees[degree])
            if degree == '0':
                plt.plot(degrees[degree], df['u'].max(), 'o', label=material, color=colors[i])  # Use color from the colors list
            else:
                plt.plot(degrees[degree], df['u'].max(), 'o', color=colors[i])  # Use color from the colors list
    plt.xlabel('Degree')
    plt.ylabel('Max Reflectance')
    plt.legend(materials)
    plt.show()'''

#GPT prepsal
def plot_reflectance():
    plt.figure()
    degrees = {'0': 0, '22,5': 22.5, '45': 45, '67,5': 67.5}
    materials = ['deska', 'lispena', 'profilpena']
    colors = ['red', 'blue', 'green']  # Assign colors for each material
    # Initialize data storage
    plot_data = {material: [] for material in materials}
    # Load data
    for degree in degrees.keys():
        for i, material in enumerate(materials):
            df = load_excel(f'odrazivost/{material}{degree}deg.xlsx')
            max_reflectance = df['u'].max()
            plot_data[material].append((degrees[degree], max_reflectance))
            #print(f"Max reflectance for {material}: {max_reflectance}")

    # Setup plot axes
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    # Plot data
    lines = []  # To keep track of line objects for legend
    for i, material in enumerate(materials):
        xs, ys = zip(*plot_data[material])
        if material == 'deska':
            # Plot 'deska' on secondary Y-axis
            line, = ax2.plot(xs, ys, 'x-', color=colors[i], label=material.replace('deska', 'Pevná deska').replace('lispena', 'Lisovaná akustická pěna').replace('profilpena', 'Profilovaná akustická pěna -- troj.'))
        else:
            # Plot other materials on primary Y-axis
            line, = ax1.plot(xs, ys, 'x-', color=colors[i], label=material.replace('deska', 'Pevná deska').replace('lispena', 'Lisovaná akustická pěna').replace('profilpena', 'Profilovaná akustická pěna -- troj.'))
        lines.append(line)
    ax1.set_xlabel('Stupně')
    ax1.set_ylabel('Odrazivost U [mV]')
    ax2.set_ylabel('Odrazivost U [mV] (Deska)', color='red')
    # Combine legends
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='best')

    # Print table
    temp_df = {'material':[],'degree':[],'reflektance':[],'u':[]}
    print("Material\tDegree\tReflectance\t%")
    for material in materials:
        for degree, reflectance in plot_data[material]:
            percent = (reflectance / plot_data['deska'][0][1]) * 100
            print(f"{material}\t{degree}\t{reflectance}\t{percent:.2f}%")
            temp_df['material'].append(str(material))
            temp_df['degree'].append(float(degree))
            temp_df['u'].append(float(reflectance))
            temp_df['reflektance'].append(float(percent))

    latex_data=pd.DataFrame({
        "Materiál":temp_df['material'],
        "$\\alpha [\\unit{{\\degree}}]$":temp_df['degree'],
        "$U_{{max}}$ [\\unit{{\\mV}}]":temp_df['u'],
        "R [\\unit{{\\percent}}]":temp_df['reflektance'],
        # "$p_{{out}} [\\unit{{\\kilo\\pascal}}]$":data['mpx_kpa_with_error'],
        # "$\\Delta_{{p}} [\\unit{{\\kilo\\pascal}}]$":data['Delta_p'],
        # "$\\delta_{{ref}} [\\unit{{\\percent}}]$":data['delta_p'],
    })

    latex_table = latex_data.to_latex(index=False, 
                            float_format="%.2f",
                            decimal=',')
    
    latex_table = latex_table.replace('deska', 'Pevná deska').replace('lispena', 'Lisovaná akustická pěna').replace('profilpena', 'Profilovaná akustická pěna -- trojúhelník')
    with open('1/tex/tables/reflektance.tex','w') as f:
        f.write(latex_table)

    plt.savefig('1/tex/img/graf4.pdf')
    plt.show()


def plot_calibration_curve_YX():
    t = []
    v = []
    df = {}
    
    for i in range(1, 6):
        path = f'{i}0cm.xlsx'
        df[i] = load_excel(path)  
        t_val, v_val = load_t_v(path) 
        t.append(t_val)
        v.append(v_val)
    
    max_t = []
    l = []
    real_l = [10, 20, 30, 40, 50]
    for i in range(1, 6):
        max_t_val = df[i]['t'][df[i]['u'].idxmax()]
        max_t.append(max_t_val)
        # l.append((max_t_val / v[i-1]) * 10)
        l.append((max_t_val*1e-6*v[i-1]*100/2))
    
    # Plot the calibration curve with switched axes
    plt.plot(l, real_l, marker='x', linestyle='', label='Kalibrační body')
    
    # Plot regression with switched axes
    coefficients = np.polyfit(l, real_l, 1)  # Note the switch in order
    regression_line = np.polyval(coefficients, l)
    plt.plot(l, regression_line, color='blue', label='Lineární regrese', linestyle='--')
    
    # Adjust the annotation to reflect the new axes orientation
    plt.annotate("regrese" + f"= {coefficients[0]:.3f}"+ r"$\cdot l_{mereno}$" + f" + {coefficients[1]:.3f}", 
                 xy=(0.1, 0.9), xycoords='axes fraction', 
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    
    # Swap the labels
    plt.ylabel(r'$\mathrm{ĺ_{nastaveno}}$ [cm]')
    plt.xlabel(r'$\mathrm{ĺ_{mereno}}$ [cm]')
    # plt.grid()
    plt.legend(loc='lower right')
    
    plt.savefig('1/tex/img/graf2.pdf')
    plt.show()



def plot_two_barriers():
    df_white = load_excel('prekazky15cm.xlsx')
    df_black = load_excel('prekazky30cm.xlsx')
    df_bw = load_excel('prekazky15cma30cm.xlsx')

    plt.plot(df_white['t'], df_white['u'], label='Bílá překážka')
    plt.plot(df_black['t'], df_black['u'], label='Černá překážka')
    plt.plot(df_bw['t'], df_bw['u'], label='Obě překážky')
    plt.xlabel('t [us]')
    plt.ylabel('U [mV]')
    plt.legend()
    
    plt.savefig('1/tex/img/graf3.pdf')
    plt.show()


def plot_all_dist():
    df_10 = load_excel('10cm.xlsx')
    df_10['l'] = df_10['t']*1e-6*335*100/2
    plt.plot(df_10['t'], df_10['u'], label='10cm')

    df_20 = load_excel('20cm.xlsx')
    df_20['l'] = df_20['t']*1e-6*335*100/2
    plt.plot(df_20['t'], df_20['u'], label='20cm')

    df_30 = load_excel('30cm.xlsx')
    df_30['l'] = df_30['t']*1e-6*335*100/2
    plt.plot(df_30['t'], df_30['u'], label='30cm')

    df_40 = load_excel('40cm.xlsx')
    df_40['l'] = df_40['t']*1e-6*335*100/2
    plt.plot(df_40['t'], df_40['u'], label='40cm')

    df_50 = load_excel('50cm.xlsx')
    df_50['l'] = df_50['t']*1e-6*335*100/2
    plt.plot(df_50['t'], df_50['u'], label='50cm')

    plt.xlabel('l [cm]')
    plt.ylabel('U [mV]')
    plt.legend()
    
    plt.show()


def plot_calibratuion_curve():
    t = []
    v = []
    df = {}
    
    for i in range(1, 6):
        path = f'{i}0cm.xlsx'
        df[i] = load_excel(path)
        t_val, v_val = load_t_v(path)
        t.append(t_val)
        v.append(v_val)
    
    max_t = []
    l = []
    real_l = [10, 20, 30, 40, 50]
    for i in range(1, 6):
        max_t_val = df[i]['t'][df[i]['u'].idxmax()]
        max_t.append(max_t_val)
        l.append((max_t_val / v[i-1]) * 10)
    #print(max_t)
    print(l)
    plt.plot(real_l, l, marker='x', linestyle='', label='Data')
    # Plot regression
    plt.plot(real_l, make_regression(real_l, l), color='blue', label='Lineární regrese', linestyle='--') 
    coefficients = np.polyfit(real_l, l, 1) 
    plt.annotate(r"$l_{nastaveno}$" + f"= {coefficients[0]:.3f}"+ r"$\cdot l_{mereno}$" + f"{coefficients[1]:.3f}", xy=(0.1, 0.9), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    plt.xlabel(r'$\mathrm{ĺ_{nastaveno}}$ [cm]')
    plt.ylabel(r'$\mathrm{ĺ_{mereno}}$ [cm]')
    
    plt.savefig('1/tex/img/graf1.pdf')
    plt.show()

    latex_data=pd.DataFrame({
        "l [m]":[float(l) for l in real_l],
        "t [ms]$":[float(l) for l in max_t],
        # "R [\\unit{{\\percent}}]":temp_df['reflektance'],
        # "$p_{{out}} [\\unit{{\\kilo\\pascal}}]$":data['mpx_kpa_with_error'],
        # "$\\Delta_{{p}} [\\unit{{\\kilo\\pascal}}]$":data['Delta_p'],
        # "$\\delta_{{ref}} [\\unit{{\\percent}}]$":data['delta_p'],
    })

    latex_table = latex_data.transpose().to_latex(header=None,
                            index=False, 
                            float_format="%.0f",
                            decimal=',',
                            )
    
    with open('1/tex/tables/kalibrace.tex','w') as f:
        f.write(latex_table)

def combined_plots():
    fig, axs = plt.subplots(3, 1, figsize=(8.27, 11.69))  # A4 size in inches

    # Plot 2: Calibration Curve YX
    t = []
    v = []
    df = {}
    for i in range(1, 6):
        path = f'{i}0cm.xlsx'
        df[i] = load_excel(path)  
        t_val, v_val = load_t_v(path) 
        t.append(t_val)
        v.append(v_val)
    
    max_t = []
    l = []
    real_l = [10, 20, 30, 40, 50]
    for i in range(1, 6):
        max_t_val = df[i]['t'][df[i]['u'].idxmax()]
        max_t.append(max_t_val)
        l.append((max_t_val / v[i-1]) * 10)
    
    coefficients = np.polyfit(l, real_l, 1)
    regression_line = np.polyval(coefficients, l)
    axs[0].plot(l, real_l, marker='x', linestyle='', label='Data')
    axs[0].plot(l, regression_line, color='blue', label='Lineární regrese', linestyle='--')
    axs[0].annotate(r"$l_{nastaveno}$" + f"= {coefficients[0]:.3f}"+ r"$\cdot l_{mereno}$" + f" + {coefficients[1]:.3f}", 
                xy=(0.1, 0.88), xycoords='axes fraction', 
                bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))
    axs[0].set_xlabel(r'$\mathrm{l_{nastaveno}}$ [cm]')
    axs[0].set_ylabel(r'$\mathrm{l_{mereno}}$ [cm]')
    axs[0].set_title('Graf 1: Kalibrační křivka dálkoměru')
    axs[0].grid()

    # Plot 3: Two Barriers
    df_white = load_excel('prekazky15cm.xlsx')
    df_black = load_excel('prekazky30cm.xlsx')
    df_bw = load_excel('prekazky15cma30cm.xlsx')
    axs[1].plot(df_white['t'], df_white['u'], label='Bílá překážka')
    axs[1].plot(df_black['t'], df_black['u'], label='Černá překážka')
    axs[1].plot(df_bw['t'], df_bw['u'], label='Obě překážky')
    axs[1].set_xlabel('t [s]')
    axs[1].set_ylabel('U [V]')
    axs[1].legend(loc='best')
    axs[1].set_title('Graf 2: Průběhy měření vzdálenosti dvou předmětů')
    axs[1].grid()

    # Plot 1: Reflectance
    degrees = {'0': 0, '22,5': 22.5, '45': 45, '67,5': 67.5}
    materials = ['deska', 'lispena', 'profilpena']
    colors = ['red', 'blue', 'green']
    plot_data = {material: [] for material in materials}
    for degree in degrees.keys():
        for i, material in enumerate(materials):
            df = load_excel(f'odrazivost/{material}{degree}deg.xlsx')
            max_reflectance = df['u'].max()
            plot_data[material].append((degrees[degree], max_reflectance))
    
    ax1 = axs[2]
    ax2 = ax1.twinx()
    lines = []
    for i, material in enumerate(materials):
        xs, ys = zip(*plot_data[material])
        if material == 'deska':
            line, = ax2.plot(xs, ys, 'x-', color=colors[i], label=material)
        else:
            line, = ax1.plot(xs, ys, 'x-', color=colors[i], label=material)
        lines.append(line)
    ax1.set_xlabel(r'$\mathrm{Úhel dopadu}$ [°]')
    ax1.set_ylabel('Odrazivost U [mV]')
    ax2.set_ylabel('Odrazivost U [mV] (Deska)', color='red')
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower left')
    ax1.set_title('Graf 3: Závislost odrazivosti na úhlu a materiálu reflektoru')
    ax1.grid()

    plt.tight_layout()
    plt.savefig('1/tex/img/combined_plots.pdf')
    #plt.show()



def make_regression(x_data, y_data):
    # Perform linear regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    reg_data = slope * np.array(x_data) + intercept
    return reg_data


if __name__ == '__main__':
    main()
#    
    

