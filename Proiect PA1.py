import json
from datetime import datetime

def citeste_intrebari_si_optiuni(file_path):
    intrebari = {}
    optiuni = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        domeniu = None
        dificultate = None
        intrebari_domeniu = {}
        optiuni_domeniu = []
        for line in lines:
            line = line.strip()
            if line.startswith("["):
                domeniu, dificultate = line[1:-1].split("-")
                intrebari[f"{domeniu}-{dificultate}"] = {}
                optiuni[f"{domeniu}-{dificultate}"] = []
            elif line.startswith("-"):
                intrebare, raspuns = line[1:].split(":")
                intrebari[f"{domeniu}-{dificultate}"][intrebare.strip()] = raspuns.strip()
            elif line.startswith("*"):
                optiuni_domeniu.append(line[1:].strip().split("/"))
                intrebarie_cheie = list(intrebari[f"{domeniu}-{dificultate}"].keys())[-1]
                optiuni[f"{domeniu}-{dificultate}"].append(optiuni_domeniu)
                optiuni_domeniu = []
    return intrebari, optiuni


def joc_nou(intrebari, optiuni, numar_intrebari):
    scor = 0
    incercari = []
    incercari_corecte = 0
    nr_intrebare = 0
    schimba_utilizat = False
    litera_utilizat = False
    afisare_utilizat = False

    domeniu = input("Alege domeniul intrebarilor si dificultatea acestora (ex : orase-usor/general-greu): ").lower()
    while domeniu not in intrebari.keys():
        print("Domeniul selectat nu exista. Alege din 'orase-usor' sau 'general-greu'.")
        domeniu = input("Alege domeniul intrebarilor si dificultatea acestora (ex : orase-usor/general-greu): ").lower()

    intrebari_selectate = intrebari[domeniu]
    optiuni_selectate = optiuni[domeniu]

    for cheie, intrebare in intrebari_selectate.items():
        nr_intrebare += 1
        print("--------------------------")
        print(cheie)
        for i in optiuni_selectate[nr_intrebare - 1]:
            print(i)
        incercare = input("Scrieti raspunsul corect: (ajutoare : scrieti 'schimba' pentru a schimba intrebarea"
                          " scrieti 'afisare' pentru a afisa jumatate din raspuns, 'litera' pentru prima litera) : ").lower()

        incercari.append(incercare)

        if incercare == 'schimba':
            if schimba_utilizat:
                print("Ai folosit deja optiunea 'schimba'. Nu o mai poti utiliza.")
            else:
                schimba_utilizat = True
                continue

        if incercare == 'afisare':
            if afisare_utilizat:
                print("Ai folosit deja acest hint")
                incercare = input("Scrieti raspunsul corect sau folositi alte hinturi ('schimba'/'litera') : ")
            else:
                raspuns = intrebari_selectate[cheie]
                lungime_raspuns = len(raspuns)
                jumatate_raspuns = raspuns[:lungime_raspuns // 2]
                print("Jumatate din raspuns:", jumatate_raspuns)
                incercare = input("Scrieti raspunsul corect cu ajutorul hintului 'afisare' : ")
                afisare_utilizat = True

        if incercare == 'litera':
            if litera_utilizat:
                print("Ai folosit deja acest hint")
                incercare = input("Scrieti raspunsul corect sau folositi alte hinturi('schimba'/'afisare') : ")
                if incercare == 'afisare':
                    if afisare_utilizat:
                        print("Ai folosit deja acest hint")
                        incercare = input("Scrieti raspunsul corect sau folositi alte hinturi('schimba') : ")
                        if incercare == 'schimba':
                            if schimba_utilizat:
                                print("Ai folosit deja acest hint")
                                incercare = input("Scrieti raspunsul corect (nu mai aveti hinturi):")
                            else:
                                print("Intrebarea a fost schimbata")
                                schimba_utilizat = True
                    else:
                        raspuns = intrebari_selectate[cheie]
                        lungime_raspuns = len(raspuns)
                        jumatate_raspuns = raspuns[:lungime_raspuns // 2]
                        print("Jumatate din raspuns:", jumatate_raspuns)
                        incercare = input("Scrieti raspunsul corect sau folositi alte hinturi : ")
                        afisare_utilizat = True
            else:
                prima_litera = intrebari_selectate[cheie][0]
                print("Prima literă din răspuns:", prima_litera)
                incercare = input("Scrieti raspunsul corect cu ajutorul hintului 'litera' : ")
                litera_utilizat = True

        incercari_corecte += verificare_raspuns(intrebare, incercare)
        if nr_intrebare >= numar_intrebari:
            break

    display_scor(incercari_corecte, incercari)
    return incercari_corecte


def verificare_raspuns(raspuns, incercare):
    if raspuns == incercare:
        print("Corect")
        return 1
    else:
        print("Gresit")
        return 0


def display_scor(incercari_corecte, incercari):
    print("--------------------------")
    print("Rezultat : ")
    print("--------------------------")

    scor = int(incercari_corecte)
    print("Intrebari corecte : " + str(scor))
    return scor


def joaca_dinnou():
    raspuns = input("Vrei sa joci dinnou (da sau nu) :")
    raspuns = raspuns.lower()

    if raspuns == "da":
        return True
    else:
        return False


def actualizare_highscore(nume, scor):
    scoruri_mari = []
    try:
        with open("scoruri_mari.json", "r") as file:
            scoruri_mari = json.load(file)
    except FileNotFoundError:
        pass

    scoruri_mari.append({"nume": nume, "scor": scor, "data_ora": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    scoruri_mari.sort(key=lambda x: x['scor'], reverse=True)
    scoruri_mari = scoruri_mari[:10]

    with open("scoruri_mari.json", "w") as file:
        json.dump(scoruri_mari, file, indent=4)

    print("\nTop 10 Scoruri Mari:")
    for i, intrare in enumerate(scoruri_mari):
        data_ora = intrare.get('data_ora', 'N/A')
        print(f"{i + 1}. {intrare['nume']}: {intrare['scor']} ({data_ora})")

def start_joc():
    print("Bine ai venit la 'Vrei sa fii milionar?'!!")
    nume = input("Introduceti numele daca vrei sa fi milionar: ")
    numar_intrebari = input("Cate intrebari doresti sa raspunzi? (Apasand enter = 10, maximul de intrebari este de 20): ")
    if numar_intrebari == "":
        numar_intrebari = 10
    elif int(numar_intrebari) > 20:
        numar_intrebari = input("Nu avem atatea intrebari, va rog sa alegeti cate intrebari doriti de la 1 la 20: ")
        if int(numar_intrebari) > 20:
            print("Nu avem atatea intrebari, asa pentru tine iti dau 15 intrebari ")
            numar_intrebari = 15
    else:
        numar_intrebari = int(numar_intrebari)
    scor = joc_nou(intrebari, optiuni, numar_intrebari)
    actualizare_highscore(nume, scor)


file_path = 'intrebari.txt'
intrebari, optiuni = citeste_intrebari_si_optiuni(file_path)
start_joc()
while joaca_dinnou():
    start_joc()

print("La revedere")
