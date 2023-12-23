import React, { useEffect, useRef, useState } from 'react';
import { Container, Row, Col, Image } from "react-bootstrap";
import { HeartFill } from 'react-bootstrap-icons';
import SourceSelectText from './SourceSelectText';
import ImageSelect from './ImageSelect'
import ControlPanel from './ControlPanel';
import {Primary,Secondary,Dark_grey} from "./Color"
import LargeView from './LargeView';

// import {GallerySelect} from "./components/GallerySelect.js"
import api from '../communication';
import GridSelect from './SourceSelect';
import VideoView from './VideoView';

let highlightedObjectState = null
// function Columns({tags, handleWeightChange }) {
function Columns() {
	const [currentlyVisibleItems, setCurrentlyVisibleItems] = useState([]);
	const [HighlightedObject, setHighlightedObject] = useState({"name":"unavailable","index":0,"tags":["Note"]});

	function onKeyDown(e) {
		if (e.key == 'q') {
			api.updateImages().then(x=>(setCurrentlyVisibleItems(x.data)))
		}
		// if (e.key=='f'){
		// 	api.setFavorite(highlightedObjectState).then(x=>(setCurrentlyVisibleItems(x.data)))
		// }
		// if (e.key == 'c'){
		// 	setControlVisible((cur_state) => !cur_state)
		// }

	}

	useEffect(() => {
		document.body.addEventListener('keydown', onKeyDown);
	}, []);

	useEffect(() => {
		api.getItems().then(x=>setCurrentlyVisibleItems(x.data))

	}, []);

	const handleHover = (object) => {
		highlightedObjectState = object
		setHighlightedObject(object);
	};
	const handlePreviewClick = (source) => {
		// setSelectedGallery(currentlyVisibleItems[gallery_index])
		// console.log(gallery_index)
		console.log('requesting index',source.index)
		api.getImageGallery(source.index).then(x=>setCurrentlyVisibleItems(x.data))
	}
	let image_grid = null

	// image_grid = (<SourceSelectText sources={currentlyVisibleItems} onImageHover={handleHover} onClick={handlePreviewClick}></SourceSelectText>)
	image_grid = (<GridSelect items={currentlyVisibleItems} onImageHover={handleHover} onClick={handlePreviewClick} />)
	let control_panel = null
	// if (controlVisible){
	// 	control_panel =
	// 			<Col md={1}>
	// 				<ControlPanel tags={tags} onWeightChange={handleWeightChange} />
	// 			</Col>
	// }
	let view = null
	view = <LargeView HighlightedObject={HighlightedObject} />


	// console.log(Primary,Secondary)

					// <div style={{ position: "absolute", top: 0, right: 0, padding: "0.5rem" }}>
					// 	<HeartFill color="pink" size={80} />
					// </div>
	// console.log(highlightedImage)
	return (
		<Container fluid style={{ "justifyContent": "center","color":Primary}}>
			<Row>
				<Col md={3}>
					{image_grid}
				</Col>
				<Col md={9} style={{"justifyContent": "center", "alignItems": "center"}}>
					{view}
				</Col>
			</Row>
		</Container>
	);
}

export default Columns;
