import React, { useState, useRef, useEffect, KeyboardEvent } from "react";
import { get_canvs_position } from "../lib/utils";
import { flask_url } from "../lib/utils";

export class Detection {
  constructor(
    public bbox_x: number,
    public bbox_y: number,
    public bbox_w: number,
    public bbox_h: number,
    public class_id: number,
    public label: string,
    public timestamp: number,
    public confidence: number = 2,
    public real_detection: number = 1,
    public track_id: number = 99,
    public n: number = 1,
    public postproc: string = "None"
  ) {}
}

class ZoomParameters {
  constructor(
    public basezoom: number,
	public xpadding : number,
    public zoom: number,
    public x_offset: number,
    public y_offset: number
  ) {}

  combined_zoom() {
    return this.basezoom * this.zoom;
  }

  create_zoomed_annotation(rect: Detection) {
    const bbox_x =
      (rect.bbox_x - this.x_offset / this.basezoom) * this.combined_zoom() + this.xpadding;
    const bbox_y =
      (rect.bbox_y - this.y_offset / this.basezoom) * this.combined_zoom();
    const bbow_w = rect.bbox_w * this.combined_zoom();
    const bbox_h = rect.bbox_h * this.combined_zoom();
    return new Detection(
      bbox_x,
      bbox_y,
      bbow_w,
      bbox_h,
      rect.class_id,
      rect.label,
      rect.timestamp,
      rect.confidence,
      rect.real_detection,
      rect.track_id,
      rect.n,
      rect.postproc
    );
  }

  compensate_annotation_for_zoom(rect: Detection) {
    const bbox_x = (rect.bbox_x-this.xpadding) / this.combined_zoom() + this.x_offset;
    const bbox_y = rect.bbox_y / this.combined_zoom() + this.y_offset;
    const bbow_w = rect.bbox_w / this.combined_zoom();
    const bbox_h = rect.bbox_h / this.combined_zoom();
    return new Detection(
      bbox_x,
      bbox_y,
      bbow_w,
      bbox_h,
      rect.class_id,
      rect.label,
      rect.timestamp,
      rect.confidence,
      rect.real_detection,
      rect.track_id,
      rect.n,
      rect.postproc
    );
  }

  draw_zoomed_image(ctx: CanvasRenderingContext2D, img: HTMLImageElement) {
    // console.log('drawing image',this.combined_zoom())
    ctx.drawImage(
      img,
      -this.x_offset * this.zoom + this.xpadding,
      -this.y_offset * this.zoom,
      img.width * this.combined_zoom(),
      img.height * this.combined_zoom()
    ); // Draw the image at coordinates (0, 0)
  }
}

