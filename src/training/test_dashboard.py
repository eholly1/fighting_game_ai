"""
Simple test dashboard to debug Streamlit issues
"""
import streamlit as st

def main():
    st.title("🥊 Test Dashboard")
    st.write("If you can see this, Streamlit is working!")
    
    st.header("Basic Test")
    st.write("This is a simple test to verify Streamlit functionality.")
    
    # Test basic widgets
    name = st.text_input("Enter your name:")
    if name:
        st.write(f"Hello, {name}!")
    
    # Test button
    if st.button("Click me!"):
        st.success("Button clicked successfully!")
    
    # Test chart
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    
    st.line_chart(chart_data)

if __name__ == "__main__":
    main()
