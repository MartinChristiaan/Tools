
import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { renderImages } from './RenderImages'

const SourceSelectText = ({ sources, onImageHover, onClick}) => {
  return (
    <>
    <h3>SourceSelect</h3>
    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
      {sources.map((source) =>
        <div
          style={{ border: '1px solid black', padding: '10px',width:"100%"}}
          onMouseOver={() => onImageHover(source)}
          onClick={() => onClick(source)}
        >
          <h5>{source.title}</h5>
        </div>
      )}
    </div>

    </>
  );
};

export default SourceSelectText;
