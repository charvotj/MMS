import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def main():
    #plot_calibratuion_curve()
    #plot_two_barriers()
    plot_reflectance()

def load_excel(path:str)->pd.DataFrame:
    df = pd.read_excel(path, skiprows=3, usecols='G:I', names=['t', 'u', 'db'])
    return df

def load_t_v(path:str)->float:
    t = pd.read_excel(path, usecols='D', nrows=1, skiprows=4).iloc[0, 0]
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

    # Setup plot axes
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    # Plot data
    lines = []  # To keep track of line objects for legend
    for i, material in enumerate(materials):
        xs, ys = zip(*plot_data[material])
        if material == 'deska':
            # Plot 'deska' on secondary Y-axis
            line, = ax2.plot(xs, ys, 'x-', color=colors[i], label=material)
        else:
            # Plot other materials on primary Y-axis
            line, = ax1.plot(xs, ys, 'x-', color=colors[i], label=material)
        lines.append(line)
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('Max Reflectance')
    ax2.set_ylabel('Max Reflectance (Deska)', color='red')
    # Combine legends
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='best')

    plt.show()


def plot_two_barriers():
    df_white = load_excel('prekazky15cm.xlsx')
    df_black = load_excel('prekazky30cm.xlsx')
    df_bw = load_excel('prekazky15cma30cm.xlsx')

    plt.plot(df_white['t'], df_white['u'], label='Bílá překážka')
    plt.plot(df_black['t'], df_black['u'], label='Černá překážka')
    plt.plot(df_bw['t'], df_bw['u'], label='Obě překážky')
    plt.xlabel('t [s]')
    plt.ylabel('u [V]')
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
    plt.show()

def make_regression(x_data, y_data):
    # Perform linear regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    reg_data = slope * np.array(x_data) + intercept
    return reg_data


if __name__ == '__main__':
    main()