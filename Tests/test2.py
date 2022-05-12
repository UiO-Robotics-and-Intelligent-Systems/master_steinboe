
def area(a,b):
    c=(b[0]-a[0], b[1]-a[1])
    return c[0]*c[1]

def hypervolume(ref, pointset):
    # given that the pointset is paretoFront, and correct order
    sum=0
    for i in range(len(pointset)):
        if pointset[i][0]<ref[0]: # not needed maybe, but ok
            continue
        sum+=area(ref,pointset[i])
        ref=(pointset[i][0],ref[1])
    return sum

pointset=[(1,0),(2,-1),(3,-2),(2,-3)]
ref = (0,-3) # trenger bare å sette en verdi for y her :)   y <= min stability fitness (-100 or something).

a=hypervolume(ref,pointset)
print(a)

