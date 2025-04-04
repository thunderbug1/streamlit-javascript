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
    this.state = { result: "", has_run: false }
  }
  async componentDidMount() {
    const js_code = this.props.args["js_code"]
    const poll_rate = this.props.args["poll"]

    if (!this.state.has_run) {
      let prev_result = this.props.args["default"]
      do {
        let result = ""
        try {
          // eslint-disable-next-line
          result = await eval(js_code)
        } catch (e) {
          result = String(e)
        }

        if (result != prev_result) {
          prev_result = result
          this.setState(
            prevState => ({ result: result, has_run: true }),
            () => Streamlit.setComponentValue(this.state.result)
          )
        }
        if (poll_rate)
          await new Promise(r => setTimeout(r, poll_rate));
      } while (poll_rate)
    }
  }

  public render = (): ReactNode => {
    return null
  }

}

export default withStreamlitConnection(JavascriptComponent)