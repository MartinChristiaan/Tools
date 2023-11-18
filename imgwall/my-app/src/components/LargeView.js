import React from 'react';
import ReactMarkdown from 'react-markdown';

import { Container, Row, Col, Image } from "react-bootstrap";
// const HighlightedObject = {
//   title: 'Example',
//   dtype: 'img_url',
//   content: 'https://example.com/image.jpg',
//   body: '# Example\n\nThis is an example.'
// };
const TitleWithTags = ({ title, tags }) => {
  return (
    <div style={{ display: "flex", alignItems: "center" }}>
      <h3>{title}</h3>
      {tags.map((tag) => (
        <div
          key={tag.title}
          // key={tag}
          style={{
            marginLeft: "10px",
            backgroundColor: tag.color,
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

      ))}
    </div>
  );
};

const LargeView = ({ HighlightedObject}) => {
  // const tags_for_object = tags.filter(x => HighlightedObject.tags.includes(x.title));
     return(<Image
          src={'http://localhost:3333/get_image:' + HighlightedObject.index.toString()}
          style={{
            width: "100%",
            height: "1600px",
            maxWidth: "100%",
            maxHeight: "100%",
            objectFit: "contain",
          }}
        />)
};


export default LargeView;
