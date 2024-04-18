import BboxDrawer from "../components/bbox_drawer";
import TemporalPlot  from "../components/plot";
import { useEffect, useState } from "react";
import { ServerData } from "../components/input_selector";
import InputSelector from "../components/input_selector";
import { flask_url } from "../lib/utils";

export default function Home() {
  const [timestamp, setTimestamp] = useState(0);
  const [comment, setComment] = useState("");
  const [serverData, setServerData] = useState<ServerData>(
    new ServerData({
      videoset: "",
      camera: "",
      cameras: [],
      videosets: [],
      sources: [],
      selected_sources: [],
      timestamps: [],
      cached_timestamps: [],
      groupbys: [],
      groupbys_options: [],
      plotmode: "markers",
      color:"",
      comment:""
    })
  );

  const drawers = function handleKeyDown(event: KeyboardEvent) {
    const server_keys = ["d", "a"];
    const key = event.key;
    const current_tindex = serverData.timestamps.indexOf(timestamp);
    if (key === "a") {
      setTimestamp(serverData.timestamps[current_tindex - 1]);
    }
    if (key === "d") {
      setTimestamp(serverData.timestamps[current_tindex + 1]);
    }
    // TODO : does this work?
    if (key === "A") {
      setTimestamp(serverData.timestamps[current_tindex - 100]);
    }
    if (key === "D") {
      setTimestamp(serverData.timestamps[current_tindex + 100]);
    }
  };

  useEffect(() => {
    // // Keyboard event listener to clear rectangles
    // window.addEventListener('keydown', handleKeyDown);
    // return () => {
    //   window.removeEventListener('keydown', handleKeyDown);
    // };
  }, []);
  const handleSave = async () => {
    try {
      const response = await fetch(flask_url + "/save/" + timestamp.toString() + "___" + comment, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        console.log("Save successful");
      } else {
        console.log("Save failed");
      }
    } catch (error) {
      console.log("Error saving data:", error);
    }
  };
  

  //  Add css styling so that drawers are in horizontal flexbox and temproal plots are in vertical flexbox.
  // The entire Component should take up the entire window size
  console.log(serverData);
  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100vw" }}>
      <InputSelector serverData={serverData} setServerData={setServerData} />
      <button className="btn btn-primary" onClick={handleSave}>Save</button>
      <input type="text" value={comment} onChange= {(x) => setComment(x.target.value)}/>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          width: "100vw",
          height: "40vh",
        }}
      >
        {serverData.selected_sources.map((source) => (
          <BboxDrawer timestamp={timestamp} source={source} key={source} />
        ))}
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "row",
          width: "100vw",
          height: "50vh",
        }}
      >
      {serverData.selected_sources &&
        serverData.selected_sources.map((source) => (
          <TemporalPlot
            timestamp={timestamp}
            setTimestamp={setTimestamp}
            source={source}
            camera={serverData.camera}
            timestamps={serverData.timestamps}
            groupbys={serverData.groupbys}
            num_elements={serverData.selected_sources.length}
            key={source}
          />
        ))}
      </div>
    </div>
  );
}
