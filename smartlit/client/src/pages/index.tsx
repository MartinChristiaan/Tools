
import 'bootstrap/dist/css/bootstrap.min.css';
import { useEffect, useState } from "react";
import { flask_url } from "../lib/utils";
import { Card, Form } from "react-bootstrap";


export default function Home() {
  const [uiData, setUiData] = useState(null);

  useEffect(() => {
    fetch(flask_url+'/get_ui_data')
      .then(response => response.json())
      .then(data => setUiData(data));
  }, []);


  function onUpdate(cardKey, innerKey, value) {
    // Make a copy of uiData
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


  const renderOptions = (options) => {
    if (Array.isArray(options)) {
      return options.map(option => <option key={option}>{option}</option>);
    } else {
      return null;
    }
  };

  const renderFormElement = (outerKey,innerkey, data) => {
    switch (data.uimode) {
      case "selectbox":
        return (
          <Form.Group key={innerkey}>
            <Form.Label>{innerkey}</Form.Label>
            <Form.Control as="select" defaultValue={data.value} onChange={(e) => onUpdate(outerKey,innerkey,e.target.value)}>
              {renderOptions(data.options)}
            </Form.Control>
          </Form.Group>
        );
      default:
        return null;
    }
  };

  const renderCard = (key, innerData) => {
    return (
      <Card key={key} className="my-3">
        <Card.Body>
          <Card.Title>{key}</Card.Title>
          <Form>
            {Object.entries(innerData).map(([innerKey, innerData]) =>
              renderFormElement(key,innerKey, innerData)
            )}
          </Form>
        </Card.Body>
      </Card>
    );
  };

  return (
    <div>
      {uiData &&
        Object.entries(uiData).map(([outerKey, innerData]) =>
          renderCard(outerKey, innerData)
        )}
    </div>
  );
}
