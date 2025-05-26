from model import EmailReplyModel
from reward import RewardFunction

def main():
    # Initialize model and reward function
    print("Initializing model and reward function...")
    model = EmailReplyModel()
    reward_function = RewardFunction()
    
    # Example training data (in practice, you'd want a larger dataset)
    training_data = [
        "Could you help me with the project deadline?",
        "I'm having trouble with my computer.",
        "When is the next team meeting?",
        "Can you review my presentation?",
        "I need access to the shared drive."
    ]
    
    print("\nBefore fine-tuning example:")
    example_email = "Could you help me schedule a meeting with the team?"
    initial_reply = model.generate_reply(example_email)
    initial_scores = reward_function.calculate_total_score(initial_reply)
    print(f"Reply: {initial_reply}")
    print(f"Scores: {initial_scores}")
    
    # Fine-tune the model
    print("\nStarting RLHF fine-tuning...")
    model.fine_tune(training_data, reward_function, epochs=3)
    
    print("\nAfter fine-tuning example:")
    final_reply = model.generate_reply(example_email)
    final_scores = reward_function.calculate_total_score(final_reply)
    print(f"Reply: {final_reply}")
    print(f"Scores: {final_scores}")
    
    # Save the fine-tuned model
    model.save_model("fine_tuned_email_model")
    print("\nFine-tuned model saved to 'fine_tuned_email_model' directory")

if __name__ == "__main__":
    main() 