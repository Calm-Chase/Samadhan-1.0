import streamlit as st
import replicate
import os
from typing import Dict, List, Optional, Generator
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration settings for LLM models"""
    temperature: float = 0.1
    top_p: float = 0.9
    max_length: int = 512
    repetition_penalty: float = 1.0

class StreamlitLLMChat:
    """
    A class to handle Streamlit-based LLM chat interface with Replicate API integration
    """
    
    # Model ID mappings
    LLAMA_MODELS = {
        'Llama2-7B': 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea',
        'Llama2-13B': 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
        'Llama2-70B': 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    }

    def __init__(self):
        """Initialize the chat application with default settings"""
        self.setup_page_config()
        self.initialize_session_state()
        
    def setup_page_config(self) -> None:
        """Configure the Streamlit page settings"""
        st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")
        
    def initialize_session_state(self) -> None:
        """Initialize or reset the session state for chat history"""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "How may I assist you today?"}
            ]

    def setup_sidebar(self) -> tuple:
        """
        Set up the sidebar with API input and model configurations
        
        Returns:
            tuple: (api_key, selected_model, config)
        """
        with st.sidebar:
            st.title('🦙💬 Llama 2 Chatbot')
            
            # API Token Input
            api_key = st.text_input('Enter Replicate API token:', type='password')
            self._validate_api_key(api_key)
            
            # Model Selection and Parameters
            st.subheader('Models and parameters')
            selected_model = st.selectbox(
                'Choose a Llama2 model',
                list(self.LLAMA_MODELS.keys()),
                key='selected_model'
            )
            
            # Configuration Parameters
            config = LLMConfig(
                temperature=st.slider('temperature', 0.01, 5.0, 0.1, 0.01),
                top_p=st.slider('top_p', 0.01, 1.0, 0.9, 0.01),
                max_length=st.slider('max_length', 64, 4096, 512, 8)
            )
            
            # Clear Chat Button
            st.button('Clear Chat History', on_click=self.clear_chat_history)
            
            # Documentation Link
            st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')
            
        return api_key, selected_model, config

    def _validate_api_key(self, api_key: str) -> None:
        """
        Validate the provided API key format
        
        Args:
            api_key (str): The API key to validate
        """
        if not (api_key.startswith('r8_') and len(api_key) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    def clear_chat_history(self) -> None:
        """Reset the chat history to initial state"""
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]

    def generate_llama2_response(self, prompt_input: str, model_id: str, config: LLMConfig) -> Generator:
        """
        Generate response using the LLaMA model
        
        Args:
            prompt_input (str): User's input prompt
            model_id (str): The ID of the selected model
            config (LLMConfig): Configuration parameters for the model
            
        Returns:
            Generator: Stream of response tokens
        """
        string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\n\n"
        
        # Build conversation history
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            string_dialogue += f"{role.capitalize()}: {content}\n\n"
        
        return replicate.run(
            model_id,
            input={
                "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                "temperature": config.temperature,
                "top_p": config.top_p,
                "max_length": config.max_length,
                "repetition_penalty": config.repetition_penalty
            }
        )

    def display_chat_messages(self) -> None:
        """Display all messages in the chat history"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def run(self) -> None:
        """Main method to run the chat application"""
        # Setup sidebar and get configurations
        api_key, selected_model, config = self.setup_sidebar()
        
        # Set API token
        if api_key:
            os.environ['REPLICATE_API_TOKEN'] = api_key
        
        # Display chat history
        self.display_chat_messages()
        
        # Handle user input
        if prompt := st.chat_input(disabled=not api_key):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate and display assistant response
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = self.generate_llama2_response(
                            prompt,
                            self.LLAMA_MODELS[selected_model],
                            config
                        )
                        placeholder = st.empty()
                        full_response = ''
                        for item in response:
                            full_response += item
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

# Main execution
if __name__ == "__main__":
    chat_app = StreamlitLLMChat()
    chat_app.run()