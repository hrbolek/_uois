import { Link, useParams } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";

import Card from "react-bootstrap/Card";

const root = "/ui"

export const FacultySmall = (props) => {
    return (
        <Link to={root + "/groups/faculty/" + (props.id)}>{props.name}</Link>
    )
}

export const FacultyPage = (props) => {
    const { id } = useParams();

    return (
        <>
        Fakulta {JSON.stringify(id)}
        </>
    )
}