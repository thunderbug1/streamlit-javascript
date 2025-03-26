import os
from typing import Any
import streamlit.components.v1 as components
from streamlit.runtime.state.common import WidgetCallback

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_javascript",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3003",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend","build")
    _component_func = components.declare_component("streamlit_javascript", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_javascript(
    js_code: str,
    default: Any = 0,
    key: str | None = None,
    poll: int = 0,
    on_change: WidgetCallback | None = None,
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


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run streamlit_javascript/__init__.py  --browser.gatherUsageStats false`
if not _RELEASE:
    import streamlit as st

    #return_value = javascript_component('alert("World")')
    #return_value = javascript_component('1+1')
    js_code = """await fetch("https://reqres.in/api/products/3")
    .then(function(response) {return response.json();})"""
    st.subheader("Executing javascript code:")
    st.markdown(f"""```
    {js_code}""")
    return_value = st_javascript(js_code)
    st.markdown(f"Return value was: {return_value}")
    print(f"Return value was: {return_value}")
