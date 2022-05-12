import random
import matplotlib.pyplot as plt
import numpy as np
import sys

from morphologyTransform import positions, positionsToString, positionsToString2

class WaveIndividual:
    def __init__(self,input):
        self.evolvCnt = input[0]
        self.evolvMorph = input[1]
        self.nrOfCntParams = input[2]
        self.nrOfMorParams = input[3]
        
        self.stability1 =0
        self.stability2 =0
        self.nrOfJoints = 12#nrOfJoints  
        self.evalDone = 0
   
        if self.nrOfCntParams!=0 and self.nrOfCntParams!=15 and self.nrOfCntParams!=18 and self.nrOfCntParams!=24:
            raise ValueError("Wave control is not implemented for " +str(self.nrOfCntParams)+" control parameters")
        
        if self.nrOfMorParams!=0 and self.nrOfMorParams!=4 and self.nrOfMorParams!=6:
            raise ValueError("Wave control is not implemented for " +str(self.nrOfMorParams)+" morphology parameters")
        
        self.controlParams = [None]*self.nrOfCntParams
        self.morphologyParams = [None]*self.nrOfMorParams

        if self.evolvCnt:
            #self.controlParams=[-0.931219088010147, 0.4319570538702997, 0.3460881012007009, 0.03952891923100532, 0.8365506857535063, -0.5681241640865371, -0.9282822861543707, 0.9883025949949993, -0.8404521480458047, 0.7180659110131584, -0.04204748607360953, 0.20256718767593362, 0.6151898908675559, -0.401612836443928, -0.6635480066931323, 0.5303914202378959, 0.8586391102628492, -0.8774982539999847]
            for i in range(self.nrOfCntParams):
                self.controlParams[i]= random.uniform(-1, 1)
        if self.evolvMorph:
            for i in range(self.nrOfMorParams):
                self.morphologyParams[i]= random.uniform(-1, 1)

        #try: #if we have pretrained morphologies to load
        #    self.morphologyParams=config["PRETRAINED_MORPHOLOGIES"][config["MORPHOLOGI_NUMBER"]]
        #except KeyError:
        #    pass

    def morphologyString(self,config):
        # scale legs between 0.5 and 3

        morphologyParams=None
        if config["MIRROR_MORPH"]:
            if self.nrOfMorParams!=4 and self.nrOfMorParams!=6:
                sys.exit("Mirror mode on morphology is not implemented for "+str(config["NUM_MORPHOLOGY_PARAMS"])+" params")
            morphologyParams = self.morphologyParams[:4]*2

        else:
            if self.nrOfMorParams!=8:
                sys.exit("Non-mirror mode on morphology is not implemented for "+str(config["NUM_MORPHOLOGY_PARAMS"])+" params")
            morphologyParams=self.morphologyParams        

        min=-1
        max=1
        newMin=config["MIN_LEG_LENGTH"]
        newMax=config["MAX_LEG_LENGTH"]
        m=newMax-newMin
        scaledMorphologyParams = [(float(i)-min)/(max-min)*m+newMin for i in morphologyParams[:8]]

        

        legs = positions(scaledMorphologyParams)
        
        
        if self.nrOfMorParams==6:
            morphologyParams.append(self.morphologyParams[4])
            morphologyParams.append(self.morphologyParams[5])
        
            newMin=config["MIN_LEG_TRANS"]
            newMax=config["MAX_LEG_TRANS"]
            m=newMax-newMin
            scaledMorphologyParamsTrans = [(float(i)-min)/(max-min)*m+newMin for i in morphologyParams[8:]]
            return positionsToString2(legs, scaledMorphologyParamsTrans)


        else:        
            return positionsToString(legs)#, scaledMorphologyParamsTrans)

    def crossover(self,partner, crossoverProb, recombControl=True, recombMorphology=False):
        # preforme crossover between self and partner
        # todo: need to investigate better crossover solution
        
        #if recombControl and not recombMorphology:
        
        
        if recombControl:
            gene1 =self.controlParams
            #gene2 = partner.controller.controlParams
            gene2 = partner.controlParams
            for i in range(self.nrOfCntParams):
                if random.random()<crossoverProb:
                    # switch value at index i
                    temp = gene1[i]
                    gene1[i]=gene2[i]
                    gene2[i]=temp

        if recombMorphology:
            gene1 =self.morphologyParams
            #gene2 = partner.controller.controlParams
            gene2 = partner.morphologyParams
            for i in range(self.nrOfMorParams):
                if random.random()<crossoverProb:
                    # switch value at index i
                    temp = gene1[i]
                    gene1[i]=gene2[i]
                    gene2[i]=temp

        #elif not recombControl and recombMorphology:
        #    sys.exit("Morphology crossover is not implemented")
        #elif recombControl and recombMorphology:
        #    sys.exit("Morphology crossover is not implemented")
        #else:
        #    sys.exit("Invalid recomb option")

    

    def mutate(self, type, mutation_rate, mutation_sigma, randomInitProb, mutateControl, mutateMorphology):
        
        # call the standard mutation
        if type=="gaussian":
            self.gaussianMutation(mutation_rate, mutation_sigma, mutateControl, mutateMorphology)
        if type=="gaussianAndRandomInit":
            self.gaussianMutation(mutation_rate, mutation_sigma, mutateControl, mutateMorphology)
            self.randomInitial(randomInitProb, mutateControl, mutateMorphology)
        # self.randomInitial() # - replaces one element with a new one
        # anotherMutation(mutation_rate, mutation_sigma)

    def gaussianMutation(self, mutation_rate, mutation_sigma, mutateContol, mutateMorphology):
        #if mutateContol and not mutateMorphology:
        if mutateContol:
            for i in range(self.nrOfCntParams):
                if random.random()<mutation_rate:
                    self.controlParams[i] += random.gauss(0,mutation_sigma)
                    
                    if self.controlParams[i]>1:
                        self.controlParams[i]=1
                    elif self.controlParams[i]<-1:
                        self.controlParams[i]=-1

        if mutateMorphology:
            for i in range(self.nrOfMorParams):
                if random.random()<mutation_rate:
                    self.morphologyParams[i] += random.gauss(0,mutation_sigma)
                    
                    if self.morphologyParams[i]>1:
                        self.morphologyParams[i]=1
                    elif self.morphologyParams[i]<-1:
                        self.morphologyParams[i]=-1

        #elif not mutateContol and mutateMorphology:
        #    sys.exit("Mutation for morphology is not implemented")
        #elif mutateContol and mutateMorphology:
        #    sys.exit("Mutation for morphology is not implemented")
        #else:
        #    sys.exit("Invalid mutation options")

    def randomInitial(self, randomInitProb, mutateContol, mutateMorphology):
        if mutateContol and not mutateMorphology:
            for i in range(self.nrOfCntParams):
                if random.random()<randomInitProb:
                    self.controlParams[i]=random.uniform(-1, 1)
                    
        elif not mutateContol and mutateMorphology:
            for i in range(self.nrOfMorParams):
                if random.random()<randomInitProb:
                    self.morphologyParams[i]=random.uniform(-1, 1)

        elif mutateContol and mutateMorphology:
            for i in range(self.nrOfCntParams):
                if random.random()<randomInitProb:
                    self.controlParams[i]=random.uniform(-1, 1)
            for i in range(self.nrOfMorParams):
                if random.random()<randomInitProb:
                    self.morphologyParams[i]=random.uniform(-1, 1)
        else:
            sys.exit("Invalid mutation options")

    def createAction(self,t):
        # t = timestep
        # Create joint angle from genotype parameters
        # controlParams size = 15
        #self.nrOfActionParams = self.nrOfJoints
        action = [None]*self.nrOfJoints

        
        if self.nrOfCntParams==15:
            params = self.controlVersion15()
        elif self.nrOfCntParams==18:
            params = self.controlVersion18()
        elif self.nrOfCntParams==24:
            params = self.controlVersion24()
        else:
            sys.exit("No control version implemented for "+str(self.nrOfCntParams)+" control parameters")

        for i in range(self.nrOfJoints):
            action[i]=minMaxPhase(t, params[i][0], params[i][1], params[i][2])    

        return action
    
    def controlVersion24(self):
        params=[] # Mirror, noe one is in phase
                # (view in walking direction)
            # leg0 upper. Back right 
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[12]/2])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[13]/2])
        # leg1 upper. Back left (same as back right, but with phase shift)
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[14]/2+0.5])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[15]/2+0.5])
        # leg2 upper. Front left
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[16]/2])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[17]/2])
        # leg3 upper. Front right (same as front left, but with phase shift)
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[18]/2+0.5])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[19]/2+0.5])

        #leg0-4 lower
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[20]/2])
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[21]/2+0.5])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[22]/2])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[23]/2+0.5])
        return params

    def controlVersion18(self):
        # 18 parameters. Mirror, but: leg0 and 2 are in phase. Leg1 and 3 are in phase. These phases are not opposit of each other
        params=[]
        # leg0 upper. Back right 
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[12]/2])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[13]/2])
        # leg1 upper. Back left (same as back right, but with phase shift)
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[14]/2])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[15]/2])
        # leg2 upper. Front left
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[12]/2])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[13]/2])
        # leg3 upper. Front right (same as front left, but with phase shift)
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[14]/2])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[15]/2])

        #leg0-4 lower
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[16]/2])
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[17]/2])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[16]/2])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[17]/2])
        return params

    def controlVersion15(self):
        # 15 parameters. Mirror, but: leg0 and 2 are in phase. Leg1 and 3 are in phase. These phases are opposit of each other
        params=[]
        # leg0 upper. Back right 
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[12]/2])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[13]/2])
        # leg1 upper. Back left (same as back right, but with phase shift)
        params.append([self.controlParams[0], self.controlParams[1], self.controlParams[12]/2+0.5])
        params.append([self.controlParams[2], self.controlParams[3], self.controlParams[13]/2+0.5])
        # leg2 upper. Front left
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[12]/2])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[13]/2])
        # leg3 upper. Front right (same as front left, but with phase shift)
        params.append([self.controlParams[6],  self.controlParams[7],  self.controlParams[12]/2+0.5])
        params.append([self.controlParams[8],  self.controlParams[9],  self.controlParams[13]/2+0.5])

        #leg0-4 lower
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[14]/2])
        params.append([self.controlParams[4], self.controlParams[5], self.controlParams[14]/2+0.5])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[14]/2])
        params.append([self.controlParams[10], self.controlParams[11], self.controlParams[14]/2+0.5])
        return params


