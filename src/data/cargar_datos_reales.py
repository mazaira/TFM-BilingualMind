# cargar_datos_reales.py  
import pandas as pd  
import pyreadstat  
import sqlite3  
  
print("INICIANDO CARGA DE DATOS REALES...")  
conn = sqlite3.connect('bilingualmind.db')  
  
try:  
    print("Cargando PISA...")  
    df_pisa, meta = pyreadstat.read_sav('2. datasets/data/CY08MSP_STU_QQQ.SAV')  
    df_pisa[['CNT','PV1READ','ESCS','ST004D01T']].to_sql('pisa_data', conn, if_exists='replace', index=False)  
    print(f"PISA: {len(df_pisa)} registros")  
except Exception as e:  
    print(f"Error PISA: {e}")  
  
try:  
    print("Cargando ESS...")  
    df_ess, meta = pyreadstat.read_sav('2. datasets/data/ESS11.sav')  
    df_ess[['gndr','eduyrs','health']].to_sql('ess_data', conn, if_exists='replace', index=False)  
    print(f"ESS: {len(df_ess)} registros")  
except Exception as e:  
    print(f"Error ESS: {e}")  
  
conn.close()  
print("CARGA COMPLETADA!") 
