export const LeftFixedMenu = (props) => {
    return (
        <div className="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark" style={{'position': 'fixed', 'top': 0, 'zIndex': 1030}}>
            <div className="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
                {props.children}
            </div>
        </div>      
    )
}

export const LeftFloatMenu = (props) => {
    return (
        <div className="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark">
            <div className="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
                {props.children}
            </div>
        </div>      
    )
}