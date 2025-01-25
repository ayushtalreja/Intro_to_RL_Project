import sys
import subprocess


def check_dependencies():
    """Check and install required dependencies"""
    required_packages = ['numpy', 'matplotlib']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)


def train_model():
    """Train the reinforcement learning model"""
    from SARSA1
    ent import SARSALearningAgent
    from checkers_env import checkers_env
    from performancetracker import PerformanceTracker
    from modelpersistance import ModelPersistence

    env = checkers_env()
    agent = SARSALearningAgent(env=env)
    tracker = PerformanceTracker(agent)
    persistmodel = ModelPersistence()

    print("Starting training...")
    tracker.start_training()
    num_episodes = 1000

    try:
        for episode in range(num_episodes):
            env.reset()  # Reset the environment
            total_reward = agent.learning(num_episodes=num_episodes)  

            # Determine game outcome
            game_winner = env.game_winner(env.board)
            if game_winner == 1:  # Agent wins
                result = 1
            elif game_winner == -1:  # Opponent wins
                result = -1
            else:  # Draw
                result = 0.5

            # Track episode performance and update results
            is_win = (game_winner == env.player)
            tracker.track_episode(episode, total_reward, is_win)
            tracker.update_results(result)  # Update win/loss/draw counts

            print(f"Tracked Episode {episode + 1}/{num_episodes}: Reward={total_reward}, Win={is_win}")

        tracker.end_training()
        tracker.plot_learning_progress()
        tracker.save_performance_data()
        persistmodel.save_q_table(agent)
    except Exception as e:
        print(f"Training error: {e}")


    except Exception as e:
        print(f"Training error: {e}")


def run_game():
    """Run the Checkers game GUI"""
    from gui import main as run_gui
    run_gui()


def main():
    check_dependencies()

    print("Checkers Reinforcement Learning Project")
    print("1. Train Model")
    print("2. Play Game")

    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        train_model()
    elif choice == '2':
        run_game()
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()