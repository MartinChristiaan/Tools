import React, { useState, useEffect } from "react";
import ReactPlayer from 'react-player/youtube'


const VideoView = ({ HighlightedObject, tags }) => {
    // console.log(HighlightedObject.path)
    return (
          <ReactPlayer
            url={HighlightedObject.path}
            playing={true}
            width={"100%"}
            height={"100%"}
          />)
};

export default VideoView;
