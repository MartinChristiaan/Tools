
import { Card, Box, Heading, Form } from "@chakra-ui/react";

import { useEffect, useState } from "react";
import { flask_url } from "../lib/utils";
import { render_selectbox } from "../lib/selectbox";
import Control from "@/components/control";

export default function Home() {
  const [containers, setContainers] = useState(null);

  useEffect(() => {
    fetch(flask_url+'/get_cards')
      .then(response => response.json())
      .then(data => setContainers(data));
  }, []);

  function renderContainer(key,containertype){
    switch (containertype){
      case "card":
        return <Control key={key}></Control>
      case "plot":
        return null
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

