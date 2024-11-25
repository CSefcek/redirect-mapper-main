# EXCEL RELATED ESSENTIAL REQUIREMENTS

#open an Excel file ***DONE!!!***

#read the first columns of its first worksheet: list of old URLs, list of new URLs (in this case URLs must be scraped with Screaming Frog) ***DONE!!!***
#OR!!!
#remove all the non required columns of the Screaming Frog
#read all the remaining columns of the Screaming Frog (URL, status code, title, description, h1, redirect destination)
#open another Excel file containing the list of new URLs

#output a new Excel file or create a second worksheet within the same file             ***DONE!!!***
#create 3 columns in the new worksheet: URL sorgente, Status code, URL destinazione)
#fill the 1st column with the list of old URLs (keep the same order of the input file) ***DONE!!!***
#fill the 2nd column with correct status code
#fill the 3rd column with matched destination URLs

import pandas as pd
from rapidfuzz import fuzz

#INPUTS

#Legge tutto il contenuto della tab "crawl" da due file separati
source_file = pd.read_excel("crawl-current-website.xlsx", sheet_name="crawl")
#source_file.head()

destination_file = pd.read_excel("crawl-new-website.xlsx", sheet_name="crawl")
#destination_file.head()

# Verifica delle colonne richieste
if "URL sorgente" not in source_file.columns:
    raise ValueError("La colonna 'URL sorgente' non è presente nel file delle URL sorgente.")
if "URL destinazione" not in destination_file.columns:
    raise ValueError("La colonna 'URL destinazione' non è presente nel file delle URL destinazione.")



# Legge il contenuto delle specifiche colonne
#url_sorgente = pd.read_excel("crawl-current-website.xlsx", usecols=[0])
urls_source = source_file["URL sorgente"].str.strip()
urls_destination = destination_file["URL destinazione"].str.strip()

# Controllo del numero di URL caricate
print(f"Sono state caricate {len(urls_source)} URL sorgenti")
print(f"Sono state caricate {len(urls_destination)} URL destinazione")


#LOGICA DEL MAPPING

# Creazione liste da Series di Pandas
urls_source_list = list(urls_source)
urls_destination_list = list(urls_destination)

# Creazione lista per salvare i mappings, loop delle liste e logica con RapidFuzz
mappings = []

for src_url in urls_source_list:
    best_match = None
    best_score = 0
    for dest_url in urls_destination_list:
        score = fuzz.ratio(src_url,dest_url)

        if score > best_score:
            best_score = score
            best_match = dest_url

    # Determina status code da implementare
    status_code = 200 if src_url in urls_destination_list else 301

    # Aggiunge il risultato alla lista dei mappings
    mappings.append({"URL sorgente": src_url, "Status code da implementare": status_code, "Best Match": best_match, "Score": best_score})




#OUTPUTS

# Converte i risultati in un Datarame di Pandas
mappings_df = pd.DataFrame(mappings)

# Salva i risultati in un Excel
mappings_df.to_excel("mapping_results.xlsx", sheet_name="Results", index=False)

print("Mapping completato! File salvato come 'mapping_results.xlsx'.")
