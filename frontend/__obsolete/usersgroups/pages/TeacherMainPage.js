import { useParams } from 'react-router-dom';

import { Fetching } from 'generals/components/Fetching'
import { LeftFixedMenu, LeftFloatMenu } from 'generals/components/LeftMenu'
import { TeacherLarge, TeacherPersonals } from 'usersgroups/components/TeacherLarge'
import { TeacherMenu } from 'usersgroups/components/TeacherMenu'
import { TeacherLargeQuery } from 'usersgroups/queries/teacher'
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';

import { TeacherGrantPageComponent } from 'usersgroups/pages/TeacherGrantPage'
import { TeacherMessagesPageComponent } from 'usersgroups/pages/TeacherMessagesPage'
import { TeacherStudyGroupsPageComponent } from 'usersgroups/pages/TeacherStudyGroupsPage'
import { TeacherSubjectsPageComponent } from 'usersgroups/pages/TeacherSubjectsPage'
import { TeacherSupervisorPageComponent } from 'usersgroups/pages/TeacherSupervisorPage'
import { TeacherTasksPageComponent } from 'usersgroups/pages/TeacherTasksPage'
import { TeacherTimeTablePageComponent } from 'usersgroups/pages/TeacherTimeTablePage'

import { TeacherGrant } from 'usersgroups/components/TeacherGrant'
import { TeacherMessages } from 'usersgroups/components/TeacherMessages'
import { TeacherStudyGroups } from 'usersgroups/components/TeacherStudyGroups'
import { TeacherSupervisor } from 'usersgroups/components/TeacherSupervisor'
import { TeacherTimeTable } from 'usersgroups/components/TeacherTimeTable'

import { SearchSmall } from 'search/components/search'

export const TeacherMainPageComponent = (props) => {
    const { user } = props
    return (
        <Container fluid >
        <div className="row flex-nowrap">
            <LeftFixedMenu>
                <TeacherMenu {...props}/>
            </LeftFixedMenu>            
            <LeftFloatMenu>
                <TeacherMenu {...props}/>
            </LeftFloatMenu>   
            <Col className="py-3">
                <TeacherLarge {...props} />
            </Col>
        </div>
    </Container>
    )
}


const Visualisers = [
    {'type': 'grant', 'visualiser': TeacherGrantPageComponent },
    {'type': 'timetable', 'visualiser': TeacherTimeTablePageComponent },
    {'type': 'subjects', 'visualiser': TeacherSubjectsPageComponent },
    {'type': 'groups', 'visualiser': TeacherStudyGroupsPageComponent },
    {'type': 'supervisor', 'visualiser': TeacherSupervisorPageComponent },
    {'type': 'tasks', 'visualiser': TeacherTasksPageComponent },
    {'type': 'requests', 'visualiser': TeacherMessagesPageComponent },


    

]

export const TeacherMainPage = (props) => {
    const { id, pageType } = useParams();
/*
        Visualiser: UniversityLarge,
        query: UniversityLargeQuery,
        selector: json => json.data.groupById

*/
    //console.log(pageType)
    const VisualiserRow = Visualisers.find( item => item.type == pageType)
    //console.log(VisualiserRow)
    //const Visualiser = VisualiserRow?.visualiser ||TeacherMainPageComponent
    const Visualiser = TeacherFullPageComponent
    return (
        <Fetching id={id} Visualiser={Visualiser} selector={json => json.data.userById} query={TeacherLargeQuery} />
    )
}

/*
TeacherGrant
TeacherMessages
TeacherStudyGroups
TeacherSupervisor
TeacherTimeTable
*/
export const TeacherTopMenuTemplate = (props) => {
    return (
        <nav id="navbar-example2" className="navbar bg-light px-3 mb-3">
            <a className="navbar-brand" href="#">Navbar</a>
            <ul className="nav nav-pills">
                <li className="nav-item">
                <a className="nav-link" href="#scrollspyHeading1">First</a>
                </li>
                <li className="nav-item">
                <a className="nav-link" href="#scrollspyHeading2">Second</a>
                </li>
                <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">Dropdown</a>
                <ul className="dropdown-menu">
                    <li><a className="dropdown-item" href="#scrollspyHeading3">Third</a></li>
                    <li><a className="dropdown-item" href="#scrollspyHeading4">Fourth</a></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><a className="dropdown-item" href="#scrollspyHeading5">Fifth</a></li>
                </ul>
                </li>
            </ul>
        </nav>
            
    )
}

const FullPageItems = [
    {'id': 'TeacherPersonal', 'label': 'Osobní', 'component': TeacherPersonals },

    {'id': 'TeacherTimeTable', 'label': 'Rozvrh', 'component': TeacherTimeTable},
    {'id': 'TeacherStudyGroups', 'label': 'Skupiny', 'component': TeacherStudyGroups},
    {'id': 'TeacherGrant', 'label': 'Garant', 'component': TeacherGrant},
    {'id': 'TeacherSupervisor', 'label': 'Školitel / vedoucí', 'component': TeacherSupervisor},
]

//            <a className="navbar-brand" href="#">Domů</a>

export const TeacherTopMenu = (props) => {
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


//        <div data-bs-spy="scroll" data-bs-target="#navbar" data-bs-root-margin="0px 0px -40%" data-bs-smooth-scroll="true" className="scrollspy-example bg-light p-3 rounded-2" tabindex="0">

export const TeacherAllParts = (props) => {
    const { user } = props
    return (
        <>
            {FullPageItems.map(
                    (item, index) => {
                        const ItemVisualiser = item.component
                        let result = null
                        if (index === 0) {
                            result =(
                            <div key={item.id} id={item.id} className="container-fluid" style={{"paddingTop": "80px", "paddingBottom": "20px"}}>
                                <ItemVisualiser user={user} />
                            </div>)
                    } else {
                        result =(
                            <div key={item.id} id={item.id} className="container-fluid" style={{"paddingBottom": "20px"}}>
                                <ItemVisualiser user={user} />
                            </div>)

                    }
                    return result
                    }
            )}
        </>
    )

    /*
                                <div key={item.id} id={item.id} className="container-fluid" style={{"padding": "100px 20px;"}}>
                                <ItemVisualiser {...props} />
                            </div>
*/
}

export const TeacherFullPageComponent = (props) => {
    const { user } = props
    return (
        <>
            <TeacherTopMenu user={user} />
            <TeacherAllParts user={user} />
        </>
    )
}