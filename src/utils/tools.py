

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
def create_tps_file(go, kegg, min_support, min_identity, name):
        file_name=f"Results-{name}.tps"
        with open(file_name,'w') as file:
                file.write(f"###Functional Annotations Results for {name}\n")
                file.write(f"###Minimum identity score: {min_identity}%\n")
                file.write(f"###Minimum support score: {min_support}\n")
                file.write(f"\tGo Annotations:\n")
                file.write(f"Term\tSupport\n")
                for go_item in go:
                        file.write(f"{go_item['label']}\t")
                        file.write(f"{go_item['value']}\n")
                file.write(f"\tKEGG Annotations:\n")
                file.write(f"Term\tSupport\n")
                for kegg_item in kegg:
                        file.write(f"{kegg_item['label']}\t")
                        file.write(f"{kegg_item['value']}\n")
        file.close()
