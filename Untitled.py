#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
df=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Book.xls')
df1=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Book2.xls')
ef=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/Emissionsfaktoren.xls')
ef_pro=pd.read_excel(r'C:/Users/parimal/OneDrive/Desktop/Thesis/NEW_scripts/data/EF_process.xls')

###################################################################
# go on for all data

Substrate1=('cattle slurry') # type of substrate 

# print(df['FM'])
# print(df['DM'])
# print(df['oDM'])
# print(df['N'])
# print(df['P'])
# print(df['K'])
# print(df['Fertilizer_N'])
# print(df['Fertilizer_P2O5'])
# print(df['Fertilizer_K2O'])
# print(df['liming'])
# print(df['Seed'])
# print(df['Pesticides'])
# print(df['Harvest_yield'])
# print(df['Seed'])
# print(df['Fuel'])
# print(df['Hectar'])
# ############

# print(df['Methane_yield'])
# print(df['Silolosses'])
# print(df['Methane_production'])
# print(df['Biogas_yield'])
# print(df['Biogas_production'])
# print(df['Methane_content'])
# print(df['TAN'])
# print(df['Fugatfaktor'])
# print(df['G_TAN'])
# print(df['N_Min'])
# print(df['HNV'])
# print(df['X_N_above'])
# print(df['X_AGR_DM'])
# print(df['X_N_below'])
# print(df['A_above'])
# print(df['A_below'])
# print(df['X_renew'])
# print(df['X_mow'])
# print(df['Yield_Duev'])
# print(df['Yield_diff'])
# print(df['Supp_yield'])
# print(df['Redu_yield'])
# print(df['EF_seed'])


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

Sum_N= sum(df['N_C'])
print('Sum_N_C = ', Sum_N)
N_t = df['N_C']/1000    # Nitrogen content [t] in whole fresh matter
N_t_Y = N_t.values.tolist()

df['N_t']= N_t_Y

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

###################################################################
# Calculation of the density of biogas #[kg/m³]
x0 = ((df['Methane_yield']*16.04 )+ (1-df['Methane_yield'])*44.01)/ 22.4
g0 = round(x0, 2)
y0 = g0.values.tolist()

df['biogas_density'] = y0
###################################################################
x = df['DM']*df['FM']*1 -df['Silolosses']
g = round(x, 2)
y = g.values.tolist()

df['Silo_DM_loss'] = y

###################################################################

x1= df['oDM']*df['Silo_DM_loss']
g1 = round(x1, 2)
y1= g1.values.tolist()

df['Silo_oDM_loss'] = y1

##################################################################

x2 = df['FM']-(df['DM']*df['FM']*df['Silolosses'])
g2 = round(x2, 2)
y2 = g2.values.tolist()

df['Silo_FM_loss'] = y2
###################################################################
# possible methane production in m³
x3 = df['Silo_oDM_loss']*df['Methane_production']
g3 = round(x3, 2)
y3 = g3.values.tolist()

df['CH4_m3'] = y3
###################################################################
# possible methane production in t for all used substrates!

x4 = (df['CH4_m3']*ef['Dichte_CH4'])/1000  # EF_gen = general emissionfactors and Dichte_Ch4 ? Value??????? # 
g4 = round(x4, 2)
y4 = g4.values.tolist()  

df['Silo_CH4_t'] = y4
###################################################################
# water content is difference between fresh mass and dry mass

x5 = df['Silo_FM_loss']-df['Silo_DM_loss']                   #water content of substrates at silo
g5 = round(x5, 2)
y5 = g5.values.tolist()

df['Silo_H2O']= y5
###################################################################
#mineral compounds of substrates:   
x6 = df['Silo_DM_loss']-df['Silo_oDM_loss']
g6 = round(x6, 2)
y6 = g6.values.tolist() 

df['mineral'] = y6

################################################################## 

p =df1['prestorage']*df['Silo_CH4_t']*df1['EF_CH4']
r = round(p, 2)
q = r.values.tolist()
df1['ps_CH4_E'] = q

