import {
    BrowserRouter as Router, Routes, Route,
    Outlet, Link, useMatch, useParams
  } from "react-router-dom";

import { DepartmentLargeStoryBook, DepartmentLargeQuery } from './department';
import { UniversityLarge, UniversityLargeQuery } from './university';
import { ImportPage } from './ugimporter';
import { Fetching } from '../../helpers/index';

export const GroupRoute = (props) => {
    return (
        <Route path={"groups/"} element={<GroupPage />}>
            <Route path={`:pageType/:id`} element={<GroupPage />} />
            <Route path={`:id`} element={<GroupPage />} />
        </Route>
    )
}

const pageTypes = {
    department: DepartmentLargeStoryBook
}

const pageQueries = {
    department: DepartmentLargeQuery
}

const pageAttributes = {
    university: {
        Visualiser: UniversityLarge,
        query: UniversityLargeQuery,
        selector: json => json.data.groupById
    },
    department: {
        Visualiser: DepartmentLargeStoryBook,
        query: DepartmentLargeQuery,
        selector: json => json.data.groupById
    },

}

export const GroupPage = (props) => {
    const { id, pageType } = useParams();

    console.log('pageType: ' + pageType)
    const pageAttrs = pageAttributes[pageType] ? pageAttributes[pageType] : pageAttributes.university
    
    console.log(id)

    if (!id) {
        return (
            <ImportPage />
        )
    } else {
        return (
            <Fetching {...props} id={id} {...pageAttrs}/>
        )       
    }
}