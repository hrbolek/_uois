import { useEffect } from "react"
import { Col, Row } from "react-bootstrap"
import { Link, useLoaderData, useNavigate } from "react-router-dom"


const LocalLink = ({group}) => {
    return (
        <Link to={"./" + group.grouptype.nameEn + "/" + group.id}>{group.name}</Link>
    )
}

export const IntroductionPage = ({children}) => {
    console.log("IntroductionPage")
    return (
        <>
        <Link to="./2d9dcd22-a4a2-11ed-b9df-0242ac120003">U</Link>
        {children}
        </>
        
    )
}