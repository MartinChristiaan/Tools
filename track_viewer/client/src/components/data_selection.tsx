//# uses chackra autocomplete to select videoset camera and detection source

import { Videoset,defaultVideoset,VideosetOption, fetchVideosetOptions } from "@/lib/ServerData";
import { flask_url } from "@/lib/utils";
import { FormControl, FormLabel } from "@chakra-ui/react";
import { AutoComplete, AutoCompleteInput, AutoCompleteItem, AutoCompleteList, AutoCompleteTag } from "@choc-ui/chakra-autocomplete";
import { use, useEffect,useState } from "react";


function AutocompleteBox({ label, value, options, onSelect }: { label: string, value: any, options: string[], onSelect: (value: string) => void }) {
	const autoCompleteOptions = (
		<div>
			<AutoCompleteInput variant="filled" placeholder={value}/>
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
			<AutoComplete openOnFocus onSelectOption={(x) => onSelect(x.item.value)} onChange={vals => console.log(vals)}>
				{autoCompleteOptions}
			</AutoComplete>
		</FormControl>
	);
}

function MultipleAutocompleteBox({ label, value, options, onSelect }: { label: string, value: any, options: string[], onSelect: (value: string[]) => void }) {
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
		if(videoset.detection_paths.length==0 || !detectionOptions.includes(videoset.detection_paths[0])){
			console.log('setting detection path')
			SetVideoset({...videoset,detection_paths:[detectionOptions[0]]})
		}
	}, [videoset.camera]);


	const videoset_names = videosetOptions.map(videoset=>videoset.videoset)
	const cameras = videosetOptions.find(x=>x.videoset==videoset.name)?.cameras || []

	return <>
		<AutocompleteBox label="Videoset" value={videoset.name} options={videoset_names} onSelect={(value: string) => SetVideoset({ ...videoset, name: value })} />
		<AutocompleteBox label="Camera" key={videoset.name} value={videoset.camera} options={cameras} onSelect={(value: string) => SetVideoset({ ...videoset, camera: value })} />
		<MultipleAutocompleteBox label="Detections" key={videoset.name+videoset.camera} value={videoset.detection_paths} options={detectionOptions} onSelect={(value: string[]) => SetVideoset({ ...videoset, detection_paths: value })} />
	</>
}