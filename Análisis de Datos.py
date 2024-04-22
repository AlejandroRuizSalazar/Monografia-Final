import pandas as pd

#Es necesario convertir los valores dados por Labview que son de la forma "c,00000" siendo c un natural a un float para poder compararlos
def stringADecimal(a):
    valor = a
    valor_sin_coma = valor.replace(",", ".")  
    valor_float = float(valor_sin_coma)
    return valor_float

# Comparación de los datos para 2 PMTs
#for i in range(1,1140):
#    data = pd.read_table(f"Tiempo_Datos_{i}.txt",sep='\t' ,header=None)
#    archivo = open(f'NuevosDatos_{i}.txt','w')

#    for j in range(0,len(data[0])):
#        PMTY1 = stringADecimal(data[4][j])
#        PMTY2 = stringADecimal(data[5][j])
#        PMTX1 = stringADecimal(data[6][j])
#        PMTX2 = stringADecimal(data[7][j])
#        if PMTY1 >= 100 and PMTX1 >= 100:
#            archivo.write(f"{data[0][j]}\t{data[1][j]}\t{data[2][j]}\t{data[3][j]}\t{data[4][j]}\t{data[5][j]}\t{data[6][j]}\t{data[7][j]}\t{data[8][j]}\n")
#            continue
#        elif PMTY1 >= 100 and PMTX2 >= 100:
#            archivo.write(f"{data[0][j]}\t{data[1][j]}\t{data[2][j]}\t{data[3][j]}\t{data[4][j]}\t{data[5][j]}\t{data[6][j]}\t{data[7][j]}\t{data[8][j]}\n")
#            continue
#        elif PMTY2 >= 100 and PMTX1 >= 100:
#            archivo.write(f"{data[0][j]}\t{data[1][j]}\t{data[2][j]}\t{data[3][j]}\t{data[4][j]}\t{data[5][j]}\t{data[6][j]}\t{data[7][j]}\t{data[8][j]}\n")
#            continue
#        elif PMTY2 >= 100 and PMTX2 >= 100:
#            archivo.write(f"{data[0][j]}\t{data[1][j]}\t{data[2][j]}\t{data[3][j]}\t{data[4][j]}\t{data[5][j]}\t{data[6][j]}\t{data[7][j]}\t{data[8][j]}\n")
#            continue

# Comparación de los datos para 4 PMTs
for i in range(1,1140):
    data = pd.read_table(f"Tiempo_Datos_{i}.txt",sep='\t' ,header=None)
    archivo = open(f'NuevosDatos_{i}.txt','w')
    print(i)
    for j in range(0,len(data[0])):
        PMTY1 = stringADecimal(data[4][j])
        PMTY2 = stringADecimal(data[5][j])
        PMTX1 = stringADecimal(data[6][j])
        PMTX2 = stringADecimal(data[7][j])
        if PMTY1 >= 100 and PMTY2 >= 100 and PMTX1 >= 100 and PMTX2 >= 100:
            archivo.write(f"{data[0][j]}\t{data[1][j]}\t{data[2][j]}\t{data[3][j]}\t{data[4][j]}\t{data[5][j]}\t{data[6][j]}\t{data[7][j]}\t{data[8][j]}\n")
    archivo.close()
