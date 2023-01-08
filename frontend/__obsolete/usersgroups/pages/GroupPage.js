import { useParams } from 'react-router-dom';

import { UniversityLarge } from 'usersgroups/components/UniversityLarge';
import { FacultyLarge } from 'usersgroups/components/FacultyLarge';
import { DepartmentLarge} from 'usersgroups/components/DepartmentLarge';

import { UniversityLargeQuery } from 'usersgroups/queries/university';
import { FacultyLargeQuery } from 'usersgroups/queries/faculty';
import { DepartmentLargeQuery } from 'usersgroups/queries/department';

import { Fetching } from 'generals/components/Fetching'

import { SearchSmall } from 'search/components/search'


const FullPageItems = [
    {'id': 'TeacherTimeTable', 'label': 'Rozvrh', 'component': 'TeacherTimeTable'},
    {'id': 'TeacherStudyGroups', 'label': 'Skupiny', 'component': 'TeacherStudyGroups'},
    {'id': 'TeacherGrant', 'label': 'Garant', 'component': 'TeacherGrant'},
    {'id': 'TeacherSupervisor', 'label': 'Školitel / vedoucí', 'component': 'TeacherSupervisor'},
]

//            <a className="navbar-brand" href="#">Domů</a>

export const GroupTopMenu = (props) => {
    return (
        <nav id="navbar" className="navbar navbar-expand-sm fixed-top bg-light navbar-light">
            <div className="container-fluid">
            <ul className="nav nav-pills">
                <li key={0} className="nav-item">
                    <a className="navbar-brand nav-link" href="#">Domů</a>
                </li>
                {FullPageItems.map(
                    (item) =>                 
                        <li key={item.id} className="nav-item">
                            <a className="nav-link" href={"#" + item.id}>{item.label}</a>
                        </li>
    
                )}
            </ul>
            <SearchSmall />
            </div>
        </nav>
            
    )
}



const pageAttributes = {
    university: {
        Visualiser: UniversityLarge,
        query: UniversityLargeQuery,
        selector: json => json.data.groupById
    },
    faculty: {
        Visualiser: FacultyLarge,
        query: FacultyLargeQuery,
        selector: json => json.data.groupById
    },
    department: {
        Visualiser: DepartmentLarge,
        query: DepartmentLargeQuery,
        selector: json => json.data.groupById
    },

}

export const GroupPage = (props) => {
    const { id, pageType } = useParams();

    console.log('pageType: ' + pageType)
    const pageAttrs = pageAttributes[pageType] ? pageAttributes[pageType] : pageAttributes.university
    
    console.log(id)

    return (
        <Fetching {...props} id={id} {...pageAttrs}/>
    )
}