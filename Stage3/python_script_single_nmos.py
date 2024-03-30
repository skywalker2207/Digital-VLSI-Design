import pandas as pd

def single_nmos(width, voltage, A):
    Isub = 0 
    Ib = 0
    Igate = 0 
    LeakPower = 0
    
    filename = 'output_non.csv' if A == 1 else 'output_noff.csv'
    
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return
    
    df['Width'] = df['Width'].astype(str)   # Convert width to string and add 'w'
    N_str = str(int(width)) + 'w'
    df_width = df[df['Width'] == N_str]
    
    if df_width.empty:
        print(f"No data found for width {width}w.")
        return
    
    row = df_width[(df_width['step'] == voltage)]
    
    if row.empty:
        print(f"No data found for width {width}w and voltage {voltage}.")
        return
    
    nrow = row.iloc[0]
    
    Igate = (nrow['I(Vg)'])
    Isub = (nrow['I(Vs)']) if A == 0 else 0  # Isub is non-zero only when PMOS is off
    Ib = (nrow['I(Vb)'])
    
    LeakPower = voltage * (abs(Isub) + abs(Igate) + abs(Ib))  
    return LeakPower, Isub, Ib, Igate

try:
    A = int(input('What is the input signal level? Enter 1 for on and 0 for off: '))
    width = input('What is the nmos width? ')  # Accept width as string
    voltage = float(input('What is the supply voltage step level? '))
    temp = float(input('What is the temperature of operation? '))
    
    if temp != 25:
        print("Temperature other than 25°C is not supported.")
        exit()
except ValueError:
    print("Invalid input. Please enter numerical values.")
    exit()

result = single_nmos(width, voltage, A)

if result is not None:
    LeakPower, Isub, Ib, Ig = result
    print("\nThe leakage currents are:\n")
    print(f"Subthreshold current = {Isub}\n")
    print(f"Gate Leakage current = {Ig}\n")
    print(f"Body Leakage current = {Ib}\n")
    print(f"Leakage Power = {LeakPower}\n\n")
