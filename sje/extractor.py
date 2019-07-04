#!/usr/bin/env python
import sqlparse


def flatten_all(fields):
    out = []

    def flatten(x, i, cur_name=""):
        if i >= len(x):
            return
        if x[i]["type"] != "RECORD":
            x[i]["name"] = cur_name + "_" + x[i]["name"] if cur_name else x[i]["name"]
            out.append(x[i])
        else:
            flatten(
                x[i]["fields"],
                0,
                cur_name + "_" + x[i]["name"] if cur_name else x[i]["name"],
            )
        flatten(x, i + 1, cur_name)

    flatten(fields, 0)
    return out


def flatten_all_as_sql(fields, trailer_clause=None):
    tmp = {}
    out = []

    def flatten(x, i, cur_name=""):
        if i >= len(x):
            return
        if x[i]["type"] != "RECORD":
            name = cur_name + "." + x[i]["name"] if cur_name else x[i]["name"]
            tmp[name] = x[i]["type"]
        else:
            flatten(
                x[i]["fields"],
                0,
                cur_name + "." + x[i]["name"] if cur_name else x[i]["name"],
            )
        flatten(x, i + 1, cur_name)

    flatten(fields, 0)
    for k, v in tmp.items():
        if "." in k:
            parent = k.split(".", 1)[0]
            child = k.split(".", 1)[1]
            column = k.replace(".", "_")
            out.append(f"CAST(JSON_EXTRACT({parent}, '$.{child}') AS {v}) AS {column}")
        else:
            out.append(f"CAST({k} AS {v})")
    sql = f"SELECT {', '.join(out)} {trailer_clause if trailer_clause else ''}"
    result = sqlparse.format(sql, reindent=True, keyword_case="upper")
    return result
