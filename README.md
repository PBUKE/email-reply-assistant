# Email Reply Assistant 📧

A professional email reply generation system that uses AI to create polite and helpful responses. The system includes a web interface, quality metrics, and business-appropriate formatting.

## 🌟 Features

- **Smart Reply Generation**: Uses GPT-3.5-turbo for generating contextual responses
- **Quality Metrics**: Real-time scoring for politeness and helpfulness
- **Professional Formatting**: Ensures business-appropriate email structure
- **Interactive UI**: User-friendly web interface with example templates
- **Response Analysis**: Visual metrics and quality indicators

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/email-reply-assistant.git
cd email-reply-assistant
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure OpenAI API**
- Create a `.env` file in the project root
- Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

## 💻 Project Structure

```
email-reply-assistant/
├── app.py              # Streamlit web interface
├── model.py            # Email generation model
├── reward.py          # Response quality scoring
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (create this)
└── README.md          # Project documentation
```

## 🛠️ Technologies Used

- **Python 3.8+**
- **OpenAI GPT-3.5-turbo**: For generating responses
- **Streamlit**: Web interface
- **Plotly**: Visualization
- **NLTK**: Text processing
- **PyTorch & Transformers**: Model handling

## 📊 Features in Detail

### Email Generation
- Context-aware responses
- Professional formatting
- Business-appropriate language
- Error handling and fallbacks

### Quality Metrics
- Politeness scoring
- Helpfulness evaluation
- Business appropriateness
- Response clarity

### User Interface
- Real-time generation
- Interactive examples
- Visual metrics
- Response analysis

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

### Custom Settings
Adjust model parameters in `model.py`:
- Temperature
- Response length
- Formatting options
- Business rules

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo
- Streamlit for the amazing web framework
- The open-source community for various tools and libraries

## 📫 Contact

Your Name - pinarbbuke@gmail.com
Project Link: [https://github.com/PBUKE/email-reply-assistant]
