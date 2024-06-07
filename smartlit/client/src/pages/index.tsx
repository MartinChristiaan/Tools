
import { Card, Box, Heading, Form } from "@chakra-ui/react";

import { useEffect, useState } from "react";
import { flask_url } from "../lib/utils";
import { render_selectbox } from "../lib/selectbox";
import Control from "@/components/control";
import TemporalPlot from "@/components/plot";





export default function Home() {
  const [containers, setContainers] = useState(null);
  const [setUpdateCnt, updateCnt] = useState(0);
  const [plotState,setPlotState] = useState([0,0])

  useEffect(() => {
    fetch(flask_url+'/get_cards')
      .then(response => response.json())
      .then(data => setContainers(data));
  }, []);

  function renderContainer(key,containertype){
    switch (containertype){
      case "card":
        return <Control key={key} setUpdateCnt={setUpdateCnt} updateCnt={updateCnt}></Control>
      case "plot":
        return <TemporalPlot plotState={plotState} setPlotState={setPlotState} updateCnt={updateCnt}></TemporalPlot>
      default:
        return null
    }
  }

  return (
    <div>
      {containers &&
        Object.entries(containers).map(([outerKey, innerData]) =>
          renderContainer(outerKey, innerData)
        )}
    </div>
  );
}

