from tree import Tree

gb_xp_singleton = Tree.from_list(["XP", ["X'", "X"]])
gb_xp_w_comp = Tree.from_list(["XP", ["X'", "X", ["YP", ["Y'", "Y"]]]])
gb_xp_w_comp_spec = Tree.from_list(
    ["XP",
     ["ZP", ["Z'", "Z"]],
     ["X'", "X", ["YP", ["Y'", "Y"]]]])
gb_xp_w_spec_no_comp = Tree.from_list(
    ["XP",
     ["ZP", ["Z'", "Z"]],
     ["X'", "X"]])

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
        ["I'", "I",
            ["VP",
                ["V'", "V",
                    ["NP",
                        ["DP", ["D'", "D"]],
                        ["N'", "N"]]]]]])
gb_pp_comp_cp_comp = Tree.from_list(
    ["IP",
        ["NP",
            ["DP", ["D'", "D"]],
            ["N'", "N", ["PP", ["P'", "P", ["NP", ["N'", "N"]]]]]],
        ["I'", "I",
            ["VP",
                ["V'", "V",
                    ["CP",
                        ["C'", "C",
                            ["IP",
                                ["NP", ["N'", "N"]],
                                ["I'", "I", ["VP", ["V'", "V"]]]]]]]]]])

min_xp_singleton = Tree.from_list(["XP"])
min_xp_w_comp = Tree.from_list(["XP", "X", "YP"])
min_xp_w_comp_spec = Tree.from_list(
    ["XP", "ZP", ["X'", "X", "YP"]])
min_xp_w_spec_no_comp = Tree.from_list(
    ["?P",
     ["ZP", ["Z'", "Z"]],
     ["?'", "?", "XP"]])

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
gb_pp_comp_cp_comp = Tree.from_list(
    ["IP",
        ["NP",
            ["DP", ["D'", "D"]],
            ["N'", "N", ["PP", ["P'", "P", ["NP", ["N'", "N"]]]]]],
        ["I'", "I",
            ["VP",
                ["V'", "V",
                    ["CP",
                        ["C'", "C",
                            ["IP",
                                ["NP", ["N'", "N"]],
                                ["I'", "I", ["VP", ["V'", "V"]]]]]]]]]])
