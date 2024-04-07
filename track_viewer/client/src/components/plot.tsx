// import { Slider } from '@material-ui/core';

import React, { useEffect } from "react";
import { flask_url } from "../lib/utils";

import dynamic from "next/dynamic";
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export default function TemporalPlot({
  timestamp,
  setTimestamp,
  source,
  camera,
  timestamps,
  groupbys,
  num_elements,
}: {
  timestamp: number;
  setTimestamp: (timestamp: number) => void;
  source: string;
  camera: string;
  timestamps: number[];
  groupbys: string[];
  num_elements: number;
}) {
  const handleClick = (event) => {
    console.log("Clicked on the plot:", event.points[0].x);
    setTimestamp(event.points[0].x);
  };
  const [dataDict, setDataDict] = React.useState({});
  const [maxY, setMaxY] = React.useState(1080);

  useEffect(() => {
    fetch(flask_url + "/plotdata/" + source.replaceAll("/", "DASH"))
      .then((response) => response.json())
      .then((data) => {
        setDataDict(data);
        setTimestamp(data[0]["x"][0]);
        const floats = data[0]["y"].map((y: string) => parseFloat(y));
        setMaxY(Math.max(...floats));
        // console.log(((data['y'])))
      });
  }, [camera, source,groupbys]);

  // console.log(dataDict)

  const handleSliderChange = (event) => {
    console.log("Slider changed:", event);
    setTimestamp(event.target.value);
  };
  if (!dataDict[0] || !dataDict[0]["x"]) {

    return(<></>);
  }

  console.log(dataDict)
  const auxdatas = [
    {
      x: [timestamp, timestamp],
      y: [0, maxY],
      mode: "lines",
      line: {
        color: "red",
        width: 2,
      },
      name: "Vertical Line",
    },
    {
      x: timestamps,
      y: new Array(timestamps.length).fill(0),
      mode: "lines",
      line: {
        color: "black",
        width: 2,
      },
      name: "timestamps",
    },
  ];
  const combined_data = dataDict.concat(auxdatas)
  console.log(combined_data)


  return (
    <>
      (
        <Plot
          data={combined_data}
          layout={{ title: "XT : " + source, width: window.innerWidth/num_elements}}
          config={{ displayModeBar: false }}
          onClick={handleClick}
        />
      )
      {/* {dataDict['x'] && (
        <input
        value={timestamp}
        min={dataDict['x'][0]}
        max={dataDict['x'][dataDict['x'].length - 1]}
        onChange={handleSliderChange}
        aria-labelledby="timestamp-slider"
        type='range'
        // width={typeof window !== 'undefined' ? window.innerWidth : 100}
        />
      )} */}
    </>
  );
}
