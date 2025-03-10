import React from "react"
import { createRoot } from 'react-dom/client'
import MyComponent from "./JavascriptComponent"

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <MyComponent />
  </React.StrictMode>,
)
