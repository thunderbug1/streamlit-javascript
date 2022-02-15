import streamlit as st
from streamlit_javascript import st_javascript

js_code = """await fetch("https://reqres.in/api/products/3")
.then(function(response) {return response.json();})"""

st.subheader("Executing javascript code:")
st.markdown(f"""```
{js_code}""")

return_value = st_javascript(js_code)
st.markdown(f"Return value was: {return_value}")
print(f"Return value was: {return_value}")
