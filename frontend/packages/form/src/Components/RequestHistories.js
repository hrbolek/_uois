export const RequestHistories = ({request}) => {
    const histories = request?.histories || []
    return (
        <>
            {histories.map(
                history => <RequestHistory key={history.id} history={history} />
            )}
        </>
    )
}

export const RequestHistory = ({history}) => {
    return (
        <>
            <hr/>
            {JSON.stringify(history)}
        </>
    )
}
