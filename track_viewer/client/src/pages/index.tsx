// import BboxDrawer from "../components/bbox_drawer";
// import TemporalPlot  from "../components/plot";
import { useEffect, useState } from "react";
// import InputSelector from "../components/input_selector";
// import { flask_url } from "../lib/utils";
import { Videoset,defaultVideoset } from "@/lib/ServerData";
import VideosetSelector from "@/components/data_selection";
import { flask_url } from "@/lib/utils";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';



export default function Home() {
  const [videoset, setVideoset] = useState<Videoset>(defaultVideoset);

  useEffect(() => {
    fetch(flask_url + '/load_ux_state')
    .then(response => response.json())
    .then(data => {
      setVideoset(new Videoset(data));
    })
    .catch(error => {
      console.error("Error loading videoset data:", error);
    });
  }, []);


  useEffect(() => {
  const saveVideosetData = async () => {
      try {
        await axios.post(flask_url+"/save_ux_state", videoset);
        console.log("Videoset data saved successfully!");
      } catch (error) {
        console.error("Error saving videoset data:", error);
      }
    };

    saveVideosetData();
  }, [videoset]);
  return <>
    <VideosetSelector videoset={videoset} SetVideoset={setVideoset}/>
  </>
}

