import pygal
import os
import datetime

from yaspin import yaspin
from pygal.style import Style
from utils.tools import create_tsv_file
from utils.tools import create_html_file

# Plots the multi pie chart and stats.
def plot(go, kegg, min_support, min_identity,name, outfile):
    start_time = datetime.datetime.now()
    with yaspin(text="Generating statistics and plotting charts...", color="cyan") as sp:
        custom_style = Style(
            opacity='0.8',
            opacity_hover='0.5',
            title_font_size=36,
            tooltip_font_size=10,
            inner_radius=0.75,
            plot_background="rgba(249, 249, 249, 1)"
        )

        multi_pie = pygal.Pie(height=800, tooltip_border_radius=1, style=custom_style)


        if go:
            multi_pie.add('GO', go)
        if kegg:
            multi_pie.add('KEGG', kegg)

        plot_file_name = f"{outfile}.svg"
        multi_pie.render_to_file(plot_file_name)

        create_html_file(go, kegg, min_identity, min_support, os.path.basename(plot_file_name),name,outfile)
        create_tsv_file(go, kegg, min_support, min_identity,name, outfile)
        time_diff = (datetime.datetime.now() - start_time).total_seconds()

        sp.text = f"Generating statistics and plotting charts => Task done in {time_diff} seconds."
        sp.ok("✔")
