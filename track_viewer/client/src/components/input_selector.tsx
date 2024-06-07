//A class to select videoset and camera in the server. use bootstrap-react for styling

import React, { useState, useEffect } from 'react';
import { flask_url } from '../lib/utils';
import { Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Typeahead } from 'react-bootstrap-typeahead'; // ES2015
import 'react-bootstrap-typeahead/css/Typeahead.css';
import { ServerData } from '../lib/ServerData';

export default function InputSelector({serverData, setServerData} : {serverData:ServerData,setServerData:any})
{

	const [selectionsVideoset, setSelectionsVideoset] = useState<Array<string>>([]);
	const [SelectionsCamera, setSelectionsCamera] = useState<Array<string>>([]);
	const [SelectionsSources, setSelectionsSources] = useState<Array<string>>([]);
	const [SelectionsGroupbys, setSelectionsGroupbys] = useState<Array<string>>([]);
	const [SelectionsPlotmode, setSelectionsPlotMode] = useState<Array<string>>([]);
	const [SelectionsColor, setSelectionsColor] = useState<Array<string>>([]);
	const PLOTMODES = ['markers','lines','lines+markers']

	useEffect(() => {
		// Fetch videoset and camera data from the server
		fetch(flask_url + '/videoset')
			.then(response => response.json())
			.then(data => {
				// Handle the response from the server
				console.log('Server data:', data);
				setServerData(new ServerData(data));
			})
			.catch(error => {
				console.error('Error fetching data:', error);
			});
	}, []);

	useEffect(() => {
		handleSelection(selectionsVideoset, serverData.videosets, 'videoset');
	}, [selectionsVideoset]);

	useEffect(() => {
		handleSelection(SelectionsCamera, serverData.cameras, 'camera');
	}, [SelectionsCamera]);

	useEffect(() => {
		handleSelection(SelectionsPlotmode, PLOTMODES, 'plotmode');
	}, [SelectionsPlotmode]);

	useEffect(() => {
		handleSelection(SelectionsColor, serverData.groupbys_options, 'color');
	}, [SelectionsColor]);

	const handleSelection = (selection: Array<string>, options: Array<string>, field: string) => {
		const selectedValue = selection[0];
		console.log('selectedValue:', selectedValue, 'options:', options);
		if (options.includes(selectedValue)) {
			console.log('submitting', field + ':', selectedValue);
			handleSubmit({
				...serverData,
				[field]: selectedValue
			});
		}
	};

	useEffect(() => {
		const sources = SelectionsSources;
		if (Array.isArray(sources) && sources.every(source => serverData.sources.includes(source))) {
			handleSubmit({
				...serverData,
				selected_sources: sources
			});
		}
	}, [SelectionsSources]);

	useEffect(() => {
		const groupbys = SelectionsGroupbys;
		if (Array.isArray(groupbys) && groupbys.every(groupby => serverData.groupbys_options.includes(groupby))) {
			handleSubmit({
				...serverData,
				groupbys: groupbys
			});
		}
	}, [SelectionsGroupbys]);


	const handleSubmit = (new_serverdata:ServerData) => {
		// Submit the selected videoset and camera to the server
		if(new_serverdata.videoset === '' || new_serverdata.camera === ''){
			return;
		}
		console.log('Submitting data:', new_serverdata);

		fetch(flask_url+'/videoset', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(new_serverdata),
		})
			.then(response => response.json())
			.then(data => {
				const new_serverdata = new ServerData(data);
				setServerData(new_serverdata);
			})
			.catch(error => {
				console.error('Error submitting data:', error);
			});
	};
	console.log('singleSelections:', serverData.videoset);
	if (serverData === undefined){
		return(<></>);
	}

	return (
	<>
	  <Form.Group>
		<Form.Label>Data Selection</Form.Label>
		<div style={{ display: 'flex' }}>
		  <div style={{ flex: 1 }}>
			<Form.Label>Videoset</Form.Label>
			<Typeahead
			  id="basic-typeahead-videoset"
			  labelKey="Videoset"
			  onChange={setSelectionsVideoset}
			  options={serverData.videosets}
			  placeholder={serverData.videoset}
			  selected={selectionsVideoset}
			/>
		  </div>
		  <div style={{ flex: 1 }}>
			<Form.Label>Camera</Form.Label>
			<Typeahead
			  id="basic-typeahead-camera"
			  labelKey="camera"
			  onChange={setSelectionsCamera}
			  options={serverData.cameras}
			  placeholder={serverData.camera}
			  selected={SelectionsCamera}
			/>
		  </div>
		</div>
	  </Form.Group>
	  <Form.Group>
		<div style={{ display: 'flex' }}>
		  <div style={{ flex: 1 }}>
			<Form.Label>Sources</Form.Label>
			<Typeahead
			  id="basic-typeahead-sources"
			  labelKey="source"
			  multiple
			  onChange={setSelectionsSources}
			  options={serverData.sources}
			  placeholder={serverData.selected_sources}
			  selected={SelectionsSources}
			/>
		  </div>
		  <div style={{ flex: 1 }}>
			<Form.Label>Groupbys</Form.Label>
			<Typeahead
			  id="basic-typeahead-sources"
			  labelKey="groupby"
			  multiple
			  onChange={setSelectionsGroupbys}
			  options={serverData.groupbys_options}
			  placeholder={serverData.groupbys}
			  selected={SelectionsGroupbys}
			/>
		  </div>
		</div>
	  </Form.Group>
	  <Form.Group>
		<div style={{ display: 'flex' }}>
		  <div style={{ flex: 1 }}>
			<Form.Label>Plotmode</Form.Label>
			<Typeahead
			  id="basic-typeahead-sources"
			  labelKey="plotmode"
			  onChange={setSelectionsPlotMode}
			  options={PLOTMODES}
			  placeholder={serverData.plotmode}
			  selected={SelectionsPlotmode}
			/>
		  </div>
		  <div style={{ flex: 1 }}>
			<Form.Label>Color</Form.Label>
			<Typeahead
			  id="basic-typeahead-sources"
			  labelKey="colormode"
			  onChange={setSelectionsColor}
			  options={serverData.groupbys_options}
			  placeholder={serverData.color}
			  selected={SelectionsColor}
			/>
		  </div>
		</div>
	  </Form.Group>
	</>

	);
};

