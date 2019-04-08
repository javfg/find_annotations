

#
# Selects rows with values higher than "value" in column "column".
#
def select_data(source, column, value):
    selected_data = source[source[column] >= value]
    print(f"* Selected {len(selected_data.index)} rows.")

    return selected_data


#
# Creates a tab separated file with annotation data
#
def create_tsv_file(go, kegg, min_support, min_identity, name, outfile):
    with open(f"{outfile}.tsv", "w") as tsv_file:
        tsv_file.write(f"### Functional Annotations Results for {name}\n")
        tsv_file.write(f"### Minimum identity score: {min_identity}%\n")
        tsv_file.write(f"### Minimum support score: {min_support}\n\n")

        tsv_file.write(f"Type\tTerm\tSupport\n")

        for go_item in go:
            tsv_file.write(f"GO\t{go_item['label']}\t{go_item['value']}\n")

        for kegg_item in kegg:
            tsv_file.write(f"KEGG\t{kegg_item['label']}\t{kegg_item['value']}\n")
