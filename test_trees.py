from tree import Tree

gb_np_n = Tree.from_list(["NP", ["N'", "N"]])
gb_np_d_n = Tree.from_list(
    ["NP",
        ["DP", ["D'", "D"]],
        ["N'", "N"]])
gb_simple_trans_clause = Tree.from_list(
    ["IP",
        ["NP",
            ["DP", ["D'", "D"]],
            ["N'", "N"]],
        ["I'",
            "I",
            ["VP",
                ["V'",
                    "V",
                    ["NP",
                        ["DP", ["D'", "D"]],
                        ["N'", "N"]]]]]])

min_dp_leaf = Tree.from_list(["DP"])
min_dp_d_n = Tree.from_list(["DP", "D", "NP"])
min_simple_trans_clause = Tree.from_list(
    ["TP",
        ["DP", "D", "NP"],
        ["T'",
            ["T"],
            ["VP",
                ["V"],
                ["DP", "D", "NP"]]]])
