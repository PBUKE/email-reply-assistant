from model import EmailReplyModel
from reward import RewardFunction
import time

def format_scores(scores):
    """Format the reward scores for display."""
    return (
        f"\nScores:\n"
        f"- Total Score: {scores['total_score']:.2f}\n"
        f"- Politeness: {scores['politeness_score']:.2f}\n"
        f"- Helpfulness: {scores['helpfulness_score']:.2f}\n"
    )

def main():
    print("Initializing Email Reply Assistant...")
    model = EmailReplyModel()
    reward_function = RewardFunction()
    
    print("\nEmail Reply Assistant is ready!")
    print("Enter your email text below (type 'quit' to exit):")
    print("-" * 50)
    
    while True:
        email_text = input("\nYour email: ").strip()
        
        if email_text.lower() == 'quit':
            break
        
        if not email_text:
            print("Please enter some text!")
            continue
        
        print("\nGenerating reply...")
        start_time = time.time()
        
        # Generate reply
        reply = model.generate_reply(email_text)
        
        # Calculate scores
        scores = reward_function.calculate_total_score(reply)
        
        # Display results
        print(f"\nGenerated Reply ({time.time() - start_time:.2f}s):")
        print("-" * 50)
        print(reply)
        print("-" * 50)
        print(format_scores(scores))

if __name__ == "__main__":
    main() 