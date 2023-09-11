
import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { renderImages } from './RenderImages'


const ItemPreview = ({ item, onImageHover, onClick}) => {
  // console.log(item.thumbnail)
  // const tags_for_object = tags.filter(x => item.tags.includes(x.title));
    return (
        <Image
          src={'http://localhost:3333/get_image:' + item.index.toString()}
          style={{ height: '100%', width: '100%', objectFit: 'cover', verticalAlign: 'middle' }}
        />
    );
  } 

const GridSelect = ({ items, onImageHover, onClick}) => {
  // console.log("tags",tags)
  if(items.length > 0){
    console.log()
  }
  return (
    <>
      <h3>itemselect</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
          {items.map((item, i) => (

            <div style={{ height: '250px', width: '20%', boxSizing: 'border-box', padding: "0px" }} key={i}>
              <div style={{ height: '100%',
                           display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          border:"3px solid white", //+ tags.filter(x => item.tags.includes(x.title))[0].color ,
                          // borderRadius:"5px"
                          }} 
                onMouseOver={() => onImageHover(item)}
                onClick={() => onClick(item)}>
                <ItemPreview item={item} onImageHover={onImageHover} onClick={onClick}  />
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default GridSelect;
