# Streamlit javascript execution

[![GitHub][github_badge]][github_link]

## Installation

```
pip install streamlit-javascript
```

## Getting started

```import streamlit as st
from streamlit_javascript import st_javascript

st.subheader("Javascript API call")

return_value = st_javascript("""await fetch("https://reqres.in/api/products/3").then(function(response) {
    return response.json();
}) """)

st.markdown(f"Return value was: {return_value}")
print(f"Return value was: {return_value}")
```

## Demo

![example image](https://github.com/thunderbug1/streamlit-javascript/raw/main/group_selection_example.gif)

[github_link]: https://github.com/thunderbug1/streamlit-javascript
[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label