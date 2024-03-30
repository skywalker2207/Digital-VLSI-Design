import pandas as pd

with open(r'32nm_LP_pstack_AandBp', 'r') as file:
    read_file = file.read()

    read_file=read_file.replace('  ',' ')
    
with open(r'32nm_LP_pstack_AandBp', 'w') as file:    
    file.write(read_file)
        
print("Extra Spaces Removed")

LP_32nm_pstack_AandBp=pd.read_table('32nm_LP_pstack_AandBp', header=None, sep=' ')
LP_32nm_pstack_AandBp=LP_32nm_pstack_AandBp.dropna(axis=1)
LP_32nm_pstack_AandBp.columns=['Temperature','Width','Temperature1','Vdd','Temperature2','Va','Temperature3','Vb','Temperature4','Vint']
LP_32nm_pstack_AandBp=LP_32nm_pstack_AandBp.drop(['Temperature1','Temperature2','Temperature3','Temperature4'],axis=1)
LP_32nm_pstack_AandBp.to_csv('32nm_LP_pstack_AandBp.csv',index = None)

#print(Nmos_off_32nm_LP_Wmin)
print('CSV File created successfully.')
