import plotly
from plotly.graph_objs import *
import igraph as ig
import json
import requests
import os
import fnmatch
import pandas as pd


def create_graph_html(data, ofile):
    N = len(data['nodes'])
    L = len(data['links'])
    Edges = [(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
    G = ig.Graph(Edges, directed=False)

    # to_delete_ids = [v.index for v in G.vs if '@enron.com' not in v['label']]
    # G.delete_vertices(to_delete_ids)

    labels = []
    group = []

    companies = []
    for node in data['nodes']:
        if 'company' in node:
            labels.append(node['name'] + "<br>" + node["company"])
            companies.append(node['company'])
        elif 'group' in node:
            labels.append(node['name'] + "<br>links:" + str(node["group"]))
        else:
            labels.append(node['name'])
            companies.append(1)
        group.append(node['group'])
    companies = sorted(set(companies))

    colors = [companies.index(g) if g in companies else 1 for g in group]

    layt = G.layout('kk', dim=3)
    Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
    Yn = [layt[k][1] for k in range(N)]  # y-coordinates
    Zn = [layt[k][2] for k in range(N)]  # z-coordinates

    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    trace1 = Scatter3d(x=Xe,
                       y=Ye,
                       z=Ze,
                       mode='lines',
                       line=Line(color='rgb(125,125,125)', width=1),
                       hoverinfo='none'
                       )

    trace2 = Scatter3d(x=Xn,
                       y=Yn,
                       z=Zn,
                       mode='markers',  # 'markers+text'
                       name='actors',
                       marker=Marker(symbol='dot',
                                     size=6,
                                     # color=group,
                                     color=colors,
                                     colorscale='Viridis',
                                     line=Line(color='rgb(50,50,50)', width=0.5)
                                     ),
                       text=labels,
                       hoverinfo='text',
                       )

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=axis_title
                )

    layout = Layout(
        title=title,
        width=1000,
        height=1000,
        showlegend=False,
        scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
        ),
        margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
            Annotation(
                showarrow=False,
                text=left_title,
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                    size=14
                )
            )
        ]),
    )

    # x = trace2.get("x")
    # y = trace2.get("y")
    # z = trace2.get("z")
    #
    # clusters = dict(
    #     alphahull=7,
    #     name="y",
    #     opacity=0.1,
    #     type="mesh3d",
    #     x=x, y=y, z=y
    # )

    # data = Data([trace1, trace2, clusters])
    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=ofile)


def prepare_data(data, ofile_degree):
    print("links:", len(data["links"]))
    # data["links"] = [row for row in data["links"] if row["value"] > 1]
    # print("new_links:", len(data["links"]))
    degree_dict = {}

    for row in data["links"]:
        a = row["source"]
        b = row["target"]
        v = row["value"]
        if a in degree_dict:
            degree_dict[a] += 1
        else:
            degree_dict[a] = 1

        if b in degree_dict:
            degree_dict[b] += 1
        else:
            degree_dict[b] = 1

    node_list = []
    header = ["name", "degree"]

    for i, node in enumerate(data["nodes"]):
        name = node["name"]
        degree = degree_dict.get(i, 0)
        node_list.append([name, degree])

    df_node = pd.DataFrame.from_records(node_list, columns=header)
    df_node.sort_values("degree", inplace=True, ascending=False)
    df_node.to_csv(ofile_degree, sep='\t')
    return data


if __name__ == '__main__':

    axis_title = ''
    idir = r'static/json/'
    odir = 'static/html/'
    print(idir)

    files = fnmatch.filter(os.listdir(idir), 'G*all*.json')
    print(files)
    for file_name in files:
        left_title = ""  # left_title
        title = file_name.replace(".json", "")
        ifile = idir + file_name
        ofile = odir + file_name.replace('.json', '_comp.html')

        print('\t', ifile)
        print('\t', ofile)
        ofile_degree = odir + file_name.replace('.json', '_degree.txt')
        data = json.load(open(ifile))
        data = prepare_data(data, ofile_degree)
        print(["{}: {}".format(k, len(v)) for k, v in data.items()])
        create_graph_html(data, ofile)

        # try:
        # if not os.path.exists(ofile):
        #     create_graph_html(data, ofile)
        # else:
        #     print("\tfile already exists")
        # create_graph_html(data, ofile)
        # except Exception as ex:
        #     print(ex)
