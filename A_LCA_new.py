# change direction of the data!
import os
os.chdir(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/py') 

# import funtions and packasum
import pandas as pd
from smop.libsmop import *
import numpy as np

#DATA
#reading data for substrates ( maybe enter by user)
#substrate_data=pd.read_excel("Stoffdaten.xlsx", encoding='unicode-escape',sep=";", decimal=",")
#substrate_data.set_index('type',inplace=True)
#del substrate_data['units']   
# the data has to be optimized...
#create a new table in python where the entered data and the data from excel where combined.
# if there is nothing entered, then the data from excel must choosen

#############################################################################################
#input for growing and data
#USER QUERY

# !!!!create query for used substrates :CCM","Getreidekoerner","GPS","Hirse","Koernermais","Silomais","Zuckerruebe","Ackerfutter","Grassilage","LAPF","Kleegrassilage","Silphie","Getreidestroh","Maisstroh","Huehnertrockenkot","Rinderfestmist","Rinderguelle","Rinderguelle_fest", "Schweinefestmist", "Schweineguelle","Schweineguelle_fest"]
# create a query with drop down or something else where the user could choose the substrate and enter the used mass > S=Substrate
# ask the user if he grows the substrate or does he buys the substrates?
# if he only buys the substrates, he haven't information about the growing process, he should know:
    #dry matter
    #nitrogen content
    #organic dry matter
    # other data you will get from excel, maybe we have to optimize these excel sheet 
# if the user is growing the substrate, then he should enter:
    # dry matter
    # organic dry matter
    # nitrogen content
    # (P,K and other contents)
    # used fertilizer
    # how much fertilizer
    # pesticides
    # Seeds
    # yield 
    # fuel
    # liming  
# if there is no value entered than the values from excel for the substrate should be choose
########################################################################################
df=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Book.xls')
df1=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Book2.xls')
ef=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Emissionsfaktoren.xls')
ef_pro=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/EF_process.xls')

# go on for all data

Substrate1=('cattle slurry') # type of substrate 

print(df['FM'])
print(df['DM'])
print(df['oDM'])
print(df['N'])
print(df['P'])
print(df['K'])
print(df['Fertilizer_N'])
print(df['Fertilizer_P2O5'])
print(df['Fertilizer_K2O'])
print(df['liming'])
print(df['Seed'])
print(df['Pesticides'])
print(df['Harvest_yield'])
print(df['Seed'])
print(df['Fuel'])
print(df['Hectar'])
############

print(df['Methane_yield'])
print(df['Silolosses'])
print(df['Methane_production'])
print(df['Biogas_yield'])
print(df['Biogas_production'])
print(df['Methane_content'])
print(df['TAN'])
print(df['Fugatfaktor'])
print(df['G_TAN'])
print(df['N_Min'])
print(df['HNV'])
print(df['X_N_above'])
print(df['X_AGR_DM'])
print(df['X_N_below'])
print(df['A_above'])
print(df['A_below'])
print(df['X_renew'])
print(df['X_mow'])
print(df['Yield_Duev'])
print(df['Yield_diff'])
print(df['Supp_yield'])
print(df['Redu_yield'])
print(df['EF_seed'])

#create the Substrate allocation  in percent: 

#sum of fresh matter
Sum_FM = sum(df['FM'])
print('Sum_Fm =', Sum_FM)

#Allocation:allo['S1']=FM[S1]/sum(FM(S1:S8))
Allo = df['FM']/Sum_FM
Allo_y = Allo.values.tolist()

df['Allo'] = Allo_y

#sum of hectar
Sum_hectar= sum(df['Hectar'])
print('Sum_hectar =', Sum_hectar)
  
# 1. process  Growing and harvesting Substrates

#methane allocation of all substrates = Substrate allocation * methane_yield

CH4_Allo = df['Allo'] * df['Methane_yield']  #methane allocation
CH4_Allo_y = CH4_Allo.values.tolist()

df['CH4_Allo'] = CH4_Allo_y

#sum of methane allocation
Sum_CH4_Allo= sum(df['CH4_Allo'])
print('Sum_CH4_Allo = ',Sum_CH4_Allo)

# calculation of nitrogen content in each substarte> important for fermentation and residues

N_C = df['N']*df['FM']                    #Nitrogen content* freshmatter input
n_f = N_C.values.tolist()


df['N_C'] = n_f
#sum of Nitrogen content*

Sum_N= sum(df['N_C'])
print('Sum_N_C = ', Sum_N)

N_t = df['N_C']/1000    # Nitrogen content [t] in whole fresh matter
N_t_Y = N_t.values.tolist()

df['N_t'] = N_t_Y

#total ammonium nitrogen TAN > calculation > for more information read Thunene Report

tan_t = (df['N_C']*df['TAN'])/1000     #[TAN_t] total ammonium nitrogen in fresh matter [t]
TAN_t_Y = tan_t.values.tolist()

df['tan_t'] = TAN_t_Y 

TAN_fm = df['tan_t']/df['FM']

# organic nitrogen content
N_org_t = df['N_t']-df['tan_t']       # calculation of organic nitrogen content [t N_org]
N_org_t_Y = N_org_t.values.tolist()

df['N_org_t'] = N_org_t_Y

N_org_FM = (df['N_org_t']*1000)/df['DM']     #[N_org/t FM]# calculation of organic nitrogen content based on 1 ton of fresh mass [kg N_org /tFM]
N_org_FM_Y = N_org_FM.values.tolist()

df['N_org_FM'] = N_org_FM_Y
#please create a dict or dataframe to save all data for the substrates

# importing functions and Emissionfactors wich are needed
from B_Emissionen_Substrate_new import *
os.chdir(r"C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/py") 

# general Emissions
emissionfactors=pd.read_csv("Emissionsfaktoren.csv",usecols=[0,1], encoding='unicode-escape',sep=";", decimal=",", header=None, index_col=0, squeeze=True).to_frame().transpose()

EF_gen=emissionfactors

# emissions for growing substrates
Emissionfactors_growing=pd.read_csv("EF_growing.csv", usecols=[0,1], encoding='unicode-escape',sep=";", decimal=",", header=0, index_col=0, squeeze=True ).to_frame().transpose()

EF_grow=Emissionfactors_growing

# Emissions for transport
emissionfactors_transportation=pd.read_csv("EF_transport.csv", usecols=[0,1], encoding='unicode-escape',sep=";", decimal=",", header=0, index_col=0, squeeze=True ).to_frame().transpose()

EF_tran=emissionfactors_transportation

os.chdir(r"C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/py")
514
402058
#GHG / CO2 emissions for cultivation/growing and harvesting
#emissions of the substrate has to be calculated > therefore the emissionsfactors of growing, transportations and general are neccessary, and the substrate data from excel or user

Substratemissionen=Substrat_Emissionen(substrate_data, EF_grow, EF_tran, EF_gen) # calculations of substrate emissions

# calculation of nitrogenfertilizer of the substrates >requirement of the law DUEV > N_fert is calculatet in BB_Substrat_Emissionen_new > you have to return this variable,so that you can reuse it

N_fert_ha = df['Fertilizer_N']*100000*df['Hectar']            # Calculation of nitrogen fertilizer for the area
N_fert_ha_Y = N_fert_ha.values.tolist()

df['N_fert_ha'] = N_fert_ha_Y

N_fert_sum = sum(df['N_fert_ha'])                              # sum of nitrogen fertilizer
print('N_fert_sum = ',N_fert_sum)

GhG={} #creatio  of dict, to save all results of GHG emission 
GhG['E_N2O_FM'] =multiply(np.array(Substratemissionen.CO2_N2O),Fm) # N2O emissions for the whole fresh matter [kg co2]    
GhG['growing_FM'] = multiply(np.array(Substratemissionen.E_GhG_growing),Fm) # emissions for growing the substartes, unit [[kg CO2/ t FM] * t FM]
GhG['growing_FM'][np.isnan(GhG['growing_FM'])]=0
GhG['growing_FM_sum'] = (sum(GhG['growing_FM'],2)) # sum of emissions for gorwing
# Substratemissionen.CO2_N2O  =   which value I consider? as well as is there two seperate value? Substratemissionen? CO2_N2O?
#Substratemissionen.E_GhG_growing =  which value I consider? as well as is there two seperate value? Substratemissionen? E_GhG_growing?
########################################################################################
#  USER QUERY  CHP 
#define data of CHP (could be enter by user) random values >create a entry field for each variable

P_el = 380     # installed power of CHP
in_year = 2010    #start year
engine_typ = 1  #engine type of used  > GAS-Otto-Motor=1, ignition jet engine=0
no_chp = 1             #quantity of CHP (mostly 1, if there are more than 1 then you have to adjust the query and variables)       
W_fedin=3298774      #energy fed into grid
P_inst =1  #could be enter by user
VBH = W_fedin/ (P_inst)   # FULL USE HOURS (VBH)of CHP calculation or user
year_h=8760             # hours of a year       this is a constant value!!                                   
VBH_pro = VBH / year_h     # Calculation of the percentage hours of use        
eta_el=0.369 #random values > user # electric efficiency of the CHP
P_th=455 # random value > user # thermal power of CHP
P_Burn=1030 # random value > user # Burning Power > whole power of CHP
eta_th=0.44 # random value > user# thermal efficiency of CHP
el_own=0.1 # determine own electricity demand (user)

# calculation how much energy and CH4 is needed for the CHP to reach the full used hours VBH
energy_need = multiply(VBH, P_Burn)
energy_need_el = multiply(energy_need,eta_el[0])
CH4_need = energy_need / (EF_gen.Energiegehalt_CH4[1])

#methane allocation 
#CH4_allo2=(CH4_need/sum_CH4_allo[:,0]) # to check Ch4_allo, compare
#CH4_allo2[np.isnan(CH4_allo2)]=0
 
# please create a dict for saving all the variables of CHP
######################################################################################
# BIOGASprocess
# emissions for biogasprocess (disumter, disumtate storage)
emissionfactors_process=pd.read_csv("EF_process.csv", usecols=[0,1], encoding='unicode-escape',sep=";", decimal=",", header=0, index_col=0, squeeze=True ).to_frame().transpose()
EF_pro=emissionfactors_process

# creation of dict'S
Silo = []
ps={}
reSto={}
dig={} 

##############################################################################################################
#Silo_DM_loss={'S1':558.20, 'S2':580.37, 'S3':343.85,'S4':382.05, 'S5':957.67,'S6':216.82 }
#Silo_oDM_loss={'S1':446.56, 'S2':493.31, 'S3':326.65,'S4':343.85, 'S5':928.94,'S6':199.48 }
#Silo_FM_loss={'S1':5582, 'S2':2348, 'S3':1070,'S4':1188, 'S5':1103,'S6':980 }
#Silo_CH4_m3={'S1':93331, 'S2':122096, 'S3':107797,'S4':109344, 'S5':352625,'S6':71215 }
#Silo_CH4_t={'S1':62.53, 'S2':81.80, 'S3':72.22,'S4':73.26, 'S5':236.25,'S6':47.71 }
#Silo_H2O={'S1':5023.80, 'S2':1767.63, 'S3':725.66,'S4':806.28, 'S5':145.13,'S6':764.11 }
#Silo_Mineral={'S1':111.64, 'S2':87.05, 'S3':17.19,'S4':38.20, 'S5':28.73,'S6':17.34 }

##############################################################################################################
#PS_CH4_E ={'S1':0.125, 'S2':0.122, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_GHG_CH4 = {'S1':3126.59, 'S2':3067.66, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_oDM_t = {'S1':445.66, 'S2':492.57, 'S3':326.65, 'S4':343.85, 'S5':928.94,'S6':199.48}
#PS_DM_T = {'S1':557.30, 'S2':579.63, 'S3':343.85, 'S4':382.05, 'S5':957.67,'S6':216.82}
#PS_FM_t = {'S1':5581.10, 'S2':2347.26, 'S3':1069.51, 'S4':1188.34, 'S5':1102.80,'S6':980.94}
#PS_H20 = {'S1':5023.80, 'S2':1767.63, 'S3':725.66, 'S4':806.28, 'S5':145.13,'S6':764.11}
#PS_E_N2O_d= {'S1':0, 'S2':12.49, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_NO= {'S1':0, 'S2':12.49, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_N2= {'S1':0, 'S2':37.47, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_NH3= {'S1':0, 'S2':55.98, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_N_sum= {'S1':0, 'S2':0.0502, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_N2O_in_Norg= {'S1':0, 'S2':0.0388, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_N_org_t= {'S1':14.24, 'S2':10.28, 'S3':5.24, 'S4':9.98, 'S5':24.03,'S6':1.76}
#PS_TAN_t = {'S1':18.12, 'S2':1.94, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_N_t= {'S1':32.37, 'S2':12.23, 'S3':5.24, 'S4':9.98, 'S5':24.03,'S6':1.76}
#PS_E_N2O_in = {'S1':0, 'S2':0.5598, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_E_N2O = {'S1':0, 'S2':20.49, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#PS_BG = {'S1':169353.50, 'S2':221659.77, 'S3':202528.46, 'S4':206310.82, 'S5':678126.65,'S6':139638.39}
#PS_CH4_m3 = {'S1':93144.42, 'S2':121912.87, 'S3':107797.40, 'S4':109344.73, 'S5':352625.86,'S6':71215.58}
#PS_CH4_t = {'S1':62.40, 'S2':81.68, 'S3':72.22, 'S4':73.26, 'S5':236.25,'S6':47.71}

##############################################################################################################

#reSto_DM_t ={'S1':373.34, 'S2':338.85, 'S3':119.55, 'S4':153.56, 'S5':199.44,'S6':59.21}
#reSto_H2O = {'S1':4991.33, 'S2':1725.14, 'S3':686.07, 'S4':765.96, 'S5':11.32,'S6':736.29}
#resto_FM = {'S1':5469.49, 'S2':2182.96, 'S3':802.134, 'S4':891.26, 'S5':275.701,'S6':784.755} 
#resto_oDM_t = {'S1':261.70, 'S2':251.79, 'S3':102.35, 'S4':115.36, 'S5':170.71,'S6':41.86}
#resto_CH3_E = {'S1':0.1250, 'S2':0.1227, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#resto_NH3_E = {'S1':0, 'S2':0, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#resto_N2O_E = {'S1':0, 'S2':0, 'S3':0, 'S4':0, 'S5':0,'S6':0}
#resto_CH4_t = {'S1':2.87, 'S2':3.75, 'S3':3.32, 'S4':3.37, 'S5':10.86,'S6':2.19}
#resto_TAN = {'S1':22.68, 'S2':5.23, 'S3':2.93, 'S4':5.58, 'S5':13.45,'S6':0.988}
#resto_N = {'S1':32.37, 'S2':12.23, 'S3':5.24, 'S4':9.98, 'S5':24.03,'S6':1.76}
#resto_N_org = {'S1':9.68, 'S2':6.99, 'S3':2.30, 'S4':4.39, 'S5':10.57,'S6':0.77}
#resto_N_Crop = {'S1':0, 'S2':0, 'S3':5.24, 'S4':9.98, 'S5':24.30,'S6':1.76}
#resto_CHP_CH4_use = {'S1':93144.42, 'S2':121912.87, 'S3':107797.40, 'S4':109344.73, 'S5':352625.86,'S6':71215.58}

##############################################################################################################

#dig_H2O_con = {'S1':32.46, 'S2':42.49, 'S3':39.58, 'S4':40.32, 'S5':133.80,'S6':27.81}
#dig_DM_con = {'S1':183.96, 'S2':240.78, 'S3':224.30, 'S4':228.48, 'S5':758.22,'S6':157.61}
#dig_BG_t = {'S1':216.42, 'S2':283.27, 'S3':263.88, 'S4':268.81, 'S5':892.02,'S6':185.42}
#dig_CH4_t = {'S1':59.53, 'S2':77.92, 'S3':68.90, 'S4':69.89, 'S5':225.39,'S6':45.51}
#dig_CH4_E = {'S1':0.595, 'S2':0.779, 'S3':0.689, 'S4':0.698, 'S5':2.253,'S6':0.455}
#dig_CHP_CH4_use = {'S1':58.94, 'S2':77.14, 'S3':68.21, 'S4':69.19, 'S5':223.13,'S6':45.06}
#dig_TAN = {'S1':22.68, 'S2':5.23, 'S3':2.93, 'S4':5.58, 'S5':13.45,'S6':0.98}
#dig_N_t = {'S1':32.37, 'S2':12.23, 'S3':5.24, 'S4':9.98, 'S5':24.03,'S6':1.76}
#dig_N_org = {'S1':9.68, 'S2':6.99, 'S3':2.30, 'S4':4.39, 'S5':10.57,'S6':0.77}


# Calculation of the density of biogas #[kg/m³]
x0 = ((df['Methane_yield']*16.04 )+ (1 - df['Methane_yield'])*44.01)/ 22.4
g0 = round(x0, 2)
y0 = g0.values.tolist()
df['biogas_density'] = y0

####################################################
# 2a:Silo
#Calculation of dry mass based on silage losses.

x = df['DM']*df['FM']*1 -df['Silolosses']                   # dryMatter [%] * Fresh matter [t] * (1-siloLosses[%])
g = round(x, 2)
y = g.values.tolist()

df['Silo_DM_loss'] = y

# organic dry mass (oDM) at silo
x1= df['oDM']*df['Silo_DM_loss']                                  # Organic dry mass [%] * dry matter at silo minus losses
g1 = round(x1, 2)
y1= g1.values.tolist()

df['Silo_oDM_loss'] = y1

#fresh matter 
x2 = df['FM']-(df['DM']*df['FM']*df['Silolosses'])                  # fresh matter at Silo minus the fresh matter losses 
g2 = round(x2, 2)
y2 = g2.values.tolist()

df['Silo_FM_loss'] = y2

# possible methane production in m³
x3 = df['Silo_oDM_loss']*df['Methane_production']
g3 = round(x3, 2)
y3 = g3.values.tolist()

df['CH4_m3'] = y3

# possible methane production in t for all used substrates!

x4 = (df['CH4_m3']*ef['Dichte_CH4'])/1000  # EF_gen = general emissionfactors and Dichte_Ch4 ? Value??????? # 
g4 = round(x4, 2)
y4 = g4.values.tolist()  

df['Silo_CH4_t'] = y4

# water content is difference between fresh mass and dry mass

x5 = df['Silo_FM_loss']-df['Silo_DM_loss']                   #water content of substrates at silo
g5 = round(x5, 2)
y5 = g5.values.tolist()

df['Silo_H2O]']= y5
#mineral compounds of substrates:   
x6 = df['Silo_DM_loss']-df['Silo_oDM_loss']
g6 = round(x6, 2)
y6 = g6.values.tolist() 

df['mineral'] = y6


#output Silo is input digester
# 2b:prestorage  
#only for manure   

#reading specific data for prestorage emissions
prestorage=pd.read_csv("EF_prestorage.csv", encoding='unicode-escape',sep=";", decimal=",")
prestorage.set_index('type',inplace=True)
del prestorage['units'] 
df1=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Book2.xls')

EF_ps= prestorage
EF_ps['S1']# find out Emissionfactors for prestorage for each substrate type! use dataframe prestorage and type of substrate to find the column
EF_ps['S2']
EF_ps['S3']
EF_ps['S4']
EF_ps['S5']

#Methane Emissions of prestorage: 

p =df1['prestorage']*df['Silo_CH4_t']*df1['EF_CH4']  # Matrix of Substrates wich are stored in prestorage=EF_ps.prestorage * quantity of possible Methane production * Emissionfactor of Methane at prestorage
r = round(p, 2)
q = r.values.tolist()
df1['ps_CH4_E'] = q

#conversion of Methane to CO2     

p1 = df1['prestorage']*df1['ps_CH4_E']*ef['GWP_CH4']*1000
r1 = round(p1, 2)
q1 = r1.values.tolist()
df1['ps_GHG_CH4'] = q1

#calculation of organic dry mass of substrates in prestorage (only to assembling all losses (the manure as only losses in prestorage not in silo, the other substrates have only losses in silo not in prestorage) )

p2 = (df['Silo_oDM_loss']-df1['ps_CH4_E'])/((df['Methane_production']/100)*ef['Dichte_CH4'])    #organic dry matter= Organic dry matter Silo [t oDM] - (Emissions of methane in PS [kg CH4]/ (methane production of substrate[m³ CH4/t oDM] *denisity of methane [kg CH4/m³CH4]))
r2 = round(p1, 2)
q2 = r2.values.tolist()
df1['ps_oDM_t'] = q2

#sum of organic dry matter    
ps_oDM_sum= sum(df1['ps_oDM_t'])
print('Sum_oDM_sum = ', ps_oDM_sum)

#dry mass contents at prestorage of mineral compounds and organic dry mass 
p3 = df1['ps_oDM_t']+ df['mineral'] 
r3 = round(p3, 2)
q3 = r3.values.tolist()
df1['ps_DM_t']  = q3

sum_ps_DM_t= sum(df['ps_DM_t'])
print('sum_ps_DM_t = ', sum_ps_DM_t)

#there is only organic losses in prestorage, that's why water content is not changing    
p4 = df['DM']+df['Silo_H2O]']
r4 = round(p4, 2)
q4 = r4.values.tolist()
df1['ps_FM_t'] = q4

sum_ps_FM_t= sum(df['ps_FM_t'])
print('sum_ps_FM_t = ', sum_ps_FM_t)

# Calculation water content before fermentation
p5 = df1['ps_FM_t'] -df1['ps_DM_t'] 
r5 = round(p5, 2)
q5 = r5.values.tolist()
df1['ps_H2O'] = q5

# calculation of dry matter concentration  
ps['DM'] = ((sum(ps['DM_t'],2)) / (sum(ps['FM_t'],2))) # dry matter concentration
p6 = sum(df1['ps_DM_t'])/sum(df1['ps_FM_t'])
r6 = round(p6, 2)
q6 = r6.values.tolist()
df1['ps_H2O'] = q6

# prestorage: N2O emissions occur from the total fresh mass input. # [Thünen S.54] 
# Calculation of N2O Emissions which genertated in prestorage

# direct N2O emissions
#ps['E_N2O_d'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_N2O))) #[kg N]

p7 = 1000*df1['EF_N2O']*df1['prestorage']*df['N_t']
r7 = round(p7, 2)
q7 = r7.values.tolist()
df1['E_N2O_d'] = q7

#NitrogenOxid Emissions   
#ps['E_NO'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_NO)))

p8 = 1000*df1['EF_NO']*df1['prestorage']*df['N_t']
r8 = round(p8, 2)
q8 = r8.values.tolist()
df1['E_NO'] = q8

#Nitrogen Emissions
#ps['E_N2'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_N2)))

p9 = df['N_t']*1000*df1['prestorage']*df1['EF_N2']
r9 = round(p9, 2)
q9 = r9.values.tolist()
df1['E_N2'] = q9

#NH3 Emissions
#ps['E_NH3'] = (multiply(multiply(TAN_t,1000.0),(EF_ps.EF_NH3))) # kg TAN

p10 = df['tan_t']*1000*df1['prestorage']*df1['EF_NH3']
r10 = round(p10, 2)
q10 = r10.values.tolist()
df1['E_NH3'] = q10

#prestorage: The N quantities that leak through emissions are subtracted from the N quantity,
#Reduction of nitrogen quantities (N2O emissions) after ensiling/prestorage #[according to "Thünen Report"].
#ps['E_N_sum'] = (ps['E_NO'] + ps['E_N2O_d'] + ps['E_N2'])  # [kg N] E_N*dig,ps

p11 = df1['ps_N2O_d']+df1['ps_N2']+df1['ps_NO']
r11 = round(p11, 2)
q11 = r11.values.tolist()
df1['ps_N_sum'] = q11

#Calculation of percentage of N2O Emission in organic nitrogen    
#ps['E_N2O_in_Norg'] = multiply(ps['E_N_sum']/1000,(TAN_t / (TAN_t+N_org_t))) # KG N *(t TAN/(tTAn+ t N)) Thünen Report 3,78

p12 = (df1['ps_N_sum']/1000)*(df['tan_t']/(df['tan_t']+df['N_org_t']))
r12 = round(p12, 2)
q12 = r12.values.tolist()
df1['ps_N2O_in_Norg'] = q12


#calculation of organic nitrogen content in prestorage
#ps['N_org_t'] = N_org_t-((ps['E_NH3']/1000)-ps['E_N_sum']/1000)  # Thunen Report 3.77

p13 = df['N_org_t']-(df1['ps_NH3']/1000)-(df1['ps_N_sum']/1000)
r13 = round(p13, 2)
q13 = r13.values.tolist()
df1['ps_N_org_t'] = q13

#prestorage: Calculation of TAN (Total ammonium nitrogene) quantity after ensiling/prestorage
#ps['TAN_t'] = TAN_t- (ps['E_NH3']/1000) - ps['E_N2O_in_Norg']

p14 = df['tan_t']-(df1['ps_NH3']/1000)-df1['ps_N2O_in_Norg']
r14 = round(p14, 2)
q14 = r14.values.tolist()
df1['ps_TAN_t'] = q14

#sum of Nitrogen content= TAN+Norganic 
#ps['N_t'] = (ps['TAN_t'] + ps['N_org_t'])
p15 = df1['ps_TAN_t']+df1['ps_N_org_t']
r15 = round(p15, 2)
q15 = r15.values.tolist()
df1['ps_N_t'] = q15
    
# indirect N2O emissions
#ps['E_N2O_in'] = (multiply(EF_pro['PS_ind'],ps['E_NH3']))

p16 = df1['ps_NH3']*ef_pro['PS_ind']
r16 = round(p16, 2)
q16 = r16.values.tolist()
df1['ps_E_N2O_in'] = q16

#  conversion to N2O emissions
#ps['E_N2O'] = (multiply((ps['E_N2O_in'] + ps['E_N2O_d']),EF_gen['U_N2O']))

p17 = (df1['ps_N2O_in']+df1['ps_N2O_d'])*ef['U_N2O']
r17 = round(p17, 2)
q17 = r17.values.tolist()
df1['ps_N2O'] = q17

#prestorage:  possible biogas production  
# Biogasproduction
#ps['BG'] = (multiply(ps['oDM_t'],(Biogas_yield)))

p18 = df1['ps_oDM_t']*df['Biogas_yield']
r18 = round(p18, 2)
q18 = r18.values.tolist()
df1['ps_BG'] = q18    

Sum_bg = sum(df1['ps_BG'])
print('Sum_ps_bg = ', Sum_bg)

#possible methane production in m³ 
#ps['CH4_m3'] = (multiply(ps['oDM_t'],(Methane_production)))

p19 = df1['ps_oDM_t']*df['Methane_production']
r19 = round(p19, 2)
q19 = r19.values.tolist()
df1['ps_CH4_m3'] = q19

ps_CH4_m3 = sum(df1['ps_CH4_m3'])
print('Sum_ps_CH4_m3 = ', ps_CH4_m3)

# conversion m³ CH4 to t Ch4    
#ps['CH4_t'] = (dot(ps['CH4_m3'],EF_gen.Dichte_CH4[1]) / 1000)
p20 = (df1['ps_CH4_m3']*ef['Dichte_CH4'])/1000 
r20 = round(p20, 2)
q20 = r20.values.tolist()
df1['ps_CH4_t'] = q20
df1

#    
#ps['CH4_sum'] = ((ps['CH4_m3_sum']) / (ps['bg_sum'])) # methane concentration
p21 = ps_CH4_m3/Sum_bg
print('ps_CH4_sum = ', p21)
#    
#ps['BG_y_sum'] = ((ps['bg_sum']) / (ps['oDM_sum'])) # biogas yield
p22 = Sum_bg/ps_oDM_sum
print('ps_BG_y_sum = ', p22)
# 
#ps['BG_den_sum'] = (sum((multiply(ps['BG'],biogas_density)),2) / ps['bg_sum']) # biogas density
p23 = (df1['ps_BG']*df['biogas_density']*2)/Sum_bg
print('ps_BG_den_sum = ', p23)

#Output prestorage ist Input Fermenter
#######################################################
#GHG Emissions in prestorage       
#GhG['ps'] = ((ps['GHG_CH4'] + multiply(EF_gen['GWP_N2O'],ps['E_N2O'])) / 1000)
    
p24 = (df1['ps_GHG_CH4']+(ef['GWP_N2O']+df1['ps_N2O']))/1000
r24 = round(p24, 2)
q19 = r24.values.tolist()
df1['Ghg_ps'] = q19

Ghg_ps = sum(df1['Ghg_ps'])
print('Sum_GhG_ps = ', Ghg_ps)
 
#3 digester

#Calculation of the consumption of water for biogas
#dig['H2O_redu']  = (0.15)
h  = (0.15)
df1['dig_H2O_redu'] = h

# consumption of water for biogasproduction
#dig['H2O_con'] = (multiply(multiply(biogas_density,ps['BG']),dig['H2O_redu'] ) / 1000

h1 = (df['biogas_density']+df1['ps_BG']+df1['dig_H2O_redu'])/1000
i1 = round(h1, 2)
j1 = i1.values.tolist()
df1['dig_H2O_con'] = j1
 
# consumption of dry matter for biogasproduction
#dig['DM_con'] = (multiply(multiply(biogas_density,ps['BG']),(1 - dig['H2O_redu'] )) / 1000
# )
h2 = (df['biogas_density']*df1['ps_BG']*(1-df1['dig_H2O_redu']))/1000
i2 = round(h2, 2)
j2 = i2.values.tolist()
df1['dig_DM_con'] = j2

#Biogas
#dig['BG_t_sum'] = (multiply(ps['bg_sum'],ps['BG_den_sum']) / 1000)

h3 = (p23*df1['ps_BG'])/1000
i3 = round(h3, 2)
j3 = i3.values.tolist()
df1['dig_BG_t_sum'] = j3

#   
#dig['BG_t'] = (multiply(ps['BG'],biogas_density) / 1000)

h4 = (df['biogas_density']*df1['ps_BG'])/1000
i4 = round(h4, 2)
j4 = i4.values.tolist()
df1['dig_BG_t'] = j4
    
# calculation of the CH4 emissions: first the potetial of the gasproduction in residue storage has to be calculatet
#reSto['CH4_t'] = (multiply(ps['CH4_t'],EF_pro.reSto_Restgas[0]))

h5 = df1['ps_CH4_t']*ef_pro['ReSto_Restgas']
i5 = round(h5, 2)
j5 = i5.values.tolist()
df1['reSto_CH4_t'] = j5

#the possible methane production in prestorage+silo minus gas prodction in residues storage = ch4 in disumter
#dig['CH4_t'] = (ps['CH4_t'] - reSto['CH4_t'])

h6 = df1['ps_CH4_t']-df1['reSto_CH4_t']
i6 = round(h6, 2)
j6 = i6.values.tolist()
df1['dig_CH4_t'] = j6

# emissions due to digetser 
#dig['CH4_E'] = (dot(EF_pro.L_dig[0],dig['CH4_t']))

h7 = df1['dig_CH4_t']*ef_pro['L_dig']
i7 = round(h7, 2)
j7 = i7.values.tolist()
df1['dig_CH4_E'] = j7

# useable ch4
#dig['CHP_CH4_use'] = (dig['CH4_t'] - dig['CH4_E'])

h8 = df1['dig_CH4_t']-df1['dig_CH4_E']
i8 = round(h8, 2)
j8 = i8.values.tolist()
df1['dig_CHP_CH4_use'] = j8

# Calculation of Nitrogen content
# amount of TAN in Substrate in digester
# dig['TAN'] = (ps['TAN_t'] + multiply((G_TAN),(ps['N_t'] - ps['TAN_t']))) # enrichment factor manure 0.32, energy crops 0.56 = g_TAN
#dig['N2O_E'] = (0) # because gastight
O = 0
df1['dig_N2O_E'] = O

h9 = df1['ps_TAN_t']+(df['G_TAN']*(df1['ps_N_t']-df1['ps_TAN_t']))
i9 = round(h9, 2)
j9 = i9.values.tolist()
df1['dig_TAN'] = j9

# quantity of Nitrogen in the Substrates in digester  > goes into residue storage 
#dig['N_t'] = (ps['N_t'] - dig['N2O_E']) 

h10 = df1['ps_N_t']-df1['dig_N2O_E']
i10 = round(h10, 2)
j10 = i10.values.tolist()
df1['dig_N_t'] = j10

# quantity of organixc
#dig['N_org'] = (dig['N_t'] - dig['TAN'])     
# N-Emissionen = 0

h11 = df1['dig_N_t']-df1['dig_TAN']
i11 = round(h11, 2)
j11 = i11.values.tolist()
df1['dig_N_org'] = j11
print(df1)

# 4.reSto=residue storage : CH4 Emissionen storage residues
    
# (simpler would be via fugate factor > but I have a calculation by Prof. Fischer, 
#because not for all substrates a fugate factor is known, and by the fugate factor 
#only the fermentation residue quantity in m³ can be determined)

Fugat=(np.array(Fugatfaktor).transpose())
    # Quantity of fermentation residue that goes into fermentation residue storage
reSto['FM']= zeros(length(Fugatfaktor))

#for loop and if-condition to calculate the quantity of residues. this calculation you have to check
# the fugatfaktor gives informastion about the quantity of residues, but tis isn't avaiable for each substrate. 
# if there is no fugatfaktor we have to calculate from dry matter, water content and the consumption of it during fermentation

for f in range(length(Fugatfaktor)):
        if (multiply(Fugatfaktor[f],ps['FM_t'].iloc[f])) == 0:
            # DM
            reSto['DM_t'] = (ps['DM_t'] - dig['DM_con'])

            reSto['DM_sum'] = sum(reSto['DM_t'],2)

            reSto['H2O'] = (ps['H2O'] - dig['H2O_con'])

                #FM
            reSto['FM'][f]=reSto['DM_t'].iloc[f] + reSto['H2O'].iloc[f]

                # t
                    #oDM
            reSto['oDM_t'] = (reSto['DM_t'] - (ps['DM_t'] - ps['oDM_t']))

            reSto['oDM_vgl'] = (ps['oDM_t'] - dig['BG_t'] + dig['H2O_con'])

            reSto['DM'] = (sum(reSto['DM_t'],2) / sum(reSto['FM'],2))

        else:
    # residue quantity with fugat
            reSto['FM'][f]=multiply(Fugat[f],ps['FM_t'].iloc[f])

 #   
reSto['FM_sum'] = (sum(reSto['FM'],2))
   
#create a query if gas-tight or not> calculatate the percentge allocation 
UF_xgt = (1)  # factor for gas tight storages 1 means 100% are gas tight. 0.5 means 50% are gastight

#   
reSto['CH4_E'] = (multiply(multiply(EF_pro.L_sto[0],reSto['CH4_t']),UF_xgt) + (multiply(multiply((1 - UF_xgt),EF_pro.MCF_oGRL[0]),reSto['CH4_t'])))

    
# storage: N emissions storage >> ATTENTION indirect N2O from NH3 and No!!!
# N2O (only if not gas-tight) 
# NH3 (only if not gas-tight)
# if not gas tight, the emissionfactors have to change to: NH3_osto, N2O_osto > adjust calculation > use calculation of reSto['CH4_E']

#NH3 emissions in residue storage
reSto['NH3_E'] = (multiply(dig['TAN'],EF_pro.NH3_sto))

#N2O emissions in residue storage    
reSto['N2O_E'] = (multiply(dig['N_t'],EF_pro.N2O_sto))

# emission factor of indirect N2O emissions   
EF_N2Oid_resto = (0.01)
#indirect N2O emissions in reSto
reSto['N2Oid_E'] = (multiply(EF_N2Oid_resto,reSto['NH3_E']))
   
# Calculation of the nitrogen quantities in the residues 

#TAN content of residues Thunen 3.82
reSto['TAN'] = (dig['TAN'] - reSto['NH3_E'] - multiply(reSto['N2O_E'],(dig['TAN'] / dig['N_t'])))
reSto['TAN'][np.isnan(reSto['TAN'])]=0
reSto['TAN_sum'] = ((sum(reSto['TAN'],2)))

#Nitrogen content of residues   
reSto['N'] = (dig['N_t'] - reSto['NH3_E'] - reSto['N2O_E'])

# organic nitrogen content in residues   
reSto['N_org'] = (reSto['N'] - reSto['TAN'])  
reSto['N'][np.isnan(reSto['N'])]=0


#sum of Nitrogen in residues>> is needed for spreading 
reSto['N_sum_t'] = (sum(reSto['N'],2))
reSto['N_sum'] = ((sum(multiply(reSto['N'],1000),2)))

# function to create a Matrix with 0 and 1 to check out wich substrates are energy crop
Substrate_names=list(S_allo_CH4.columns)

def EnergyCrop(Substrate_names):
   
    Animal_straw=['cereal straw', 'maize straw','poultry dry manure','cattle manure','cattle slurry','pig manure','pig slurry']
    z=0
    row=length(Substrate_names)
    column=1
    K=ones(row,column)
    Zeile=zeros(row,length(Animal_straw))
    Spalte=zeros(row,length(Animal_straw))
    for u in range(length(Animal_straw)):
        for i in range(row):
            for r in range(column):
                if Substrate_names[i] == Animal_straw[u]:
                    Zeile[z,u]=i
                    Spalte[z,u]=r
                    z=z + 1
        z=0
  
    for z in range(row):
        for u in range(length(Animal_straw)):
            if Zeile[z,u] != 0 or Spalte[z,u] != 0:
                K[Zeile[z,u],Spalte[z,u]]=0
    return K

# figure out the N content which is from energy crop
Crop=EnergyCrop(Substrate_names)
Animal_Straw=zeros(length(Crop),1)

for i in range(length(Crop)):
    if Crop[i] == 1:
        Animal_Straw[i]=0
    else:
        Animal_Straw[i]=1
  
reSto['N_Crop'] = (multiply(reSto['N'],Crop.T))

##############################################################################################
# GhG: Conversion of emissions into CO2 equivalence from digester and residuestorage
    
dig_res_CH4_E = (multiply(EF_gen.GWP_CH4[1],(dig['CH4_E'] + reSto['CH4_E'])))
  
GhG['dig_res'] = (dig_res_CH4_E + multiply(EF_gen.GWP_N2O,(reSto['N2O_E'] + reSto['N2Oid_E'])))    
GhG['dig_res'][np.isnan(GhG['dig_res'])]=0
GhG['dig_res_sum'] = (sum(GhG['dig_res'],2)) # stimmt nciht ganz mit Matlab überrein

# quantity of CH4 from residue Storage which could be use
reSto['CHP_CH4_use'] = (reSto['CH4_t'] - reSto['CH4_E'])

CHP = 'combined heat and power'
CHP['CH4_use']=reSto['CHP_CH4_use']+dig['CHP_CH4_use']

# 5. CHP
    
CHP['CH4_use'] = (sum(dig['CHP_CH4_use'],2) + sum(reSto['CHP_CH4_use'],2)) # in dataframe CHP

    
CHP['CH4_use_m3'] = (dot(CHP['CH4_use'] / EF_gen.Dichte_CH4[1],1000)) # in dataframe CHP

#Usable methane quantity in the CHP unit in m3
# Methane losses from pre-storage to disumter
Pro = []
Pro['loss_CH4_t'] = (sum(ps['CH4_E'],2) + sum(dig['CH4_E'],2) + sum(reSto['CH4_E'],2))
    
Pro['loss_CH4_m3'] = (dot(Pro['loss_CH4_t'] / EF_gen.Dichte_CH4[1],1000))
    
rest = (ps['bg_sum'] - ps['CH4_m3_sum'])
    
CHP['BG_use_m3']= (rest + CHP['CH4_use_m3'])
   
CHP['CH4_content_use'] = (CHP['CH4_use_m3'] / CHP['BG_use_m3'])

# CHP # Methane content refers to volume! 
# Electrical energy and methane slip
CHP['E_CH4'] = (multiply(EF_pro.Schlupf[0],CHP['CH4_con']))
CHP['CH4_t'] = (CHP['CH4_use'] - CHP['E_CH4'])
CHP['E_CH4_m'] = (multiply(EF_pro.Schlupf[0],CHP['CH4_use_m3']))
CHP['CH4_m']= (CHP['CH4_use_m3'] - CHP['E_CH4_m'])
CHP['CH4_m3'] = (multiply(CHP['CH4_t'] / EF_gen.Dichte_CH4[1],1000))
CHP['BG_Heiz'] = (multiply(CHP['CH4_content_use'],EF_gen.Energiegehalt_CH4[1]))
CHP['kWh_CH4'] = ((multiply(CHP['CH4_m3'],EF_gen.Energiegehalt_CH4[1])))
CHP['kWh_el'] = (multiply(multiply(CHP['kWh_CH4'],(CHP.eta_el)),VBH_pro))
CHP['el_energie_diff'] = (CHP.Energie_Erf_el - CHP['kWh_el'])
CHP['CH4_loss'] = (1 - CHP['CH4_m3'] / CHP.CH4_erf)
CHP['own_el'] = (multiply(CHP['kWh_el'],el_own))
CHP['kWh_el_use'] = (CHP['kWh_el'] - CHP['own_el'])

#####
GhG['CHP'] = (multiply(EF_gen.GWP_CH4[1],CHP['E_CH4']))

GhG['CHP_m3'] = (multiply(EF_gen.GWP_CH4[1],CHP['E_CH4_m']))
#Engine oil >> Determine consumption!!! Assumption > 1 L per 1000 m³ fuel [http://www.baukontor-schmidt.de/cms/startseite/CHP/lexikon-zum-thema-CHP_hDMl]
CHP_oil=1.000000000000000e-03
CHP['Motor'] = (multiply(CHP['BG_use_m3'],CHP_oil))

    
GhG['E_Motor'] = (multiply(CHP['Motor'],EF_tran.Diesel_spec_vol[0]))
    
    # updating calculation > differenc between Gas Otto engine and Ignition jet engine https://de.wikipedia.org/wiki/Z%C3%BCndstrahlmotor
    #https://de.wikipedia.org/wiki/Biogasmotor 
#later
####################################################################################################
# # emissions of spreading disumtate/fermentation residue
# emissionfactors_spreading=pd.read_csv("Ausbringung.csv", usecols=[0,1], encoding='unicode-escape',sep=";", decimal=",", header=0, index_col=0, squeeze=True ).to_frame().transpose()

# EF_Spr=emissionfactors_spreading

#residues, growing, Spreading, Reduktion= Ausbringung(residues, growing, substrate_data, EF_gen, EF_grow, EF_Spr) #calculation spreading of disumtate
#Ap, Ep, GhG, transport=Transportwege(EF_tran, EF_gen, growing, Spreading, S_allo, Silo, GhG, Ap, Ep) #transport emissions
#Ep, Ap, GhG, Wd, W=WD_Gutschrift(S_allo, growing, substrate_data, EF_gen, Ep, Ap, GhG) # manure credit
#Gut_GhG, Gut_th=Waerme(S_allo, VBH_pro, ChP, W) # heat
# from sumamtEmissionen import *
# EP_kWh, Ap_kWh, GhG_kWh, GhG_FM=sumamtEmissionen(EF_gen, EF_grow, EF_Spr, growing, ChP, residues, Reduktion, Spreading, prestorage, GhG, Ap, Ep, Gut_GhG) # all emissions
             