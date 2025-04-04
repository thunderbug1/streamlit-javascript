from typing import Any
import streamlit as st
from streamlit.runtime.state.common import WidgetCallback

# Replace st_javascript to use the URL version which does hot reload in combination with `pkg_mgr` run start
from streamlit_javascript import st_javascript as st_javascript_noupdate


def st_javascript_hotupdates(
    js_code: str,
    default: Any = 0,
    key: str | None = None,
    poll: int = 0,
    on_change: WidgetCallback | None = None,
) -> Any:
    return st_javascript_noupdate(js_code, default, key, poll, on_change, True)


################################################################################
st.set_page_config("Hot Reload Development", ":hotsprings:", layout="wide")


################################################################################
# This HTML hides the iframe components so they don't use space on the page
st.markdown(
    """
<style>
.stElementContainer:has(IFrame) { display: none; }
.pretty-json-container { background-color: rgb(248, 249, 251); }
</style>
    """,
    unsafe_allow_html=True,
)


################################################################################
st.subheader("Executing browser javascript simple expression:")
js_expr = "1+2+3"
st.code(js_expr, "javascript")
st.markdown(f"Return value was: {st_javascript_hotupdates(js_expr)}")
print(f"Return value was:")


################################################################################
st.subheader("Executing browser javascript async code:")
js_code = """
(async function(){
  return await fetch("https://reqres.in/api/products/3")
    .then(function(response) {return response.json();});
})()
"""
st.code(js_code, "typescript", line_numbers=True)
return_json = st_javascript_hotupdates(js_code, {"waiting for browser": "Async = TRUE"})
st.json(return_json)

################################################################################
st.subheader(
    "Executing browser javascript immediate function, also using on_change and poll=1000:"
)
js_code = "(function(){ return window.parent.document.body.clientWidth; })()"
st.markdown(
    "***This has to be use the path component (normal install) so it can escape from the iframe***"
)
st.markdown(
    "***But only URL:3003 components are hot source updated, so changes to .ts files need a program restart***"
)
st.code(js_code, "javascript")
st.markdown(
    f"ScreenWidth (using port 3003)={st_javascript_hotupdates(js_code,"?","WIDTH_URL")}"
)


def width_change() -> None:
    st.toast(f"width_change() callback={st.session_state['WIDTH_PATH']}")
    print(f"width_change() callback={st.session_state['WIDTH_PATH']}")


st.markdown(
    f"ScreenWidth (using release path)={st_javascript_noupdate(js_code,"?","WIDTH_PATH", 1000, width_change)}"
)
