import random
import numpy as np
from collections import deque



from tensorforce import Environment, Agent, Runner


from MyEnvironment import MyEnvironment, MyEnvironmentViciousDrone

if __name__ == "__main__":


    environment = Environment.create(
        environment=MyEnvironmentViciousDrone
    )
    agent = Agent.create(
        agent='ppo', environment=environment, batch_size=64, learning_rate=0.000250, likelihood_ratio_clipping=0.1,
        entropy_regularization=0.01,subsampling_fraction=1.0,config=dict(device='GPU'),saver=dict(
            directory='data',
            frequency=100  # save checkpoint every 100 updates
        )


    )
    # agent = Agent.create(
    #     agent='a2c', environment=environment,batch_size=64,memory=128
    #
    #
    # )



    #agent = Agent.load(directory='data/checkpoints')
    runner = Runner(
        agent=agent,
        environment=environment
    )
    runner.run(num_episodes=10000,mean_horizon=10)
    # runner.run(num_episodes=100, )
    runner.close()



        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")