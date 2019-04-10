

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
#
# Creates an entry inside a collection.
#

def create_entry(entry, link_body, color):
    return {
        "value": entry['count'],
        "label": entry.description.capitalize(),
        "xlink": {"href": f"{link_body}{entry.accession}"},
        "color": color
    }

#
# Creates a list of entries inside a collection.
#

def create_list(source, min_support, link_body, color, source_name):
    result = []

    for index, entry in source.iterrows():
        if (entry['count'] > min_support):
            result.append(create_entry(entry, link_body, color))
    print (f"* Filtered {len(source)-len(result)} {source_name} unique annotations.")
    return result



#
# Creates a HTML file with multi-pie plot embedded in it.
#

def create_html_file(go, kegg, min_identity, min_support, plot_file_name,name,outfile):
    with open(f"{outfile}.html", "w") as html_file:
        html_file.write(f"\
            <!doctype html>\
            <html>\
                <head>\
                    <meta charset=\"utf-8\">\
                    <title>{name}</title>\
                    <style>\
                        body {{background-color: #f9f9f9; font-family: Helvetica, Sans-Serif;}}\
                        a {{color: blue; text-decoration: none;}}\
                    </style>\
                </head>\
                \
                <body>\
                    <h1 style=\"text-align: center;\">Functional annotations of {name}</h1>\
                    <div style=\"display: flex;\">\
                        <object type=\"image/svg+xml\"data=\"{plot_file_name}\" height=\"800\"></object>\
                        <div>\
                            <div>\
                                <h4>Minimum identity score: {min_identity} %</h4>\
                                <h4>Minimum support score: {min_support}</h4>\
                                <div style=\"display: flex;\">")
        if go:

                    html_file.write(f"\
                                    <h2>GO:</h2>\
                                    <ul>")

                    for go_item in go:
                        html_file.write(f"<li><strong>{go_item['value']}x</strong>\
                            <a target=\"_blank\" href=\"{go_item['xlink']['href']}\">{go_item['label']}</a></li>")
                    if kegg:
                        html_file.write(f"\
                                        </ul>")
        if kegg:

                    html_file.write(f"\
                                        <h2>KEGG:</h2>\
                                        <ul>")

                    for kegg_item in kegg:
                        html_file.write(f"<li><strong>{kegg_item['value']}x</strong>\
                            <a target=\"_blank\" href=\"{kegg_item['xlink']['href']}\">{kegg_item['label']}</a></li>")

        html_file.write(f"\
                                    </ul>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </body>\
            </html>")
