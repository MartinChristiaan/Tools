//# uses chackra autocomplete to select videoset camera and detection source

import { Videoset,defaultVideoset,VideosetOption, fetchVideosetOptions } from "@/lib/ServerData";
import { flask_url } from "@/lib/utils";
import { FormControl, FormLabel } from "@chakra-ui/react";
import { AutoComplete, AutoCompleteInput, AutoCompleteItem, AutoCompleteList, AutoCompleteTag } from "@choc-ui/chakra-autocomplete";
import { use, useEffect,useState } from "react";


function get_autocomplete_box(label:string,value:any,options:string[],onSelect:any){
	const [internalValue, setInternalValue] = useState(value);

	const autoCompleteOptions = (
		<div>
				<AutoCompleteInput variant="filled" value={internalValue} onChange={(val:any)=>console.log(val)} />
				<AutoCompleteList>
					{options.map((option, cid) => (
						<AutoCompleteItem
							key={`option-${cid}`}
							value={option}
						>
							{option}
						</AutoCompleteItem>
					))}
				</AutoCompleteList>
			</div>
	);
	return (
		<FormControl w="200">
			<FormLabel>{label}</FormLabel>
			<AutoComplete openOnFocus onSelectOption={(x) => onSelect(x.item.value)}>
				{autoCompleteOptions}
			</AutoComplete>
		</FormControl>
	);

}


function getMultipleAutocompleteBox(label:string,value:any,options:string[],onSelect:any){
	return (
		<FormControl w="200">
			<FormLabel>{label}</FormLabel>
			<AutoComplete openOnFocus multiple onChange={vals => onSelect(vals)} value={value}>
				<AutoCompleteInput variant="filled">
					{({ tags }) =>
						tags.map((tag, tid) => (
							<AutoCompleteTag
								key={tid}
								label={tag.label}
								onRemove={tag.onRemove}
							/>
						))
					}
				</AutoCompleteInput>
				<AutoCompleteList>
					{options.map((option, cid) => (
						<AutoCompleteItem
							key={`option-${cid}`}
							value={option}
							_selected={{ bg: "whiteAlpha.50" }}
							_focus={{ bg: "whiteAlpha.100" }}
						>
							{option}
						</AutoCompleteItem>
					))}
				</AutoCompleteList>
			</AutoComplete>
		</FormControl>
	);
}



// @app.route("/detections_options", methods=["GET"])
// def get_detections_options():
//     videoset = request.args.get("videoset")
//     camera = request.args.get("camera")

//     options = videoset_api.get_detections_options(videoset, camera)
//     return jsonify(options)


export default function VideosetSelector({videoset,SetVideoset}:{videoset:Videoset,SetVideoset:any}){
	const [videosetOptions,setVideosetOptions] = useState<VideosetOption[]>([]);
	const [detectionOptions,setDetectionOptions] = useState<string[]>([]);

	function fetch_detections_options(){
		fetch(flask_url+'/detections_options?videoset='+videoset.name+'&camera='+videoset.camera).then(
			response=>response.json()
		).then(
			data=>setDetectionOptions(data)
		)
	}
	useEffect(() => {
		fetchVideosetOptions(setVideosetOptions)
	}, []);

	useEffect(() => {
		SetVideoset({...videoset,camera:videosetOptions.find(x=>x.videoset==videoset.name)?.cameras[0] || ''})
		console.log('videoset:',videoset)	
	}, [videoset.name]);

	useEffect(() => {
		fetch_detections_options()
	}, [videoset.name,videoset.camera]);


	const videoset_names = videosetOptions.map(videoset=>videoset.videoset)
	const cameras = videosetOptions.find(x=>x.videoset==videoset.name)?.cameras || []

	return <>
		{get_autocomplete_box('Videoset',videoset.name,videoset_names,(value:string)=>{SetVideoset({...videoset,name:value})})}
		{get_autocomplete_box('Camera',videoset.camera,cameras,(value:string)=>{SetVideoset({...videoset,camera:value})})}
		{getMultipleAutocompleteBox('detections',videoset.detection_paths,detectionOptions,(value:string)=>{SetVideoset({...videoset,detection_paths:value})})}
	</>
}