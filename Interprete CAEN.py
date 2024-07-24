"""
Código creado por: Alejandro Ruiz Salazar
Tester: Diego Lodoño

Versión 4.5
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Inicializar listas vacías para almacenar los datos
timestamps = []
trgids = []
brds = []
chs = []
cnts = []


# Lista para almacenar timestamps únicos
unique_timestamps = []


##Decimales

def Conversiondetiempo(value):
    # Definición de las conversiones
    conversions = {
        's': 1,
        'ms': 0.001,
        'µs': 1e-6,
        'ns': 1e-9,
        'ps':1e-12,

    }
    
    # Determinar la unidad a mostrar
    if value >= 1:
        converted_value = value
        unit = 's'
    elif value >= 0.001:
        converted_value = value / conversions['ms']
        unit = 'ms'
    elif value >= 1e-6:
        converted_value = value / conversions['µs']
        unit = 'µs'
    elif value >= 1e-9:
        converted_value = value / conversions['ns']
        unit = 'ns'
    else:
        converted_value = value / conversions['ps']
        unit = 'ps'

    # Formatear la salida
    num = f"{round(float(converted_value),2)} {unit}"
    return num, round(float(converted_value),2), unit

# Abrir y leer el archivo de texto línea por línea
with open('Run1_list.txt', 'r') as file:
    lines = file.readlines()
    
    # Omitir la primera línea (encabezados)
    for line in tqdm(lines[9:]):

        # Quitar espacios en blanco al principio y al final de la línea
        line = line.strip()

        # Si la línea no está vacía, procesar los datos
        if line:
            parts = line.split()
            if len(parts) == 5:  # Nueva entrada completa
                current_timestamp, current_trgid, brd, ch, cnt = parts
                timestamps.append(float(current_timestamp)/1000000)
                trgids.append(current_trgid)
                brds.append(brd)
                chs.append(ch)
                cnts.append(cnt)
                if current_timestamp not in unique_timestamps:
                    unique_timestamps.append(float(current_timestamp)/1000000)
            elif len(parts) == 3:  # Continuación de entrada existente
                brd, ch, cnt = parts
                timestamps.append(float(current_timestamp)/1000000)
                trgids.append(current_trgid)
                brds.append(brd)
                chs.append(ch)
                cnts.append(cnt)
            else:
                print(f"Línea no reconocida: {line}")



# Crear un DataFrame de pandas con los datos procesados
df = pd.DataFrame({
    'Tstamp_us': timestamps,
    'TrgID': trgids,
    'Brd': brds,
    'Ch': chs,
    'Cnt': cnts
})

N = len(df['Ch'])


##Filtro Eliminar Filas Con canales iguales a 0 y Creación de un diccionario que toma como llaves Time Stamp



j = 0
Intervalodetiempo = 0
DiccionarioPrincipal = {}
Totalidad = {}
Canales = []
tiempo = float(unique_timestamps[0])

for i in range(0,64):
    if i >= 0 and i <=29:
        a = df['Ch'][i]
        Canales.append(a)
        Totalidad[a]={'ConteosTotal': 0}
    elif i >=34 and i <= 63:
        a = df['Ch'][i]
        Canales.append(a)
        Totalidad[a]={'ConteosTotal': 0}
    


unit = Conversiondetiempo(float(unique_timestamps[1])-float(unique_timestamps[0]))[2]

for i in tqdm(range(len(unique_timestamps))):
    Channel = {}
    Channel["Canales"] = []
    Channel["Conteos"] = []
    Channel['Tiempo'] = []
    centinela = True

    if i != 0:
        tiempo = float(unique_timestamps[i]) - float(unique_timestamps[i-1])
    
    while j < N-1 and centinela:
        if int(df['Ch'][j]) >= 0 and int(df['Ch'][j]) <=29:
            con = Totalidad[df['Ch'][j]]['ConteosTotal']  
            cnt = int(df['Cnt'][j])
            Totalidad[df['Ch'][j]]['ConteosTotal'] = con + cnt
        elif int(df['Ch'][j]) >=34 and int(df['Ch'][j]) <= 63:
            con = Totalidad[df['Ch'][j]]['ConteosTotal']  
            cnt = int(df['Cnt'][j])
            Totalidad[df['Ch'][j]]['ConteosTotal'] = con + cnt
        
        
        if int(df['Cnt'][j]) > 0:  # Solo acumular si el conteo es mayor a 0
            Channel['Canales'].append(df['Ch'][j])
            Channel['Conteos'].append(df['Cnt'][j])
            Channel['Tiempo'].append(Conversiondetiempo(tiempo)[1])

        if df['Ch'][j] == '63':
            centinela = False 
            if int(df['Cnt'][j]) > 0: # Terminar el bucle para el último canal
                Channel['Canales'].append(df['Ch'][j])
                Channel['Conteos'].append(df['Cnt'][j])
                Channel['Tiempo'].append(Conversiondetiempo(tiempo)[1])
        j += 1
    # Verificar si hay al menos un conteo mayor a 0
    if any(int(c) > 0 for c in Channel['Conteos']):
        Intervalodetiempo += 1
        DiccionarioPrincipal[Intervalodetiempo] = {}
        DiccionarioPrincipal[Intervalodetiempo]['Instante de Tiempo'] = i+1
        DiccionarioPrincipal[Intervalodetiempo]['TStamp'] = unique_timestamps[i]
        DiccionarioPrincipal[Intervalodetiempo]['Trigger ID'] = df['TrgID'][j-1]
        DiccionarioPrincipal[Intervalodetiempo]['Channel'] = Channel

##Creación del histograma

ConteosTotales = []
for k in Totalidad.keys():
    ConteosTotales.append(Totalidad[k]['ConteosTotal'])



##Interfaz Gráfica

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interprete de CAEN (v 4.2)")
        self.geometry("800x600")

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(fill="both", expand=True)

        self.create_main_tab()

        self.details_tabs = {}

    def create_main_tab(self):
        main_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(main_tab, text="Menú")

        title_label = tk.Label(main_tab, text="Seleccione el Instante de Tiempo que Presenta Conteos:", font=("Arial", 16))
        title_label.pack(pady=10)

        search_frame = ttk.Frame(main_tab)
        search_frame.pack(pady=10)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=10)

        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_timestamp)
        search_button.pack(side=tk.LEFT, padx=10)

        range_label = tk.Label(main_tab, text=f"\nmín: 1   máx: {len(DiccionarioPrincipal)}", fg="black")
        range_label.pack(pady=5)

        self.search_status_label = tk.Label(main_tab, text="", fg="green")
        self.search_status_label.pack(pady=5)

        self.details_button = ttk.Button(main_tab, text="Mostrar Detalles", state=tk.DISABLED, command=self.show_details)
        self.details_button.pack(padx=10, pady=5)

        update_button = ttk.Button(main_tab, text="Reiniciar Búsqueda", command=self.update_search)
        update_button.pack(padx=10, pady=5)

        # Línea horizontal
        separator = ttk.Separator(main_tab, orient='horizontal')
        separator.pack(fill='x', padx=50, pady=20)

        # Título adicional
        additional_title_label = tk.Label(main_tab, text="Histograma de las Conteos Totales", font=("Arial", 14))
        additional_title_label.pack(pady=10)

        # Botón para mostrar diagrama de barras
        show_bar_chart_button = ttk.Button(main_tab, text="Mostrar Histograma de Conteos Totales ", command=self.show_bar_chart, width=35)
        show_bar_chart_button.pack(pady=10)

    def search_timestamp(self):
        search_query = self.search_entry.get()

        try:
            timestamp_index = int(search_query)
            if 1 <= timestamp_index <= len(DiccionarioPrincipal):
                self.details_button.config(state=tk.NORMAL)
                self.search_status_label.config(text="Instante de Tiempo seleccionado correctamente", fg="green")
            else:
                self.details_button.config(state=tk.DISABLED)
                self.search_status_label.config(text="No existe ese Instante de Tiempo. Intente nuevamente.", fg="red")
        except ValueError:
            self.details_button.config(state=tk.DISABLED)
            self.search_status_label.config(text="Entrada no válida. Introduzca un número.", fg="blue")

    def show_details(self):
        timestamp_index = int(self.search_entry.get())
        self.show_details_tab(timestamp_index)

    def show_details_tab(self, timestamp_index):
        timestamp_data = DiccionarioPrincipal.get(timestamp_index)
        if not timestamp_data:
            return

        timestamp = str(timestamp_index)
        if timestamp in self.details_tabs:
            self.tab_control.select(self.details_tabs[timestamp])
            return

        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=f"Instante de Tiempo con Conteos {timestamp}")
        self.tab_control.select(tab)

        # Encabezado principal (Trigger ID)
        lbl_header_tab = tk.Label(tab, text=f"Trigger ID: {timestamp_data['Trigger ID']}", font=("Arial", 18, "bold"))
        lbl_header_tab.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_close = tk.Button(lbl_header_tab , text="Cerrar", font=("Arial", 12), width=15, command=lambda: self.close_tab(tab,timestamp))
        btn_close.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)  # Ajuste de posición en la parte superior izquierda

        # Subtítulo (Time Stamp)
        lbl_subheader = tk.Label(tab, text=f"Número de Toma: {timestamp_data['Instante de Tiempo']}", font=("Arial", 12))
        lbl_subheader.pack(padx=10, pady=(0, 10))

        lbl_subheader = tk.Label(tab, text=f"Time Stamp Inicial: {Conversiondetiempo(float(unique_timestamps[0]))[0]}", font=("Arial", 12))
        lbl_subheader.pack(padx=10, pady=(0, 10))

        lbl_subheader = tk.Label(tab, text=f"Time Stamp: {Conversiondetiempo(timestamp_data['TStamp'])[0]}", font=("Arial", 12))
        lbl_subheader.pack(padx=10, pady=(0, 10))

        # Separador
        separator = ttk.Separator(tab, orient="horizontal")
        separator.pack(fill="x", padx=50, pady=(20, 10))

        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill="both", expand=True, padx=50)  # Ajuste de sangría

        tree_scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(tree_frame, columns=("Canales", "Conteos", "Tiempo"), show="headings", yscrollcommand=tree_scroll_y.set)
        tree.pack(fill="both", expand=True)
        tree_scroll_y.config(command=tree.yview)

        # Configurar encabezados en negrilla y centrados
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        tree.heading("Canales", text="Canales", anchor=tk.CENTER)
        tree.heading("Conteos", text="Conteos", anchor=tk.CENTER)
        tree.heading("Tiempo", text=f"Δ Tiempo ({unit})", anchor=tk.CENTER)

        tree.column("Canales", anchor=tk.CENTER, width=100)
        tree.column("Conteos", anchor=tk.CENTER, width=100)
        tree.column("Tiempo", anchor=tk.CENTER, width=100)

        for canal, conteo, tiempo in zip(timestamp_data['Channel']['Canales'],
                                             timestamp_data['Channel']['Conteos'],
                                             timestamp_data['Channel']['Tiempo']):
            tree.insert("", tk.END, values=(canal, conteo, tiempo))


        self.details_tabs[timestamp] = tab

    def close_tab(self, tab, timestamp):
        self.tab_control.forget(tab)
        del self.details_tabs[timestamp]

    def close_tab_chart(self, tab):
        self.tab_control.forget(tab)
        if len(self.tab_control.tabs()) == 1:
            self.state('normal')

    def update_search(self):
        # Reinicia la búsqueda limpiando la entrada y los mensajes de estado
        self.search_entry.delete(0, tk.END)
        self.search_status_label.config(text="")
        self.details_button.config(state=tk.DISABLED)
       

    def show_bar_chart(self):
        self.state('zoomed')  # Maximizar la ventana al abrir una nueva pestaña

        bar_chart_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(bar_chart_tab, text="Histograma de Conteos")
        self.tab_control.select(bar_chart_tab)

        lbl_header_bar_chart_tab = tk.Label(bar_chart_tab, text="Histograma de Conteos Totales", font=("Arial", 18, "bold"))
        lbl_header_bar_chart_tab.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_close = tk.Button(lbl_header_bar_chart_tab, text="Cerrar", font=("Arial", 12), width=15, command=lambda: self.close_tab_chart(bar_chart_tab))
        btn_close.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Crear figura del diagrama de barras
        fig = Figure(figsize=(16, 8))
        self.bar_chart_ax = fig.add_subplot(111)
        self.bar_chart_ax.bar(Canales, ConteosTotales)

        self.bar_chart_ax.set_xlabel('Canales')
        self.bar_chart_ax.set_ylabel('Conteos Totales')
        self.bar_chart_ax.tick_params(axis='x', labelsize=8)

        # Guardar los xticklabels
        self.xticklabels = self.bar_chart_ax.get_xticklabels()

        canvas = FigureCanvasTkAgg(fig, master=bar_chart_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.bind("<Configure>", self.on_resize)


    def on_resize(self, event):
        self.update_xtick_labels()

    def update_xtick_labels(self):
        width = self.winfo_width()
        step = 1 if width >= 1200 else 5  # Ajusta el paso según el ancho

        for index, label in enumerate(self.xticklabels):
            label.set_visible(index % step == 0)

        # Redibuja el gráfico para aplicar cambios
        self.bar_chart_ax.figure.canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()
