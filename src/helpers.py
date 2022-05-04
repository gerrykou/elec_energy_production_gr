#!/usr/bin/env python 

list_of_content = [
    {"new_header": "time", "row": 4},
    {"new_header": "net_load", "row": 10},
    {"new_header": "total_imports", "row": 24},
    {"new_header": "total_exports", "row": 30},
    {"new_header": "lignite_total", "row": 51},
    {"new_header": "diesel_total", "row": 55},
    {"new_header": "gas_total", "row": 83},
    {"new_header": "hydro_total", "row": 106,},
    {"new_header": "res_total", "row": 187},
]

lignite_units_list = [
    {"new_header": "lign_ag_dimitrios_1", "row": 35},
    {"new_header": "lign_ag_dimitrios_2", "row": 36},
    {"new_header": "lign_ag_dimitrios_3", "row": 37},
    {"new_header": "lign_ag_dimitrios_4", "row": 38},
    {"new_header": "lign_ag_dimitrios_5", "row": 39},
    {"new_header": "lign_aminteo_1", "row": 40},
    {"new_header": "lign_aminteo_2", "row": 41},
    {"new_header": "lign_kardia_1", "row": 42},
    {"new_header": "lign_kardia_2", "row": 43},
    {"new_header": "lign_kardia_3", "row": 44},
    {"new_header": "lign_kardia_4", "row": 45},
    {"new_header": "lign_megalopoli_3", "row": 46},
    {"new_header": "lign_megalopoli_4", "row": 47},
    {"new_header": "lign_meliti", "row": 48},
    {"new_header": "lign_ptolemaida_3", "row": 49},
    {"new_header": "lign_ptolemaida_4", "row": 50},
    ]

ngas_units_list = [
    {"new_header": "ngas_elpedison_thess", "row": 58},
    {"new_header": "ngas_elpedison_thisvi", "row": 59},
    {"new_header": "ngas_elpedison_thisvi(st)", "row": 60},
    {"new_header": "ngas_korinthos_power", "row": 61},
    {"new_header": "ngas_motor_oil", "row": 62},
    {"new_header": "ngas_protergia_cc", "row": 63},
    {"new_header": "ngas_aliveri_5", "row": 64},
    {"new_header": "ngas_aluminio(GT1)", "row": 65},
    {"new_header": "ngas_aluminio(GT2)", "row": 66},
    {"new_header": "ngas_aluminio(ST)", "row": 67},
    {"new_header": "ngas_iron_1", "row": 68},
    {"new_header": "ngas_iron_2", "row": 69},
    {"new_header": "ngas_iron_3", "row": 70},
    {"new_header": "ngas_this_iron", "row": 71},
    {"new_header": "ngas_komotini(GT1)", "row": 72},
    {"new_header": "ngas_komotini(GT2)", "row": 73},
    {"new_header": "ngas_komotini(ST)", "row": 74},
    ]

[list_of_content.append(i) for i in lignite_units_list]


# list_of_content = [
#     {"new_header": "time", "row": 4, "col_start":1, "col_end":26},
#     {"new_header": "net_load", "row": 10, "col_start":1, "col_end":26},
#     {"new_header": "total_imports", "row": 24, "col_start":1, "col_end":26},
#     {"new_header": "total_exports", "row": 30, "col_start":1, "col_end":26},
#     {"new_header": "lignite_total", "row": 51, "col_start": 1, "col_end": 26},
#     {"new_header": "diesel_total", "row": 55, "col_start": 1, "col_end": 26},
#     {"new_header": "gas_total", "row": 83, "col_start":1, "col_end":26},
#     {"new_header": "hydro_total", "row": 106, "col_start":1, "col_end":26},
#     {"new_header": "res_total", "row": 187, "col_start": 1, "col_end": 26},
# ]
