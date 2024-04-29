
import { Card, Box, Heading, Form } from "@chakra-ui/react";

import { useEffect, useState } from "react";
import { flask_url } from "../lib/utils";
import { render_selectbox } from "../lib/selectbox";


export default function Control({key}) {
  const [uiData, setUiData] = useState(null);

  useEffect(() => {
    fetch(flask_url+'/get_ui_data/'+name)
      .then(response => response.json())
      .then(data => setUiData(data));
  }, []);

  function onUpdate(cardKey, innerKey, value) {
    // Make a copy of uiData
    console.log("updating",cardKey,innerKey,value)
    let newUiData = { ...uiData };
    // Update the value in the local state
    newUiData[cardKey][innerKey].value = value;

    // Perform the POST request to update the server
    fetch(flask_url + "/set_ui_data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newUiData),
    })
      .then(response => response.json())
      .then((data) => {
        setUiData(data);
      })
      .catch((error) => {
        console.error("Error updating UI data:", error);
      });
  }


  const renderFormElement = (outerKey,innerkey,data) => {
    console.log(data.uimode)
    switch (data.uimode) {
      case "selectbox":
        return render_selectbox(innerkey, data, onUpdate, outerKey);
      default:
        return null;
    }
  };


  return (
    <Card key={key} my={3}>
      <Box p={4}>
        <Heading as="h2" size="md" mb={4}>
          {key}
        </Heading>
          {Object.entries(uiData).map(([innerKey, innerData]) =>
            renderFormElement(key, innerKey, innerData)
          )}
      </Box>
    </Card>
  );
};