################################################################## 
p1 = df1['prestorage']*df1['ps_CH4_E']*ef['GWP_CH4']*1000
r1 = round(p1, 2)
q1 = r1.values.tolist()
df1['ps_GHG_CH4'] = q1

################################################################## 
p2 = (df['Silo_oDM_loss']-df1['ps_CH4_E'])/((df['Methane_production']/100)*ef['Dichte_CH4'])    
r2 = round(p2, 2)
q2 = r2.values.tolist()
df1['ps_oDM_t'] = q2

##################################################################
ps_oDM_sum= sum(df1['ps_oDM_t'])
print('Sum_oDM_sum = ', ps_oDM_sum)
##################################################################
p3 = df1['ps_oDM_t']+ df['mineral'] 
r3 = round(p3, 2)
q3 = r3.values.tolist()
df1['ps_DM_t'] = q3

sum_ps_DM_t= sum(df1['ps_DM_t'])
print('sum_ps_DM_t = ', sum_ps_DM_t)
##################################################################
p4 = df['DM']+df['Silo_H2O']
r4 = round(p4, 2)
q4 = r4.values.tolist()
df1['ps_FM_t'] = q4

sum_ps_FM_t= sum(df1['ps_FM_t'])
print('sum_ps_FM_t = ', sum_ps_FM_t)
#################################################################
p5 = df1['ps_FM_t'] -df1['ps_DM_t'] 
r5 = round(p5, 2)
q5 = r5.values.tolist()
df1['ps_H2O'] = q5

##################################################################
#ps['DM'] = ((sum(ps['DM_t'],2)) / (sum(ps['FM_t'],2))) # dry matter concentration
p6 = sum_ps_DM_t/sum_ps_FM_t
r6 = round(p6, 2)

df1['DM'] = r6

##################################################################
#ps['E_N2O_d'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_N2O))) 
 
p7 = 1000*df1['EF_N2O']*df1['prestorage']*df['N_t']
r7 = round(p7, 2)
q7 = r7.values.tolist()
df1['ps_N2O_d'] = q7

##################################################################
#ps['E_NO'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_NO)))

p8 = 1000*df1['EF_NO']*df1['prestorage']*df['N_t']
r8 = round(p8, 2)
q8 = r8.values.tolist()
df1['ps_NO'] = q8

##################################################################
#ps['E_N2'] = (multiply(multiply(N_t,1000.0),(EF_ps.EF_N2)))

p9 = df['N_t']*1000*df1['prestorage']*df1['EF_N2']
r9 = round(p9, 2)
q9 = r9.values.tolist()
df1['ps_N2'] = q9

##################################################################
#ps['E_NH3'] = (multiply(multiply(TAN_t,1000.0),(EF_ps.EF_NH3)))

p10 = df['tan_t']*1000*df1['prestorage']*df1['EF_NH3']
r10 = round(p10, 2)
q10 = r10.values.tolist()
df1['ps_NH3'] = q10

##################################################################
#ps['E_N_sum'] = (ps['E_NO'] + ps['E_N2O_d'] + ps['E_N2'])    # [kg N] E_N*dig,ps

p11 = df1['ps_N2O_d']+df1['ps_N2']+df1['ps_NO']
r11 = round(p11, 2)
q11 = r11.values.tolist()
df1['ps_N_sum'] = q11

##################################################################
#ps['E_N2O_in_Norg'] = multiply(ps['E_N_sum']/1000,(TAN_t / (TAN_t+N_org_t))) # KG N *(t TAN/(tTAn+ t N)) Thünen Report 3,78

p12 = (df1['ps_N_sum']/1000)*(df['tan_t']/(df['tan_t']+df['N_org_t']))
r12 = round(p12, 2)
q12 = r12.values.tolist()
df1['ps_N2O_in_Norg'] = q12

