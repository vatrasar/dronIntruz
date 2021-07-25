from tensorforce import Environment, Agent, Runner
#UWAGA. prawdopodobieństwo ataku powinno być ustawione na 100%. W przeciwnym wypadku czasem dron może uciekać na drugi krąg
from MyEnvironment import MyEnvironment

if __name__ == "__main__":


    environment = Environment.create(
        environment=MyEnvironment
    )
    agent = Agent.create(
        agent='ppo', environment=environment, batch_size=64, learning_rate=0.000250, likelihood_ratio_clipping=0.1,
        entropy_regularization=0.01,subsampling_fraction=1.0


    )



    #agent = Agent.load(directory='data/checkpoints')
    runner = Runner(
        agent=agent,
        environment=environment,
        max_episode_timesteps=100
    )
    runner.run(num_episodes=20000,mean_horizon=100)
    # runner.run(num_episodes=100, )
    runner.close()



        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")