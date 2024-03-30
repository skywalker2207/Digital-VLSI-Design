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
    
    Igate = abs(nrow['I(Vg)'])
    Isub = abs(nrow['I(Vs)']) if A == 1 else 0  # Isub is non-zero only when PMOS is off
    Ib = abs(nrow['I(Vb)'])
    
    LeakPower = voltage * (abs(Isub) + abs(Igate) + abs(Ib))  
    return LeakPower, Isub, Ib, Igate


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
    
    Igate = abs(nrow['I(Vg)'])
    Isub = abs(nrow['I(Vs)']) if A == 0 else 0  # Isub is non-zero only when PMOS is off
    Ib = abs(nrow['I(Vb)'])
    
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
		row = df.loc[(df['Width'] == (float(N)*32e-9))  & (df['Va'] == A*0.9) & (df['Vb'] == B*0.9)]
		vint = round(abs(row.iloc[0]['Vint']), 2)
		LeakPowera, Isuba, Iba, Iga = single_pmos( N, round((0.9-vint), 2), A)
		LeakPowerb, Isubb, Ibb, Igb = single_pmos( N, vint , B)
	
	LeakPower = LeakPowera + LeakPowerb
	Isub = Isuba + Isubb
	Ib = Iba + Ibb
	Ig = Iga + Igb	
	
	return LeakPower, Isub, Ib, Ig


def and_stack_nmos( N, A, B):
	Isub=0 
	Ib=0 
	Ig=0 
	LeakPower=0 
	df=pd.read_csv('./32nm_LP_nstack_AandBn.csv') 
	if (A == 0 & B == 0) or (A == 0 & B == 1): 
		row = df.loc[(df['Width'] == (float(N)*32e-9)) & (df['Va'] == A*0.9) & (df['Vb'] == B*0.9)] 
        
		vint = round(abs(row.iloc[0]['Vint']), 2) 
		LeakPowera, Isuba, Iba, Iga = single_nmos( N, vint, A) 
		LeakPowerb, Isubb, Ibb, Igb = single_nmos( N, round((0.9-vint), 2), B) 
	else:
		LeakPowera, Isuba, Iba, Iga = single_nmos( N, 0.9, A)
		LeakPowerb, Isubb, Ibb, Igb = single_nmos( N, 0.9, B)
	
	LeakPower = LeakPowera + LeakPowerb
	Isub = Isuba + Isubb
	Ib = Iba + Ibb
	Ig = Iga + Igb	
	
	return LeakPower, Isub, Ib, Ig
	
def inv(N, A):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPowerp, Isubp, Ibp, Igp = single_pmos( 2, 0.9, A)  # doubt regarding width
	LeakPowern, Isubn, Ibn, Ign = single_nmos( 1, 0.9, A)
	
	LeakPower = LeakPowerp + LeakPowern
	Isub = Isubp + Isubn
	Ib = Ibp + Ibn
	Ig = Igp + Ign
	
	return LeakPower, Isub, Ib, Ig
	
def nand( N,A, B):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPowerp1, Isubp1, Ibp1, Igp1 = single_pmos(1, 0.9, A)
	LeakPowerp2, Isubp2, Ibp2, Igp2 = single_pmos(1, 0.9, B)
	LeakPowern, Isubn, Ibn, Ign = and_stack_nmos(2, A, B)
	
	LeakPower = LeakPowerp1 + LeakPowerp2 + LeakPowern
	Isub = Isubp1 + Isubp2 + Isubn
	Ib = Ibp1 + Ibp2 + Ibn
	Ig = Igp1 + Igp2 + Ign
	
	return LeakPower, Isub, Ib, Ig
	
def andg(N, A, B):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPower_nand, Isub_nand, Ib_nand, Ig_nand = nand(N, A, B)
	if A == 1 & B == 1:
		LeakPower_inv, Isub_inv, Ib_inv, Ig_inv = inv(N,0)
	else:
		LeakPower_inv, Isub_inv, Ib_inv, Ig_inv = inv(N,1)
	
	LeakPower = LeakPower_nand + LeakPower_inv
	Isub = Isub_nand + Isub_inv
	Ib = Ib_nand + Ib_inv
	Ig = Ig_nand + Ig_inv
	
	return LeakPower, Isub, Ib, Ig	
 
