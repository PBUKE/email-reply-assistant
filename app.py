import streamlit as st
import plotly.graph_objects as go
from model import EmailReplyModel
from reward import RewardFunction
import time
import os

# Page configuration
st.set_page_config(
    page_title="Professional Email Assistant",
    page_icon="✉️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stTextArea textarea {
        height: 200px;
    }
    .main {
        padding: 2rem;
    }
    .css-1v0mbdj.ebxwdo61 {
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .response-box {
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the model and reward function (cached)"""
    model = EmailReplyModel()
    reward_function = RewardFunction()
    return model, reward_function

def create_score_gauge(score, title):
    """Create a gauge chart for displaying scores"""
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 33], 'color': "lightgray"},
                {'range': [33, 66], 'color': "gray"},
                {'range': [66, 100], 'color': "lightblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))

def main():
    st.title("✉️ Professional Email Assistant")
    st.markdown("""
    Generate polite and professional email replies using AI. The assistant will evaluate the
    response based on business appropriateness, politeness, and helpfulness metrics.
    """)
    
    # Initialize model and reward function
    model, reward_function = load_model()
    
    # Create two columns for input and output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Email")
        email_text = st.text_area(
            "Enter the email you want to reply to:",
            height=200,
            placeholder="e.g., Could you help me schedule a meeting with the team?"
        )
        
        generate_button = st.button("🚀 Generate Professional Reply", type="primary")
        
        # Add example emails
        st.markdown("### 📋 Example Professional Emails")
        examples = {
            "Meeting Request": "I would like to schedule a team meeting to discuss the Q2 project timeline. What times work best for you next week?",
            "Project Update": "Could you provide an update on the status of the marketing campaign deliverables? We need to report progress to stakeholders.",
            "Document Review": "Please review the attached proposal document and provide your feedback by Friday. This is crucial for the client presentation.",
        }
        
        for title, example in examples.items():
            if st.button(title):
                st.session_state.email_text = example
                email_text = example
    
    with col2:
        st.subheader("💌 Generated Reply")
        if generate_button and email_text:
            with st.spinner("Generating professional reply..."):
                start_time = time.time()
                reply = model.generate_reply(email_text)
                scores = reward_function.calculate_total_score(reply)
                generation_time = time.time() - start_time
                
                st.markdown("#### Response:")
                st.markdown('<div class="response-box">' + reply.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
                
                st.markdown("#### 📊 Quality Metrics")
                
                # Create three columns for the metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    fig1 = create_score_gauge(scores['total_score'], 'Overall Score')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with metric_col2:
                    fig2 = create_score_gauge(scores['politeness_score'], 'Professionalism')
                    st.plotly_chart(fig2, use_container_width=True)
                
                with metric_col3:
                    fig3 = create_score_gauge(scores['helpfulness_score'], 'Clarity')
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Additional response details
                st.markdown("#### ✨ Response Details")
                st.markdown(f"""
                - ⚡ Generation time: {generation_time:.2f} seconds
                - 📝 Response length: {len(reply.split())} words
                - 🎯 Topic identified: {model.extract_topic(email_text)}
                """)
        else:
            st.info("Enter a professional email on the left and click 'Generate Professional Reply' to get started!")
    
    # Add footer with business writing tips
    st.markdown("---")
    st.markdown("""
    ### 💡 Professional Email Writing Tips
    1. **Be Clear and Concise**
       - Get to the point quickly
       - Use simple, professional language
    
    2. **Maintain Proper Structure**
       - Start with a clear greeting
       - Organize content in paragraphs
       - End with an appropriate signature
    
    3. **Stay Professional**
       - Use appropriate business tone
       - Proofread before sending
       - Include necessary context
    """)

if __name__ == "__main__":
    main() 