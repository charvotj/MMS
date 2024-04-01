import pandas as pd
import numpy as np
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


def procces_data(filename:str):
    # Read the CSV file, skipping the first two rows
    # and considering the third row as the header
    data = pd.read_csv(filename, skiprows=2)

    # Convert ALMEMO pressure to kPa
    data['p_alm_kpa']=0.1*data['p_alm']
    # Calculate MPX4115A pressure (kPa) according to datasheet
    # Datasheet transfer function:
    # V_out = V_S * (P*0.009 - 0.095) +- (Pressure Error * Temp Error * 0.009 * V_S)
    # V_out = V_S * ((P*0.009 - 0.095) +- (Pressure Error * Temp Error * 0.009))
    # V_out = V_S * (0.009(P+- (Pressure Error * Temp Error)) - 0.095)
    # V_out / V_S + 0.095 = 0.009(P+- (Pressure Error * Temp Error))
    # P +- (Pressure Error * Temp Error) = (V_out / V_S + 0.095) / 0.009
    v_s = 5.0 # V
    data['mpx_kpa_with_error'] = ((data['v_out'] / v_s) + 0.095) / 0.009

    # Calculate absolute and relative error
    # abs_error [kPa] = p_sensor - p_alm [kPa]
    data['Delta_p'] = data['mpx_kpa_with_error'] - data['p_alm_kpa']
    # rel_error [%] = abs_error / p_alm * 100
    data['delta_p'] = data['Delta_p'] / data['p_alm_kpa'] * 100

    # Display the data
    print(data)

    return data

def make_regresion(x_data,y_data):
    # Perform linear regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    reg_data = slope * x_data + intercept
    return [reg_data, slope, intercept]

def make_first_plot(data):
    x_data = data['p_alm_kpa']
    y_data = data['v_out']
    # Plot the data
    plt.plot(x_data, y_data, marker='x', linestyle='', label='Data')
    # Plot regression
    regrese = make_regresion(x_data,y_data)
    plt.plot(x_data, regrese[0] , color='red', label=f'regrese=${regrese[1]:.3f}'+r'\cdot p_{ref}+'+f'{regrese[2]:.3f}$')  
    plt.xlabel(r'$p_{ref}$ [kPa]')
    plt.ylabel(r'$V_{out}$ [V]')
    plt.grid(True)  # Add gridlines
    plt.legend()
    plt.savefig("4/tex/img/graf-1.pdf")
    plt.show()

def make_second_plot(data):
    x_data = data['p_alm_kpa']
    y_data = data['mpx_kpa_with_error']
    tolerance = [1.5]
    # Plot the data
    plt.errorbar(x_data, y_data,yerr=tolerance,marker='x', linestyle='', label='Data',ecolor='lightblue')
    # Plot regression
    regrese = make_regresion(x_data,y_data)
    plt.plot(x_data, regrese[0], color='red', label=f'regrese=${regrese[1]:.3f}'+r'\cdot p_{ref}+'+f'{regrese[2]:.3f}$')  
    plt.xlabel(r'$p_{ref}$ [kPa]')
    plt.ylabel(r'$p_{out} \pm 1.5$ [kPa]')
    plt.grid(True)  # Add gridlines
    plt.legend()
    plt.savefig("4/tex/img/graf-2.pdf")
    plt.show()

def make_third_plot(data):
    x_data = data['p_alm_kpa']
    y_data = data['Delta_p']
    tolerance = [1.5]
    y2_data = data['delta_p']
    y2_err = abs((data['Delta_p']+1.5 / data['p_alm_kpa'] * 100)-(data['Delta_p']-1.5 / data['p_alm_kpa'] * 100))
    # Plot the data
    fig, ax1 = plt.subplots()
    ax1.plot(x_data, y_data, marker='x', linestyle='', label='Abs. chyba')
    # Plot regression
    regrese = make_regresion(x_data,y_data)
    ax1.plot(x_data, regrese[0], color='red', label=f'regrese=${regrese[1]:.3f}'+r'\cdot p_{ref}+'+f'{regrese[2]:.3f}$')  
    ax1.set_xlabel(r'$p_{ref}$ [kPa]')
    ax1.set_ylabel(r'$\Delta_{p}$ [kPa]')
    ax1.grid(True)  # Add gridlines
    ax1.legend(loc='lower left')

    # Creating a second y-axis
    ax2 = ax1.twinx()
    ax2.errorbar(x_data, y2_data,yerr=y2_err, color='green',ecolor='lightgreen',linestyle='',marker='+', label='Rel. chyba')
    ax2.axhline(y=1.5,linestyle='--',color='green', label='Tolerance z kat. listu')
    ax2.axhline(y=-1.5,linestyle='--',color='green')
    ax2.set_ylabel(r'$\delta_{p}$ [\%]', color='green')
    ax2.legend(loc='upper right')

    plt.savefig("4/tex/img/graf-3.pdf")
    plt.show()


def make_latex_table(data:pd.DataFrame,filename):
    latex_data=pd.DataFrame({
        "$p_{{ref}} [\\unit{{\\milli\\bar}}]$":data['p_alm'],
        "$p_{{ref}} [\\unit{{\\kilo\\pascal}}]$":data['p_alm_kpa'],
        "$U_{{out}} [\\unit{{\\volt}}]$":data['v_out'],
        "$p_{{out}} [\\unit{{\\kilo\\pascal}}]$":data['mpx_kpa_with_error'],
        "$\\Delta_{{p}} [\\unit{{\\kilo\\pascal}}]$":data['Delta_p'],
        "$\\delta_{{ref}} [\\unit{{\\percent}}]$":data['delta_p'],
    })

    latex_table = latex_data.to_latex(index=False, 
                            float_format="%.3f",
                            decimal=',')
    
    with open(filename,'w') as f:
        f.write(latex_table)

def main():
    data = procces_data('4/tex/data/data4.csv')
    make_latex_table(data,'4/tex/tables/hodnoty.tex')
   
    make_first_plot(data)
    make_second_plot(data)
    make_third_plot(data)
    


if __name__ == "__main__":
    main()
