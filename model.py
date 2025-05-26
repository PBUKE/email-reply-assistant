import os
from openai import OpenAI
import re
from dotenv import load_dotenv

class EmailReplyModel:
    def __init__(self):
        """Initialize the email reply model using OpenAI's GPT-3.5-turbo."""
        load_dotenv()  # Load environment variables from .env file
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Define email components
        self.greetings = [
            "Dear {recipient},",
            "Hello {recipient},",
            "Hi {recipient},"
        ]
        
        self.closings = [
            "Best regards,",
            "Kind regards,",
            "Sincerely,",
            "Thank you,",
            "Best,"
        ]

    def clean_text(self, text):
        """Clean and validate the input text."""
        if not text:
            return ""
        
        # Remove any obviously problematic patterns
        text = re.sub(r'\b(\w+)(\s+\1\s*)+', r'\1', text)  # Remove word repetitions
        text = re.sub(r'[^\w\s.,!?;:()\'-@]', '', text)  # Remove unusual characters
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text.strip()

    def extract_recipient(self, email_text):
        """Extract recipient name from email or use default."""
        # Try to find a name at the start of the email
        lines = email_text.split('\n')
        first_line = lines[0].strip()
        
        # Check if first line contains a name
        if ':' in first_line:
            name = first_line.split(':')[0].strip()
            if len(name.split()) <= 3:  # Reasonable name length
                return name
        
        return "valued colleague"

    def generate_reply(self, email_text):
        """Generate a reply using OpenAI's GPT-3.5-turbo."""
        # Clean input
        email_text = self.clean_text(email_text)
        
        if not email_text:
            return "I apologize, but I received an empty message. Could you please provide more details?"
        
        try:
            # Create the prompt for GPT-3.5-turbo
            prompt = f"""You are a professional business email assistant. Generate a polite and helpful reply to the following email.
            Follow these guidelines:
            1. Be professional and courteous
            2. Address the specific points in the email
            3. Keep the response clear and concise
            4. Use appropriate business language
            5. If the input is unclear or nonsensical, respond professionally asking for clarification
            6. Always maintain a helpful and professional tone

            Original Email:
            {email_text}

            Write a professional business email reply that appropriately addresses this message.
            """

            # Generate response using GPT-3.5-turbo
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional business email assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )

            # Extract the generated reply
            reply = response.choices[0].message.content.strip()

            # Ensure proper formatting
            if not any(reply.startswith(greeting.split(',')[0]) for greeting in self.greetings):
                recipient = self.extract_recipient(email_text)
                reply = f"Dear {recipient},\n\n{reply}"

            if not any(closing in reply for closing in self.closings):
                reply += "\n\nBest regards,"

            return reply

        except Exception as e:
            print(f"Error generating reply: {str(e)}")
            recipient = self.extract_recipient(email_text)
            return f"""Dear {recipient},

I apologize, but I need some clarification to better assist you. Could you please provide more details or rephrase your message?

Best regards,
Assistant"""

    def save_model(self, path):
        """Placeholder for model saving - not needed for API-based implementation."""
        pass 