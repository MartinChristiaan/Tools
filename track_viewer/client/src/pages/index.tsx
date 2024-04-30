// import BboxDrawer from "../components/bbox_drawer";
// import TemporalPlot  from "../components/plot";
import { useEffect, useState } from "react";
// import InputSelector from "../components/input_selector";
// import { flask_url } from "../lib/utils";
import { Videoset,defaultVideoset } from "@/lib/ServerData";
import VideosetSelector from "@/components/data_selection";


export default function Home() {
  const [videoset, setVideoset] = useState<Videoset>(defaultVideoset);


  return <>
    <VideosetSelector videoset={videoset} SetVideoset={setVideoset}/>
  </>
}
