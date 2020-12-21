def ErlangLoss(demand, stack_num, used_num):
    possibility = ((demand / (2 * stack_num)) ** used_num) / \
        (sum([(demand / (2 * stack_num)) ** t for t in range(used_num + 1)]))
    return possibility


def RelocateTime(used_num):
    return used_num


def ExpectLotR(demand_ls, stack_num, spot_num_ls):
    demand_total = sum(demand_ls)
    exp_r = sum([sum([(demand_ls[i] /
                       (demand_total * 2 * stack_num) *
                       ErlangLoss(demand_ls[i], stack_num, v))
                      for v in range(spot_num_ls[i])])
                 for i in range(len(demand_ls))])
    return exp_r
