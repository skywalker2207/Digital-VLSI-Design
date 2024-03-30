import pandas as pd

def single_pmos(width, voltage, A):
    Isub = 0 
    Ib = 0
    Igate = 0 
    LeakPower = 0
    
    filename = 'output_poff.csv' if A == 1 else 'output_pon.csv'
    
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
    Isub = (nrow['I(Vs)']) if A == 1 else 0  # Isub is non-zero only when PMOS is off
    Ib = (nrow['I(Vb)'])
    
    LeakPower = voltage * (abs(Isub) + abs(Igate) + abs(Ib))  
    return LeakPower, Isub, Ib, Igate


def and_stack_pmos( N, A, B):
	Isub=0
	Ib=0 
	Ig=0 
	LeakPower=0 
    
	df=pd.read_csv('./32nm_LP_pstack_AandBp.csv')
	if (A == 0 & B == 0) or (A == 0 & B == 1):
		LeakPowera, Isuba, Iba, Iga = single_pmos( N, 0.9, A)
		LeakPowerb, Isubb, Ibb, Igb = single_pmos( N, 0.9, B)
	else:
		row = df.loc[(df['Width'] == (float(N)*22e-9))  & (df['Va'] == A*0.9) & (df['Vb'] == B*0.9)]
		vint = round(abs(row.iloc[0]['Vint']), 2)
		LeakPowera, Isuba, Iba, Iga = single_pmos( N, round((0.9-vint), 2), A)
		LeakPowerb, Isubb, Ibb, Igb = single_pmos( N, vint , B)
	
	LeakPower = LeakPowera + LeakPowerb
	Isub = Isuba + Isubb
	Ib = Iba + Ibb
	Ig = Iga + Igb	
	
	return LeakPower, Isub, Ib, Ig


try:
    A = int(input('What is the input signal level? Enter 1 for off and 0 for on: '))
    B = int(input('What is the input signal level? Enter 1 for off and 0 for on: '))
    width = input('What is the pmos width? ')  # Accept width as string
    temp = float(input('What is the temperature of operation? '))
    
    if temp != 25:
        print("Temperature other than 25°C is not supported.")
        exit()
except ValueError:
    print("Invalid input. Please enter numerical values.")
    exit()

result = and_stack_pmos(width,A,B)

if result is not None:
    LeakPower, Isub, Ib, Ig = result
    print("\nThe leakage currents are:\n")
    print(f"Subthreshold current = {Isub}\n")
    print(f"Gate Leakage current = {Ig}\n")
    print(f"Body Leakage current = {Ib}\n")
    print(f"Leakage Power = {LeakPower}\n\n")
		
