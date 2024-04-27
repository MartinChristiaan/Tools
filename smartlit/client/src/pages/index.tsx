import React, { useState } from "react";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

const Home = () => {
  const xdata=[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
  const [series, setSeries] = useState([
    {
      name: "data1",
      data: [0, 1, 2, 3, 4, 5, 6, 7, 8],
    },
  ]);
  const [options, setOptions] = useState({
    chart: {
      id: "basic-line",
      events: {
        click: (event, chartContext, config) => {
          const clickedX = xdata[config.dataPointIndex];
          const updatedOptions = {
            ...options,
            annotations: {
              xaxis: [
                {
                  x: clickedX,
                  borderColor: "#000",
                },
              ],
            },
          };
          setOptions(updatedOptions);
        },
      },
    },
    xaxis: {
      categories: xdata,
    },
  });



  return (
    <div className="app">
      <div className="row">
        <div className="line-chart">
          <Chart options={options} series={series} type="line" width="500" />
        </div>
      </div>
    </div>
  );
};

export default Home;
