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
    from LearningAgent import LearningAgent
    from checkers_env import checkers_env
    from PerformanceTracker import PerformanceTracker
    
    env = checkers_env()
    agent = LearningAgent(env=env)
    tracker = PerformanceTracker(agent)
    
    agent.learning(num_episodes=1)
    tracker.plot_learning_progress()
    tracker.save_performance_data()

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