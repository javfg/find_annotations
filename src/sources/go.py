import datetime
import pandas

from yaspin import yaspin


#
# Sums data of data frame into a single list.
#
def accumulate_go(source):
    start_time = datetime.datetime.now()

    with yaspin(text="Parsing GO annotations...", color="cyan") as sp:

        go = pandas.DataFrame({"accession": [], "description": []})

        # Explodes go accesion values in lists to dataframe.
        for row in source.dropna().iteritems():
            for element in str(row[1]).split(";"):
                description, accession = element[:-1].rsplit("[",1)
                go.loc[len(go)] = (accession, description.strip())

        # Add column of counts.
        go["count"] = go.groupby("accession")["accession"].transform("count")
        go = (
            go.drop_duplicates(subset="accession")
            .sort_values(by="count", ascending=False)
            .reset_index(drop=True)
        )

        time_diff = (datetime.datetime.now() - start_time).total_seconds()

        sp.text = f"Parsing GO annotations => Task done in {time_diff} seconds."
        sp.ok("✔")
        print (f"* Found {sum(go['count'])} GO terms from which {len(go)} were unique.")

        return go
