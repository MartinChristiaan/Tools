import React, { Component } from "react";
import dynamic from "next/dynamic";

const Chart = dynamic(
  () => {
    return import("react-apexcharts");
  },
  { ssr: false }
);

class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      options: {
        chart: {
          id: "basic-scatter",
          events: {
            click: (event, chartContext, config) => {
              console.log(event, chartContext, config);
            },
          },
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
        },
      },
      series: [
        {
          name: "data1",
          data: [0,1,2,3,4,5,6,7,8]        
        },
      ],
    };
  }

  onclick(c) {
    console.log(c);
  }

  render() {
    return (
      <div className="app">
        <div className="row">
          <div className="scatter-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type="scatter"
              width="500"
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Home;

