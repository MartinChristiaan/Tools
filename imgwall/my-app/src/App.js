import React,{useEffect,useState} from 'react';
import ControlPanel from './components/ControlPanel';
import Columns from './components/Columns'
import api from './communication';

function App() {
  const [tags, setTags] = useState([]);

  // useEffect(() => {
  //   // Fetch initial state from server
  //   api.getTags().then(x => {
  //     setTags(x.data);
  //   });
  // }, []);

  // const handleWeightChange = (index, newWeight) => {
  //   api.updateWeight(index,newWeight).then(x=>setTags(x.data))
  // };


  return (
    <div style={{"background":"black","color":"white"}}>
      <Columns/>

    </div>

  );
}

export default App;
