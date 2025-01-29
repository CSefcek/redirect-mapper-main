import pandas as pd
from rapidfuzz import fuzz

#INPUTS

#Legge tutto il contenuto della tab "crawl" da due file separati
source_file = pd.read_excel("crawl-current-website.xlsx", sheet_name="crawl")

destination_file = pd.read_excel("crawl-new-website.xlsx", sheet_name="crawl")

# Verifica delle colonne richieste
if "URL sorgente" not in source_file.columns:
    raise ValueError("La colonna 'URL sorgente' non è presente nel file delle URL sorgente.")
if "URL destinazione" not in destination_file.columns:
    raise ValueError("La colonna 'URL destinazione' non è presente nel file delle URL destinazione.")
if "Status code" not in destination_file.columns:
    raise ValueError("La colonna 'Status code' non è presente nel file delle URL destinazione.")



# Legge il contenuto delle specifiche colonne
urls_source = source_file["URL sorgente"].str.strip()
urls_destination = destination_file["URL destinazione"].str.strip()
status_codes = destination_file["Status code"]

# Controllo del numero di URL caricate
print(f"Sono state caricate {len(urls_source)} URL sorgenti")
print(f"Sono state caricate {len(urls_destination)} URL destinazione")


#LOGICA DEL MAPPING

# Creazione liste da Series di Pandas
urls_source_list = list(urls_source)
urls_destination_list = list(urls_destination)
status_codes_list = list(status_codes)

# Creazione dizionario per associarci i rispettivi status code
#print("Unique Status Codes in Destination File:", status_codes.unique()) #DEBUG
destination_status_mapping = dict(zip(urls_destination_list, status_codes_list))


# Creazione lista per salvare i mappings, loop delle liste e logica con RapidFuzz
mappings = []
destinations_no_200 = []
seen_non_200_urls = set() 

for src_url in urls_source_list:
    best_match = None
    best_score = 0

    # Calcola miglior match
    for dest_url in urls_destination_list:
        score = fuzz.ratio(src_url,dest_url)

        if score > best_score:
            best_score = score
            best_match = dest_url

    # Determina status code da implementare
    status_code = 200 if src_url in urls_destination_list else 301

    # Aggiunge il risultato alla lista dei mappings
    mappings.append({"URL sorgente": src_url, "Status code da implementare": status_code, "Best Match": best_match, "Score": best_score})

    # Se il best match ha status code diverso da 200, aggiungilo alla lista delle destinazioni no 200, senza ripetizioni
    if best_match and destination_status_mapping.get(best_match) != 200:
        if best_match not in seen_non_200_urls:
            destinations_no_200.append({
                "URL destinazione": best_match,
                "Status code attuale": destination_status_mapping.get(best_match)
                })
            seen_non_200_urls.add(best_match)
    

#OUTPUTS

# Converte i risultati in un Datarame di Pandas
mappings_df = pd.DataFrame(mappings)
destinations_no_200_df = pd.DataFrame(destinations_no_200)


# Identifica le URL di destinazione inutilizzate
used_destinations = set(mappings_df["Best Match"].dropna())
unused_destinations_set = {dest_url for dest_url in urls_destination_list if dest_url not in used_destinations} # Python set comprehension

unused_destinations_df = pd.DataFrame({"URL destinazione": list(unused_destinations_set)})


# Salva i risultati in un Excel
with pd.ExcelWriter("mapping_results.xlsx") as writer:
    mappings_df.to_excel(writer, sheet_name="Results", index=False)
    destinations_no_200_df.to_excel(writer, sheet_name="Destinazioni no 200", index=False)
    unused_destinations_df.to_excel(writer, sheet_name="Destinazioni inutilizzate", index=False)

print("Mapping completato! File salvato come 'mapping_results.xlsx'.")