def minMaxPhase(t,v,w,ps,p=2*np.pi):
    # controlsystem
    # t - timestep, v and w - used to find amplitude and vertical phase,
    # ps - phase shift,  periode = 2pi/p. (p=2*pi->periode=1)
    a = (v-w)/2 # amplitude
    b = (v+w)/2 # verticalPhase
    return a*np.tanh(4*np.sin(p*(t+ps)))+b    
# Tønnes brukte 4 her^, men why?

def sin(t,a,ps,b,p=2*np.pi):
    # for refrence plot
    #  periode = 2pi/p
    return a*np.sin(p*(t+ps))+b

def koos(t,a,b):
    # for refrence plot
    return a * np.tanh(4*np.sin(2*np.pi*(t+b)))

if __name__ == "__main__":

    """
    # test crossover
    c1 = WaveIndividual(12)
    c2 = WaveIndividual(12)
    print(c1.controlParams)
    print(c2.controlParams)
    print("cross")
    c1.crossover(c2)

    print(c1.controlParams)
    print(c2.controlParams)
    """

    

    """   # test mutation:
    for i in range(10):
        control = WaveIndividual(12)
        #print(control.controlParams)

        b = control.controlParams.copy()
        mutation_rate = 0.2
        mutation_sigma = 0.1
        control.gaussianMutation(mutation_rate, mutation_sigma)
        a = control.controlParams
        if a!=b:
            print(i)
            print(b)
            print(a)
            print([abs(a_i - b_i) for a_i, b_i in zip(a, b)])

        else:
            print("no mutation",i)
    """

    random.seed(12345)
    # tests control
    input = [True, False, 18, 6]
    control = WaveIndividual(input)

    resolution = 50
    t = np.linspace(0,3,resolution*4)
    
    
    control.controlParams[0]=-0.1
    control.controlParams[1]=-0.7
    control.controlParams[12]=0.6

    action = control.createAction(t)
    print(type(t),type(action[0]), type(action))
    a = action[0]

    plt.plot(t, koos(t, a=0.6, b=0.4))
    plt.plot(t, action[0],label='leg0UpperX')
    plt.plot(t,sin(t,1,0,0),label="sin")

    #plt.plot(t, action[1],label='leg0UpperY')
    #plt.plot(t, action[2],label='leg0Lower')

    #plt.plot(t, action[3],label='leg1UpperX')
    #plt.plot(t, action[4],label='leg1UpperY')
    #plt.plot(t, action[5],label='leg1Lower')
    
    #plt.plot(t, action[0+6],label='leg2UpperX')
    #plt.plot(t, action[1+6],label='leg2UpperY')
    #plt.plot(t, action[2+6],label='leg2Lower')

    #plt.plot(t, action[3+6],label='leg3UpperX')
    #plt.plot(t, action[4+6],label='leg3UpperY')
    #plt.plot(t, action[5+6],label='leg3Lower')
    #plt.legend()
    
    #print(action[0])
    plt.show()
    

