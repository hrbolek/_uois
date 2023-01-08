import { Loading } from './Loading';
import { LoadingError } from './LoadingError';

import { useQueryGQL } from 'generals/useQuery';

/*
 * @param props.id identification of data entity to be fetched and visualised
 * @param props.query query (async) fetching data from API
 * @param props.responseToJson func for transformation of API response (json) into state data
 * @param props.Visualiser ReactJS component capable to receive selected data and visualise them
 * 
 * if loading is in process, the Loading is displayed
 * if an error occured the LoadingError is displayed
*/
export const Fetching = (props) => {
    const { id, query, Visualiser, selector } = props;
    const [state, error] = useQueryGQL(id, query, selector, [id])
    if (!query || !Visualiser || !selector) {
        return (<LoadingError error={"Bad use of component Fetching. Missing parameters query and/or Visualiser and/or jsonMapper"} />)
    } else {
        if (state != null) {
            return <Visualiser {...state} />
        } else if (error != null) {
            return <LoadingError error={error} />
        } else {
            return <Loading>DataEntity {id}</Loading>
        }
    }
}