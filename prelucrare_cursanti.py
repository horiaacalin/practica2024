def prelucrare_date_citite(data):
    if len(data) < 3:
        print("Datele introduse pentru cursant sunt incomplete")
        return False
    nume = data[0]
    if len(data) == 3:
        prenume = data[1]
        cnp = data[2]
    if len(data) == 4:
        prenume = data[1] + " " + data[2]
        cnp = data[3]
    return nume, prenume, cnp


def validare_nume(nume_introdus):
    return True


def validare_cnp(cnp_introdus):
    # Verificam daca lungimea CNP-ului introdus este de 13 caractere
    if len(cnp_introdus) != 13:
        print("Lungimea CNP-ului nu este corecta.")
        return False
    if not cnp_introdus.isdigit():
        print("CNP-ul trebuie sa contina doar cifre.")
        return False

    # Calculam cifra de control
    constanta_control = "279146358279"
    suma = 0
    for i in range(12):
        suma += int(cnp_introdus[i]) * int(constanta_control[i])
    cifra_control_calculata = suma % 11
    if cifra_control_calculata == 10:
        cifra_control_calculata = 1

    # Verificam cifra_control_calculata vs cifra_control din CNP
    if cifra_control_calculata != int(cnp_introdus[12]):
        print("Cifra de control a CNP-ului nu este corecta.")
        return False
    return True

def salveaza_date(format_fisier):
    global lista_cursanti
    #TODO: Tratarea cazului pentru format_fisier == csv
    if format_fisier == "txt":
        with open("lista_cursanti.txt", mode="w") as my_file:
            my_file.write("Nume \t Prenume \t CNP \n")
        with open("lista_cursanti.txt", mode="a") as my_file:
            for cursant in lista_cursanti:
                my_file.write(cursant['nume'] + "\t" + cursant['prenume'] + "\t" + cursant['cnp'] + "\n")
        print("Fisierul lista_cursanti.txt a fost salvat cu success.")



if __name__ == "__main__":
    lista_cursanti = []
    while True:
        dict_cursant = dict()
        new_line = input("Introduceti un nou cursant sau introduceti EXIT sau SAVE.")
        if new_line == "EXIT":
            print("Programul se inchide")
            break
        if new_line == "SAVE":
            format_fisier = input("In ce format doriti salvarea datelor? txt/csv?").lower()
            salveaza_date(format_fisier)
            continue
        date_cursant = new_line.split()
        rezultat = prelucrare_date_citite(date_cursant)
        if not rezultat:
            continue
        nume = rezultat[0]
        prenume = rezultat[1]
        cnp = rezultat[2]
        if not validare_cnp(cnp):
            continue
        #TODO: Adaugare validare pentru nume + prenume
        if not validare_nume(nume):
            print("Numele introdus nu este valid.")
        if not validare_nume(prenume):
            print("Prenumele introdus nu este valid.")
        # dict_cursant['nume'] = nume
        # dict_cursant['prenume'] = prenume
        # dict_cursant['cnp'] = cnp
        dict_cursant = {"nume": nume, "prenume": prenume, "cnp": cnp}
        lista_cursanti.append(dict_cursant)
        print(lista_cursanti)