export default function BboxDrawer({
  timestamp,
  source,
}: {
  timestamp: number;
  source: string;
}) {
  const [rectangles, setRectangles] = useState<Detection[]>([]);
  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const [startPosition, setStartPosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });
  const [currentPosition, setCurrentPosition] = useState<{
    x: number;
    y: number;
  }>({ x: 0, y: 0 });
  const [zoom, setZoom] = useState<ZoomParameters>(
    new ZoomParameters(1, 0,1, 0, 0)
  );
  const [img, setImg] = useState<HTMLImageElement>();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // console.log('bboxdrawer, drawing at timestamp / source',timestamp,source,rectangles)

  useEffect(() => {
    fetch(
      flask_url +
        "/detections/" +
        source.replaceAll("/", "DASH") +
        "SPLIT" +
        timestamp.toString()
    )
      .then((response) => response.json())
      .then((data) => {
        setRectangles(data);
        console.log("Fetched rectangles:", data);
      })
      .catch((error) => {
        console.error("Error fetching rectangles:", error);
      });
  }, [timestamp]);

  useEffect(() => {
    const canvas = canvasRef.current!;
    function handleMouseDown(event: MouseEvent) {
      const { x, y } = get_canvs_position(canvas, event);
      if (event.button === 2) {
        const rect = rectangles.find((rect) => {
          return (
            x >= rect.bbox_x &&
            x <= rect.bbox_x + rect.bbox_w &&
            y >= rect.bbox_y &&
            y <= rect.bbox_y + rect.bbox_h
          );
        });
        if (rect) {
          setRectangles(rectangles.filter((r) => r !== rect));
        }
        return;
      }

      setIsDrawing(true);
      setStartPosition({ x, y });
      setCurrentPosition({ x, y });
      const rect = new Detection(x, y, 0, 0, 0, "Object", timestamp);
      setRectangles([...rectangles, zoom.compensate_annotation_for_zoom(rect)]);
    }

    function handleMouseMove(event: MouseEvent) {
      if (!canvas) return; // Check if canvasRef is null
      if (!isDrawing) return;
      const { x, y } = get_canvs_position(canvasRef.current, event);
      setCurrentPosition({ x, y });
      const rect = rectangles.pop()!;
      rect.bbox_h = (y - startPosition.y) / zoom.zoom;
      rect.bbox_w = (x - startPosition.x) / zoom.zoom;
      setRectangles([...rectangles, rect]);
    }

    function handleMouseUp(event: MouseEvent) {
      setIsDrawing(false);
      fetch(flask_url + "/annotations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(rectangles),
      })
        .then((response) => {
          if (response.ok) {
            console.log("Annotations posted successfully");
          } else {
            console.error("Failed to post annotations");
          }
        })
        .catch((error) => {
          console.error("Error posting annotations:", error);
        });
    }

    function handleScroll(event: WheelEvent) {
      event.preventDefault();
      const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1;
      setZoom((prevZoom) => {
          const { x, y } = get_canvs_position(canvas, event);
          const xcomp = (x - prevZoom.xpadding);
          const newZoom = Math.max(1, Math.min(16, prevZoom.zoom * zoomFactor));
          // const xi = prevZoom.x_offset/newZoom + xcomp/newZoom;
          // const yi = prevZoom.y_offset/newZoom + y/newZoom;
          const xi = xcomp
          const yi = y

          console.log(xi,yi)
          const newZoomParams = new ZoomParameters(
          prevZoom.basezoom,
          prevZoom.xpadding,
          newZoom,
          xi - xi / newZoom,
          yi- yi / newZoom
        );
        return newZoomParams;
      });
    }

    canvas.addEventListener("mousedown", handleMouseDown);
    canvas.addEventListener("mousemove", handleMouseMove);
    canvas.addEventListener("mouseup", handleMouseUp);
    canvas.addEventListener("wheel", handleScroll);
    canvas.oncontextmenu = function (e) {
      e.preventDefault();
      e.stopPropagation();
    };

    return () => {
      canvas.removeEventListener("mousedown", handleMouseDown);
      canvas.removeEventListener("mousemove", handleMouseMove);
      canvas.removeEventListener("mouseup", handleMouseUp);
      canvas.removeEventListener("wheel", handleScroll);
    };
  }, [isDrawing, currentPosition, startPosition, rectangles, zoom]);

  useEffect(() => {
	const canvas = canvasRef.current;
	if (!canvas) return;
    const img = new Image();
    (img.src = flask_url + "/frame/" + timestamp), toString(); // Replace 'URL_OF_YOUR_IMAGE' with the actual URL of your image
    img.onload = () => {
      setImg(img);
	  const scaling  = canvas!.height / img.height
	  const xpadding = (canvas!.width - img.width * scaling) / 2
      const new_zoom = new ZoomParameters(
        scaling,
        xpadding,
        zoom.zoom,
        zoom.x_offset,
        zoom.y_offset
      );
      console.log("setting zoom", new_zoom, window.innerHeight);
      setZoom(new_zoom);
    };
  }, [timestamp]);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d")!;

    const zoomed_rectangles = rectangles.map((rect) =>
      zoom.create_zoomed_annotation(rect)
    );
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    if (img) zoom.draw_zoomed_image(ctx, img);
    // Draw rectangles
    zoomed_rectangles.forEach((rect) => {
      ctx.fillStyle = "rgba(0, 0, 0, 0)"; // Set fill style to invisible
      ctx.strokeStyle = "green"; // Set border style to green
      ctx.lineWidth = 3; // Set border width to 3 pixels
      ctx.strokeRect(rect.bbox_x, rect.bbox_y, rect.bbox_w, rect.bbox_h); // Draw border

      // Draw text
      ctx.fillStyle = "green"; // Set text color to green
      ctx.font = "16px Arial"; // Set font size and family
      ctx.fillText(rect.label, rect.bbox_x, rect.bbox_y - 5); // Draw text above rectangle
    });
    // img.src = flask_url + '/frame/' + timestamp,toString(); // Replace 'URL_OF_YOUR_IMAGE' with the actual URL of your image
  }, [rectangles, zoom, img]);
  // if (!img) return <canvas ref={canvasRef} width="100%"  />;

  // <canvas ref={canvasRef} width={window.innerWidth} height={window.innerHeight / 2} style={{ width: '100%', height: '100%' }} />
  const curcanvas = canvasRef.current;
  if (!curcanvas) return <canvas ref={canvasRef} width="100%" />;
  return (
    <canvas
      ref={canvasRef}
      width={
        canvasRef.current!.parentElement!.clientWidth /
        canvasRef.current!.parentElement!.childElementCount
      }
      height={canvasRef.current?.parentElement?.clientHeight}
      style={{ width: "100%", height: "100%" }}
    />
  );
}
