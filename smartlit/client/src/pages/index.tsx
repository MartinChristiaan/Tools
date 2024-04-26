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

  const renderOptions = (options) => {
    if (Array.isArray(options)) {
      return options.map(option => <option key={option}>{option}</option>);
    } else {
      return null;
    }
  };

  const renderFormElement = (key, data) => {
    switch (data.uimode) {
      case "selectbox":
        return (
          <Form.Group key={key}>
            <Form.Label>{key}</Form.Label>
            <Form.Control as="select" defaultValue={data.value}>
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
              renderFormElement(innerKey, innerData)
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
