import streamlit as st
import math
import pandas as pd


def calculate_hyperband_iters(R, eta, verbose=False):

    result_dict = {}

    smax = math.floor(math.log(R, eta))
    B = (smax + 1) * R
    if verbose:
        print("smax: " + str(smax))
        print("B: " + str(B))
        print("")
    for s in reversed((range(smax + 1))):

        # n = int(math.ceil(int((B/R) * ((hta**s)/(s+1)))))
        n = int(math.ceil(int(B / R / (s + 1)) * eta ** s))
        r = R * (eta ** (-s))
        result_dict[n] = {"n_i": [], "r_i": []}

        if verbose:
            print("s: " + str(s))
            print("     n: " + str(n) + "   r: " + str(r))
            print("---------------------------")
        for i in range(s + 1):
            ni = math.floor(n * (eta ** (-i)))
            ri = r * (eta ** i)
            if verbose:
                print("     ni: " + str(ni) + "   ri (epochs): " + str(ri))
            result_dict[n]["n_i"].append(ni)
            result_dict[n]["r_i"].append(ri)
        if verbose:
            print("")
            print("===========================")
    return result_dict


st.title("Hyperband calculator")

st.image("hyperband_algorithm.png")

R = st.number_input(
    "Insert R, the maximum amount of resource that can be allocated to a single configuration",
    value=81,
)

eta = st.number_input(
    "Insert η, a value that controls the proportion of configurations discarded in each round of SuccessiveHalving",
    value=3,
)
budgets_per_bracket = calculate_hyperband_iters(R, eta, verbose=False)


for bracket, runs in budgets_per_bracket.items():
    st.subheader("bracket: " + str(bracket))

    st.dataframe(
        pd.DataFrame(
            {
                "num_configs": pd.Series(runs["n_i"], dtype="int"),
                "max_num_epochs": pd.Series(runs["r_i"], dtype="int"),
            }
        )
    )

