import numpy as np
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import (
    ActionTuple
)

DELTA_TIME = 0.2
AMPLITUDE = 2
N_EVALUATIONS = 5
MAX_N_STEPS_PER_EVALUATION = 10000
DOF=20

Path= "C:\\Users\\stein\\Documents\\Unity2\\builds\\Crawler"

def k(t,a,phi,b,per):
    return a*np.tanh(4*np.sin(per*(t+phi)))+b

def control(DOF, timestep, t, a ,phi, b, per):
    #action = np.random.rand(1,DOF)
    action = np.zeros((1,DOF))

    # leggs. In x-direction
    for i in range(0,8,4):    
        action[0,i] =k(timestep[t],a,phi,b, per) #timestep[t]
    for i in range(2,8,4):    
        action[0,i] =k(timestep[t],a,phi,b, per) #timestep[t]

    # forlegg
    for i in range(8,12,2):    
        action[0,i] = k(timestep[t],a,phi,b, per) #timestep[t]
    for i in range(9,12,2):    
        action[0,i] = k(timestep[t],a,phi,b, per) #timestep[t]

    # strength
    for i in range(12,len(action[0])):
        # what is a reasonable strength?
        action[0,i] = 1#-0.90
    
    return action


def evaluate(env):
    env.reset()
    individual_name = list(env._env_specs)[0]
    fitness = 0

    res = 80
    #timestep = np.concatenate([np.linspace(-1,1,res//2), np.linspace(1,-1,res//2)])
    
    
    timestep = np.linspace(-2,2,res)

    # the function, which is y = x^2 here
    per=2*np.pi #periode
    a=1 # amplitude
    phi=0.25 # phase
    b=0.5  # offset

    t=0
    for j in range(MAX_N_STEPS_PER_EVALUATION):
        if t==res-1:
            t=0
        else:
            t+=1

        obs,other = env.get_steps(individual_name)
        if (len(obs.agent_id)>0):
            

            #print(obs.agent_id)
            
            
            # Numbers in action will be limited to [-1,1]
            # 4 -->1 and -454 --> -1. 
            action = control(DOF, timestep, t, a, phi, b, per)

            env.set_action_for_agent(individual_name,obs.agent_id,ActionTuple(action))
            env.step()

            fitness += obs.obs[0][0][0]
    return fitness


if __name__ == "__main__":
    # Load the unity environment
    env = UnityEnvironment(file_name=Path, seed = 1, side_channels = [], no_graphics=False)
    # Reset the environment
    env.reset()
    print(list(env._env_specs))
    individual_name = list(env._env_specs)[0]
    behavior_keys = env.behavior_specs.keys()
    # warmup rounds # I do this since the first evaluations sometimes have 
    for i in range(2):
        print(f"(warmup) fitness was {evaluate(env)}")

    for i in range(N_EVALUATIONS):
        print(f"fitness was {evaluate(env)}")
   