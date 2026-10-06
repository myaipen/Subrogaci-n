import pandas as pd, pickle, json, re, unicodedata, itertools
W='/tmp/claude-0/-home-claude/c6b41dbf-fe43-52b4-854b-a5a6707d4971/scratchpad/work/'
CLA="/root/.claude/uploads/c6b41dbf-fe43-52b4-854b-a5a6707d4971/764b0d1f-Clasificacio_n_3.xlsx".replace('4971/764','4971/764')
CLA="/root/.claude/uploads/c6b41dbf-fe43-52b4-854b-a5a6707d4971/764b0d1f-Clasificacio_n_3.xlsx"
def norm(s):
    if pd.isna(s): return None
    s=re.sub(r'\s+',' ',str(s).strip()); s=unicodedata.normalize('NFKD',s)
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()
g1=pd.read_pickle(W+'v4_g1.pkl');g2=pd.read_pickle(W+'v4_g2.pkl');g3=pd.read_pickle(W+'v4_g3.pkl')
pl=pd.read_pickle(W+'v4_pac_lookup.pkl')
g1['Grupo']='G1';g2['Grupo']='G23';g3['Grupo']='G23'
df=pd.concat([g1,g2,g3],ignore_index=True)
# --- clasificación 3
sv=pd.read_excel(CLA,sheet_name='Servicios').iloc[:,:4]
sv.columns=['prod','serv','sub','sub2']
sv['serv']=sv['serv'].replace({'wellness':'Wellness'})
sv=sv.drop_duplicates('prod').set_index(sv.drop_duplicates('prod')['prod'].str.strip())
df['prod']=df['Nombre Prod.'].astype(str).str.strip()
df['Serv']=df['prod'].map(sv['serv']).fillna('Sin clasificar')
df['Sub']=df['prod'].map(sv['sub']).fillna('')
df['Consulta']=''
# sede
sd=pd.read_excel(CLA,sheet_name='Sedes'); sede_map=dict(zip(sd['Delegación'].str.strip(),sd['Sede']))
df['Sede']=df['Delegación'].astype(str).str.strip().map(sede_map).fillna('Otra')
sub=pd.read_excel(CLA,sheet_name='Médicos subsedes GDL',header=1).dropna(how='all'); 
sub_map={norm(r['Nombres de médicos']):r['Subsede'] for _,r in sub.iterrows()}
df['Subsede']=df['Profesional Historia'].map(norm).map(sub_map).fillna('')
# agencia por paciente (Procedencia ya normalizada)
AG={'gestacy':'Gestacy','my surrogacy journey':'My Surrogacy Journey','gsm':'GSM','her helping habit':'Her Helping Habit','mx familia':'MX Familia','vip surrogacy':'VIP Surrogacy','vip subrogacy':'VIP Surrogacy','smartpath':'SmartPath'}
proc=pl['Procedencia'].map(norm)
ag=proc.map(lambda x:AG.get(x) if x else None)
ag=ag.where(ag.notna(), proc.map(lambda x: 'Otra procedencia' if x else 'Sin dato'))
df['Agencia']=df['Historia_norm_fix'].map(ag).fillna('Sin dato')
df['Medico']=df['Profesional Historia'].fillna('Sin médico').astype(str).str.strip()
df['MedTipo']=df['MedicoIntExt']
df['M']=df['F. Cargo'].dt.month   # 1..9
df['ing']=df['Total Venta'].round(2)
df['esSub']=(df['Serv']=='Subrogación')
# pacientes anónimos: nunca se exporta nombre
df['pid']=df['Historia_norm_fix']
# debut month por paciente (primer cargo)
debut=df.groupby('pid')['F. Cargo'].min().dt.month
df['debut']=df['pid'].map(debut)

df['Sede']=df['Sede'].where(df['Sede']=='Ciudad de México','Otras sedes (GDL/Metepec)')
df['Prod']=df['prod'].where(df['Serv'].isin(['Subrogación','Sin clasificar']),'')
df.loc[df['Serv']=='Consultas','Consulta']=df['Sub']
def cube(dims):
    d=df.groupby(dims,dropna=False).apply(lambda x:pd.Series({'ing':round(x.ing.sum(),2),'n':len(x),'ingS':round(x.loc[x.esSub,'ing'].sum(),2)})).reset_index()
    d['n']=d['n'].astype(int)
    return d.to_dict('records')
base=['M','Grupo','Sede']
cubes={'serv':cube(base+['Serv','Sub']),'med':cube(base+['Medico','MedTipo']),'ag':cube(base+['Agencia']),'prod':cube(base+['Prod','Serv']),'tot':cube(base)}
grupos=['ALL','G1','G23']; sedes=['ALL','Ciudad de México','Otras sedes (GDL/Metepec)']
pat={}
for g in grupos:
  for s_ in sedes:
    d=df
    if g!='ALL': d=d[d.Grupo==g]
    if s_!='ALL': d=d[d.Sede==s_]
    for a in range(1,10):
      for b in range(a,10):
        r=d[(d.M>=a)&(d.M<=b)]
        dd=r.drop_duplicates('pid')
        pat[f'{g}|{s_}|{a}|{b}']=[int(r.pid.nunique()),int(r[r.esSub].pid.nunique()),int(((dd['debut']>=max(a,2))&(dd['debut']<=b)).sum())]
# serie mensual de pacientes (activos/nuevos) por grupo/sede = pat a==b
gr=pickle.load(open(W+'v4_grupos.pkl','rb'))
out={'cubes':cubes,'pat':pat,'sedes':sedes,
 'universo':{'G1':len(gr['grupo1_names']),'G2':len(gr['grupo2_names']),'G3':len(gr['grupo3_names'])},
 'activos':{'G1':int(df[df.Grupo=='G1'].pid.nunique()),'G23':int(df[df.Grupo=='G23'].pid.nunique())},
 'corte':'30 de septiembre de 2026'}
json.dump(out,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
print('TOTAL',round(df.ing.sum(),2),'Sub',round(df[df.esSub].ing.sum(),2),'activos',df.pid.nunique(),'universo',out['universo'])
print(df.groupby('Prod').ing.agg(['size','sum']).round(0).to_string())
print(df.groupby('Medico').ing.agg(['size','sum']).round(0).sort_values('sum',ascending=False).to_string())
print(df.groupby(['Sede']).pid.nunique())
import os;print(os.path.getsize('data.json'))
