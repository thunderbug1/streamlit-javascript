# *Streamlit javascript execution extension*

[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link] 

## Installation using pypi
Activate your python virtual environment
```sh
pip install streamlit-javascript>=1.42.0
```
## Installation using github source
Activate your python virtual environment
```sh
pip install git+https://github.com/thunderbug1/streamlit-javascript.git@1.42.0
```
## Installation using local source
Activate your python virtual environment
```sh
git clone https://github.com/thunderbug1/streamlit-javascript.git
cd streamlit-javascript
pip install .
```
## Installing tools required for build
You may need to install some packages to build the source
```sh
# APT
sudo apt install python-pip protobuf-compiler libgconf-2-4
# HOMEBREW
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install protobuf graphviz gawk
# YARN v4 - if you set PACKAGE_MGR="yarn" in setup.py
sudo npm uninstall --global yarn
corepack enable || sudo npm install --global corepack && corepack enable
```

## Running a local development environment (hot source update)
Activate your python virtual environment
```sh
git clone https://github.com/thunderbug1/streamlit-javascript.git
cd streamlit-javascript
pip install -e .

# NPM option - if you set PACKAGE_MGR="npm" in setup.py
(cd streamlit_javascript/frontend && npm install -D)
(cd streamlit_javascript/frontend && npm run start)
# YARN alternate - if you set PACKAGE_MGR="yarn" in setup.py
(cd streamlit_javascript/frontend && yarn install --production=false)
(cd streamlit_javascript/frontend && yarn start)
```
### which will run this streamlit site concurrently with the following command
```sh
streamlit run dev.py --browser.serverAddress localhost --browser.gatherUsageStats false
```
This allows hot reloading of both the streamlit python and ReAct typescript

## Debugging python in a local development environment (hot source update)
Activate your python virtual environment
```sh
git clone https://github.com/thunderbug1/streamlit-javascript.git
cd streamlit-javascript
pip install -e .

# NPM option - if you set PACKAGE_MGR="npm" in setup.py
(cd streamlit_javascript/frontend && npm run hottsx)
# YARN alternate - if you set PACKAGE_MGR="yarn" in setup.py
(cd streamlit_javascript/frontend && yarn hottsx)
```
### Now run this in your debugging tool
Remembering to match your python virtual environment in the debugger
```sh
streamlit run dev.py --browser.serverAddress localhost --browser.gatherUsageStats false
```
This sill allows hot reloading of both the streamlit python and ReAct typescript

## Using st_javascript in your code
You can look at dev.py for working examples by getting the github source
### Simple expression
```py
import streamlit as st
from streamlit_javascript import st_javascript

st.subheader("Javascript API call")
return_value = st_javascript("1+1")
st.markdown(f"Return value was: {return_value}")
```
### An in place function (notice the brace positions)
```py
return_value = st_javascript("(function(){ return window.parent.document.body.clientWidth; })()")
```
### An async place function (notice the brace positions)
```py
return_value = st_javascript("""
    (async function(){
    return await fetch("https://reqres.in/api/products/3")
        .then(function(response) {return response.json();});
    })()
""","Waiting for response")
```
### A muplitple setComponentValue
```py
st.markdown("Browser Time: "+st_javascript("today.toUTCString()","...","TODAY",1000))
```
### An on_change muplitple setComponentValue (with a block while we wait for the first return value)
```py
def width_changed() -> None:
    st.toast(st.session_state['WIDTH'])
return_value = st_javascript("window.parent.document.body.clientWidth",None,"WIDTH",1000,width_changed)
if return_value is None:
    st.stop()
```
### You can also this code at the top of your page to hide the code frames
```py
st.markdown("""<style> .stElementContainer:has(IFrame) { display: none;} </style>""", unsafe_allow_html=True)
```

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/thunderbug1/streamlit-javascript

[pypi_badge]: https://badge.fury.io/py/streamlit-javascript.svg
[pypi_link]: https://pypi.org/project/streamlit-javascript/
