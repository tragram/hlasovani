import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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
# plt.rcParams['figure.figsize'] = (15, 5)

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


def vote_result_to_number(result):
    if result == 'A':
        return 1
    elif result == 'B':
        return -1
    else:
        return 0

def get_mp_by_id(id, list_of_mps):
    for mp in list_of_mps:
        if mp.id_poslanec == id:
            return mp
    return None


# extract MPs and create objects
current_mps = poslanci[poslanci['id_obdobi'] == 172]
final_mps = []
for index, row in current_mps.iterrows():
    person = osoby[osoby['id_osoba'] == row['id_osoba']]
    party = organy[organy['id_organ'] == row['id_kandidatka']]
    final_mps.append(MP(row['id_poslanec'], row['id_osoba'], party['nazev_organu_cz'].item(
    ), person['jmeno'].item(), person['prijmeni'].item()))

# prepare the data for PCA
votes_labels = hl_hlasovani['id_hlasovani'].tolist()
votes_labels.append('id_poslanec')
list_of_mp_votes = []
for mp in final_mps:
    mp_votes = list(map(vote_result_to_number,
                        hl_poslanec[hl_poslanec['id_poslanec'] == mp.id_poslanec]['vysledek'].tolist()))
    mp_votes.append(mp.id_poslanec)
    if len(mp_votes) != len(votes_labels):
        print("Ignoring {}, only voted {} times".format(mp, len(mp_votes)-1))
        continue
    list_of_mp_votes.append(pd.Series(data=mp_votes, index=votes_labels))

#PCA itself
df = pd.DataFrame(list_of_mp_votes, columns=votes_labels)
x = df.loc[:, votes_labels[:-1]].values
y = df.loc[:, ['id_poslanec']].values
x = StandardScaler().fit_transform(x)
pca = PCA(n_components=2)
principal_components = pca.fit_transform(x)
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
final_df = pd.concat([principal_df, df[['id_poslanec']]], axis=1)

# print(final_df)
# graph it
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('PC1', fontsize=15)
ax.set_ylabel('PC2', fontsize=15)
ax.set_title('Distribuce stran dle hlasování', fontsize=20)
parties = ["ANO2011", "Česká pirátská strana", "Česká strana sociálně demokratická", "Starostove a nezavisli", "Občanská demokratická strana",
           "Křesťanská a demokratická unie - Československá strana lidová", "Komunistická strana Čech a Moravy", "Svoboda a prima demokracie - Tomio Okamura", "TOP 09"]
colors = ["midnightblue", "black", "orange", "green", "royalblue", "gold", "red", "lightpink", "darkviolet"]

for index, mp in final_df.iterrows():
    mp_object=get_mp_by_id(mp['id_poslanec'], final_mps)
    party_index=parties.index(mp_object.party)
    ax.scatter(mp['PC1'], mp['PC2'], c=colors[party_index], s=50)

#ax.legend(parties)
ax.grid()
fig.savefig('graph.png')
""" sklearn_pca=sklearnPCA(n_components=2)
X_std = StandardScaler().fit_transform(X)
Y_sklearn = sklearn_pca.fit_transform(X_std) """
# print(hl_poslanec[hl_poslanec['id_poslanec']==final_mps[0].id_poslanec])
