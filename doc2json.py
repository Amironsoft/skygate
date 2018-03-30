# coding: utf-8
import numpy as np
import pandas as pd
import json
from pprint import pprint
from itertools import product
import os
import fnmatch

auth_comp_dict = {}


def apply_auth(author_line):
    global auth_comp_dict
    auth_str_list = author_line.split("|")
    auth_ans_list = []
    for auth in auth_str_list:
        company = ['']
        try:
            name, surname, *company = auth.split(", ")
        except:
            print(auth)
            name = auth
            surname = ''
        full_auth_name = name.lower().strip() + " " + surname.lower().strip()
        if company:
            auth_comp_dict[full_auth_name] = company[0]
        else:
            auth_comp_dict[full_auth_name] = ''
        auth_ans_list.append(full_auth_name)
    return auth_ans_list


def apply_comp(author_line):
    auth_str_list = author_line.split("|")
    auth_company_list = []
    for auth in auth_str_list:
        try:
            name, surname, *company = auth.split(", ")
        except:
            print(auth)
            name = auth
            surname = ''
        auth_company_list.append(' '.join(c.lower() for c in company))
    return auth_company_list


def get_agg_df(nodes, rename_dict):
    df_local = pd.DataFrame.from_records(nodes, columns=["source", "target"])
    df_local["total"] = [a + " " + b for a, b in nodes]
    total_list = df_local["total"].values.tolist()
    df_local["count"] = df_local["total"].apply(lambda x: total_list.count(x))
    df_local = df_local.drop_duplicates(subset=["total"])
    df_local['source_num'] = df_local['source'].apply(lambda x: rename_dict[x])
    df_local['target_num'] = df_local['target'].apply(lambda x: rename_dict[x])
    return df_local


def save_json(df_local, nodes, uniq_tokens, ofile, auth_mode=False):
    if auth_mode:
        cur_nodes = [{"name": a, "group": auth_comp_dict.get(a, 'undefined'), "company": auth_comp_dict.get(a, 'undefined')} for a in uniq_tokens]
    else:
        cur_nodes = [{"name": a, "group": 1} for a in uniq_tokens]
    cur_dict = {"nodes": cur_nodes}

    cur_links = []
    for source, target, value in zip(df_local["source_num"].values, df_local["target_num"].values,
                                     df_local["count"].values):
        cur_links.append({
            "source": int(source),
            "target": int(target),
            "value": int(value)
        })

    cur_dict["links"] = cur_links
    # pprint(comp_dict)
    with open(ofile, 'w') as outfile:
        json.dump(cur_dict, outfile, indent=4)


def process_file(ifile, ofile):
    df = pd.read_csv(ifile, encoding='cp1251')
    print("columns:", df.columns)
    print("len:", len(df))

    df_keywords = df['keywords'].dropna().values
    uniq_keywords = set()
    err_num = 0
    for line in df_keywords:
        if line.startswith("Document Type"):
            err_num += 1
        else:
            words = [w.strip().lower() for w in line.split(", ")]
            uniq_keywords |= set(words)

    print("total keywords rows:", len(df_keywords), "err_num:", err_num, "uniq_keys:", len(uniq_keywords))
    uniq_keywords = sorted(uniq_keywords)

    print("uniq_keywords", uniq_keywords[:10])

    df['author_list'] = df['author_df'].apply(apply_auth)
    df['author_company_list'] = df['author_df'].apply(apply_comp)
    df['author_list'].head()
    df['author_company_list'].head()

    err_count = 0
    uniq_auth = set()
    uniq_comp = set()

    auth_nodes = []
    company_nodes = []

    for i, row in df.groupby("id_df"):
        title = row['title_df'].values[0]
        auth = row['author_df'].values[0]
        keywords = row['keywords'].values[0]

        print("id:", i)
        print("title:", title)
        print("auth:", auth)

        if str(keywords) != 'nan' and not keywords.startswith("Document Type"):
            print("keywords items", keywords)
        else:
            print("no keywords")
            err_count += 1

        auth_list = apply_auth(auth)
        comp_list = apply_comp(auth)

        uniq_auth |= set(auth_list)
        uniq_comp |= set(comp_list)

        print("#" * 4)
        for a, b in product(auth_list, repeat=2):
            if a != b:
                print('\t\t', a, b)
                auth_nodes.append([a, b])

        for a, b in product(comp_list, repeat=2):
            if a != b:
                print('\t\t', a, b)
                company_nodes.append([a, b])
        print("#" * 4)

        print("auth items", auth_list)
        print("comp items", comp_list)
        print("_" * 30)
    print("err_count", err_count)

    rename_auth_dict = {c: i for i, c in enumerate(uniq_auth)}
    rename_comp_dict = {c: i for i, c in enumerate(uniq_comp)}

    df_company = get_agg_df(company_nodes, rename_comp_dict)
    df_auth = get_agg_df(auth_nodes, rename_auth_dict)

    df_auth.sort_values("count", ascending=False, inplace=True)
    df_company.sort_values("count", ascending=False, inplace=True)

    print(df_auth.sort_values("count", ascending=False).head())

    # auth_nodes
    # company_nodes

    ofile_comp = ofile.replace('.json', 'comp_data.json')
    save_json(df_company, company_nodes, uniq_comp, ofile_comp)

    ofile_auth = ofile.replace('.json', 'auth_data.json')

    save_json(df_auth, auth_nodes, uniq_auth, ofile_auth, auth_mode=True)

    df_auth.to_csv(ofile_auth.replace('.json', '.tsv').replace("json/", "csv/"))
    df_company.to_csv(ofile_comp.replace('.json', '.tsv').replace("json/", "csv/"))


if __name__ == '__main__':
    idir = r"gmech/"
    odir = r"static/json/"

    for ifile in fnmatch.filter(os.listdir(idir), "*.csv"):
        print(idir+ifile)
        ofile = ifile.replace(".csv", ".json")
        process_file(idir + ifile, odir + ofile)