def nor( N,A, B):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPowerp1, Isubp1, Ibp1, Igp1 = single_nmos( 1, 0.9, A)
	LeakPowerp2, Isubp2, Ibp2, Igp2 = single_nmos( 1, 0.9, B)
	LeakPowern, Isubn, Ibn, Ign = and_stack_pmos( 8, A, B)
	
	LeakPower = LeakPowerp1 + LeakPowerp2 + LeakPowern
	Isub = Isubp1 + Isubp2 + Isubn
	Ib = Ibp1 + Ibp2 + Ibn
	Ig = Igp1 + Igp2 + Ign
	
	return LeakPower, Isub, Ib, Ig
	
def org(N, A, B):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPower_nor, Isub_nor, Ib_nor, Ig_nor = nor(N, A, B)
 
	if A == 0 & B == 0:
		LeakPower_inv, Isub_inv, Ib_inv, Ig_inv = inv( N,1)
	else:
		LeakPower_inv, Isub_inv, Ib_inv, Ig_inv = inv(N, 0)
	
	LeakPower = LeakPower_nor + LeakPower_inv
	Isub = Isub_nor + Isub_inv
	Ib = Ib_nor + Ib_inv
	Ig = Ig_nor + Ig_inv
	
	return LeakPower, Isub, Ib, Ig

def cirp(P0,P1,P2,P3,N):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPower_or0, Isub_or0, Ib_or0, Ig_or0 = org(N, P0, P1) 
	LeakPower_or1, Isub_or1, Ib_or1, Ig_or1 = org(N, P2, P3) 
	LeakPower_or2, Isub_or2, Ib_or2, Ig_or2 = org(N, P0 or P1, P2 or P3) 
    	
	LeakPower = LeakPower_or0 + LeakPower_or1+ LeakPower_or2
	Isub = Isub_or1 + Isub_or0+Isub_or2
	Ib = Ib_or0 + Ib_or1+Ib_or2
	Ig = Ig_or0 + Ig_or1+Ig_or2
	
	return LeakPower, Isub, Ib, Ig

def cirg(P0,G0,P1,G1,P2,G2,P3,G3,N):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
	
	LeakPower_and0, Isub_and0, Ib_and0, Ig_and0 = andg(N, G0, G1) 
	LeakPower_and1, Isub_and1, Ib_and1, Ig_and1 = andg(N, G2, G3) 
	LeakPower_and2, Isub_and2, Ib_and2, Ig_and2 = andg(N, G0 and G1, G2 and G3) 
 
	LeakPower_and3, Isub_and3, Ib_and3, Ig_and3 = andg(N, P1, G3) 
	LeakPower_and4, Isub_and4, Ib_and4, Ig_and4 = andg(N, G2, G1) 
	LeakPower_and5, Isub_and5, Ib_and5, Ig_and5 = andg(N, P1 and G3,G2 and G1) 
 
	LeakPower_and6, Isub_and6, Ib_and6, Ig_and6 = andg(N, P2, G3) 
	LeakPower_and7, Isub_and7, Ib_and7, Ig_and7 = andg(N, P2 and G3,G2) 
 
	LeakPower_and8, Isub_and8, Ib_and8, Ig_and8 = andg(N, P3,G3) 
 
   
	LeakPower_or0, Isub_or0, Ib_or0, Ig_or0 = org(N, G0 and G1 and G2 and G3, P1 and G3 and G2 and G1) 
	LeakPower_or1, Isub_or1, Ib_or1, Ig_or1 = org(N, P2 and G3 and G2, P3 and G2) 
	LeakPower_or2, Isub_or2, Ib_or2, Ig_or2 = org(N,(G0 and G1 and G2 and G3) or  ( P1 and G3 and G2 and G1) , (P2 and G3 and G2) or ( P3 and G2) )
    	
	LeakPower = LeakPower_or0 + LeakPower_or1+ LeakPower_or2+LeakPower_and0+LeakPower_and2+LeakPower_and3+LeakPower_and1+LeakPower_and4+LeakPower_and5+LeakPower_and6+LeakPower_and7+LeakPower_and8
	Isub = Isub_or1 + Isub_or0+Isub_or2 + Isub_and0+Isub_and1+Isub_and2+Isub_and3+Isub_and4+Isub_and5+Isub_and6+Isub_and7+Isub_and8
	Ib = Ib_or0 + Ib_or1+Ib_or2 + Ib_and0+Ib_and1+Ib_and2+Ib_and3+Ib_and4+Ib_and5+Ib_and6+Ib_and7+Ib_and8
	Ig = Ig_or0 + Ig_or1+Ig_or2+Ig_and0+Ig_and1+Ig_and2+Ig_and3+Ig_and4+Ig_and5+Ig_and6+Ig_and7+Ig_and8
    
	return LeakPower, Isub, Ib, Ig
 

