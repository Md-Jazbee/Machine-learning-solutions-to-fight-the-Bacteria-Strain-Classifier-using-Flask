from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import pylab

def circular_graph(fasta_file):
    record = SeqIO.read(fasta_file, "fasta")

    gd_diagram = GenomeDiagram.Diagram(record.id)
    gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
    gd_feature_set = gd_track_for_features.new_set()



    for feature in record.features:
        if feature.type != "gene":
            # Exclude this feature
            continue
        if len(gd_feature_set) % 2 == 0:
            color = colors.blue
        else:
            color = colors.lightblue
        gd_feature_set.add_feature(
            feature, sigil="ARROW", color=color, label=True, label_size=14, label_angle=0
        )

    # I want to include some strandless features, so for an example
    # will use EcoRI recognition sites etc.
    for site, name, color in [
        ("GAATTC", "EcoRI", colors.green),
        ("CCCGGG", "SmaI", colors.orange),
        ("AAGCTT", "HindIII", colors.red),
        ("GGATCC", "BamHI", colors.purple),
    ]:
        index = 0
        while True:
            index = record.seq.find(site, start=index)
            if index == -1:
                break
            feature = SeqFeature(FeatureLocation(index, index + len(site)))
            gd_feature_set.add_feature(
                feature,
                color=color,
                name=name,
                label=True,
                label_size=2,
                label_color=color,
            )
            index += len(site)

    gd_diagram.draw(format="linear", pagesize="A4", fragments=4, start=0, end=len(record))
    #gd_diagram.write("plasmid_linear_nice.pdf", "PDF")
    #gd_diagram.write("plasmid_linear_nice.eps", "EPS")
    gd_diagram.write("my_app/static/graph/plasmid_linear_nice.svg", "SVG")

    gd_diagram.draw(
        format="circular",
        circular=True,
        pagesize=(50 * cm, 50 * cm),
        start=0,
        end=len(record),
        circle_core=0.5,
    )
    #gd_diagram.write("plasmid_circular_nice.pdf", "PDF")
    #gd_diagram.write("plasmid_circular_nice.eps", "EPS")
    gd_diagram.write("my_app/static/graph/plasmid_circular_nice.svg", "SVG")


def histogram(fasta_file):
    sizes = [len(rec) for rec in SeqIO.parse(fasta_file, "fasta")]
    pylab.hist(sizes, bins=20)
    pylab.title(
        "%sequences\nLengths %i to %i" % (len(sizes), min(sizes), max(sizes))
    )
    pylab.xlabel("Sequence length (bp)")
    pylab.ylabel("Count")

    pylab.savefig('my_app/static/graph/seq_histogram.svg') 
    return sizes