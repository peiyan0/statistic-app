def anova(arrays):
    print("ANOVA: ")
    k = len(arrays)
    n = sum(len(array)for array in arrays)
    grand_mean = sum(sum(array)for array in arrays) / n

    df_between = k - 1
    df_within = n - k
    SSB = sum(len(array) * (sum(array) / len(array) - grand_mean) ** 2 for array in arrays)
    SSW = sum(sum((x - sum(array) / len(array)) ** 2 for x in array) for array in arrays)
    MSB = SSB / df_between
    MSW = SSW / df_within
    F_test = MSB / MSW
    # print(f"k = {k:<3}n = {n:<4}grand mean = {grand_mean:<8.4f}SSB = {SSB:<10.4f}SSW = {SSW:.4f}")
    # return f"F-test: {F_test:<8.4f} DF(between): {df_between:<3} DF(within): {df_within}"
    return {
        "k": k,
        "n": n,
        "grand_mean": round(grand_mean,4),
        "SSB": round(SSB,4),
        "SSW": round(SSW,4),
        "MSB": round(MSB,4),
        "MSW": round(MSW,4),
        "F_test": round(F_test,4),
        "df_between": round(df_between,4),
        "df_within": round(df_within,4)
    } 

