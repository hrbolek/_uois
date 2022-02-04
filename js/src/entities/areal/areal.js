//import MapaSumavska from "../../media/sumak_svg.SVG";
//import MapaCP from "../../media/cernapole_svg.SVG";
//import MapaKOU from "../../media/kounicova_svg.SVG";
//import MapaBAB from "../../media/babak_svg.SVG";

import MapaSumavska from "./media/sumak_svg.svg";
import MapaCP from "./media/cernapole_svg.svg";
import MapaKOU from "./media/kounicova_svg.svg";
import MapaBAB from "./media/babak_svg.svg";


import  Card  from "react-bootstrap/Card";
import  Accordion  from "react-bootstrap/Accordion";
import { Row,Table,Button, Col } from "react-bootstrap";
//import ArealData from "../../media/classrooms2.js";
import ArealData from "./classrooms2";

import { Link, useParams } from "react-router-dom";

import React, { useState, useEffect } from "react";

import { root } from "../index";
import { useQueryGQL, Loading, LoadingError } from "../index";
import { BuildingSmall } from "./building";
import { RoomSmall } from "./room";

//import {ClassroomsListAPI, ClassroomsList} from "../classroom/classroom";

//import { useButtonProps } from "@restart/ui/esm/Button";
import  CardGroup  from "react-bootstrap/CardGroup";

/** @module Areal */

export const arealRoot = root + "/areals"

export const ArealSmall = (props) => {
    return(
            <Link to={arealRoot + `/areal/${props.id}`}>{props.name}{props.children}</Link>
    )
}

export const ArealLargeSUM = () => {
    const arealRoot = root + "areals/5"
        return(
            <Card>
                <Card.Header>
                    <Card.Title>
                        Areál Šumavská - Mapa
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    <map name="sumavska">
                        <area shape="rect" coords="276,613,400,649" href={arealRoot+"/šumák1"} target="_self" alt="Š1"/>
                        <area shape="rect" coords="265,442,329,483" href={arealRoot+"/šumák3"} target="_self" alt="Š3"/>
                        <area shape="rect" coords="193,437,250,487" href={arealRoot+"/šumák4"} target="_self" alt="Š4"/>
                        <area shape="poly" coords="102,422,102,488,185,488,185,445,162,445,162,465,129,465,129,423,103,423" href={arealRoot+"/asiŠ5-zakroucenabudova"} target="_self" alt="zakroucenaBudovaAsiŠ5" />
                        <area shape="rect" coords="97,378,141,415" href={arealRoot+"/šumák5A"} target="_self" alt="Š5A"/>
                        <area shape="rect" coords="97,169,143,253" href={arealRoot+"/šumák5B"} target="_self" alt="Š5B"/>
                        <area shape="rect" coords="97,88,220,143" href={arealRoot+"/šumák6"} target="_self" alt="Š6"/>
                        <area shape="rect" coords="284,88,419,141" href={arealRoot+"/šumák8"} target="_self" alt="Š8"/>
                        <area shape="rect" coords="359,160,419,287" href={arealRoot+"/šumák9"} target="_self" alt="Š9"/>
                        <area shape="rect" coords="359,288,419,404" href={arealRoot+"/šumák9A"} target="_self" alt="Š9A"/>
                    </map>
                    <img useMap="#sumavska" src={MapaSumavska} alt="mapa Sumavska" />              
                </Card.Body>           
            </Card>
        )

}

export const ArealLargeCP = () => {
    const arealRoot = root + "areals/2"
    return(
        <div>

        <div>
            <map name="cernapole">
                <area shape="rect" coords="276,613,400,649" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="265,442,329,483" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="193,437,250,487" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="poly" coords="102,422,102,488,185,488,185,445,162,445,162,465,129,465,129,423,103,423" href={arealRoot+"/..."} target="_self" alt="." />
            </map>
            <img usemap="#cernapole" src={MapaCP} alt="mapa Cerna Pole" />              

        </div>

        </div>
    )

}

export const ArealLargeKOU = () => {
const arealRoot = root + "areals/7"
    return(
        <div>    
    
        <div>
            <map name="kounicova">
                <area shape="rect" coords="276,613,400,649" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="265,442,329,483" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="193,437,250,487" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="poly" coords="102,422,102,488,185,488,185,445,162,445,162,465,129,465,129,423,103,423" href={arealRoot+"/..."} target="_self" alt="." />
            </map>
            <img usemap="#kounicova" src={MapaKOU} alt="mapa Kounicova a Soudni" />              
        </div>
    
        </div>
    )
    
}

export const ArealLargeBAB = () => {
const arealRoot = root + "areals/6"
    return(
        <div>        
        
        <div>
            <map name="babak">
                <area shape="rect" coords="276,613,400,649" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="265,442,329,483" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="rect" coords="193,437,250,487" href={arealRoot+"/..."} target="_self" alt="."/>
                <area shape="poly" coords="102,422,102,488,185,488,185,445,162,445,162,465,129,465,129,423,103,423" href={arealRoot+"/..."} target="_self" alt="." />
            </map>
            <img usemap="#babak" src={MapaBAB} alt="mapa Jana Babaka" />              
        
        </div>
        
        </div>
    )
        
}

//---------------------------------Nové, správné provedení pomocí FETCH (GraphQL)-----------------------------

