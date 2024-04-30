//# uses chackra autocomplete to select videoset camera and detection source

import { Videoset,defaultVideoset,VideosetOption, fetchVideosetOptions } from "@/lib/ServerData";
import { flask_url } from "@/lib/utils";
import { FormControl, FormLabel } from "@chakra-ui/react";
import { AutoComplete, AutoCompleteInput, AutoCompleteItem, AutoCompleteList } from "@choc-ui/chakra-autocomplete";
import { use, useEffect,useState } from "react";


function get_autocomplete_box(label:string,value:string,options:string[],onSelect:any){
	return (
	<FormControl w="200">
        <FormLabel>{label}</FormLabel>
        <AutoComplete openOnFocus onSelectOption={(x) => onSelect(x.item.value)}>
          <AutoCompleteInput variant="filled" placeholder={value} />
          <AutoCompleteList>
            {options.map((options, cid) => (
              <AutoCompleteItem
                key={`option-${cid}`}
                value={options}
              >
                {options}
              </AutoCompleteItem>
            ))}
          </AutoCompleteList>
        </AutoComplete>
      </FormControl>
	)
}


export default function VideosetSelector({videoset,SetVideoset}:{videoset:Videoset,SetVideoset:any}){
	const [videosetOptions,setVideosetOptions] = useState<VideosetOption[]>([]);
	useEffect(() => {
		fetchVideosetOptions(setVideosetOptions)
	}, []);

	const videoset_names = videosetOptions.map(videoset=>videoset.videoset)

	return <>
		{get_autocomplete_box('Videoset',videoset.name,videoset_names,(value:string)=>{SetVideoset({...videoset,name:value})})}
	</>
}