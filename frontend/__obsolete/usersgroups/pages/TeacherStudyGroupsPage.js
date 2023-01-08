import { useParams } from 'react-router-dom';

import { Fetching } from 'generals/components/Fetching'
import { LeftFixedMenu, LeftFloatMenu } from 'generals/components/LeftMenu'

import { TeacherLarge } from 'usersgroups/components/TeacherLarge'
import { TeacherStudyGroups } from 'usersgroups/components/TeacherStudyGroups'
import { TeacherMenu } from 'usersgroups/components/TeacherMenu'
import { TeacherLargeQuery } from 'usersgroups/queries/teacher'
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';


export const TeacherStudyGroupsPageComponent = (props) => {
    return (
        <Container fluid >
        <div className="row flex-nowrap">
            <LeftFloatMenu>
                <TeacherMenu {...props}/>
            </LeftFloatMenu>   
            <LeftFixedMenu>
                <TeacherMenu {...props}/>
            </LeftFixedMenu>            
            <Col className="py-3">
                <TeacherStudyGroups {...props} />
            </Col>
        </div>
    </Container>
    )
}

export const TeacherStudyGroupsPage = (props) => {
    const { id, pageType } = useParams();
/*
        Visualiser: UniversityLarge,
        query: UniversityLargeQuery,
        selector: json => json.data.groupById

*/
    return (
        
        <Fetching id={id} Visualiser={TeacherStudyGroupsPageComponent} selector={json => json.data.userById} query={TeacherLargeQuery}/>
        
    )
}