import csv
from datetime import datetime


# Functia pentru a citi fisierul CSV
def citeste_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"Fișierul {file_path} nu a fost găsit.")
        return []
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        return []


# Functia pentru a procesa datele
def proceseaza_date(date):
    statistici = {
        'total_bani_cheltuiti': 0,
        'total_curse': 0,
        'curse_completed': 0,
        'curse_canceled': 0,
        'curse_per_an': {},
        'curse_per_oras': {},
        'curse_per_luna': {},
        'distanta_totala_km': 0,
        'curse_per_produs': {},
        'timp_total_secunde': 0,
        'cea_mai_scurta_cursa_min': float('inf'),
        'cea_mai_lunga_cursa_min': 0
    }

    for cursa in date:
        fare_amount = 0
        if cursa['Fare Amount']:
            fare_amount = cursa['Fare Amount']
        # Total bani cheltuiti
        statistici['total_bani_cheltuiti'] += float(fare_amount)

        # Total curse
        statistici['total_curse'] += 1

        # Curse completed vs canceled
        if cursa['Trip or Order Status'] == 'COMPLETED':
            statistici['curse_completed'] += 1
        elif cursa['Trip or Order Status'] == 'CANCELED':
            statistici['curse_canceled'] += 1

        # Curse per an
        anul = cursa['Request Time'].split('-')[0]
        if anul not in statistici['curse_per_an']:
            statistici['curse_per_an'][anul] = 0
        statistici['curse_per_an'][anul] += 1

        # Curse per oras
        oras = cursa['City']
        if oras not in statistici['curse_per_oras']:
            statistici['curse_per_oras'][oras] = 0
        statistici['curse_per_oras'][oras] += 1

        # Curse per luna
        luna = cursa['Request Time'].split('-')[1]
        if luna not in statistici['curse_per_luna']:
            statistici['curse_per_luna'][luna] = 0
        statistici['curse_per_luna'][luna] += 1

        # Distanta totala (in miles)
        distance_miles = 0
        if cursa['Distance (miles)']:
            distance_miles = cursa['Distance (miles)']

        statistici['distanta_totala_km'] += float(distance_miles)

        # Curse per produs
        produs = cursa['Product Type']
        if produs:
            if produs not in statistici['curse_per_produs']:
                statistici['curse_per_produs'][produs] = 0
            statistici['curse_per_produs'][produs] += 1

        # Perioada totala petrecuta in curse
        if cursa['Trip or Order Status'] == 'COMPLETED':
            stop_cursa = datetime.strptime(cursa['Dropoff Time'], "%Y-%m-%d %H:%M:%S %z %Z")
            start_cursa = datetime.strptime(cursa['Begin Trip Time'], "%Y-%m-%d %H:%M:%S %z %Z")

            durata_secunde = (stop_cursa - start_cursa).seconds

            statistici['timp_total_secunde'] += durata_secunde

            durata_minute = durata_secunde / 60

            if durata_minute < statistici['cea_mai_scurta_cursa_min']:
                statistici['cea_mai_scurta_cursa_min'] = durata_minute
            if durata_minute > statistici['cea_mai_lunga_cursa_min']:
                statistici['cea_mai_lunga_cursa_min'] = durata_minute

    # Convertește timpul total în secunde în minute, ore și zile
    statistici['timp_total_minute'] = statistici['timp_total_secunde'] / 60
    statistici['timp_total_ore'] = statistici['timp_total_minute'] / 60
    statistici['timp_total_zile'] = statistici['timp_total_ore'] / 24

    return statistici


# Functia pentru a afisa statisticile
def afiseaza_statistici(statistici):
    print(f"Total bani cheltuiti: {statistici['total_bani_cheltuiti']} RON")
    print(f"Total curse: {statistici['total_curse']}")
    print(f"  COMPLETED: {statistici['curse_completed']}")
    print(f"  CANCELED: {statistici['curse_canceled']}")
    print("Total curse per an:")
    for an, numar in statistici['curse_per_an'].items():
        print(f"  {an}: {numar}")
    print("Total curse per oras:")
    for oras, numar in statistici['curse_per_oras'].items():
        print(f"  {oras}: {numar}")
    print("Total curse per luna:")
    for luna, numar in statistici['curse_per_luna'].items():
        print(f"  {luna}: {numar}")
    print(f"Distanta totala: {statistici['distanta_totala_km']} km")
    print("Curse per produs:")
    for produs, numar in statistici['curse_per_produs'].items():
        print(f"  {produs}: {numar}")
    print(f"Perioada totala petrecuta in curse: {statistici['timp_total_secunde']} secunde")
    print(f"  Minute: {statistici['timp_total_minute']}")
    print(f"  Ore: {statistici['timp_total_ore']}")
    print(f"  Zile: {statistici['timp_total_zile']}")
    print(f"Cea mai scurta cursa: {statistici['cea_mai_scurta_cursa_min']} minute")
    print(f"Cea mai lunga cursa: {statistici['cea_mai_lunga_cursa_min']} minute")


# Functia principala
def main():
    file_path = 'trips_data.csv'
    date = citeste_csv(file_path)
    if date:
        statistici = proceseaza_date(date)
        afiseaza_statistici(statistici)
    else:
        print("Nu au fost găsite date pentru procesare.")


if __name__ == "__main__":
    main()
