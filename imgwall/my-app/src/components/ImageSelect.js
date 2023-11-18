import React from 'react';
import { Image } from 'react-bootstrap';

import {renderImages} from './RenderImages'
const ImageSelect = ({ gallery, onImageHover, onClick }) => {
  console.log("imggal",gallery)
  return (
    <>
      <h3>ImageSelect</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
       {renderImages(gallery.image_urls,onClick,onImageHover)}
      </div>
    </>
  );
};

export default ImageSelect;
