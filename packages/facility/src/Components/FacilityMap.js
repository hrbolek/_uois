import { useCallback, useMemo, useRef, useState } from "react"
import { MapContainer, Marker, Polygon, Popup, TileLayer, useMapEvents } from "react-leaflet"
// import * as LS from 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';


const whiteRectangle = L.divIcon({
    html: `
  <svg
    width="20"
    height="20"
    viewBox="-10 -10 20 20"
    version="1.1"
    preserveAspectRatio="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path d="M -10 -10 v 20 h 20 v -20 h -20" fill="#FFFFFF77" stroke="blue"></path>
  </svg>`,
    className: "",
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });


export const MapViewSettings = ({ onMapZoom, onMapMove }) => {   
    const map = useMapEvents({
        zoomend: (event) => {
            console.log(JSON.stringify(map.getZoom()))
            
        },
        moveend: (event) => {
            console.log(JSON.stringify(map.getCenter()))
            console.log(JSON.stringify(map.getZoom()))
            if (onMapZoom) {
                onMapZoom(map.getZoom())
            }
            if (onMapMove) {
                const mc = map.getCenter()
                onMapMove([mc.lat, mc.lng])
            }
        },
    })
    return null
}


export const DraggableMarker = ({position, onMove, index=0}) => {
    const [draggable, setDraggable] = useState(true)
    const [position_, setPosition] = useState(position)
    const markerRef = useRef(null)
    const eventHandlers = useMemo(
      () => ({
        dragend() {
          const marker = markerRef.current
          if (marker != null) {

            const newPosition = marker.getLatLng()
            //console.log(newPosition)
            setPosition(marker.getLatLng())
            if (onMove) {
                onMove(index, [newPosition.lat, newPosition.lng])
            }
          }
        },
      }),
      [],
    )
    const toggleDraggable = useCallback(() => {
      setDraggable((d) => !d)
    }, [])
  
    return (
      <Marker
        draggable={draggable}
        eventHandlers={eventHandlers}
        position={position_}
        ref={markerRef}
        icon={whiteRectangle}>
        <Popup minWidth={90}>
          <span onClick={toggleDraggable}>
            {draggable
              ? 'Marker is draggable'
              : 'Click here to make marker draggable'}
          </span>
        </Popup>
      </Marker>
    )
  }


export const FacilityMap = ({facility, onMapZoom, onMapMove}) => {
  let mapsetup = {location: [49.21056, 16.61667], zoom: 17}
  if (facility.geolocation) {
      const mapsetup = JSON.parse(facility.geolocation)
  }

  const [mapState, setMapState] = useState(mapsetup)
    const onMove = (index, newPos) => {
        console.log(index, newPos)
        //setMapState(s => ({...s, location: newPos}))
    }
    
    
    let polyline = null
    if (facility.geometry) {
        const pntsJson = JSON.parse(facility.geometry)
        polyline = <Polygon pathOptions={{ color: 'red' }} positions={pntsJson} />
    }
    
    return (
        <>
        <style>
            {`.leaflet-container {
                height: 75vh;
                width: 100%;
            }`}
        </style>
      
    
    <MapContainer center={mapState.location} zoom={mapState.zoom} scrollWheelZoom={true}>
        {/* <MapViewSettings onMapZoom={onMapZoom} onMapMove={onMapMove}/> */}
        <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {polyline}
        
        {/* <DraggableMarker position={mapState.location} onMove={onMove}/> */}
        
    </MapContainer>
    </>
    )
}