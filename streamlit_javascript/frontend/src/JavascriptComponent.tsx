import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import { ReactNode } from "react"

interface State {
  result: unknown,
  has_run: boolean
}

class JavascriptComponent extends StreamlitComponentBase<State> {
  constructor(props: any) {
    super(props);
    this.state = {result: "", has_run: false}
  }
   async componentDidMount() {
    const js_code = this.props.args["js_code"]

    if(!this.state.has_run)
    {
      let result = "";
      try
      {
        // eslint-disable-next-line
        result = await eval("(async () => {return " + js_code + "})()")
      } catch (e) {
        result = String(e);
        ;
      }

      this.setState(
        prevState => ({ result: result, has_run: true }),
        () => Streamlit.setComponentValue(this.state.result)
      )
    }
 }

  public render = (): ReactNode => {
    return null
  }

}

export default withStreamlitConnection(JavascriptComponent)