import datetime

# TODO:
# 1. Numele fisierelor in care sunt salvate datele trebuie sa aiba formatul: Lista_cursanti_AN_LUNA_ZI_ORA_MINUTE.txt/csv
# 2. Stergerea inregistrarilor din cadrul listei de cursanti (adaugarea de index pentru fiecare inregistrare si stergere pe baza de index)
# 2'. Stergerea inregistrarilor pe baza de CNP
# 3. Incarcarea datelor dintr-un fisier de cursanti in cadrul listei cu eliminarea duplicatelor.
# 4. Adaugati validarea pentru unicitatea CNP-ului in functia prelucrare_date_citite
# 5. Adaugati o comanda care sa permita actualizarea numelui/prenumelui/CNP-ului unei inregistrari dintr-o lista pe baza de ID.
# 6. Adaugati o comanda care sa permita concatenarea contintului din mai multe fisiere TXT/CSV (indicate in cadrul comenzii). Concatenarea se va putea face
# doar intre fisiere de acelasi tip. (TXT cu TXT si CSV cu CSV)


lista_cursanti = []
_id = 1


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
    # TODO: Adaugarea validarii pentru unicitatea CNP-ului
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
    # TODO: Tratarea cazului pentru format_fisier == csv
    current_time = datetime.datetime.now()
    nume_fisier = f"Lista_cursanti_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.{format_fisier}"
    if format_fisier == "txt":
        with open(nume_fisier, mode="w") as my_file:
            my_file.write("Nume \t Prenume \t CNP \n")
        with open(nume_fisier, mode="a") as my_file:
            for cursant in lista_cursanti:
                my_file.write(cursant['nume'] + "\t" + cursant['prenume'] + "\t" + cursant['cnp'] + "\n")
    elif format_fisier == "csv":
        with open(nume_fisier, mode="w") as my_file:
            my_file.write("Nume,Prenume,CNP\n")
        with open(nume_fisier, mode="a") as my_file:
            for cursant in lista_cursanti:
                my_file.write(f"{cursant['nume']},{cursant['prenume']},{cursant['cnp']}\n")
    print(f"Fisierul {nume_fisier} a fost salvat cu success.")


def sterge_inregistrare(val, tip_stergere):
    global lista_cursanti
    if tip_stergere == "id":
        val = int(val)
    for cursant in lista_cursanti:
        if cursant[f'{tip_stergere}'] == val:
            lista_cursanti.remove(cursant)
            print(f"A fost sters cursantul {cursant['nume']} {cursant['prenume']}")
            return True
    print(f"Cursantul cu {tip_stergere}-ul {val} nu a fost gasit.")
    return False


def verifica_duplicat(cnp_introdus):
    global lista_cursanti
    for cursant in lista_cursanti:
        if cursant['cnp'] == cnp_introdus:
            print(f"CNP-ul {cnp_introdus} exista deja in lista de cursanti.")
            return False
    return True


def incarca_date(nume_fisier):
    global lista_cursanti, _id
    extensie = nume_fisier.split(".")[1]
    if extensie == "txt":
        with open(nume_fisier, mode="rt") as my_file:
            continut_fisier = my_file.readlines()
        for i in range(1, len(continut_fisier)):
            date = continut_fisier[i].split()
            nume, prenume, cnp = prelucrare_date_citite(date)
            if verifica_duplicat(cnp):
                dict_cursant = {"id": _id, "nume": nume, "prenume": prenume, "cnp": cnp}
                _id += 1
                lista_cursanti.append(dict_cursant)


if __name__ == "__main__":
    while True:
        dict_cursant = dict()
        new_line = input("Introduceti un nou cursant sau introduceti EXIT/SAVE/DELETE/DISPLAY/LOAD.")
        if new_line == "EXIT":
            print("Programul se inchide")
            break
        if new_line == "SAVE":
            format_fisier = input("In ce format doriti salvarea datelor? txt/csv?").lower()
            salveaza_date(format_fisier)
            continue
        if new_line == "DELETE":
            tip_stergere = input("Stergerea se face pe baza de ID/CNP?").lower()
            id_sters = input(f"Introduceti {tip_stergere}-ul cursantului pe care vreti sa il stergeti: ")
            sterge_inregistrare(id_sters, tip_stergere)
            continue
        if new_line == "DISPLAY":
            print(lista_cursanti)
            continue
        if new_line == "LOAD":
            nume_fisier = input("Introduceti numele fisierului din care se face incarcarea datelor: ")
            incarca_date(nume_fisier)
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
        # TODO: Adaugare validare pentru nume + prenume
        if not validare_nume(nume):
            print("Numele introdus nu este valid.")
        if not validare_nume(prenume):
            print("Prenumele introdus nu este valid.")
        dict_cursant = {"id": _id, "nume": nume, "prenume": prenume, "cnp": cnp}
        lista_cursanti.append(dict_cursant)
        _id += 1
        print(lista_cursanti)
