import numpy as np
import ast
import random
import webbrowser
import string
from faker import Faker

# Liczba klientów
liczba_klientow = 5

# Wybór bazy danych
baza = "baza_wieczor_100"
#baza = "baza_noc_1AM_100"

# Zmienne do algorytmu
path=[0]
level=0
node=0
macierz=[]
koszt=0
infinity = float('inf')
macierz_nasza = []

# Zmienne do bazy danych
adresy = []
czasy = {}
odleglosci = {}
temp_time = []
temp_dist = []
time = []
dist = []
czas_temp = []
odleglosc_temp = []
randomlist =[]
wspolrzedne = []

# Zmienne do danych wyjściowych
best_route_id = []
best_route_addr = []
best_route_coor = []


# Wypełnienie przekątnej macierzy przez "inf"
def matrixinf(matrix,size):
    for i in range(size):
        for k in range(size):
            if i==k:
                matrix[i][k]=infinity
    matrix = np.array(matrix)
    return matrix

# Wypełnienie danej komórki macierzy przez "inf"
def infinity_point(matrix,row,col):
    for i in range(size):
        for k in range(size):
            if i==row:
                if k==col:
                    matrix[i][k]=infinity
    matrix = np.array(matrix)
    return matrix

# Wypełnienie danego wiersza i kolumny przez "inf"
def infinity_col_row(matrix,row,col):
    for i in range(size):
        for k in range(size):
            if i==row:
                matrix[i][k] = infinity
            if k==col:
                matrix[i][k] = infinity
    matrix=np.array(matrix)
    return matrix

# Redukcja macierzy
def reduce_row_col(matrix,size):
    matrix=np.array(matrix)
    reduce_cost=0
    for i in range(size):
        minimal = min(matrix[i])
        if minimal == infinity:
            minimal=0
        reduce_cost = reduce_cost + minimal
        for k in range(size):
            matrix[i][k]=(matrix[i][k]-minimal)
    pom=np.array(matrix)
    pom=pom.T
    for i in range(size):
        minimal = min(pom[i])
        if minimal == infinity:
            minimal=0
        reduce_cost = reduce_cost+ minimal
        for k in range(size):
            pom[i][k]=(pom[i][k]-minimal)
    matrix=pom.T
    return matrix, reduce_cost

# Implementacja algorytmu
def algorithm(m0,size,c0,node,level,path):
    global macierz, koszt
    macierz = m0
    all_matrix=[]
    all_cost=[]
    for i in range(size):
        pom = np.array(macierz)
        temp=infinity_point(pom,i,node)
        if level !=0:
            temp = infinity_point(temp,i,path[level-1])
        temp=infinity_col_row(temp,node,i)
        temp,cost1=reduce_row_col(temp, size)
        cost_path = c0 + float(m0[node][i])+cost1
        all_matrix.append(temp)
        all_cost.append(cost_path)
        if level != size-1:
            all_cost[0]=infinity
    lowest=np.argmin(all_cost)
    path.append(lowest)
    #print(all_cost)
    level=level+1
    if level >= size:
        return path
    matrixnext = all_matrix[lowest]
    costnext = all_cost[lowest]
    #print("MACIERZ NEXT")
    macierz =matrixnext
    koszt = costnext
    #print(matrixnext)
    #print(costnext)
    algorithm(matrixnext, size, costnext, lowest, level, path)
    return path, koszt


