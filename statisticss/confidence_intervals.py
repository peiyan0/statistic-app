# confidence interval for 2 populations
def two_pop_CI(args):
    print("Confidence Interval for Two Populations:")
    pop1, pop2, t, e = args
    n1, x1, s1 = pop1
    n2, x2, s2 = pop2
    # assume t-distribution 
    if e == "equal":
        df = n1+n2 - 2
        Sp = ( ((n1 - 1)* s1**2 + (n2 - 1) * s2 **2) / df) ** 0.5
        Sx1_x2 = Sp * (1/n1 + 1/n2) ** 0.5
    if e == "unequal":
        s12_n1 = (s1 ** 2) / n1
        s22_n2 = (s2 ** 2) / n2
        # floor function
        df = int((s12_n1+s22_n2) ** 2 / (((s12_n1**2) / (n1-1)) + ((s22_n2**2) / (n2-1))) //1 )
        Sx1_x2 = (s12_n1 + s22_n2) ** 0.5

    moe = t*Sx1_x2 # margin of error
    mean_diff = x1 - x2
    print(e)
    print(f'df: {df}')
    print(f"= ({x1} - {x2}) +- {t}({Sx1_x2:.4f})")
    print(f"= {mean_diff:.4f} +- {moe:.4f}")
    lower_bound = mean_diff - moe
    upper_bound = mean_diff + moe
    t_test = mean_diff / Sx1_x2
    return f"Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f}) \nt-test: {t_test:.3f}" 

# dependant data 
def dep_data(args):
    print("Dependent Data T-Test:")
    before, after = args
    d = [i - j for i,j in zip(before, after)] 
    n = len(before)
    mean = sum(d)/n 
    sum2 = sum(i ** 2 for i in d)
    Sd = ( (sum2 - (sum(d)**2) / n) / (n-1)) ** 0.5
    t_test = mean / (Sd/(n ** 0.5))
    print(f"mean d: {mean:.4f}\nSd = {Sd:.4f}\nt-test: {t_test:.3f}")

# 2 sample proportion
def two_samp_prop(args):
    print("Two Sample Proportion")
    pop1, pop2 = args
    n1,p1 = pop1
    n2,p2 = pop2
    x1 = n1*p1
    x2 = n2*p2
    p_mean = (x1+x2) / (n1+n2)
    q_mean = 1 - p_mean
    z_test = (p1-p2)/((p_mean*q_mean)*(1/n1 + 1/n2))**0.5
    return f"z-test: {z_test:.4f}"