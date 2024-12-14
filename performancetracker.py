import matplotlib.pyplot as plt
import numpy as np

class PerformanceTracker:
    def __init__(self, agent):
        self.agent = agent
        self.episode_rewards = []
        self.episode_wins = []
        self.cumulative_learning_curve = []
    
    def track_episode(self, episode, total_reward, is_win):
        """
        Track performance metrics for each episode
        """
        self.episode_rewards.append(total_reward)
        self.episode_wins.append(1 if is_win else 0)
        
        # Compute cumulative average
        if len(self.episode_rewards) > 0:
            cumulative_avg = np.mean(self.episode_rewards)
            self.cumulative_learning_curve.append(cumulative_avg)
    
    def plot_learning_progress(self):
        """
        Visualize learning progress
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Rewards Plot
        ax1.plot(self.episode_rewards, label='Episode Rewards')
        ax1.set_title('Episode Rewards Over Training')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Total Reward')
        ax1.legend()
        
        # Cumulative Average Plot
        ax2.plot(self.cumulative_learning_curve, label='Cumulative Average Reward', color='green')
        ax2.set_title('Cumulative Average Reward')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Average Reward')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
    
    def save_performance_data(self, filename='performance/performance_data.npz'):
        """
        Save performance metrics
        """
        np.savez(filename, 
                 rewards=self.episode_rewards, 
                 wins=self.episode_wins,
                 cumulative_curve=self.cumulative_learning_curve)
    
    def load_performance_data(self, filename='performance/performance_data.npz'):
        """
        Load previously saved performance data
        """
        data = np.load(filename)
        self.episode_rewards = data['rewards'].tolist()
        self.episode_wins = data['wins'].tolist()
        self.cumulative_learning_curve = data['cumulative_curve'].tolist()