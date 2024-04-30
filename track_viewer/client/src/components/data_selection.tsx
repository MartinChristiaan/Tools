//# uses chackra autocomplete to select videoset camera and detection source

import { Videoset,defaultVideoset,VideosetOption, fetchVideosetOptions } from "@/lib/ServerData";
import { flask_url } from "@/lib/utils";
import { use, useEffect,useState } from "react";
export default function VideosetSelector({videoset,SetVideoset}:{videoset:Videoset,SetVideoset:any}){
	const [videosetOptions,setVideosetOptions] = useState<VideosetOption[]>([]);
	useEffect(() => {
		fetchVideosetOptions(setVideosetOptions)
	}, []);
	return <></>
}