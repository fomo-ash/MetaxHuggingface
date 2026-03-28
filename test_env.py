from environment import StudentLifeEnv

env = StudentLifeEnv()
state = env.reset()

for _ in range(10):
    state, reward, done, _ = env.step("study")
    print(state, reward)