##################################################################
#ps['N_org_t'] = N_org_t-((ps['E_NH3']/1000)-ps['E_N_sum']/1000)  # Thunen Report 3.77

p13 = df['N_org_t']-(df1['ps_NH3']/1000)-(df1['ps_N_sum']/1000)
r13 = round(p13, 2)
q13 = r13.values.tolist()
df1['ps_N_org_t'] = q13

##################################################################
#ps['TAN_t'] = TAN_t- (ps['E_NH3']/1000) - ps['E_N2O_in_Norg']

p14 = df['tan_t']-(df1['ps_NH3']/1000)-df1['ps_N2O_in_Norg']
r14 = round(p14, 2)
q14 = r14.values.tolist()
df1['ps_TAN_t'] = q14

##################################################################
#ps['N_t'] = (ps['TAN_t'] + ps['N_org_t'])

p15 = df1['ps_TAN_t']+df1['ps_N_org_t']
r15 = round(p15, 2)
q15 = r15.values.tolist()
df1['ps_N_t'] = q15

##################################################################
#ps['E_N2O_in'] = (multiply(EF_pro['PS_ind'],ps['E_NH3']))

p16 = df1['ps_NH3']*ef_pro['PS_ind']
r16 = round(p16, 2)
q16 = r16.values.tolist()
df1['ps_N2O_in'] = q16

##################################################################
#ps['E_N2O'] = (multiply((ps['E_N2O_in'] + ps['E_N2O_d']),EF_gen['U_N2O']))

p17 = (df1['ps_N2O_in']+df1['ps_N2O_d'])*ef['U_N2O']
r17 = round(p17, 2)
q17 = r17.values.tolist()
df1['ps_N2O'] = q17

##################################################################
#ps['BG'] = (multiply(ps['oDM_t'],(Biogas_yield)))

p18 = df1['ps_oDM_t']*df['Biogas_yield']
r18 = round(p18, 2)
q18 = r18.values.tolist()
df1['ps_BG'] = q18

Sum_bg = sum(df1['ps_BG'])
print('Sum_ps_bg = ', Sum_bg)
##################################################################
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

##################################################################
#ps['CH4_sum'] = ((ps['CH4_m3_sum']) / (ps['bg_sum'])) # methane concentration
p21 = ps_CH4_m3/Sum_bg
print('ps_CH4_sum = ', p21)

##################################################################
#ps['BG_y_sum'] = ((ps['bg_sum']) / (ps['oDM_sum'])) # biogas yield
p22 = Sum_bg/ps_oDM_sum
print('ps_BG_y_sum = ', p22)

##################################################################
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
h  = (0.15)
df1['dig_H2O_redu'] = h

# consumption of water for biogasproduction
#dig['H2O_con'] = (multiply(multiply(biogas_density,ps['BG']),dig['H2O_redu'] ) / 1000)

h1 = (df['biogas_density']*df1['ps_BG']*df1['dig_H2O_redu'])/1000
i1 = round(h1, 2)
j1 = i1.values.tolist()
df1['dig_H2O_con'] = j1

# consumption of dry matter for biogasproduction
#dig['DM_con'] = (multiply(multiply(biogas_density,ps['BG']),(1 - dig['H2O_redu'] )) / 1000)

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

##############################################################
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

h10 = df1['ps_N_t']- df1['dig_N2O_E']
i10 = round(h10, 2)
j10 = i10.values.tolist()
df1['dig_N_t'] = j10

# quantity of organixc
#dig['N_org'] = (dig['N_t'] - dig['TAN']) #     
# N-Emissionen = 0

h11 = df1['dig_N_t']-df1['dig_TAN']
i11 = round(h11, 2)
j11 = i11.values.tolist()
df1['dig_N_org'] = j11

# DM
#reSto['DM_t'] = (ps['DM_t'] - dig['DM_con'])

a = df1['ps_DM_t']-df1['dig_DM_con']
b = round(a, 2)
c = b.values.tolist()
df1['reSto_DM_t'] = c