def circx(P0,G0,P1,G1,P2,G2,P3,G3,C,N):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0

	LeakPower_and0, Isub_and0, Ib_and0, Ig_and0 = andg(N, G0, P0) 

	LeakPower_and1, Isub_and1, Ib_and1, Ig_and1 = andg(N, G0, 1-C) 
	LeakPower_nor, Isub_nor, Ib_nor, Ig_nor = nor(N,P0 and G0, G0 and (1-C)) 
 
	LeakPower = LeakPower_and0+LeakPower_and1+LeakPower_nor
 
	Isub = Isub_and0+Isub_and1+Isub_nor
	Ib = Ib_and0 + Ib_and1  + Ib_nor
	Ig = Ig_and0 + Ig_and1  + Ig_nor 
	
	return LeakPower, Isub, Ib, Ig
 
def circy(P0,G0,P1,G1,P2,G2,P3,G3,C,N):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0

	LeakPower_and0, Isub_and0, Ib_and0, Ig_and0 = andg(N, P1, G1) 
 
	LeakPower_and1, Isub_and1, Ib_and1, Ig_and1 = andg(N, G1, G0) 
	LeakPower_and2, Isub_and2, Ib_and2, Ig_and2 = andg(N, G0 and G1, P0)
 
	LeakPower_and3, Isub_and3, Ib_and3, Ig_and3 = andg(N, G1, G0) 
	LeakPower_and4, Isub_and4, Ib_and4, Ig_and4 = andg(N, G0 and G1, 1-C)

	LeakPower_or0, Isub_or0, Ib_or0, Ig_or0 = org(N,P1 and G1, G0 and G1 and P0) 
	LeakPower_nor1, Isub_nor1, Ib_nor1, Ig_nor1 = nor(N,G1 and G0 and (1-C), ((P1 and G1) or (G0 and G1 and P0) )) 
  
	LeakPower = LeakPower_and0+LeakPower_and1+LeakPower_or0+LeakPower_and3+LeakPower_and4+LeakPower_nor1+LeakPower_and2
 
	Isub = Isub_and0+Isub_and1+Isub_or0 + Isub_and2 +Isub_and3 +Isub_and4 +Isub_nor1
	Ib = Ib_and0 + Ib_and1  + Ib_or0+Ib_nor1+Ib_and2+Ib_and3+Ib_and4
	Ig = Ig_and0 + Ig_and1  + Ig_or0+Ig_nor1+Ig_and2+Ig_and3+Ig_and4 
	
	return LeakPower, Isub, Ib, Ig


def circz(P0,G0,P1,G1,P2,G2,P3,G3,C,N):
	Isub=0 
	Ib=0
	Ig=0 
	LeakPower=0
 
	LeakPower_and0, Isub_and0, Ib_and0, Ig_and0 = andg(N, G0, G1) 
	LeakPower_and1, Isub_and1, Ib_and1, Ig_and1 = andg(N, G2, (1-C)) 
	LeakPower_and2, Isub_and2, Ib_and2, Ig_and2 = andg(N, G0 and G1, G2 and (1-C)) 
 
	LeakPower_and3, Isub_and3, Ib_and3, Ig_and3 = andg(N, P0, G0) 
	LeakPower_and4, Isub_and4, Ib_and4, Ig_and4 = andg(N, G1, G2) 
	LeakPower_and5, Isub_and5, Ib_and5, Ig_and5 = andg(N, P0 and G0,G1 and G2) 
 
	LeakPower_and6, Isub_and6, Ib_and6, Ig_and6 = andg(N, P1, G1) 
	LeakPower_and7, Isub_and7, Ib_and7, Ig_and7 = andg(N, P1 and G1,G2) 
 
	LeakPower_and8, Isub_and8, Ib_and8, Ig_and8 = andg(N, P2,G2) 
 
	LeakPower_or0, Isub_or0, Ib_or0, Ig_or0 = org(N, G0 and G1 and G2 and (1-C), P0 and G0 and G2 and G1) 
	LeakPower_or1, Isub_or1, Ib_or1, Ig_or1 = org(N, P1 and G1 and G2, P2 and G2) 
	LeakPower_nor2, Isub_nor2, Ib_nor2, Ig_nor2 = nor(N,(G0 and G1 and G2 and (1-C)) or  ( P0 and G0 and G2 and G1) , (P1 and G1 and G2) or ( P2 and G2) )
    	
	LeakPower = LeakPower_or0 + LeakPower_or1+ LeakPower_nor2+LeakPower_and0+LeakPower_and2+LeakPower_and3+LeakPower_and1+LeakPower_and4+LeakPower_and5+LeakPower_and6+LeakPower_and7+LeakPower_and8 
	Isub = Isub_or1 + Isub_or0+Isub_nor2 + Isub_and0+Isub_and1+Isub_and2+Isub_and3+Isub_and4+Isub_and5+Isub_and6+Isub_and7+Isub_and8 
	Ib = Ib_or0 + Ib_or1+Ib_nor2 + Ib_and0+Ib_and1+Ib_and2+Ib_and3+Ib_and4+Ib_and5+Ib_and6+Ib_and7+Ib_and8
	Ig = Ig_or0 + Ig_or1+Ig_nor2+Ig_and0+Ig_and1+Ig_and2+Ig_and3+Ig_and4+Ig_and5+Ig_and6+Ig_and7+Ig_and8
	
	return LeakPower, Isub, Ib, Ig 

