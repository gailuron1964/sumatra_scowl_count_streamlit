from textwrap import dedent
import streamlit.components.v1 as components

def customize_styling():
  """ Disables fancy quote for all st.text_input """
  return components.html(
    dedent("""
      <script>
      const inputs = window.parent.document.querySelectorAll('.stTextInput input');
      inputs.forEach(input => {
        input.setAttribute("spellcheck", "false");
      });
      </script>
    """), 
    height = 0,
    width = 0
  )
