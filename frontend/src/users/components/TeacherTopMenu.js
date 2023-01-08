
import { SearchSmall } from 'search/components/search'

const FullPageItems = [
    {'id': 'TeacherPersonal', 'label': 'Osobní', 'component': 'TeacherPersonals' },

    {'id': 'TeacherTimeTable', 'label': 'Rozvrh', 'component': 'TeacherTimeTable'},
    {'id': 'TeacherStudyGroups', 'label': 'Skupiny', 'component': 'TeacherStudyGroups'},
    {'id': 'TeacherGrant', 'label': 'Garant', 'component': 'TeacherGrant'},
    {'id': 'TeacherSupervisor', 'label': 'Školitel / vedoucí', 'component': 'TeacherSupervisor'},
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