const tableStyle = {
    color: '#333333',
    width: '70%',
    border: '1px solid black',
    'border-collapse': 'collapse',
        
    //'background-color': '#CCCCCC',
    };




export const ArealLarge = (props) => {

        return (
            <Card>
                <Card.Header>
                    <Card.Title>
                    <ArealSmall {...props}></ArealSmall>
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col md={8} xs={12}>
                            <ArealLargeSUM />
                        </Col>
                        <Col md={4} xs={12}>
                            <BuildingsCondition {...props} />
                        </Col>
                    </Row>
                    
                </Card.Body>
            </Card>
        
        )
}


export const BuildingMulti = (props) => {
    let BuildingComponent = BuildingMedium;
    if (props.as) {
        BuildingComponent = props.as
    }

    let buldingsComponents = props.buildings.map((building, index) => <BuildingComponent key={index} {...building} />)
    return (
        <>
            {buldingsComponents}
        </>
    )

}

export const ArealMedium = (props) => {

    //VYŘEŠENO zmizení [0]teho prvku ----> ale je to správně ? ---> NENÍ TO NEJLEPŠÍ, NĚKDE SE OBJEVÍ CHYBA !!!
    // const state ={
    //     'name': props.name,
    //     'id': props.id
    // };
    //console.log("ArealMedium state: ", state)
    //useEffect(()=>{})
    
    //<ArealSmall name={" budovy v arealu - " + props.name} id={props.id}/>
    //<BuildingMulti buildings={props.buildings} />

    return (
        <Card>
            <Card.Header>Název AREÁLU: <b>{props.name}</b> areal id: {props.id}</Card.Header>
            <Card.Body>
            <Card.Title>
               Budovy

            </Card.Title>
            <BuildingMulti buildings={props.buildings} />
            </Card.Body> 
        {/*<Link to={arealRoot + `/${props.code}`}>{props.name}{props.children}</Link>*/}
        </Card>
    )

}


export const BuildingMedium = (props) => {

    //console.log("props code v building je: ", props.code)
    //{JSON.stringify(props.rooms)}
    return(
        <CardGroup>
        <Card>
                <Card.Header><Row><h3>Třídy:</h3></Row><Row>budova id: {props.id}</Row></Card.Header>
                <Card.Body>
                        {props.rooms.map((room, index) => <><RoomSmall {...room} /><br/></>)}
                </Card.Body>
                
        </Card>
        </CardGroup>

    )
}


//Accordion
export const BuildingsCondition = (props) => { 
    return (
        <Card>
            <Card.Header>
                <Card.Title>Budovy</Card.Title>
            </Card.Header>
            <Card.Body>
                <Accordion>
                    {props.buildings.map((building, index) => (
                        <Accordion.Item eventKey={index}>
                            <Accordion.Header>
                                <BuildingSmall {...building} />
                            </Accordion.Header>
                            <Accordion.Body>
                                {JSON.stringify(building)}
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a page with data representing an areal, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const ArealLargeStoryBook = (props) => {
    const extraProps = {
        "id": "1",
        "name": "Kasárna Šumavská",
        "buildings": [
          { "id": "1", "name": "Jídelna",
            "rooms": [
              { "id": "1", "name": "Jídelna / 1" },
              { "id": "2", "name": "Jídelna / 2" },
              { "id": "3", "name": "Jídelna / 3" },
              { "id": "4", "name": "Jídelna / 4" },
              { "id": "5", "name": "Jídelna / 5" },
              { "id": "6", "name": "Jídelna / 6" },
              { "id": "7", "name": "Jídelna / 7" },
            ]
          },
          { "id": "2", "name": "Katedra Informatiky",
            "rooms": [
              { "id": "13", "name": "Katedra Informatiky / 1" },
              { "id": "14", "name": "Katedra Informatiky / 2" },
              { "id": "15", "name": "Katedra Informatiky / 3" },
              { "id": "16", "name": "Katedra Informatiky / 4" },
              { "id": "17", "name": "Katedra Informatiky / 5" },
              { "id": "18", "name": "Katedra Informatiky / 6" },
            ]
          },
          { "id": "3", "name": "Katedra matematiky",
            "rooms": [
              { "id": "37", "name": "Katedra matematiky / 1" },
              { "id": "38", "name": "Katedra matematiky / 2" },
              { "id": "39", "name": "Katedra matematiky / 3" },
              { "id": "40", "name": "Katedra matematiky / 4" },
              { "id": "41", "name": "Katedra matematiky / 5" },

            ]
          }
        ]
      }
    return (
        <ArealLarge {...extraProps} {...props} />
    )
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const ArealLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
                query {
                    areal: area(id: ${id}) {
                      id
                      name
                      buildings {
                        id
                        name
                        rooms {
                          id
                          name
                        }
                      }
                    }
                  }
            `
        }),
    })

/**
 * Fetch the data from API endpoint and renders a page representing a Areal
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = ArealLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = ArealLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const ArealFetching = (props) => {

    const Visualizer = props.as || ArealLargeStoryBook;
    const queryFunc = props.with || ArealLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.areal, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Areál {props.id}</Loading>
    }
}

export const ArealPage = (props) => {
    const { id } = useParams();

    return <ArealFetching {...props} id={id} />;

}