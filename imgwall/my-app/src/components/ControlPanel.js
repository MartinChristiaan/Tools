import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Image } from 'react-bootstrap';
// import './ControlPanel.css'; // import the CSS file
import RangeSlider from 'react-bootstrap-range-slider';

function ControlPanel(props) {
  const handleWeightChange = (e, index) => {
    props.onWeightChange(index, parseInt(e.target.value));
  };
  console.log(props)

  return (
    <div>
      <h2>weight</h2>
      {props.tags.map((tag) => (
        <Form.Group key={tag.title} className="slider-container">
          <div
            key={tag}
            style={{
              marginLeft: "10px",
              backgroundColor: "red",
              color: "white",
              height: "25px",
              borderRadius: "12.5px",
              border: "1px solid white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "0 10px",
            }}
          >
          {tag.title} {tag.icon}
        </div>
          <RangeSlider min="0" max="5" value={tag.weight} onChange={(e) => handleWeightChange(e, tag.title)} />
        </Form.Group>
      ))}
    </div>
  );
}

export default ControlPanel;
