from environment import StudentLifeEnv

env = StudentLifeEnv()
state = env.reset()

print("Initial:", state)

for i in range(5):
    state, reward, done, _ = env.step("rest")
    print(f"\nStep {i+1}")
    print("State:", state)
    print("Reward:", reward)