# Wczytywanie bazy danych
def czytaj_baze():
    global adresy, temp_dist, temp_time, wspolrzedne, czasy, odleglosci
    # Wczytywanie wszystkich współrzędnych
    name = baza + "/wspolrzedne.txt"
    file = open(name, "r", encoding="UTF-8")
    contents = file.read()
    wspolrzedne = ast.literal_eval(contents)
    file.close()
    #print(wspolrzedne)

    # Wczytywanie macierzy danych
    for j in range(4):
        name = baza + "/baza_danych_0_" + str(j) + ".txt"
        file = open(name, "r", encoding="UTF-8")
        contents = file.read()
        adresy_dict = ast.literal_eval(contents)
        file.close()
        adresy = adresy + adresy_dict['destination_addresses']

    # Wczytywanie macierzy danych
    nr_origin = 100
    nr_destination = 25
    origin = list(range(0,nr_origin))
    destination = list(range(0,nr_destination))

    for k in origin:
        for l in range(4):
            name = baza + "/baza_danych_" + str(k) + "_" + str(l) + ".txt"
            file = open(name, "r", encoding="UTF-8")
            contents = file.read()
            dictionary = ast.literal_eval(contents)
            file.close()
            for i in destination:
                temp_time.append(dictionary['rows'][0]['elements'][i]['duration']['value'])
                temp_dist.append(dictionary['rows'][0]['elements'][i]['distance']['value'])
        time = temp_time
        dist = temp_dist
        temp_time = []
        temp_dist = []
        czasy[k] = time
        odleglosci[k] = dist

    # Stworzenie bazy danych klientów
    fake = Faker('pl_PL')
    Faker.seed(13)
    dane_osob = []
    for _ in origin:
        dane_osob.append(fake.name())
    return adresy, dane_osob


# Utworzenie macierzy czasów
def lista_indeksów(ID_list):
    global macierz_nasza, czas_temp, liczba_klientow, czasy, randomlist
    randomlist = ID_list
    #print("Wylosowane indeksy: "+ str(randomlist))

    # Czas
    #print(type(int(randomlist[0])))
    for i in range(len(randomlist)):
        for j in randomlist:
            czas_temp.append(czasy[randomlist[i]][j])
        macierz_nasza.append(czas_temp)
        czas_temp = []
    macierz_temp = macierz_nasza
    macierz_nasza = []
    czas_temp = []
    #print("Wylosowana macierz: "+ str(macierz_temp))
    return macierz_temp


# Start algorytmu
def start_alg(ID_list):
    global best_route_coor, best_route_addr, best_route_id, size
    path = [0]
    level = 0
    node = 0
    randomlist = ID_list
    matrix = lista_indeksów(ID_list)
    size = len(matrix[0])
    matrix = matrixinf(matrix,size)
    m0,c0=reduce_row_col(matrix,size)
    route, ccoosstt=algorithm(m0,size,c0,node,level,path)
    #print("Najlepsza ścieżka to: " + str(route))
    #print("Jest to trasa o koszcie równym: " + str(ccoosstt))

    for i in route:
        best_route_id.append(randomlist[i])
        best_route_addr.append(adresy[randomlist[i]])
        best_route_coor.append(wspolrzedne[randomlist[i]])
    best_route_id_temp = best_route_id
    best_route_addr_temp = best_route_addr
    best_route_coor_temp = best_route_coor
    #print("Tablica adresów dla najlepszej trasy: ")
    #print(best_route_addr_temp)
    #print(best_route_id_temp)
    best_route_id = []
    best_route_addr = []
    best_route_coor = []
    return best_route_id_temp, ccoosstt, best_route_coor_temp


# Utworzenie mapy i trasy
def rysuj_mape(best_route_coor_temp):
    # RYSOWANIE TRASY NA MAPIE
    adres_mapy = "https://maps.googleapis.com/maps/api/staticmap?size=640x480&scale=2&maptype=roadmap"
    markery = ""
    markery_opcje = "&markers=color:red|size:mid|label:"
    trasa = "&path=color:0x0000ff|weight:5"
    klucz_API = "YOUR_GOOGLE_API_KEY"

    for i in range(len(best_route_coor_temp)):
        if i != (len(best_route_coor_temp)-1):
          # MARKERY
          markery = markery + markery_opcje + string.ascii_uppercase[i] + "|" + str(best_route_coor_temp[i][0]) + "," + str(best_route_coor_temp[i][1])
        # TRASA
        trasa = trasa + "|" + str(best_route_coor_temp[i][0]) + "," + str(best_route_coor_temp[i][1])
    adres_https = adres_mapy + markery + trasa + klucz_API
    return adres_https
    #webbrowser.open(adres_https)


# Start algorytmu
def wyznacz_trase(ID_list):
    czytaj_baze()
    trasa_opt, koszt_trasy, best_route_coor_temp = start_alg(ID_list)
    url = rysuj_mape(best_route_coor_temp)
    return url, trasa_opt, koszt_trasy