def circuit(P0,G0,P1,G1,P2,G2,P3,G3,C,N,voltage):
	Isub=0 
	Ib=0 
	Ig=0 
	LeakPower=0
	
	LeakPower_P, Isub_P, Ib_P, Ig_P = cirp( P0,P1,P2,P3,N) 
	LeakPower_G, Isub_G, Ib_G, Ig_G = cirg(P0,G0,P1,G1,P2,G2,P3,G3,N) 
	LeakPower_Cx, Isub_Cx, Ib_Cx, Ig_Cx = circx(P0,G0,P1,G1,P2,G2,P3,G3,C,N) 
	LeakPower_Cy, Isub_Cy, Ib_Cy, Ig_Cy = circy(P0,G0,P1,G1,P2,G2,P3,G3,C,N) 
	LeakPower_Cz, Isub_Cz, Ib_Cz, Ig_Cz = circz(P0,G0,P1,G1,P2,G2,P3,G3,C,N) 
	LeakPower_inv, Isub_inv, Ib_inv, Ig_inv = inv(N, C) 
    
	LeakPower = (LeakPower_P + LeakPower_G + LeakPower_Cx + LeakPower_Cy + LeakPower_Cz+LeakPower_inv )
	Isub = (Isub_P + Isub_G + Isub_Cx + Isub_Cy + Isub_Cz +Isub_inv)/1.5
	Ib = (Ib_P + Ib_G + Ib_Cx + Ib_Cy + Ib_Cz +Ib_inv)
	Ig = (Ig_P + Ig_G + Ig_Cx + Ig_Cy + Ig_Cz+Ig_inv) 
 
	return LeakPower, Isub, Ib, Ig
	

try:
    P0 = int(input('What is the P0 signal level?'))
    G0 = int(input('What is the G0 signal level?'))
    P1 = int(input('What is the P1 signal level?'))
    G1 = int(input('What is the G1 signal level?'))
    P2 = int(input('What is the P2 signal level?'))
    G2 = int(input('What is the G2 signal level?'))
    P3 = int(input('What is the P3 signal level?'))
    G3 = int(input('What is the G3 signal level?'))
    
    C = int(input('What is the C carry value?'))
    
    width = input('What is the nmos width? ')  # Accept width as string
    voltage = float(input('What is the supply voltage step level? '))
    temp = float(input('What is the temperature of operation? '))
    
    if temp != 25:
        print("Temperature other than 25°C is not supported.")
        exit()
except ValueError:
    print("Invalid input. Please enter numerical values.")
    exit()

result = circuit(P0,G0,P1,G1,P2,G2,P3,G3,C,width,voltage)
#result = single_nmos(width,voltage,P0)

if result is not None:
    LeakPower, Isub, Ib, Ig = result
    print("\nThe leakage currents are:\n")
    print(f"Subthreshold current = {Isub}\n")
    print(f"Gate Leakage current = {Ig}\n")
    print(f"Body Leakage current = {Ib}\n")
    print(f"Leakage Power = {LeakPower}\n\n")



 
