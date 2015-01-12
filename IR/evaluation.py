"""
Calculate P@5, P@10 of phase1

Use seqEval to evaluate phase2
"""


def seqEval(list1, correct):
    # Evaluate the ordering of a seuence `list1` with correctly-ordered seq `correct`
    # Note that the two input seqs must both contain the same numbers (but in different order

    # Validation
    for i in list1:
        assert i in correct, "Error: Invalid input sequence, " + str(i) + " is not in" + str(correct)
    err = float(0)
    for i in list1:
        if list1.index(i) == len(list1) - 1:
            err += len(correct) - correct.index(i) - 1
        elif correct.index(i) == len(correct) - 1:
            err += len(list1) - list1.index(i) - 1
        else:
            suberr = 0
            cp1 = list1[list1.index(i) + 1:]
            cp2 = correct[correct.index(i) + 1:]
            for j in cp2:
                if j not in cp1:
                    suberr += 1
            for j in cp1:
                if j not in cp2:
                    suberr += 1
            err += suberr
    return float(err) / float(len(list1) * (len(list1) - 1))


def evalPhase2():
    baseline = open("baseline.txt", "r").readlines()
    ans = open("selfeval.txt", "r").readlines()
    totalerr = float(0)
    for i in range(len(baseline)):
        anslist = ans[i].strip().split()
        baselist = baseline[i].strip().split()
        totalerr += seqEval(anslist, baselist)
    print "Estimated sorting err for Phase 2 is " + str(totalerr / float(len(baseline)))
    return


def evalPhase1():
    print("Phase 1 Evaluation:")
    ta = open("phase1_pooling_result.txt").readlines()
    result = open("result.txt").readlines()

    assert len(ta) == len(result), "Error: Wrong input files"
    totalpat5 = float(0)
    totalpat10 = float(0)
    for i in range(len(ta)):
        talist = ta[i].strip().split()
        relist = result[i].strip().split()
        pat5 = float(0)
        pat10 = float(0)
        for j in range(5):
            if relist[j] in talist:
                pat5 += 1
                totalpat5 += 1
        for j in range(10):
            if relist[j] in talist:
                pat10 += 1
                totalpat10 += 1
        print("P@5  of query #" + str(i) + " = " + str(float(pat5)/float(5)) + ", P@10" + " = " + str(float(pat10)/float(10)))
    print("Average P@5  = " + str(totalpat5/float(100)) + ", average P@10 = " + str(totalpat10/float(200)))
    
    return


if __name__ == "__main__":
    print("##########")
    evalPhase1()
    print("##########")
    evalPhase2()
    print("##########")

