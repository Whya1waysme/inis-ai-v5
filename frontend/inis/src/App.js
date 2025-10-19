
import './App.css';
import React from "react";

function App() {
  return (
    <div className="App">
      <NewComponent/>
      <NewComponent/>
      <NewComponent/>
      <NewComponent/>
      <NewComponent/>
      <ClassComponent/>

    </div>
  );
}


const NewComponent = () => {
  return (<div>
    Книжный киоск
  </div>)
}

class ClassComponent extends React.Component {
  render() {
    return (<div>44444</div>)
  }
}
export default App;
