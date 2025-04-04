import os
from typing import Any
import streamlit.components.v1 as components
from streamlit.runtime.state.common import WidgetCallback


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "build")
_component_func_path = components.declare_component(
    "streamlit_javascript", path=build_dir
)

_component_func_url = components.declare_component(
    "streamlit_javascript_url",
    # Pass `url` here to tell Streamlit that the component will be served
    # by the local dev server that you run via `npm run start`.
    url="http://localhost:3003",
)


def st_javascript(
    js_code: str,
    default: Any = 0,
    key: str | None = None,
    poll: int = 0,
    on_change: WidgetCallback | None = None,
    _use_url=False,
) -> Any:
    """Create a new instance of "st_javascript".

    Parameters
    ----------
    js_code: str
        The javascript expression that is to be evaluated on the client side.
        It can be synchronous or asynchronous.
    default: any or None
        The default return value for the component. This is returned when
        the component's frontend hasn't yet specified a value with
        `setComponentValue`.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    poll: int
        If greater than 0, the number of milliseconds to pause between repeatedly
        checking the value of the javascript expression, and calling
        `setComponentValue` for each change
    on_change: callback function with no arguments returning None
        Will be called each time the expression evaluation changes, best used
        in combination with poll, and key so you can access the updated value with
        st.session_state[key]


    Returns
    -------
    obj
        The result of the executed javascript expression
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    if _use_url:
        _component_func = _component_func_url
    else:
        _component_func = _component_func_path
    component_value = _component_func(
        js_code=js_code,
        default=default,
        key=key,
        poll=poll,
        on_change=on_change,
        height=0,
        width=0,
    )
    # We could modify the value returned from the component if we wanted.
    return component_value
