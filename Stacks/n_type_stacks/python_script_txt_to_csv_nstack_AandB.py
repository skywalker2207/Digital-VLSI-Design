import pandas as pd

with open(r'32nm_LP_nstack_AandBn', 'r') as file:
    read_file = file.read()

    read_file=read_file.replace('  ',' ')
    
with open(r'32nm_LP_nstack_AandBn', 'w') as file:    
    file.write(read_file)
        
print("Extra Spaces Removed")

LP_32nm_nstack_AandBn=pd.read_table('32nm_LP_nstack_AandBn', header=None, sep=' ')
LP_32nm_nstack_AandBn=LP_32nm_nstack_AandBn.dropna(axis=1)
LP_32nm_nstack_AandBn.columns=['Temperature','Width','Temperature1','Vdd','Temperature2','Va','Temperature3','Vb','Temperature4','Vint',]
LP_32nm_nstack_AandBn=LP_32nm_nstack_AandBn.drop(['Temperature1','Temperature2','Temperature3','Temperature4'],axis=1)
LP_32nm_nstack_AandBn.to_csv('32nm_LP_nstack_AandBn.csv',index = None)

#print(Nmos_off_32nm_LP_Wmin)
print('CSV File created successfully.')
