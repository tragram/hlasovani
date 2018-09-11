import pandas as pd
import matplotlib.pyplot as plt


class MP:
    def __init__(self, id_poslanec, id_osoba, party, first_name, last_name):
        self.id_poslanec = id_poslanec
        self.id_osoba = id_osoba
        self.party = party
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return self.first_name + " " + self.last_name+" ("+str(self.party)+") ["+str(self.id_poslanec)+"/"+str(self.id_osoba)+"]"


# pd.set_option('display.mpl_style', 'default')  # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)

# import the databases
hl_hlasovani = pd.read_csv(
    'data/hl2017s.unl', header=None, sep='|', encoding='windows-1250', usecols=range(0, 17))
hl_hlasovani.columns = ['id_hlasovani', 'id_organ', 'schuze', 'cislo', 'bod', 'datum', 'cas', 'pro', 'proti',
                        'zdrzel', 'nehlasoval', 'prihlaseno', 'kvorum', 'druh_hlasovani', 'vysledek', 'nazev_dlouhy', 'nazev_kratky']

hl_poslanec = pd.read_csv(
    'data/hl2017h1.unl', header=None, sep='|', encoding='windows-1250', usecols=[0, 1, 2])
hl_poslanec.columns = ['id_poslanec', 'id_hlasovani', 'vysledek']

osoby = pd.read_csv(
    'data/osoby.unl', header=None, sep='|', encoding='windows-1250', usecols=range(0, 9))
osoby.columns = ['id_osoba', 'pred', 'jmeno', 'prijmeni',
                 'za', 'narozeni', 'pohlavi', 'zmena', 'umrti']

poslanci = pd.read_csv(
    'data/poslanec.unl', header=None, sep='|', encoding='windows-1250', usecols=range(0, 15))
poslanci.columns = ['id_poslanec', 'id_osoba', 'id_kraj', 'id_kandidatka', 'id_obdobi',
                    'web', 'ulice', 'obec', 'psc', 'email', 'telefon', 'fax', 'psp_telefon', 'facebook', 'foto']

organy = pd.read_csv(
    'data/organy.unl', header=None, sep='|', encoding='windows-1250', usecols=range(0, 10))
organy.columns = ['id_organ', 'id_nadrazeny_organ', 'id_typ_organu', 'id_zkratka',
                  'nazev_organu_cz', 'nazev_organu_en', 'od_organ', 'do_organ', 'priorita', 'ci_organ_base']

current_mps = poslanci[poslanci['id_obdobi'] == 172]
final_mps = []
for index, row in current_mps.iterrows():
    person = osoby[osoby['id_osoba'] == row['id_osoba']]
    party = organy[organy['id_organ'] == row['id_kandidatka']]
    final_mps.append(MP(row['id_poslanec'], row['id_osoba'], party['nazev_organu_cz'].item(
    ), person['jmeno'].item(), person['prijmeni'].item()))
for mp in final_mps:
    print(mp)
