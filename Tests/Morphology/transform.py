import random
import sys

"""
Send in 8-len list of legLengst to positions - return positions
Send in positions to positionsToString - return string og leg settings (send this to unity)"""

def positions(legLength):
    """

    Return: [leg0, leg1, leg2, leg3] (list(list(int)))
    leg0/2 = [Upper ScaleY, Upper PositionZ, lower scaleY, Lower positionZ]
    leg1/3 = [Upper ScaleY, Upper PositionX, lower scaleY, lower positionX]
    """
    leg0U_legLength = legLength[0]
    leg0L_legLength = legLength[1]
    leg3U_legLength = legLength[2]
    leg3L_legLength = legLength[3]

    leg1U_legLength = legLength[4]
    leg1L_legLength = legLength[5]
    leg2U_legLength = legLength[6]
    leg2L_legLength = legLength[7]

    # body:
    bodyDiam = 1
    bodyRad = bodyDiam/2

    ###### leg0 and 2 ##########
    # leg0Upper
    leg0U_scaleY = leg0U_legLength/2
    leg0U_positionZ = -(leg0U_scaleY+bodyRad)
    # leg0Lower
    leg0L_scaleY = leg0L_legLength/2
    leg0L_positionZ = -(leg0L_scaleY+leg0U_legLength+bodyRad)
    # leg0
    leg0 = [leg0U_scaleY, leg0U_positionZ, leg0L_scaleY, leg0L_positionZ]

    # leg2Upper
    leg2U_scaleY = leg2U_legLength/2
    leg2U_positionZ = leg2U_scaleY+bodyRad
    # leg2Lower
    leg2L_scaleY = leg2L_legLength/2
    leg2L_positionZ = leg2L_scaleY+leg2U_legLength+bodyRad
    #leg2
    leg2 = [leg2U_scaleY, leg2U_positionZ, leg2L_scaleY, leg2L_positionZ]

    ###### leg1 and 3 ##########
    # leg1Upper
    leg1U_scaleY = leg1U_legLength/2
    leg1U_positionX = -(leg1U_scaleY+bodyRad)
    # leg1Lower
    leg1L_scaleY = leg1L_legLength/2
    leg1L_positionX = -(leg1L_scaleY+leg1U_legLength+bodyRad)
    # leg1
    leg1 = [leg1U_scaleY, leg1U_positionX, leg1L_scaleY, leg1L_positionX]

    # leg3Upper
    leg3U_scaleY = leg3U_legLength/2
    leg3U_positionX = leg3U_scaleY+bodyRad
    # leg3Lower
    leg3L_scaleY = leg3L_legLength/2
    leg3L_positionX = leg3L_scaleY+leg3U_legLength+bodyRad
    #leg3
    leg3 = [leg3U_scaleY, leg3U_positionX, leg3L_scaleY, leg3L_positionX]

    return [leg0,leg1,leg2,leg3]


def positionsToString(legs):
    """
    Input: legs = [leg0, leg1, leg2, leg3] (list(list(int)))
    leg0/2 = [Upper ScaleY, Upper PositionZ, lower scaleY, Lower positionZ]
    leg1/3 = [Upper ScaleY, Upper PositionX, lower scaleY, lower positionX]
    

    return:
        pos leg0Upper U0P
        pos leg1Upper U1P
        pos leg2Upper U2P
        pos leg3Upper U3P
        legLen leg0Upper U0S
        legLen leg1Upper U1S 
        legLen leg2Upper U2S
        legLen leg3Upper U3S
    
        // lower
        pos leg0Lower L0P
        pos leg1Lower L1P
        pos leg2Lower L2P
        pos leg3Lower L3P
        legLen leg0Lower L0S
        legLen leg1Lower L1S
        legLen leg2Lower L2S
        legLen leg3Lower L3S
    return string: "U0P+ U1P+ U2P+ U3P+   U0S+ U1S+ U2S+ U3S+      L0P+ L1P+ L2P+ L3P+   L0S+ L1S+ L2S+ L3S+  
    """
    otherScales = [0.3,0.3,0.3]
    otherPos =[0,0,0]
    
    # default Scales
    U0S = otherScales.copy() 
    U1S = otherScales.copy()
    U2S = otherScales.copy() 
    U3S = otherScales.copy()
    L0S = otherScales.copy()
    L1S = otherScales.copy()
    L2S = otherScales.copy()
    L3S = otherScales.copy()
    # default position
    U0P =  otherPos.copy()  
    U1P =  otherPos.copy() 
    U2P =  otherPos.copy()  
    U3P =  otherPos.copy() 
    L0P =  otherPos.copy() 
    L1P =  otherPos.copy() 
    L2P =  otherPos.copy() 
    L3P =  otherPos.copy() 

    # setting correct scales
    U0S[1] = legs[0][0]
    U1S[1] = legs[1][0]
    U2S[1] = legs[2][0]
    U3S[1] = legs[3][0]
    L0S[1] = legs[0][2]
    L1S[1] = legs[1][2]
    L2S[1] = legs[2][2]
    L3S[1] = legs[3][2]

    #setting correct positions
    U0P[2] =legs[0][1]
    U1P[0] =legs[1][1]
    U2P[2] =legs[2][1]
    U3P[0] =legs[3][1]
    L0P[2] =legs[0][3]
    L1P[0] =legs[1][3]
    L2P[2] =legs[2][3]
    L3P[0] =legs[3][3]

    finalList = U0P+ U1P+ U2P+ U3P+  U0S+ U1S+ U2S+ U3S+    L0P+ L1P+ L2P+ L3P+  L0S+ L1S+ L2S+ L3S 

    assert (len(finalList)==48)

    return ','.join([str(elem) for elem in finalList]) # list to string with elements



if __name__ == "__main__":
    ######## REMEMBER!! scale is not equal to lenght. The scale-y is only half the actual length (because of the legshape)

    legLengths=[1]*8
    #rand=True
    #if rand:
    #    for i in range(len(legLengths)):
    #        legLengths[i]=random.uniform(0.2,3)
    legLengths[0]=1 #leg0Upper
    legLengths[1]=1 #leg0Lower 
    legLengths[2]=1 #leg3Upper
    legLengths[3]=1 #leg3Lower
    #
    legLengths[4]=1 #leg1Upper
    legLengths[5]=1 #leg1Lower 
    legLengths[6]=1 #leg2Upper
    legLengths[7]=1 #leg2Lower


    print(legLengths)
    legs = positions(legLengths)
    legsString = positionsToString(legs)

    # legs = [leg0, leg1, leg2, leg3]
    # leg0/2 = [Upper ScaleY, Upper PositionZ, lower scaleY, Lower positionZ]
    # leg1/3 = [Upper ScaleY, Upper PositionX, lower scaleY, lower positionX]

    legsReset = []
    legsReset.append([0.5,-1,1,-2.5])

    # leg0 and 2: positionZ
    # leg1 and 3: positionX


    print("legs0:",legs[0])
    print("legs1:",legs[1])
    print("legs2:",legs[2])
    print("legs3:",legs[3])

    resetStr = "0,0,-1.0,-1.0,0,0,0,0,1.0,1,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0,0,-2.5,-2.5,0,0,0,0,2.5,2.5,0,0,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3";        

    #str = "0,0,-1.0,-1.0,0,0,0,0,1.0,1.0,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0,0,-2.5,-2.5,0,0,0,0,2.5,2.5,0,0,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3"

    print("should be:",resetStr)
    print("and is:   ",legsString)

    assert (resetStr==legsString)